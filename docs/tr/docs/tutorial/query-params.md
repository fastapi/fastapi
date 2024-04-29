# Sorgu Parametreleri

Fonksiyonda yol parametrelerinin parçası olmayan diğer tanımlamalar otomatik olarak "sorgu" parametresi olarak yorumlanır.

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial001.py!}
```

Sorgu, bağlantıdaki `?` kısmından sonra gelen ve `&` işareti ile ayrılan anahtar-değer çiftlerinin oluşturduğu bir kümedir.

Örneğin, aşağıdaki bağlantıda:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...sorgu parametreleri şunlardır:

* `skip`: değeri `0`'dır
* `limit`: değeri `10`'dır

Parametreler bağlantının bir parçası oldukları için doğal olarak string olarak değerlendirilirler.

Fakat, Python tipleri ile tanımlandıkları zaman (yukarıdaki örnekte `int` oldukları gibi), parametreler o tiplere dönüştürülür ve o tipler çerçevesinde doğrulanırlar.

Yol parametreleri için geçerli olan her türlü işlem aynı şekilde sorgu parametreleri için de geçerlidir:

* Editör desteği (şüphesiz)
* Veri "<abbr title="HTTP isteği ile birlikte gelen string'i Python verisine dönüştürme">ayrıştırma</abbr>"
* Veri doğrulama
* Otomatik dokümantasyon

## Varsayılanlar

Sorgu parametreleri, adres yolunun sabit bir parçası olmadıklarından dolayı isteğe bağlı ve varsayılan değere sahip olabilirler.

Yukarıdaki örnekte `skip=0` ve `limit=10` varsayılan değere sahiplerdir.

Yani, aşağıdaki bağlantıya gitmek:

```
http://127.0.0.1:8000/items/
```

şu adrese gitmek ile aynı etkiye sahiptir:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Ancak, mesela şöyle bir adresi ziyaret ederseniz:

```
http://127.0.0.1:8000/items/?skip=20
```

Fonksiyonunuzdaki parametre değerleri aşağıdaki gibi olacaktır:

* `skip=20`: çünkü bağlantıda böyle tanımlandı.
* `limit=10`: çünkü varsayılan değer buydu.

## İsteğe Bağlı Parametreler

Aynı şekilde, varsayılan değerlerini `None` olarak atayarak isteğe bağlı parametreler tanımlayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params/tutorial002_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params/tutorial002.py!}
    ```

Bu durumda, `q` fonksiyon parametresi isteğe bağlı olacak ve varsayılan değer olarak `None` alacaktır.

!!! check "Ek bilgi"
    Ayrıca, dikkatinizi çekerim ki; **FastAPI**, `item_id` parametresinin bir yol parametresi olduğunu ve `q` parametresinin yol değil bir sorgu parametresi olduğunu fark edecek kadar beceriklidir.

## Sorgu Parametresi Tip Dönüşümü

Aşağıda görüldüğü gibi dönüştürülmek üzere `bool` tipleri de tanımlayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/query_params/tutorial003_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/query_params/tutorial003.py!}
    ```

Bu durumda, eğer şu adrese giderseniz:

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

veya adres, herhangi farklı bir harf varyasyonu içermesi durumuna rağmen (büyük harf, sadece baş harfi büyük kelime, vb.) fonksiyonunuz, `bool` tipli `short` parametresini `True` olarak algılayacaktır. Aksi halde `False` olarak algılanacaktır.


## Çoklu Yol ve Sorgu Parametreleri

**FastAPI** neyin ne olduğunu ayırt edebileceğinden dolayı aynı anda birden fazla yol ve sorgu parametresi tanımlayabilirsiniz.

Ve parametreleri, herhangi bir sıraya koymanıza da gerek yoktur.

İsimlerine göre belirleneceklerdir:

=== "Python 3.10+"

    ```Python hl_lines="6  8"
    {!> ../../../docs_src/query_params/tutorial004_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="8  10"
    {!> ../../../docs_src/query_params/tutorial004.py!}
    ```

## Zorunlu Sorgu Parametreleri

Türü yol olmayan bir parametre (şu ana kadar sadece sorgu parametrelerini gördük) için varsayılan değer tanımlarsanız o parametre zorunlu olmayacaktır.

Parametre için belirli bir değer atamak istemeyip parametrenin sadece isteğe bağlı olmasını istiyorsanız değerini `None` olarak atayabilirsiniz.

Fakat, bir sorgu parametresini zorunlu yapmak istiyorsanız varsayılan bir değer atamamanız yeterli olacaktır:

```Python hl_lines="6-7"
{!../../../docs_src/query_params/tutorial005.py!}
```

Burada `needy` parametresi `str` tipinden oluşan zorunlu bir sorgu parametresidir.

Eğer tarayıcınızda şu bağlantıyı:

```
http://127.0.0.1:8000/items/foo-item
```

...`needy` parametresini eklemeden açarsanız şuna benzer bir hata ile karşılaşırsınız:

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
      "input": null,
      "url": "https://errors.pydantic.dev/2.1/v/missing"
    }
  ]
}
```

`needy` zorunlu bir parametre olduğundan dolayı bağlantıda tanımlanması gerekir:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...bu iş görür:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

Ve elbette, bazı parametreleri zorunlu, bazılarını varsayılan değerli ve bazılarını tamamen opsiyonel olarak tanımlayabilirsiniz:

=== "Python 3.10+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/query_params/tutorial006_py310.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/query_params/tutorial006.py!}
    ```

Bu durumda, 3 tane sorgu parametresi var olacaktır:

* `needy`, zorunlu bir `str`.
* `skip`, varsayılan değeri `0` olan bir `int`.
* `limit`, isteğe bağlı bir `int`.

!!! tip "İpucu"
    Ayrıca, [Yol Parametrelerinde](path-params.md#on-tanml-degerler){.internal-link target=_blank} de kullanıldığı şekilde `Enum` sınıfından faydalanabilirsiniz.
