"""
自定义API测试
这是一个示例测试文件，展示如何在FastAPI项目中编写测试
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import Optional


# 创建一个简单的FastAPI应用用于测试
app = FastAPI()


# 定义数据模型
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


class User(BaseModel):
    username: str
    email: str


# 定义API路由
@app.get("/")
def read_root():
    return {"message": "Hello Custom API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "status": "created"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "username": f"user_{user_id}"}


# 创建测试客户端
client = TestClient(app)


# 测试用例
class TestCustomAPI:
    """自定义API测试类"""
    
    def test_read_root(self):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Custom API"}
    
    def test_read_item_with_params(self):
        """测试带参数的商品查询"""
        response = client.get("/items/5?q=somequery")
        assert response.status_code == 200
        assert response.json() == {"item_id": 5, "q": "somequery"}
    
    def test_read_item_without_params(self):
        """测试不带查询参数的商品查询"""
        response = client.get("/items/10")
        assert response.status_code == 200
        assert response.json() == {"item_id": 10, "q": None}
    
    def test_create_item(self):
        """测试创建商品"""
        item_data = {
            "name": "Test Item",
            "price": 99.99,
            "is_offer": True
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "created"
        assert response_data["item"]["name"] == "Test Item"
        assert response_data["item"]["price"] == 99.99
        assert response_data["item"]["is_offer"] is True
    
    def test_get_user(self):
        """测试获取用户信息"""
        response = client.get("/users/123")
        assert response.status_code == 200
        assert response.json() == {"user_id": 123, "username": "user_123"}
    
    @pytest.mark.parametrize("item_id,expected_id", [
        (1, 1),
        (42, 42),
        (999, 999),
    ])
    def test_read_item_parametrized(self, item_id, expected_id):
        """参数化测试：测试不同的商品ID"""
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["item_id"] == expected_id
    
    def test_invalid_item_id(self):
        """测试无效的商品ID"""
        response = client.get("/items/not_a_number")
        assert response.status_code == 422  # 验证错误
    
    def test_create_item_invalid_data(self):
        """测试创建商品时的无效数据"""
        invalid_data = {
            "name": "Test Item",
            # 缺少必需的price字段
            "is_offer": True
        }
        response = client.post("/items/", json=invalid_data)
        assert response.status_code == 422  # 验证错误


# 独立的测试函数（不在类中）
def test_app_startup():
    """测试应用启动"""
    assert app.title == "FastAPI"


def test_openapi_schema():
    """测试OpenAPI schema生成"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema


# Fixture示例
@pytest.fixture
def sample_item():
    """测试用的示例商品数据"""
    return {
        "name": "Sample Item",
        "price": 50.0,
        "is_offer": False
    }


def test_with_fixture(sample_item):
    """使用fixture的测试"""
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["item"]["name"] == sample_item["name"]
