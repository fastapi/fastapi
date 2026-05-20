# Sıkı Content-Type Kontrolü { #strict-content-type-checking }

Varsayılan olarak FastAPI, JSON request body'leri için sıkı Content-Type header kontrolü uygular. Bu, JSON request'lerin body'lerinin JSON olarak parse edilebilmesi için geçerli bir Content-Type header'ı (örn. application/json) içermesi gerektiği anlamına gelir.

## CSRF Riski { #csrf-risk }

Bu varsayılan davranış, çok belirli bir senaryoda bir sınıf Cross-Site Request Forgery (CSRF) saldırılarına karşı koruma sağlar.

Bu saldırılar, tarayıcıların aşağıdaki durumlarda herhangi bir CORS preflight kontrolü yapmadan script’lerin request göndermesine izin vermesinden faydalanır:

- bir Content-Type header’ı yoksa (örn. body olarak Blob ile fetch() kullanıldığında)
- ve herhangi bir kimlik doğrulama bilgisi gönderilmiyorsa.

Bu tür saldırılar özellikle şu durumlarda önemlidir:

- uygulama yerelde (örn. localhost’ta) veya dahili bir ağda çalışıyorsa
- ve uygulamada hiç kimlik doğrulama yoksa, aynı ağdan gelen her request’in güvenilir olduğu varsayılıyorsa.

## Örnek Saldırı { #example-attack }

Yerelde çalışan bir AI agent’ı (yapay zeka ajanı) çalıştırmanın bir yolunu geliştirdiğinizi düşünün.

Bir API sunuyor:

```
http://localhost:8000/v1/agents/multivac
```

Ayrıca bir frontend var:

```
http://localhost:8000
```

/// tip | İpucu

İkisinin de host’u aynıdır.

///

Frontend’i kullanarak AI agent’a sizin adınıza işler yaptırabiliyorsunuz.

Uygulama yerelde çalıştığı ve açık internette olmadığı için, sadece yerel ağa güvenip herhangi bir kimlik doğrulama kurmamaya karar verdiniz.

Kullanıcılarınızdan biri de bunu indirip yerelde çalıştırabilir.

Sonra kötü niyetli bir web sitesini açabilir, örneğin:

```
https://evilhackers.example.com
```

Ve bu kötü niyetli site, body olarak Blob kullanan fetch() ile yerel API’ye request’ler gönderebilir:

```
http://localhost:8000/v1/agents/multivac
```

Kötü niyetli sitenin host’u ile yerel uygulamanın host’u farklı olsa bile, tarayıcı şu nedenlerle bir CORS preflight isteği tetiklemez:

- Herhangi bir kimlik doğrulama yoktur, bu nedenle credential göndermesi gerekmez.
- Tarayıcı, Content-Type header’ı eksik olduğundan JSON gönderildiğini düşünmez.

Böylece kötü niyetli site, yerel AI agent’ın kullanıcının eski patronuna sinirli mesajlar göndermesini sağlayabilir... ya da daha kötüsü. 😅

## Açık İnternet { #open-internet }

Uygulamanız açık internetteyse “ağa güvenmez” ve kimlik doğrulama olmadan kimsenin ayrıcalıklı request’ler göndermesine izin vermezsiniz.

Saldırganlar tarayıcı etkileşimine ihtiyaç duymadan basitçe bir script çalıştırıp API’nize request gönderebilir, bu yüzden muhtemelen ayrıcalıklı endpoint’leri zaten güvenceye almışsınızdır.

Bu durumda bu saldırı/riski sizler için geçerli değildir.

Bu risk ve saldırı, esasen uygulama sadece yerel ağda çalıştığında ve tek koruma varsayımının bu olduğu durumlarda önemlidir.

## Content-Type Olmadan Gelen Request’lere İzin Vermek { #allowing-requests-without-content-type }

Content-Type header’ı göndermeyen client’ları desteklemeniz gerekiyorsa, strict kontrolü strict_content_type=False ayarıyla kapatabilirsiniz:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

Bu ayarla, Content-Type header’ı olmayan request’lerin body’si JSON olarak parse edilir. Bu, FastAPI’nin eski sürümlerindeki davranışla aynıdır.

/// info | Bilgi

Bu davranış ve yapılandırma FastAPI 0.132.0’da eklendi.

///
