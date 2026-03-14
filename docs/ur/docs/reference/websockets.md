# WebSockets

WebSockets define کرتے وقت، آپ عام طور پر `WebSocket` type کا parameter declare کرتے ہیں اور اس کے ذریعے client سے ڈیٹا پڑھ سکتے ہیں اور اسے ڈیٹا بھیج سکتے ہیں۔

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)

یہ Starlette کی طرف سے براہ راست فراہم کیا گیا ہے، لیکن آپ اسے `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import WebSocket
```

/// tip | مشورہ

جب آپ ایسی dependencies define کرنا چاہیں جو HTTP اور WebSockets دونوں کے ساتھ مطابقت رکھتی ہوں، تو آپ `Request` یا `WebSocket` کی بجائے `HTTPConnection` لینے والا parameter define کر سکتے ہیں۔

///

::: fastapi.WebSocket
    options:
        members:
            - scope
            - app
            - url
            - base_url
            - headers
            - query_params
            - path_params
            - cookies
            - client
            - state
            - url_for
            - client_state
            - application_state
            - receive
            - send
            - accept
            - receive_text
            - receive_bytes
            - receive_json
            - iter_text
            - iter_bytes
            - iter_json
            - send_text
            - send_bytes
            - send_json
            - close

## WebSockets - اضافی classes

WebSockets کو سنبھالنے کے لیے اضافی classes۔

Starlette کی طرف سے براہ راست فراہم کی گئی ہیں، لیکن آپ انہیں `fastapi` سے import کر سکتے ہیں:

```python
from fastapi.websockets import WebSocketDisconnect, WebSocketState
```

::: fastapi.websockets.WebSocketDisconnect

جب کوئی client منقطع ہوتا ہے تو `WebSocketDisconnect` exception raise ہوتا ہے، آپ اسے catch کر سکتے ہیں۔

آپ اسے براہ راست `fastapi` سے import کر سکتے ہیں:

```python
from fastapi import WebSocketDisconnect
```

اس کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں WebSockets](https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients)

::: fastapi.websockets.WebSocketState

`WebSocketState` ایک enumeration ہے جو WebSocket connection کی ممکنہ حالتوں کو ظاہر کرتا ہے۔
