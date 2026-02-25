# Form Verisi { #form-data }

JSON yerine form alanlarını almanız gerektiğinde `Form` kullanabilirsiniz.

/// info | Bilgi

Formları kullanmak için önce <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> paketini kurun.

Bir [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, onu etkinleştirdiğinizden emin olun ve ardından örneğin şöyle kurun:

```console
$ pip install python-multipart
```

///

## `Form`'u Import Edin { #import-form }

`Form`'u `fastapi`'den import edin:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## `Form` Parametrelerini Tanımlayın { #define-form-parameters }

Form parametrelerini `Body` veya `Query` için yaptığınız gibi oluşturun:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

Örneğin OAuth2 spesifikasyonunun kullanılabileceği ("password flow" olarak adlandırılan) yollardan birinde, form alanları olarak bir `username` ve `password` göndermek zorunludur.

<dfn title="spesifikasyon">Spesifikasyon</dfn>, alanların adının tam olarak `username` ve `password` olmasını ve JSON değil form alanları olarak gönderilmesini gerektirir.

`Form` ile `Body` (ve `Query`, `Path`, `Cookie`) ile yaptığınız aynı konfigürasyonları tanımlayabilirsiniz; validasyon, örnekler, alias (örn. `username` yerine `user-name`) vb. dahil.

/// info | Bilgi

`Form`, doğrudan `Body`'den miras alan bir sınıftır.

///

/// tip | İpucu

Form gövdelerini tanımlamak için `Form`'u açıkça kullanmanız gerekir; çünkü bunu yapmazsanız parametreler query parametreleri veya body (JSON) parametreleri olarak yorumlanır.

///

## "Form Alanları" Hakkında { #about-form-fields }

HTML formlarının (`<form></form>`) verileri sunucuya gönderme şekli normalde bu veri için JSON'dan farklı "özel" bir encoding kullanır.

**FastAPI** bu veriyi JSON yerine doğru yerden okuyacaktır.

/// note | Teknik Detaylar

Formlardan gelen veri normalde "media type" `application/x-www-form-urlencoded` kullanılarak encode edilir.

Ancak form dosyalar içerdiğinde `multipart/form-data` olarak encode edilir. Dosyaları ele almayı bir sonraki bölümde okuyacaksınız.

Bu encoding'ler ve form alanları hakkında daha fazla okumak isterseniz, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla Geliştirici Ağı">MDN</abbr> web docs for <code>POST</code></a> sayfasına gidin.

///

/// warning | Uyarı

Bir *path operation* içinde birden fazla `Form` parametresi tanımlayabilirsiniz, ancak JSON olarak almayı beklediğiniz `Body` alanlarını da ayrıca tanımlayamazsınız; çünkü bu durumda request'in body'si `application/x-www-form-urlencoded` ile encode edilmiş olur.

Bu **FastAPI**'ın bir kısıtlaması değildir, HTTP protokolünün bir parçasıdır.

///

## Özet { #recap }

Form verisi girdi parametrelerini tanımlamak için `Form` kullanın.
