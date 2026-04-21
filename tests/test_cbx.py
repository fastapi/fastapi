from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.cbx import cbr, cbv
from fastapi.testclient import TestClient


# ==============================================
# Shared mock resources
# ==============================================
class FakeDB:
    def __init__(self):
        self.users = {1: "Alice", 2: "Bob"}

    def get_user(self, user_id: int):
        return self.users.get(user_id)

    def update_user(self, user_id: int, name: str):
        if user_id not in self.users:
            return False
        self.users[user_id] = name
        return True

    def delete_user(self, user_id: int):
        if user_id not in self.users:
            return False
        del self.users[user_id]
        return True


db = FakeDB()


class FakeSession:
    def __init__(self):
        self.uid = 1001


def get_session():
    return FakeSession()


# ==============================================
# Application & Routers (All with prefix)
# ==============================================
app = FastAPI(title="fastapi-cbx")


# One scenario, one route

# ==============================================
# 1. FR (Function Route)
# ==============================================
router = APIRouter(prefix="/fr")


@router.get("/")
def index():
    return {"route": "function"}


app.include_router(router)

# ==============================================
# 2. CBV (Class-Based View)
# ==============================================
router = APIRouter(prefix="/user")


@cbv(router=router)
class UserCBV:
    def __init__(self, db: FakeDB = db):
        self.db = db

    def get(self, user_id: int, session: FakeSession = Depends(get_session)):
        user = self.db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"user": user, "operated_by": session.uid}

    async def post(self, user_id: int, name: str):
        if self.db.get_user(user_id):
            raise HTTPException(status_code=400, detail="User already exists")

        return {
            "user_id": user_id,
            "name": name,
            "message": "User created successfully",
        }

    async def put(self, user_id: int, name: str):
        if not self.db.update_user(user_id, name):
            raise HTTPException(status_code=404, detail="User not found, update failed")

    def delete(self, user_id: int):
        if not self.db.delete_user(user_id):
            raise HTTPException(status_code=404, detail="User not found, delete failed")


UserCBV(db)

app.include_router(router)

# ==============================================
# 3. CBR (Class-Based Route)
# ==============================================
router = APIRouter(prefix="/order")


@cbr(router=router)
class OrderCBR:
    _order_prefix = "ORDER-"

    def __init__(self, db: FakeDB = db):
        self.db = db

    @cbr.get("/info")
    def info(self, order_id: int, session: FakeSession = Depends(get_session)):
        return {
            "order_id": f"{self._order_prefix}{order_id}",
            "current_user_id": session.uid,
            "db": self.db,
        }

    @cbr.post("/create")
    async def create(self, order_id: int, name: str):
        return {
            "order_id": f"{self._order_prefix}{order_id}",
            "user": name,
            "db_tag": str(self.db),
        }

    @cbr.post("/batch")
    @classmethod
    def batch_create(cls, total: int):
        return {
            "method": "classmethod",
            "order_prefix": cls._order_prefix,
            "batch_total": total,
        }

    @cbr.get("/validate")
    @staticmethod
    def validate_order(order_id: int):
        return {"method": "staticmethod", "is_valid": order_id > 0}


OrderCBR(db)

app.include_router(router)


# ==============================================
# FULL TEST COVERAGE (100%)
# ==============================================
client = TestClient(app)


# --------------------------
# 1. Test FR /fr/
# --------------------------
def test_fr_index():
    """Test FR (Function Route) endpoint"""
    resp = client.get("/fr/")
    assert resp.status_code == 200
    assert resp.json() == {"route": "function"}


# --------------------------
# 2. Test CBV /user
# --------------------------
def test_cbv_user_get():
    """Test GET method for CBV User endpoint"""
    resp = client.get("/user?user_id=1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["user"] == "Alice"
    assert data["operated_by"] == 1001


def test_cbv_user_post():
    """Test POST method for CBV User endpoint"""
    resp = client.post("/user?user_id=5&name=test_user")
    assert resp.status_code == 201
    data = resp.json()
    assert data == {
        "message": "User created successfully",
        "user_id": 5,
        "name": "test_user",
    }


def test_cbv_user_put():
    """Test PUT method for CBV User endpoint"""
    resp = client.put("/user?user_id=1&name=updated_user")
    assert resp.status_code == 204


def test_cbv_user_delete():
    """Test DELETE method for CBV User endpoint"""
    resp = client.delete("/user?user_id=2")
    assert resp.status_code == 204


# --------------------------
# 3. Test CBR /order/info
# --------------------------
def test_cbr_order_info():
    """Test GET info endpoint for CBR Order class"""
    resp = client.get("/order/info?order_id=1001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["order_id"] == "ORDER-1001"
    assert data["current_user_id"] == 1001


def test_cbr_order_create():
    """Test POST create endpoint for CBR Order class"""
    resp = client.post("/order/create?order_id=100&name=test_order")
    assert resp.status_code == 200
    data = resp.json()
    assert data["order_id"] == "ORDER-100"
    assert data["user"] == "test_order"
    assert "db_tag" in data


def test_cbr_order_batch_create():
    """Test class method batch create endpoint for CBR Order class"""
    resp = client.post("/order/batch?total=50")
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "classmethod"
    assert data["order_prefix"] == "ORDER-"
    assert data["batch_total"] == 50


def test_cbr_order_validate_valid():
    """Test static method validate endpoint with valid order ID"""
    resp = client.get("/order/validate?order_id=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "staticmethod"
    assert data["is_valid"] is True


def test_cbr_order_validate_invalid():
    """Test static method validate endpoint with invalid order ID"""
    resp = client.get("/order/validate?order_id=-1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid"] is False
