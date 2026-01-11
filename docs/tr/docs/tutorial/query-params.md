# Sorgu Parametreleri { #query-parameters }

Fonksiyonda path parametrelerinin parçası olmayan diğer fonksiyon parametrelerini tanımladığınızda, bunlar otomatik olarak "query" parametreleri olarak yorumlanır.

{* ../../docs_src/query_params/tutorial001_py39.py hl[9] *}

Query, URL'deki `?` işaretinden sonra gelen ve `&` karakterleri ile ayrılan anahtar-değer çiftleri kümesidir.

Örneğin, şu URL'de:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...query parametreleri şunlardır:

* `skip`: değeri `0` olan
* `limit`: değeri `10` olan

URL'nin bir parçası oldukları için "doğal olarak" string'dirler.

Ama onları Python tipleri ile tanımladığınızda (yukarıdaki örnekte `int` olarak), o tipe dönüştürülürler ve o tipe göre doğrulanırlar.

Path parametreleri için geçerli olan tüm süreç, query parametreleri için de geçerlidir:

* Editör desteği (tabii ki)
* Veri <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>
* Veri doğrulama
* Otomatik dokümantasyon

## Varsayılanlar { #defaults }

Query parametreleri path'in sabit bir parçası olmadığından, opsiyonel olabilir ve varsayılan değerlere sahip olabilirler.

Yukarıdaki örnekte `skip=0` ve `limit=10` varsayılan değerlerine sahipler.

Yani şu URL'ye gitmek:

```
http://127.0.0.1:8000/items/
```

şuna gitmek ile aynı olacaktır:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Ama örneğin şuna giderseniz:

```
http://127.0.0.1:8000/items/?skip=20
```

Fonksiyonunuzdaki parametre değerleri şöyle olacaktır:

* `skip=20`: çünkü URL'de siz ayarladınız
* `limit=10`: çünkü varsayılan değer buydu

## Opsiyonel parametreler { #optional-parameters }

Aynı şekilde, varsayılanını `None` yaparak opsiyonel query parametreleri tanımlayabilirsiniz:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Bu durumda, fonksiyon parametresi `q` opsiyonel olacaktır ve varsayılan olarak `None` olacaktır.

/// check | Ek bilgi

Ayrıca **FastAPI**'nin, path parametresi `item_id`'nin bir path parametresi olduğunu ve `q`'nun olmadığını, dolayısıyla bir query parametresi olduğunu fark edecek kadar akıllı olduğuna da dikkat edin.

///

## Query parametresi tip dönüşümü { #query-parameter-type-conversion }

`bool` tiplerini de tanımlayabilirsiniz ve dönüştürüleceklerdir:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Bu durumda, şuna giderseniz:

```
http://127.0.0.1:8000/items/foo?short=1
```

veya

```
http://127.0.0.1:8000/items/foo?short=True
```

veya

```
http://127.0.0.1:8000/items/foo?short=true
```

veya

```
http://127.0.0.1:8000/items/foo?short=on
```

veya

```
http://127.0.0.1:8000/items/foo?short=yes
```

veya başka herhangi bir büyük/küçük harf varyasyonunda (tamamı büyük harf, ilk harfi büyük, vb.), fonksiyonunuz `short` parametresini `bool` değeri `True` olacak şekilde görecektir. Aksi halde `False` olarak görecektir.


## Çoklu path ve query parametreleri { #multiple-path-and-query-parameters }

Aynı anda birden fazla path parametresi ve query parametresi tanımlayabilirsiniz, **FastAPI** hangisinin hangisi olduğunu bilir.

Ve onları belirli bir sırayla tanımlamak zorunda değilsiniz.

İsimlerine göre tespit edileceklerdir:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Zorunlu query parametreleri { #required-query-parameters }

Path olmayan parametreler (şimdilik sadece query parametrelerini gördük) için varsayılan bir değer tanımladığınızda, bu zorunlu değildir.

Belirli bir değer eklemek istemiyor ama sadece opsiyonel olmasını istiyorsanız, varsayılanı `None` olarak ayarlayın.

Ama bir query parametresini zorunlu yapmak istediğinizde, herhangi bir varsayılan değer tanımlamamanız yeterlidir:

{* ../../docs_src/query_params/tutorial005_py39.py hl[6:7] *}

Burada query parametresi `needy`, `str` tipinde zorunlu bir query parametresidir.

Tarayıcınızda şöyle bir URL açarsanız:

```
http://127.0.0.1:8000/items/foo-item
```

...zorunlu parametre `needy`'yi eklemeden, şuna benzer bir hata görürsünüz:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

`needy` zorunlu bir parametre olduğundan, URL'de ayarlamanız gerekir:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...bu çalışır:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Ve elbette, bazı parametreleri zorunlu, bazılarını varsayılan değerli ve bazılarını tamamen opsiyonel olarak tanımlayabilirsiniz:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Bu durumda, 3 query parametresi vardır:

* `needy`, zorunlu bir `str`.
* `skip`, varsayılan değeri `0` olan bir `int`.
* `limit`, opsiyonel bir `int`.

/// tip | İpucu

[Path Parameters](path-params.md#predefined-values){.internal-link target=_blank} ile aynı şekilde `Enum`'ları da kullanabilirsiniz.

///
