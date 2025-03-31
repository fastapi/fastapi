# WSGI - Flask, Django ve Daha Fazlasını FastAPI ile Kullanma

WSGI uygulamalarını [Sub Applications - Mounts](sub-applications.md){.internal-link target=_blank}, [Behind a Proxy](behind-a-proxy.md){.internal-link target=_blank} bölümlerinde gördüğünüz gibi bağlayabilirsiniz.

Bunun için `WSGIMiddleware` ile Flask, Django vb. WSGI uygulamanızı sarmalayabilir ve FastAPI'ya bağlayabilirsiniz.

## `WSGIMiddleware` Kullanımı

`WSGIMiddleware`'ı projenize dahil edin.

Ardından WSGI (örneğin Flask) uygulamanızı middleware ile sarmalayın.

Son olarak da bir yol altında bağlama işlemini gerçekleştirin.

{* ../../docs_src/wsgi/tutorial001.py hl[2:3,23] *}

## Kontrol Edelim

Artık `/v1/` yolunun altındaki her istek Flask uygulaması tarafından işlenecektir.

Geri kalanı ise **FastAPI** tarafından işlenecektir.

Eğer uygulamanızı çalıştırıp <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a> adresine giderseniz, Flask'tan gelen yanıtı göreceksiniz:

```txt
Hello, World from Flask!
```

Eğer <a href="http://localhost:8000/v2/" class="external-link" target="_blank">http://localhost:8000/v2/</a> adresine giderseniz, FastAPI'dan gelen yanıtı göreceksiniz:

```JSON
{
    "message": "Hello World"
}
```
