from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websocketio import SocketIOMerger
import time
import socketio

app = FastAPI()
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)
html = """
<!-- test-io-client.html -->
<script src="https://cdn.socket.io/4.2.0/socket.io.js"></script>
<script>

    function init()
    {
        output = document.getElementById("output");
        testSocket();
    }
    var socket = io.connect('http://localhost:8000/');
    function writeToScreen(message)
    {
        var pre = document.createElement("p");
        pre.style.wordWrap = "break-word";
        pre.innerHTML = message;
        output.appendChild(pre);
    }
    function testSocket()
    {
        socket.on('connect', onConnect );
        socket.on('disconnect', onDisconnect );
        socket.on('connect_error', onError );
        socket.on('reconnect_error', onError );
        socket.on('hello2you', onName )


        function onDisconnect(evt)
        {
            writeToScreen("DISCONNECTED");
        }
        function onConnect(evt)
        {
            writeToScreen("CONNECTED");
        }

        function onName(data)
        {
            writeToScreen('<span style="color: blue;">NAME: ' + data.Name+'</span>');
        }

        function onError(message)
        {
            writeToScreen('<span style="color: red;">ERROR:</span> ' + message);
        }

    }
    function submitForm(e)
    {
        e.preventDefault()
        writeToScreen('<span style="color: green;">SENT:</span> ' + document.getElementById("name").value);
        socket.emit('hello', {name: document.getElementById("name").value})
    }
    window.addEventListener("load", init, false);
</script>

<h2>Socket.io Test</h2>
<form onsubmit="submitForm(event)">
<input id="name" />
</form>
<fieldset>
<legend>Output</legend>
<div id="output"></div>
</fieldset>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

@sio.on("hello")
async def hello(sid, data):
    print({"Name": data["name"]})
    await sio.emit("hello2you",{"Name": data["name"], "sid": sid})

@app.get("/")
async def root():
    return {"message": "Hello World"}
app = SocketIOMerger(app, sio)