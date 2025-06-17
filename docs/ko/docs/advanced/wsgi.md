# WSGI 포함하기 - Flask, Django 그 외

[서브 응용 프로그램 - 마운트](sub-applications.md){.internal-link target=_blank}, [프록시 뒤편에서](behind-a-proxy.md){.internal-link target=_blank}에서 보았듯이 WSGI 응용 프로그램들을 다음과 같이 마운트 할 수 있습니다.

`WSGIMiddleware`를 사용하여 WSGI 응용 프로그램(예: Flask, Django 등)을 감쌀 수 있습니다.

## `WSGIMiddleware` 사용하기

`WSGIMiddleware`를 불러와야 합니다.

그런 다음, WSGI(예: Flask) 응용 프로그램을 미들웨어로 포장합니다.

그 후, 해당 경로에 마운트합니다.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,23] *}

## 확인하기

이제 `/v1/` 경로에 있는 모든 요청은 Flask 응용 프로그램에서 처리됩니다.

그리고 나머지는 **FastAPI**에 의해 처리됩니다.

실행하면 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>으로 이동해서 Flask의 응답을 볼 수 있습니다:

```txt
Hello, World from Flask!
```

그리고 다음으로 이동하면 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> Flask의 응답을 볼 수 있습니다:

```JSON
{
    "message": "Hello World"
}
```
