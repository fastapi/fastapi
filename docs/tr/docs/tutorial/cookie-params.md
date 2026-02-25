# Cookie (Çerez) Parametreleri { #cookie-parameters }

`Query` ve `Path` parametrelerini tanımladığınız şekilde Cookie parametreleri tanımlayabilirsiniz.

## `Cookie`'yi Import Edin { #import-cookie }

Öncelikle, `Cookie`'yi import edin:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` Parametrelerini Tanımlayın { #declare-cookie-parameters }

Ardından, `Path` ve `Query` ile aynı yapıyı kullanarak Cookie parametrelerini tanımlayın.

Varsayılan değeri ve tüm ekstra doğrulama veya annotation parametrelerini tanımlayabilirsiniz:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Teknik Detaylar

`Cookie`, `Path` ve `Query`'nin "kardeş" sınıfıdır. O da aynı ortak `Param` sınıfından miras alır.

Ancak `fastapi`'dan `Query`, `Path`, `Cookie` ve diğerlerini import ettiğinizde, bunlar aslında özel sınıflar döndüren fonksiyonlardır, bunu unutmayın.

///

/// info | Bilgi

Cookie'leri tanımlamak için `Cookie` kullanmanız gerekir, aksi halde parametreler query parametreleri olarak yorumlanır.

///

/// info | Bilgi

**Tarayıcılar cookie'leri** özel şekillerde ve arka planda işlediği için, **JavaScript**'in onlara dokunmasına kolayca izin **vermezler**.

`/docs` adresindeki **API docs UI**'a giderseniz, *path operation*'larınız için cookie'lerin **dokümantasyonunu** görebilirsiniz.

Ancak **veriyi doldurup** "Execute" düğmesine tıklasanız bile, docs UI **JavaScript** ile çalıştığı için cookie'ler gönderilmez ve herhangi bir değer yazmamışsınız gibi bir **hata** mesajı görürsünüz.

///

## Özet { #recap }

`Query` ve `Path` ile aynı ortak deseni kullanarak, cookie'leri `Cookie` ile tanımlayın.
