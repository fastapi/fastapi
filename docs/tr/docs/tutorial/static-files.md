# Statik Dosyalar { #static-files }

`StaticFiles`'ı kullanarak statik dosyaları bir yol altında sunabilirsiniz.

## `StaticFiles` Kullanımı { #use-staticfiles }

* `StaticFiles` sınıfını projenize dahil edin.
* Bir `StaticFiles()` örneğini belirli bir yola bağlayın.

{* ../../docs_src/static_files/tutorial001_py39.py hl[2,6] *}

/// note | Teknik Detaylar

Projenize dahil etmek için `from starlette.staticfiles import StaticFiles` kullanabilirsiniz.

**FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.staticfiles`'ı `fastapi.staticfiles` olarak sağlar. Ancak `StaticFiles` sınıfı aslında doğrudan Starlette'den gelir.

///

### Bağlama (Mounting) Nedir? { #what-is-mounting }

"Bağlamak", belirli bir yola tamamen "bağımsız" bir uygulama eklemek anlamına gelir ve ardından tüm alt yollara gelen istekler bu uygulama tarafından işlenir.

Bu, bir `APIRouter` kullanmaktan farklıdır çünkü bağlanmış bir uygulama tamamen bağımsızdır. Ana uygulamanızın OpenAPI ve dokümanlar, bağlanmış uygulamadan hiçbir şey içermez, vb.

[Advanced User Guide](../advanced/index.md){.internal-link target=_blank} bölümünde daha fazla bilgi edinebilirsiniz.

## Detaylar { #details }

`"/static"` ifadesi, bu "alt uygulamanın" "bağlanacağı" alt yolu belirtir. Bu nedenle, `"/static"` ile başlayan her yol, bu uygulama tarafından işlenir.

`directory="static"` ifadesi, statik dosyalarınızı içeren dizinin adını belirtir.

`name="static"` ifadesi, alt uygulamanın **FastAPI** tarafından kullanılacak ismini belirtir.

Bu parametrelerin hepsi "`static`"den farklı olabilir, bunları kendi uygulamanızın ihtiyaçlarına göre belirleyebilirsiniz.

## Daha Fazla Bilgi { #more-info }

Daha fazla detay ve seçenek için <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette'in Statik Dosyalar hakkındaki dokümantasyonunu</a> incelleyin.
