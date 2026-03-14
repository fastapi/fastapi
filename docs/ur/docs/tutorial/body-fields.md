# Body - Fields { #body-fields }

اسی طرح جیسے آپ `Query`، `Path` اور `Body` کے ساتھ *path operation function* parameters میں اضافی توثیق اور metadata اعلان کر سکتے ہیں، آپ Pydantic کے `Field` استعمال کر کے Pydantic models کے اندر بھی توثیق اور metadata اعلان کر سکتے ہیں۔

## `Field` import کریں { #import-field }

سب سے پہلے، آپ کو اسے import کرنا ہوگا:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning | انتباہ

غور کریں کہ `Field` براہ راست `pydantic` سے import کیا جاتا ہے، نہ کہ `fastapi` سے جیسے باقی سب (`Query`، `Path`، `Body` وغیرہ)۔

///

## Model attributes اعلان کریں { #declare-model-attributes }

پھر آپ model attributes کے ساتھ `Field` استعمال کر سکتے ہیں:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` بالکل `Query`، `Path` اور `Body` کی طرح کام کرتا ہے، اس کے وہی تمام parameters وغیرہ ہیں۔

/// note | تکنیکی تفصیلات

دراصل، `Query`، `Path` اور دوسرے جو آپ آگے دیکھیں گے ایک مشترک `Param` class کی ذیلی classes کے objects بناتے ہیں، جو خود Pydantic کی `FieldInfo` class کی ذیلی class ہے۔

اور Pydantic کا `Field` بھی `FieldInfo` کا ایک instance واپس کرتا ہے۔

`Body` بھی براہ راست `FieldInfo` کی ذیلی class کے objects واپس کرتا ہے۔ اور دوسرے بھی ہیں جو آپ بعد میں دیکھیں گے جو `Body` class کی ذیلی classes ہیں۔

یاد رکھیں جب آپ `fastapi` سے `Query`، `Path` اور دوسرے import کرتے ہیں، وہ دراصل functions ہیں جو خاص classes واپس کرتے ہیں۔

///

/// tip | مشورہ

غور کریں کہ type، طے شدہ قدر اور `Field` کے ساتھ ہر model کی attribute کی ساخت ویسی ہی ہے جیسی *path operation function* کے parameter کی ہوتی ہے، `Path`، `Query` اور `Body` کی بجائے `Field` کے ساتھ۔

///

## اضافی معلومات شامل کریں { #add-extra-information }

آپ `Field`، `Query`، `Body` وغیرہ میں اضافی معلومات اعلان کر سکتے ہیں۔ اور یہ تیار کردہ JSON Schema میں شامل ہوں گی۔

آپ مثالیں اعلان کرنا سیکھتے وقت docs میں بعد میں اضافی معلومات شامل کرنے کے بارے میں مزید جانیں گے۔

/// warning | انتباہ

`Field` کو دیے گئے اضافی keys آپ کی ایپلیکیشن کے نتیجے میں بننے والے OpenAPI schema میں بھی موجود ہوں گے۔
چونکہ یہ keys ضروری نہیں کہ OpenAPI تصریح کا حصہ ہوں، کچھ OpenAPI ٹولز، مثال کے طور پر [OpenAPI validator](https://validator.swagger.io/)، شاید آپ کے تیار کردہ schema کے ساتھ کام نہ کریں۔

///

## خلاصہ { #recap }

آپ Pydantic کا `Field` استعمال کر کے model attributes کے لیے اضافی validations اور metadata اعلان کر سکتے ہیں۔

آپ اضافی JSON Schema metadata دینے کے لیے اضافی keyword arguments بھی استعمال کر سکتے ہیں۔
