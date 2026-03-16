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

## Özet { #summary }

**FastAPI**'de **headers** tanımlamak için **Pydantic model** kullanabilirsiniz. 😎
