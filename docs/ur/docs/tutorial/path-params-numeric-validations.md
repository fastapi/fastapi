# Path Parameters اور عددی Validations { #path-parameters-and-numeric-validations }

اسی طرح جیسے آپ `Query` کے ساتھ query parameters کے لیے مزید validations اور metadata کا اعلان کر سکتے ہیں، آپ `Path` کے ساتھ path parameters کے لیے بھی اسی قسم کی validations اور metadata کا اعلان کر سکتے ہیں۔

## `Path` import کریں { #import-path }

سب سے پہلے، `fastapi` سے `Path` import کریں، اور `Annotated` import کریں:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | معلومات

FastAPI نے ورژن 0.95.0 میں `Annotated` کی تعاون شامل کی (اور اسے تجویز کرنا شروع کیا)۔

اگر آپ کے پاس پرانا ورژن ہے، تو `Annotated` استعمال کرنے کی کوشش کرنے پر errors آئیں گی۔

`Annotated` استعمال کرنے سے پہلے یقینی بنائیں کہ آپ [FastAPI ورژن اپ گریڈ کریں](../deployment/versions.md#upgrading-the-fastapi-versions) کم از کم 0.95.1 تک۔

///

## Metadata اعلان کریں { #declare-metadata }

آپ `Query` کی طرح تمام وہی parameters اعلان کر سکتے ہیں۔

مثال کے طور پر، path parameter `item_id` کے لیے `title` metadata قدر اعلان کرنے کے لیے آپ لکھ سکتے ہیں:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | نوٹ

Path parameter ہمیشہ لازمی ہوتا ہے کیونکہ یہ path کا حصہ ہونا ضروری ہے۔ چاہے آپ اسے `None` کے ساتھ اعلان کریں یا طے شدہ قدر سیٹ کریں، یہ کسی چیز پر اثر نہیں ڈالے گا، یہ پھر بھی ہمیشہ لازمی ہوگا۔

///

## Parameters کو اپنی ضرورت کے مطابق ترتیب دیں { #order-the-parameters-as-you-need }

/// tip | مشورہ

اگر آپ `Annotated` استعمال کرتے ہیں تو شاید یہ اتنا اہم یا ضروری نہیں ہے۔

///

فرض کریں کہ آپ query parameter `q` کو لازمی `str` کے طور پر اعلان کرنا چاہتے ہیں۔

اور آپ کو اس parameter کے لیے کچھ اور اعلان کرنے کی ضرورت نہیں، تو آپ کو واقعی `Query` استعمال کرنے کی ضرورت نہیں۔

لیکن آپ کو ابھی بھی `item_id` path parameter کے لیے `Path` استعمال کرنا ہے۔ اور آپ کسی وجہ سے `Annotated` استعمال نہیں کرنا چاہتے۔

Python شکایت کرے گا اگر آپ "طے شدہ" والی قدر کو بغیر "طے شدہ" والی قدر سے پہلے رکھیں۔

لیکن آپ انہیں دوبارہ ترتیب دے سکتے ہیں، اور بغیر طے شدہ والی قدر (query parameter `q`) کو پہلے رکھ سکتے ہیں۔

**FastAPI** کے لیے اس سے فرق نہیں پڑتا۔ یہ parameters کو ان کے ناموں، اقسام اور طے شدہ اعلانات (`Query`، `Path` وغیرہ) سے پہچانے گا، ترتیب سے کوئی فرق نہیں پڑتا۔

تو، آپ اپنا function اس طرح اعلان کر سکتے ہیں:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

لیکن یاد رکھیں کہ اگر آپ `Annotated` استعمال کرتے ہیں، تو آپ کو یہ مسئلہ نہیں ہوگا، کوئی فرق نہیں پڑتا کیونکہ آپ `Query()` یا `Path()` کے لیے function parameter طے شدہ اقدار استعمال نہیں کر رہے۔

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## Parameters کو اپنی ضرورت کے مطابق ترتیب دیں، ترکیبیں { #order-the-parameters-as-you-need-tricks }

/// tip | مشورہ

اگر آپ `Annotated` استعمال کرتے ہیں تو شاید یہ اتنا اہم یا ضروری نہیں ہے۔

///

یہاں ایک **چھوٹی ترکیب** ہے جو کام آ سکتی ہے، لیکن آپ کو اکثر اس کی ضرورت نہیں ہوگی۔

اگر آپ چاہتے ہیں:

* `q` query parameter کو `Query` یا کسی طے شدہ قدر کے بغیر اعلان کرنا
* `item_id` path parameter کو `Path` استعمال کر کے اعلان کرنا
* انہیں مختلف ترتیب میں رکھنا
* `Annotated` استعمال نہ کرنا

...Python میں اس کے لیے ایک خاص syntax ہے۔

Function کے پہلے parameter کے طور پر `*` دیں۔

Python اس `*` کے ساتھ کچھ نہیں کرے گا، لیکن یہ جان لے گا کہ تمام اگلے parameters کو keyword arguments (key-value جوڑوں) کے طور پر کال کیا جانا چاہیے، جنہیں <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr> بھی کہتے ہیں۔ چاہے ان کی طے شدہ قدر نہ ہو۔

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### `Annotated` کے ساتھ بہتر { #better-with-annotated }

یاد رکھیں کہ اگر آپ `Annotated` استعمال کرتے ہیں، چونکہ آپ function parameter طے شدہ اقدار استعمال نہیں کر رہے، تو آپ کو یہ مسئلہ نہیں ہوگا، اور شاید آپ کو `*` استعمال کرنے کی ضرورت نہیں ہوگی۔

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## عددی validations: اس سے بڑا یا مساوی { #number-validations-greater-than-or-equal }

`Query` اور `Path` (اور دوسرے جو آپ بعد میں دیکھیں گے) کے ساتھ آپ عددی حدود کا اعلان کر سکتے ہیں۔

یہاں، `ge=1` کے ساتھ، `item_id` کو ایک integer نمبر ہونا ہوگا جو `1` سے "`g`reater than or `e`qual" ہو۔

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## عددی validations: اس سے بڑا اور اس سے چھوٹا یا مساوی { #number-validations-greater-than-and-less-than-or-equal }

یہی لاگو ہوتا ہے:

* `gt`: `g`reater `t`han (اس سے بڑا)
* `le`: `l`ess than or `e`qual (اس سے چھوٹا یا مساوی)

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## عددی validations: floats، اس سے بڑا اور اس سے چھوٹا { #number-validations-floats-greater-than-and-less-than }

عددی validations `float` اقدار کے لیے بھی کام کرتی ہیں۔

یہاں جہاں یہ اہم ہو جاتا ہے کہ <abbr title="greater than"><code>gt</code></abbr> اعلان کر سکیں نہ کہ صرف <abbr title="greater than or equal"><code>ge</code></abbr>۔ اس کے ساتھ آپ مثال کے طور پر تقاضا کر سکتے ہیں کہ قدر `0` سے بڑی ہونی چاہیے، چاہے یہ `1` سے کم ہو۔

تو، `0.5` ایک درست قدر ہوگی۔ لیکن `0.0` یا `0` نہیں ہوگی۔

اور <abbr title="less than"><code>lt</code></abbr> کے لیے بھی یہی ہے۔

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## خلاصہ { #recap }

`Query`، `Path` (اور دوسرے جو آپ نے ابھی نہیں دیکھے) کے ساتھ آپ [Query Parameters اور String Validations](query-params-str-validations.md) کی طرح ہی metadata اور string validations اعلان کر سکتے ہیں۔

اور آپ عددی validations بھی اعلان کر سکتے ہیں:

* `gt`: `g`reater `t`han (اس سے بڑا)
* `ge`: `g`reater than or `e`qual (اس سے بڑا یا مساوی)
* `lt`: `l`ess `t`han (اس سے چھوٹا)
* `le`: `l`ess than or `e`qual (اس سے چھوٹا یا مساوی)

/// info | معلومات

`Query`، `Path`، اور دوسری classes جو آپ بعد میں دیکھیں گے ایک مشترک `Param` class کی ذیلی classes ہیں۔

یہ سب اضافی توثیق اور metadata کے لیے وہی parameters شیئر کرتی ہیں جو آپ نے دیکھے ہیں۔

///

/// note | تکنیکی تفصیلات

جب آپ `fastapi` سے `Query`، `Path` اور دوسرے import کرتے ہیں، تو وہ دراصل functions ہیں۔

جب کال کیے جاتے ہیں، تو وہ اسی نام کی classes کے instances واپس کرتے ہیں۔

تو، آپ `Query` import کرتے ہیں، جو ایک function ہے۔ اور جب آپ اسے کال کرتے ہیں، تو یہ `Query` نامی class کا بھی ایک instance واپس کرتا ہے۔

یہ functions اس لیے ہیں (classes کو براہ راست استعمال کرنے کی بجائے) تاکہ آپ کا ایڈیٹر ان کی اقسام کے بارے میں errors نہ دکھائے۔

اس طرح آپ ان errors کو نظرانداز کرنے کے لیے حسب ضرورت ترتیبات شامل کیے بغیر اپنا عام ایڈیٹر اور کوڈنگ ٹولز استعمال کر سکتے ہیں۔

///
