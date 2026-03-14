# Header Parameters { #header-parameters }

آپ Header parameters کو اسی طرح define کر سکتے ہیں جیسے آپ `Query`، `Path` اور `Cookie` parameters define کرتے ہیں۔

## `Header` Import کریں { #import-header }

سب سے پہلے `Header` import کریں:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header` parameters declare کریں { #declare-header-parameters }

پھر header parameters کو اسی طریقے سے declare کریں جیسے `Path`، `Query` اور `Cookie` کے ساتھ کرتے ہیں۔

آپ default value کے ساتھ ساتھ تمام اضافی validation یا annotation parameters بھی define کر سکتے ہیں:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | تکنیکی تفصیلات

`Header` ایک "بہن" class ہے `Path`، `Query` اور `Cookie` کی۔ یہ بھی اسی مشترکہ `Param` class سے inherit کرتی ہے۔

لیکن یاد رکھیں کہ جب آپ `fastapi` سے `Query`، `Path`، `Header` اور دیگر import کرتے ہیں، تو یہ دراصل ایسے functions ہیں جو خاص classes واپس کرتے ہیں۔

///

/// info | معلومات

Headers declare کرنے کے لیے آپ کو `Header` استعمال کرنا ضروری ہے، ورنہ parameters کو query parameters سمجھا جائے گا۔

///

## خودکار تبدیلی { #automatic-conversion }

`Header` میں `Path`، `Query` اور `Cookie` کے مقابلے میں تھوڑی اضافی فعالیت ہے۔

زیادہ تر معیاری headers "ہائفن" حرف سے الگ ہوتے ہیں، جسے "مائنس علامت" (`-`) بھی کہتے ہیں۔

لیکن `user-agent` جیسا variable Python میں غلط ہے۔

لہذا، بطور ڈیفالٹ، `Header` parameter ناموں کے حروف کو underscore (`_`) سے hyphen (`-`) میں تبدیل کرے گا تاکہ headers کو extract اور document کیا جا سکے۔

نیز، HTTP headers حروف کے بڑے چھوٹے ہونے سے بے پرواہ (case-insensitive) ہوتے ہیں، لہذا آپ انہیں معیاری Python طرز (جسے "snake_case" بھی کہتے ہیں) میں declare کر سکتے ہیں۔

تو آپ `user_agent` کو ویسے ہی استعمال کر سکتے ہیں جیسے آپ عام طور پر Python code میں کرتے ہیں، بجائے اس کے کہ پہلے حروف کو بڑا لکھیں جیسے `User_Agent` یا کچھ ایسا۔

اگر کسی وجہ سے آپ کو underscores سے hyphens میں خودکار تبدیلی بند کرنی ہو، تو `Header` کا parameter `convert_underscores` کو `False` پر سیٹ کریں:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | انتباہ

`convert_underscores` کو `False` پر سیٹ کرنے سے پہلے، یہ ذہن میں رکھیں کہ بعض HTTP proxies اور servers underscores والے headers کے استعمال کی اجازت نہیں دیتے۔

///

## ڈپلیکیٹ headers { #duplicate-headers }

ڈپلیکیٹ headers وصول کرنا ممکن ہے۔ یعنی، ایک ہی header متعدد قدروں کے ساتھ۔

آپ ان معاملات کو type declaration میں list استعمال کر کے define کر سکتے ہیں۔

آپ کو ڈپلیکیٹ header کی تمام قدریں Python `list` کے طور پر ملیں گی۔

مثال کے طور پر، `X-Token` کا header declare کرنے کے لیے جو ایک سے زیادہ بار آ سکتا ہے، آپ اس طرح لکھ سکتے ہیں:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

اگر آپ اس *path operation* کے ساتھ دو HTTP headers بھیج کر بات کریں جیسے:

```
X-Token: foo
X-Token: bar
```

تو response اس طرح ہوگا:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## خلاصہ { #recap }

Headers کو `Header` کے ساتھ declare کریں، اسی عام pattern کو استعمال کرتے ہوئے جو `Query`، `Path` اور `Cookie` کے لیے ہے۔

اور اپنے variables میں underscores کی فکر نہ کریں، **FastAPI** انہیں تبدیل کرنے کا خیال رکھے گا۔
