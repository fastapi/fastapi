from fastapi import FastAPI, Request, route_middleware

app = FastAPI()


# You can define your own middlewares
async def verify_jwt(req: Request):
    if req.query_params.get("token") != "secret":
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token"
        )
    req.scope["user"] = "admin"


def log_route(req: Request):
    print(f"Request to: {req.url.path}")


@app.post("/secure")
@route_middleware(verify_jwt, log_route)
async def secure_route(req: Request, is_true: bool):
    return {"status": "ok", "is_true": is_true, "user": req.scope.get("user")}


@app.post("/open")
async def open_route(is_true: bool):
    return {"status": "open", "is_true": is_true}
