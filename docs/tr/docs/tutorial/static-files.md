# Statik Dosyalar { #static-files }

`StaticFiles`'ı kullanarak bir dizinden statik dosyaları otomatik olarak sunabilirsiniz.

## `StaticFiles`'ı Kullanma { #use-staticfiles }

* `StaticFiles`'ı içe aktarın.
* Belirli bir path altında bir `StaticFiles()` örneğini "mount" edin.

{* ../../docs_src/static_files/tutorial001_py39.py hl[2,6] *}

/// note | Teknik Detaylar

Ayrıca `from starlette.staticfiles import StaticFiles` kullanabilirsiniz.

**FastAPI**, geliştirici olarak sizin için bir kolaylık olarak `starlette.staticfiles`'ı `fastapi.staticfiles` olarak sağlar. Ancak aslında doğrudan Starlette'den gelir.

///

### "Mounting" Nedir { #what-is-mounting }

"Mounting", belirli bir path'e tamamen "bağımsız" bir uygulama eklemek anlamına gelir; bu uygulama daha sonra tüm alt path'leri işlemekle ilgilenir.

Bu, bir `APIRouter` kullanmaktan farklıdır çünkü mount edilmiş bir uygulama tamamen bağımsızdır. Ana uygulamanızın OpenAPI ve dokümanları, mount edilmiş uygulamadan hiçbir şey içermez, vb.

Bununla ilgili daha fazlasını [Advanced User Guide](../advanced/index.md){.internal-link target=_blank} bölümünde okuyabilirsiniz.

## Detaylar { #details }

İlk `"/static"`, bu "alt uygulamanın" üzerine "mount" edileceği alt path'i ifade eder. Dolayısıyla, `"/static"` ile başlayan herhangi bir path bunun tarafından işlenir.

`directory="static"`, statik dosyalarınızı içeren dizinin adını ifade eder.

`name="static"`, **FastAPI** tarafından dahili olarak kullanılabilecek bir isim verir.

Bu parametrelerin tümü "`static`"den farklı olabilir; bunları kendi uygulamanızın ihtiyaçlarına ve spesifik detaylarına göre ayarlayın.

## Daha Fazla Bilgi { #more-info }

Daha fazla detay ve seçenek için <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Statik Dosyalar hakkında Starlette dokümanlarını</a> inceleyin.
