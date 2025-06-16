# Ek Durum Kodları

**FastAPI** varsayılan olarak, *yol operasyonu* ile döndürdüğünüz içeriği `JSONResponse`'ın içerisinde yerleştirerek yanıtları döndürecektir.

Varsayılan durum kodunu veya *yol operasyonu* ile belirlediğiniz durum kodunu kullanacaktır.

## Ek Durum Kodları

Varsayılan durum kodunun dışında ek durum kodları döndürmek istiyorsanız, bunu doğrudan bir `Response` döndürerek yapabilirsiniz, örneğin bir `JSONResponse` ile ek durum kodunu doğrudan belirleyebilirsiniz.

Örneğin, öğeleri güncellemeye izin veren ve başarılı olduğunda her şeyin yolunda olduğunu belirten "200" HTTP durum kodunu döndüren bir *yol operasyonu* oluşturmak istediğinizi varsayalım.

Aynı zamanda, yeni öğeler kabul etmek istiyorsunuz ve bu öğereler mevcut değilse öğeleri oluşturmak ve "Oluşturuldu" anlamına gelen 201 HTTP durum kodunu döndürmek istiyorsunuz.

Bunun için `JSONResponse`'ı projenize dahil edin ve içeriğinizi doğrudan `JSONResponse` içerisinde istediğiniz `status_code` ile birlikte yanıt olarak döndürün:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | Uyarı

Yukarıdaki örnekte olduğu gibi bir `Response` döndürdüğünüzde, doğrudan döndürülecektir.

Bu yanıt herhangi bir modelle dönüştürülme işlemine tabi tutulmayacaktır.

Yanıtın, istediğiniz veriye sahip olduğundan ve (eğer `JSONResponse` kullanıyorsanız) değerlerin geçerli JSON olduğundan emin olun.

///

/// note | Teknik Detaylar

Projenize dahil etmek için `from starlette.responses import JSONResponse` kullanabilirsiniz.

**FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.responses`'ı `fastapi.responses` olarak sağlar. Ancak mevcut yanıtların çoğu doğrudan Starlette'den gelir. Aynı durum `status` için de geçerlidir.

///

## OpenAPI ve API Dokümantasyonu

Eğer ek durum kodları ve yanıtlarını doğrudan döndürürseniz, bunlar OpenAPI şemasına (API belgeleri) dahil edilmeyecektir, çünkü FastAPI'ın önceden ne döndüreceğinizi bilmesi için bir yol yoktur.

Ancak [Additional Responses](additional-responses.md){.internal-link target=_blank} sayfasında belirtildiği gibi "ek yanıtlar" kullanarak, bunu kodunuzda dokümante edebilirsiniz.
