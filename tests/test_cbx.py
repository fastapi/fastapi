from fastapi import APIRouter, FastAPI
from fastapi.cbx import cbr, cbv
from fastapi.testclient import TestClient
from pydantic import BaseModel


# ==============================
# 请求体模型（用于 POST 传参）
# ==============================
class UserCreate(BaseModel):
    username: str
    age: int


# ==============================
# 1. CBV 测试：自动路由 + 接口传参
# ==============================
@cbv(prefix="/cbv", router=APIRouter())
class CBVTest:
    def __init__(self, message: str):
        self.message = message

    # GET 传参：查询参数
    def get(self, user_id: int, name: str = None):
        return {"hello": self.message, "user_id": user_id, "name": name}

    # POST 传参：请求体
    def post(self, user: UserCreate):
        return {
            "method": "POST",
            "message": self.message,
            "user": user.model_dump(),  # 🔥 修复在这里
        }


# ==============================
# 2. CBR 测试：装饰器路由 + 接口传参
# ==============================
@cbr(prefix="/cbr", router=APIRouter())
class CBRTest:
    def __init__(self, service_name: str):
        self.service_name = service_name

    @cbr.get("/info")
    def get_info(self, id: int):
        return {"service": self.service_name, "id": id}

    @cbr.post("/create")
    def create_user(self, user: UserCreate):
        return {
            "service": self.service_name,
            "user": user.model_dump(),  # 🔥 修复在这里
        }


# ==============================
# ✅ 优雅初始化（传参）+ 挂载路由
# ==============================
cbv_instance = CBVTest(message="cbv_success")
cbr_instance = CBRTest(service_name="cbr_service")

app = FastAPI()
app.include_router(cbv_instance.router)
app.include_router(cbr_instance.router)
client = TestClient(app)


# ==============================
# 🟢 CBV 测试用例（带真实传参）
# ==============================
def test_cbv_get_with_params():
    resp = client.get("/cbv?user_id=100&name=test")
    assert resp.status_code == 200
    assert resp.json()["hello"] == "cbv_success"


def test_cbv_post_with_body():
    resp = client.post("/cbv", json={"username": "test", "age": 20})
    assert resp.status_code == 200
    assert resp.json()["user"]["username"] == "test"


# ==============================
# 🟢 CBR 测试用例（带真实传参）
# ==============================
def test_cbr_get_with_query():
    resp = client.get("/cbr/info?id=999")
    assert resp.status_code == 200
    assert resp.json()["service"] == "cbr_service"


def test_cbr_post_with_body():
    resp = client.post("/cbr/create", json={"username": "cbr_user", "age": 25})
    assert resp.status_code == 200
    assert resp.json()["user"]["age"] == 25
