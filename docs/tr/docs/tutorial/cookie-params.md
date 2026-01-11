# Cookie Parametreleri { #cookie-parameters }

`Query` ve `Path` parametrelerini tanımladığınız şekilde Cookie parametreleri tanımlayabilirsiniz.

## `Cookie`'yi Import Edin { #import-cookie }

Önce `Cookie`'yi import edin:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` Parametrelerini Tanımlayın { #declare-cookie-parameters }

Sonra Cookie parametrelerini `Path` ve `Query` ile aynı yapıyı kullanarak tanımlayın.

Varsayılan değeri ve tüm ekstra doğrulama veya annotation parametrelerini tanımlayabilirsiniz:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Teknik Detaylar

`Cookie`, `Path` ve `Query`'nin "kardeş" sınıfıdır. O da aynı ortak `Param` sınıfından miras alır.

Ama `fastapi`'dan `Query`, `Path`, `Cookie` ve diğerlerini import ettiğinizde, bunların aslında özel sınıflar döndüren fonksiyonlar olduğunu unutmayın.

///

/// info | Bilgi

Cookie'leri tanımlamak için `Cookie` kullanmanız gerekir, aksi takdirde parametreler query parametreleri olarak yorumlanır.

///

/// info | Bilgi

**Tarayıcılar Cookie'leri** arka planda ve özel şekillerde işlediği için **JavaScript**'in onlara dokunmasına kolayca izin **vermezler**.

`/docs` altındaki **API dokümantasyonu arayüzü**ne giderseniz, *path operation*'larınız için Cookie'lerin **dokümantasyonunu** görebilirsiniz.

Ama **veriyi doldurup** "Execute"'a tıklasanız bile, dokümantasyon arayüzü **JavaScript** ile çalıştığı için Cookie'ler gönderilmez ve herhangi bir değer yazmamışsınız gibi bir **hata** mesajı görürsünüz.

///

## Özet { #recap }

Cookie'leri `Cookie` ile, `Query` ve `Path` ile aynı ortak kalıbı kullanarak tanımlayın.
