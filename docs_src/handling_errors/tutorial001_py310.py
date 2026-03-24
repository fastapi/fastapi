from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Padronização Alantec: Tratamento de Erros de Validação.
    Objetivo: Transformar erros complexos em respostas claras e estruturadas.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Erro de validação detectado pela Alantec",
            "details": exc.errors(),
            "status": "error",
            "code": 422,
        },
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
