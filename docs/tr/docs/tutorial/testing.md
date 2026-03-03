# Test Etme { #testing }

<a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a> sayesinde **FastAPI** uygulamalarını test etmek kolay ve keyiflidir.

Temelde <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> üzerine kuruludur; HTTPX de Requests’i temel alarak tasarlandığı için oldukça tanıdık ve sezgiseldir.

Bununla birlikte **FastAPI** ile <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a>'i doğrudan kullanabilirsiniz.

## `TestClient` Kullanımı { #using-testclient }

/// info | Bilgi

`TestClient` kullanmak için önce <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>'i kurun.

Bir [Sanal Ortam](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu aktifleştirdiğinizden ve sonra kurulumu yaptığınızdan emin olun; örneğin:

```console
$ pip install httpx
```

///

`TestClient`'ı import edin.

**FastAPI** uygulamanızı ona vererek bir `TestClient` oluşturun.

Adı `test_` ile başlayan fonksiyonlar oluşturun (bu, `pytest`'in standart konvansiyonudur).

`TestClient` nesnesini `httpx` ile kullandığınız şekilde kullanın.

Kontrol etmeniz gereken şeyler için standart Python ifadeleriyle basit `assert` satırları yazın (bu da `pytest` standardıdır).

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | İpucu

Test fonksiyonlarının `async def` değil, normal `def` olduğuna dikkat edin.

Client'a yapılan çağrılar da `await` kullanılmadan, normal çağrılardır.

Bu sayede `pytest`'i ek bir karmaşıklık olmadan doğrudan kullanabilirsiniz.

///

/// note | Teknik Detaylar

İsterseniz `from starlette.testclient import TestClient` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.testclient`'ı `fastapi.testclient` üzerinden de sunar. Ancak asıl kaynak doğrudan Starlette'tır.

///

/// tip | İpucu

FastAPI uygulamanıza request göndermenin dışında testlerinizde `async` fonksiyonlar çağırmak istiyorsanız (örn. asenkron veritabanı fonksiyonları), ileri seviye bölümdeki [Asenkron Testler](../advanced/async-tests.md){.internal-link target=_blank} dokümanına göz atın.

///

## Testleri Ayırma { #separating-tests }

Gerçek bir uygulamada testlerinizi büyük ihtimalle farklı bir dosyada tutarsınız.

Ayrıca **FastAPI** uygulamanız birden fazla dosya/modül vb. ile de oluşturulmuş olabilir.

### **FastAPI** Uygulama Dosyası { #fastapi-app-file }

[Daha Büyük Uygulamalar](bigger-applications.md){.internal-link target=_blank}'te anlatılan şekilde bir dosya yapınız olduğunu varsayalım:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

`main.py` dosyasında **FastAPI** uygulamanız bulunuyor olsun:

{* ../../docs_src/app_testing/app_a_py310/main.py *}

### Test Dosyası { #testing-file }

Sonra testlerinizin olduğu bir `test_main.py` dosyanız olabilir. Bu dosya aynı Python package içinde (yani `__init__.py` dosyası olan aynı dizinde) durabilir:

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Bu dosya aynı package içinde olduğu için, `main` modülünden (`main.py`) `app` nesnesini import etmek üzere relative import kullanabilirsiniz:

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}

...ve test kodunu da öncekiyle aynı şekilde yazabilirsiniz.

## Test Etme: Genişletilmiş Örnek { #testing-extended-example }

Şimdi bu örneği genişletelim ve farklı parçaların nasıl test edildiğini görmek için daha fazla detay ekleyelim.

### Genişletilmiş **FastAPI** Uygulama Dosyası { #extended-fastapi-app-file }

Aynı dosya yapısıyla devam edelim:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Diyelim ki **FastAPI** uygulamanızın bulunduğu `main.py` dosyasında artık başka **path operations** da var.

Hata döndürebilecek bir `GET` operation'ı var.

Birden fazla farklı hata döndürebilecek bir `POST` operation'ı var.

Her iki *path operation* da `X-Token` header'ını gerektiriyor.

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### Genişletilmiş Test Dosyası { #extended-testing-file }

Sonrasında `test_main.py` dosyanızı genişletilmiş testlerle güncelleyebilirsiniz:

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}

Client'ın request içinde bir bilgi göndermesi gerektiğinde ve bunu nasıl yapacağınızı bilemediğinizde, `httpx` ile nasıl yapılacağını aratabilirsiniz (Google) ya da HTTPX’in tasarımı Requests’e dayandığı için `requests` ile nasıl yapıldığını da arayabilirsiniz.

Sonra testlerinizde aynısını uygularsınız.

Örn.:

* Bir *path* veya *query* parametresi geçirmek için, URL’nin kendisine ekleyin.
* JSON body göndermek için, `json` parametresine bir Python nesnesi (örn. bir `dict`) verin.
* JSON yerine *Form Data* göndermeniz gerekiyorsa, bunun yerine `data` parametresini kullanın.
* *headers* göndermek için, `headers` parametresine bir `dict` verin.
* *cookies* için, `cookies` parametresine bir `dict` verin.

Backend'e veri geçme hakkında daha fazla bilgi için (`httpx` veya `TestClient` kullanarak) <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX dokümantasyonu</a>'na bakın.

/// info | Bilgi

`TestClient`'ın Pydantic model'lerini değil, JSON'a dönüştürülebilen verileri aldığını unutmayın.

Testinizde bir Pydantic model'iniz varsa ve test sırasında verisini uygulamaya göndermek istiyorsanız, [JSON Uyumlu Encoder](encoder.md){.internal-link target=_blank} içinde açıklanan `jsonable_encoder`'ı kullanabilirsiniz.

///

## Çalıştırma { #run-it }

Bundan sonra yapmanız gereken tek şey `pytest`'i kurmaktır.

Bir [Sanal Ortam](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu aktifleştirdiğinizden ve sonra kurulumu yaptığınızdan emin olun; örneğin:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Dosyaları ve testleri otomatik olarak bulur, çalıştırır ve sonuçları size raporlar.

Testleri şu şekilde çalıştırın:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
