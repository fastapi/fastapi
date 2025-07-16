from fastapi import FastAPI, Form, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

def get_user(
    name: str = Form(..., description="The user's name"),
    age: int = Form(..., description="The user's age")
) -> User:
    return User(name=name, age=age)

@app.post("/submit")
def submit(user: User = Depends(get_user)):
    return JSONResponse(content={"name": user.name, "age": user.age})