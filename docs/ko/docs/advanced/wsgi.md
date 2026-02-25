# WSGI 포함하기 - Flask, Django 등 { #including-wsgi-flask-django-others }

[서브 애플리케이션 - 마운트](sub-applications.md){.internal-link target=_blank}, [프록시 뒤에서](behind-a-proxy.md){.internal-link target=_blank}에서 본 것처럼 WSGI 애플리케이션을 마운트할 수 있습니다.

이를 위해 `WSGIMiddleware`를 사용해 WSGI 애플리케이션(예: Flask, Django 등)을 감쌀 수 있습니다.

## `WSGIMiddleware` 사용하기 { #using-wsgimiddleware }

/// info | 정보

이를 사용하려면 `a2wsgi`를 설치해야 합니다. 예: `pip install a2wsgi`

///

`a2wsgi`에서 `WSGIMiddleware`를 import 해야 합니다.

그런 다음, WSGI(예: Flask) 애플리케이션을 미들웨어로 감쌉니다.

그리고 해당 경로에 마운트합니다.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | 참고

이전에 `fastapi.middleware.wsgi`의 `WSGIMiddleware` 사용을 권장했지만 이제는 더 이상 권장되지 않습니다.

대신 `a2wsgi` 패키지 사용을 권장합니다. 사용 방법은 동일합니다.

단, `a2wsgi` 패키지가 설치되어 있고 `a2wsgi`에서 `WSGIMiddleware`를 올바르게 import 하는지만 확인하세요.

///

## 확인하기 { #check-it }

이제 `/v1/` 경로에 있는 모든 요청은 Flask 애플리케이션에서 처리됩니다.

그리고 나머지는 **FastAPI**에 의해 처리됩니다.

실행하고 <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>로 이동하면 Flask의 응답을 볼 수 있습니다:

```txt
Hello, World from Flask!
```

그리고 <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>로 이동하면 **FastAPI**의 응답을 볼 수 있습니다:

```JSON
{
    "message": "Hello World"
}
```
