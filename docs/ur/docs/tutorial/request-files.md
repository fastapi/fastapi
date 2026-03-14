# Request Files { #request-files }

آپ `File` استعمال کر کے client کی جانب سے upload کی جانے والی files کی وضاحت کر سکتے ہیں۔

/// info

Upload کی گئی files وصول کرنے کے لیے پہلے [`python-multipart`](https://github.com/Kludex/python-multipart) انسٹال کریں۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر اسے انسٹال کریں، مثال کے طور پر:

```console
$ pip install python-multipart
```

یہ اس لیے ضروری ہے کیونکہ upload کی گئی files "form data" کے طور پر بھیجی جاتی ہیں۔

///

## `File` کو Import کریں { #import-file }

`fastapi` سے `File` اور `UploadFile` کو import کریں:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## `File` کے Parameters کی وضاحت کریں { #define-file-parameters }

File parameters بالکل اسی طرح بنائیں جیسے آپ `Body` یا `Form` کے لیے بناتے ہیں:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info

`File` ایک class ہے جو براہ راست `Form` سے inherit ہوتی ہے۔

لیکن یاد رکھیں کہ جب آپ `fastapi` سے `Query`، `Path`، `File` اور دوسرے import کرتے ہیں تو یہ دراصل functions ہیں جو خاص classes واپس کرتے ہیں۔

///

/// tip | مشورہ

File bodies بیان کرنے کے لیے آپ کو `File` استعمال کرنا ہوگا، کیونکہ ورنہ parameters کو query parameters یا body (JSON) parameters سمجھا جائے گا۔

///

Files "form data" کے طور پر upload ہوں گی۔

اگر آپ اپنے *path operation function* کے parameter کی type `bytes` بیان کرتے ہیں تو **FastAPI** آپ کے لیے file پڑھے گا اور آپ کو مواد `bytes` کے طور پر ملے گا۔

ذہن میں رکھیں کہ اس کا مطلب ہے کہ پورا مواد memory میں محفوظ ہوگا۔ یہ چھوٹی files کے لیے اچھا کام کرے گا۔

لیکن کئی ایسے معاملات ہیں جن میں آپ کو `UploadFile` استعمال کرنے سے فائدہ ہوگا۔

## `UploadFile` کے ساتھ File Parameters { #file-parameters-with-uploadfile }

`UploadFile` کی type کے ساتھ ایک file parameter بیان کریں:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

`UploadFile` استعمال کرنے کے `bytes` کے مقابلے میں کئی فوائد ہیں:

* آپ کو parameter کی default value میں `File()` استعمال کرنے کی ضرورت نہیں۔
* یہ ایک "spooled" file استعمال کرتا ہے:
    * ایک مخصوص حد تک memory میں محفوظ ہونے والی file، اور اس حد سے گزرنے کے بعد یہ disk پر محفوظ ہو جائے گی۔
* اس کا مطلب ہے کہ یہ بڑی files جیسے تصاویر، ویڈیوز، بڑی binaries وغیرہ کے لیے تمام memory استعمال کیے بغیر اچھا کام کرے گا۔
* آپ upload کی گئی file سے metadata حاصل کر سکتے ہیں۔
* اس کا ایک [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) `async` interface ہے۔
* یہ ایک حقیقی Python [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) object فراہم کرتا ہے جسے آپ براہ راست ان دوسری libraries کو دے سکتے ہیں جو file-like object کی توقع رکھتی ہیں۔

### `UploadFile` { #uploadfile }

`UploadFile` کے درج ذیل attributes ہیں:

* `filename`: ایک `str` جس میں upload کی گئی اصل file کا نام ہوتا ہے (مثلاً `myimage.jpg`)۔
* `content_type`: ایک `str` جس میں content type (MIME type / media type) ہوتا ہے (مثلاً `image/jpeg`)۔
* `file`: ایک [`SpooledTemporaryFile`](https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile) (ایک [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) object)۔ یہ حقیقی Python file object ہے جسے آپ براہ راست دوسرے functions یا libraries کو دے سکتے ہیں جو "file-like" object کی توقع رکھتے ہیں۔

`UploadFile` کے درج ذیل `async` methods ہیں۔ یہ سب اندرونی `SpooledTemporaryFile` استعمال کرتے ہوئے متعلقہ file methods کو call کرتے ہیں۔

* `write(data)`: File میں `data` (`str` یا `bytes`) لکھتا ہے۔
* `read(size)`: File کے `size` (`int`) bytes/characters پڑھتا ہے۔
* `seek(offset)`: File میں byte position `offset` (`int`) پر جاتا ہے۔
    * مثلاً `await myfile.seek(0)` file کے شروع میں لے جائے گا۔
    * یہ خاص طور پر مفید ہے اگر آپ `await myfile.read()` ایک بار چلائیں اور پھر مواد دوبارہ پڑھنا چاہیں۔
* `close()`: File کو بند کرتا ہے۔

چونکہ یہ سب `async` methods ہیں، آپ کو انہیں "await" کرنا ہوگا۔

مثال کے طور پر، ایک `async` *path operation function* کے اندر آپ مواد اس طرح حاصل کر سکتے ہیں:

```Python
contents = await myfile.read()
```

اگر آپ ایک عام `def` *path operation function* کے اندر ہیں تو آپ `UploadFile.file` تک براہ راست رسائی حاصل کر سکتے ہیں، مثال کے طور پر:

```Python
contents = myfile.file.read()
```

/// note | `async` تکنیکی تفصیلات

جب آپ `async` methods استعمال کرتے ہیں تو **FastAPI** file methods کو ایک threadpool میں چلاتا ہے اور ان کا انتظار کرتا ہے۔

///

/// note | Starlette تکنیکی تفصیلات

**FastAPI** کا `UploadFile` براہ راست **Starlette** کے `UploadFile` سے inherit ہوتا ہے، لیکن اسے **Pydantic** اور FastAPI کے دوسرے حصوں کے ساتھ مطابقت پذیر بنانے کے لیے کچھ ضروری حصے شامل کرتا ہے۔

///

## "Form Data" کیا ہے { #what-is-form-data }

HTML forms (`<form></form>`) جس طرح سے server کو data بھیجتے ہیں وہ عام طور پر اس data کے لیے ایک "خاص" encoding استعمال کرتے ہیں، جو JSON سے مختلف ہوتی ہے۔

**FastAPI** اس data کو JSON کی بجائے صحیح جگہ سے پڑھنے کو یقینی بنائے گا۔

/// note | تکنیکی تفصیلات

Forms سے آنے والا data عام طور پر "media type" `application/x-www-form-urlencoded` کے ساتھ encode ہوتا ہے جب اس میں files شامل نہ ہوں۔

لیکن جب form میں files شامل ہوں تو یہ `multipart/form-data` کے طور پر encode ہوتا ہے۔ اگر آپ `File` استعمال کرتے ہیں تو **FastAPI** جان لے گا کہ اسے body کے صحیح حصے سے files حاصل کرنی ہیں۔

اگر آپ ان encodings اور form fields کے بارے میں مزید پڑھنا چاہتے ہیں تو [<abbr title="Mozilla Developer Network">MDN</abbr> web docs for `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) دیکھیں۔

///

/// warning | انتباہ

آپ ایک *path operation* میں متعدد `File` اور `Form` parameters بیان کر سکتے ہیں، لیکن آپ ساتھ میں `Body` fields بھی بیان نہیں کر سکتے جو آپ JSON کے طور پر وصول کرنا چاہتے ہیں، کیونکہ request کا body `application/json` کی بجائے `multipart/form-data` کے ساتھ encode ہوگا۔

یہ **FastAPI** کی کوئی حد نہیں ہے، یہ HTTP protocol کا حصہ ہے۔

///

## اختیاری File Upload { #optional-file-upload }

آپ معیاری type annotations استعمال کر کے اور `None` کی default value مقرر کر کے file کو اختیاری بنا سکتے ہیں:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## اضافی Metadata کے ساتھ `UploadFile` { #uploadfile-with-additional-metadata }

آپ `File()` کو `UploadFile` کے ساتھ بھی استعمال کر سکتے ہیں، مثال کے طور پر، اضافی metadata مقرر کرنے کے لیے:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## متعدد File Uploads { #multiple-file-uploads }

ایک ہی وقت میں کئی files upload کرنا ممکن ہے۔

وہ "form data" استعمال کرتے ہوئے بھیجے گئے ایک ہی "form field" سے منسلک ہوں گی۔

اس کے لیے `bytes` یا `UploadFile` کی ایک list بیان کریں:

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

آپ کو، جیسا کہ بیان کیا گیا ہے، `bytes` یا `UploadFile` کی ایک `list` ملے گی۔

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import HTMLResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.responses` بطور `fastapi.responses` فراہم کرتا ہے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔

///

### اضافی Metadata کے ساتھ متعدد File Uploads { #multiple-file-uploads-with-additional-metadata }

اور پہلے کی طرح، آپ `File()` استعمال کر کے اضافی parameters مقرر کر سکتے ہیں، حتیٰ کہ `UploadFile` کے لیے بھی:

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## خلاصہ { #recap }

Request میں form data کے طور پر upload ہونے والی files بیان کرنے کے لیے `File`، `bytes`، اور `UploadFile` استعمال کریں۔
