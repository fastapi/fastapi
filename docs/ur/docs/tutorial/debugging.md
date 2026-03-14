# Debugging { #debugging }

آپ اپنے editor میں debugger سے connect کر سکتے ہیں، مثال کے طور پر Visual Studio Code یا PyCharm کے ساتھ۔

## `uvicorn` کو call کریں { #call-uvicorn }

اپنی FastAPI application میں، `uvicorn` کو import اور براہ راست چلائیں:

{* ../../docs_src/debugging/tutorial001_py310.py hl[1,15] *}

### `__name__ == "__main__"` کے بارے میں { #about-name-main }

`__name__ == "__main__"` کا بنیادی مقصد یہ ہے کہ کچھ code ہو جو اس وقت execute ہو جب آپ کی فائل اس طرح call کی جائے:

<div class="termy">

```console
$ python myapp.py
```

</div>

لیکن اس وقت call نہ ہو جب دوسری فائل اسے import کرے، جیسے:

```Python
from myapp import app
```

#### مزید تفصیلات { #more-details }

فرض کریں آپ کی فائل کا نام `myapp.py` ہے۔

اگر آپ اسے اس طرح چلائیں:

<div class="termy">

```console
$ python myapp.py
```

</div>

تو Python کی طرف سے خودکار طور پر بنایا گیا اندرونی variable `__name__` آپ کی فائل میں، بطور قدر string `"__main__"` رکھے گا۔

تو، یہ سیکشن:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

چلے گا۔

---

اگر آپ اس module (فائل) کو import کریں تو ایسا نہیں ہوگا۔

تو، اگر آپ کے پاس ایک اور فائل `importer.py` ہے:

```Python
from myapp import app

# Some more code
```

اس صورت میں، `myapp.py` کے اندر خودکار طور پر بنایا گیا variable `__name__` قدر `"__main__"` نہیں رکھے گا۔

تو، یہ لائن:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

execute نہیں ہوگی۔

/// info | معلومات

مزید معلومات کے لیے، [سرکاری Python دستاویزات](https://docs.python.org/3/library/__main__.html) دیکھیں۔

///

## اپنا code debugger کے ساتھ چلائیں { #run-your-code-with-your-debugger }

چونکہ آپ Uvicorn server کو اپنے code سے براہ راست چلا رہے ہیں، آپ اپنے Python program (آپ کی FastAPI application) کو debugger سے براہ راست call کر سکتے ہیں۔

---

مثال کے طور پر، Visual Studio Code میں، آپ:

* "Debug" panel پر جائیں۔
* "Add configuration..." پر کلک کریں۔
* "Python" منتخب کریں۔
* "`Python: Current File (Integrated Terminal)`" اختیار کے ساتھ debugger چلائیں۔

یہ آپ کے **FastAPI** code کے ساتھ server شروع کرے گا، آپ کے breakpoints پر رکے گا، وغیرہ۔

یہ اس طرح نظر آ سکتا ہے:

<img src="/img/tutorial/debugging/image01.png">

---

اگر آپ Pycharm استعمال کرتے ہیں، تو آپ:

* "Run" مینو کھولیں۔
* "Debug..." اختیار منتخب کریں۔
* پھر ایک context مینو ظاہر ہوگا۔
* Debug کرنے کے لیے فائل منتخب کریں (اس صورت میں، `main.py`)۔

یہ آپ کے **FastAPI** code کے ساتھ server شروع کرے گا، آپ کے breakpoints پر رکے گا، وغیرہ۔

یہ اس طرح نظر آ سکتا ہے:

<img src="/img/tutorial/debugging/image02.png">
