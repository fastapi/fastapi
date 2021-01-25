from fastapi import Depends


async def dependency(value):
    # do something before
    yield value
    # do something after


@app.get("/dependency")
async def endpoint(value=Depends(dependency, exit_before_response=True)):
    return value
