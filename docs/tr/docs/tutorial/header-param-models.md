# Header Parametre Modelleri { #header-parameter-models }

Birbiriyle ilişkili **header parametreleri**nden oluşan bir grubunuz varsa, bunları tanımlamak için bir **Pydantic model** oluşturabilirsiniz.

Bu sayede modeli **birden fazla yerde yeniden kullanabilir**, ayrıca tüm parametreler için doğrulamaları ve metadata bilgilerini tek seferde tanımlayabilirsiniz. 😎

/// note | Not

Bu özellik FastAPI `0.115.0` sürümünden beri desteklenmektedir. 🤓

///

## Pydantic Model ile Header Parametreleri { #header-parameters-with-a-pydantic-model }

İhtiyacınız olan **header parametreleri**ni bir **Pydantic model** içinde tanımlayın, ardından parametreyi `Header` olarak belirtin:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI**, request içindeki **headers** bölümünden **her alan** için veriyi **çıkarır** ve size tanımladığınız Pydantic model örneğini verir.

## Dokümanları Kontrol Edin { #check-the-docs }

Gerekli header'ları `/docs` altındaki doküman arayüzünde görebilirsiniz:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## Ek Header'ları Yasaklayın { #forbid-extra-headers }

Bazı özel kullanım senaryolarında (muhtemelen çok yaygın değil), kabul etmek istediğiniz header'ları **kısıtlamak** isteyebilirsiniz.

Pydantic'in model yapılandırmasını kullanarak `extra` alanları `forbid` edebilirsiniz:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

Bir client bazı **ek header'lar** göndermeye çalışırsa, **hata** response'u alır.

Örneğin client, değeri `plumbus` olan bir `tool` header'ı göndermeye çalışırsa, `tool` header parametresine izin verilmediğini söyleyen bir **hata** response'u alır:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## Alt Çizgileri Dönüştürmeyi Kapatın { #disable-convert-underscores }

Normal header parametrelerinde olduğu gibi, parametre adlarında alt çizgi karakterleri olduğunda bunlar **otomatik olarak tireye dönüştürülür**.

Örneğin kodda `save_data` adlı bir header parametreniz varsa, beklenen HTTP header `save-data` olur ve dokümanlarda da bu şekilde görünür.

Herhangi bir sebeple bu otomatik dönüşümü kapatmanız gerekiyorsa, header parametreleri için kullandığınız Pydantic model'lerde de bunu devre dışı bırakabilirsiniz.

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | Uyarı

`convert_underscores` değerini `False` yapmadan önce, bazı HTTP proxy'lerinin ve server'ların alt çizgi içeren header'ların kullanımına izin vermediğini unutmayın.

///

## Parametre Modellerini Birleştirin { #combine-parameter-models }

Birden fazla header parametre modelini, ayrı header parametreleri ve bağımlılıklarla birleştirebilirsiniz. [Query parametre modelleri](query-param-models.md#combine-parameter-models) için açıklandığı gibi, her modelin verileri bağımsız olarak çıkarılır ve doğrulanır.

Her modelin `extra` yapılandırması, diğer modellerde veya bağımlılıklarda tanımlananlar dahil tüm header parametrelerine uygulanır. `extra="forbid"` kullanıldığında, o modelin dışındaki tüm header'lar reddedilir. `extra="allow"` kullanıldığında ise bu header'lar modele ek alanlar olarak dahil edilir.

Her model, hem request'i okurken hem de OpenAPI oluştururken kendi `Header(convert_underscores=...)` ayarını kullanır. Açıkça belirtilen alan alias'ları, değiştirilmeden header adı olarak kullanılır.

## İsteğe Bağlı Header Parametre Modelleri { #optional-header-parameter-models }

Grubu isteğe bağlı yapmak için header parametre modelini `| None` ile tanımlayın ve varsayılan değerini `None` olarak ayarlayın.

{* ../../docs_src/header_param_models/tutorial004_an_py310.py hl[15] *}

Ne `x-client-name` ne de `x-client-version` gönderilirse, `client` değeri `None` olur. İkisinden biri gönderilirse, FastAPI modeli doğrular ve her iki alanı da zorunlu tutar.

Varsayılan değerler, ek alanlar ve OpenAPI için [isteğe bağlı query parametre modelleri](query-param-models.md#optional-query-parameter-models) ile aynı kurallar geçerlidir.

`Host` gibi header'lar da modelin `extra` yapılandırmasına tabidir. `extra="allow"` kullanıldığında, tanımlanan iki alanın hiçbiri gönderilmese bile bu header'lar modelin oluşturulmasını sağlar.

## Özet { #summary }

**FastAPI**'de **headers** tanımlamak için **Pydantic model** kullanabilirsiniz. 😎
