# Daha Büyük Uygulamalar - Birden Fazla Dosya { #bigger-applications-multiple-files }

Bir uygulama veya web API geliştirirken, her şeyi tek bir dosyaya sığdırabilmek nadirdir.

**FastAPI**, tüm esnekliği korurken uygulamanızı yapılandırmanıza yardımcı olan pratik bir araç sunar.

/// info | Bilgi

Flask'ten geliyorsanız, bu yapı Flask'in Blueprints'ine denk gelir.

///

## Örnek Bir Dosya Yapısı { #an-example-file-structure }

Diyelim ki şöyle bir dosya yapınız var:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

/// tip | İpucu

Birden fazla `__init__.py` dosyası var: her dizinde veya alt dizinde bir tane.

Bu sayede bir dosyadaki kodu diğerine import edebilirsiniz.

Örneğin `app/main.py` içinde şöyle bir satırınız olabilir:

```
from app.routers import items
```

///

* `app` dizini her şeyi içerir. Ayrıca boş bir `app/__init__.py` dosyası olduğu için bir "Python package" (bir "Python module" koleksiyonu) olur: `app`.
* İçinde bir `app/main.py` dosyası vardır. Bir Python package'in (içinde `__init__.py` dosyası olan bir dizinin) içinde olduğundan, o package'in bir "module"’üdür: `app.main`.
* Benzer şekilde `app/dependencies.py` dosyası da bir "module"’dür: `app.dependencies`.
* `app/routers/` adında bir alt dizin vardır ve içinde başka bir `__init__.py` dosyası bulunur; dolayısıyla bu bir "Python subpackage"’dir: `app.routers`.
* `app/routers/items.py` dosyası `app/routers/` package’i içinde olduğundan bir submodule’dür: `app.routers.items`.
* `app/routers/users.py` için de aynı şekilde, başka bir submodule’dür: `app.routers.users`.
* `app/internal/` adında bir alt dizin daha vardır ve içinde başka bir `__init__.py` dosyası bulunur; dolayısıyla bu da bir "Python subpackage"’dir: `app.internal`.
* Ve `app/internal/admin.py` dosyası başka bir submodule’dür: `app.internal.admin`.

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

Aynı dosya yapısı, yorumlarla birlikte:

```bash
.
├── app                  # "app" bir Python package'idir
│   ├── __init__.py      # bu dosya, "app"i bir "Python package" yapar
│   ├── main.py          # "main" module'ü, örn. import app.main
│   ├── dependencies.py  # "dependencies" module'ü, örn. import app.dependencies
│   └── routers          # "routers" bir "Python subpackage"idir
│   │   ├── __init__.py  # "routers"ı bir "Python subpackage" yapar
│   │   ├── items.py     # "items" submodule'ü, örn. import app.routers.items
│   │   └── users.py     # "users" submodule'ü, örn. import app.routers.users
│   └── internal         # "internal" bir "Python subpackage"idir
│       ├── __init__.py  # "internal"ı bir "Python subpackage" yapar
│       └── admin.py     # "admin" submodule'ü, örn. import app.internal.admin
```

## `APIRouter` { #apirouter }

Diyelim ki sadece kullanıcıları yönetmeye ayrılmış dosyanız `/app/routers/users.py` içindeki submodule olsun.

Kullanıcılarla ilgili *path operation*’ları, kodun geri kalanından ayrı tutmak istiyorsunuz; böylece düzenli kalır.

Ancak bu hâlâ aynı **FastAPI** uygulaması/web API’sinin bir parçasıdır (aynı "Python Package" içinde).

Bu module için *path operation*’ları `APIRouter` kullanarak oluşturabilirsiniz.

### `APIRouter` Import Edin { #import-apirouter }

`FastAPI` class’ında yaptığınız gibi import edip bir "instance" oluşturursunuz:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}

### `APIRouter` ile *Path Operations* { #path-operations-with-apirouter }

Sonra bunu kullanarak *path operation*’larınızı tanımlarsınız.

`FastAPI` class’ını nasıl kullanıyorsanız aynı şekilde kullanın:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

`APIRouter`’ı "mini bir `FastAPI`" class’ı gibi düşünebilirsiniz.

Aynı seçeneklerin hepsi desteklenir.

Aynı `parameters`, `responses`, `dependencies`, `tags`, vb.

/// tip | İpucu

Bu örnekte değişkenin adı `router`. Ancak istediğiniz gibi adlandırabilirsiniz.

///

Bu `APIRouter`’ı ana `FastAPI` uygulamasına ekleyeceğiz; ama önce dependency’lere ve bir diğer `APIRouter`’a bakalım.

## Dependencies { #dependencies }

Uygulamanın birden fazla yerinde kullanılacak bazı dependency’lere ihtiyacımız olacağını görüyoruz.

Bu yüzden onları ayrı bir `dependencies` module’üne koyuyoruz (`app/dependencies.py`).

Şimdi, özel bir `X-Token` header'ını okumak için basit bir dependency kullanalım:

{* ../../docs_src/bigger_applications/app_an_py310/dependencies.py hl[3,6:8] title["app/dependencies.py"] *}

/// tip | İpucu

Örneği basit tutmak için uydurma bir header kullanıyoruz.

Ancak gerçek senaryolarda, entegre [Security yardımcı araçlarını](security/index.md) kullanarak daha iyi sonuç alırsınız.

///

## `APIRouter` ile Başka Bir Module { #another-module-with-apirouter }

Diyelim ki uygulamanızdaki "items" ile ilgili endpoint'ler de `app/routers/items.py` module’ünde olsun.

Şunlar için *path operation*’larınız var:

* `/items/`
* `/items/{item_id}`

Bu, `app/routers/users.py` ile aynı yapıdadır.

Ancak biraz daha akıllı davranıp kodu sadeleştirmek istiyoruz.

Bu module’deki tüm *path operation*’ların şu ortak özelliklere sahip olduğunu biliyoruz:

* Path `prefix`: `/items`.
* `tags`: (tek bir tag: `items`).
* Ek `responses`.
* `dependencies`: hepsinin, oluşturduğumuz `X-Token` dependency’sine ihtiyacı var.

Dolayısıyla bunları her *path operation*’a tek tek eklemek yerine `APIRouter`’a ekleyebiliriz.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

Her *path operation*’ın path’i aşağıdaki gibi `/` ile başlamak zorunda olduğundan:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...prefix’in sonunda `/` olmamalıdır.

Yani bu örnekte prefix `/items` olur.

Ayrıca, bu router içindeki tüm *path operation*’lara uygulanacak bir `tags` listesi ve ek `responses` da ekleyebiliriz.

Ve router’daki tüm *path operation*’lara eklenecek, her request için çalıştırılıp çözülecek bir `dependencies` listesi de ekleyebiliriz.

/// tip | İpucu

[ *path operation decorator*’larındaki dependency’lerde](dependencies/dependencies-in-path-operation-decorators.md) olduğu gibi, *path operation function*’ınıza herhangi bir değer aktarılmayacağını unutmayın.

///

Sonuç olarak item path’leri artık:

* `/items/`
* `/items/{item_id}`

...tam da istediğimiz gibi olur.

* Hepsi, içinde tek bir string `"items"` bulunan bir tag listesiyle işaretlenir.
    * Bu "tags", özellikle otomatik interaktif dokümantasyon sistemleri (OpenAPI) için çok faydalıdır.
* Hepsi önceden tanımlı `responses`’ları içerir.
* Bu *path operation*’ların hepsinde, öncesinde `dependencies` listesi değerlendirilip çalıştırılır.
    * Ayrıca belirli bir *path operation* içinde dependency tanımlarsanız, **onlar da çalıştırılır**.
    * Önce router dependency’leri, sonra decorator’daki [`dependencies`](dependencies/dependencies-in-path-operation-decorators.md), sonra da normal parametre dependency’leri çalışır.
    * Ayrıca [`scopes` ile `Security` dependency’leri](../advanced/security/oauth2-scopes.md) de ekleyebilirsiniz.

/// tip | İpucu

`APIRouter` içinde `dependencies` kullanmak, örneğin bir grup *path operation* için kimlik doğrulamayı zorunlu kılmakta kullanılabilir. Dependency’leri tek tek her birine eklemeseniz bile.

///

/// check | Ek bilgi

`prefix`, `tags`, `responses` ve `dependencies` parametreleri (çoğu başka örnekte olduğu gibi) kod tekrarını önlemenize yardımcı olan, **FastAPI**’nin bir özelliğidir.

///

### Dependency'leri Import Edin { #import-the-dependencies }

Bu kod `app.routers.items` module’ünde, yani `app/routers/items.py` dosyasında duruyor.

Dependency function’ını ise `app.dependencies` module’ünden, yani `app/dependencies.py` dosyasından almamız gerekiyor.

Bu yüzden dependency’ler için `..` ile relative import kullanıyoruz:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[3] title["app/routers/items.py"] *}

#### Relative Import Nasıl Çalışır { #how-relative-imports-work }

/// tip | İpucu

Import’ların nasıl çalıştığını çok iyi biliyorsanız, bir sonraki bölüme geçin.

///

Tek bir nokta `.`, örneğin:

```Python
from .dependencies import get_token_header
```

şu anlama gelir:

* Bu module’ün (yani `app/routers/items.py` dosyasının) bulunduğu package içinden başla ( `app/routers/` dizini)...
* `dependencies` module’ünü bul (`app/routers/dependencies.py` gibi hayali bir dosya)...
* ve oradan `get_token_header` function’ını import et.

Ama o dosya yok; bizim dependency’lerimiz `app/dependencies.py` dosyasında.

Uygulama/dosya yapımızın nasıl göründüğünü hatırlayın:

<img src="/img/tutorial/bigger-applications/package.drawio.svg">

---

İki nokta `..`, örneğin:

```Python
from ..dependencies import get_token_header
```

şu anlama gelir:

* Bu module’ün bulunduğu package içinden başla (`app/routers/` dizini)...
* üst (parent) package’e çık (`app/` dizini)...
* burada `dependencies` module’ünü bul (`app/dependencies.py` dosyası)...
* ve oradan `get_token_header` function’ını import et.

Bu doğru şekilde çalışır! 🎉

---

Aynı şekilde, üç nokta `...` kullansaydık:

```Python
from ...dependencies import get_token_header
```

şu anlama gelirdi:

* Bu module’ün bulunduğu package içinden başla (`app/routers/` dizini)...
* üst package’e çık (`app/` dizini)...
* sonra bir üstüne daha çık (orada bir üst package yok; `app` en üst seviye 😱)...
* ve orada `dependencies` module’ünü bul (`app/dependencies.py` dosyası)...
* ve oradan `get_token_header` function’ını import et.

Bu, `app/` dizininin üstünde, kendi `__init__.py` dosyası olan başka bir package’e işaret ederdi. Ama bizde böyle bir şey yok. Dolayısıyla bu örnekte hata verirdi. 🚨

Artık nasıl çalıştığını bildiğinize göre, uygulamalarınız ne kadar karmaşık olursa olsun relative import’ları kullanabilirsiniz. 🤓

### Özel `tags`, `responses` ve `dependencies` Ekleyin { #add-some-custom-tags-responses-and-dependencies }

`/items` prefix’ini ya da `tags=["items"]` değerini her *path operation*’a tek tek eklemiyoruz; çünkü bunları `APIRouter`’a ekledik.

Ama yine de belirli bir *path operation*’a uygulanacak _ek_ `tags` tanımlayabilir, ayrıca o *path operation*’a özel `responses` ekleyebiliriz:

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[30:31] title["app/routers/items.py"] *}

/// tip | İpucu

Bu son *path operation*’da tag kombinasyonu şöyle olur: `["items", "custom"]`.

Ayrıca dokümantasyonda iki response da görünür: biri `404`, diğeri `403`.

///

## Ana `FastAPI` { #the-main-fastapi }

Şimdi `app/main.py` module’üne bakalım.

Burada `FastAPI` class’ını import edip kullanırsınız.

Bu dosya, uygulamanızda her şeyi bir araya getiren ana dosya olacak.

Mantığın büyük kısmı artık kendi module’lerinde yaşayacağı için ana dosya oldukça basit kalır.

### `FastAPI` Import Edin { #import-fastapi }

Normal şekilde bir `FastAPI` class’ı oluşturursunuz.

Hatta her `APIRouter` için olan dependency’lerle birleştirilecek [global dependencies](dependencies/global-dependencies.md) bile tanımlayabilirsiniz:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}

### `APIRouter` Import Edin { #import-the-apirouter }

Şimdi `APIRouter` içeren diğer submodule’leri import ediyoruz:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

`app/routers/users.py` ve `app/routers/items.py` dosyaları aynı Python package’i olan `app`’in parçası olan submodule’ler olduğu için, onları "relative import" ile tek bir nokta `.` kullanarak import edebiliriz.

### Import Nasıl Çalışır { #how-the-importing-works }

Şu bölüm:

```Python
from .routers import items, users
```

şu anlama gelir:

* Bu module’ün (yani `app/main.py` dosyasının) bulunduğu package içinden başla (`app/` dizini)...
* `routers` subpackage’ini bul (`app/routers/` dizini)...
* ve buradan `items` submodule’ünü (`app/routers/items.py`) ve `users` submodule’ünü (`app/routers/users.py`) import et...

`items` module’ünün içinde `router` adında bir değişken vardır (`items.router`). Bu, `app/routers/items.py` dosyasında oluşturduğumuz aynı değişkendir; bir `APIRouter` nesnesidir.

Sonra aynı işlemi `users` module’ü için de yaparız.

Ayrıca şöyle de import edebilirdik:

```Python
from app.routers import items, users
```

/// info | Bilgi

İlk sürüm "relative import"tur:

```Python
from .routers import items, users
```

İkinci sürüm "absolute import"tur:

```Python
from app.routers import items, users
```

Python Packages ve Modules hakkında daha fazlası için, [Python'ın Modules ile ilgili resmi dokümantasyonunu](https://docs.python.org/3/tutorial/modules.html) okuyun.

///

### İsim Çakışmalarını Önleyin { #avoid-name-collisions }

`items` submodule’ünü doğrudan import ediyoruz; sadece içindeki `router` değişkenini import etmiyoruz.

Çünkü `users` submodule’ünde de `router` adlı başka bir değişken var.

Eğer şöyle sırayla import etseydik:

```Python
from .routers.items import router
from .routers.users import router
```

`users` içindeki `router`, `items` içindeki `router`’ın üstüne yazardı ve ikisini aynı anda kullanamazdık.

Bu yüzden ikisini de aynı dosyada kullanabilmek için submodule’leri doğrudan import ediyoruz:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[5] title["app/main.py"] *}

### `users` ve `items` için `APIRouter`’ları Dahil Edin { #include-the-apirouters-for-users-and-items }

Şimdi `users` ve `items` submodule’lerindeki `router`’ları dahil edelim:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info | Bilgi

`users.router`, `app/routers/users.py` dosyasının içindeki `APIRouter`’ı içerir.

`items.router` ise `app/routers/items.py` dosyasının içindeki `APIRouter`’ı içerir.

///

`app.include_router()` ile her bir `APIRouter`’ı ana `FastAPI` uygulamasına ekleyebiliriz.

Böylece o router içindeki tüm route’lar uygulamanın bir parçası olarak dahil edilir.

/// note | Teknik Detaylar

Aslında içeride, `APIRouter` içinde tanımlanan her *path operation* için bir *path operation* oluşturur.

Yani perde arkasında, her şey tek bir uygulamaymış gibi çalışır.

///

/// check | Ek bilgi

Router’ları dahil ederken performans konusunda endişelenmeniz gerekmez.

Bu işlem mikrosaniyeler sürer ve sadece startup sırasında olur.

Dolayısıyla performansı etkilemez. ⚡

///

### Özel `prefix`, `tags`, `responses` ve `dependencies` ile Bir `APIRouter` Dahil Edin { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Şimdi, kurumunuzun size `app/internal/admin.py` dosyasını verdiğini düşünelim.

Bu dosyada, kurumunuzun birden fazla proje arasında paylaştığı bazı admin *path operation*’larını içeren bir `APIRouter` var.

Bu örnekte çok basit olacak. Ancak kurum içinde başka projelerle paylaşıldığı için, bunu değiştirip `prefix`, `dependencies`, `tags` vs. doğrudan `APIRouter`’a ekleyemediğimizi varsayalım:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

Yine de bu `APIRouter`’ı dahil ederken özel bir `prefix` ayarlamak istiyoruz ki tüm *path operation*’ları `/admin` ile başlasın; ayrıca bu projede hâlihazırda kullandığımız `dependencies` ile güvene almak, `tags` ve `responses` eklemek istiyoruz.

Orijinal `APIRouter`’ı değiştirmeden, bu parametreleri `app.include_router()`’a vererek hepsini tanımlayabiliriz:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

Böylece orijinal `APIRouter` değişmeden kalır; yani aynı `app/internal/admin.py` dosyasını kurum içindeki diğer projelerle de paylaşmaya devam edebiliriz.

Sonuç olarak, uygulamamızda `admin` module’ündeki her bir *path operation* şunlara sahip olur:

* `/admin` prefix’i.
* `admin` tag’i.
* `get_token_header` dependency’si.
* `418` response’u. 🍵

Ancak bu sadece bizim uygulamamızdaki o `APIRouter` için geçerlidir; onu kullanan diğer kodlar için değil.

Dolayısıyla örneğin diğer projeler aynı `APIRouter`’ı farklı bir authentication yöntemiyle kullanabilir.

### Bir *Path Operation* Dahil Edin { #include-a-path-operation }

*Path operation*’ları doğrudan `FastAPI` uygulamasına da ekleyebiliriz.

Burada bunu yapıyoruz... sadece yapabildiğimizi göstermek için 🤷:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[21:23] title["app/main.py"] *}

ve `app.include_router()` ile eklenen diğer tüm *path operation*’larla birlikte doğru şekilde çalışır.

/// info | Çok Teknik Detaylar

**Not**: Bu oldukça teknik bir detay; büyük ihtimalle **direkt geçebilirsiniz**.

---

`APIRouter`’lar "mount" edilmez; uygulamanın geri kalanından izole değildir.

Çünkü *path operation*’larını OpenAPI şemasına ve kullanıcı arayüzlerine dahil etmek istiyoruz.

Onları tamamen izole edip bağımsız şekilde "mount" edemediğimiz için, *path operation*’lar doğrudan eklenmek yerine "klonlanır" (yeniden oluşturulur).

///

## `pyproject.toml` İçinde `entrypoint` Yapılandırın { #configure-the-entrypoint-in-pyproject-toml }

FastAPI `app` nesneniz `app/main.py` içinde yaşadığına göre, `pyproject.toml` dosyanızda `entrypoint`’i şöyle yapılandırabilirsiniz:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

bu da şu import’a denktir:

```python
from app.main import app
```

Böylece `fastapi` komutu uygulamanızı nerede bulacağını bilir.

/// Note | Not

Komuta dosya yolunu da verebilirsiniz, örneğin:

```console
$ fastapi dev app/main.py
```

Ama o zaman her `fastapi` komutunu çalıştırdığınızda doğru yolu hatırlayıp geçirmeniz gerekir.

Ayrıca, diğer araçlar uygulamayı bulamayabilir; örneğin [VS Code Eklentisi](../editor-support.md) veya [FastAPI Cloud](https://fastapicloud.com). Bu yüzden `pyproject.toml` içinde `entrypoint` kullanmanız önerilir.

///

## Otomatik API Dokümanını Kontrol Edin { #check-the-automatic-api-docs }

Şimdi uygulamanızı çalıştırın:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ve dokümanları [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) adresinde açın.

Tüm submodule’lerdeki path’leri, doğru path’ler (ve prefix’ler) ve doğru tag’lerle birlikte içeren otomatik API dokümanını göreceksiniz:

<img src="/img/tutorial/bigger-applications/image01.png">

## Aynı Router'ı Farklı `prefix` ile Birden Fazla Kez Dahil Edin { #include-the-same-router-multiple-times-with-different-prefix }

`.include_router()` ile aynı router’ı farklı prefix’ler kullanarak birden fazla kez de dahil edebilirsiniz.

Örneğin aynı API’yi `/api/v1` ve `/api/latest` gibi farklı prefix’ler altında sunmak için faydalı olabilir.

Bu, muhtemelen ihtiyacınız olmayan ileri seviye bir kullanımdır; ancak gerekirse diye mevcut.

## Bir `APIRouter`’ı Başka Birine Dahil Edin { #include-an-apirouter-in-another }

Bir `APIRouter`’ı `FastAPI` uygulamasına dahil ettiğiniz gibi, bir `APIRouter`’ı başka bir `APIRouter`’a da şu şekilde dahil edebilirsiniz:

```Python
router.include_router(other_router)
```

`router`’ı `FastAPI` uygulamasına dahil etmeden önce bunu yaptığınızdan emin olun; böylece `other_router` içindeki *path operation*’lar da dahil edilmiş olur.
