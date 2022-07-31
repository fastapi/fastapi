from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class ResponseModelA(BaseModel):
    a: str

class ResponseModelB(BaseModel):
    b: str

@app.get("/a", response_model=ResponseModelA)
def get_a_with_response_model_a():
    return ResponseModelA(a="a")

@app.get("/b", response_model=ResponseModelA)
def get_b_with_response_model_a_and_return_model_b() -> ResponseModelB:
    return ResponseModelA(a="a")

@app.get("/c")
def get_c_with_return_type_b() -> ResponseModelB:
    return ResponseModelB(b="b")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)