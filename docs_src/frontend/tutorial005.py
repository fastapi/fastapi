from fastapi import FastAPI

app = FastAPI()

app.frontend("/", directory="dist", fallback=None)
