# https://github.com/fastapi/fastapi/issues/10180

from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

def test_mount_subapp_on_apirouter_should_not_work():
    app = FastAPI()
    router = APIRouter(prefix="/api")

    @router.get("/main")
    def main():
        return {"msg": "main"}

    subapp = FastAPI()

    @subapp.get("/sub")
    def sub():
        return {"msg": "sub"}

    # Tentativa de montar subapp no router (não funciona)
    router.mount("/subapi", subapp)
    app.include_router(router)

    client = TestClient(app)
    # A rota principal funciona
    assert client.get("/api/main").status_code == 200
    # A rota da subaplicação NÃO funciona (deveria retornar 404)
    assert client.get("/api/subapi/sub").status_code == 404


def test_mount_subapp_on_app_should_work():
    app = FastAPI()
    router = APIRouter(prefix="/api")

    @router.get("/main")
    def main():
        return {"msg": "main"}

    subapp = FastAPI()

    @subapp.get("/sub")
    def sub():
        return {"msg": "sub"}

    app.include_router(router)
    # Montando corretamente no app principal
    app.mount("/api/subapi", subapp)

    client = TestClient(app)
    # A rota principal funciona
    assert client.get("/api/main").status_code == 200
    # A rota da subaplicação funciona
    assert client.get("/api/subapi/sub").status_code == 200


# Testes adicionais para melhorar cobertura:


def test_mount_multiple_subapps():
    """Testa se é possível montar múltiplas subaplicações"""
    app = FastAPI()

    # Primeira subaplicação
    subapp1 = FastAPI()

    @subapp1.get("/test1")
    def read_test1():
        return {"msg": "test1"}

    # Segunda subaplicação
    subapp2 = FastAPI()

    @subapp2.get("/test2")
    def read_test2():
        return {"msg": "test2"}

    # Montando ambas as subaplicações
    app.mount("/sub1", subapp1)
    app.mount("/sub2", subapp2)

    client = TestClient(app)
    # Verifica se ambas as subaplicações funcionam
    assert client.get("/sub1/test1").status_code == 200
    assert client.get("/sub2/test2").status_code == 200
    assert client.get("/sub1/test1").json() == {"msg": "test1"}
    assert client.get("/sub2/test2").json() == {"msg": "test2"}


def test_nested_routes():
    """Testa rotas aninhadas em diferentes níveis"""
    app = FastAPI()

    # Criando routers aninhados
    router1 = APIRouter(prefix="/v1")
    router2 = APIRouter(prefix="/api")

    @router2.get("/deep")
    def read_deep():
        return {"msg": "deep route"}

    # Aninhando os routers
    router1.include_router(router2)
    app.include_router(router1)

    client = TestClient(app)
    # Verifica se a rota aninhada funciona
    response = client.get("/v1/api/deep")
    assert response.status_code == 200
    assert response.json() == {"msg": "deep route"}

    # Verifica se uma rota inexistente retorna 404
    assert client.get("/v1/api/nonexistent").status_code == 404


def test_method_not_allowed():
    """Testa se métodos HTTP não permitidos são tratados corretamente"""
    app = FastAPI()

    @app.get("/only-get")
    def read_only():
        return {"msg": "get only"}

    client = TestClient(app)
    # Verifica se GET funciona
    assert client.get("/only-get").status_code == 200

    # Verifica se outros métodos retornam 405 (Method Not Allowed)
    assert client.post("/only-get").status_code == 405
    assert client.put("/only-get").status_code == 405
    assert client.delete("/only-get").status_code == 405
