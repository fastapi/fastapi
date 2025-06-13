import pytest
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

# ======================
# Configuração do app e rotas
# ======================

app = FastAPI()
router = APIRouter()


class Item(BaseModel):
    nome: str
    quantidade: int


@router.route("/items/", methods=["GET", "POST"])
async def read_items(request: Request):
    if request.method == "POST":
        try:
            dados = await request.json()
            item = Item(**dados)
            return JSONResponse(
                {"message": "Item criado", "item": item.model_dump()}, status_code=201
            )
        except Exception:
            return JSONResponse({"detail": "Erro ao processar JSON"}, status_code=400)
    return JSONResponse({"hello": "world"})


app.include_router(router)
client = TestClient(app)


################ Testes


# Testa se a rota GET /items/ retorna a resposta padrão esperada
def test_get_items():
    resposta = client.get("/items/")
    assert resposta.status_code == 200
    assert resposta.json() == {"hello": "world"}


# Testa se a rota POST /items/ aceita e retorna corretamente um JSON válido
def test_post_items():
    payload = {"nome": "Caderno", "quantidade": 10}
    resposta = client.post("/items/", json=payload)
    assert resposta.status_code == 201
    assert resposta.json() == {
        "message": "Item criado",
        "item": {"nome": "Caderno", "quantidade": 10},
    }


# Testa se a rota POST /items/ retorna erro ao receber JSON inválido (faltando campo obrigatório)
def test_post_json_invalido():
    payload = {"quantidade": 5}  # Campo 'nome' está ausente
    resposta = client.post("/items/", json=payload)
    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Erro ao processar JSON"


# Testa se a rota POST /items/ retorna erro ao receber corpo que não seja JSON
def test_post_com_corpo_nao_json():
    resposta = client.post("/items/", content="texto")  # Texto cru, não é JSON
    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Erro ao processar JSON"


# Testa se a rota POST /items/ aceita headers customizados e responde corretamente
def test_post_com_header_customizado():
    headers = {"Custom-Header": "123"}
    payload = {"nome": "Caneta", "quantidade": 3}
    resposta = client.post("/items/", json=payload, headers=headers)
    assert resposta.status_code == 201
    assert resposta.json()["item"]["nome"] == "Caneta"


# Testa se métodos não permitidos como PUT são corretamente bloqueados pela API
def test_method_not_allowed():
    resposta = client.put("/items/")
    assert resposta.status_code == 405  # 405 Method Not Allowed
    assert "detail" in resposta.json()


# Testa múltiplos métodos HTTP para a mesma rota usando parametrização
# Verifica se cada método responde com o status esperado
@pytest.mark.parametrize(
    "metodo,status_esperado",
    [
        ("GET", 200),
        ("POST", 201),
        ("PUT", 405),
        ("DELETE", 405),
        ("PATCH", 405),
    ],
)
def test_varios_metodos(metodo, status_esperado):
    payload = {"nome": "Caneta", "quantidade": 1}
    resposta = client.request(metodo, "/items/", json=payload)
    assert resposta.status_code == status_esperado


# Testa se a resposta da rota GET /items/ contém o header correto de Content-Type (application/json)
def test_headers_da_resposta():
    resposta = client.get("/items/")
    assert resposta.headers["content-type"].startswith("application/json")


# Testa se a rota GET ignora parâmetros de query (ex: ?busca=algo)
def test_get_com_query_params_ignorados():
    resposta = client.get("/items/?busca=algo")
    assert resposta.status_code == 200
    assert resposta.json() == {"hello": "world"}
