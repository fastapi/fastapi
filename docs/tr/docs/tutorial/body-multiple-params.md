# Body - Birden Fazla Parametre { #body-multiple-parameters }

Artık `Path` ve `Query` kullanmayı gördüğümüze göre, request body bildirimlerinin daha ileri kullanım senaryolarına bakalım.

## `Path`, `Query` ve body parametrelerini karıştırma { #mix-path-query-and-body-parameters }

Öncelikle, elbette `Path`, `Query` ve request body parametre bildirimlerini serbestçe karıştırabilirsiniz ve **FastAPI** ne yapacağını bilir.

Ayrıca, varsayılan değeri `None` yaparak body parametrelerini opsiyonel olarak da tanımlayabilirsiniz:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | Not

Bu durumda body'den alınacak `item` opsiyoneldir. Çünkü varsayılan değeri `None` olarak ayarlanmıştır.

///

## Birden fazla body parametresi { #multiple-body-parameters }

Önceki örnekte, *path operation*'lar `Item`'ın özelliklerini içeren bir JSON body beklerdi, örneğin:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Ancak birden fazla body parametresi de tanımlayabilirsiniz; örneğin `item` ve `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


Bu durumda **FastAPI**, fonksiyonda birden fazla body parametresi olduğunu fark eder (iki parametre de Pydantic modelidir).

Bunun üzerine, body içinde anahtar (field name) olarak parametre adlarını kullanır ve şu şekilde bir body bekler:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | Not

`item` daha öncekiyle aynı şekilde tanımlanmış olsa bile, artık body içinde `item` anahtarı altında gelmesi beklenir.

///

**FastAPI**, request'ten otomatik dönüşümü yapar; böylece `item` parametresi kendi içeriğini alır, `user` için de aynı şekilde olur.

Birleşik verinin validasyonunu yapar ve OpenAPI şeması ile otomatik dokümantasyonda da bunu bu şekilde dokümante eder.

## Body içinde tekil değerler { #singular-values-in-body }

Query ve path parametreleri için ek veri tanımlamak üzere `Query` ve `Path` olduğu gibi, **FastAPI** bunların karşılığı olarak `Body` de sağlar.

Örneğin, önceki modeli genişleterek, aynı body içinde `item` ve `user` dışında bir de `importance` anahtarı olmasını isteyebilirsiniz.

Bunu olduğu gibi tanımlarsanız, tekil bir değer olduğu için **FastAPI** bunun bir query parametresi olduğunu varsayar.

Ama `Body` kullanarak, **FastAPI**'ye bunu body içinde başka bir anahtar olarak ele almasını söyleyebilirsiniz:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


Bu durumda **FastAPI** şu şekilde bir body bekler:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

Yine veri tiplerini dönüştürür, validate eder, dokümante eder, vb.

## Birden fazla body parametresi ve query { #multiple-body-params-and-query }

Elbette ihtiyaç duyduğunuzda, body parametrelerine ek olarak query parametreleri de tanımlayabilirsiniz.

Varsayılan olarak tekil değerler query parametresi olarak yorumlandığı için, ayrıca `Query` eklemeniz gerekmez; şöyle yazmanız yeterlidir:

```Python
q: str | None = None
```

Örneğin:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// info | Bilgi

`Body`, `Query`, `Path` ve daha sonra göreceğiniz diğerleriyle aynı ek validasyon ve metadata parametrelerine de sahiptir.

///

## Tek bir body parametresini gömme { #embed-a-single-body-parameter }

Diyelim ki Pydantic'teki `Item` modelinden gelen yalnızca tek bir `item` body parametreniz var.

Varsayılan olarak **FastAPI**, body'nin doğrudan bu modelin içeriği olmasını bekler.

Ancak, ek body parametreleri tanımladığınızda olduğu gibi, `item` anahtarı olan bir JSON ve onun içinde modelin içeriğini beklemesini istiyorsanız, `Body`'nin özel parametresi olan `embed`'i kullanabilirsiniz:

```Python
item: Item = Body(embed=True)
```

yani şöyle:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


Bu durumda **FastAPI** şu şekilde bir body bekler:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

şunun yerine:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Özet { #recap }

Bir request yalnızca tek bir body içerebilse de, *path operation function*'ınıza birden fazla body parametresi ekleyebilirsiniz.

Ancak **FastAPI** bunu yönetir; fonksiyonunuza doğru veriyi verir ve *path operation* içinde doğru şemayı validate edip dokümante eder.

Ayrıca tekil değerlerin body'nin bir parçası olarak alınmasını da tanımlayabilirsiniz.

Ve yalnızca tek bir parametre tanımlanmış olsa bile, **FastAPI**'ye body'yi bir anahtarın içine gömmesini söyleyebilirsiniz.
