# اضافی ڈیٹا Types { #extra-data-types }

اب تک آپ عام ڈیٹا types استعمال کر رہے ہیں، جیسے:

* `int`
* `float`
* `str`
* `bool`

لیکن آپ مزید پیچیدہ ڈیٹا types بھی استعمال کر سکتے ہیں۔

اور آپ کو پھر بھی وہی خصوصیات ملیں گی جو اب تک دیکھی ہیں:

* بہترین editor سپورٹ۔
* آنے والی requests سے ڈیٹا کی تبدیلی۔
* response ڈیٹا کی تبدیلی۔
* ڈیٹا validation۔
* خودکار annotation اور documentation۔

## دیگر ڈیٹا types { #other-data-types }

یہاں کچھ اضافی ڈیٹا types ہیں جو آپ استعمال کر سکتے ہیں:

* `UUID`:
    * ایک معیاری "Universally Unique Identifier"، جو بہت سے databases اور systems میں ID کے طور پر عام ہے۔
    * Requests اور responses میں یہ `str` کے طور پر ظاہر ہوگا۔
* `datetime.datetime`:
    * Python کا `datetime.datetime`۔
    * Requests اور responses میں یہ ISO 8601 format میں `str` کے طور پر ظاہر ہوگا، جیسے: `2008-09-15T15:53:00+05:00`۔
* `datetime.date`:
    * Python کا `datetime.date`۔
    * Requests اور responses میں یہ ISO 8601 format میں `str` کے طور پر ظاہر ہوگا، جیسے: `2008-09-15`۔
* `datetime.time`:
    * Python کا `datetime.time`۔
    * Requests اور responses میں یہ ISO 8601 format میں `str` کے طور پر ظاہر ہوگا، جیسے: `14:23:55.003`۔
* `datetime.timedelta`:
    * Python کا `datetime.timedelta`۔
    * Requests اور responses میں یہ کل سیکنڈز کے `float` کے طور پر ظاہر ہوگا۔
    * Pydantic اسے "ISO 8601 time diff encoding" کے طور پر بھی ظاہر کرنے کی اجازت دیتا ہے، [مزید معلومات کے لیے docs دیکھیں](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers)۔
* `frozenset`:
    * Requests اور responses میں، `set` کی طرح برتاؤ ہوگا:
        * Requests میں، ایک list پڑھی جائے گی، ڈپلیکیٹس ہٹائے جائیں گے اور اسے `set` میں تبدیل کیا جائے گا۔
        * Responses میں، `set` کو `list` میں تبدیل کیا جائے گا۔
        * تیار کردہ schema بتائے گا کہ `set` کی قدریں منفرد ہیں (JSON Schema کا `uniqueItems` استعمال کر کے)۔
* `bytes`:
    * معیاری Python `bytes`۔
    * Requests اور responses میں `str` کے طور پر برتاؤ ہوگا۔
    * تیار کردہ schema بتائے گا کہ یہ `binary` "format" کا `str` ہے۔
* `Decimal`:
    * معیاری Python `Decimal`۔
    * Requests اور responses میں، `float` کی طرح handle ہوگا۔
* آپ تمام درست Pydantic ڈیٹا types یہاں چیک کر سکتے ہیں: [Pydantic data types](https://docs.pydantic.dev/latest/usage/types/types/)۔

## مثال { #example }

یہاں ایک مثال *path operation* ہے جس کے parameters اوپر بیان کردہ کچھ types استعمال کرتے ہیں۔

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

نوٹ کریں کہ function کے اندر parameters کی اپنی فطری ڈیٹا type ہوتی ہے، اور آپ مثلاً عام تاریخ کی کارروائیاں کر سکتے ہیں، جیسے:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
