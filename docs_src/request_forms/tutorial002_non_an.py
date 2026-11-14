from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/preferences/")
async def update_preferences(subscribe: bool = Form(default=False)):
    return {"subscribe": subscribe}
