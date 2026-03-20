# Adicionando WSGI - Flask, Django, entre outros { #including-wsgi-flask-django-others }

Como você viu em [Subaplicações - Montagens](sub-applications.md) e [Atrás de um Proxy](behind-a-proxy.md), você pode montar aplicações WSGI.

Para isso, você pode utilizar o `WSGIMiddleware` para encapsular a sua aplicação WSGI, como por exemplo Flask, Django, etc.

## Usando `WSGIMiddleware` { #using-wsgimiddleware }

/// info | Informação

Isso requer instalar `a2wsgi`, por exemplo com `pip install a2wsgi`.

///

Você precisa importar o `WSGIMiddleware` de `a2wsgi`.

Em seguida, encapsule a aplicação WSGI (e.g. Flask) com o middleware.

E então monte isso sob um path.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Nota

Anteriormente, recomendava-se usar `WSGIMiddleware` de `fastapi.middleware.wsgi`, mas agora está descontinuado.

É aconselhável usar o pacote `a2wsgi` em seu lugar. O uso permanece o mesmo.

Apenas certifique-se de que o pacote `a2wsgi` está instalado e importe `WSGIMiddleware` corretamente de `a2wsgi`.

///

## Confira { #check-it }

Agora, todas as requisições sob o path `/v1/` serão manipuladas pela aplicação Flask.

E o resto será manipulado pelo **FastAPI**.

Se você rodar a aplicação e ir até [http://localhost:8000/v1/](http://localhost:8000/v1/), você verá o retorno do Flask:

```txt
Hello, World from Flask!
```

E se você for até [http://localhost:8000/v2](http://localhost:8000/v2), você verá o retorno do FastAPI:

```JSON
{
    "message": "Hello World"
}
```
