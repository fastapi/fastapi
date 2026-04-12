#!/usr/bin/env python3
"""Truncate test file to remove stray snapshot data."""

with open('tests/test_include_router_defaults_overrides.py', 'r') as f:
    lines = f.readlines()

# Find test_openapi function
for i, line in enumerate(lines):
    if 'def test_openapi():' in line:
        print(f"Found test_openapi at line {i+1}")
        # Find the end of this function
        for j in range(i+1, len(lines)):
            if lines[j].strip() == 'response.json()':
                print(f"Found response.json() at line {j+1}")
                # Keep up to this line
                new_lines = lines[:j+1]
                
                with open('tests/test_include_router_defaults_overrides.py', 'w') as f:
                    f.writelines(new_lines)
                print(f"Truncated file to {j+1} lines (originally {len(lines)} lines)")
                break
        break
