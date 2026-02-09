# JSON Uyumlu Encoder { #json-compatible-encoder }

Bazı durumlarda, bir veri tipini (örneğin bir Pydantic model) JSON ile uyumlu bir şeye (örneğin `dict`, `list` vb.) dönüştürmeniz gerekebilir.

Örneğin, bunu bir veritabanında saklamanız gerekiyorsa.

Bunun için **FastAPI**, `jsonable_encoder()` fonksiyonunu sağlar.

## `jsonable_encoder` Kullanımı { #using-the-jsonable-encoder }

Yalnızca JSON ile uyumlu veri kabul eden bir veritabanınız olduğunu düşünelim: `fake_db`.

Örneğin bu veritabanı, JSON ile uyumlu olmadıkları için `datetime` objelerini kabul etmez.

Dolayısıyla bir `datetime` objesinin, <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO formatında</a> veriyi içeren bir `str`'e dönüştürülmesi gerekir.

Aynı şekilde bu veritabanı bir Pydantic model'i (attribute'lara sahip bir obje) de kabul etmez; yalnızca bir `dict` kabul eder.

Bunun için `jsonable_encoder` kullanabilirsiniz.

Bir Pydantic model gibi bir obje alır ve JSON ile uyumlu bir versiyonunu döndürür:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

Bu örnekte, Pydantic model'i bir `dict`'e, `datetime`'ı da bir `str`'e dönüştürür.

Bu fonksiyonun çağrılmasıyla elde edilen sonuç, Python standardındaki <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a> ile encode edilebilecek bir şeydir.

JSON formatında (string olarak) veriyi içeren büyük bir `str` döndürmez. Bunun yerine, tüm değerleri ve alt değerleri JSON ile uyumlu olacak şekilde, Python’un standart bir veri yapısını (örneğin bir `dict`) döndürür.

/// note | Not

`jsonable_encoder`, aslında **FastAPI** tarafından veriyi dönüştürmek için internal olarak kullanılır. Ancak birçok farklı senaryoda da oldukça faydalıdır.

///
