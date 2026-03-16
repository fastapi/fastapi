# WSGI'yi Dahil Etme - Flask, Django ve Diğerleri { #including-wsgi-flask-django-others }

WSGI uygulamalarını [Alt Uygulamalar - Mount Etme](sub-applications.md){.internal-link target=_blank}, [Bir Proxy Arkasında](behind-a-proxy.md){.internal-link target=_blank} bölümlerinde gördüğünüz gibi mount edebilirsiniz.

Bunun için `WSGIMiddleware`'ı kullanabilir ve bunu WSGI uygulamanızı (örneğin Flask, Django vb.) sarmalamak için kullanabilirsiniz.

## `WSGIMiddleware` Kullanımı { #using-wsgimiddleware }

/// info | Bilgi

Bunun için `a2wsgi` kurulmalıdır; örneğin `pip install a2wsgi` ile.

///

`WSGIMiddleware`'ı `a2wsgi` paketinden import etmeniz gerekir.

Ardından WSGI (örn. Flask) uygulamasını middleware ile sarmalayın.

Ve sonra bunu bir path'in altına mount edin.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Not

Önceden, `fastapi.middleware.wsgi` içindeki `WSGIMiddleware`'ın kullanılması öneriliyordu, ancak artık kullanımdan kaldırıldı.

Bunun yerine `a2wsgi` paketini kullanmanız önerilir. Kullanım aynıdır.

Sadece `a2wsgi` paketinin kurulu olduğundan emin olun ve `WSGIMiddleware`'ı `a2wsgi` içinden doğru şekilde import edin.

///

## Kontrol Edelim { #check-it }

Artık `/v1/` path'i altındaki her request Flask uygulaması tarafından işlenecektir.

Geri kalanı ise **FastAPI** tarafından işlenecektir.

Eğer uygulamanızı çalıştırıp <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> adresine giderseniz, Flask'tan gelen response'u göreceksiniz:

```txt
Hello, World from Flask!
```

Ve eğer <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a> adresine giderseniz, FastAPI'dan gelen response'u göreceksiniz:

```JSON
{
    "message": "Hello World"
}
```
