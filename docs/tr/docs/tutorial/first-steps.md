# İlk Adımlar

En sade FastAPI dosyası şu şekilde görünür:

{* ../../docs_src/first_steps/tutorial001.py *}

Yukarıdaki içeriği bir `main.py` dosyasına kopyalayalım.

Uygulamayı çalıştıralım:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

/// note | Not

`uvicorn main:app` komutunu şu şekilde açıklayabiliriz:

* `main`: dosya olan `main.py` (yani Python "modülü").
* `app`: ise `main.py` dosyasının içerisinde `app = FastAPI()` satırında oluşturduğumuz `FastAPI` nesnesi.
* `--reload`: kod değişikliklerinin ardından sunucuyu otomatik olarak yeniden başlatır. Bu parameteyi sadece geliştirme aşamasında kullanmalıyız.

///

Çıktı olarak şöyle bir satır ile karşılaşacaksınız:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Bu satır, yerel makinenizde uygulamanızın çalıştığı bağlantıyı gösterir.

### Kontrol Edelim

Tarayıcınızı açıp <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> bağlantısına gidin.

Şu şekilde bir JSON yanıtı ile karşılaşacağız:

```JSON
{"message": "Hello World"}
```

### Etkileşimli API Dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> bağlantısını açalım.

<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tarafından sağlanan otomatik etkileşimli bir API dokümantasyonu göreceğiz:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatif API Dokümantasyonu

Şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> bağlantısını açalım.

<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tarafından sağlanan otomatik dokümantasyonu göreceğiz:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI**, **OpenAPI** standardını kullanarak tüm API'ınızın tamamını tanımlayan bir "şema" oluşturur.

#### "Şema"

"Şema", bir şeyin tanımı veya açıklamasıdır. Geliştirilen koddan ziyade soyut bir açıklamadır.

#### API "Şeması"

Bu durumda, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>, API şemasını nasıl tanımlayacağınızı belirten bir şartnamedir.

Bu şema tanımı, API yollarınızla birlikte yollarınızın aldığı olası parametreler gibi tanımlamaları içerir.

#### Veri "Şeması"

"Şema" terimi, JSON içeriği gibi bazı verilerin şeklini de ifade edebilir.

Bu durumda, JSON özellikleri ve sahip oldukları veri türleri gibi anlamlarına gelir.

#### OpenAPI ve JSON Şema

OpenAPI, API'niz için bir API şeması tanımlar. Ve bu şema, JSON veri şemaları standardı olan **JSON Şema** kullanılarak API'niz tarafından gönderilen ve alınan verilerin tanımlarını (veya "şemalarını") içerir.

#### `openapi.json` Dosyasına Göz At

Ham OpenAPI şemasının nasıl göründüğünü merak ediyorsanız, FastAPI otomatik olarak tüm API'ınızın tanımlamalarını içeren bir JSON (şeması) oluşturur.

Bu şemayı direkt olarak <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a> bağlantısından görüntüleyebilirsiniz.

Aşağıdaki gibi başlayan bir JSON ile karşılaşacaksınız:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI Ne İşe Yarar?

OpenAPI şeması, FastAPI projesinde bulunan iki etkileşimli dokümantasyon sistemine güç veren şeydir.

OpenAPI'ya dayalı düzinelerce alternatif etkileşimli dokümantasyon aracı mevcuttur. **FastAPI** ile oluşturulmuş uygulamanıza bu alternatiflerden herhangi birini kolayca ekleyebilirsiniz.

Ayrıca, API'ınızla iletişim kuracak önyüz, mobil veya IoT uygulamaları gibi istemciler için otomatik olarak kod oluşturabilirsiniz.

## Adım Adım Özetleyelim

### Adım 1: `FastAPI`yı Projemize Dahil Edelim

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI`, API'niz için tüm işlevselliği sağlayan bir Python sınıfıdır.

/// note | Teknik Detaylar

`FastAPI` doğrudan `Starlette`'i miras alan bir sınıftır.

<a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>'in tüm işlevselliğini `FastAPI` ile de kullanabilirsiniz.

///

### Adım 2: Bir `FastAPI` "Örneği" Oluşturalım

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

Burada `app` değişkeni `FastAPI` sınıfının bir örneği olacaktır.

Bu, tüm API'yı oluşturmak için ana etkileşim noktası olacaktır.

Bu `app` değişkeni, `uvicorn` komutunda atıfta bulunulan değişkenin ta kendisidir.

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Uygulamanızı aşağıdaki gibi oluşturursanız:

{* ../../docs_src/first_steps/tutorial002.py hl[3] *}

Ve bunu `main.py` dosyasına yerleştirirseniz eğer `uvicorn` komutunu şu şekilde çalıştırabilirsiniz:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Adım 3: Bir *Yol Operasyonu* Oluşturalım

#### <abbr title="Yol: Path">Yol</abbr>

Burada "yol" bağlantıda bulunan ilk `/` ile başlayan ve sonrasında gelen kısmı ifade eder.

Yani, şu şekilde bir bağlantıda:

```
https://example.com/items/foo
```

... yol şöyle olur:

```
/items/foo
```

/// info | Bilgi

"Yol" genellikle "<abbr title="Endpoint: Bitim Noktası">endpoint</abbr>" veya "<abbr title="Route: Yönlendirme/Yön">route</abbr>" olarak adlandırılır.

///

Bir API oluştururken, "yol", "kaynaklar" ile "endişeleri" ayırmanın ana yöntemidir.

#### Operasyonlar

Burada "operasyon" HTTP "metodlarından" birini ifade eder.

Bunlardan biri:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...veya daha az kullanılan diğerleri:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP protokolünde, bu "metodlardan" birini (veya daha fazlasını) kullanarak her bir yol ile iletişim kurabilirsiniz.

---

API oluştururkan, belirli bir amaca hizmet eden belirli HTTP metodlarını kullanırsınız.

Normalde kullanılan:

* `POST`: veri oluşturmak.
* `GET`: veri okumak.
* `PUT`: veriyi güncellemek.
* `DELETE`: veriyi silmek.

Bu nedenle, OpenAPI'da HTTP metodlarından her birine "operasyon" denir.

Biz de onları "**operasyonlar**" olarak adlandıracağız.

#### Bir *Yol Operasyonu Dekoratörü* Tanımlayalım

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

`@app.get("/")` dekoratörü, **FastAPI**'a hemen altındaki fonksiyonun aşağıdaki durumlardan sorumlu olduğunu söyler:

* <abbr title="Bir HTTP GET metodu"><code>get</code> operasyonu</abbr> ile
* `/` yoluna gelen istekler

/// info | `@decorator` Bilgisi

Python'da `@something` sözdizimi "<abbr title="Decorator">dekoratör</abbr>" olarak adlandırılır.

Dekoratörler, dekoratif bir şapka gibi (sanırım terim buradan geliyor) fonksiyonların üzerlerine yerleştirilirler.

Bir "dekoratör" hemen altında bulunan fonksiyonu alır ve o fonksiyon ile bazı işlemler gerçekleştirir.

Bizim durumumuzda, kullandığımız dekoratör, **FastAPI**'a altındaki fonksiyonun `/` yoluna gelen `get` metodlu isteklerden sorumlu olduğunu söyler.

Bu bir **yol operasyonu dekoratörüdür**.

///

Ayrıca diğer operasyonları da kullanabilirsiniz:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Daha az kullanılanları da kullanabilirsiniz:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | İpucu

Her işlemi (HTTP metod) istediğiniz gibi kullanmakta özgürsünüz.

**FastAPI** herhangi bir özel amacı veya anlamı olması konusunda ısrarcı olmaz.

Buradaki bilgiler bir gereklilik değil, bir kılavuz olarak sunulmaktadır.

Mesela GraphQL kullanırkan genelde tüm işlemleri yalnızca `POST` operasyonunu kullanarak gerçekleştirirsiniz.

///

### Adım 4: **Yol Operasyonu Fonksiyonunu** Tanımlayın

Aşağıdaki, bizim **yol operasyonu fonksiyonumuzdur**:

* **yol**: `/`
* **operasyon**: `get`
* **fonksiyon**: "dekoratör"ün (`@app.get("/")`'in) altındaki fonksiyondur.

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Bu bir Python fonksiyonudur.

Bu fonksiyon bir `GET` işlemi kullanılarak "`/`" bağlantısına bir istek geldiğinde **FastAPI** tarafından çağrılır.

Bu durumda bu fonksiyon bir `async` fonksiyondur.

---

Bu fonksiyonu `async def` yerine normal bir fonksiyon olarak da tanımlayabilirsiniz.

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note | Not

Eğer farkı bilmiyorsanız, [Async: *"Aceleniz mi var?"*](../async.md#in-a-hurry){.internal-link target=_blank} sayfasını kontrol edebilirsiniz.

///

### Adım 5: İçeriği Geri Döndürün

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Bir `dict`, `list` veya `str`, `int` gibi tekil değerler döndürebilirsiniz.

Ayrıca, Pydantic modelleri de döndürebilirsiniz (bu konu ileriki aşamalarda irdelenecektir).

Otomatik olarak JSON'a dönüştürülecek (ORM'ler vb. dahil) başka birçok nesne ve model vardır. En beğendiklerinizi kullanmayı deneyin, yüksek ihtimalle destekleniyordur.

## Özet

* `FastAPI`'yı projemize dahil ettik.
* Bir `app` örneği oluşturduk.
* Bir **yol operasyonu dekoratörü** (`@app.get("/")` gibi) yazdık.
* Bir **yol operasyonu fonksiyonu** (`def root(): ...` gibi) yazdık.
* Geliştirme sunucumuzu (`uvicorn main:app --reload` gibi) çalıştırdık.
