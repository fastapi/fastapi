from typing import Dict

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root() -> Dict[str, str]:
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
