# Static Files { #static-files }

آپ `StaticFiles` استعمال کر کے ایک directory سے static files خودکار طور پر serve کر سکتے ہیں۔

## `StaticFiles` استعمال کریں { #use-staticfiles }

* `StaticFiles` import کریں۔
* ایک مخصوص path پر `StaticFiles()` instance کو "Mount" کریں۔

{* ../../docs_src/static_files/tutorial001_py310.py hl[2,6] *}

/// note | تکنیکی تفصیلات

آپ `from starlette.staticfiles import StaticFiles` بھی استعمال کر سکتے ہیں۔

**FastAPI** آپ کی سہولت کے لیے وہی `starlette.staticfiles` بطور `fastapi.staticfiles` فراہم کرتا ہے۔ لیکن یہ دراصل براہ راست Starlette سے آتا ہے۔

///

### "Mounting" کیا ہے { #what-is-mounting }

"Mounting" کا مطلب ہے ایک مکمل "آزاد" application کو کسی مخصوص path پر شامل کرنا، جو پھر تمام sub-paths کو handle کرنے کا ذمہ لے لیتی ہے۔

یہ `APIRouter` استعمال کرنے سے مختلف ہے کیونکہ mount شدہ application مکمل طور پر آزاد ہوتی ہے۔ آپ کی مرکزی application کا OpenAPI اور docs mount شدہ application سے کچھ بھی شامل نہیں کریں گے، وغیرہ۔

آپ اس کے بارے میں مزید [Advanced User Guide](../advanced/index.md) میں پڑھ سکتے ہیں۔

## تفصیلات { #details }

پہلا `"/static"` اس sub-path سے مراد ہے جس پر یہ "sub-application" "mount" ہوگی۔ تو، کوئی بھی path جو `"/static"` سے شروع ہو اسے اس کے ذریعے handle کیا جائے گا۔

`directory="static"` آپ کی static files پر مشتمل directory کے نام سے مراد ہے۔

`name="static"` اسے ایک نام دیتا ہے جو **FastAPI** کی طرف سے اندرونی طور پر استعمال کیا جا سکتا ہے۔

یہ تمام parameters "`static`" سے مختلف ہو سکتے ہیں، انہیں اپنی application کی ضروریات اور مخصوص تفصیلات کے مطابق ایڈجسٹ کریں۔

## مزید معلومات { #more-info }

مزید تفصیلات اور اختیارات کے لیے [Starlette کی Static Files کی دستاویزات](https://www.starlette.dev/staticfiles/) دیکھیں۔
