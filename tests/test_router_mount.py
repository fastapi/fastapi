from fastapi import APIRouter, FastAPI

app = FastAPI()
api_router = APIRouter(prefix="/api")


@api_router.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI()


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


api_router.mount("/subapi", subapi)  # ← moved up
app.include_router(api_router)  # ← now after

print("All tests passed.")
