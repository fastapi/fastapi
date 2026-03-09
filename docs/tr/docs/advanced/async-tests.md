# Async Testler { #async-tests }

Sağlanan `TestClient` ile **FastAPI** uygulamalarınızı nasıl test edeceğinizi zaten gördünüz. Şimdiye kadar yalnızca senkron testler yazdık, yani `async` fonksiyonlar kullanmadan.

Testlerinizde asenkron fonksiyonlar kullanabilmek faydalı olabilir; örneğin veritabanınızı asenkron olarak sorguluyorsanız. Diyelim ki FastAPI uygulamanıza request gönderilmesini test etmek ve ardından async bir veritabanı kütüphanesi kullanırken backend'in doğru veriyi veritabanına başarıyla yazdığını doğrulamak istiyorsunuz.

Bunu nasıl çalıştırabileceğimize bir bakalım.

## pytest.mark.anyio { #pytest-mark-anyio }

Testlerimizde asenkron fonksiyonlar çağırmak istiyorsak, test fonksiyonlarımızın da asenkron olması gerekir. AnyIO bunun için güzel bir plugin sağlar; böylece bazı test fonksiyonlarının asenkron olarak çağrılacağını belirtebiliriz.

## HTTPX { #httpx }

**FastAPI** uygulamanız `async def` yerine normal `def` fonksiyonları kullanıyor olsa bile, altta yatan yapı hâlâ bir `async` uygulamadır.

`TestClient`, standart pytest kullanarak normal `def` test fonksiyonlarınızın içinden asenkron FastAPI uygulamasını çağırmak için içeride bazı “sihirli” işlemler yapar. Ancak bu sihir, onu asenkron fonksiyonların içinde kullandığımızda artık çalışmaz. Testlerimizi asenkron çalıştırdığımızda, test fonksiyonlarımızın içinde `TestClient` kullanamayız.

`TestClient`, <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> tabanlıdır ve neyse ki API'yi test etmek için HTTPX'i doğrudan kullanabiliriz.

## Örnek { #example }

Basit bir örnek için, [Bigger Applications](../tutorial/bigger-applications.md){.internal-link target=_blank} ve [Testing](../tutorial/testing.md){.internal-link target=_blank} bölümlerinde anlatılana benzer bir dosya yapısı düşünelim:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

`main.py` dosyası şöyle olur:

{* ../../docs_src/async_tests/app_a_py310/main.py *}

`test_main.py` dosyasında `main.py` için testler yer alır, artık şöyle görünebilir:

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## Çalıştırma { #run-it }

Testlerinizi her zamanki gibi şu şekilde çalıştırabilirsiniz:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## Detaylı Anlatım { #in-detail }

`@pytest.mark.anyio` marker'ı, pytest'e bu test fonksiyonunun asenkron olarak çağrılması gerektiğini söyler:

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | İpucu

Test fonksiyonu artık `TestClient` kullanırken eskiden olduğu gibi sadece `def` değil, `async def`.

///

Ardından app ile bir `AsyncClient` oluşturup `await` kullanarak ona async request'ler gönderebiliriz.

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

Bu, şu kullanıma denktir:

```Python
response = client.get('/')
```

...ki daha önce request'leri `TestClient` ile bu şekilde gönderiyorduk.

/// tip | İpucu

Yeni `AsyncClient` ile async/await kullandığımızı unutmayın; request asenkron çalışır.

///

/// warning | Uyarı

Uygulamanız lifespan event'lerine dayanıyorsa, `AsyncClient` bu event'leri tetiklemez. Tetiklendiklerinden emin olmak için <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a> paketindeki `LifespanManager`'ı kullanın.

///

## Diğer Asenkron Fonksiyon Çağrıları { #other-asynchronous-function-calls }

Test fonksiyonu artık asenkron olduğundan, testlerinizde FastAPI uygulamanıza request göndermenin yanında başka `async` fonksiyonları da (çağırıp `await` ederek) kodunuzun başka yerlerinde yaptığınız gibi aynı şekilde kullanabilirsiniz.

/// tip | İpucu

Testlerinize asenkron fonksiyon çağrıları entegre ederken `RuntimeError: Task attached to a different loop` hatasıyla karşılaşırsanız (ör. <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB'nin MotorClient</a> kullanımı), event loop gerektiren nesneleri yalnızca async fonksiyonların içinde oluşturmanız gerektiğini unutmayın; örneğin bir `@app.on_event("startup")` callback'i içinde.

///
