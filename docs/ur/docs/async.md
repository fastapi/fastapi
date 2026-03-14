# Concurrency اور async / await { #concurrency-and-async-await }

*path operation functions* کے لیے `async def` syntax کے بارے میں تفصیلات اور asynchronous code، concurrency، اور parallelism کا پس منظر۔

## جلدی میں ہیں؟ { #in-a-hurry }

<abbr title="too long; didn't read"><strong>TL;DR:</strong></abbr>

اگر آپ third party libraries استعمال کر رہے ہیں جو آپ سے `await` کے ساتھ call کرنے کو کہتی ہیں، جیسے:

```Python
results = await some_library()
```

تو اپنے *path operation functions* کو `async def` کے ساتھ declare کریں جیسے:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | نوٹ

آپ `await` صرف `async def` سے بنائے گئے functions کے اندر استعمال کر سکتے ہیں۔

///

---

اگر آپ کوئی third party library استعمال کر رہے ہیں جو کسی چیز سے communicate کرتی ہے (database، API، file system وغیرہ) اور `await` کے استعمال کی سہولت نہیں رکھتی (فی الحال زیادہ تر database libraries کے ساتھ یہی صورتحال ہے)، تو اپنے *path operation functions* کو عام طریقے سے صرف `def` کے ساتھ declare کریں، جیسے:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

اگر آپ کی application کو (کسی بھی طرح) کسی اور چیز سے communicate کرکے اس کے جواب کا انتظار نہیں کرنا ہے، تو `async def` استعمال کریں، چاہے آپ کو اندر `await` استعمال کرنے کی ضرورت نہ ہو۔

---

اگر آپ کو نہیں معلوم، تو عام `def` استعمال کریں۔

---

**نوٹ**: آپ اپنے *path operation functions* میں `def` اور `async def` کو جتنا چاہیں ملا جلا کر استعمال کر سکتے ہیں اور ہر ایک کو اپنی بہترین ضرورت کے مطابق define کر سکتے ہیں۔ FastAPI ان کے ساتھ صحیح طریقے سے کام کرے گا۔

بہرحال، اوپر کے کسی بھی معاملے میں، FastAPI پھر بھی asynchronously کام کرے گا اور انتہائی تیز ہوگا۔

لیکن اوپر دیے گئے اقدامات پر عمل کرنے سے، یہ کچھ performance optimizations کر سکے گا۔

## تکنیکی تفصیلات { #technical-details }

Python کے جدید ورژنز **"asynchronous code"** کی سہولت فراہم کرتے ہیں جسے **"coroutines"** کہتے ہیں، **`async` اور `await`** syntax کے ساتھ۔

آئیے اس جملے کو نیچے دیے گئے حصوں میں تفصیل سے دیکھتے ہیں:

* **Asynchronous Code**
* **`async` اور `await`**
* **Coroutines**

## Asynchronous Code { #asynchronous-code }

Asynchronous code کا مطلب صرف یہ ہے کہ زبان 💬 کے پاس computer / program 🤖 کو یہ بتانے کا ایک طریقہ ہے کہ code میں کسی مقام پر، اسے 🤖 کسی اور جگہ *کچھ اور* مکمل ہونے کا انتظار کرنا ہوگا۔ فرض کریں کہ وہ *کچھ اور* "slow-file" 📝 کہلاتا ہے۔

تو اس وقت کے دوران، computer جا کر کوئی اور کام کر سکتا ہے، جب تک "slow-file" 📝 مکمل ہوتا ہے۔

پھر computer / program 🤖 ہر بار واپس آئے گا جب اسے موقع ملے کیونکہ وہ دوبارہ انتظار میں ہے، یا جب بھی اس 🤖 نے اس وقت تک کا سارا کام مکمل کر لیا ہو۔ اور یہ 🤖 دیکھے گا کہ جن tasks کا انتظار تھا ان میں سے کوئی مکمل ہو چکا ہے، اور جو کچھ اسے کرنا تھا وہ کرے گا۔

پھر، یہ 🤖 مکمل ہونے والا پہلا task لیتا ہے (فرض کریں ہمارا "slow-file" 📝) اور جو کچھ اسے اس کے ساتھ کرنا تھا وہ جاری رکھتا ہے۔

وہ "کسی اور چیز کا انتظار" عام طور پر <abbr title="Input and Output">I/O</abbr> operations کی طرف اشارہ کرتا ہے جو نسبتاً "سست" ہوتے ہیں (processor اور RAM memory کی رفتار کے مقابلے میں)، جیسے انتظار کرنا:

* client کے ذریعے network سے بھیجے جانے والے data کا
* آپ کے program کے ذریعے بھیجے گئے data کا client تک network سے پہنچنے کا
* disk پر فائل کے مواد کو system کے ذریعے پڑھ کر آپ کے program کو دینے کا
* آپ کے program نے system کو جو مواد دیا اسے disk پر لکھنے کا
* ایک remote API operation کا
* ایک database operation مکمل ہونے کا
* ایک database query کے نتائج واپس آنے کا
* وغیرہ۔

چونکہ execution time زیادہ تر <abbr title="Input and Output">I/O</abbr> operations کے انتظار میں صرف ہوتا ہے، انہیں "I/O bound" operations کہتے ہیں۔

اسے "asynchronous" اس لیے کہتے ہیں کیونکہ computer / program کو سست task کے ساتھ "synchronized" نہیں رہنا پڑتا، task مکمل ہونے کے صحیح لمحے کا انتظار کرتے ہوئے کچھ نہ کرتے ہوئے، تاکہ task کا نتیجہ لے کر کام جاری رکھ سکے۔

اس کی بجائے، ایک "asynchronous" system ہونے کی وجہ سے، ایک بار مکمل ہونے کے بعد، task تھوڑی دیر (کچھ microseconds) قطار میں انتظار کر سکتا ہے جب تک computer / program جو بھی کام کر رہا تھا وہ مکمل کرے، اور پھر واپس آ کر نتائج لے اور ان کے ساتھ کام جاری رکھے۔

"Synchronous" ("asynchronous" کے برعکس) کے لیے عام طور پر "sequential" کی اصطلاح بھی استعمال ہوتی ہے، کیونکہ computer / program تمام مراحل کو ترتیب سے follow کرتا ہے کسی مختلف task پر جانے سے پہلے، چاہے ان مراحل میں انتظار شامل ہو۔

### Concurrency اور برگرز { #concurrency-and-burgers }

اوپر بیان کردہ **asynchronous** code کے اس تصور کو بعض اوقات **"concurrency"** بھی کہا جاتا ہے۔ یہ **"parallelism"** سے مختلف ہے۔

**Concurrency** اور **parallelism** دونوں کا تعلق "مختلف چیزوں کا کم و بیش ایک ہی وقت میں ہونا" سے ہے۔

لیکن *concurrency* اور *parallelism* کے درمیان تفصیلات کافی مختلف ہیں۔

فرق سمجھنے کے لیے، برگرز کے بارے میں یہ کہانی تصور کریں:

### Concurrent برگرز { #concurrent-burgers }

آپ اپنے ساتھی کے ساتھ fast food لینے جاتے ہیں، آپ قطار میں کھڑے ہوتے ہیں جب کہ cashier آپ سے پہلے والے لوگوں کے آرڈرز لے رہا ہوتا ہے۔ 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

پھر آپ کی باری آتی ہے، آپ اپنے ساتھی اور اپنے لیے 2 بہت عمدہ برگرز کا آرڈر دیتے ہیں۔ 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Cashier کچن میں باورچی کو کچھ کہتا ہے تاکہ انہیں معلوم ہو کہ آپ کے برگرز تیار کرنے ہیں (حالانکہ وہ ابھی پہلے والے گاہکوں کے برگرز تیار کر رہے ہیں)۔

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

آپ ادائیگی کرتے ہیں۔ 💸

Cashier آپ کو آپ کی باری کا نمبر دیتا ہے۔

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

جب آپ انتظار کر رہے ہوتے ہیں، آپ اپنے ساتھی کے ساتھ جا کر ایک میز چنتے ہیں، بیٹھتے ہیں اور کافی دیر تک بات کرتے ہیں (کیونکہ آپ کے برگرز بہت عمدہ ہیں اور تیار ہونے میں وقت لگتا ہے)۔

جب آپ اپنے ساتھی کے ساتھ میز پر بیٹھے برگرز کا انتظار کر رہے ہوتے ہیں، آپ اس وقت کو یہ دیکھنے میں صرف کر سکتے ہیں کہ آپ کا ساتھی کتنا زبردست، خوبصورت اور ذہین ہے ✨😍✨۔

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

انتظار کرتے ہوئے اور اپنے ساتھی سے بات کرتے ہوئے، وقتاً فوقتاً آپ کاؤنٹر پر دکھائے جانے والے نمبر کو چیک کرتے ہیں کہ کیا آپ کی باری آ گئی ہے۔

پھر کسی وقت، آخرکار آپ کی باری آتی ہے۔ آپ کاؤنٹر پر جاتے ہیں، اپنے برگرز لیتے ہیں اور واپس میز پر آتے ہیں۔

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

آپ اور آپ کا ساتھی برگرز کھاتے ہیں اور اچھا وقت گزارتے ہیں۔ ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info | معلومات

خوبصورت تصاویر بنانے والی [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot)۔ 🎨

///

---

تصور کریں کہ آپ اس کہانی میں computer / program 🤖 ہیں۔

جب آپ قطار میں ہوتے ہیں، آپ بس خالی بیٹھے 😴 اپنی باری کا انتظار کر رہے ہوتے ہیں، کوئی خاص "productive" کام نہیں کر رہے۔ لیکن قطار تیز ہے کیونکہ cashier صرف آرڈرز لے رہا ہے (تیار نہیں کر رہا)، تو یہ ٹھیک ہے۔

پھر جب آپ کی باری آتی ہے، آپ حقیقی "productive" کام کرتے ہیں، مینو پر غور کرتے ہیں، فیصلہ کرتے ہیں کہ آپ کیا چاہتے ہیں، اپنے ساتھی کی پسند لیتے ہیں، ادائیگی کرتے ہیں، چیک کرتے ہیں کہ آپ نے صحیح بل یا کارڈ دیا ہے، چیک کرتے ہیں کہ آپ سے صحیح رقم لی گئی ہے، چیک کرتے ہیں کہ آرڈر میں صحیح آئٹمز ہیں، وغیرہ۔

لیکن پھر، حالانکہ آپ کے پاس ابھی تک برگرز نہیں ہیں، cashier کے ساتھ آپ کا کام "روک" ⏸ پر ہے، کیونکہ آپ کو اپنے برگرز تیار ہونے کا انتظار 🕙 کرنا ہے۔

لیکن جیسے ہی آپ کاؤنٹر سے ہٹ کر اپنی باری کے نمبر کے ساتھ میز پر بیٹھتے ہیں، آپ اپنی توجہ 🔀 اپنے ساتھی کی طرف کر سکتے ہیں، اور اس پر "کام" ⏯ 🤓 کر سکتے ہیں۔ پھر آپ دوبارہ کچھ بہت "productive" کر رہے ہیں جیسے اپنے ساتھی سے فلرٹ کرنا 😍۔

پھر cashier 💁 کہتا ہے "میں نے برگرز تیار کر دیے" آپ کا نمبر کاؤنٹر کی display پر لگا کر، لیکن آپ پاگلوں کی طرح فوراً نہیں کودتے جب display نمبر آپ کی باری کے نمبر پر بدلتا ہے۔ آپ جانتے ہیں کہ کوئی آپ کے برگرز نہیں چرائے گا کیونکہ آپ کے پاس آپ کی باری کا نمبر ہے، اور ان کے پاس ان کا۔

تو آپ اپنے ساتھی کی کہانی مکمل ہونے کا انتظار کرتے ہیں (موجودہ کام ⏯ / task مکمل ہونا 🤓)، نرمی سے مسکراتے ہیں اور کہتے ہیں کہ آپ برگرز لینے جا رہے ہیں ⏸۔

پھر آپ کاؤنٹر 🔀 پر جاتے ہیں، اس ابتدائی task کی طرف جو اب مکمل ہو چکا ہے ⏯، برگرز لیتے ہیں، شکریہ کہتے ہیں اور انہیں میز پر لے آتے ہیں۔ یہ کاؤنٹر کے ساتھ تعامل کا وہ مرحلہ / task ختم کرتا ہے ⏹۔ یہ بدلے میں ایک نیا task شروع کرتا ہے، "برگرز کھانا" 🔀 ⏯، لیکن پچھلا "برگرز لینا" مکمل ہو چکا ہے ⏹۔

### Parallel برگرز { #parallel-burgers }

اب تصور کریں کہ یہ "Concurrent برگرز" نہیں بلکہ "Parallel برگرز" ہیں۔

آپ اپنے ساتھی کے ساتھ parallel fast food لینے جاتے ہیں۔

آپ قطار میں کھڑے ہوتے ہیں جب کہ کئی (فرض کریں 8) cashiers جو بیک وقت باورچی بھی ہیں، آپ سے پہلے والے لوگوں کے آرڈرز لے رہے ہیں۔

آپ سے پہلے ہر شخص کاؤنٹر چھوڑنے سے پہلے اپنے برگرز تیار ہونے کا انتظار کر رہا ہے کیونکہ 8 cashiers میں سے ہر ایک اگلا آرڈر لینے سے پہلے برگر فوراً تیار کرتا ہے۔

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

پھر آخرکار آپ کی باری آتی ہے، آپ اپنے ساتھی اور اپنے لیے 2 بہت عمدہ برگرز کا آرڈر دیتے ہیں۔

آپ ادائیگی کرتے ہیں 💸۔

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Cashier کچن میں جاتا ہے۔

آپ کاؤنٹر کے سامنے کھڑے رہتے ہیں 🕙، تاکہ کوئی اور آپ سے پہلے آپ کے برگرز نہ لے لے، کیونکہ باری کے نمبر نہیں ہیں۔

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

چونکہ آپ اور آپ کا ساتھی کسی کو اپنے سامنے آنے اور جب بھی وہ آئیں آپ کے برگرز لینے سے روکنے میں مصروف ہیں، آپ اپنے ساتھی پر توجہ نہیں دے سکتے۔ 😞

یہ "synchronous" کام ہے، آپ cashier/باورچی 👨‍🍳 کے ساتھ "synchronized" ہیں۔ آپ کو انتظار 🕙 کرنا ہے اور بالکل اس لمحے وہاں موجود ہونا ہے جب cashier/باورچی 👨‍🍳 برگرز مکمل کرے اور آپ کو دے، ورنہ کوئی اور لے سکتا ہے۔

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

پھر آپ کا cashier/باورچی 👨‍🍳 آخرکار آپ کے برگرز لے کر واپس آتا ہے، کاؤنٹر کے سامنے لمبے انتظار 🕙 کے بعد۔

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

آپ اپنے برگرز لیتے ہیں اور اپنے ساتھی کے ساتھ میز پر جاتے ہیں۔

آپ بس انہیں کھاتے ہیں، اور ہو گیا۔ ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

زیادہ بات چیت یا فلرٹنگ نہیں ہوئی کیونکہ زیادہ تر وقت کاؤنٹر کے سامنے انتظار 🕙 میں صرف ہوا۔ 😞

/// info | معلومات

خوبصورت تصاویر بنانے والی [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot)۔ 🎨

///

---

Parallel برگرز کے اس منظرنامے میں، آپ ایک computer / program 🤖 ہیں جس کے دو processors ہیں (آپ اور آپ کا ساتھی)، دونوں انتظار 🕙 کر رہے ہیں اور اپنی توجہ ⏯ "کاؤنٹر پر انتظار" 🕙 میں لمبے عرصے تک لگائے ہوئے ہیں۔

Fast food store کے 8 processors (cashiers/باورچی) ہیں۔ جبکہ concurrent برگرز والے store میں شاید صرف 2 ہوں (ایک cashier اور ایک باورچی)۔

لیکن پھر بھی، حتمی تجربہ بہترین نہیں ہے۔ 😞

---

یہ برگرز کی parallel مساوی کہانی ہوگی۔ 🍔

"حقیقی زندگی" کی مزید مثال کے لیے، ایک بینک تصور کریں۔

حال ہی تک، زیادہ تر بینکوں میں متعدد cashiers 👨‍💼👨‍💼👨‍💼👨‍💼 ہوتے تھے اور ایک بڑی قطار 🕙🕙🕙🕙🕙🕙🕙🕙۔

تمام cashiers ایک کے بعد ایک client کے ساتھ سارا کام کرتے 👨‍💼⏯۔

اور آپ کو قطار میں لمبا انتظار 🕙 کرنا ہوتا ہے ورنہ آپ اپنی باری کھو دیتے ہیں۔

آپ شاید اپنے ساتھی 😍 کو اپنے ساتھ بینک 🏦 میں کام کرانے نہیں لے جانا چاہیں گے۔

### برگرز کا نتیجہ { #burger-conclusion }

"اپنے ساتھی کے ساتھ fast food برگرز" کے اس منظرنامے میں، چونکہ بہت زیادہ انتظار 🕙 ہے، concurrent system ⏸🔀⏯ رکھنا بہت زیادہ معنی رکھتا ہے۔

زیادہ تر web applications کے ساتھ یہی معاملہ ہے۔

بہت سارے، بہت سارے users، لیکن آپ کا server ان کے اتنے اچھے نہ ہونے والے connection سے requests بھیجنے کا انتظار 🕙 کر رہا ہے۔

اور پھر دوبارہ responses واپس آنے کا انتظار 🕙۔

یہ "انتظار" 🕙 microseconds میں ماپا جاتا ہے، لیکن پھر بھی، سب کو جمع کریں تو آخر میں بہت زیادہ انتظار ہوتا ہے۔

اسی لیے web APIs کے لیے asynchronous ⏸🔀⏯ code استعمال کرنا بہت معنی رکھتا ہے۔

اسی قسم کی asynchronicity نے NodeJS کو مقبول بنایا (حالانکہ NodeJS parallel نہیں ہے) اور یہی Go کی بطور programming language طاقت ہے۔

اور یہ وہی سطح کی performance ہے جو آپ کو **FastAPI** کے ساتھ ملتی ہے۔

اور چونکہ آپ parallelism اور asynchronicity دونوں بیک وقت حاصل کر سکتے ہیں، آپ کو زیادہ تر tested NodeJS frameworks سے زیادہ اور Go کے برابر performance ملتی ہے، جو C کے قریب ایک compiled language ہے [(یہ سب Starlette کی بدولت ہے)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1)۔

### کیا concurrency، parallelism سے بہتر ہے؟ { #is-concurrency-better-than-parallelism }

نہیں! یہ کہانی کا سبق نہیں ہے۔

Concurrency، parallelism سے مختلف ہے۔ اور یہ ان **مخصوص** منظرناموں میں بہتر ہے جن میں بہت زیادہ انتظار شامل ہو۔ اس وجہ سے، یہ عام طور پر web application development کے لیے parallelism سے بہت بہتر ہے۔ لیکن ہر چیز کے لیے نہیں۔

تو اسے متوازن کرنے کے لیے، یہ مختصر کہانی تصور کریں:

> آپ کو ایک بڑا، گندا گھر صاف کرنا ہے۔

*ہاں، یہی پوری کہانی ہے*۔

---

کہیں بھی انتظار 🕙 نہیں ہے، بس گھر کی مختلف جگہوں پر بہت سارا کام کرنا ہے۔

آپ برگرز کی مثال کی طرح باریاں لے سکتے ہیں، پہلے بیٹھک، پھر کچن، لیکن چونکہ آپ کسی چیز کا انتظار 🕙 نہیں کر رہے، بس صفائی اور صفائی، تو باریاں کسی چیز پر اثر نہیں ڈالیں گی۔

باریوں (concurrency) کے ساتھ یا بغیر مکمل ہونے میں اتنا ہی وقت لگے گا اور آپ نے اتنا ہی کام کیا ہوگا۔

لیکن اس صورت میں، اگر آپ 8 سابقہ cashier/باورچی/اب صفائی والے لا سکتے، اور ہر ایک (آپ سمیت) گھر کا ایک حصہ صاف کر سکتا، تو آپ سارا کام **parallel** میں، اضافی مدد سے، بہت جلد مکمل کر سکتے تھے۔

اس منظرنامے میں، ہر صفائی کرنے والا (آپ سمیت) ایک processor ہوگا، جو اپنے حصے کا کام کر رہا ہوگا۔

اور چونکہ زیادہ تر execution time حقیقی کام میں صرف ہوتا ہے (انتظار کی بجائے)، اور computer میں کام ایک <abbr title="Central Processing Unit">CPU</abbr> کے ذریعے ہوتا ہے، وہ ان مسائل کو "CPU bound" کہتے ہیں۔

---

CPU bound operations کی عام مثالیں وہ چیزیں ہیں جنہیں پیچیدہ ریاضیاتی processing کی ضرورت ہوتی ہے۔

مثال کے طور پر:

* **Audio** یا **image processing**۔
* **Computer vision**: ایک تصویر لاکھوں pixels پر مشتمل ہوتی ہے، ہر pixel میں 3 values / رنگ ہوتے ہیں، ان کی processing میں عام طور پر ان pixels پر بیک وقت کوئی حساب لگانا ہوتا ہے۔
* **Machine Learning**: عام طور پر بہت سی "matrix" اور "vector" multiplications کی ضرورت ہوتی ہے۔ نمبروں سے بھری ایک بڑی spreadsheet کا تصور کریں اور ان سب کو بیک وقت ضرب دینا۔
* **Deep Learning**: یہ Machine Learning کا ایک ذیلی شعبہ ہے، تو وہی اصول لاگو ہوتے ہیں۔ بس اتنا ہے کہ ضرب دینے کے لیے نمبروں کی ایک ہی spreadsheet نہیں بلکہ ایک بہت بڑا مجموعہ ہوتا ہے، اور بہت سے معاملات میں آپ ان models کو بنانے اور/یا استعمال کرنے کے لیے ایک خاص processor استعمال کرتے ہیں۔

### Concurrency + Parallelism: Web + Machine Learning { #concurrency-parallelism-web-machine-learning }

**FastAPI** کے ساتھ آپ concurrency کا فائدہ اٹھا سکتے ہیں جو web development کے لیے بہت عام ہے (NodeJS کی وہی بنیادی کشش)۔

لیکن آپ parallelism اور multiprocessing (متعدد processes بیک وقت چلنا) کے فوائد کو بھی **CPU bound** workloads کے لیے استعمال کر سکتے ہیں جیسے Machine Learning systems۔

یہ، اور اس سادہ حقیقت کے ساتھ کہ Python **Data Science**، Machine Learning اور خاص طور پر Deep Learning کی بنیادی زبان ہے، FastAPI کو Data Science / Machine Learning web APIs اور applications کے لیے ایک بہت اچھا انتخاب بناتے ہیں (بہت سی دوسری چیزوں کے علاوہ)۔

production میں یہ parallelism کیسے حاصل کریں یہ جاننے کے لیے [Deployment](deployment/index.md) کا سیکشن دیکھیں۔

## `async` اور `await` { #async-and-await }

Python کے جدید ورژنز میں asynchronous code define کرنے کا ایک بہت بدیہی طریقہ ہے۔ یہ اسے عام "sequential" code جیسا بناتا ہے اور صحیح لمحات پر آپ کے لیے "awaiting" کرتا ہے۔

جب کوئی operation ہو جو نتائج دینے سے پہلے انتظار کی ضرورت رکھتا ہو اور Python کی ان نئی features کی سہولت رکھتا ہو، آپ اسے اس طرح code کر سکتے ہیں:

```Python
burgers = await get_burgers(2)
```

یہاں کلید `await` ہے۔ یہ Python کو بتاتا ہے کہ اسے `get_burgers(2)` کا اپنا کام 🕙 مکمل کرنے تک انتظار ⏸ کرنا ہے `burgers` میں نتائج محفوظ کرنے سے پہلے۔ اس کے ساتھ، Python جان لے گا کہ وہ اس دوران 🔀 ⏯ کچھ اور کام کر سکتا ہے (جیسے کوئی اور request وصول کرنا)۔

`await` کام کرنے کے لیے، اسے ایک ایسے function کے اندر ہونا ضروری ہے جو اس asynchronicity کی سہولت رکھتا ہو۔ ایسا کرنے کے لیے، بس اسے `async def` کے ساتھ declare کریں:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

...`def` کی بجائے:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

`async def` کے ساتھ، Python جانتا ہے کہ اس function کے اندر اسے `await` expressions کا خیال رکھنا ہے، اور یہ کہ وہ اس function کی execution کو "روک" ⏸ کر واپس آنے سے پہلے 🔀 کچھ اور کام کر سکتا ہے۔

جب آپ کسی `async def` function کو call کرنا چاہیں، تو آپ کو اسے "await" کرنا ہوگا۔ تو یہ کام نہیں کرے گا:

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

---

تو اگر آپ کوئی library استعمال کر رہے ہیں جو آپ سے `await` کے ساتھ call کرنے کو کہتی ہے، تو آپ کو اسے استعمال کرنے والے *path operation functions* کو `async def` کے ساتھ بنانا ہوگا، جیسے:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### مزید تکنیکی تفصیلات { #more-technical-details }

آپ نے غور کیا ہوگا کہ `await` صرف `async def` سے define کیے گئے functions کے اندر استعمال ہو سکتا ہے۔

لیکن ساتھ ہی، `async def` سے define کیے گئے functions کو "await" کرنا ضروری ہے۔ تو `async def` والے functions صرف `async def` سے define کیے گئے functions کے اندر ہی call ہو سکتے ہیں۔

تو انڈے اور مرغی کے بارے میں، آپ پہلا `async` function کیسے call کریں؟

اگر آپ **FastAPI** کے ساتھ کام کر رہے ہیں تو آپ کو اس کی فکر نہیں کرنی، کیونکہ وہ "پہلا" function آپ کا *path operation function* ہوگا، اور FastAPI جانے گا کہ صحیح کام کیسے کرنا ہے۔

لیکن اگر آپ FastAPI کے بغیر `async` / `await` استعمال کرنا چاہیں، تو آپ ایسا بھی کر سکتے ہیں۔

### اپنا async code لکھیں { #write-your-own-async-code }

Starlette (اور **FastAPI**) [AnyIO](https://anyio.readthedocs.io/en/stable/) پر مبنی ہیں، جو اسے Python کی standard library [asyncio](https://docs.python.org/3/library/asyncio-task.html) اور [Trio](https://trio.readthedocs.io/en/stable/) دونوں کے ساتھ compatible بناتا ہے۔

خاص طور پر، آپ اپنے advanced concurrency use cases کے لیے براہ راست [AnyIO](https://anyio.readthedocs.io/en/stable/) استعمال کر سکتے ہیں جنہیں آپ کے اپنے code میں مزید advanced patterns کی ضرورت ہو۔

اور اگر آپ FastAPI استعمال نہیں بھی کر رہے ہوتے، تو بھی آپ [AnyIO](https://anyio.readthedocs.io/en/stable/) کے ساتھ اپنی async applications لکھ سکتے تھے جو بہت compatible ہوں اور اس کے فوائد حاصل کریں (مثلاً *structured concurrency*)۔

میں نے AnyIO کے اوپر ایک اور library بنائی ہے، ایک پتلی layer کے طور پر، type annotations کو تھوڑا بہتر بنانے اور بہتر **autocompletion**، **inline errors** وغیرہ حاصل کرنے کے لیے۔ اس میں ایک دوستانہ تعارف اور tutorial بھی ہے جو آپ کو **سمجھنے** اور **اپنا async code** لکھنے میں مدد کرے: [Asyncer](https://asyncer.tiangolo.com/)۔ یہ خاص طور پر مفید ہوگا اگر آپ کو **async code کو regular** (blocking/synchronous) code کے ساتھ ملانے کی ضرورت ہو۔

### Asynchronous code کی دوسری شکلیں { #other-forms-of-asynchronous-code }

`async` اور `await` استعمال کرنے کا یہ انداز زبان میں نسبتاً نیا ہے۔

لیکن یہ asynchronous code کے ساتھ کام کرنا بہت آسان بناتا ہے۔

یہی syntax (یا تقریباً ایک جیسا) حال ہی میں JavaScript کے جدید ورژنز (Browser اور NodeJS میں) میں بھی شامل کیا گیا۔

لیکن اس سے پہلے، asynchronous code کو سنبھالنا کافی زیادہ پیچیدہ اور مشکل تھا۔

Python کے پچھلے ورژنز میں، آپ threads یا [Gevent](https://www.gevent.org/) استعمال کر سکتے تھے۔ لیکن code سمجھنے، debug کرنے، اور سوچنے میں بہت زیادہ پیچیدہ ہوتا ہے۔

NodeJS / Browser JavaScript کے پچھلے ورژنز میں، آپ "callbacks" استعمال کرتے۔ جو "callback hell" کی طرف لے جاتا ہے۔

## Coroutines { #coroutines }

**Coroutine** بس اس چیز کے لیے ایک بہت فینسی اصطلاح ہے جو `async def` function واپس کرتا ہے۔ Python جانتا ہے کہ یہ ایک function جیسی چیز ہے، جو شروع ہو سکتی ہے اور کسی وقت ختم ہوگی، لیکن یہ اندرونی طور پر بھی ⏸ روکی جا سکتی ہے، جب بھی اس کے اندر `await` ہو۔

لیکن `async` اور `await` کے ساتھ asynchronous code استعمال کرنے کی یہ ساری functionality اکثر "coroutines" استعمال کرنا کہہ کر خلاصہ کی جاتی ہے۔ یہ Go کی بنیادی خصوصیت "Goroutines" سے قابل موازنہ ہے۔

## نتیجہ { #conclusion }

آئیے اوپر والا وہی جملہ دوبارہ دیکھتے ہیں:

> Python کے جدید ورژنز **"asynchronous code"** کی سہولت فراہم کرتے ہیں جسے **"coroutines"** کہتے ہیں، **`async` اور `await`** syntax کے ساتھ۔

اب یہ زیادہ سمجھ آنا چاہیے۔ ✨

یہی سب **FastAPI** کو (Starlette کے ذریعے) طاقت دیتا ہے اور اسے اتنی شاندار performance دیتا ہے۔

## انتہائی تکنیکی تفصیلات { #very-technical-details }

/// warning | انتباہ

آپ شاید اسے چھوڑ سکتے ہیں۔

یہ بہت تکنیکی تفصیلات ہیں کہ **FastAPI** اندرونی طور پر کیسے کام کرتا ہے۔

اگر آپ کے پاس کافی تکنیکی علم ہے (coroutines، threads، blocking وغیرہ) اور آپ جاننا چاہتے ہیں کہ FastAPI `async def` بمقابلہ عام `def` کو کیسے سنبھالتا ہے، تو آگے بڑھیں۔

///

### Path operation functions { #path-operation-functions }

جب آپ *path operation function* کو `async def` کی بجائے عام `def` کے ساتھ declare کرتے ہیں، تو اسے ایک بیرونی threadpool میں چلایا جاتا ہے جس کا پھر await کیا جاتا ہے، براہ راست call کرنے کی بجائے (کیونکہ یہ server کو block کر دے گا)۔

اگر آپ کسی اور async framework سے آ رہے ہیں جو اوپر بیان کردہ طریقے سے کام نہیں کرتا اور آپ عام `def` کے ساتھ معمولی compute-only *path operation functions* define کرنے کے عادی ہیں تھوڑی سی performance بہتری (تقریباً 100 nanoseconds) کے لیے، تو براہ کرم نوٹ کریں کہ **FastAPI** میں اثر بالکل الٹا ہوگا۔ ان صورتوں میں، `async def` استعمال کرنا بہتر ہے جب تک کہ آپ کے *path operation functions* ایسا code استعمال نہ کریں جو blocking <abbr title="Input/Output: disk reading or writing, network communications.">I/O</abbr> کرتا ہو۔

پھر بھی، دونوں صورتوں میں، امکان ہے کہ **FastAPI** آپ کے پچھلے framework سے [پھر بھی تیز](index.md#performance) ہوگا (یا کم از کم اس کے برابر)۔

### Dependencies { #dependencies }

یہی [dependencies](tutorial/dependencies/index.md) پر بھی لاگو ہوتا ہے۔ اگر dependency ایک عام `def` function ہے `async def` کی بجائے، تو اسے بیرونی threadpool میں چلایا جاتا ہے۔

### Sub-dependencies { #sub-dependencies }

آپ کے متعدد dependencies اور [sub-dependencies](tutorial/dependencies/sub-dependencies.md) ہو سکتے ہیں جو ایک دوسرے کی ضرورت رکھتے ہوں (function definitions کے parameters کے طور پر)، ان میں سے کچھ `async def` سے بنائے جا سکتے ہیں اور کچھ عام `def` سے۔ یہ پھر بھی کام کرے گا، اور عام `def` سے بنائے گئے ایک بیرونی thread (threadpool سے) پر call کیے جائیں گے "await" کیے جانے کی بجائے۔

### دوسرے utility functions { #other-utility-functions }

کوئی بھی دوسرا utility function جسے آپ براہ راست call کرتے ہیں، عام `def` یا `async def` سے بنایا جا سکتا ہے اور FastAPI اس پر اثر نہیں ڈالے گا جس طرح آپ اسے call کرتے ہیں۔

یہ ان functions کے برعکس ہے جو FastAPI آپ کے لیے call کرتا ہے: *path operation functions* اور dependencies۔

اگر آپ کا utility function ایک عام `def` والا function ہے، تو اسے براہ راست call کیا جائے گا (جیسا کہ آپ اسے اپنے code میں لکھتے ہیں)، threadpool میں نہیں، اگر function `async def` سے بنایا گیا ہے تو آپ کو اس function کو اپنے code میں call کرتے وقت `await` کرنا چاہیے۔

---

دوبارہ، یہ بہت تکنیکی تفصیلات ہیں جو شاید مفید ہوں اگر آپ انہیں تلاش کرتے ہوئے آئے ہیں۔

ورنہ، آپ اوپر والے سیکشن کی ہدایات سے ٹھیک ہونے چاہئیں: <a href="#in-a-hurry">جلدی میں ہیں؟</a>
