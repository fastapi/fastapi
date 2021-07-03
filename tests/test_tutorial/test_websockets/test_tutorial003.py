from fastapi.testclient import TestClient

from docs_src.websockets.tutorial003 import app

client = TestClient(app)


def test_websocket_handle_disconnection():
    with client.websocket_connect("/ws/1234") as connection, client.websocket_connect(
        "/ws/5678"
    ) as connection_two:
        connection.send_text("Hello from 1234")
        data1 = connection.receive_text()
        assert data1 == "You wrote: Hello from 1234"
        data2 = connection_two.receive_text()
        client1_says = "Client #1234 says: Hello from 1234"
        assert data2 == client1_says
        data1 = connection.receive_text()
        assert data1 == client1_says
        connection_two.close()
        data1 = connection.receive_text()
        assert data1 == "Client #5678 left the chat"
