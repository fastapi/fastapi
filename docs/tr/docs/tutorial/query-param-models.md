# Query Parameter Modelleri { #query-parameter-models }

Birbirleriyle ilişkili bir **query parameter** grubunuz varsa, bunları tanımlamak için bir **Pydantic model** oluşturabilirsiniz.

Böylece **modeli yeniden kullanabilir**, **birden fazla yerde** tekrar tekrar kullanabilir ve tüm parametreler için validation (doğrulama) ile metadata'yı tek seferde tanımlayabilirsiniz. 😎

/// note | Not

Bu özellik FastAPI `0.115.0` sürümünden beri desteklenmektedir. 🤓

///

## Pydantic Model ile Query Parameters { #query-parameters-with-a-pydantic-model }

İhtiyacınız olan **query parameter**'ları bir **Pydantic model** içinde tanımlayın, ardından parametreyi `Query` olarak belirtin:

{* ../../docs_src/query_param_models/tutorial001.py hl[9:13,17] *}

**FastAPI**, request'teki **query parameter**'lardan **her field** için veriyi **extract** eder ve tanımladığınız Pydantic model'i size verir.

## Dokümanları Kontrol Edin { #check-the-docs }

Query parameter'ları `/docs` altındaki dokümantasyon arayüzünde görebilirsiniz:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## Ek Query Parameter'ları Yasaklayın { #forbid-extra-query-parameters }

Bazı özel kullanım senaryolarında (muhtemelen çok yaygın değil), almak istediğiniz query parameter'ları **kısıtlamak** isteyebilirsiniz.

Pydantic'in model konfigürasyonunu kullanarak `extra` field'ları `forbid` edebilirsiniz:

{* ../../docs_src/query_param_models/tutorial002.py hl[10] *}

Bir client, **query parameter**'larda **ek (extra)** veri göndermeye çalışırsa, **error** response alır.

Örneğin client, değeri `plumbus` olan bir `tool` query parameter'ı göndermeye çalışırsa:

```http
https://example.com/items/?limit=10&tool=plumbus
```

`tool` query parameter'ına izin verilmediğini söyleyen bir **error** response alır:

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

## Parametre Modellerini Birleştirin { #combine-parameter-models }

Birden fazla query parameter modeli tanımlayabilir ve bunları tekil query parameter'larla veya dependency'lerle birleştirebilirsiniz.

{* ../../docs_src/query_param_models/tutorial003.py hl[9:15,20:22] *}

Request parametreleri aynı seviyede kalır.

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

Query string'de `pagination` veya `filters` anahtarları bulunmaz. Her model, kendi varsayılan değerleri, field validator'ları ve model validator'larıyla query parameter'ları bağımsız olarak doğrular. Modeller veya tekil parametreler dependency'lerde tanımlandığında da aynı durum geçerlidir.

Modeller aynı parametre adını veya alias'ı paylaşıyorsa, her model bu request parametresini bağımsız olarak doğrular. Bağımsız değerler için farklı adlar veya alias'lar kullanın. OpenAPI, dependency'lerle paylaşılan parametrelerde olduğu gibi, paylaşılan bir parametreyi yalnızca bir kez listeler. Bu nedenle, paylaşılan parametre tanımları aynı türü ve kısıtlamaları belirtmelidir.

Her modelin `extra` konfigürasyonu, diğer modellerde veya dependency'lerde tanımlananlar da dahil olmak üzere tüm query parameter'lara uygulanır. `extra="forbid"` kullanıldığında, modelin dışında kalan tüm parametreler reddedilir. `extra="allow"` kullanıldığında ise bu parametreler modele ek veriler olarak dahil edilir.

Bu, `Header` ve `Cookie` modelleri için de geçerlidir.

## İsteğe Bağlı Query Parameter Modelleri { #optional-query-parameter-models }

Grubu isteğe bağlı hale getirmek için query parameter modelini `| None` ile tanımlayın ve varsayılan değerini `None` olarak ayarlayın.

{* ../../docs_src/query_param_models/tutorial004.py hl[18] *}

Ne `start` ne de `end` gönderilirse, `date_range` değeri `None` olur. İkisinden biri gönderilirse, FastAPI modeli doğrular ve her iki field'ı da zorunlu kılar.

Varsayılan değer belirtmeden `| None` kullanıldığında parametre yine zorunludur.

Ek parametreler modelin `extra` konfigürasyonuna göre işlenir. Yok sayılan ek parametreler, modelin gönderilmiş sayılmasına neden olmaz.

OpenAPI, gruptaki field'ları ayrı ayrı listeler ve isteğe bağlı olarak işaretler.

İsteğe bağlı [header parameter modelleri](header-param-models.md#optional-header-parameter-models) ve [cookie parameter modelleri](cookie-param-models.md#optional-cookie-parameter-models) de tanımlayabilirsiniz.

## Özet { #summary }

**FastAPI** içinde **query parameter**'ları tanımlamak için **Pydantic model**'leri kullanabilirsiniz. 😎

/// tip | İpucu

Spoiler: cookie ve header'ları tanımlamak için de Pydantic model'leri kullanabilirsiniz; ancak bunu tutorial'ın ilerleyen bölümlerinde göreceksiniz. 🤫

///
