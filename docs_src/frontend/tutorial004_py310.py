from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

router.frontend("/", directory="dist", fallback="index.html")
app.include_router(router, prefix="/app")
