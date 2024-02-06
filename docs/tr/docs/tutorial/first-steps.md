# İlk Adımlar

En sade FastAPI dosyası şu şekilde görünür:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Yukarıda ki içeriği bir `main.py` dosyasına kopyalayın.

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

!!! note "Not"
    `uvicorn main:app` komutu şunu ifade eder:

    * `main`: `main.py` dosyası (Python "modülü").
    * `app`: `main.py` dosyası içerisinde `app = FastAPI()` satırıyla oluşturulan nesne.
    * `--reload`: Kod içerisinde değişiklik yapıldığında sunucunun yeniden başlatılmasını sağlar. Yalnızca geliştirme aşamasında kullanın.

Çıktı olarak şöyle bir satır göreceksiniz:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Bu satır, yerel makinenizde uygulamanızın çalıştığı bağlantıyı gösterir.

### Kontrol Edelim

Tarayıcınızı açıp <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> bağlantısına gidin.

Şu lekilde bir JSON yanıtı göreceksiniz:

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

#### API "Şemaları"

Bu durumda, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>, API şemasını nasıl tanımlayacağınızı belirten şartnamedir.

Bu şema tanımı, API yollarınızla birlikte aldıkları olası parametreleri gibi tanımlamaları içerir.

#### Veri "Şeması"

"Şema" terimi, JSON içeriği gibi bazı verilerin şeklini de ifade edebilir.

Bu durumda, JSON özellikleri ve sahip oldukları veri türleri gibi anlamına gelir.

#### OpenAPI ve JSON Şema

OpenAPI, API'niz için bir API şeması tanımlar. Ve bu şema, JSON veri şemaları standardı olan **JSON Şema** kullanılarak API'niz tarafından gönderilen ve alınan verilerin tanımlarını (veya "şemalarını") içerir.

#### `openapi.json` kontrol et

OpenAPI şemasının nasıl göründüğünü merak ediyorsanız, FastAPI otomatik olarak tüm API'ınızın tanımlamalarını içeren bir JSON (şema) oluşturur.

Doğrudan şu bağlantıda görebilirsiniz: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

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

#### OpenAPI Ne İçindir?

OpenAPI şeması, FastAPI projesinde bulunan iki etkileşimli dokümantasyon sistemine güç veren şeydir.

OpenAPI'ya dayalı düzinelerce alternativ etkileşimli dokümantasyon aracı mevcuttur. **FastAPI** ile oluşturulmuş uygulamanıza bu alternatiflerden herhangi birini kolayca ekleyebilirsiniz.

Ayrıca API'ınızla iletişim kuracak istemciler için otomatik olarak kod oluşturabilirsiniz. Mesela, önyüz, mobil veya IoT uygulamaları gibi istemciler.

## Adım Adım Özetleyelim

### Adım 1: `FastAPI`yı Projemize Dahil Edelim

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI`, API'niz için tüm fonksiyonları sağlayan bir Python sınıfıdır.

!!! note "Teknik Detaylar"
    `FastAPI` doğrudan `Starlette`'i miras alan bir sınıftır.

    Tüm <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> fonksiyonlarını `FastAPI` ile kullanabilirsiniz.

### Adım 2: Bir `FastAPI` "örneği" oluşturalım

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Burada `app` değişkeni `FastAPI` sınıfının bir örneği olacaktır.

Bu tüm API'yı oluşturmak için ana etkileşim noktası olacaktır.

`uvicorn` komutunda atıfta bulunulan `app` ile aynıdır.

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Uygulamanızı aşağıdaki gibi oluşturursanız:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

Ve bunu `main.py` dosyasına yerleştirirseniz eğer `uvicorn` komutunu şu şekilde çalıştırabilirsiniz:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Adım 3: *Yol Operasyonu* Oluşturmak

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

!!! info "Bilgi"
    "Yol" genellikle "<abbr title="Endpoint: Bitim Noktası">endpoint</abbr>" veya "<abbr title="Route: Yönlendirme/Yön">route</abbr>" olarak adlandırılabilir.

Bir API oluştururken, "yol", "kaynakları" ile "endişeleri" ayırmanın ana yoludur.

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

HTTP protokolünde, bu "metodlardan" birini (veya daha fazlasını) kullanarak her yol ile iletişim kurabilirsiniz.

---

API'lar oluştururkan, belirli bir amaca hizmet eden belirli HTTP methodlarını kullanırsınız.

Normalde kullanılan:

* `POST`: veri oluşturmak.
* `GET`: veri okumak.
* `PUT`: veriyi güncellemek.
* `DELETE`: veriyi silmek.

Bu nedenle, OpenAPI'de HTTP methodlarından her birine "operasyon" denir.

Bizde onlara "**operasyonlar**" diyeceğiz.

#### Bir *Yol Operasyonu Dekoratörü* Tanımlayalım

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` **FastAPI**'a hemen altındaki fonksiyonun aşağıdaki durumlardan sorumlu olduğunu söyler:

* <abbr title="Bir HTTP GET metodu"><code>get</code> operasyonu</abbr> ile
* `/` yoluna gelen istekler

!!! info "`@decorator` Bilgisi"
    Python'da `@something` sözdizimi "<abbr title="Decorator">dekoratör</abbr>" olarak adlandırılır.

    Dekoratörü bir fonksiyonun üzerine koyarsınız. Dekoratif bir şapka gibi (sanırım terim buradan geliyor).

    Bir "dekoratör" hemen altında bulunan fonksiyonu alır ve o fonksiyon ile bazı işlemler gerçekleştirir.

    Bizim durumumzda kullandığımız dekoratör **FastAPI**'a altındaki fonksiyonun `/` yoluna gelen `get` metodlu isteklerden sorumlu olduğunu söyler.

    Bu bir **yol operasyon dekoratörü**.

Ayrıca diğer operasyonları de kullanabilirsiniz:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Daha az kullanılanları da kullanabilirsiniz:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip "İpucu"
    Her işlemi (HTTP metod) istediğiniz gibi kullanmakta özgürsünüz.

    **FastAPI** herhangi bir özel amacı veya anlamı olması konusunda ısrarcı olmaz.

    Buradaki bilgiler bir gereklilik değil, bir kılavuz olarak sunulmaktadır.

    Mesela GraphQL kullanırkan genelde tüm işlemleri yalnızca `POST` operasyonunu kullanarak gerçekleştirirsiniz.

### Adım 4: **Yol Operasyonu Fonksiyonunu** Tanımlayın

Aşağıdakiler bizim **yol operasyonu fonksiyonlarımızdır**:

* **yol**: `/`
* **operasyon**: `get`
* **fonksiyon**: "dekorar"ün (`@app.get("/")`) altındaki fonksiyondur.

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Bu bir Python fonksiyonudur.

Bir `GET` işlemi kullanarak "`/`" bağlantısına bir istek geldiğinde **FastAPI** tarafından çağrılır.

Bu durumda bir `async` fonksiyonudur.

---

Bunu `async def` yerine normal bir fonksiyon olarakta tanımlayabilirsiniz.

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note "Not"
    Eğer farkı bilmiyorsanız, [Async: *"Aceleniz mi var?"*](../async.md#in-a-hurry){.internal-link target=_blank} sayfasını kontrol edebilirsiniz.

### Adım 5: İçeriği Geri Döndürün

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Bir `dict`, `list`veya `str`, `int` gibi tekil değerler döndürebilirsiniz.

Ayrıca, Pydantic modellerini de döndürebilirsiniz (bununla ilgili daha sonra ayrıntılı bilgi göreceksiniz).

Otomatik olarak JSON'a dönüştürülecek (ORM'ler vb. dahil) başka birçok nesne ve model vardır. En beğendiklerinizi kullanmayı deneyin, yüksek ihtimalle destekleniyordur.

## Özet

* `FastAPI`'yı projemize dahil ettik.
* Bir `app` örneği oluşturduk.
* **yol operasyonu dekoratörü** (`@app.get("/")` gibi) yazdık.
* **yol operasyonu fonksiyonu** (`def root(): ...` gibi) yazdık.
* Geliştirme sunucumuzu (`uvicorn main:app --reload` gibi) çalıştırdık.
