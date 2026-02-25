# Ek Veri Tipleri { #extra-data-types }

Şimdiye kadar şunlar gibi yaygın veri tiplerini kullanıyordunuz:

* `int`
* `float`
* `str`
* `bool`

Ancak daha karmaşık veri tiplerini de kullanabilirsiniz.

Ve yine, şimdiye kadar gördüğünüz özelliklerin aynısına sahip olursunuz:

* Harika editör desteği.
* Gelen request'lerden veri dönüştürme.
* response verileri için veri dönüştürme.
* Veri doğrulama.
* Otomatik annotation ve dokümantasyon.

## Diğer veri tipleri { #other-data-types }

Kullanabileceğiniz ek veri tiplerinden bazıları şunlardır:

* `UUID`:
    * Birçok veritabanı ve sistemde ID olarak yaygın kullanılan, standart bir "Universally Unique Identifier".
    * request'lerde ve response'larda `str` olarak temsil edilir.
* `datetime.datetime`:
    * Python `datetime.datetime`.
    * request'lerde ve response'larda ISO 8601 formatında bir `str` olarak temsil edilir, örn: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * Python `datetime.date`.
    * request'lerde ve response'larda ISO 8601 formatında bir `str` olarak temsil edilir, örn: `2008-09-15`.
* `datetime.time`:
    * Python `datetime.time`.
    * request'lerde ve response'larda ISO 8601 formatında bir `str` olarak temsil edilir, örn: `14:23:55.003`.
* `datetime.timedelta`:
    * Python `datetime.timedelta`.
    * request'lerde ve response'larda toplam saniye sayısını ifade eden bir `float` olarak temsil edilir.
    * Pydantic, bunu ayrıca bir "ISO 8601 time diff encoding" olarak temsil etmeye de izin verir, daha fazla bilgi için <a href="https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers" class="external-link" target="_blank">dokümanlara bakın</a>.
* `frozenset`:
    * request'lerde ve response'larda, `set` ile aynı şekilde ele alınır:
        * request'lerde bir list okunur, tekrarlar kaldırılır ve `set`'e dönüştürülür.
        * response'larda `set`, `list`'e dönüştürülür.
        * Üretilen schema, `set` değerlerinin benzersiz olduğunu belirtir (JSON Schema'nın `uniqueItems` özelliğini kullanarak).
* `bytes`:
    * Standart Python `bytes`.
    * request'lerde ve response'larda `str` gibi ele alınır.
    * Üretilen schema, bunun `binary` "format"ına sahip bir `str` olduğunu belirtir.
* `Decimal`:
    * Standart Python `Decimal`.
    * request'lerde ve response'larda `float` ile aynı şekilde işlenir.
* Geçerli tüm Pydantic veri tiplerini burada görebilirsiniz: <a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Pydantic data types</a>.

## Örnek { #example }

Yukarıdaki tiplerden bazılarını kullanan parametrelere sahip bir örnek *path operation* şöyle:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

Fonksiyonun içindeki parametrelerin doğal veri tiplerinde olduğunu unutmayın; örneğin normal tarih işlemleri yapabilirsiniz:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
