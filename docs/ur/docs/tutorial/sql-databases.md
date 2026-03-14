# SQL (Relational) Databases { #sql-relational-databases }

**FastAPI** آپ سے SQL (relational) database استعمال کرنے کا تقاضا نہیں کرتا۔ لیکن آپ **کوئی بھی database** استعمال کر سکتے ہیں جو آپ چاہیں۔

یہاں ہم [SQLModel](https://sqlmodel.tiangolo.com/) استعمال کرنے کی ایک مثال دیکھیں گے۔

**SQLModel** [SQLAlchemy](https://www.sqlalchemy.org/) اور Pydantic کے اوپر بنایا گیا ہے۔ اسے **FastAPI** کے اسی مصنف نے بنایا تھا تاکہ یہ ان FastAPI applications کے لیے بہترین ہو جنہیں **SQL databases** استعمال کرنے کی ضرورت ہوتی ہے۔

/// tip | مشورہ

آپ کوئی بھی دوسری SQL یا NoSQL database library استعمال کر سکتے ہیں (بعض صورتوں میں جنہیں <abbr title="Object Relational Mapper: ایک فینسی اصطلاح ایسی library کے لیے جہاں کچھ classes SQL tables کی نمائندگی کرتی ہیں اور instances ان tables میں rows کی نمائندگی کرتے ہیں">"ORMs"</abbr> کہا جاتا ہے)، FastAPI آپ کو کسی بھی چیز کے استعمال پر مجبور نہیں کرتا۔ 😎

///

چونکہ SQLModel SQLAlchemy پر مبنی ہے، آپ آسانی سے SQLAlchemy کی طرف سے **حمایت یافتہ کوئی بھی database** استعمال کر سکتے ہیں (جو انہیں SQLModel کی طرف سے بھی حمایت یافتہ بناتا ہے)، جیسے:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server، وغیرہ

اس مثال میں، ہم **SQLite** استعمال کریں گے، کیونکہ یہ ایک واحد فائل استعمال کرتا ہے اور Python میں اس کی بلٹ ان حمایت موجود ہے۔ تو، آپ اس مثال کو کاپی کر کے جیسے ہے ویسے چلا سکتے ہیں۔

بعد میں، اپنی production application کے لیے، آپ **PostgreSQL** جیسا database server استعمال کرنا چاہ سکتے ہیں۔

/// tip | مشورہ

**FastAPI** اور **PostgreSQL** کے ساتھ ایک سرکاری project generator موجود ہے جس میں frontend اور مزید tools شامل ہیں: [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

یہ ایک بہت سادہ اور مختصر tutorial ہے، اگر آپ databases کے بارے میں عمومی طور پر، SQL کے بارے میں، یا مزید جدید خصوصیات کے بارے میں سیکھنا چاہتے ہیں، تو [SQLModel دستاویزات](https://sqlmodel.tiangolo.com/) پر جائیں۔

## `SQLModel` انسٹال کریں { #install-sqlmodel }

سب سے پہلے، یقینی بنائیں کہ آپ نے اپنا [virtual environment](../virtual-environments.md) بنایا ہے، اسے فعال کیا ہے، اور پھر `sqlmodel` انسٹال کریں:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## ایک واحد Model کے ساتھ App بنائیں { #create-the-app-with-a-single-model }

ہم پہلے ایک واحد **SQLModel** model کے ساتھ app کا سب سے آسان ورژن بنائیں گے۔

بعد میں ہم اسے **متعدد models** کے ساتھ بہتر بنائیں گے تاکہ security اور versatility بڑھے۔ 🤓

### Models بنائیں { #create-models }

`SQLModel` import کریں اور ایک database model بنائیں:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` class ایک Pydantic model سے بہت ملتی جلتی ہے (حقیقت میں، اندرونی طور پر، یہ دراصل *ایک Pydantic model ہے*)۔

کچھ فرق ہیں:

* `table=True` SQLModel کو بتاتا ہے کہ یہ ایک *table model* ہے، اسے SQL database میں ایک **table** کی نمائندگی کرنی چاہیے، یہ صرف ایک *data model* نہیں ہے (جیسا کہ کوئی بھی دوسری عام Pydantic class ہوگی)۔

* `Field(primary_key=True)` SQLModel کو بتاتا ہے کہ `id` SQL database میں **primary key** ہے (آپ SQLModel دستاویزات میں SQL primary keys کے بارے میں مزید سیکھ سکتے ہیں)۔

    **نوٹ:** ہم primary key field کے لیے `int | None` استعمال کرتے ہیں تاکہ Python code میں ہم *`id` کے بغیر ایک object بنا سکیں* (`id=None`)، یہ فرض کرتے ہوئے کہ database *اسے محفوظ کرتے وقت خود بنائے گا*۔ SQLModel سمجھتا ہے کہ database `id` فراہم کرے گا اور database schema میں *column کو non-null `INTEGER` کے طور پر define کرتا ہے*۔ تفصیلات کے لیے [SQLModel دستاویزات primary keys کے بارے میں](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id) دیکھیں۔

* `Field(index=True)` SQLModel کو بتاتا ہے کہ اس column کے لیے ایک **SQL index** بنایا جائے، جو database میں اس column سے فلٹر شدہ data پڑھتے وقت تیز تر lookups کی اجازت دے گا۔

    SQLModel جانتا ہے کہ `str` کے طور پر declare کی گئی چیز `TEXT` (یا `VARCHAR`، database پر منحصر ہے) قسم کا SQL column ہوگا۔

### ایک Engine بنائیں { #create-an-engine }

ایک SQLModel `engine` (اندرونی طور پر یہ دراصل SQLAlchemy `engine` ہے) وہ ہے جو database سے **connections رکھتا ہے**۔

آپ کے پاس اپنے تمام code کے لیے ایک ہی database سے connect ہونے کے لیے **ایک واحد `engine` object** ہوگا۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False` استعمال کرنا FastAPI کو مختلف threads میں ایک ہی SQLite database استعمال کرنے کی اجازت دیتا ہے۔ یہ ضروری ہے کیونکہ **ایک واحد request** **ایک سے زیادہ threads** استعمال کر سکتی ہے (مثلاً dependencies میں)۔

فکر نہ کریں، code کی ساخت کے مطابق، ہم بعد میں یقینی بنائیں گے کہ ہم **فی request ایک واحد SQLModel *session*** استعمال کریں، یہ وہی ہے جو `check_same_thread` حاصل کرنے کی کوشش کر رہا ہے۔

### Tables بنائیں { #create-the-tables }

پھر ہم ایک function شامل کرتے ہیں جو `SQLModel.metadata.create_all(engine)` استعمال کرتا ہے تاکہ تمام *table models* کے لیے **tables بنائے**۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### ایک Session Dependency بنائیں { #create-a-session-dependency }

ایک **`Session`** وہ ہے جو **memory میں objects** کو محفوظ رکھتا ہے اور data میں ضروری تبدیلیوں کا ریکارڈ رکھتا ہے، پھر یہ database سے بات چیت کے لیے **`engine` استعمال کرتا ہے**۔

ہم `yield` کے ساتھ ایک FastAPI **dependency** بنائیں گے جو ہر request کے لیے ایک نیا `Session` فراہم کرے گی۔ یہی وہ چیز ہے جو یقینی بناتی ہے کہ ہم فی request ایک واحد session استعمال کریں۔ 🤓

پھر ہم ایک `Annotated` dependency `SessionDep` بنائیں گے تاکہ باقی code جو اس dependency کو استعمال کرے گا وہ آسان ہو جائے۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Application شروع ہونے پر Database Tables بنائیں { #create-database-tables-on-startup }

ہم application شروع ہونے پر database tables بنائیں گے۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

یہاں ہم application startup event پر tables بناتے ہیں۔

Production کے لیے آپ شاید ایک migration script استعمال کریں گے جو آپ کی app شروع ہونے سے پہلے چلتی ہے۔ 🤓

/// tip | مشورہ

SQLModel میں Alembic کو wrap کرنے والی migration utilities آئیں گی، لیکن ابھی کے لیے، آپ براہ راست [Alembic](https://alembic.sqlalchemy.org/en/latest/) استعمال کر سکتے ہیں۔

///

### ایک Hero بنائیں { #create-a-hero }

چونکہ ہر SQLModel model ایک Pydantic model بھی ہے، آپ اسے انہی **type annotations** میں استعمال کر سکتے ہیں جو آپ Pydantic models کے لیے استعمال کرتے۔

مثال کے طور پر، اگر آپ `Hero` قسم کا parameter declare کرتے ہیں، تو اسے **JSON body** سے پڑھا جائے گا۔

اسی طرح، آپ اسے function کی **return type** کے طور پر declare کر سکتے ہیں، اور پھر data کی شکل خودکار API docs UI میں نظر آئے گی۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

یہاں ہم `SessionDep` dependency (ایک `Session`) استعمال کرتے ہیں تاکہ نیا `Hero` `Session` instance میں شامل کیا جائے، database میں تبدیلیاں commit کی جائیں، `hero` میں data refresh کیا جائے، اور پھر اسے واپس کیا جائے۔

### Heroes پڑھیں { #read-heroes }

ہم `select()` استعمال کرتے ہوئے database سے `Hero`s **پڑھ** سکتے ہیں۔ ہم نتائج کو paginate کرنے کے لیے `limit` اور `offset` شامل کر سکتے ہیں۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### ایک Hero پڑھیں { #read-one-hero }

ہم ایک واحد `Hero` **پڑھ** سکتے ہیں۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### ایک Hero حذف کریں { #delete-a-hero }

ہم ایک `Hero` کو **حذف** بھی کر سکتے ہیں۔

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### App چلائیں { #run-the-app }

آپ app چلا سکتے ہیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

پھر `/docs` UI پر جائیں، آپ دیکھیں گے کہ **FastAPI** ان **models** کو API **document** کرنے کے لیے استعمال کر رہا ہے، اور یہ data کو **serialize** اور **validate** کرنے کے لیے بھی انہیں استعمال کرے گا۔

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## متعدد Models کے ساتھ App کو اپ ڈیٹ کریں { #update-the-app-with-multiple-models }

اب آئیں اس app کو تھوڑا **refactor** کریں تاکہ **security** اور **versatility** بڑھے۔

اگر آپ پچھلی app دیکھیں، UI میں آپ دیکھ سکتے ہیں کہ، ابھی تک، یہ client کو `Hero` بناتے وقت `id` فیصلہ کرنے دیتی ہے۔ 😱

ہمیں ایسا نہیں ہونے دینا چاہیے، وہ ایسا `id` overwrite کر سکتے ہیں جو ہم نے پہلے سے DB میں assign کیا ہے۔ `id` کا فیصلہ **backend** یا **database** کو کرنا چاہیے، **client کو نہیں**۔

اس کے علاوہ، ہم hero کے لیے ایک `secret_name` بناتے ہیں، لیکن ابھی تک، ہم اسے ہر جگہ واپس بھیج رہے ہیں، یہ بہت **خفیہ** نہیں ہے... 😅

ہم ان چیزوں کو چند **اضافی models** شامل کر کے ٹھیک کریں گے۔ یہیں SQLModel چمکے گا۔ ✨

### متعدد Models بنائیں { #create-multiple-models }

**SQLModel** میں، کوئی بھی model class جس میں `table=True` ہو وہ **table model** ہے۔

اور کوئی بھی model class جس میں `table=True` نہ ہو وہ **data model** ہے، یہ دراصل صرف Pydantic models ہیں (چند چھوٹی اضافی خصوصیات کے ساتھ)۔ 🤓

SQLModel کے ساتھ، ہم تمام صورتوں میں تمام fields کو **دہرانے سے بچنے** کے لیے **inheritance** استعمال کر سکتے ہیں۔

#### `HeroBase` - بنیادی class { #herobase-the-base-class }

آئیں ایک `HeroBase` model سے شروع کریں جس میں وہ تمام **fields ہیں جو سب models میں مشترک ہیں**:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *table model* { #hero-the-table-model }

پھر آئیں `Hero` بنائیں، اصل *table model*، جس میں وہ **اضافی fields** ہیں جو ہمیشہ دوسرے models میں نہیں ہوتیں:

* `id`
* `secret_name`

چونکہ `Hero` `HeroBase` سے inherit کرتا ہے، اس میں `HeroBase` میں declare شدہ **fields بھی** ہیں، تو `Hero` کے تمام fields ہیں:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - عوامی *data model* { #heropublic-the-public-data-model }

اس کے بعد، ہم ایک `HeroPublic` model بناتے ہیں، یہ وہ ہے جو API کے clients کو **واپس بھیجا** جائے گا۔

اس میں `HeroBase` جیسے ہی fields ہیں، تو اس میں `secret_name` شامل نہیں ہوگا۔

آخرکار، ہمارے heroes کی شناخت محفوظ ہے! 🥷

یہ `id: int` کو دوبارہ declare بھی کرتا ہے۔ ایسا کرنے سے، ہم API clients کے ساتھ ایک **contract** بنا رہے ہیں، تاکہ وہ ہمیشہ توقع کر سکیں کہ `id` موجود ہوگا اور ہمیشہ `int` ہوگا (کبھی `None` نہیں ہوگا)۔

/// tip | مشورہ

return model میں اس بات کو یقینی بنانا کہ ایک قدر ہمیشہ دستیاب ہو اور ہمیشہ `int` ہو (`None` نہیں) API clients کے لیے بہت مفید ہے، وہ اس یقین کے ساتھ بہت آسان code لکھ سکتے ہیں۔

اس کے علاوہ، **خودکار طور پر بنائے گئے clients** کے سادہ تر interfaces ہوں گے، تاکہ آپ کی API کے ساتھ بات چیت کرنے والے developers کو آپ کی API کے ساتھ کام کرنے کا بہت بہتر تجربہ ہو۔ 😎

///

`HeroPublic` کے تمام fields `HeroBase` جیسے ہی ہیں، `id` کو `int` (نہ کہ `None`) کے طور پر declare کیا گیا ہے:

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - hero بنانے کے لیے *data model* { #herocreate-the-data-model-to-create-a-hero }

اب ہم ایک `HeroCreate` model بناتے ہیں، یہ وہ ہے جو clients سے آنے والے data کو **validate** کرے گا۔

اس میں `HeroBase` جیسے ہی fields ہیں، اور اس میں `secret_name` بھی ہے۔

اب، جب clients **نیا hero بنائیں** گے، وہ `secret_name` بھیجیں گے، اسے database میں محفوظ کیا جائے گا، لیکن وہ خفیہ نام API میں clients کو واپس نہیں بھیجے جائیں گے۔

/// tip | مشورہ

**passwords** کو آپ اسی طرح handle کریں گے۔ انہیں وصول کریں، لیکن API میں واپس نہ بھیجیں۔

آپ passwords کی قدروں کو محفوظ کرنے سے پہلے **hash** بھی کریں گے، **انہیں کبھی سادہ متن میں محفوظ نہ کریں**۔

///

`HeroCreate` کے fields ہیں:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - hero کو اپ ڈیٹ کرنے کے لیے *data model* { #heroupdate-the-data-model-to-update-a-hero }

ہمارے پاس پچھلے ورژن میں **hero کو اپ ڈیٹ** کرنے کا طریقہ نہیں تھا، لیکن اب **متعدد models** کے ساتھ، ہم ایسا کر سکتے ہیں۔ 🎉

`HeroUpdate` *data model* کچھ خاص ہے، اس میں وہ **تمام fields** ہیں جو نیا hero بنانے کے لیے درکار ہوں گے، لیکن تمام fields **optional** ہیں (سب کی ڈیفالٹ قدر ہے)۔ اس طرح، جب آپ hero کو اپ ڈیٹ کریں، تو آپ صرف وہی fields بھیج سکتے ہیں جنہیں آپ اپ ڈیٹ کرنا چاہتے ہیں۔

چونکہ تمام **fields دراصل تبدیل ہو جاتے ہیں** (قسم اب `None` شامل کرتی ہے اور اب ان کی ڈیفالٹ قدر `None` ہے)، ہمیں انہیں **دوبارہ declare** کرنا ہوگا۔

ہمیں واقعی `HeroBase` سے inherit کرنے کی ضرورت نہیں ہے کیونکہ ہم تمام fields دوبارہ declare کر رہے ہیں۔ میں نے اسے مستقل مزاجی کے لیے inherit کرتا چھوڑ دیا ہے، لیکن یہ ضروری نہیں ہے۔ یہ ذاتی پسند کا معاملہ ہے۔ 🤷

`HeroUpdate` کے fields ہیں:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate` سے بنائیں اور `HeroPublic` واپس کریں { #create-with-herocreate-and-return-a-heropublic }

اب جبکہ ہمارے پاس **متعدد models** ہیں، ہم app کے ان حصوں کو اپ ڈیٹ کر سکتے ہیں جو انہیں استعمال کرتے ہیں۔

ہم request میں ایک `HeroCreate` *data model* وصول کرتے ہیں، اور اس سے ایک `Hero` *table model* بناتے ہیں۔

یہ نیا *table model* `Hero` client کی بھیجی گئی fields رکھے گا، اور database کی طرف سے بنایا گیا `id` بھی ہوگا۔

پھر ہم function سے وہی *table model* `Hero` جیسے ہے ویسے واپس کرتے ہیں۔ لیکن چونکہ ہم `response_model` کو `HeroPublic` *data model* کے ساتھ declare کرتے ہیں، **FastAPI** data کو validate اور serialize کرنے کے لیے `HeroPublic` استعمال کرے گا۔

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | مشورہ

اب ہم **return type annotation** `-> HeroPublic` کی بجائے `response_model=HeroPublic` استعمال کرتے ہیں کیونکہ جو قدر ہم واپس کر رہے ہیں وہ دراصل `HeroPublic` *نہیں* ہے۔

اگر ہم `-> HeroPublic` declare کرتے، تو آپ کا editor اور linter (بجا طور پر) شکایت کرتا کہ آپ `HeroPublic` کی بجائے `Hero` واپس کر رہے ہیں۔

اسے `response_model` میں declare کر کے ہم **FastAPI** کو اپنا کام کرنے دے رہے ہیں، بغیر type annotations اور آپ کے editor اور دیگر tools کی مدد میں مداخلت کیے۔

///

### `HeroPublic` کے ساتھ Heroes پڑھیں { #read-heroes-with-heropublic }

ہم پہلے کی طرح `Hero`s **پڑھ** سکتے ہیں، دوبارہ، ہم `response_model=list[HeroPublic]` استعمال کرتے ہیں تاکہ data درست طریقے سے validate اور serialize ہو۔

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic` کے ساتھ ایک Hero پڑھیں { #read-one-hero-with-heropublic }

ہم ایک واحد hero **پڑھ** سکتے ہیں:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate` کے ساتھ Hero کو اپ ڈیٹ کریں { #update-a-hero-with-heroupdate }

ہم **hero کو اپ ڈیٹ** کر سکتے ہیں۔ اس کے لیے ہم HTTP `PATCH` operation استعمال کرتے ہیں۔

اور code میں، ہم client کی بھیجی گئی تمام data کے ساتھ ایک `dict` حاصل کرتے ہیں، **صرف client کی بھیجی گئی data**، ان قدروں کو چھوڑ کر جو صرف ڈیفالٹ قدروں کی وجہ سے وہاں ہوتیں۔ ایسا کرنے کے لیے ہم `exclude_unset=True` استعمال کرتے ہیں۔ یہ اصل چال ہے۔ 🪄

پھر ہم `hero_db.sqlmodel_update(hero_data)` استعمال کرتے ہیں تاکہ `hero_db` کو `hero_data` کے data سے اپ ڈیٹ کیا جائے۔

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Hero کو دوبارہ حذف کریں { #delete-a-hero-again }

**Hero حذف کرنا** تقریباً وہی رہتا ہے۔

ہم اس بار ہر چیز کو refactor کرنے کی خواہش پوری نہیں کریں گے۔ 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### App دوبارہ چلائیں { #run-the-app-again }

آپ app دوبارہ چلا سکتے ہیں:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

اگر آپ `/docs` API UI پر جائیں، تو آپ دیکھیں گے کہ اب یہ اپ ڈیٹ ہو چکا ہے، اور hero بناتے وقت client سے `id` کی توقع نہیں کرے گا، وغیرہ۔

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## خلاصہ { #recap }

آپ SQL database کے ساتھ تعامل کرنے اور *data models* اور *table models* کے ذریعے code کو آسان بنانے کے لیے [**SQLModel**](https://sqlmodel.tiangolo.com/) استعمال کر سکتے ہیں۔

آپ **SQLModel** دستاویزات میں بہت کچھ سیکھ سکتے ہیں، وہاں ایک طویل mini [tutorial **FastAPI** کے ساتھ SQLModel استعمال کرنے کا](https://sqlmodel.tiangolo.com/tutorial/fastapi/) موجود ہے۔ 🚀
