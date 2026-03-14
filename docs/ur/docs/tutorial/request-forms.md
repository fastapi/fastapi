# Form Data { #form-data }

جب آپ کو JSON کی بجائے form fields وصول کرنے کی ضرورت ہو تو آپ `Form` استعمال کر سکتے ہیں۔

/// info

Forms استعمال کرنے کے لیے پہلے [`python-multipart`](https://github.com/Kludex/python-multipart) انسٹال کریں۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر اسے انسٹال کریں، مثال کے طور پر:

```console
$ pip install python-multipart
```

///

## `Form` کو Import کریں { #import-form }

`fastapi` سے `Form` کو import کریں:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[3] *}

## `Form` کے parameters کی وضاحت کریں { #define-form-parameters }

Form parameters بالکل اسی طرح بنائیں جیسے آپ `Body` یا `Query` کے لیے بناتے ہیں:

{* ../../docs_src/request_forms/tutorial001_an_py310.py hl[9] *}

مثال کے طور پر، OAuth2 specification کے استعمال کے ایک طریقے میں (جسے "password flow" کہتے ہیں) `username` اور `password` کو form fields کے طور پر بھیجنا ضروری ہوتا ہے۔

<dfn title="specification">spec</dfn> کے مطابق ان fields کا نام بالکل `username` اور `password` ہونا چاہیے، اور انہیں JSON کی بجائے form fields کے طور پر بھیجا جانا چاہیے۔

`Form` کے ساتھ آپ وہی configurations بیان کر سکتے ہیں جو `Body` (اور `Query`، `Path`، `Cookie`) کے ساتھ کرتے ہیں، بشمول validation، examples، ایک alias (مثلاً `username` کی بجائے `user-name`)، وغیرہ۔

/// info

`Form` ایک class ہے جو براہ راست `Body` سے inherit ہوتی ہے۔

///

/// tip | مشورہ

Form bodies بیان کرنے کے لیے آپ کو واضح طور پر `Form` استعمال کرنا ہوگا، کیونکہ اس کے بغیر parameters کو query parameters یا body (JSON) parameters سمجھا جائے گا۔

///

## "Form Fields" کے بارے میں { #about-form-fields }

HTML forms (`<form></form>`) جس طرح سے server کو data بھیجتے ہیں وہ عام طور پر اس data کے لیے ایک "خاص" encoding استعمال کرتے ہیں، جو JSON سے مختلف ہوتی ہے۔

**FastAPI** اس data کو JSON کی بجائے صحیح جگہ سے پڑھنے کو یقینی بنائے گا۔

/// note | تکنیکی تفصیلات

Forms سے آنے والا data عام طور پر "media type" `application/x-www-form-urlencoded` کے ساتھ encode ہوتا ہے۔

لیکن جب form میں files شامل ہوں تو یہ `multipart/form-data` کے طور پر encode ہوتا ہے۔ آپ اگلے باب میں files کو سنبھالنے کے بارے میں پڑھیں گے۔

اگر آپ ان encodings اور form fields کے بارے میں مزید پڑھنا چاہتے ہیں تو [<abbr title="Mozilla Developer Network">MDN</abbr> web docs for `POST`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) دیکھیں۔

///

/// warning | انتباہ

آپ ایک *path operation* میں متعدد `Form` parameters بیان کر سکتے ہیں، لیکن آپ ساتھ میں `Body` fields بھی بیان نہیں کر سکتے جو آپ JSON کے طور پر وصول کرنا چاہتے ہیں، کیونکہ request کا body `application/json` کی بجائے `application/x-www-form-urlencoded` کے ساتھ encode ہوگا۔

یہ **FastAPI** کی کوئی حد نہیں ہے، یہ HTTP protocol کا حصہ ہے۔

///

## خلاصہ { #recap }

Form data کے input parameters بیان کرنے کے لیے `Form` استعمال کریں۔
