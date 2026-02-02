#!/usr/bin/env python3
"""
Process raw transcript to extract all messages and generate summaries.
Handles both incremental (Stop event) and final (SessionEnd) processing.
Cross-platform support for Windows, macOS, and Linux.
"""
import json
import sys
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
from claude_code_capture_utils import get_log_file_path, add_ab_metadata, detect_model_lane, get_experiment_root

def read_and_process_raw_transcript(transcript_path):
    """
    Read raw transcript and extract all unique messages.
    Returns deduplicated messages with last occurrence (final state).
    Also extracts thinking blocks as separate entries.
    """
    if not os.path.exists(transcript_path):
        return []
    
    # Track assistant messages by message.id (they have IDs, can have duplicates)
    assistant_messages = {}
    # Track thinking blocks separately (won't be counted in token usage)
    thinking_blocks = {}
    # Track user messages by uuid (they don't have message.id, use uuid)
    user_messages = {}
    
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    event = json.loads(line)
                    event_type = event.get('type')
                    message = event.get('message', {})
                    
                    # Process assistant messages (have message.id)
                    if event_type == 'assistant':
                        msg_id = message.get('id')
                        if msg_id:
                            # Check for thinking blocks in content
                            content = message.get('content', [])
                            if isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict) and item.get('type') == 'thinking':
                                        # Extract thinking block as separate entry
                                        thinking_entry = {
                                            'type': 'assistant_thinking',
                                            'timestamp': event.get('timestamp'),
                                            'message_id': msg_id,
                                            'thinking_content': item.get('thinking', ''),
                                            'session_id': event.get('sessionId'),
                                            'cwd': event.get('cwd')
                                        }
                                        # Use message_id as key (one thinking block per message)
                                        thinking_blocks[msg_id] = thinking_entry
                            
                            # Store/overwrite with last occurrence (streaming)
                            assistant_msg = {
                                'type': event_type,
                                'timestamp': event.get('timestamp'),
                                'message': message,
                                'session_id': event.get('sessionId'),
                                'cwd': event.get('cwd')
                            }
                            
                            # Preserve stop_reason from message if present
                            if message.get('stop_reason'):
                                assistant_msg['stop_reason'] = message['stop_reason']
                            
                            assistant_messages[msg_id] = assistant_msg
                    
                    # Process user messages (use uuid as key, no message.id)
                    elif event_type == 'user':
                        uuid = event.get('uuid')
                        if uuid:
                            user_msg = {
                                'type': event_type,
                                'timestamp': event.get('timestamp'),
                                'message': message,
                                'session_id': event.get('sessionId'),
                                'cwd': event.get('cwd'),
                                'uuid': uuid
                            }
                            
                            # Preserve thinking metadata if present
                            if 'thinkingMetadata' in event:
                                user_msg['thinkingMetadata'] = event['thinkingMetadata']
                            
                            # Preserve isMeta flag if present
                            if event.get('isMeta'):
                                user_msg['isMeta'] = event['isMeta']
                            
                            user_messages[uuid] = user_msg
                        
                except json.JSONDecodeError:
                    continue
                    
    except Exception as e:
        print(f"[ERROR] Reading raw transcript: {e}", file=sys.stderr)
        return []
    
    # Combine all: assistant messages + thinking blocks + user messages
    # Thinking blocks inserted right before their corresponding assistant message
    all_messages = []
    
    # First, add all messages with their thinking blocks properly ordered
    assistant_list = list(assistant_messages.values())
    user_list = list(user_messages.values())
    
    # Combine and sort all by timestamp
    combined = assistant_list + user_list
    combined.sort(key=lambda m: m.get('timestamp', ''))
    
    # Insert thinking blocks right before their parent assistant message
    for msg in combined:
        if msg['type'] == 'assistant':
            msg_id = msg['message'].get('id')
            # If there's a thinking block for this message, insert it first
            if msg_id in thinking_blocks:
                all_messages.append(thinking_blocks[msg_id])
        all_messages.append(msg)
    
    return all_messages

def aggregate_token_usage(messages):
    """Aggregate token usage from all assistant messages.
    Note: assistant_thinking entries are explicitly excluded to avoid double-counting.
    """
    total_usage = {
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_cache_creation_tokens': 0,
        'total_cache_read_tokens': 0,
        'total_ephemeral_5m_tokens': 0,
        'total_ephemeral_1h_tokens': 0,
        'service_tier': None
    }
    
    for msg_data in messages:
        # Only count tokens from 'assistant' type, NOT 'assistant_thinking'
        # Thinking tokens are already included in the parent assistant message's output_tokens
        if msg_data['type'] == 'assistant':
            message = msg_data['message']
            usage = message.get('usage', {})
            
            if usage:
                total_usage['total_input_tokens'] += usage.get('input_tokens', 0)
                total_usage['total_output_tokens'] += usage.get('output_tokens', 0)
                total_usage['total_cache_creation_tokens'] += usage.get('cache_creation_input_tokens', 0)
                total_usage['total_cache_read_tokens'] += usage.get('cache_read_input_tokens', 0)
                
                cache_creation = usage.get('cache_creation', {})
                total_usage['total_ephemeral_5m_tokens'] += cache_creation.get('ephemeral_5m_input_tokens', 0)
                total_usage['total_ephemeral_1h_tokens'] += cache_creation.get('ephemeral_1h_input_tokens', 0)
                
                if usage.get('service_tier'):
                    total_usage['service_tier'] = usage.get('service_tier')
    
    # Add calculated total
    total_usage['total_actual_input_tokens'] = (
        total_usage['total_input_tokens'] + 
        total_usage['total_cache_creation_tokens'] + 
        total_usage['total_cache_read_tokens']
    )
    
    return total_usage

def analyze_tool_calls(messages):
    """Extract tool call metrics from messages."""
    tool_calls = defaultdict(int)
    tool_results = defaultdict(int)
    
    for msg_data in messages:
        # Skip entries without 'message' key (e.g., assistant_thinking)
        if 'message' not in msg_data:
            continue
        message = msg_data['message']
        content = message.get('content', [])
        
        if not isinstance(content, list):
            continue
        
        for item in content:
            if not isinstance(item, dict):
                continue
            
            if item.get('type') == 'tool_use':
                tool_name = item.get('name', 'unknown')
                tool_calls[tool_name] += 1
            
            elif item.get('type') == 'tool_result':
                # Try to infer tool name from context (simplified)
                tool_results['total'] += 1
    
    return {
        'tool_calls_by_type': dict(tool_calls),
        'total_tool_calls': sum(tool_calls.values()),
        'total_tool_results': tool_results.get('total', 0)
    }

def analyze_thinking_usage(messages, transcript_path):
    """Analyze thinking mode usage in messages."""
    thinking_stats = {
        'thinking_enabled_turns': 0,
        'thinking_disabled_turns': 0,
        'assistant_with_thinking_blocks': 0,
        'thinking_levels': defaultdict(int)
    }
    
    # Track which turns had thinking enabled (from user thinkingMetadata)
    for msg_data in messages:
        if msg_data['type'] == 'user' and 'thinkingMetadata' in msg_data:
            metadata = msg_data['thinkingMetadata']
            if not metadata.get('disabled', True):
                thinking_stats['thinking_enabled_turns'] += 1
                level = metadata.get('level', 'none')
                thinking_stats['thinking_levels'][level] += 1
            else:
                thinking_stats['thinking_disabled_turns'] += 1
    
    # Count assistant messages with thinking blocks
    # Check ALL occurrences in raw transcript (not just final deduplicated state)
    assistant_msg_ids_with_thinking = set()
    
    try:
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        if event.get('type') == 'assistant':
                            message = event.get('message', {})
                            msg_id = message.get('id')
                            content = message.get('content', [])
                            
                            if msg_id and isinstance(content, list):
                                # Check if this occurrence has thinking
                                has_thinking = any(
                                    isinstance(item, dict) and item.get('type') == 'thinking'
                                    for item in content
                                )
                                if has_thinking:
                                    assistant_msg_ids_with_thinking.add(msg_id)
                    except:
                        continue
    except Exception:
        pass
    
    thinking_stats['assistant_with_thinking_blocks'] = len(assistant_msg_ids_with_thinking)
    
    return {
        'thinking_enabled_turns': thinking_stats['thinking_enabled_turns'],
        'thinking_disabled_turns': thinking_stats['thinking_disabled_turns'],
        'assistant_with_thinking_blocks': thinking_stats['assistant_with_thinking_blocks'],
        'thinking_levels': dict(thinking_stats['thinking_levels'])
    }

def calculate_git_metrics(cwd, base_commit):
    """Calculate git metrics from diff."""
    try:
        original_cwd = os.getcwd()
        os.chdir(cwd)
        
        if not base_commit:
            os.chdir(original_cwd)
            return {}
        
        # Add untracked files
        excluded_patterns = ['.claude/', '__pycache__/', 'node_modules/', '.mypy_cache/', 
                           '.pytest_cache/', '.DS_Store', '.vscode/', '.idea/']
        
        untracked_result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard'],
            capture_output=True, text=True, timeout=30
        )
        
        if untracked_result.returncode == 0 and untracked_result.stdout.strip():
            untracked_files = [
                f.strip() for f in untracked_result.stdout.strip().split('\n')
                if f.strip() and not any(pattern in f for pattern in excluded_patterns)
            ]
            
            for file in untracked_files:
                subprocess.run(['git', 'add', '-N', file], capture_output=True, timeout=5)
        
        # Calculate numstat
        result = subprocess.run(
            ['git', 'diff', '--numstat', base_commit, '--', '.', 
             ':!.claude', ':!**/.mypy_cache', ':!**/__pycache__', ':!**/.pytest_cache',
             ':!**/.DS_Store', ':!**/node_modules', ':!**/.vscode', ':!**/.idea'],
            capture_output=True, text=True, timeout=30
        )
        
        os.chdir(original_cwd)
        
        if result.returncode != 0:
            return {}
        
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        files_changed = 0
        total_lines_changed = 0
        
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        added = int(parts[0]) if parts[0] != '-' else 0
                        removed = int(parts[1]) if parts[1] != '-' else 0
                        files_changed += 1
                        total_lines_changed += added + removed
                    except ValueError:
                        continue
        
        return {
            "files_changed_count": files_changed,
            "lines_of_code_changed_count": total_lines_changed
        }
        
    except Exception as e:
        print(f"Warning: Could not calculate git metrics: {e}", file=sys.stderr)
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        return {}

def copy_raw_transcript(transcript_path, session_id, cwd):
    """Copy raw transcript to logs folder."""
    try:
        source_path = Path(transcript_path)
        if not source_path.exists():
            print(f"Warning: Raw transcript not found at {source_path}", file=sys.stderr)
            return False
        
        model_lane = detect_model_lane(cwd)
        experiment_root = get_experiment_root(cwd)
        
        if model_lane and experiment_root:
            logs_dir = Path(experiment_root) / "logs" / model_lane
            logs_dir.mkdir(parents=True, exist_ok=True)
            dest_path = logs_dir / f"session_{session_id}_raw.jsonl"
        else:
            project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
            logs_dir = Path(project_dir) / "logs"
            logs_dir.mkdir(exist_ok=True)
            dest_path = logs_dir / f"session_{session_id}_raw.jsonl"
        
        shutil.copy2(source_path, dest_path)
        print(f"[OK] Copied raw transcript to {dest_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Copying raw transcript: {e}", file=sys.stderr)
        return False

def get_base_commit_from_log(log_file):
    """Extract base commit from session_start event."""
    try:
        if not os.path.exists(log_file):
            return None
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        if event.get('type') == 'session_start':
                            git_metadata = event.get('git_metadata', {})
                            return git_metadata.get('base_commit')
                    except json.JSONDecodeError:
                        continue
        return None
    except Exception:
        return None

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: process_transcript.py [incremental|final]", file=sys.stderr)
            sys.exit(1)
        
        mode = sys.argv[1].lower()
        if mode not in ["incremental", "final"]:
            print("Mode must be 'incremental' or 'final'", file=sys.stderr)
            sys.exit(1)
        
        input_data = json.load(sys.stdin)
        
        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")
        cwd = input_data.get("cwd", "")
        
        log_file = get_log_file_path(session_id, cwd)
        
        if mode == "incremental":
            # Stop event: incremental processing (fault tolerance)
            messages = read_and_process_raw_transcript(transcript_path)
            
            if not messages:
                return
            
            # Append all new unique messages to log
            # Track what we've already logged (assistant by msg_id, thinking by msg_id, user by uuid)
            existing_assistant_ids = set()
            existing_thinking_ids = set()
            existing_user_uuids = set()
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            event = json.loads(line)
                            event_type = event.get('type')
                            if event_type == 'assistant':
                                msg = event.get('message', {})
                                if msg.get('id'):
                                    existing_assistant_ids.add(msg['id'])
                            elif event_type == 'assistant_thinking':
                                msg_id = event.get('message_id')
                                if msg_id:
                                    existing_thinking_ids.add(msg_id)
                            elif event_type == 'user':
                                uuid = event.get('uuid')
                                if uuid:
                                    existing_user_uuids.add(uuid)
                        except:
                            continue
            
            # Append new messages
            new_count = 0
            with open(log_file, "a", encoding="utf-8") as f:
                for msg_data in messages:
                    # Check if this is a new message
                    is_new = False
                    if msg_data['type'] == 'assistant':
                        msg_id = msg_data['message'].get('id')
                        if msg_id and msg_id not in existing_assistant_ids:
                            is_new = True
                            existing_assistant_ids.add(msg_id)
                    elif msg_data['type'] == 'assistant_thinking':
                        msg_id = msg_data.get('message_id')
                        if msg_id and msg_id not in existing_thinking_ids:
                            is_new = True
                            existing_thinking_ids.add(msg_id)
                    elif msg_data['type'] == 'user':
                        uuid = msg_data.get('uuid')
                        if uuid and uuid not in existing_user_uuids:
                            is_new = True
                            existing_user_uuids.add(uuid)
                    
                    if is_new:
                        # Add A/B metadata
                        log_entry = add_ab_metadata(msg_data.copy(), cwd)
                        f.write(json.dumps(log_entry) + "\n")
                        new_count += 1
            
            if new_count > 0:
                print(f"[OK] Processed {new_count} new messages (total: {len(messages)} unique)")
                
        elif mode == "final":
            # SessionEnd: complete processing + summary
            
            # Step 1: Copy raw transcript
            copy_raw_transcript(transcript_path, session_id, cwd)
            
            # Step 2: Process complete raw transcript
            messages = read_and_process_raw_transcript(transcript_path)
            
            if not messages:
                print("Warning: No messages found in raw transcript", file=sys.stderr)
                return
            
            # Step 3: REBUILD processed log in perfect chronological order
            # Read existing non-message events (session_start, etc.)
            non_message_events = []
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            event = json.loads(line)
                            # Keep session_start and other non-message events
                            # Exclude assistant, assistant_thinking, and user messages (they come from raw transcript)
                            if event.get('type') not in ['assistant', 'assistant_thinking', 'user']:
                                non_message_events.append(event)
                        except:
                            continue
            
            # Combine all events and sort by timestamp
            session_start = [e for e in non_message_events if e.get('type') == 'session_start']
            other_events = [e for e in non_message_events if e.get('type') != 'session_start']
            
            # Build chronological list: session_start first, then messages sorted by time
            all_events = []
            
            # Add session_start first (if exists)
            if session_start:
                all_events.extend(session_start)
            
            # Add all messages (already sorted by timestamp from read_and_process_raw_transcript)
            # Messages already include thinking blocks inserted before their parent assistant message
            for msg_data in messages:
                all_events.append(add_ab_metadata(msg_data.copy(), cwd))
            
            print(f"[OK] Rebuilding log with {len(all_events)} events in chronological order")
            
            # Step 4: Generate session summary
            usage_totals = aggregate_token_usage(messages)
            tool_metrics = analyze_tool_calls(messages)
            thinking_metrics = analyze_thinking_usage(messages, transcript_path)
            
            # Calculate duration
            timestamps = [
                datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                for msg in messages if msg.get('timestamp')
            ]
            
            total_duration = 0
            if len(timestamps) >= 2:
                duration = max(timestamps) - min(timestamps)
                total_duration = duration.total_seconds()
            
            # Count messages with proper categorization
            # Note: assistant_thinking is NOT counted as a separate message (it's part of assistant message)
            assistant_count = sum(1 for m in messages if m['type'] == 'assistant')
            thinking_count = sum(1 for m in messages if m['type'] == 'assistant_thinking')
            
            # Categorize user messages
            user_prompts = 0
            tool_results = 0
            system_messages = 0
            
            for m in messages:
                if m['type'] == 'user':
                    message_content = m['message'].get('content', '')
                    
                    # Check if it's a system/meta message
                    if m.get('isMeta'):
                        system_messages += 1
                    # Check if it's a tool result
                    elif isinstance(message_content, list):
                        has_tool_result = any(
                            isinstance(item, dict) and item.get('type') == 'tool_result'
                            for item in message_content
                        )
                        if has_tool_result:
                            tool_results += 1
                        else:
                            user_prompts += 1
                    # Check if it's an exit/system command
                    elif isinstance(message_content, str) and (
                        '<command-name>' in message_content or 
                        '<local-command-stdout>' in message_content
                    ):
                        system_messages += 1
                    # Real user prompt (string content, not system)
                    elif isinstance(message_content, str):
                        user_prompts += 1
                    else:
                        user_prompts += 1  # Default to user prompt
            
            total_user_events = user_prompts + tool_results + system_messages
            
            # Calculate actual total messages (excluding thinking blocks as they're not separate messages)
            actual_total_messages = assistant_count + total_user_events
            
            # Get git metrics
            base_commit = get_base_commit_from_log(log_file)
            git_metrics = calculate_git_metrics(cwd, base_commit) if base_commit else {}
            
            # Create session summary
            model_lane = detect_model_lane(cwd)
            
            summary = {
                "type": "session_summary",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id,
                "transcript_path": transcript_path,
                "cwd": cwd,
                "summary_data": {
                    "total_duration_seconds": round(total_duration, 2),
                    "total_messages": actual_total_messages,
                    "assistant_messages": assistant_count,
                    "user_prompts": user_prompts,
                    "user_metrics": {
                        "user_prompts": user_prompts,
                        "tool_results": tool_results,
                        "system_messages": system_messages,
                        "total_user_events": total_user_events
                    },
                    "usage_totals": usage_totals,
                    "tool_metrics": tool_metrics,
                    "thinking_metrics": {
                        **thinking_metrics,
                        "assistant_thinking_blocks_captured": thinking_count
                    },
                    "git_metrics": git_metrics,
                    "files": {
                        "processed_log": f"session_{session_id}.jsonl",
                        "raw_transcript": f"session_{session_id}_raw.jsonl",
                        "git_diff": f"{model_lane}_diff.patch" if model_lane else None
                    },
                    "validation": {
                        "complete": True,
                        "unique_messages_processed": actual_total_messages,
                        "thinking_blocks_extracted": thinking_count
                    }
                }
            }
            
            summary = add_ab_metadata(summary, cwd)
            
            # Add session summary to events
            all_events.append(summary)
            
            # Step 5: Rewrite log file with all events in perfect chronological order
            # Write to temp file first, then rename (atomic)
            temp_log_file = log_file + ".tmp"
            
            with open(temp_log_file, "w", encoding="utf-8") as f:
                for event in all_events:
                    f.write(json.dumps(event) + "\n")
            
            # Atomic rename
            os.replace(temp_log_file, log_file)
            
            print(f"[OK] Rebuilt log with {len(all_events)} events in chronological order")
            print(f"[OK] Generated session summary: {actual_total_messages} messages, {assistant_count} assistant, {user_prompts} user prompts")
            if thinking_count > 0:
                print(f"[OK] Captured {thinking_count} thinking blocks (tokens already included in assistant output)")
            print(f"[OK] User breakdown: {user_prompts} prompts, {tool_results} tool results, {system_messages} system")
            print(f"[OK] Tokens: {usage_totals['total_actual_input_tokens']:,} input, {usage_totals['total_output_tokens']:,} output")
            
    except Exception as e:
        print(f"[ERROR] Processing transcript: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_git_metrics(cwd, base_commit):
    """Calculate git metrics from diff."""
    try:
        original_cwd = os.getcwd()
        os.chdir(cwd)
        
        if not base_commit:
            os.chdir(original_cwd)
            return {}
        
        # Add untracked files
        excluded_patterns = ['.claude/', '__pycache__/', 'node_modules/', '.mypy_cache/', 
                           '.pytest_cache/', '.DS_Store', '.vscode/', '.idea/']
        
        untracked_result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard'],
            capture_output=True, text=True, timeout=30
        )
        
        if untracked_result.returncode == 0 and untracked_result.stdout.strip():
            untracked_files = [
                f.strip() for f in untracked_result.stdout.strip().split('\n')
                if f.strip() and not any(pattern in f for pattern in excluded_patterns)
            ]
            
            for file in untracked_files:
                subprocess.run(['git', 'add', '-N', file], capture_output=True, timeout=5)
        
        # Calculate numstat
        result = subprocess.run(
            ['git', 'diff', '--numstat', base_commit, '--', '.', 
             ':!.claude', ':!**/.mypy_cache', ':!**/__pycache__', ':!**/.pytest_cache',
             ':!**/.DS_Store', ':!**/node_modules', ':!**/.vscode', ':!**/.idea'],
            capture_output=True, text=True, timeout=30
        )
        
        os.chdir(original_cwd)
        
        if result.returncode != 0:
            return {}
        
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        files_changed = 0
        total_lines_changed = 0
        
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        added = int(parts[0]) if parts[0] != '-' else 0
                        removed = int(parts[1]) if parts[1] != '-' else 0
                        files_changed += 1
                        total_lines_changed += added + removed
                    except ValueError:
                        continue
        
        return {
            "files_changed_count": files_changed,
            "lines_of_code_changed_count": total_lines_changed
        }
        
    except Exception as e:
        print(f"Warning: Could not calculate git metrics: {e}", file=sys.stderr)
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        return {}

if __name__ == "__main__":
    main()

