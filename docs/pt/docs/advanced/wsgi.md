# Adicionando WSGI - Flask, Django, entre outros { #including-wsgi-flask-django-others }

Como você viu em [Subaplicações - Montagens](sub-applications.md){.internal-link target=_blank} e [Atrás de um Proxy](behind-a-proxy.md){.internal-link target=_blank}, você pode montar aplicações WSGI.

Para isso, você pode utilizar o `WSGIMiddleware` para encapsular a sua aplicação WSGI, como por exemplo Flask, Django, etc.

## Usando `WSGIMiddleware` { #using-wsgimiddleware }

Você precisa importar o `WSGIMiddleware`.

Em seguida, encapsule a aplicação WSGI (e.g. Flask) com o middleware.

E então monte isso sob um path.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,3] *}

## Confira { #check-it }

Agora, todas as requisições sob o path `/v1/` serão manipuladas pela aplicação Flask.

E o resto será manipulado pelo **FastAPI**.

Se você rodar a aplicação e ir até <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, você verá o retorno do Flask:

```txt
Hello, World from Flask!
```

E se você for até <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, você verá o retorno do FastAPI:

```JSON
{
    "message": "Hello World"
}
```
