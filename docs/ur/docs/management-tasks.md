# Repository Management Tasks

یہ وہ کام ہیں جو FastAPI repository کو manage کرنے کے لیے [ٹیم ممبران](./fastapi-people.md#team) انجام دے سکتے ہیں۔

/// tip | مشورہ

یہ سیکشن صرف مٹھی بھر لوگوں کے لیے مفید ہے، وہ ٹیم ممبران جن کے پاس repository manage کرنے کی اجازتیں ہیں۔ آپ شاید اسے چھوڑ سکتے ہیں۔ 😉

///

...تو آپ [FastAPI کی ٹیم کے ممبر](./fastapi-people.md#team) ہیں؟ واہ، آپ بہت زبردست ہیں! 😎

آپ [FastAPI کی مدد کریں - مدد حاصل کریں](./help-fastapi.md) میں سب کچھ بیرونی شراکت داروں کی طرح مدد کر سکتے ہیں۔ لیکن اس کے علاوہ، کچھ کام ایسے ہیں جو صرف آپ (ٹیم کے حصے کے طور پر) انجام دے سکتے ہیں۔

یہاں ان کاموں کی عمومی ہدایات ہیں جو آپ انجام دے سکتے ہیں۔

آپ کی مدد کے لیے بہت شکریہ۔ 🙇

## مہربان رہیں

سب سے پہلے، مہربان رہیں۔ 😊

اگر آپ ٹیم میں شامل کیے گئے تو شاید آپ بہت مہربان ہیں، لیکن یہ ذکر کرنا ضروری ہے۔ 🤓

### جب چیزیں مشکل ہوں

جب چیزیں اچھی ہوں تو سب کچھ آسان ہوتا ہے، تو اس کے لیے زیادہ ہدایات کی ضرورت نہیں۔ لیکن جب چیزیں مشکل ہوں، یہاں کچھ رہنمائی ہے۔

اچھی بات تلاش کرنے کی کوشش کریں۔ عام طور پر، اگر لوگ غیر دوستانہ نہیں ہو رہے، تو ان کی محنت اور دلچسپی کا شکریہ ادا کرنے کی کوشش کریں، چاہے آپ بنیادی موضوع (بحث، PR) سے متفق نہ ہوں، بس project میں دلچسپی لینے، یا کچھ کرنے کی کوشش میں وقت لگانے کا شکریہ ادا کریں۔

متن میں جذبات ظاہر کرنا مشکل ہوتا ہے، مدد کے لیے emojis استعمال کریں۔ 😅

Discussions اور PRs میں، بہت سے معاملات میں لوگ اپنی پریشانی لاتے ہیں اور بغیر فلٹر کے دکھاتے ہیں، بہت سے معاملات میں مبالغہ آرائی، شکایت، حق جتانا وغیرہ۔ یہ واقعی اچھا نہیں ہے، اور جب ایسا ہوتا ہے تو ان کے مسائل حل کرنے کی ہماری ترجیح کم ہو جاتی ہے۔ لیکن پھر بھی، سانس لینے کی کوشش کریں، اور اپنے جوابات میں نرم رہیں۔

تلخ طنز یا ممکنہ طور پر passive-aggressive تبصروں سے بچنے کی کوشش کریں۔ اگر کچھ غلط ہے، تو طنزیہ ہونے سے بہتر ہے کہ براہ راست (نرمی سے) بات کریں۔

جتنا ہو سکے مخصوص اور معروضی ہونے کی کوشش کریں، عمومی باتوں سے بچیں۔

ان گفتگو کے لیے جو زیادہ مشکل ہوں، مثلاً PR مسترد کرنا، آپ مجھ سے (@tiangolo) براہ راست سنبھالنے کو کہہ سکتے ہیں۔

## PR Titles ترمیم کریں

* PR title ترمیم کریں تاکہ یہ [gitmoji](https://gitmoji.dev/) سے emoji کے ساتھ شروع ہو۔
    * Emoji character استعمال کریں، GitHub code نہیں۔ تو `🐛` استعمال کریں `:bug:` کی بجائے۔ تاکہ GitHub سے باہر بھی صحیح دکھائی دے، مثلاً release notes میں۔
    * تراجم کے لیے `🌐` emoji ("globe with meridians") استعمال کریں۔
* Title فعل سے شروع کریں۔ مثلاً `Add`، `Refactor`، `Fix` وغیرہ۔ اس طرح title بتائے گا کہ PR کیا کرتا ہے۔ جیسے `Add support for teleporting`، بجائے `Teleporting wasn't working, so this PR fixes it`۔
* PR title کا متن "امری" انداز میں ترمیم کریں، جیسے حکم دے رہے ہوں۔ تو `Adding support for teleporting` کی بجائے `Add support for teleporting` استعمال کریں۔
* Title وضاحتی ہو کہ یہ کیا حاصل کرتا ہے۔ اگر feature ہے تو اسے بیان کرنے کی کوشش کریں، مثلاً `Add support for teleporting` بجائے `Create TeleportAdapter class`۔
* Title نقطے (`.`) سے ختم نہ کریں۔
* جب PR ترجمے کے لیے ہو، `🌐` سے شروع کریں اور پھر `Add {language} translation for` اور پھر ترجمہ شدہ فائل کا path۔ مثال کے طور پر:

```Markdown
🌐 Add Spanish translation for `docs/es/docs/teleporting.md`
```

PR merge ہونے کے بعد، ایک GitHub Action ([latest-changes](https://github.com/tiangolo/latest-changes)) خودکار طور پر تازہ ترین تبدیلیاں اپڈیٹ کرنے کے لیے PR title استعمال کرے گی۔

تو اچھا PR title ہونا نہ صرف GitHub میں اچھا دکھائے گا، بلکہ release notes میں بھی۔ 📝

## PRs میں Labels شامل کریں

وہی GitHub Action [latest-changes](https://github.com/tiangolo/latest-changes) release notes میں اس PR کو کس سیکشن میں رکھنا ہے یہ فیصلہ کرنے کے لیے PR میں ایک label استعمال کرتی ہے۔

یقینی بنائیں کہ آپ [latest-changes labels کی فہرست](https://github.com/tiangolo/latest-changes#using-labels) سے supported label استعمال کریں:

* `breaking`: Breaking Changes
    * موجودہ code ٹوٹ جائے گا اگر وہ اپنا code تبدیل کیے بغیر ورژن اپڈیٹ کریں۔ یہ شاذ و نادر ہوتا ہے، تو یہ label کم استعمال ہوتا ہے۔
* `security`: Security Fixes
    * یہ security fixes کے لیے ہے، جیسے vulnerabilities۔ یہ تقریباً کبھی استعمال نہیں ہوگا۔
* `feature`: Features
    * نئی features، ایسی چیزوں کی سہولت شامل کرنا جو پہلے موجود نہیں تھیں۔
* `bug`: Fixes
    * کوئی چیز جو supported تھی وہ کام نہیں کر رہی تھی، اور یہ اسے ٹھیک کرتا ہے۔
* `refactor`: Refactors
    * یہ عام طور پر اندرونی code میں تبدیلیوں کے لیے ہے جو رویے کو نہیں بدلتیں۔
* `upgrade`: Upgrades
    * یہ project سے براہ راست dependencies کے upgrades کے لیے ہے۔
* `docs`: Docs
    * Docs میں تبدیلیاں۔ اس میں تراجم کی تبدیلیاں شامل نہیں ہیں۔
* `lang-all`: Translations
    * تراجم کے لیے استعمال کریں۔
* `internal`: Internal
    * ایسی تبدیلیوں کے لیے استعمال کریں جو صرف repo management کو متاثر کرتی ہیں۔

/// tip | مشورہ

Dependabot جیسے tools کچھ labels شامل کریں گے، جیسے `dependencies`، لیکن یاد رکھیں کہ یہ label `latest-changes` GitHub Action استعمال نہیں کرتی، تو release notes میں استعمال نہیں ہوگا۔ براہ کرم یقینی بنائیں کہ اوپر والے labels میں سے ایک شامل ہو۔

///

## ترجمے کی PRs میں Labels شامل کریں

جب ترجمے کی PR ہو، `lang-all` label کے علاوہ، زبان کے لیے بھی label شامل کریں۔

ہر زبان کے لیے زبان code کا استعمال کرتے ہوئے ایک label ہوگا، جیسے `lang-{lang code}`، مثلاً ہسپانوی کے لیے `lang-es`، فرانسیسی کے لیے `lang-fr` وغیرہ۔

* مخصوص زبان کا label شامل کریں۔
* `awaiting-review` label شامل کریں۔

`awaiting-review` label خاص ہے، صرف تراجم کے لیے۔ ایک GitHub Action اسے detect کرے گا، پھر زبان کا label پڑھے گا، اور اس زبان کے تراجم manage کرنے والی GitHub Discussions کو اپڈیٹ کرے گا تاکہ لوگوں کو بتایا جائے کہ review کے لیے نیا ترجمہ ہے۔

جب کوئی مقامی بولنے والا آئے، PR کا review کرے، اور اسے منظور کرے، GitHub Action آ کر `awaiting-review` label ہٹائے گا، اور `approved-1` label شامل کرے گا۔

اس طرح، ہم نوٹ کر سکتے ہیں جب نئے تراجم تیار ہوں، کیونکہ ان کے پاس `approved-1` label ہوتا ہے۔

## ترجمے کی PRs Merge کریں

تراجم LLMs اور scripts سے خودکار طور پر generate کیے جاتے ہیں۔

ایک GitHub Action ہے جو کسی زبان کے تراجم شامل یا اپڈیٹ کرنے کے لیے دستی طور پر چلایا جا سکتا ہے: [`translate.yml`](https://github.com/fastapi/fastapi/actions/workflows/translate.yml)۔

ان زبان کے ترجمے کی PRs کے لیے، تصدیق کریں کہ:

* PR خودکار تھا (@tiangolo کی طرف سے)، کسی اور صارف نے نہیں بنایا۔
* اس میں `lang-all` اور `lang-{lang code}` labels ہیں۔
* اگر PR کم از کم ایک مقامی بولنے والے نے منظور کیا ہو، آپ اسے merge کر سکتے ہیں۔

## PRs کا Review کریں

* اگر PR نہیں بتاتی کہ یہ کیا کرتی ہے یا کیوں، اگر ایسا لگے کہ مفید ہو سکتی ہے، مزید معلومات مانگیں۔ ورنہ، آزادانہ طور پر اسے بند کر دیں۔

* اگر PR spam لگے، بے معنی لگے، صرف اعداد و شمار تبدیل کرنے کے لیے ("contributor" ظاہر ہونے کے لیے) یا اسی طرح، آپ اسے `invalid` نشان زد کر سکتے ہیں، اور یہ خودکار طور پر بند ہو جائے گی۔

* اگر PR AI سے generate شدہ لگتی ہے، اور ایسا لگے کہ اس کا review کرنا prompt لکھنے سے زیادہ وقت لے گا، اسے `maybe-ai` نشان زد کریں، اور یہ خودکار طور پر بند ہو جائے گی۔

* PR کا کوئی مخصوص use case ہونا چاہیے جو یہ حل کر رہی ہو۔

* اگر PR feature کے لیے ہے تو اس میں docs ہونے چاہئیں۔
    * جب تک یہ ایسی feature نہ ہو جسے ہم حوصلہ شکنی کرنا چاہتے ہیں۔
* Docs میں source مثالی فائل شامل ہونی چاہیے، براہ راست Markdown میں Python نہیں لکھنا چاہیے۔
* اگر source مثال فائل(فائلوں) کے مختلف Python ورژنز کے لیے مختلف syntax ہو سکتے ہیں، تو فائل کے مختلف ورژنز ہونے چاہئیں، اور docs میں tabs میں دکھائے جانے چاہئیں۔
* Source مثال ٹیسٹ کرنے والے tests ہونے چاہئیں۔
* PR لاگو کرنے سے پہلے، نئے tests fail ہونے چاہئیں۔
* PR لاگو کرنے کے بعد، نئے tests pass ہونے چاہئیں۔
* Coverage 100% رہنا چاہیے۔
* اگر آپ دیکھیں کہ PR درست ہے، یا ہم نے بحث کی اور فیصلہ کیا کہ اسے قبول کیا جائے، آپ PR کے اوپر commits شامل کر سکتے ہیں اسے بہتر بنانے، docs شامل کرنے، tests، فارمیٹ کرنے، refactor کرنے، اضافی فائلیں ہٹانے وغیرہ کے لیے۔
* PR میں تبصرہ کرنے کے لیے آزاد محسوس کریں مزید معلومات مانگنے، تبدیلیاں تجویز کرنے وغیرہ کے لیے۔
* جب آپ سمجھیں کہ PR تیار ہے، اسے اندرونی GitHub project میں میرے review کے لیے منتقل کریں۔

## FastAPI People PRs

ہر مہینے، ایک GitHub Action FastAPI People data اپڈیٹ کرتی ہے۔ وہ PRs اس طرح نظر آتی ہیں: [👥 Update FastAPI People](https://github.com/fastapi/fastapi/pull/11669)۔

اگر tests pass ہو رہے ہوں، آپ اسے فوراً merge کر سکتے ہیں۔

## Dependabot PRs

Dependabot مختلف چیزوں کے لیے dependencies اپڈیٹ کرنے کی PRs بنائے گا، اور وہ PRs ملتی جلتی نظر آتی ہیں، لیکن کچھ دوسروں سے بہت زیادہ نازک ہوتی ہیں۔

* اگر PR براہ راست dependency کے لیے ہو، تو Dependabot بنیادی dependencies میں `pyproject.toml` تبدیل کر رہا ہے، **اسے merge نہ کریں**۔ 😱 مجھے پہلے چیک کرنے دیں۔
* اگر PR اندرونی dependencies میں سے کسی کو اپڈیٹ کرتی ہے، مثلاً `pyproject.toml` میں `dev` group، یا GitHub Action ورژنز، اگر tests pass ہو رہے ہیں، release notes (PR میں خلاصے میں دکھائی جاتی ہیں) میں کوئی واضح ممکنہ breaking change نظر نہیں آتی، آپ اسے merge کر سکتے ہیں۔ 😎

## GitHub Discussions جوابات نشان زد کریں

جب GitHub Discussions میں کسی سوال کا جواب دیا گیا ہو، "Mark as answer" پر کلک کرکے جواب نشان زد کریں۔

آپ discussions کو [`Questions` جو `Unanswered` ہیں](https://github.com/tiangolo/fastapi/discussions/categories/questions?discussions_q=category:Questions+is:open+is:unanswered) سے فلٹر کر سکتے ہیں۔
