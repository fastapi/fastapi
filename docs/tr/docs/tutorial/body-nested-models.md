# Body - İç İçe Modeller { #body-nested-models }

**FastAPI** ile (Pydantic sayesinde) istediğiniz kadar derin iç içe geçmiş modelleri tanımlayabilir, doğrulayabilir, dokümante edebilir ve kullanabilirsiniz.

## List alanları { #list-fields }

Bir attribute’u bir alt tipe sahip olacak şekilde tanımlayabilirsiniz. Örneğin, bir Python `list`:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

Bu, `tags`’in bir list olmasını sağlar; ancak list’in elemanlarının tipini belirtmez.

## Tip parametresi olan list alanları { #list-fields-with-type-parameter }

Ancak Python’da, iç tipleri olan list’leri (ya da "type parameter" içeren tipleri) tanımlamanın belirli bir yolu vardır:

### Tip parametresiyle bir `list` tanımlayın { #declare-a-list-with-a-type-parameter }

`list`, `dict`, `tuple` gibi type parameter (iç tip) alan tipleri tanımlamak için, iç tipi(leri) köşeli parantezlerle "type parameter" olarak verin: `[` ve `]`

```Python
my_list: list[str]
```

Bu, tip tanımları için standart Python sözdizimidir.

İç tipleri olan model attribute’ları için de aynı standart sözdizimini kullanın.

Dolayısıyla örneğimizde, `tags`’i özel olarak bir "string list’i" yapabiliriz:

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## Set tipleri { #set-types }

Sonra bunu düşününce, tag’lerin tekrar etmemesi gerektiğini fark ederiz; büyük ihtimalle benzersiz string’ler olmalıdır.

Python’da benzersiz öğelerden oluşan kümeler için özel bir veri tipi vardır: `set`.

O zaman `tags`’i string’lerden oluşan bir set olarak tanımlayabiliriz:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

Böylece duplicate veri içeren bir request alsanız bile, bu veri benzersiz öğelerden oluşan bir set’e dönüştürülür.

Ve bu veriyi ne zaman output etseniz, kaynakta duplicate olsa bile, benzersiz öğelerden oluşan bir set olarak output edilir.

Ayrıca buna göre annotate / dokümante edilir.

## İç İçe Modeller { #nested-models }

Bir Pydantic modelinin her attribute’unun bir tipi vardır.

Ancak bu tip, kendi başına başka bir Pydantic modeli de olabilir.

Yani belirli attribute adları, tipleri ve validation kurallarıyla derin iç içe JSON "object"leri tanımlayabilirsiniz.

Hem de istediğiniz kadar iç içe.

### Bir alt model tanımlayın { #define-a-submodel }

Örneğin bir `Image` modeli tanımlayabiliriz:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### Alt modeli tip olarak kullanın { #use-the-submodel-as-a-type }

Ardından bunu bir attribute’un tipi olarak kullanabiliriz:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

Bu da **FastAPI**’nin aşağıdakine benzer bir body bekleyeceği anlamına gelir:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

Yine, sadece bu tanımı yaparak **FastAPI** ile şunları elde edersiniz:

* Editör desteği (tamamlama vb.), iç içe modeller için bile
* Veri dönüştürme
* Veri doğrulama (validation)
* Otomatik dokümantasyon

## Özel tipler ve doğrulama { #special-types-and-validation }

`str`, `int`, `float` vb. normal tekil tiplerin yanında, `str`’den türeyen daha karmaşık tekil tipleri de kullanabilirsiniz.

Tüm seçenekleri görmek için <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic Türlerine Genel Bakış</a> sayfasına göz atın. Sonraki bölümde bazı örnekleri göreceksiniz.

Örneğin `Image` modelinde bir `url` alanımız olduğuna göre, bunu `str` yerine Pydantic’in `HttpUrl` tipinden bir instance olacak şekilde tanımlayabiliriz:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

String’in geçerli bir URL olup olmadığı kontrol edilir ve JSON Schema / OpenAPI’de de buna göre dokümante edilir.

## Alt modellerden oluşan list’lere sahip attribute’lar { #attributes-with-lists-of-submodels }

Pydantic modellerini `list`, `set` vb. tiplerin alt tipi olarak da kullanabilirsiniz:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

Bu, aşağıdaki gibi bir JSON body bekler (dönüştürür, doğrular, dokümante eder vb.):

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info | Bilgi

`images` key’inin artık image object’lerinden oluşan bir list içerdiğine dikkat edin.

///

## Çok derin iç içe modeller { #deeply-nested-models }

İstediğiniz kadar derin iç içe modeller tanımlayabilirsiniz:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | Bilgi

`Offer`’ın bir `Item` list’i olduğuna, `Item`’ların da opsiyonel bir `Image` list’ine sahip olduğuna dikkat edin.

///

## Sadece list olan body’ler { #bodies-of-pure-lists }

Beklediğiniz JSON body’nin en üst seviye değeri bir JSON `array` (Python’da `list`) ise, tipi Pydantic modellerinde olduğu gibi fonksiyonun parametresinde tanımlayabilirsiniz:

```Python
images: list[Image]
```

şu örnekte olduğu gibi:

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## Her yerde editör desteği { #editor-support-everywhere }

Ve her yerde editör desteği alırsınız.

List içindeki öğeler için bile:

<img src="/img/tutorial/body-nested-models/image01.png">

Pydantic modelleri yerine doğrudan `dict` ile çalışsaydınız bu tür bir editör desteğini alamazdınız.

Ancak bunlarla uğraşmanız da gerekmez; gelen dict’ler otomatik olarak dönüştürülür ve output’unuz da otomatik olarak JSON’a çevrilir.

## Rastgele `dict` body’leri { #bodies-of-arbitrary-dicts }

Body’yi, key’leri bir tipte ve value’ları başka bir tipte olan bir `dict` olarak da tanımlayabilirsiniz.

Bu şekilde (Pydantic modellerinde olduğu gibi) geçerli field/attribute adlarının önceden ne olduğunu bilmeniz gerekmez.

Bu, önceden bilmediğiniz key’leri almak istediğiniz durumlarda faydalıdır.

---

Bir diğer faydalı durum da key’lerin başka bir tipte olmasını istediğiniz zamandır (ör. `int`).

Burada göreceğimiz şey de bu.

Bu durumda, `int` key’lere ve `float` value’lara sahip olduğu sürece herhangi bir `dict` kabul edersiniz:

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | İpucu

JSON key olarak yalnızca `str` destekler, bunu unutmayın.

Ancak Pydantic otomatik veri dönüştürme yapar.

Yani API client’larınız key’leri sadece string olarak gönderebilse bile, bu string’ler saf tamsayı içeriyorsa Pydantic bunları dönüştürür ve doğrular.

Ve `weights` olarak aldığınız `dict`, gerçekte `int` key’lere ve `float` value’lara sahip olur.

///

## Özet { #recap }

**FastAPI** ile Pydantic modellerinin sağladığı en yüksek esnekliği elde ederken, kodunuzu da basit, kısa ve şık tutarsınız.

Üstelik tüm avantajlarla birlikte:

* Editör desteği (her yerde tamamlama!)
* Veri dönüştürme (diğer adıyla parsing / serialization)
* Veri doğrulama (validation)
* Schema dokümantasyonu
* Otomatik dokümanlar
