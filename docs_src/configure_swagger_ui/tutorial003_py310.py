from fastapi import FastAPI

app = FastAPI(swagger_ui_parameters={"deepLinking": False})


@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
