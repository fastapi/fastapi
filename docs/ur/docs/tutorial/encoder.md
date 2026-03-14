# JSON Compatible Encoder { #json-compatible-encoder }

کچھ ایسے معاملات ہیں جن میں آپ کو کسی data type (جیسے Pydantic model) کو JSON کے ساتھ مطابقت رکھنے والی چیز (جیسے `dict`، `list` وغیرہ) میں تبدیل کرنے کی ضرورت ہو سکتی ہے۔

مثال کے طور پر، اگر آپ کو اسے database میں محفوظ کرنا ہو۔

اس کے لیے **FastAPI** ایک `jsonable_encoder()` function فراہم کرتا ہے۔

## `jsonable_encoder` کا استعمال { #using-the-jsonable-encoder }

آئیے تصور کریں کہ آپ کے پاس ایک database `fake_db` ہے جو صرف JSON کے ساتھ مطابقت رکھنے والا data وصول کرتا ہے۔

مثال کے طور پر، یہ `datetime` objects وصول نہیں کرتا، کیونکہ وہ JSON کے ساتھ مطابقت نہیں رکھتے۔

تو ایک `datetime` object کو [ISO format](https://en.wikipedia.org/wiki/ISO_8601) میں data رکھنے والی `str` میں تبدیل کرنا ہوگا۔

اسی طرح، یہ database کوئی Pydantic model (attributes والا object) وصول نہیں کرے گا، صرف ایک `dict`۔

آپ اس کے لیے `jsonable_encoder` استعمال کر سکتے ہیں۔

یہ ایک object وصول کرتا ہے، جیسے Pydantic model، اور اس کا JSON کے ساتھ مطابقت رکھنے والا version واپس کرتا ہے:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

اس مثال میں، یہ Pydantic model کو `dict` میں، اور `datetime` کو `str` میں تبدیل کرے گا۔

اسے call کرنے کا نتیجہ ایسی چیز ہے جسے Python کے معیاری [`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps) کے ساتھ encode کیا جا سکتا ہے۔

یہ JSON format میں data رکھنے والی کوئی بڑی `str` واپس نہیں کرتا (بطور string)۔ یہ Python کا معیاری data structure (مثلاً ایک `dict`) واپس کرتا ہے جس کی values اور ذیلی values سب JSON کے ساتھ مطابقت رکھتی ہیں۔

/// note | نوٹ

`jsonable_encoder` دراصل **FastAPI** اندرونی طور پر data تبدیل کرنے کے لیے استعمال کرتا ہے۔ لیکن یہ بہت سے دوسرے منظرناموں میں بھی مفید ہے۔

///
