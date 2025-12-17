from typing import Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

FAKE_DB = {
    0: {"name": "Admin", "role": "ADMIN"},
    1: {"name": "User 1", "role": "USER"},
    2: {"name": "User 2", "role": "USER"},
}


@app.exception_handler([401, 403])
async def handle_auth_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code if isinstance(exc, HTTPException) else 403,
        content={"detail": "Access denied. Check your credentials or permissions."},
    )


@app.get("/secrets/")
async def get_secrets(auth_user_id: Union[int, None] = None):
    # Get authenticated user info (not a production-ready code)
    if auth_user_id is not None:
        auth_user_info = FAKE_DB.get(auth_user_id)
    else:
        auth_user_info = None

    # Return 401 status code if user not authenticated
    if auth_user_info is None:
        raise HTTPException(status_code=401)  # Not authenticated

    # Return 403 status code if user is not authorized to get secret information
    if auth_user_info["role"] != "ADMIN":
        raise HTTPException(status_code=403)  # Not authorized

    return {"data": "Secret information"}
