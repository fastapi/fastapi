# docs_src/index.py
from fastapi import FastAPI
from fastapi.contrib.export.routes import router as export_router
 
app = FastAPI()
 
app.include_router(export_router)
