from fastapi import FastAPI

my_awesome_api = FastAPI()


@my_awesome_api.get("/")
def root():
    return {"message": "Hello World"}
