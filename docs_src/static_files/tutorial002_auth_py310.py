from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import AuthStaticFiles


async def verify_token(request: Request) -> None:
    """Check for a valid Bearer token in the Authorization header."""
    token = request.headers.get("Authorization")
    if token != "Bearer mysecrettoken":
        raise HTTPException(status_code=401, detail="Not authenticated")


app = FastAPI()

# Private files - requires a valid token to access
app.mount(
    "/private",
    AuthStaticFiles(directory="private_files", auth=verify_token),
    name="private",
)
