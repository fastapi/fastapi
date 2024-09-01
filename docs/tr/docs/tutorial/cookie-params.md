# Çerez (Cookie) Parametreleri

`Query` (Sorgu) ve `Path` (Yol) parametrelerini tanımladığınız şekilde çerez parametreleri tanımlayabilirsiniz.

## Import `Cookie`

Öncelikle, `Cookie`'yi projenize dahil edin:

//// tab | Python 3.10+

```Python hl_lines="3"
{!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="3"
{!> ../../../docs_src/cookie_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | "İpucu"

Mümkün mertebe 'Annotated' sınıfını kullanmaya çalışın.

///

```Python hl_lines="1"
{!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "İpucu"

Mümkün mertebe 'Annotated' sınıfını kullanmaya çalışın.

///

```Python hl_lines="3"
{!> ../../../docs_src/cookie_params/tutorial001.py!}
```

////

## `Cookie` Parametrelerini Tanımlayın

Çerez parametrelerini `Path` veya `Query` tanımlaması yapar gibi tanımlayın.

İlk değer varsayılan değerdir; tüm ekstra doğrulama veya belirteç parametrelerini kullanabilirsiniz:

//// tab | Python 3.10+

```Python hl_lines="9"
{!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10"
{!> ../../../docs_src/cookie_params/tutorial001_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | "İpucu"

Mümkün mertebe 'Annotated' sınıfını kullanmaya çalışın.

///

```Python hl_lines="7"
{!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "İpucu"

Mümkün mertebe 'Annotated' sınıfını kullanmaya çalışın.

///

```Python hl_lines="9"
{!> ../../../docs_src/cookie_params/tutorial001.py!}
```

////

/// note | "Teknik Detaylar"

`Cookie` sınıfı `Path` ve `Query` sınıflarının kardeşidir. Diğerleri gibi `Param` sınıfını miras alan bir sınıftır.

Ancak `fastapi`'dan projenize dahil ettiğiniz `Query`, `Path`, `Cookie` ve diğerleri aslında özel sınıflar döndüren birer fonksiyondur.

///

/// info | "Bilgi"

Çerez tanımlamak için `Cookie` sınıfını kullanmanız gerekmektedir, aksi taktirde parametreler sorgu parametreleri olarak yorumlanır.

///

## Özet

Çerez tanımlamalarını `Cookie` sınıfını kullanarak `Query` ve `Path` tanımlar gibi tanımlayın.
