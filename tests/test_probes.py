from fastapi import FastAPI, Request

app = FastAPI(liveness_probe_url="/health/liveness")


@app.get("/")
def change_state(request: Request):
    request.app.probes_state.alive = not request.app.probes_state.alive
