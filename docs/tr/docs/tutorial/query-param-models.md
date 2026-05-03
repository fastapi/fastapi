# Query Parameter Modelleri { #query-parameter-models }

Birbirleriyle ilişkili bir **query parameter** grubunuz varsa, bunları tanımlamak için bir **Pydantic model** oluşturabilirsiniz.

Böylece **modeli yeniden kullanabilir**, **birden fazla yerde** tekrar tekrar kullanabilir ve tüm parametreler için validation (doğrulama) ile metadata’yı tek seferde tanımlayabilirsiniz. 😎

/// note | Not

Bu özellik FastAPI `0.115.0` sürümünden beri desteklenmektedir. 🤓

///

## Pydantic Model ile Query Parameters { #query-parameters-with-a-pydantic-model }

İhtiyacınız olan **query parameter**’ları bir **Pydantic model** içinde tanımlayın, ardından parametreyi `Query` olarak belirtin:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI**, request’teki **query parameter**’lardan **her field** için veriyi **extract** eder ve tanımladığınız Pydantic model’i size verir.

## Dokümanları Kontrol Edin { #check-the-docs }

Query parameter’ları `/docs` altındaki dokümantasyon arayüzünde görebilirsiniz:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Ek Query Parameter'ları Yasaklayın { #forbid-extra-query-parameters }

Bazı özel kullanım senaryolarında (muhtemelen çok yaygın değil), almak istediğiniz query parameter’ları **kısıtlamak** isteyebilirsiniz.

Pydantic’in model konfigürasyonunu kullanarak `extra` field’ları `forbid` edebilirsiniz:

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

Bir client, **query parameter**’larda **ek (extra)** veri göndermeye çalışırsa, **error** response alır.

Örneğin client, değeri `plumbus` olan bir `tool` query parameter’ı göndermeye çalışırsa:

```http
https://example.com/items/?limit=10&tool=plumbus
```

`tool` query parameter’ına izin verilmediğini söyleyen bir **error** response alır:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## Özet { #summary }

**FastAPI** içinde **query parameter**’ları tanımlamak için **Pydantic model**’leri kullanabilirsiniz. 😎

/// tip | İpucu

Spoiler: cookie ve header’ları tanımlamak için de Pydantic model’leri kullanabilirsiniz; ancak bunu tutorial’ın ilerleyen bölümlerinde göreceksiniz. 🤫

///
