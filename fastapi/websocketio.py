import socketio
def SocketIOMerger(fast_app, sio):
    app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=fast_app,
        socketio_path='/socket.io/'
    )
    app.socketio = sio
    return app