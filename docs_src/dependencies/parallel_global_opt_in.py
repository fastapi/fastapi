from fastapi import FastAPI

app = FastAPI(depends_default_parallelizable=True)
