# Form Verisi { #form-data }

JSON yerine form alanları almanız gerektiğinde `Form` kullanabilirsiniz.

/// info | Bilgi

Formları kullanmak için önce <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> paketini kurun.

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan emin olun, onu aktive edin ve ardından örneğin şöyle kurun:

```console
$ pip install python-multipart
```

///

## `Form`'u Import Edin { #import-form }

`Form`'u `fastapi`'den import edin:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## `Form` Parametrelerini Tanımlayın { #define-form-parameters }

Form parametrelerini `Body` veya `Query` için yaptığınız gibi oluşturun:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

Örneğin, OAuth2 spesifikasyonunun kullanılabileceği ("password flow" olarak adlandırılan) yollardan birinde, form alanları olarak `username` ve `password` göndermek gerekir.

<abbr title="specification - spesifikasyon">spec</abbr> alanların isimlerinin birebir `username` ve `password` olmasını ve JSON değil form alanları olarak gönderilmesini gerektirir.

`Form` ile `Body` (ve `Query`, `Path`, `Cookie`) ile yaptığınız aynı konfigurasyonları (validasyon, örnekler, bir alias (ör. `username` yerine `user-name`), vb.) bildirebilirsiniz.

/// info | Bilgi

`Form`, doğrudan `Body`'den miras alan bir sınıftır.

///

/// tip | İpucu

Form gövdelerini bildirmek için `Form`'u açıkça kullanmanız gerekir; çünkü bu olmadan parametreler query parametreleri veya gövde (JSON) parametreleri olarak yorumlanır.

///

## "Form Alanları" Hakkında { #about-form-fields }

HTML formlarının (`<form></form>`) verileri sunucuya gönderme şekli normalde bu veriler için JSON'dan farklı "özel" bir kodlama kullanır.

**FastAPI** bu veriyi JSON yerine doğru yerden okuduğundan emin olur.

/// note | Teknik Detaylar

Formlardan gelen veriler normalde "media type" `application/x-www-form-urlencoded` kullanılarak kodlanır.

Ancak form dosyalar içerdiğinde `multipart/form-data` olarak kodlanır. Bir sonraki bölümde dosyaların işlenmesi hakkında okuyacaksınız.

Bu kodlamalar ve form alanları hakkında daha fazla bilgi edinmek isterseniz <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs for <code>POST</code></a> sayfasına gidin.

///

/// warning | Uyarı

Bir *path operation* içinde birden fazla `Form` parametresi bildirebilirsiniz, ancak JSON olarak almayı beklediğiniz `Body` alanlarını da bildiremezsiniz; çünkü bu durumda request gövdesi `application/json` yerine `application/x-www-form-urlencoded` kullanılarak kodlanır.

Bu **FastAPI**'ın bir kısıtlaması değildir, HTTP protokolünün bir parçasıdır.

///

## Özet { #recap }

Form verisi input parametrelerini bildirmek için `Form` kullanın.
