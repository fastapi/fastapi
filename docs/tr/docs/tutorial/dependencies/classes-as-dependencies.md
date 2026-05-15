# Dependency Olarak Class'lar { #classes-as-dependencies }

**Dependency Injection** sistemine daha derinlemesine geçmeden önce, bir önceki örneği geliştirelim.

## Önceki Örnekten Bir `dict` { #a-dict-from-the-previous-example }

Önceki örnekte, dependency'mizden ("dependable") bir `dict` döndürüyorduk:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Ama sonra *path operation function* içindeki `commons` parametresinde bir `dict` alıyoruz.

Ve biliyoruz ki editor'ler `dict`'ler için çok fazla destek (ör. completion) veremez; çünkü key'lerini ve value type'larını bilemezler.

Daha iyisini yapabiliriz...

## Bir Şeyi Dependency Yapan Nedir { #what-makes-a-dependency }

Şimdiye kadar dependency'leri function olarak tanımlanmış şekilde gördünüz.

Ancak dependency tanımlamanın tek yolu bu değil (muhtemelen en yaygını bu olsa da).

Buradaki kritik nokta, bir dependency'nin "callable" olması gerektiğidir.

Python'da "**callable**", Python'ın bir function gibi "çağırabildiği" her şeydir.

Yani elinizde `something` adlı bir nesne varsa (function _olmak zorunda değil_) ve onu şöyle "çağırabiliyorsanız" (çalıştırabiliyorsanız):

```Python
something()
```

veya

```Python
something(some_argument, some_keyword_argument="foo")
```

o zaman bu bir "callable" demektir.

## Dependency Olarak Class'lar { #classes-as-dependencies_1 }

Python'da bir class'tan instance oluştururken de aynı söz dizimini kullandığınızı fark etmiş olabilirsiniz.

Örneğin:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

Bu durumda `fluffy`, `Cat` class'ının bir instance'ıdır.

Ve `fluffy` oluşturmak için `Cat`'i "çağırmış" olursunuz.

Dolayısıyla bir Python class'ı da bir **callable**'dır.

O zaman **FastAPI** içinde bir Python class'ını dependency olarak kullanabilirsiniz.

FastAPI'nin aslında kontrol ettiği şey, bunun bir "callable" olması (function, class ya da başka bir şey) ve tanımlı parametreleridir.

Eğer **FastAPI**'de bir dependency olarak bir "callable" verirseniz, FastAPI o "callable" için parametreleri analiz eder ve bunları *path operation function* parametreleriyle aynı şekilde işler. Sub-dependency'ler dahil.

Bu, hiç parametresi olmayan callable'lar için de geçerlidir. Tıpkı hiç parametresi olmayan *path operation function*'larda olduğu gibi.

O zaman yukarıdaki `common_parameters` adlı "dependable" dependency'sini `CommonQueryParams` class'ına çevirebiliriz:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Class instance'ını oluşturmak için kullanılan `__init__` metoduna dikkat edin:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...bizim önceki `common_parameters` ile aynı parametrelere sahip:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Bu parametreler, dependency'yi "çözmek" için **FastAPI**'nin kullanacağı şeylerdir.

Her iki durumda da şunlar olacak:

* `str` olan opsiyonel bir `q` query parametresi.
* Default değeri `0` olan `int` tipinde bir `skip` query parametresi.
* Default değeri `100` olan `int` tipinde bir `limit` query parametresi.

Her iki durumda da veriler dönüştürülecek, doğrulanacak, OpenAPI şemasında dokümante edilecek, vb.

## Kullanalım { #use-it }

Artık bu class'ı kullanarak dependency'nizi tanımlayabilirsiniz.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI**, `CommonQueryParams` class'ını çağırır. Bu, o class'ın bir "instance"ını oluşturur ve bu instance, sizin function'ınıza `commons` parametresi olarak geçirilir.

## Type Annotation vs `Depends` { #type-annotation-vs-depends }

Yukarıdaki kodda `CommonQueryParams`'ı iki kez yazdığımıza dikkat edin:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

Şuradaki son `CommonQueryParams`:

```Python
... Depends(CommonQueryParams)
```

...FastAPI'nin dependency'nin ne olduğunu anlamak için gerçekten kullandığı şeydir.

FastAPI tanımlanan parametreleri buradan çıkarır ve aslında çağıracağı şey de budur.

---

Bu durumda, şuradaki ilk `CommonQueryParams`:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons: CommonQueryParams ...
```

////

...**FastAPI** için özel bir anlam taşımaz. FastAPI bunu veri dönüştürme, doğrulama vb. için kullanmaz (çünkü bunlar için `Depends(CommonQueryParams)` kullanıyor).

Hatta şunu bile yazabilirsiniz:

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons = Depends(CommonQueryParams)
```

////

...şu örnekte olduğu gibi:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Ancak type'ı belirtmeniz önerilir; böylece editor'ünüz `commons` parametresine ne geçirileceğini bilir ve size code completion, type check'leri vb. konularda yardımcı olur:

<img src="/img/tutorial/dependencies/image02.png">

## Kısayol { #shortcut }

Ama burada bir miktar kod tekrarımız olduğunu görüyorsunuz; `CommonQueryParams`'ı iki kez yazıyoruz:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI**, bu durumlar için bir kısayol sağlar: dependency'nin *özellikle* FastAPI'nin bir instance oluşturmak için "çağıracağı" bir class olduğu durumlar.

Bu özel durumlarda şunu yapabilirsiniz:

Şunu yazmak yerine:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...şunu yazarsınız:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ Annotated Olmadan

/// tip | İpucu

Mümkünse `Annotated` sürümünü kullanmayı tercih edin.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Dependency'yi parametrenin type'ı olarak tanımlarsınız ve `Depends(CommonQueryParams)` içinde class'ı *yeniden* yazmak yerine, parametre vermeden `Depends()` kullanırsınız.

Aynı örnek şu hale gelir:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...ve **FastAPI** ne yapması gerektiğini bilir.

/// tip | İpucu

Bu size faydalı olmaktan çok kafa karıştırıcı geliyorsa, kullanmayın; buna *ihtiyacınız* yok.

Bu sadece bir kısayoldur. Çünkü **FastAPI** kod tekrarını en aza indirmenize yardımcı olmayı önemser.

///
