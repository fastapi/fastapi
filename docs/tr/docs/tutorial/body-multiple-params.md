# Gövde - Çoklu Parametreler

`Path` ve `Query` ifadelerinin kullanımına aşina olduğumuza göre hadi gelin istek gövdesi tanımlamalarının daha ileri kullanımlarını irdeleyelim.

## `Path`, `Query` ve Gövde Parametrelerinin Bir Arada Kullanımı

Her şeyden önce, `Path`, `Query` ve istek gövdesi parametre tanımlamaları özgürce bir arada kullanılabilir ve **FastAPI** bunlar ile ne yapması gerektiğinin bilincindedir.

Ayrıca, `None` varsayılan ifadesi kullanılarak gövde parametreleri isteğe bağlı duruma getirilebilir:

=== "Python 3.10+"

    ```Python hl_lines="18-20"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="18-20"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="17-19"
    {!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001.py!}
    ```

!!! note "Not"
    Dikkatinizi çekerim ki, bu durumda, `None` varsayılan değeri tanımlı olduğundan dolayı gövdeden alınacak olan `item` parametresi isteğe bağlıdır.

## Çoklu Gövde Parametreleri

Bir önceki örnekte, *yol operasyonları*, `Item` ifadesinin özniteliklerini kapsayan alttaki gibi bir JSON gövdesi bekliyor olurdu:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

Fakat, birden fazla gövde parametresi tanımı da yapılabilir, örneğin `item` ve `user`:

=== "Python 3.10+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial002.py!}
    ```

Bu durumda, **FastAPI**, fonksiyonda birden fazla (Pydantic modelleri olan iki) gövde parametresi olduğunun farkına varacaktır.

Böylece, daha sonra FastAPI, parametre adlarını gövdede anahtar (alan adları) olarak kullanacak ve şuna benzer bir gövde bekliyor olacaktır:

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

!!! note "Not"
    Fark ettiyseniz, `item` ifadesi eskisi gibi tanımlanmasına rağmen şimdi gövdenin içerisinde `item` isminde bir anahtar olarak bekleniyor olacaktır.


**FastAPI**, `item` ve `user` ifadelerinin kendilerine özgü içerikleri edinmeleri için istek içerisinden otomatik dönüştürme yapacaktır.

Ayrıca, bileşik verinin doğrulamasını gerçekleştirecek, otomatik dokümantasyon ve OpenAPI şemaları için dokümante edecektir.

## Gövde İçinde Tekil Değerler

Sorgu ve yol parametreleri için ek veri tanımlamak adına `Query` ve `Path` ifadeleri mevcutta bulunduğu gibi **FastAPI**, `Body` ifadesini de temin eder.

Örneğin, önceki modeli genişleterek aynı gövde içerisinde `item` ve `user` ifadelerinin dışında `importance` adında başka bir ifadenin de yer alıp almamasını belirleyebilirsiniz.

Eğer bu ifadeyi olduğu gibi yazarsanız ifade tekil değer olduğundan dolayı **FastAPI** ifadeyi bir sorgu parametresi olarak varsayacaktır.

`Body` ifadesini kullanarak **FastAPI**'a, ifadeye bir gövde anahtarı olarak davranması gerektiğinin talimatını verebilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="23"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial003.py!}
    ```

Bu durumda, **FastAPI** şuna benzer bir gövde bekliyor olacaktır:

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

Aynı şekilde, FastAPI veri tiplerini dönüştürür, doğrular, dokümante eder vb.

## Çoklu Gövde ve Sorgu Parametreleri

Ve elbette, ihtiyacınız oldukça herhangi bir gövde parametresine ek olarak sorgu parametreleri de tanımlayabilirsiniz.

Tekil değerler varsayılan olarak sorgu parametreleri biçiminde değerlendirildiklerinden dolayı açıkça `Query` ifadesini eklemenize gerek yoktur, onun yerine şunu kullanabilirsiniz:

```Python
q: Union[str, None] = None
```

Ya da, Python 3.10 veya daha üst versiyonlarda şunu:

```Python
q: str | None = None
```

Örneğin:

=== "Python 3.10+"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="28"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="25"
    {!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004.py!}
    ```

!!! info "Bilgi"
    `Body` ifadesi, `Query`, `Path` ve ileride göreceğiniz diğer ifadelerde geçerli olan bütün ek doğrulama ve üstveri parametrelerine de sahiptir.

## Tek Gövde Parametresi Yerleştirmek

Diyelim ki, `Item` isimli Pydantic modeli içerisinde `item` adında tek bir gövde parametresine sahipsiniz.

Varsayılan olarak **FastAPI**, direkt olarak gövdesini bekliyor olacaktır.

Ancak eğer, FastAPI'ın, `item` isminde bir anahtara sahip ve içerisinde ek gövde parametreleri tanımı yapıldığında olduğu gibi modelin içeriklerinin bulunduğu bir JSON bekliyor olmasını istiyorsanız özel `Body` parametresi olan `embed` ifadesini kullanabilirsiniz:

```Python
item: Item = Body(embed=True)
```

şuradaki gibi:

=== "Python 3.10+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an.py!}
    ```

=== "Python 3.10+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="15"
    {!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
    ```

=== "Python 3.8+ Annotated'sız"

    !!! tip "İpucu"
        Mümkün oldukça `Annotated`'lı versiyonu kullanmaya özen gösteriniz.

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005.py!}
    ```

Bu durumda, **FastAPI**, şunun gibi bir gövde bekliyor olacaktır:

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

bunun aksine:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Özet

Bir isteğin sadece tek bir gövdeye sahip olabilmesine rağmen *yol operasyon fonksiyonunuza* birden fazla gövde parametresi ekleyebilirsiniz.

**FastAPI**, fonksiyonda doğru veriyi sağlayacak, *yol operasyonundaki* doğru şemayı doğruladıktan sonra dokümante edip her şeyin üstesinden gelecektir.

Gövdenin bir parçası olarak değerlendirilmeleri adına tekil değerler de tanımlayabilirsiniz.

Ve ayrıca, tek bir parametre tanımlandığı durumlarda bile **FastAPI**'a gövdeyi bir anahtarın içine yerleştirmesi gerektiğinin talimatını verebilirsiniz.
