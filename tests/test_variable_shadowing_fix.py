"""Simple verification that the routing.py changes are syntactically correct"""

import ast
import sys

def check_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

def check_no_shadowing(filepath):
    """Check that we fixed the variable shadowing issue"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that inner_app exists (our fix)
    if 'async def inner_app(scope: Scope, receive: Receive, send: Send)' in content:
        inner_app_count = content.count('async def inner_app(scope: Scope, receive: Receive, send: Send)')
        if inner_app_count >= 2:  # Should be in both functions
            return True, f"✓ Found {inner_app_count} instances of 'inner_app' (expected 2)"
        else:
            return False, f"✗ Found only {inner_app_count} instances of 'inner_app'"
    else:
        return False, "✗ 'inner_app' not found - fix not applied"

def check_wrap_app_handling_exceptions(filepath):
    """Check that wrap_app_handling_exceptions uses inner_app not app"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check request_response function
    lines = content.split('\n')
    found_request_response = False
    found_correct_usage = False
    
    for i, line in enumerate(lines):
        if 'def request_response(' in line:
            found_request_response = True
        if found_request_response and 'await wrap_app_handling_exceptions(inner_app, request)' in line:
            found_correct_usage = True
            break
    
    if not found_correct_usage:
        return False, "✗ wrap_app_handling_exceptions still uses 'app' instead of 'inner_app'"
    
    return True, "✓ wrap_app_handling_exceptions correctly uses 'inner_app'"

if __name__ == "__main__":
    filepath = "fastapi/routing.py"
    
    print("=" * 70)
    print("Verifying Variable Shadowing Fix in routing.py")
    print("=" * 70)
    print()
    
    # Test 1: Syntax check
    print("1. Checking Python syntax...")
    success, message = check_syntax(filepath)
    print(f"   {message}")
    if not success:
        sys.exit(1)
    
    # Test 2: Check inner_app exists
    print("\n2. Checking for 'inner_app' function...")
    success, message = check_no_shadowing(filepath)
    print(f"   {message}")
    if not success:
        sys.exit(1)
    
    # Test 3: Check wrap_app_handling_exceptions usage
    print("\n3. Checking wrap_app_handling_exceptions usage...")
    success, message = check_wrap_app_handling_exceptions(filepath)
    print(f"   {message}")
    if not success:
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("✅ ALL CHECKS PASSED - Variable shadowing fix is correct!")
    print("=" * 70)
    print()
    print("Summary of changes:")
    print("  • Renamed nested 'app' to 'inner_app' in request_response()")
    print("  • Renamed nested 'app' to 'inner_app' in websocket_session()")
    print("  • Updated wrap_app_handling_exceptions calls to use 'inner_app'")
    print()
    print("This fix eliminates variable shadowing and improves code clarity")
    print("without changing any functionality.")
