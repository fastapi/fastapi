# Overrides کے ساتھ Dependencies کی جانچ { #testing-dependencies-with-overrides }

## جانچ کے دوران dependencies کو override کرنا { #overriding-dependencies-during-testing }

کچھ ایسے منظرنامے ہیں جہاں آپ جانچ کے دوران کسی dependency کو override کرنا چاہیں گے۔

آپ نہیں چاہتے کہ اصل dependency چلے (اور نہ ہی اس کی sub-dependencies)۔

اس کی بجائے، آپ ایک مختلف dependency فراہم کرنا چاہتے ہیں جو صرف جانچ کے دوران استعمال ہو (ممکنہ طور پر صرف کچھ مخصوص ٹیسٹوں میں)، اور ایسی قدر فراہم کرے جو اصل dependency کی قدر کی جگہ استعمال ہو سکے۔

### استعمال کے مواقع: بیرونی سروس { #use-cases-external-service }

ایک مثال یہ ہو سکتی ہے کہ آپ کے پاس ایک بیرونی authentication فراہم کنندہ ہے جسے آپ کو call کرنا ہے۔

آپ اسے ایک token بھیجتے ہیں اور وہ ایک authenticated صارف واپس کرتا ہے۔

یہ فراہم کنندہ شاید آپ سے فی request چارج کرتا ہو، اور اسے call کرنے میں ٹیسٹ کے لیے ایک مقررہ mock صارف رکھنے سے زیادہ وقت لگ سکتا ہے۔

آپ شاید بیرونی فراہم کنندہ کو ایک بار ٹیسٹ کرنا چاہتے ہیں، لیکن ہر ٹیسٹ کے لیے اسے call کرنا ضروری نہیں۔

اس صورت میں، آپ اس dependency کو override کر سکتے ہیں جو فراہم کنندہ کو call کرتی ہے، اور ایک حسب ضرورت dependency استعمال کر سکتے ہیں جو صرف آپ کے ٹیسٹوں کے لیے ایک mock صارف واپس کرتی ہے۔

### `app.dependency_overrides` attribute استعمال کریں { #use-the-app-dependency-overrides-attribute }

ان صورتوں کے لیے، آپ کی **FastAPI** ایپلیکیشن میں ایک attribute `app.dependency_overrides` ہے، یہ ایک سادہ `dict` ہے۔

جانچ کے لیے dependency کو override کرنے کے لیے، آپ key کے طور پر اصل dependency (ایک function) رکھیں، اور value کے طور پر اپنی dependency override (ایک اور function)۔

اور پھر **FastAPI** اصل dependency کی بجائے اس override کو call کرے گا۔

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | مشورہ

آپ اپنی **FastAPI** ایپلیکیشن میں کہیں بھی استعمال ہونے والی dependency کے لیے dependency override سیٹ کر سکتے ہیں۔

اصل dependency *path operation function*، *path operation decorator* (جب آپ واپسی قدر استعمال نہیں کرتے)، `.include_router()` call وغیرہ میں استعمال ہو سکتی ہے۔

FastAPI پھر بھی اسے override کر سکے گا۔

///

پھر آپ `app.dependency_overrides` کو خالی `dict` بنا کر اپنے overrides کو ری سیٹ (ہٹا) سکتے ہیں:

```Python
app.dependency_overrides = {}
```

/// tip | مشورہ

اگر آپ صرف کچھ ٹیسٹوں کے دوران dependency override کرنا چاہتے ہیں، تو آپ ٹیسٹ کے شروع میں (test function کے اندر) override سیٹ کر سکتے ہیں اور آخر میں (test function کے آخر میں) اسے ری سیٹ کر سکتے ہیں۔

///
