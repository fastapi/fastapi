# İlk Adımlar { #first-steps }

En sade FastAPI dosyası şu şekilde görünür:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Yukarıdakini `main.py` adlı bir dosyaya kopyalayın.

Canlı sunucuyu çalıştırın:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Çıktıda, şuna benzer bir satır göreceksiniz:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Bu satır, uygulamanızın yerel makinenizde hangi URL'de sunulduğunu gösterir.

### Kontrol Edelim { #check-it }

Tarayıcınızı açıp <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> adresine gidin.

Şu şekilde bir JSON response göreceksiniz:

```JSON
{"message": "Hello World"}
```

### Etkileşimli API Dokümantasyonu { #interactive-api-docs }

Şimdi <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresine gidin.

Otomatik etkileşimli API dokümantasyonunu ( <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> tarafından sağlanan) göreceksiniz:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatif API Dokümantasyonu { #alternative-api-docs }

Ve şimdi <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine gidin.

Alternatif otomatik dokümantasyonu ( <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> tarafından sağlanan) göreceksiniz:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI**, API'ları tanımlamak için **OpenAPI** standardını kullanarak tüm API'nızın tamamını içeren bir "şema" üretir.

#### "Şema" { #schema }

"Şema", bir şeyin tanımı veya açıklamasıdır. Onu uygulayan kod değil, sadece soyut bir açıklamadır.

#### API "şeması" { #api-schema }

Bu durumda, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>, API'nızın şemasını nasıl tanımlayacağınızı belirleyen bir şartnamedir.

Bu şema tanımı, API path'leriniz, alabilecekleri olası parametreler vb. şeyleri içerir.

#### Veri "şeması" { #data-schema }

"Şema" terimi, JSON içeriği gibi bazı verilerin şeklini de ifade edebilir.

Bu durumda, JSON attribute'ları ve sahip oldukları veri türleri vb. anlamına gelir.

#### OpenAPI ve JSON Schema { #openapi-and-json-schema }

OpenAPI, API'nız için bir API şeması tanımlar. Ve bu şema, JSON veri şemaları standardı olan **JSON Schema** kullanılarak API'nız tarafından gönderilen ve alınan verilerin tanımlarını (veya "şemalarını") içerir.

#### `openapi.json` Dosyasına Göz At { #check-the-openapi-json }

Ham OpenAPI şemasının nasıl göründüğünü merak ediyorsanız, FastAPI otomatik olarak tüm API'nızın açıklamalarını içeren bir JSON (şema) üretir.

Bunu doğrudan şuradan görebilirsiniz: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Şuna benzer bir şekilde başlayan bir JSON gösterecektir:

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

#### OpenAPI Ne İşe Yarar? { #what-is-openapi-for }

OpenAPI şeması, dahil edilen iki etkileşimli dokümantasyon sistemine güç veren şeydir.

Ve OpenAPI tabanlı düzinelerce alternatif vardır. **FastAPI** ile oluşturulmuş uygulamanıza bu alternatiflerden herhangi birini kolayca ekleyebilirsiniz.

Ayrıca, API'nızla iletişim kuran istemciler için otomatik olarak kod üretmekte de kullanabilirsiniz. Örneğin frontend, mobil veya IoT uygulamaları.

### Uygulamanızı Yayınlayın (opsiyonel) { #deploy-your-app-optional }

İsterseniz FastAPI uygulamanızı <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>'a deploy edebilirsiniz; henüz katılmadıysanız gidip bekleme listesine yazılın. 🚀

Zaten bir **FastAPI Cloud** hesabınız varsa (bekleme listesinden sizi davet ettiysek 😉), uygulamanızı tek komutla deploy edebilirsiniz.

Deploy etmeden önce giriş yaptığınızdan emin olun:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Ardından uygulamanızı deploy edin:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

Bu kadar! Artık uygulamanıza o URL üzerinden erişebilirsiniz. ✨

## Adım Adım Özetleyelim { #recap-step-by-step }

### Adım 1: `FastAPI` import edin { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI`, API'nız için tüm işlevselliği sağlayan bir Python class'ıdır.

/// note | Teknik Detaylar

`FastAPI`, doğrudan `Starlette`'ten miras alan bir class'tır.

<a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>'in tüm işlevselliğini `FastAPI` ile de kullanabilirsiniz.

///

### Adım 2: bir `FastAPI` "instance"ı oluşturun { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Burada `app` değişkeni `FastAPI` class'ının bir "instance"ı olacaktır.

Bu, tüm API'nızı oluşturmak için ana etkileşim noktası olacaktır.

### Adım 3: bir *path operation* oluşturun { #step-3-create-a-path-operation }

#### Path { #path }

Buradaki "Path", URL'in ilk `/` işaretinden başlayarak son kısmını ifade eder.

Yani, şu şekilde bir URL'de:

```
https://example.com/items/foo
```

...path şöyle olur:

```
/items/foo
```

/// info | Bilgi

Bir "path" genellikle "endpoint" veya "route" olarak da adlandırılır.

///

Bir API oluştururken, "path", "concerns" ve "resources" ayrımını yapmanın ana yoludur.

#### Operation { #operation }

Burada "Operation", HTTP "method"larından birini ifade eder.

Şunlardan biri:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...ve daha egzotik olanlar:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTP protokolünde, her bir path ile bu "method"lardan biri (veya birden fazlası) ile iletişim kurabilirsiniz.

---

API oluştururken, normalde belirli bir aksiyon için bu spesifik HTTP method'larını kullanırsınız.

Normalde şunları kullanırsınız:

* `POST`: veri oluşturmak için.
* `GET`: veri okumak için.
* `PUT`: veriyi güncellemek için.
* `DELETE`: veriyi silmek için.

Bu nedenle, OpenAPI'da HTTP method'larının her birine "operation" denir.

Biz de bunlara "**operation**" diyeceğiz.

#### Bir *path operation decorator* tanımlayın { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")`, **FastAPI**'a hemen altındaki fonksiyonun şuraya giden request'leri ele almakla sorumlu olduğunu söyler:

* path `/`
* <dfn title="bir HTTP GET methodu"><code>get</code> operation</dfn> kullanarak

/// info | `@decorator` Bilgisi

Python'daki `@something` söz dizimi "decorator" olarak adlandırılır.

Onu bir fonksiyonun üstüne koyarsınız. Güzel, dekoratif bir şapka gibi (sanırım terim de buradan geliyor).

Bir "decorator", altındaki fonksiyonu alır ve onunla bir şey yapar.

Bizim durumumuzda bu decorator, **FastAPI**'a altındaki fonksiyonun **path** `/` ile **operation** `get`'e karşılık geldiğini söyler.

Bu, "**path operation decorator**"dır.

///

Diğer operation'ları da kullanabilirsiniz:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Ve daha egzotik olanları:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | İpucu

Her bir operation'ı (HTTP method'unu) istediğiniz gibi kullanmakta özgürsünüz.

**FastAPI** herhangi bir özel anlamı zorunlu kılmaz.

Buradaki bilgiler bir gereklilik değil, bir kılavuz olarak sunulmaktadır.

Örneğin GraphQL kullanırken, normalde tüm aksiyonları yalnızca `POST` operation'ları kullanarak gerçekleştirirsiniz.

///

### Adım 4: **path operation function**'ı tanımlayın { #step-4-define-the-path-operation-function }

Bu bizim "**path operation function**"ımız:

* **path**: `/`.
* **operation**: `get`.
* **function**: "decorator"ün altındaki fonksiyondur (`@app.get("/")`'in altındaki).

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

Bu bir Python fonksiyonudur.

**FastAPI**, "`/`" URL'ine `GET` operation kullanarak bir request aldığında bu fonksiyonu çağıracaktır.

Bu durumda, bu bir `async` fonksiyondur.

---

Bunu `async def` yerine normal bir fonksiyon olarak da tanımlayabilirsiniz:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | Not

Eğer farkı bilmiyorsanız, [Async: *"Aceleniz mi var?"*](../async.md#in-a-hurry){.internal-link target=_blank} sayfasına bakın.

///

### Adım 5: içeriği döndürün { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

Bir `dict`, `list`, `str`, `int` vb. tekil değerler döndürebilirsiniz.

Ayrıca Pydantic modelleri de döndürebilirsiniz (bununla ilgili daha fazlasını ileride göreceksiniz).

Otomatik olarak JSON'a dönüştürülecek (ORM'ler vb. dahil) başka birçok nesne ve model vardır. En sevdiğiniz nesne/model'leri kullanmayı deneyin; büyük ihtimalle zaten destekleniyordur.

### Adım 6: Deploy edin { #step-6-deploy-it }

Uygulamanızı tek komutla **<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**'a deploy edin: `fastapi deploy`. 🎉

#### FastAPI Cloud Hakkında { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**, **FastAPI**'ın arkasındaki aynı yazar ve ekip tarafından geliştirilmiştir.

Minimum eforla bir API'ı **oluşturma**, **deploy etme** ve **erişme** sürecini sadeleştirir.

FastAPI ile uygulama geliştirirken yaşadığınız aynı **developer experience**'ı, onları buluta **deploy etme** aşamasına da taşır. 🎉

FastAPI Cloud, *FastAPI and friends* açık kaynak projelerinin birincil sponsoru ve finansman sağlayıcısıdır. ✨

#### Diğer cloud sağlayıcılarına deploy edin { #deploy-to-other-cloud-providers }

FastAPI açık kaynaklıdır ve standartlara dayanır. FastAPI uygulamalarını seçtiğiniz herhangi bir cloud sağlayıcısına deploy edebilirsiniz.

FastAPI uygulamalarını onlarla deploy etmek için cloud sağlayıcınızın kılavuzlarını takip edin. 🤓

## Özet { #recap }

* `FastAPI` import edin.
* Bir `app` instance'ı oluşturun.
* `@app.get("/")` gibi decorator'ları kullanarak bir **path operation decorator** yazın.
* Bir **path operation function** tanımlayın; örneğin `def root(): ...`.
* `fastapi dev` komutunu kullanarak geliştirme sunucusunu çalıştırın.
* İsterseniz `fastapi deploy` ile uygulamanızı deploy edin.
