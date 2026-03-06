# Ek Status Code'ları { #additional-status-codes }

Varsayılan olarak **FastAPI**, response'ları bir `JSONResponse` kullanarak döndürür; *path operation*'ınızdan döndürdüğünüz içeriği bu `JSONResponse`'un içine yerleştirir.

Varsayılan status code'u veya *path operation* içinde sizin belirlediğiniz status code'u kullanır.

## Ek status code'ları { #additional-status-codes_1 }

Ana status code'a ek olarak başka status code'lar da döndürmek istiyorsanız, `JSONResponse` gibi bir `Response`'u doğrudan döndürerek bunu yapabilirsiniz ve ek status code'u doğrudan orada ayarlarsınız.

Örneğin, item'ları güncellemeye izin veren bir *path operation*'ınız olduğunu düşünelim; başarılı olduğunda 200 "OK" HTTP status code'unu döndürüyor olsun.

Ancak yeni item'ları da kabul etmesini istiyorsunuz. Ve item daha önce yoksa, onu oluşturup 201 "Created" HTTP status code'unu döndürsün.

Bunu yapmak için `JSONResponse` import edin ve içeriğinizi doğrudan onunla döndürün; istediğiniz `status_code`'u da ayarlayın:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | Uyarı

Yukarıdaki örnekte olduğu gibi bir `Response`'u doğrudan döndürdüğünüzde, response aynen olduğu gibi döndürülür.

Bir model ile serialize edilmez, vb.

İçinde olmasını istediğiniz veriyi taşıdığından emin olun ve değerlerin geçerli JSON olduğundan emin olun (eğer `JSONResponse` kullanıyorsanız).

///

/// note | Teknik Detaylar

`from starlette.responses import JSONResponse` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.responses` içindekileri `fastapi.responses` altında da sunar. Ancak mevcut response'ların çoğu doğrudan Starlette'ten gelir. `status` için de aynı durum geçerlidir.

///

## OpenAPI ve API docs { #openapi-and-api-docs }

Ek status code'ları ve response'ları doğrudan döndürürseniz, FastAPI sizin ne döndüreceğinizi önceden bilemeyeceği için bunlar OpenAPI şemasına (API docs) dahil edilmez.

Ancak bunu kodunuzda şu şekilde dokümante edebilirsiniz: [Ek Response'lar](additional-responses.md){.internal-link target=_blank}.
