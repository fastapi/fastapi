# manual_test.py
# Run this to see the improved error messages

from fastapi import FastAPI, Depends

print("Testing improved error messages...\n")

def get_user():
    return {"user": "john"}

# Test 1: Called function
print("Test 1: Using Depends(get_user()) - should show helpful error")
try:
    app1 = FastAPI()
    
    @app1.get("/")
    def route1(user = Depends(get_user())):
        return user
    
    print("❌ No error raised (unexpected)")
except TypeError as e:
    print(f"✓ Error caught: {e}\n")

# Test 2: Nested Depends
print("Test 2: Using Depends(Depends(get_user)) - should show nested error")
try:
    app2 = FastAPI()
    
    @app2.get("/")
    def route2(user = Depends(Depends(get_user))):
        return user
    
    print("❌ No error raised (unexpected)")
except TypeError as e:
    print(f"✓ Error caught: {e}\n")

# Test 3: String instead of callable
print("Test 3: Using Depends('not_callable') - should show type error")
try:
    app3 = FastAPI()
    
    @app3.get("/")
    def route3(user = Depends("not_callable")):
        return user
    
    print("❌ No error raised (unexpected)")
except TypeError as e:
    print(f"✓ Error caught: {e}\n")

# Test 4: Correct usage (should work)
print("Test 4: Using Depends(get_user) correctly - should work")
try:
    app4 = FastAPI()
    
    @app4.get("/")
    def route4(user = Depends(get_user)):
        return user
    
    print("✓ Correct usage works! No error raised.\n")
except Exception as e:
    print(f"❌ Unexpected error: {e}\n")

print("All manual tests completed!")