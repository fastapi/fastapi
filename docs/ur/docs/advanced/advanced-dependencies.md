# ایڈوانسڈ Dependencies { #advanced-dependencies }

## پیرامیٹرائزڈ dependencies { #parameterized-dependencies }

ہم نے اب تک جتنی بھی dependencies دیکھی ہیں وہ ایک مقررہ function یا class ہیں۔

لیکن ایسے مواقع ہو سکتے ہیں جہاں آپ dependency پر parameters سیٹ کرنا چاہیں، بغیر بہت سے مختلف functions یا classes بنائے۔

آئیے تصور کریں کہ ہم ایک ایسی dependency چاہتے ہیں جو چیک کرے کہ query parameter `q` میں کوئی مقررہ مواد موجود ہے یا نہیں۔

لیکن ہم اس مقررہ مواد کو پیرامیٹرائز کرنا چاہتے ہیں۔

## ایک "callable" instance { #a-callable-instance }

Python میں کسی class کے instance کو "callable" بنانے کا ایک طریقہ ہے۔

خود class نہیں (جو پہلے سے ہی callable ہے)، بلکہ اس class کا ایک instance۔

اس کے لیے ہم `__call__` method بیان کرتے ہیں:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

اس صورت میں، یہ `__call__` وہ ہے جسے **FastAPI** اضافی parameters اور sub-dependencies چیک کرنے کے لیے استعمال کرے گا، اور بعد میں آپ کے *path operation function* میں parameter کو قدر دینے کے لیے یہی call کیا جائے گا۔

## Instance کو پیرامیٹرائز کریں { #parameterize-the-instance }

اب ہم `__init__` استعمال کر کے instance کے parameters بیان کر سکتے ہیں جنہیں ہم dependency کو "پیرامیٹرائز" کرنے کے لیے استعمال کر سکتے ہیں:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

اس صورت میں، **FastAPI** کبھی `__init__` کو چھوئے گا نہ اس کی فکر کرے گا، ہم اسے براہ راست اپنے کوڈ میں استعمال کریں گے۔

## ایک instance بنائیں { #create-an-instance }

ہم اس class کا ایک instance اس طرح بنا سکتے ہیں:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

اور اس طرح ہم اپنی dependency کو "پیرامیٹرائز" کر سکتے ہیں، جس میں اب `"bar"` موجود ہے، بطور attribute `checker.fixed_content`۔

## Instance کو dependency کے طور پر استعمال کریں { #use-the-instance-as-a-dependency }

پھر ہم اس `checker` کو `Depends(checker)` میں استعمال کر سکتے ہیں، `Depends(FixedContentQueryChecker)` کی بجائے، کیونکہ dependency خود instance ہے، `checker`، نہ کہ class۔

اور dependency حل کرتے وقت، **FastAPI** اس `checker` کو اس طرح call کرے گا:

```Python
checker(q="somequery")
```

...اور جو بھی یہ واپس کرے اسے ہمارے *path operation function* میں dependency کی قدر کے طور پر parameter `fixed_content_included` میں دے گا:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | مشورہ

یہ سب کچھ پیچیدہ لگ سکتا ہے۔ اور ابھی شاید یہ واضح نہ ہو کہ یہ کتنا مفید ہے۔

یہ مثالیں جان بوجھ کر سادہ ہیں، لیکن دکھاتی ہیں کہ یہ سب کیسے کام کرتا ہے۔

Security کے ابواب میں، ایسے utility functions ہیں جو بالکل اسی طرح بنائے گئے ہیں۔

اگر آپ نے یہ سب سمجھ لیا، تو آپ پہلے سے جانتے ہیں کہ security کے لیے وہ utility tools اندرونی طور پر کیسے کام کرتے ہیں۔

///

## `yield`، `HTTPException`، `except` اور Background Tasks کے ساتھ Dependencies { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | انتباہ

آپ کو شاید ان تکنیکی تفصیلات کی ضرورت نہیں ہے۔

یہ تفصیلات بنیادی طور پر اس وقت مفید ہیں جب آپ کی FastAPI ایپلیکیشن 0.121.0 سے پرانی ہو اور آپ کو `yield` والی dependencies کے ساتھ مسائل درپیش ہوں۔

///

`yield` والی Dependencies وقت کے ساتھ مختلف استعمال کے مواقع کے لیے اور کچھ مسائل حل کرنے کے لیے بدلتی رہی ہیں، یہاں تبدیلیوں کا خلاصہ ہے۔

### `yield` اور `scope` والی Dependencies { #dependencies-with-yield-and-scope }

ورژن 0.121.0 میں، FastAPI نے `yield` والی dependencies کے لیے `Depends(scope="function")` کی سہولت شامل کی۔

`Depends(scope="function")` استعمال کرنے سے، `yield` کے بعد والا exit کوڈ *path operation function* ختم ہونے کے فوراً بعد چلتا ہے، response کلائنٹ کو واپس بھیجنے سے پہلے۔

اور `Depends(scope="request")` (جو کہ default ہے) استعمال کرنے سے، `yield` کے بعد والا exit کوڈ response بھیجنے کے بعد چلتا ہے۔

آپ اس کے بارے میں مزید [Dependencies with `yield` - Early exit and `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) کی دستاویزات میں پڑھ سکتے ہیں۔

### `yield` اور `StreamingResponse` والی Dependencies، تکنیکی تفصیلات { #dependencies-with-yield-and-streamingresponse-technical-details }

FastAPI 0.118.0 سے پہلے، اگر آپ `yield` والی dependency استعمال کرتے، تو exit کوڈ *path operation function* کے واپس آنے کے بعد لیکن response بھیجنے سے پہلے چلتا تھا۔

اس کا مقصد وسائل کو ضرورت سے زیادہ دیر تک نہ رکھنا تھا، response کے نیٹ ورک پر سفر کرنے کا انتظار کرتے ہوئے۔

اس تبدیلی کا یہ بھی مطلب تھا کہ اگر آپ `StreamingResponse` واپس کرتے، تو `yield` والی dependency کا exit کوڈ پہلے ہی چل چکا ہوتا۔

مثال کے طور پر، اگر آپ کے پاس `yield` والی dependency میں database session ہو، تو `StreamingResponse` ڈیٹا stream کرتے وقت اس session کو استعمال نہیں کر سکتا کیونکہ `yield` کے بعد exit کوڈ میں session پہلے ہی بند ہو چکا ہوتا۔

یہ رویہ 0.118.0 میں واپس بدل دیا گیا، تاکہ `yield` کے بعد والا exit کوڈ response بھیجنے کے بعد چلے۔

/// info | معلومات

جیسا کہ آپ نیچے دیکھیں گے، یہ ورژن 0.106.0 سے پہلے کے رویے سے بہت ملتا جلتا ہے، لیکن کئی بہتریوں اور خاص صورتوں میں bug fixes کے ساتھ۔

///

#### ابتدائی Exit کوڈ کے ساتھ استعمال کے مواقع { #use-cases-with-early-exit-code }

کچھ مخصوص شرائط کے ساتھ استعمال کے مواقع ہیں جو `yield` والی dependencies کے exit کوڈ کو response بھیجنے سے پہلے چلانے کے پرانے رویے سے فائدہ اٹھا سکتے ہیں۔

مثال کے طور پر، تصور کریں کہ آپ کے پاس ایسا کوڈ ہے جو `yield` والی dependency میں database session صرف صارف کی تصدیق کے لیے استعمال کرتا ہے، لیکن database session کبھی *path operation function* میں دوبارہ استعمال نہیں ہوتا، صرف dependency میں، **اور** response بھیجنے میں بہت وقت لگتا ہے، جیسے `StreamingResponse` جو آہستہ آہستہ ڈیٹا بھیجتا ہے، لیکن کسی وجہ سے database استعمال نہیں کرتا۔

اس صورت میں، database session response مکمل ہونے تک رکھا جائے گا، لیکن اگر آپ اسے استعمال نہیں کرتے، تو اسے رکھنا ضروری نہیں ہوگا۔

یہ کچھ اس طرح نظر آ سکتا ہے:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

Exit کوڈ، `Session` کی خودکار بندش:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...سست ڈیٹا بھیجنے کے بعد response مکمل ہونے پر چلے گا:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

لیکن چونکہ `generate_stream()` database session استعمال نہیں کرتا، اس لیے response بھیجتے وقت session کھلا رکھنا واقعی ضروری نہیں ہے۔

اگر آپ کے پاس SQLModel (یا SQLAlchemy) استعمال کرنے والا یہ مخصوص معاملہ ہے، تو آپ ضرورت نہ رہنے پر session کو واضح طور پر بند کر سکتے ہیں:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

اس طرح session database connection چھوڑ دے گا، تاکہ دوسری requests اسے استعمال کر سکیں۔

اگر آپ کے پاس کوئی مختلف استعمال کا موقع ہے جس میں `yield` والی dependency سے جلد باہر نکلنے کی ضرورت ہو، تو براہ کرم اپنے مخصوص استعمال کے ساتھ ایک [GitHub Discussion Question](https://github.com/fastapi/fastapi/discussions/new?category=questions) بنائیں اور بتائیں کہ آپ کو `yield` والی dependencies کے لیے جلد بند ہونے سے کیا فائدہ ہوگا۔

اگر `yield` والی dependencies میں جلد بند ہونے کے لیے قابل ذکر استعمال کے مواقع ہوں، تو میں جلد بند ہونے کا اختیار دینے کا ایک نیا طریقہ شامل کرنے پر غور کروں گا۔

### `yield` اور `except` والی Dependencies، تکنیکی تفصیلات { #dependencies-with-yield-and-except-technical-details }

FastAPI 0.110.0 سے پہلے، اگر آپ `yield` والی dependency استعمال کرتے، اور پھر اس dependency میں `except` سے کوئی exception پکڑتے، اور آپ exception دوبارہ raise نہیں کرتے تھے، تو exception خودکار طور پر کسی بھی exception handlers یا internal server error handler کو raise/forward کر دیا جاتا تھا۔

یہ ورژن 0.110.0 میں تبدیل کیا گیا تاکہ بغیر handler کے forward کیے گئے exceptions سے غیر منظم memory consumption (internal server errors) کو ٹھیک کیا جا سکے، اور اسے عام Python کوڈ کے رویے سے ہم آہنگ بنایا جا سکے۔

### Background Tasks اور `yield` والی Dependencies، تکنیکی تفصیلات { #background-tasks-and-dependencies-with-yield-technical-details }

FastAPI 0.106.0 سے پہلے، `yield` کے بعد exceptions raise کرنا ممکن نہیں تھا، `yield` والی dependencies میں exit کوڈ response بھیجنے کے *بعد* چلتا تھا، اس لیے [Exception Handlers](../tutorial/handling-errors.md#install-custom-exception-handlers) پہلے ہی چل چکے ہوتے تھے۔

یہ بنیادی طور پر اس لیے ڈیزائن کیا گیا تھا تاکہ dependencies سے "yield" کیے گئے اشیاء کو background tasks کے اندر استعمال کیا جا سکے، کیونکہ exit کوڈ background tasks مکمل ہونے کے بعد چلتا تھا۔

یہ FastAPI 0.106.0 میں اس ارادے سے تبدیل کیا گیا کہ response کے نیٹ ورک پر سفر کرنے کا انتظار کرتے ہوئے وسائل کو نہ رکھا جائے۔

/// tip | مشورہ

مزید برآں، ایک background task عام طور پر منطق کا ایک آزاد حصہ ہوتا ہے جسے الگ سے، اپنے وسائل کے ساتھ (مثلاً اپنا database connection) سنبھالا جانا چاہیے۔

اس طرح آپ کا کوڈ شاید زیادہ صاف ہوگا۔

///

اگر آپ پہلے اس رویے پر انحصار کرتے تھے، تو اب آپ کو background task کے اندر ہی background tasks کے لیے وسائل بنانے چاہئیں، اور اندرونی طور پر صرف وہ ڈیٹا استعمال کرنا چاہیے جو `yield` والی dependencies کے وسائل پر منحصر نہ ہو۔

مثال کے طور پر، ایک ہی database session استعمال کرنے کی بجائے، آپ background task کے اندر ایک نیا database session بنائیں گے، اور اس نئے session سے database سے اشیاء حاصل کریں گے۔ اور پھر background task function کو parameter کے طور پر database سے آبجیکٹ دینے کی بجائے، آپ اس آبجیکٹ کی ID دیں گے اور پھر background task function کے اندر دوبارہ آبجیکٹ حاصل کریں گے۔
