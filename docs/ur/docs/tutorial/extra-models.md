# اضافی Models { #extra-models }

پچھلی مثال سے آگے بڑھتے ہوئے، ایک سے زیادہ متعلقہ models کا ہونا عام ہوگا۔

یہ خاص طور پر user models کے معاملے میں ہوتا ہے، کیونکہ:

* **input model** میں password ہونا ضروری ہے۔
* **output model** میں password نہیں ہونا چاہیے۔
* **database model** میں شاید hashed password ہونا ضروری ہو۔

/// danger

user کے سادہ متن کے passwords کبھی ذخیرہ نہ کریں۔ ہمیشہ ایک "محفوظ hash" ذخیرہ کریں جس کی آپ بعد میں تصدیق کر سکیں۔

اگر آپ نہیں جانتے، تو آپ [سیکیورٹی ابواب](security/simple-oauth2.md#password-hashing) میں سیکھیں گے کہ "password hash" کیا ہے۔

///

## متعدد models { #multiple-models }

یہاں ایک عام خیال ہے کہ models ان کے password fields کے ساتھ کیسے نظر آ سکتے ہیں اور وہ کہاں استعمال ہوتے ہیں:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### `**user_in.model_dump()` کے بارے میں { #about-user-in-model-dump }

#### Pydantic کا `.model_dump()` { #pydantics-model-dump }

`user_in` ایک Pydantic model ہے جس کی class `UserIn` ہے۔

Pydantic models میں `.model_dump()` method ہوتا ہے جو model کے ڈیٹا کے ساتھ ایک `dict` واپس کرتا ہے۔

تو اگر ہم ایک Pydantic object `user_in` اس طرح بنائیں:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

اور پھر کال کریں:

```Python
user_dict = user_in.model_dump()
```

تو اب ہمارے پاس variable `user_dict` میں ڈیٹا کے ساتھ ایک `dict` ہے (یہ Pydantic model object کی بجائے `dict` ہے)۔

اور اگر ہم کال کریں:

```Python
print(user_dict)
```

تو ہمیں یہ Python `dict` ملے گا:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### `dict` کو Unpack کرنا { #unpacking-a-dict }

اگر ہم `user_dict` جیسا `dict` لیں اور اسے کسی function (یا class) میں `**user_dict` کے ساتھ پاس کریں، تو Python اسے "unpack" کرے گا۔ یہ `user_dict` کی keys اور values کو براہ راست key-value arguments کے طور پر پاس کرے گا۔

تو اوپر والے `user_dict` سے آگے بڑھتے ہوئے، لکھنا:

```Python
UserInDB(**user_dict)
```

اس کے برابر ہوگا:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

یا مزید درست طور پر، `user_dict` کو براہ راست استعمال کرتے ہوئے، جو بھی مواد اس میں مستقبل میں ہو:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### ایک Pydantic model دوسرے کے مواد سے { #a-pydantic-model-from-the-contents-of-another }

جیسا کہ اوپر کی مثال میں ہم نے `user_in.model_dump()` سے `user_dict` حاصل کیا، یہ code:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

اس کے برابر ہوگا:

```Python
UserInDB(**user_in.model_dump())
```

...کیونکہ `user_in.model_dump()` ایک `dict` ہے، اور پھر ہم Python سے اسے `**` لگا کر `UserInDB` میں پاس کر کے "unpack" کراتے ہیں۔

تو ہمیں ایک Pydantic model دوسرے Pydantic model کے ڈیٹا سے ملتا ہے۔

#### `dict` Unpack کرنا اور اضافی keywords { #unpacking-a-dict-and-extra-keywords }

اور پھر اضافی keyword argument `hashed_password=hashed_password` شامل کرنا، جیسے:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...یہ اس طرح بنتا ہے:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | انتباہ

معاون اضافی functions `fake_password_hasher` اور `fake_save_user` صرف ڈیٹا کے ممکنہ بہاؤ کا مظاہرہ کرنے کے لیے ہیں، لیکن یقیناً یہ کوئی حقیقی سیکیورٹی فراہم نہیں کرتے۔

///

## تکرار کم کریں { #reduce-duplication }

Code کی تکرار کم کرنا **FastAPI** کے بنیادی خیالات میں سے ایک ہے۔

کیونکہ code کی تکرار سے bugs، سیکیورٹی مسائل، code desynchronization مسائل (جب آپ ایک جگہ اپ ڈیٹ کریں لیکن دوسری جگہوں پر نہ کریں) وغیرہ کے امکانات بڑھ جاتے ہیں۔

اور یہ models سب بہت سا ڈیٹا شیئر کر رہے ہیں اور attribute نام اور types کی تکرار کر رہے ہیں۔

ہم بہتر کر سکتے ہیں۔

ہم ایک `UserBase` model declare کر سکتے ہیں جو ہمارے دوسرے models کے لیے base کا کام کرے۔ اور پھر ہم اس model کی subclasses بنا سکتے ہیں جو اس کے attributes (type declarations، validation، وغیرہ) inherit کرتی ہیں۔

تمام ڈیٹا تبدیلی، validation، documentation وغیرہ پھر بھی عام طور پر کام کریں گے۔

اس طرح، ہم صرف models کے درمیان فرق declare کر سکتے ہیں (سادہ متن `password` کے ساتھ، `hashed_password` کے ساتھ اور بغیر password کے):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` یا `anyOf` { #union-or-anyof }

آپ ایک response کو دو یا زیادہ types کا `Union` declare کر سکتے ہیں، جس کا مطلب ہے کہ response ان میں سے کوئی بھی ہو سکتا ہے۔

یہ OpenAPI میں `anyOf` کے ساتھ define ہوگا۔

اس کے لیے، معیاری Python type hint [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union) استعمال کریں:

/// note | نوٹ

[`Union`](https://docs.pydantic.dev/latest/concepts/types/#unions) define کرتے وقت، سب سے مخصوص type پہلے رکھیں، اس کے بعد کم مخصوص type۔ نیچے کی مثال میں، زیادہ مخصوص `PlaneItem` `Union[PlaneItem, CarItem]` میں `CarItem` سے پہلے آتا ہے۔

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 میں `Union` { #union-in-python-3-10 }

اس مثال میں ہم `Union[PlaneItem, CarItem]` کو argument `response_model` کی قدر کے طور پر پاس کر رہے ہیں۔

چونکہ ہم اسے **type annotation** میں رکھنے کی بجائے **argument کی قدر** کے طور پر پاس کر رہے ہیں، ہمیں Python 3.10 میں بھی `Union` استعمال کرنا ہوگا۔

اگر یہ type annotation میں ہوتا تو ہم عمودی بار استعمال کر سکتے تھے، جیسے:

```Python
some_variable: PlaneItem | CarItem
```

لیکن اگر ہم اسے assignment `response_model=PlaneItem | CarItem` میں رکھیں تو ہمیں error ملے گا، کیونکہ Python `PlaneItem` اور `CarItem` کے درمیان ایک **غلط عمل** کرنے کی کوشش کرے گا بجائے اس کے کہ اسے type annotation سمجھے۔

## Models کی List { #list-of-models }

اسی طرح، آپ objects کی lists کے responses declare کر سکتے ہیں۔

اس کے لیے، معیاری Python `list` استعمال کریں:

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## اختیاری `dict` کے ساتھ Response { #response-with-arbitrary-dict }

آپ Pydantic model استعمال کیے بغیر، صرف keys اور values کی types declare کر کے، ایک سادہ اختیاری `dict` سے بھی response declare کر سکتے ہیں۔

یہ اس وقت مفید ہے جب آپ کو پیشگی درست field/attribute نام (جو Pydantic model کے لیے ضروری ہوتے ہیں) معلوم نہ ہوں۔

اس صورت میں، آپ `dict` استعمال کر سکتے ہیں:

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## خلاصہ { #recap }

متعدد Pydantic models استعمال کریں اور ہر معاملے کے لیے آزادانہ طور پر inherit کریں۔

آپ کو ہر entity کے لیے ایک واحد ڈیٹا model رکھنے کی ضرورت نہیں ہے اگر اس entity کی مختلف "حالتیں" ہونی ہوں۔ جیسا کہ user "entity" کا معاملہ ہے جس کی حالت `password`، `password_hash` اور بغیر password کے شامل ہے۔
