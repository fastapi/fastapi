from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


async def dependency(value):
    yield value
    raise HTTPException(status_code=400)


@app.get(
    "/raise-exception-after-yield",
)
async def read_value(value=Depends(dependency, exit_before_response=True)):
    return value
