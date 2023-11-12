from fastapi import FastAPI
from fastapi.responses import MsgSpecJSONResponse
from fastapi.testclient import TestClient
from sqlalchemy.sql.elements import quoted_name

app = FastAPI(default_response_class=MsgSpecJSONResponse)


@app.get("/msgpsec_non_str_keys")
def get_msgspec_non_str_keys():
    key = quoted_name(value="msg", quote=False)
    return {key: "Hello World", 1: 1}


client = TestClient(app)


def test_msgpsec_non_str_keys():
    with client:
        response = client.get("/msgpsec_non_str_keys")
    assert response.json() == {"msg": "Hello World", "1": 1}
