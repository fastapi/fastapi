# ایڈوانسڈ Python Types { #advanced-python-types }

یہاں کچھ اضافی خیالات ہیں جو Python types کے ساتھ کام کرتے وقت مفید ہو سکتے ہیں۔

## `Union` یا `Optional` کا استعمال { #using-union-or-optional }

اگر آپ کا کوڈ کسی وجہ سے `|` استعمال نہیں کر سکتا، مثلاً اگر یہ type annotation میں نہیں بلکہ `response_model=` جیسی کسی چیز میں ہے، تو عمودی بار (`|`) استعمال کرنے کی بجائے آپ `typing` سے `Union` استعمال کر سکتے ہیں۔

مثال کے طور پر، آپ بیان کر سکتے ہیں کہ کچھ `str` یا `None` ہو سکتا ہے:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` میں `None` بیان کرنے کا ایک شارٹ کٹ بھی ہے، `Optional` کے ساتھ۔

یہاں میرے بہت **ذاتی** نقطہ نظر سے ایک مشورہ:

* `Optional[SomeType]` استعمال کرنے سے بچیں
* اس کی بجائے **`Union[SomeType, None]`** استعمال کریں۔

دونوں ایک جیسے ہیں اور اندرونی طور پر وہی ہیں، لیکن میں `Optional` کی بجائے `Union` تجویز کروں گا کیونکہ لفظ "**optional**" یہ تاثر دے سکتا ہے کہ قدر اختیاری ہے، اور اس کا اصل مطلب ہے "یہ `None` ہو سکتا ہے"، چاہے یہ اختیاری نہ ہو اور پھر بھی ضروری ہو۔

مجھے لگتا ہے کہ `Union[SomeType, None]` زیادہ واضح طور پر بتاتا ہے کہ اس کا مطلب کیا ہے۔

یہ صرف الفاظ اور ناموں کے بارے میں ہے۔ لیکن یہ الفاظ اثر ڈال سکتے ہیں کہ آپ اور آپ کے ساتھی کوڈ کے بارے میں کیسے سوچتے ہیں۔

بطور مثال، یہ function لیں:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

parameter `name` کو `Optional[str]` بیان کیا گیا ہے، لیکن یہ **اختیاری نہیں** ہے، آپ function کو بغیر parameter کے نہیں بلا سکتے:

```Python
say_hi()  # اوہ نہیں، یہ غلطی دے گا!
```

`name` parameter پھر بھی **ضروری** ہے (نہ کہ *اختیاری*) کیونکہ اس کی ڈیفالٹ قدر نہیں ہے۔ پھر بھی، `name` قدر کے طور پر `None` قبول کرتا ہے:

```Python
say_hi(name=None)  # یہ کام کرتا ہے، None درست ہے
```

خوشخبری یہ ہے کہ زیادہ تر صورتوں میں، آپ آسانی سے types کی unions بیان کرنے کے لیے `|` استعمال کر سکتے ہیں:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

تو، عام طور پر آپ کو `Optional` اور `Union` جیسے ناموں کی فکر کرنے کی ضرورت نہیں ہے۔
