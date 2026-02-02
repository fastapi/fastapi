#!/usr/bin/env python3
"""
Utility functions for A/B testing hooks.
Cross-platform support for Windows, macOS, and Linux.
"""
import json
import os
from pathlib import Path

def detect_model_lane(cwd):
    """Detect if we're in model_a or model_b directory."""
    path_parts = Path(cwd).parts
    if 'model_a' in path_parts:
        return 'model_a'
    elif 'model_b' in path_parts:
        return 'model_b'
    return None

def get_experiment_root(cwd):
    """Get the experiment root directory (parent of model_a/model_b)."""
    current_path = Path(cwd)
    
    # Check if we're inside a model_a or model_b directory
    # Look for the parent that contains both model_a and model_b
    for parent in [current_path] + list(current_path.parents):
        if (parent / 'model_a').exists() and (parent / 'model_b').exists():
            return str(parent)
        # Also check one level up (in case we're inside the cloned repo)
        parent_up = parent.parent
        if (parent_up / 'model_a').exists() and (parent_up / 'model_b').exists():
            return str(parent_up)
    return None

def read_manifest(experiment_root):
    """Read the manifest.json file to get task_id and model assignments."""
    try:
        manifest_path = os.path.join(experiment_root, 'manifest.json')
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def get_ab_metadata(cwd):
    """Get A/B testing metadata (task_id, model_lane, model_name) from current directory."""
    model_lane = detect_model_lane(cwd)
    experiment_root = get_experiment_root(cwd)
    
    if not model_lane or not experiment_root:
        return {}
    
    manifest = read_manifest(experiment_root)
    
    metadata = {
        "task_id": manifest.get("task_id"),
        "model_lane": model_lane,
        "experiment_root": experiment_root
    }
    
    # Get model name from assignments
    assignments = manifest.get("assignments", {})
    if model_lane in assignments:
        metadata["model_name"] = assignments[model_lane]
    
    return metadata

def get_log_file_path(session_id, cwd):
    """Get the correct log file path for A/B testing (routes to model-specific directory)."""
    model_lane = detect_model_lane(cwd)
    experiment_root = get_experiment_root(cwd)
    
    if model_lane and experiment_root:
        # Route to model-specific logs directory
        logs_dir = os.path.join(experiment_root, "logs", model_lane)
        os.makedirs(logs_dir, exist_ok=True)
        return os.path.join(logs_dir, f"session_{session_id}.jsonl")
    else:
        # Fallback to current behavior
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
        logs_dir = os.path.join(project_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        return os.path.join(logs_dir, f"session_{session_id}.jsonl")

def add_ab_metadata(event, cwd):
    """Add A/B testing metadata to an event."""
    ab_metadata = get_ab_metadata(cwd)
    if ab_metadata:
        for key, value in ab_metadata.items():
            if value is not None:
                event[key] = value
    return event

