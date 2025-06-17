# Çerez (Cookie) Parametreleri

`Query` (Sorgu) ve `Path` (Yol) parametrelerini tanımladığınız şekilde çerez parametreleri tanımlayabilirsiniz.

## Import `Cookie`

Öncelikle, `Cookie`'yi projenize dahil edin:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` Parametrelerini Tanımlayın

Çerez parametrelerini `Path` veya `Query` tanımlaması yapar gibi tanımlayın.

İlk değer varsayılan değerdir; tüm ekstra doğrulama veya belirteç parametrelerini kullanabilirsiniz:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Teknik Detaylar

`Cookie` sınıfı `Path` ve `Query` sınıflarının kardeşidir. Diğerleri gibi `Param` sınıfını miras alan bir sınıftır.

Ancak `fastapi`'dan projenize dahil ettiğiniz `Query`, `Path`, `Cookie` ve diğerleri aslında özel sınıflar döndüren birer fonksiyondur.

///

/// info | Bilgi

Çerez tanımlamak için `Cookie` sınıfını kullanmanız gerekmektedir, aksi taktirde parametreler sorgu parametreleri olarak yorumlanır.

///

## Özet

Çerez tanımlamalarını `Cookie` sınıfını kullanarak `Query` ve `Path` tanımlar gibi tanımlayın.
