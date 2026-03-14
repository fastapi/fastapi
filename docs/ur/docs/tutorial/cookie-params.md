# Cookie Parameters { #cookie-parameters }

آپ Cookie parameters کو اسی طرح define کر سکتے ہیں جیسے آپ `Query` اور `Path` parameters define کرتے ہیں۔

## `Cookie` Import کریں { #import-cookie }

سب سے پہلے `Cookie` import کریں:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` parameters declare کریں { #declare-cookie-parameters }

پھر cookie parameters کو اسی طریقے سے declare کریں جیسے `Path` اور `Query` کے ساتھ کرتے ہیں۔

آپ default value کے ساتھ ساتھ تمام اضافی validation یا annotation parameters بھی define کر سکتے ہیں:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | تکنیکی تفصیلات

`Cookie` ایک "بہن" class ہے `Path` اور `Query` کی۔ یہ بھی اسی مشترکہ `Param` class سے inherit کرتی ہے۔

لیکن یاد رکھیں کہ جب آپ `fastapi` سے `Query`، `Path`، `Cookie` اور دیگر import کرتے ہیں، تو یہ دراصل ایسے functions ہیں جو خاص classes واپس کرتے ہیں۔

///

/// info | معلومات

Cookies declare کرنے کے لیے آپ کو `Cookie` استعمال کرنا ضروری ہے، ورنہ parameters کو query parameters سمجھا جائے گا۔

///

/// info | معلومات

یہ بات ذہن میں رکھیں کہ **browsers cookies** کو خاص طریقے سے اور پردے کے پیچھے handle کرتے ہیں، اور وہ **JavaScript** کو آسانی سے انہیں چھونے **نہیں** دیتے۔

اگر آپ `/docs` پر **API docs UI** میں جائیں تو آپ اپنی *path operations* کے لیے cookies کی **documentation** دیکھ سکیں گے۔

لیکن اگر آپ **ڈیٹا بھریں** اور "Execute" پر کلک کریں، تو چونکہ docs UI **JavaScript** کے ساتھ کام کرتا ہے، cookies بھیجی نہیں جائیں گی، اور آپ کو ایک **error** پیغام نظر آئے گا جیسے آپ نے کوئی قدر نہیں لکھی۔

///

## خلاصہ { #recap }

Cookies کو `Cookie` کے ساتھ declare کریں، اسی عام pattern کو استعمال کرتے ہوئے جو `Query` اور `Path` کے لیے ہے۔
