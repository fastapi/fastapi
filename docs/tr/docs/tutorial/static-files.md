# Statik Dosyalar { #static-files }

`StaticFiles` kullanarak bir dizindeki statik dosyaları otomatik olarak sunabilirsiniz.

## `StaticFiles` Kullanımı { #use-staticfiles }

* `StaticFiles`'ı import edin.
* Belirli bir path'te bir `StaticFiles()` örneğini "mount" edin.

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | Teknik Detaylar

`from starlette.staticfiles import StaticFiles` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.staticfiles`'ı `fastapi.staticfiles` olarak da sağlar. Ancak aslında doğrudan Starlette'den gelir.

///

### "Mounting" Nedir { #what-is-mounting }

"Mounting", belirli bir path'te tamamen "bağımsız" bir uygulama eklemek ve sonrasında tüm alt path'leri handle etmesini sağlamak demektir.

Bu, bir `APIRouter` kullanmaktan farklıdır; çünkü mount edilen uygulama tamamen bağımsızdır. Ana uygulamanızın OpenAPI ve docs'ları, mount edilen uygulamadan hiçbir şey içermez, vb.

Bununla ilgili daha fazla bilgiyi [Gelişmiş Kullanıcı Kılavuzu](../advanced/index.md){.internal-link target=_blank} içinde okuyabilirsiniz.

## Detaylar { #details }

İlk `"/static"`, bu "alt uygulamanın" "mount" edileceği alt path'i ifade eder. Dolayısıyla `"/static"` ile başlayan herhangi bir path bunun tarafından handle edilir.

`directory="static"`, statik dosyalarınızı içeren dizinin adını ifade eder.

`name="static"`, **FastAPI**'nin dahili olarak kullanabileceği bir isim verir.

Bu parametrelerin hepsi "`static`" ile aynı olmak zorunda değildir; kendi uygulamanızın ihtiyaçlarına ve özel detaylarına göre ayarlayın.

## Daha Fazla Bilgi { #more-info }

Daha fazla detay ve seçenek için <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette'in Statik Dosyalar hakkındaki dokümanlarını</a> inceleyin.
