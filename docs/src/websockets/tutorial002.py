from fastapi import Cookie, Depends, FastAPI, Header
from starlette.responses import HTMLResponse
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <button onclick="connect(event)">Connect</button>
            <br>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var input = document.getElementById("itemId")
                ws = new WebSocket("ws://localhost:8000/items/" + input.value + "/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_client(
    websocket: WebSocket, session: str = Cookie(None), x_client: str = Header(None)
):
    if session is None and x_client is None:
        await websocket.close(code=WS_1008_POLICY_VIOLATION)
    return session or x_client


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: int,
    q: str = None,
    cookie_or_client: str = Depends(get_cookie_or_client),
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session Cookie or X-Client Header value is: {cookie_or_client}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
