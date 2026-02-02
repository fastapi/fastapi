#!/usr/bin/env python3
"""
Hook to capture session start/end events.
Cross-platform support for Windows, macOS, and Linux.
"""
import json
import sys
import os
import subprocess
from datetime import datetime, timezone
from claude_code_capture_utils import get_log_file_path, add_ab_metadata

def get_git_metadata(repo_dir):
    """Get current git commit and branch."""
    try:
        # Get current commit hash
        commit_result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Get current branch
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10
        )

        git_metadata = {
            "base_commit": commit_result.stdout.strip() if commit_result.returncode == 0 else None,
            "branch": branch_result.stdout.strip() if branch_result.returncode == 0 else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if git_metadata["base_commit"]:
            return git_metadata
        else:
            return None

    except Exception as e:
        print(f"Warning: Could not capture git metadata: {e}", file=sys.stderr)
        return None

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: capture_session_event.py [start|end]", file=sys.stderr)
            sys.exit(1)

        event_type = sys.argv[1].lower()
        if event_type not in ["start", "end"]:
            print("Event type must be 'start' or 'end'", file=sys.stderr)
            sys.exit(1)

        input_data = json.load(sys.stdin)

        session_id = input_data.get("session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")
        cwd = input_data.get("cwd", "")

        if event_type == "start":
            # Session start: capture git metadata
            git_metadata = get_git_metadata(cwd)

            log_entry = {
                "type": "session_start",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id,
                "transcript_path": transcript_path,
                "cwd": cwd,
                "git_metadata": git_metadata
            }

            log_entry = add_ab_metadata(log_entry, cwd)

            if git_metadata:
                print(f"[OK] Captured git metadata: {git_metadata['base_commit'][:8]} on {git_metadata['branch']}")

            # Write session_start event
            log_file = get_log_file_path(session_id, cwd)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")

        elif event_type == "end":
            # Session end: log the event
            log_entry = {
                "type": "session_end",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id,
                "transcript_path": transcript_path,
                "cwd": cwd,
                "reason": input_data.get("reason", "")
            }

            log_entry = add_ab_metadata(log_entry, cwd)

            # Write session_end event
            log_file = get_log_file_path(session_id, cwd)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        print(f"[ERROR] Session {event_type}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
