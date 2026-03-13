# Request Dosyaları { #request-files }

İstemcinin upload edeceği dosyaları `File` kullanarak tanımlayabilirsiniz.

/// info | Bilgi

Upload edilen dosyaları alabilmek için önce <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> yükleyin.

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, aktive ettiğinizden ve ardından paketi yüklediğinizden emin olun. Örneğin:

```console
$ pip install python-multipart
```

Bunun nedeni, upload edilen dosyaların "form data" olarak gönderilmesidir.

///

## `File` Import Edin { #import-file }

`fastapi` içinden `File` ve `UploadFile` import edin:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## `File` Parametrelerini Tanımlayın { #define-file-parameters }

`Body` veya `Form` için yaptığınız gibi dosya parametreleri oluşturun:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info | Bilgi

`File`, doğrudan `Form`’dan türeyen bir sınıftır.

Ancak unutmayın: `fastapi` içinden `Query`, `Path`, `File` ve diğerlerini import ettiğinizde, bunlar aslında özel sınıflar döndüren fonksiyonlardır.

///

/// tip | İpucu

File body’leri tanımlamak için `File` kullanmanız gerekir; aksi halde parametreler query parametreleri veya body (JSON) parametreleri olarak yorumlanır.

///

Dosyalar "form data" olarak upload edilir.

*path operation function* parametrenizin tipini `bytes` olarak tanımlarsanız, **FastAPI** dosyayı sizin için okur ve içeriği `bytes` olarak alırsınız.

Bunun, dosyanın tüm içeriğinin bellekte tutulacağı anlamına geldiğini unutmayın. Küçük dosyalar için iyi çalışır.

Ancak bazı durumlarda `UploadFile` kullanmak size fayda sağlayabilir.

## `UploadFile` ile Dosya Parametreleri { #file-parameters-with-uploadfile }

Tipi `UploadFile` olan bir dosya parametresi tanımlayın:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

`UploadFile` kullanmanın `bytes`’a göre birkaç avantajı vardır:

* Parametrenin varsayılan değerinde `File()` kullanmak zorunda değilsiniz.
* "Spooled" bir dosya kullanır:
    * Belirli bir maksimum boyuta kadar bellekte tutulan, bu limiti aşınca diske yazılan bir dosya.
* Bu sayede görüntüler, videolar, büyük binary’ler vb. gibi büyük dosyalarda tüm belleği tüketmeden iyi çalışır.
* Upload edilen dosyadan metadata alabilirsiniz.
* <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> bir `async` arayüze sahiptir.
* <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> nesnesini dışa açar; bunu, file-like nesne bekleyen diğer library’lere doğrudan geçebilirsiniz.

### `UploadFile` { #uploadfile }

`UploadFile` şu attribute’lara sahiptir:

* `filename`: Upload edilen orijinal dosya adını içeren bir `str` (örn. `myimage.jpg`).
* `content_type`: Content type’ı (MIME type / media type) içeren bir `str` (örn. `image/jpeg`).
* `file`: Bir <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (bir <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> nesne). Bu, "file-like" nesne bekleyen diğer fonksiyonlara veya library’lere doğrudan verebileceğiniz gerçek Python file nesnesidir.

`UploadFile` şu `async` method’lara sahiptir. Bunların hepsi altta ilgili dosya method’larını çağırır (dahili `SpooledTemporaryFile` kullanarak).

* `write(data)`: Dosyaya `data` (`str` veya `bytes`) yazar.
* `read(size)`: Dosyadan `size` (`int`) kadar byte/karakter okur.
* `seek(offset)`: Dosyada `offset` (`int`) byte pozisyonuna gider.
    * Örn. `await myfile.seek(0)` dosyanın başına gider.
    * Bu, özellikle bir kez `await myfile.read()` çalıştırdıysanız ve sonra içeriği yeniden okumaya ihtiyaç duyuyorsanız faydalıdır.
* `close()`: Dosyayı kapatır.

Bu method’ların hepsi `async` olduğundan, bunları "await" etmeniz gerekir.

Örneğin, bir `async` *path operation function* içinde içeriği şöyle alabilirsiniz:

```Python
contents = await myfile.read()
```

Normal bir `def` *path operation function* içindeyseniz `UploadFile.file`’a doğrudan erişebilirsiniz, örneğin:

```Python
contents = myfile.file.read()
```

/// note | `async` Teknik Detaylar

`async` method’ları kullandığınızda, **FastAPI** dosya method’larını bir threadpool içinde çalıştırır ve bunları await eder.

///

/// note | Starlette Teknik Detaylar

**FastAPI**’nin `UploadFile`’ı doğrudan **Starlette**’in `UploadFile`’ından türetilmiştir; ancak **Pydantic** ve FastAPI’nin diğer parçalarıyla uyumlu olması için bazı gerekli eklemeler yapar.

///

## "Form Data" Nedir { #what-is-form-data }

HTML formları (`<form></form>`) veriyi server’a gönderirken normalde JSON’dan farklı, veri için "özel" bir encoding kullanır.

**FastAPI**, JSON yerine bu veriyi doğru yerden okuyacağından emin olur.

/// note | Teknik Detaylar

Formlardan gelen veri, dosya içermiyorsa normalde "media type" olarak `application/x-www-form-urlencoded` ile encode edilir.

Ancak form dosya içeriyorsa `multipart/form-data` olarak encode edilir. `File` kullanırsanız, **FastAPI** dosyaları body’nin doğru kısmından alması gerektiğini bilir.

Bu encoding’ler ve form alanları hakkında daha fazla okumak isterseniz <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla Geliştirici Ağı">MDN</abbr> web dokümanlarındaki <code>POST</code></a> sayfasına bakın.

///

/// warning | Uyarı

Bir *path operation* içinde birden fazla `File` ve `Form` parametresi tanımlayabilirsiniz, ancak JSON olarak almayı beklediğiniz `Body` alanlarını ayrıca tanımlayamazsınız; çünkü request body `application/json` yerine `multipart/form-data` ile encode edilmiş olur.

Bu, **FastAPI**’nin bir kısıtı değildir; HTTP protocol’ünün bir parçasıdır.

///

## Opsiyonel Dosya Upload { #optional-file-upload }

Standart type annotation’ları kullanıp varsayılan değeri `None` yaparak bir dosyayı opsiyonel hale getirebilirsiniz:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## Ek Metadata ile `UploadFile` { #uploadfile-with-additional-metadata }

Ek metadata ayarlamak için `UploadFile` ile birlikte `File()` da kullanabilirsiniz. Örneğin:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## Birden Fazla Dosya Upload { #multiple-file-uploads }

Aynı anda birden fazla dosya upload etmek mümkündür.

Bu dosyalar, "form data" ile gönderilen aynı "form field" ile ilişkilendirilir.

Bunu kullanmak için `bytes` veya `UploadFile` listesini tanımlayın:

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

Tanımladığınız gibi, `bytes` veya `UploadFile`’lardan oluşan bir `list` alırsınız.

/// note | Teknik Detaylar

`from starlette.responses import HTMLResponse` da kullanabilirsiniz.

**FastAPI**, geliştiriciye kolaylık olsun diye `starlette.responses` modülünü `fastapi.responses` olarak da sağlar. Ancak mevcut response’ların çoğu doğrudan Starlette’ten gelir.

///

### Ek Metadata ile Birden Fazla Dosya Upload { #multiple-file-uploads-with-additional-metadata }

Daha önce olduğu gibi, `UploadFile` için bile ek parametreler ayarlamak amacıyla `File()` kullanabilirsiniz:

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## Özet { #recap }

Request’te (form data olarak gönderilen) upload edilecek dosyaları tanımlamak için `File`, `bytes` ve `UploadFile` kullanın.
