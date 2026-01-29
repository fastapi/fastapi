import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request
from fastapi.route_middleware import route_middleware, verify_jwt, log_route

app = FastAPI()

@app.post("/secure")
@route_middleware(verify_jwt, log_route)
async def secure_route(req: Request, is_true: bool):
    
    return {"status": "ok", "is_true": is_true,"user":req.user}

@app.post("/open")
async def open_route(is_true: bool):
    return {"status": "open", "is_true": is_true}
