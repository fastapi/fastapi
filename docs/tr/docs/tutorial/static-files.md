# Statik Dosyalar

Statik dosyaları otomatik olarak bir dizinden sunmak için `StaticFiles`'ı kullanabilirsiniz.

## `StaticFiles` Kullanımı

* `StaticFiles` sınıfını projenize dahil edin.
* Bir `StaticFiles()` örneğini belirli bir yola bağlayın.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "Teknik Detaylar"
    Projenize dahil etmek için `from starlette.staticfiles import StaticFiles` kullanabilirsiniz.

    **FastAPI**, geliştirici olarak size bir kolaylık sağlamak amacıyla `starlette.staticfiles`'ı `fastapi.staticfiles` olarak sunar. Ancak `StaticFiles` sınıfı aslında doğrudan Starlette'den gelir.

### Bağlama (Mounting) Nedir?

"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

This is different from using an `APIRouter` as a mounted application is completely independent. The OpenAPI and docs from your main application won't include anything from the mounted application, etc.

You can read more about this in the [Advanced User Guide](../advanced/index.md){.internal-link target=_blank}.

## Detaylar

The first `"/static"` refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with `"/static"` will be handled by it.

The `directory="static"` refers to the name of the directory that contains your static files.

The `name="static"` gives it a name that can be used internally by **FastAPI**.

All these parameters can be different than "`static`", adjust them with the needs and specific details of your own application.

## Daha Fazla Bilgi

Daha fazla bilgi ve seçenek için <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starlette'nin Statik Dosyalar hakkındaki dokümantasyonuna</a> bakın.