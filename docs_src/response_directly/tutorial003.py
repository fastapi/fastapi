from fastapi import BackgroundTasks, FastAPI
from starlette.responses import JSONResponse

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


# Correct: use only BackgroundTasks (no background= on Response)
@app.get("/correct")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Notification sent")
    return JSONResponse(content={"message": "done"})


# Wrong: background= on Response silently overrides BackgroundTasks
@app.get("/wrong")
async def send_notification_wrong(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "This task will NOT run")
    return JSONResponse(
        content={"message": "done"},
        background=None,  # If this were a BackgroundTask, it would override the line above
    )
