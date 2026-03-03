# Sorgu Parametreleri { #query-parameters }

Fonksiyonda path parametrelerinin parçası olmayan diğer parametreleri tanımladığınızda, bunlar otomatik olarak "query" parametreleri olarak yorumlanır.

{* ../../docs_src/query_params/tutorial001_py310.py hl[9] *}

Query, bir URL'de `?` işaretinden sonra gelen ve `&` karakterleriyle ayrılan anahtar-değer çiftlerinin kümesidir.

Örneğin, şu URL'de:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...query parametreleri şunlardır:

* `skip`: değeri `0`
* `limit`: değeri `10`

URL'nin bir parçası oldukları için "doğal olarak" string'tirler.

Ancak, bunları Python tipleriyle (yukarıdaki örnekte `int` olarak) tanımladığınızda, o tipe dönüştürülürler ve o tipe göre doğrulanırlar.

Path parametreleri için geçerli olan aynı süreç query parametreleri için de geçerlidir:

* Editör desteği (tabii ki)
* Veri <dfn title="bir HTTP request'ten gelen string'i Python verisine dönüştürme">"ayrıştırma"</dfn>
* Veri doğrulama
* Otomatik dokümantasyon

## Varsayılanlar { #defaults }

Query parametreleri path'in sabit bir parçası olmadığından, opsiyonel olabilir ve varsayılan değerlere sahip olabilir.

Yukarıdaki örnekte varsayılan değerleri `skip=0` ve `limit=10`'dur.

Yani şu URL'ye gitmek:

```
http://127.0.0.1:8000/items/
```

şuraya gitmekle aynı olur:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Namunak örneğin şuraya giderseniz:

```
http://127.0.0.1:8000/items/?skip=20
```

Fonksiyonunuzdaki parametre değerleri şöyle olacaktır:

* `skip=20`: çünkü URL'de siz ayarladınız
* `limit=10`: çünkü varsayılan değer oydu

## İsteğe bağlı parametreler { #optional-parameters }

Aynı şekilde, varsayılan değerlerini `None` yaparak isteğe bağlı query parametreleri tanımlayabilirsiniz:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Bu durumda, fonksiyon parametresi `q` isteğe bağlı olur ve varsayılan olarak `None` olur.

/// check | Ek bilgi

Ayrıca, **FastAPI** path parametresi olan `item_id`'nin bir path parametresi olduğunu ve `q`'nun path olmadığını fark edecek kadar akıllıdır; dolayısıyla bu bir query parametresidir.

///

## Sorgu parametresi tip dönüşümü { #query-parameter-type-conversion }

`bool` tipleri de tanımlayabilirsiniz, ve bunlar dönüştürülür:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Bu durumda, şuraya giderseniz:

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

veya başka herhangi bir büyük/küçük harf varyasyonunda (tamamı büyük, ilk harf büyük, vb.), fonksiyonunuz `short` parametresini `bool` değeri `True` olarak görecektir. Aksi halde `False` olarak görür.


## Çoklu path ve query parametreleri { #multiple-path-and-query-parameters }

Aynı anda birden fazla path parametresi ve query parametresi tanımlayabilirsiniz; **FastAPI** hangisinin hangisi olduğunu bilir.

Ayrıca bunları belirli bir sırayla tanımlamanız gerekmez.

İsme göre tespit edilirler:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Zorunlu query parametreleri { #required-query-parameters }

Path olmayan parametreler (şimdilik sadece query parametrelerini gördük) için varsayılan değer tanımladığınızda, bu parametre zorunlu olmaz.

Belirli bir değer eklemek istemiyor ama sadece opsiyonel olmasını istiyorsanız, varsayılanı `None` olarak ayarlayın.

Ancak bir query parametresini zorunlu yapmak istediğinizde, herhangi bir varsayılan değer tanımlamamanız yeterlidir:

{* ../../docs_src/query_params/tutorial005_py310.py hl[6:7] *}

Burada query parametresi `needy`, `str` tipinde zorunlu bir query parametresidir.

Tarayıcınızda şöyle bir URL açarsanız:

```
http://127.0.0.1:8000/items/foo-item
```

...zorunlu `needy` parametresini eklemeden, şuna benzer bir hata görürsünüz:

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

Ve elbette, bazı parametreleri zorunlu, bazılarını varsayılan değerli, bazılarını da tamamen isteğe bağlı olarak tanımlayabilirsiniz:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Bu durumda, 3 tane query parametresi vardır:

* `needy`, zorunlu bir `str`.
* `skip`, varsayılan değeri `0` olan bir `int`.
* `limit`, isteğe bağlı bir `int`.

/// tip | İpucu

[Path Parametreleri](path-params.md#predefined-values){.internal-link target=_blank} ile aynı şekilde `Enum`'ları da kullanabilirsiniz.

///
