from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@app.get("/items/")
async def read_items(token: str = Security(oauth2_scheme)):
    return {"token": token}
