# ترقی - تعاون

پہلے، آپ [FastAPI کی مدد کریں اور مدد حاصل کریں](help-fastapi.md) کے بنیادی طریقے دیکھنا چاہیں گے۔

## ترقی

اگر آپ نے پہلے ہی [fastapi repository](https://github.com/fastapi/fastapi) clone کر لیا ہے اور code میں گہرائی سے جانا چاہتے ہیں، تو یہاں آپ کا ماحول ترتیب دینے کی کچھ ہدایات ہیں۔

### ضروریات install کریں

Virtual environment بنائیں اور [`uv`](https://github.com/astral-sh/uv) کے ساتھ درکار packages install کریں:

<div class="termy">

```console
$ uv sync --extra all

---> 100%
```

</div>

یہ تمام dependencies اور آپ کا مقامی FastAPI آپ کے مقامی ماحول میں install کر دے گا۔

### اپنا مقامی FastAPI استعمال کریں

اگر آپ ایک Python فائل بناتے ہیں جو FastAPI import اور استعمال کرتی ہے، اور اسے اپنے مقامی ماحول کے Python سے چلاتے ہیں، تو یہ آپ کا clone شدہ مقامی FastAPI source code استعمال کرے گا۔

اور اگر آپ اس مقامی FastAPI source code کو اپڈیٹ کرتے ہیں تو جب آپ وہ Python فائل دوبارہ چلائیں گے، یہ FastAPI کا وہ تازہ ورژن استعمال کرے گا جو آپ نے ابھی ترمیم کیا ہے۔

اس طرح، ہر تبدیلی ٹیسٹ کرنے کے لیے آپ کو اپنا مقامی ورژن "install" نہیں کرنا پڑتا۔

/// note | تکنیکی تفصیلات

یہ صرف تب ہوتا ہے جب آپ `pip install fastapi` براہ راست چلانے کی بجائے `uv sync --extra all` استعمال کرکے install کرتے ہیں۔

اس کی وجہ یہ ہے کہ `uv sync --extra all` بطور default FastAPI کا مقامی ورژن "editable" mode میں install کرتا ہے۔

///

### Code فارمیٹ کریں

ایک script ہے جسے آپ چلا سکتے ہیں جو آپ کا سارا code فارمیٹ اور صاف کر دے گی:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

یہ آپ کے تمام imports کو بھی خودکار طریقے سے ترتیب دے گی۔

## Tests

ایک script ہے جسے آپ مقامی طور پر تمام code ٹیسٹ کرنے اور HTML میں coverage reports بنانے کے لیے چلا سکتے ہیں:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

یہ command `./htmlcov/` directory بناتی ہے، اگر آپ `./htmlcov/index.html` فائل اپنے browser میں کھولیں، تو آپ انٹرایکٹو طریقے سے دیکھ سکتے ہیں کہ code کے کون سے حصے tests سے cover ہیں، اور کوئی حصہ رہ تو نہیں گیا۔

## Docs

پہلے، یقینی بنائیں کہ آپ نے اوپر بیان کردہ طریقے سے اپنا ماحول ترتیب دیا ہے، جو تمام ضروریات install کر دے گا۔

### Docs لائیو

مقامی ترقی کے دوران، ایک script ہے جو سائٹ بناتی ہے اور کسی بھی تبدیلی کو چیک کرتی ہے، لائیو ری لوڈنگ کے ساتھ:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

یہ documentation کو `http://127.0.0.1:8008` پر serve کرے گا۔

اس طرح، آپ documentation/source فائلوں میں ترمیم کر سکتے ہیں اور تبدیلیاں لائیو دیکھ سکتے ہیں۔

/// tip | مشورہ

متبادل طور پر، آپ وہی اقدامات خود دستی طور پر کر سکتے ہیں جو script کرتی ہے۔

زبان کی directory میں جائیں، بنیادی docs کے لیے انگریزی میں یہ `docs/en/` پر ہے:

```console
$ cd docs/en/
```

پھر اس directory میں `mkdocs` چلائیں:

```console
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

///

#### Typer CLI (اختیاری)

یہاں ہدایات آپ کو دکھاتی ہیں کہ `./scripts/docs.py` script کو `python` program کے ساتھ براہ راست کیسے استعمال کریں۔

لیکن آپ [Typer CLI](https://typer.tiangolo.com/typer-cli/) بھی استعمال کر سکتے ہیں، اور completion install کرنے کے بعد آپ کو اپنے terminal میں commands کے لیے autocompletion ملے گی۔

اگر آپ Typer CLI install کرتے ہیں، تو آپ اس کے ساتھ completion install کر سکتے ہیں:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Docs کی ساخت

Documentation [MkDocs](https://www.mkdocs.org/) استعمال کرتی ہے۔

اور `./scripts/docs.py` میں تراجم کو سنبھالنے کے لیے اضافی tools/scripts موجود ہیں۔

/// tip | مشورہ

آپ کو `./scripts/docs.py` کا code دیکھنے کی ضرورت نہیں، آپ بس اسے command line میں استعمال کرتے ہیں۔

///

تمام documentation `./docs/en/` directory میں Markdown فارمیٹ میں ہے۔

بہت سے tutorials میں code blocks ہوتے ہیں۔

زیادہ تر معاملات میں، یہ code blocks مکمل applications ہیں جو جیسے ہیں ویسے چلائی جا سکتی ہیں۔

درحقیقت، وہ code blocks Markdown کے اندر نہیں لکھے جاتے، بلکہ `./docs_src/` directory میں Python فائلیں ہیں۔

اور وہ Python فائلیں سائٹ generate کرتے وقت documentation میں شامل/inject کی جاتی ہیں۔

### Tests کے لیے Docs

زیادہ تر tests دراصل documentation میں موجود مثالی source فائلوں کے خلاف چلتے ہیں۔

اس سے یہ یقینی بنانے میں مدد ملتی ہے کہ:

* Documentation تازہ ترین ہے۔
* Documentation کی مثالیں جیسی ہیں ویسی چلائی جا سکتی ہیں۔
* زیادہ تر features documentation سے cover ہیں، test coverage سے یقینی بنائی گئی ہیں۔

#### Apps اور docs بیک وقت

اگر آپ مثالیں چلاتے ہیں، جیسے:

<div class="termy">

```console
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

چونکہ Uvicorn بطور default port `8000` استعمال کرتا ہے، port `8008` پر documentation اس سے نہیں ٹکرائے گی۔

### تراجم

تراجم میں مدد بہت زیادہ قدر کی جاتی ہے! اور یہ کمیونٹی کی مدد کے بغیر نہیں ہو سکتا۔ 🌎 🚀

ترجمے کی pull requests FastAPI ٹیم کی طرف سے ڈیزائن کردہ prompts سے رہنمائی حاصل کرنے والے LLMs اور ہر supported زبان کے لیے مقامی بولنے والوں کی کمیونٹی کے ساتھ مل کر بنائی جاتی ہیں۔

#### فی زبان LLM Prompt

ہر زبان کی ایک directory ہے: [https://github.com/fastapi/fastapi/tree/master/docs](https://github.com/fastapi/fastapi/tree/master/docs)، اس میں آپ `llm-prompt.md` فائل دیکھ سکتے ہیں جس میں اس زبان کے لیے مخصوص prompt ہے۔

مثال کے طور پر، ہسپانوی کے لیے prompt یہاں ہے: [`docs/es/llm-prompt.md`](https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md)۔

اگر آپ کو اپنی زبان میں غلطیاں نظر آئیں، تو آپ اپنی زبان کی فائل میں prompt کے لیے تجاویز دے سکتے ہیں، اور تبدیلیوں کے بعد ان مخصوص pages کی دوبارہ تخلیق کی درخواست کر سکتے ہیں۔

#### ترجمے کی PRs کا Review

آپ اپنی زبان کے لیے موجودہ [pull requests](https://github.com/fastapi/fastapi/pulls) بھی چیک کر سکتے ہیں۔ آپ اپنی زبان کے label کے ساتھ pull requests فلٹر کر سکتے ہیں۔ مثال کے طور پر، ہسپانوی کے لیے label [`lang-es`](https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review) ہے۔

Pull request کا review کرتے وقت، بہتر ہے کہ اسی pull request میں تبدیلیاں تجویز نہ کریں، کیونکہ یہ LLM سے generate کیا گیا ہے، اور یہ یقینی بنانا ممکن نہیں ہوگا کہ چھوٹی انفرادی تبدیلیاں دوسرے ملتے جلتے حصوں میں نقل ہوں، یا وہی مواد دوبارہ ترجمہ کرتے وقت محفوظ رہیں۔

ترجمے کی PR میں تجاویز شامل کرنے کی بجائے، اس زبان کی LLM prompt فائل میں تجاویز دیں، ایک نئی PR میں۔ مثال کے طور پر، ہسپانوی کی LLM prompt فائل یہاں ہے: [`docs/es/llm-prompt.md`](https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md)۔

/// tip | مشورہ

[Pull request review شامل کرنے](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews) کے بارے میں docs چیک کریں تاکہ اسے منظور یا تبدیلیوں کی درخواست کر سکیں۔

///

#### اپنی زبان کے لیے Notifications سبسکرائب کریں

چیک کریں کہ آیا آپ کی زبان کے تراجم کی coordination کے لیے [GitHub Discussion](https://github.com/fastapi/fastapi/discussions/categories/translations) ہے۔ آپ اسے سبسکرائب کر سکتے ہیں، اور جب review کے لیے نئی pull request ہوگی، discussion میں خودکار تبصرہ شامل کیا جائے گا۔

آپ جس زبان کا ترجمہ کرنا چاہتے ہیں اس کا 2 حرفی code جاننے کے لیے [List of ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) کا جدول استعمال کر سکتے ہیں۔

#### نئی زبان کی درخواست

فرض کریں کہ آپ ایسی زبان کے تراجم کی درخواست کرنا چاہتے ہیں جس کا ابھی تک ترجمہ نہیں ہوا، کوئی page بھی نہیں۔ مثال کے طور پر، لاطینی۔

* پہلا قدم یہ ہوگا کہ آپ 2 اور لوگ تلاش کریں جو آپ کے ساتھ اس زبان کے لیے ترجمے کی PRs کا review کرنے کو تیار ہوں۔
* جب کم از کم 3 لوگ اس زبان کی دیکھ بھال میں مدد کا عہد کرنے کو تیار ہوں، تو آپ اگلے اقدامات جاری رکھ سکتے ہیں۔
* Template کے مطابق نئی discussion بنائیں۔
* اپنے ساتھ مدد کرنے والے 2 دوسرے لوگوں کو tag کریں، اور ان سے وہاں تصدیق کرنے کو کہیں کہ وہ مدد کریں گے۔

جب discussion میں کئی لوگ ہوں، FastAPI ٹیم اس کا جائزہ لے سکتی ہے اور اسے سرکاری ترجمہ بنا سکتی ہے۔

پھر docs خودکار طور پر LLMs کے ذریعے ترجمہ ہوں گے، اور مقامی بولنے والوں کی ٹیم ترجمے کا review کر سکتی ہے، اور LLM prompts کو بہتر بنانے میں مدد کر سکتی ہے۔

جب نیا ترجمہ ہوگا، مثال کے طور پر اگر docs اپڈیٹ ہوں یا نیا سیکشن ہو، تو اسی discussion میں review کے لیے نئے ترجمے کے link کے ساتھ تبصرہ آئے گا۔

## خودکار Code اور AI

آپ کو ہر وہ tool استعمال کرنے کی ترغیب دی جاتی ہے جو آپ چاہیں تاکہ اپنا کام کریں اور جتنا ہو سکے مؤثر طریقے سے تعاون کریں، بشمول AI (LLM) tools وغیرہ۔ تاہم، تعاون میں بامعنی انسانی مداخلت، فیصلے، سیاق و سباق وغیرہ ہونا چاہیے۔

اگر PR میں لگائی گئی **انسانی محنت**، جیسے LLM prompts لکھنا، اس **محنت سے کم** ہے جو ہمیں اسے **review** کرنے میں لگانی ہوگی، تو براہ کرم PR **جمع نہ کریں**۔

اس طرح سوچیں: ہم خود LLM prompts لکھ سکتے ہیں یا خودکار tools چلا سکتے ہیں، اور یہ بیرونی PRs کا review کرنے سے تیز ہوگا۔

### خودکار اور AI PRs بند کرنا

اگر ہمیں ایسی PRs نظر آئیں جو AI سے generate کی گئی یا اسی طرح خودکار لگتی ہیں، تو ہم انہیں flag کرکے بند کر دیں گے۔

یہی تبصروں اور تفصیلات پر بھی لاگو ہوتا ہے، براہ کرم LLM سے generate کیا گیا مواد copy paste نہ کریں۔

### انسانی محنت پر Denial of Service

خودکار tools اور AI کا استعمال کرکے ایسی PRs یا تبصرے جمع کرنا جنہیں ہمیں احتیاط سے review اور سنبھالنا ہو، ہماری انسانی محنت پر [Denial-of-service attack](https://en.wikipedia.org/wiki/Denial-of-service_attack) کے مترادف ہوگا۔

PR جمع کرنے والے شخص کی طرف سے بہت کم محنت (ایک LLM prompt) ہماری طرف سے بڑی مقدار میں محنت (احتیاط سے code کا review) پیدا کرتی ہے۔

براہ کرم ایسا نہ کریں۔

ہمیں بار بار خودکار PRs یا تبصروں سے spam کرنے والے اکاؤنٹس کو block کرنا ہوگا۔

### Tools سمجھداری سے استعمال کریں

جیسا کہ Uncle Ben نے کہا:

<blockquote>
بڑی <strike>طاقت</strike> <strong>tools</strong> کے ساتھ بڑی ذمہ داری آتی ہے۔
</blockquote>

نادانستہ طور پر نقصان پہنچانے سے بچیں۔

آپ کے پاس حیرت انگیز tools ہیں، انہیں سمجھداری سے مؤثر طریقے سے مدد کرنے کے لیے استعمال کریں۔
