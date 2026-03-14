# سخت Content-Type جانچ { #strict-content-type-checking }

بطور ڈیفالٹ، **FastAPI** JSON request bodies کے لیے `Content-Type` header کی سخت جانچ کرتا ہے، اس کا مطلب ہے کہ JSON requests میں body کو JSON کے طور پر parse کرنے کے لیے درست `Content-Type` header (مثلاً `application/json`) **لازمی** شامل ہونا چاہیے۔

## CSRF خطرہ { #csrf-risk }

یہ ڈیفالٹ رویہ ایک بہت مخصوص صورت میں **Cross-Site Request Forgery (CSRF)** حملوں کی ایک قسم سے تحفظ فراہم کرتا ہے۔

یہ حملے اس حقیقت کا فائدہ اٹھاتے ہیں کہ browsers scripts کو بغیر کسی CORS preflight جانچ کے requests بھیجنے دیتے ہیں جب وہ:

* `Content-Type` header نہ رکھتی ہوں (مثلاً `fetch()` کو `Blob` body کے ساتھ استعمال کرنا)
* اور کوئی authentication credentials نہ بھیجتی ہوں۔

اس قسم کا حملہ بنیادی طور پر اس وقت متعلق ہوتا ہے جب:

* ایپلیکیشن مقامی طور پر (مثلاً `localhost` پر) یا اندرونی نیٹ ورک میں چل رہی ہو
* اور ایپلیکیشن میں کوئی authentication نہ ہو، یہ توقع رکھتی ہو کہ اسی نیٹ ورک سے کوئی بھی request قابل اعتماد ہے۔

## حملے کی مثال { #example-attack }

فرض کریں آپ مقامی AI agent چلانے کا ایک طریقہ بناتے ہیں۔

یہ اس پر API فراہم کرتا ہے:

```
http://localhost:8000/v1/agents/multivac
```

اس پر frontend بھی ہے:

```
http://localhost:8000
```

/// tip | مشورہ

غور کریں کہ دونوں کا host ایک ہی ہے۔

///

پھر frontend استعمال کر کے آپ AI agent سے اپنی طرف سے کام کروا سکتے ہیں۔

چونکہ یہ **مقامی طور پر** چل رہا ہے، اور کھلے انٹرنیٹ پر نہیں، آپ فیصلہ کرتے ہیں کہ **کوئی authentication** نہ رکھیں، صرف مقامی نیٹ ورک تک رسائی پر بھروسہ کرتے ہوئے۔

پھر آپ کے صارفین میں سے کوئی اسے انسٹال اور مقامی طور پر چلا سکتا ہے۔

پھر وہ کوئی نقصان دہ ویب سائٹ کھول سکتا ہے، مثلاً:

```
https://evilhackers.example.com
```

اور وہ نقصان دہ ویب سائٹ `fetch()` سے `Blob` body کے ساتھ مقامی API کو requests بھیجتی ہے:

```
http://localhost:8000/v1/agents/multivac
```

حالانکہ نقصان دہ ویب سائٹ اور مقامی ایپ کا host مختلف ہے، browser CORS preflight request شروع نہیں کرے گا کیونکہ:

* یہ بغیر کسی authentication کے چل رہا ہے، اسے کوئی credentials بھیجنے کی ضرورت نہیں۔
* Browser سمجھتا ہے کہ یہ JSON نہیں بھیج رہا (غائب `Content-Type` header کی وجہ سے)۔

پھر نقصان دہ ویب سائٹ مقامی AI agent سے صارف کے سابق باس کو ناراض پیغامات بھیجوا سکتی ہے... یا اس سے بھی بدتر۔

## کھلا انٹرنیٹ { #open-internet }

اگر آپ کی ایپ کھلے انٹرنیٹ پر ہے تو آپ "نیٹ ورک پر بھروسہ" نہیں کریں گے اور بغیر authentication کے کسی کو بھی مراعات یافتہ requests بھیجنے دیں گے۔

حملہ آور آسانی سے آپ کے API کو requests بھیجنے کے لیے script چلا سکتے ہیں، browser کی بات چیت کی ضرورت نہیں، تو آپ شاید پہلے سے کسی بھی مراعات یافتہ endpoint کو محفوظ کر رہے ہیں۔

اس صورت میں **یہ حملہ/خطرہ آپ پر لاگو نہیں ہوتا**۔

یہ خطرہ اور حملہ بنیادی طور پر اس وقت متعلق ہے جب ایپ **مقامی نیٹ ورک** پر چلتی ہے اور یہی **واحد فرض کردہ تحفظ** ہے۔

## Content-Type کے بغیر Requests کی اجازت { #allowing-requests-without-content-type }

اگر آپ کو ایسے clients سپورٹ کرنے ہیں جو `Content-Type` header نہیں بھیجتے، تو آپ `strict_content_type=False` سیٹ کر کے سخت جانچ غیر فعال کر سکتے ہیں:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

اس setting کے ساتھ، بغیر `Content-Type` header والی requests کی body JSON کے طور پر parse ہوگی، جو FastAPI کے پرانے ورژنز کا وہی رویہ ہے۔

/// info | معلومات

یہ رویہ اور ترتیب FastAPI 0.132.0 میں شامل کی گئی۔

///
