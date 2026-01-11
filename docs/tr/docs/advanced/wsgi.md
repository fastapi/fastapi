# WSGI Dahil Etme - Flask, Django, Diğerleri { #including-wsgi-flask-django-others }

WSGI uygulamalarını [Sub Applications - Mounts](sub-applications.md){.internal-link target=_blank}, [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank} bölümlerinde gördüğünüz gibi bağlayabilirsiniz.

Bunun için `WSGIMiddleware`'ı kullanabilir ve WSGI uygulamanızı (örneğin Flask, Django vb.) sarmalamak için bundan yararlanabilirsiniz.

## `WSGIMiddleware` Kullanımı { #using-wsgimiddleware }

`WSGIMiddleware`'ı import etmeniz gerekir.

Ardından WSGI (ör. Flask) uygulamasını middleware ile sarmalayın.

Ve sonra bunu bir path altında bağlayın.

{* ../../docs_src/wsgi/tutorial001_py39.py hl[2:3,3] *}

## Kontrol Edelim { #check-it }

Artık `/v1/` path'inin altındaki her request Flask uygulaması tarafından işlenecektir.

Geri kalanı ise **FastAPI** tarafından işlenecektir.

Eğer bunu çalıştırıp <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> adresine giderseniz, Flask'tan gelen response'u göreceksiniz:

```txt
Hello, World from Flask!
```

Ve eğer <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> adresine giderseniz, FastAPI'dan gelen response'u göreceksiniz:

```JSON
{
    "message": "Hello World"
}
```
