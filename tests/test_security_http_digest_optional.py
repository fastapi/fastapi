from fastapi import FastAPI, Security
from fastapi.security import HTTPDigest, HTTPDigestCredentials
from fastapi.testclient import TestClient

app = FastAPI()

security = HTTPDigest(realm="somewhere@host.com", auto_error=False)


@app.get("/users/me")
async def read_current_user(digest: HTTPDigestCredentials = Security(security)):
    return {"digest": digest}


client = TestClient(app)


def test_security_http_digest():
    # WHEN: The client attempts to access the protected resource with an invalid
    #       Authorization header.
    response = client.get(
        "/users/me",
        headers={"Authorization": 'Digest username="John"'},
    )

    # THEN: The server responds with a 200 OK response.
    assert response.status_code == 200
    assert response.json() == {"digest": None}
