import socketio
def SocketIOServer(fast_app):
    sio = socketio.AsyncServer(
        async_mode='asgi',
        cors_allowed_origins='*'
    )
    app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=fast_app,
        socketio_path='/socket.io/'
    )
    app.socketio = sio
    return app