# SQL (Relational) डेटाबेस { #sql-relational-databases }

**FastAPI** के लिए SQL (relational) डेटाबेस इस्तेमाल करना required नहीं है। लेकिन आप **कोई भी डेटाबेस** इस्तेमाल कर सकते हैं जो आप चाहें।

यहाँ हम [SQLModel](https://sqlmodel.tiangolo.com/) का उपयोग करके एक उदाहरण देखेंगे।

**SQLModel**, [SQLAlchemy](https://www.sqlalchemy.org/) और Pydantic के ऊपर बना है। इसे **FastAPI** के उसी लेखक ने बनाया है ताकि यह उन FastAPI applications के लिए perfect match हो जिन्हें **SQL databases** इस्तेमाल करने की जरूरत होती है।

/// tip | टिप

आप अपनी पसंद की कोई भी दूसरी SQL या NoSQL डेटाबेस लाइब्रेरी इस्तेमाल कर सकते हैं (कुछ मामलों में इन्हें <abbr title="Object Relational Mapper - ऑब्जेक्ट रिलेशनल मैपर: एक लाइब्रेरी के लिए एक fancy शब्द जिसमें कुछ classes SQL tables को represent करती हैं और instances उन tables में rows को represent करते हैं">"ORMs"</abbr> कहा जाता है), FastAPI आपको कुछ भी इस्तेमाल करने के लिए मजबूर नहीं करता। 😎

///

क्योंकि SQLModel, SQLAlchemy पर आधारित है, आप SQLAlchemy द्वारा **supported कोई भी डेटाबेस** आसानी से इस्तेमाल कर सकते हैं (जिससे वे SQLModel द्वारा भी supported हो जाते हैं), जैसे:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, आदि।

इस उदाहरण में, हम **SQLite** इस्तेमाल करेंगे, क्योंकि यह एक single file का उपयोग करता है और Python में इसके लिए integrated support है। इसलिए, आप इस उदाहरण को copy कर सकते हैं और जैसा है वैसा ही run कर सकते हैं।

बाद में, अपनी production application के लिए, आप **PostgreSQL** जैसा database server इस्तेमाल करना चाह सकते हैं।

/// tip | टिप

**FastAPI** और **PostgreSQL** के साथ एक official project generator है जिसमें frontend और अधिक tools शामिल हैं: [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

यह एक बहुत ही सरल और छोटा tutorial है, अगर आप सामान्य रूप से databases, SQL, या अधिक advanced features के बारे में सीखना चाहते हैं, तो [SQLModel docs](https://sqlmodel.tiangolo.com/) पर जाएँ।

## `SQLModel` install करें { #install-sqlmodel }

सबसे पहले, सुनिश्चित करें कि आप अपना [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और फिर `sqlmodel` install करें:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Single Model के साथ App बनाएँ { #create-the-app-with-a-single-model }

हम पहले एक single **SQLModel** model के साथ app का सबसे सरल पहला version बनाएँगे।

बाद में हम नीचे **multiple models** के साथ security और versatility बढ़ाते हुए इसे बेहतर बनाएँगे। 🤓

### Models बनाएँ { #create-models }

`SQLModel` import करें और एक डेटाबेस model बनाएँ:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` class एक Pydantic model से बहुत मिलती-जुलती है (वास्तव में, अंदर से, यह सच में *एक Pydantic model ही है*)।

कुछ अंतर हैं:

* `table=True` SQLModel को बताता है कि यह एक *table model* है, इसे SQL डेटाबेस में एक **table** को represent करना चाहिए, यह सिर्फ एक *data model* नहीं है (जैसा कि कोई भी दूसरी regular Pydantic class होती)।

* `Field(primary_key=True)` SQLModel को बताता है कि `id` SQL डेटाबेस में **primary key** है (आप SQL primary keys के बारे में SQLModel docs में अधिक जान सकते हैं)।

    **ध्यान दें:** हम primary key field के लिए `int | None` का उपयोग करते हैं ताकि Python code में हम *बिना `id` के object बना सकें* (`id=None`), यह मानते हुए कि डेटाबेस *save करते समय इसे generate करेगा*। SQLModel समझता है कि डेटाबेस `id` provide करेगा और डेटाबेस schema में *column को non-null `INTEGER` के रूप में define करता है*। विवरण के लिए [primary keys पर SQLModel docs](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id) देखें।

* `Field(index=True)` SQLModel को बताता है कि उसे इस column के लिए एक **SQL index** बनाना चाहिए, जिससे इस column द्वारा filtered data पढ़ते समय डेटाबेस में तेज़ lookups हो सकें।

    SQLModel जान जाएगा कि `str` के रूप में declared कोई चीज़ `TEXT` type का SQL column होगी (या डेटाबेस के आधार पर `VARCHAR`)।

### Engine बनाएँ { #create-an-engine }

SQLModel `engine` (अंदर से यह वास्तव में SQLAlchemy `engine` है) वह है जो डेटाबेस से **connections को hold** करता है।

आपके सभी code के लिए उसी डेटाबेस से connect करने हेतु **एक single `engine` object** होगा।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False` का उपयोग FastAPI को अलग-अलग threads में वही SQLite डेटाबेस इस्तेमाल करने देता है। यह necessary है क्योंकि **एक single request** **एक से अधिक thread** का उपयोग कर सकती है (उदाहरण के लिए dependencies में)।

चिंता न करें, code जिस तरह structured है, उससे हम सुनिश्चित करेंगे कि बाद में हम **प्रति request एक single SQLModel *session*** इस्तेमाल करें, वास्तव में `check_same_thread` यही हासिल करने की कोशिश कर रहा है।

### Tables बनाएँ { #create-the-tables }

फिर हम एक function जोड़ते हैं जो सभी *table models* के लिए **tables बनाने** हेतु `SQLModel.metadata.create_all(engine)` का उपयोग करता है।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Session Dependency बनाएँ { #create-a-session-dependency }

**`Session`** वह है जो **objects को memory में store** करता है और data में required किसी भी बदलाव का track रखता है, फिर यह डेटाबेस से communicate करने के लिए **`engine` का उपयोग करता है**।

हम `yield` के साथ एक FastAPI **dependency** बनाएँगे जो हर request के लिए एक नया `Session` provide करेगी। यही सुनिश्चित करता है कि हम प्रति request एक single session इस्तेमाल करें। 🤓

फिर हम इस dependency का उपयोग करने वाले बाकी code को आसान बनाने के लिए एक `Annotated` dependency `SessionDep` बनाते हैं।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Startup पर Database Tables बनाएँ { #create-database-tables-on-startup }

हम application शुरू होने पर database tables बनाएँगे।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

यहाँ हम application startup event पर tables बनाते हैं।

production के लिए आप शायद एक migration script इस्तेमाल करेंगे जो आपका app शुरू करने से पहले run होती है। 🤓

/// tip | टिप

SQLModel में Alembic को wrap करने वाली migration utilities होंगी, लेकिन अभी के लिए, आप सीधे [Alembic](https://alembic.sqlalchemy.org/en/latest/) इस्तेमाल कर सकते हैं।

///

### Hero बनाएँ { #create-a-hero }

क्योंकि हर SQLModel model एक Pydantic model भी है, आप इसे उसी **type annotations** में इस्तेमाल कर सकते हैं जिनमें आप Pydantic models इस्तेमाल करते।

उदाहरण के लिए, अगर आप `Hero` type का parameter declare करते हैं, तो यह **JSON body** से read किया जाएगा।

उसी तरह, आप इसे function के **return type** के रूप में declare कर सकते हैं, और फिर data का shape automatic API docs UI में दिखाई देगा।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

यहाँ हम `SessionDep` dependency (एक `Session`) का उपयोग करके नए `Hero` को `Session` instance में add करते हैं, changes को डेटाबेस में commit करते हैं, `hero` में data refresh करते हैं, और फिर उसे return करते हैं।

### Heroes पढ़ें { #read-heroes }

हम `select()` का उपयोग करके डेटाबेस से `Hero`s **read** कर सकते हैं। results को paginate करने के लिए हम `limit` और `offset` include कर सकते हैं।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### एक Hero पढ़ें { #read-one-hero }

हम एक single `Hero` **read** कर सकते हैं।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero Delete करें { #delete-a-hero }

हम एक `Hero` को **delete** भी कर सकते हैं।

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### App Run करें { #run-the-app }

आप app run कर सकते हैं:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

फिर `/docs` UI पर जाएँ, आप देखेंगे कि **FastAPI** API को **document** करने के लिए इन **models** का उपयोग कर रहा है, और यह data को **serialize** और **validate** करने के लिए भी इनका उपयोग करेगा।

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Multiple Models के साथ App Update करें { #update-the-app-with-multiple-models }

अब आइए **security** और **versatility** बढ़ाने के लिए इस app को थोड़ा **refactor** करें।

अगर आप previous app देखें, तो UI में आप देख सकते हैं कि अभी तक यह client को बनने वाले `Hero` का `id` तय करने देता है। 😱

हमें ऐसा नहीं होने देना चाहिए, वे DB में पहले से assigned किसी `id` को overwrite कर सकते हैं। `id` तय करना **backend** या **database** द्वारा किया जाना चाहिए, **client द्वारा नहीं**।

इसके अलावा, हम hero के लिए `secret_name` बनाते हैं, लेकिन अब तक, हम इसे हर जगह return कर रहे हैं, यह बहुत **secret** नहीं है... 😅

हम कुछ **extra models** जोड़कर इन चीज़ों को ठीक करेंगे। यहीं SQLModel चमकेगा। ✨

### Multiple Models बनाएँ { #create-multiple-models }

**SQLModel** में, कोई भी model class जिसमें `table=True` है, एक **table model** है।

और कोई भी model class जिसमें `table=True` नहीं है, एक **data model** है, ये वास्तव में सिर्फ Pydantic models हैं (कुछ छोटे extra features के साथ)। 🤓

SQLModel के साथ, हम सभी मामलों में सभी fields को **duplicate करने से बचने** के लिए **inheritance** का उपयोग कर सकते हैं।

#### `HeroBase` - base class { #herobase-the-base-class }

आइए एक `HeroBase` model से शुरू करें जिसमें सभी models द्वारा **shared fields** हों:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *table model* { #hero-the-table-model }

फिर आइए `Hero` बनाएँ, वास्तविक *table model*, जिसमें वे **extra fields** हों जो हमेशा दूसरे models में नहीं होते:

* `id`
* `secret_name`

क्योंकि `Hero`, `HeroBase` से inherit करता है, इसमें `HeroBase` में declared **fields** भी हैं, इसलिए `Hero` के लिए सभी fields हैं:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - public *data model* { #heropublic-the-public-data-model }

इसके बाद, हम एक `HeroPublic` model बनाते हैं, यही वह है जो API के clients को **return** किया जाएगा।

इसमें `HeroBase` जैसे ही fields हैं, इसलिए इसमें `secret_name` शामिल नहीं होगा।

आख़िरकार, हमारे heroes की identity protected है! 🥷

यह `id: int` को फिर से declare भी करता है। ऐसा करके, हम API clients के साथ एक **contract** बना रहे हैं, ताकि वे हमेशा expect कर सकें कि `id` मौजूद होगा और `int` होगा (यह कभी `None` नहीं होगा)।

/// tip | टिप

return model से यह सुनिश्चित करवाना कि कोई value हमेशा available है और हमेशा `int` है (`None` नहीं), API clients के लिए बहुत उपयोगी है, वे इस certainty के साथ बहुत सरल code लिख सकते हैं।

साथ ही, **automatically generated clients** में सरल interfaces होंगे, ताकि आपकी API से communicate करने वाले developers आपकी API के साथ काम करते समय बहुत बेहतर अनुभव पा सकें। 😎

///

`HeroPublic` में सभी fields `HeroBase` जैसे ही हैं, जिसमें `id` को `int` (`None` नहीं) के रूप में declared किया गया है:

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - hero बनाने के लिए *data model* { #herocreate-the-data-model-to-create-a-hero }

अब हम एक `HeroCreate` model बनाते हैं, यही वह है जो clients से आने वाले data को **validate** करेगा।

इसमें `HeroBase` जैसे ही fields हैं, और इसमें `secret_name` भी है।

अब, जब clients **एक नया hero create** करेंगे, वे `secret_name` भेजेंगे, यह डेटाबेस में store होगा, लेकिन वे secret names API में clients को return नहीं किए जाएँगे।

/// tip | टिप

आप **passwords** को ऐसे handle करेंगे। उन्हें receive करें, लेकिन API में return न करें।

आप passwords की values को store करने से पहले **hash** भी करेंगे, **उन्हें plain text में कभी store न करें**।

///

`HeroCreate` के fields हैं:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - hero update करने के लिए *data model* { #heroupdate-the-data-model-to-update-a-hero }

app के previous version में हमारे पास **hero update करने** का तरीका नहीं था, लेकिन अब **multiple models** के साथ, हम ऐसा कर सकते हैं। 🎉

`HeroUpdate` *data model* थोड़ा special है, इसमें **वे सभी same fields** हैं जिनकी एक नया hero create करने के लिए जरूरत होगी, लेकिन सभी fields **optional** हैं (उन सभी की default value है)। इस तरह, जब आप hero update करते हैं, तो आप सिर्फ वे fields भेज सकते हैं जिन्हें आप update करना चाहते हैं।

क्योंकि सभी **fields वास्तव में change होते हैं** (type में अब `None` शामिल है और अब उनकी default value `None` है), हमें उन्हें **re-declare** करना होगा।

हमें वास्तव में `HeroBase` से inherit करने की जरूरत नहीं है क्योंकि हम सभी fields को re-declare कर रहे हैं। मैं consistency के लिए इसे inherit करता हुआ छोड़ूँगा, लेकिन यह necessary नहीं है। यह personal taste का मामला अधिक है। 🤷

`HeroUpdate` के fields हैं:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate` के साथ create करें और `HeroPublic` return करें { #create-with-herocreate-and-return-a-heropublic }

अब जब हमारे पास **multiple models** हैं, हम app के उन parts को update कर सकते हैं जो उनका उपयोग करते हैं।

हम request में एक `HeroCreate` *data model* receive करते हैं, और उससे, हम एक `Hero` *table model* बनाते हैं।

इस नए *table model* `Hero` में client द्वारा भेजे गए fields होंगे, और इसमें डेटाबेस द्वारा generated एक `id` भी होगा।

फिर हम उसी *table model* `Hero` को function से जैसा है वैसा ही return करते हैं। लेकिन क्योंकि हम `response_model` को `HeroPublic` *data model* के साथ declare करते हैं, **FastAPI** data को validate और serialize करने के लिए `HeroPublic` का उपयोग करेगा।

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | टिप

अब हम **return type annotation** `-> HeroPublic` के बजाय `response_model=HeroPublic` इस्तेमाल करते हैं क्योंकि जो value हम return कर रहे हैं वह वास्तव में `HeroPublic` *नहीं* है।

अगर हमने `-> HeroPublic` declare किया होता, तो आपका editor और linter complain करते (और सही करते) कि आप `HeroPublic` के बजाय `Hero` return कर रहे हैं।

इसे `response_model` में declare करके हम **FastAPI** को अपना काम करने के लिए कह रहे हैं, बिना type annotations और आपके editor व अन्य tools से मिलने वाली help में interfere किए।

///

### `HeroPublic` के साथ Heroes पढ़ें { #read-heroes-with-heropublic }

हम `Hero`s को **read** करने के लिए पहले जैसा ही कर सकते हैं, फिर से, हम यह सुनिश्चित करने के लिए `response_model=list[HeroPublic]` का उपयोग करते हैं कि data सही तरीके से validate और serialize हो।

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic` के साथ एक Hero पढ़ें { #read-one-hero-with-heropublic }

हम एक single hero **read** कर सकते हैं:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate` के साथ Hero Update करें { #update-a-hero-with-heroupdate }

हम **hero update** कर सकते हैं। इसके लिए हम HTTP `PATCH` operation इस्तेमाल करते हैं।

और code में, हमें client द्वारा भेजे गए सभी data के साथ एक `dict` मिलता है, **सिर्फ client द्वारा भेजा गया data**, उन किसी भी values को exclude करते हुए जो सिर्फ default values होने के कारण वहाँ होतीं। ऐसा करने के लिए हम `exclude_unset=True` इस्तेमाल करते हैं। यही main trick है। 🪄

फिर हम `hero_data` के data के साथ `hero_db` को update करने के लिए `hero_db.sqlmodel_update(hero_data)` इस्तेमाल करते हैं।

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### फिर से Hero Delete करें { #delete-a-hero-again }

hero को **delete करना** लगभग पहले जैसा ही रहता है।

हम इसमें सब कुछ refactor करने की इच्छा पूरी नहीं करेंगे। 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### App फिर से Run करें { #run-the-app-again }

आप app फिर से run कर सकते हैं:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

अगर आप `/docs` API UI पर जाते हैं, तो आप देखेंगे कि यह अब updated है, और hero create करते समय यह client से `id` receive करने की expect नहीं करेगा, आदि।

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Recap { #recap }

आप SQL डेटाबेस के साथ interact करने और code को *data models* और *table models* के साथ सरल बनाने के लिए [**SQLModel**](https://sqlmodel.tiangolo.com/) का उपयोग कर सकते हैं।

आप **SQLModel** docs में बहुत कुछ और सीख सकते हैं, वहाँ **FastAPI** के साथ SQLModel इस्तेमाल करने पर एक लंबा mini [tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/) है। 🚀
