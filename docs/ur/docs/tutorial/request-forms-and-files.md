# Request Forms اور Files { #request-forms-and-files }

آپ `File` اور `Form` استعمال کر کے ایک ہی وقت میں files اور form fields کی وضاحت کر سکتے ہیں۔

/// info

Upload کی گئی files اور/یا form data وصول کرنے کے لیے پہلے [`python-multipart`](https://github.com/Kludex/python-multipart) انسٹال کریں۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر اسے انسٹال کریں، مثال کے طور پر:

```console
$ pip install python-multipart
```

///

## `File` اور `Form` کو Import کریں { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## `File` اور `Form` کے parameters کی وضاحت کریں { #define-file-and-form-parameters }

File اور form parameters بالکل اسی طرح بنائیں جیسے آپ `Body` یا `Query` کے لیے بناتے ہیں:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

Files اور form fields، form data کے طور پر upload ہوں گے اور آپ کو files اور form fields موصول ہوں گے۔

اور آپ کچھ files کو `bytes` اور کچھ کو `UploadFile` کے طور پر بیان کر سکتے ہیں۔

/// warning | انتباہ

آپ ایک *path operation* میں متعدد `File` اور `Form` parameters بیان کر سکتے ہیں، لیکن آپ ساتھ میں `Body` fields بھی بیان نہیں کر سکتے جو آپ JSON کے طور پر وصول کرنا چاہتے ہیں، کیونکہ request کا body `application/json` کی بجائے `multipart/form-data` کے ساتھ encode ہوگا۔

یہ **FastAPI** کی کوئی حد نہیں ہے، یہ HTTP protocol کا حصہ ہے۔

///

## خلاصہ { #recap }

جب آپ کو ایک ہی request میں data اور files دونوں وصول کرنے کی ضرورت ہو تو `File` اور `Form` کو ایک ساتھ استعمال کریں۔
