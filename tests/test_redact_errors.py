from fastapi import FastAPI, Form
from fastapi.exception_handlers import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

# Create a minimal app with the flag enabled
app = FastAPI(redact_error_details=True)


@app.post("/test")
def test_endpoint(age: int = Form()):
    return {"age": age}


# Override default handler for demonstration (optional)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Request validation failed"},  # Redacted message
    )


client = TestClient(app)


def test_redacted_validation_error():
    # Send invalid form data (empty string instead of int)
    response = client.post("/test", data={"age": ""})
    assert response.status_code == 422
    assert response.json() == {"detail": "Request validation failed"}


def test_valid_request():
    response = client.post("/test", data={"age": "25"})
    assert response.status_code == 200
    assert response.json() == {"age": 25}
