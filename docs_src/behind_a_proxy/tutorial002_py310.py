from fastapi import FastAPI, Request

app = FastAPI(root_path="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {
        "message": "Hello World",
        "path": request.scope.get("path"),
        "root_path": request.scope.get("root_path"),
    }
