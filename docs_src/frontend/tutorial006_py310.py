from fastapi import FastAPI

app = FastAPI()

app.frontend("/", directory="dist", check_dir=False)
