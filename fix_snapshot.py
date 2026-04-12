#!/usr/bin/env python3
"""Remove the old snapshot dictionary from test_include_router_defaults_overrides.py"""

import re

# Read the file
with open('tests/test_include_router_defaults_overrides.py', 'r') as f:
    lines = f.readlines()

# Find and remove the old snapshot dictionary
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # If we hit operation_ids.add(op_id), the next non-empty line should be the start of the snapshot dict
    if 'operation_ids.add(op_id)' in line:
        # Skip all lines until we find the closing paren of snapshot()
        i += 1
        brace_count = 0
        while i < len(lines):
            cur_line = lines[i]
            brace_count += cur_line.count('{') - cur_line.count('}')
            
            # Check if this is the closing paren of snapshot()
            if brace_count == 0 and cur_line.strip() == ')':
                i += 1
                break
            i += 1
        continue
    
    i += 1

# Write back
with open('tests/test_include_router_defaults_overrides.py', 'w') as f:
    f.writelines(new_lines)

print("Done! Removed snapshot dictionary")
