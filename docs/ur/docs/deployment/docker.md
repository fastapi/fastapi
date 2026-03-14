# FastAPI in Containers - Docker { #fastapi-in-containers-docker }

FastAPI ایپلیکیشنز deploy کرتے وقت ایک عام طریقہ **Linux container image** بنانا ہے۔ یہ عام طور پر [**Docker**](https://www.docker.com/) استعمال کرتے ہوئے کیا جاتا ہے۔ پھر آپ اس container image کو کئی ممکنہ طریقوں سے deploy کر سکتے ہیں۔

Linux containers استعمال کرنے کے کئی فوائد ہیں بشمول **سیکیورٹی**، **نقل پذیری**، **سادگی**، اور دیگر۔

/// tip | مشورہ

جلدی میں ہیں اور یہ سب پہلے سے جانتے ہیں؟ نیچے [`Dockerfile` 👇](#build-a-docker-image-for-fastapi) پر جائیں۔

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Container کیا ہے { #what-is-a-container }

Containers (بنیادی طور پر Linux containers) ایپلیکیشنز کو ان کی تمام dependencies اور ضروری فائلوں سمیت پیکیج کرنے کا ایک بہت **ہلکا** طریقہ ہے جبکہ انہیں اسی سسٹم میں دوسرے containers (دوسری ایپلیکیشنز یا اجزاء) سے الگ رکھتے ہیں۔

Linux containers host (مشین، virtual machine، cloud server وغیرہ) کے اسی Linux kernel کا استعمال کرتے ہوئے چلتے ہیں۔ اس کا مطلب ہے کہ وہ بہت ہلکے ہیں (مکمل virtual machines جو پورا آپریٹنگ سسٹم ایمولیٹ کرتی ہیں ان کے مقابلے میں)۔

اس طرح، containers **کم وسائل** استعمال کرتے ہیں، processes کو براہ راست چلانے کے مقابلے میں تقریباً اتنی ہی مقدار (virtual machine بہت زیادہ استعمال کرے گی)۔

Containers کے اپنے **الگ** چلنے والے processes (عام طور پر صرف ایک process)، فائل سسٹم، اور نیٹ ورک بھی ہوتے ہیں، جو deployment، سیکیورٹی، development وغیرہ کو آسان بناتے ہیں۔

## Container Image کیا ہے { #what-is-a-container-image }

ایک **container** ایک **container image** سے چلایا جاتا ہے۔

Container image تمام فائلوں، environment variables، اور ڈیفالٹ command/پروگرام کا ایک **جامد** ورژن ہے جو container میں موجود ہونا چاہیے۔ **جامد** کا مطلب ہے کہ container **image** نہیں چل رہی، عمل درآمد نہیں ہو رہا، یہ صرف پیکیج شدہ فائلیں اور metadata ہے۔

"**container image**" جو محفوظ جامد مواد ہے اس کے برعکس، "**container**" عام طور پر چلنے والے instance، اس چیز کا حوالہ دیتا ہے جو **عمل درآمد** ہو رہی ہے۔

جب **container** شروع ہوتا ہے اور چل رہا ہوتا ہے (**container image** سے شروع ہوا) تو یہ فائلیں، environment variables وغیرہ بنا یا تبدیل کر سکتا ہے۔ وہ تبدیلیاں صرف اس container میں موجود ہوں گی، لیکن بنیادی container image میں برقرار نہیں رہیں گی (ڈسک پر محفوظ نہیں ہوں گی)۔

Container image **پروگرام** فائل اور مواد سے موازنہ کی جا سکتی ہے، مثلاً `python` اور کوئی فائل `main.py`۔

اور **container** خود (**container image** کے برعکس) image کا اصل چلنے والا instance ہے، ایک **process** سے موازنہ کیا جا سکتا ہے۔ درحقیقت، ایک container صرف تبھی چل رہا ہوتا ہے جب اس کا **process چل** رہا ہو (اور عام طور پر یہ صرف ایک واحد process ہوتا ہے)۔ جب اس میں کوئی process نہ چل رہا ہو تو container رک جاتا ہے۔

## Container Images { #container-images }

Docker **container images** اور **containers** بنانے اور منظم کرنے کے اہم ٹولز میں سے ایک رہا ہے۔

اور ایک عوامی [Docker Hub](https://hub.docker.com/) ہے جس میں بہت سے ٹولز، ماحول، ڈیٹابیسز اور ایپلیکیشنز کے لیے پہلے سے بنی **سرکاری container images** ہیں۔

مثال کے طور پر، ایک سرکاری [Python Image](https://hub.docker.com/_/python) ہے۔

اور ڈیٹابیسز جیسی مختلف چیزوں کے لیے بہت سی اور images ہیں، مثلاً:

* [PostgreSQL](https://hub.docker.com/_/postgres)
* [MySQL](https://hub.docker.com/_/mysql)
* [MongoDB](https://hub.docker.com/_/mongo)
* [Redis](https://hub.docker.com/_/redis) وغیرہ۔

پہلے سے بنی container image استعمال کرنے سے مختلف ٹولز کو **ملانا** اور استعمال کرنا بہت آسان ہے۔ مثال کے طور پر، نیا ڈیٹابیس آزمانے کے لیے۔ زیادہ تر معاملات میں، آپ **سرکاری images** استعمال کر سکتے ہیں، اور بس environment variables سے انہیں ترتیب دے سکتے ہیں۔

اس طرح، بہت سے معاملات میں آپ containers اور Docker کے بارے میں سیکھ سکتے ہیں اور اس علم کو بہت سے مختلف ٹولز اور اجزاء کے ساتھ دوبارہ استعمال کر سکتے ہیں۔

تو، آپ مختلف چیزوں کے ساتھ **متعدد containers** چلائیں گے، جیسے ڈیٹابیس، Python ایپلیکیشن، React frontend ایپلیکیشن والا web server، اور انہیں ان کے اندرونی نیٹ ورک کے ذریعے جوڑیں گے۔

تمام container management systems (جیسے Docker یا Kubernetes) میں یہ نیٹ ورکنگ خصوصیات شامل ہوتی ہیں۔

## Containers اور Processes { #containers-and-processes }

ایک **container image** عام طور پر اپنے metadata میں ڈیفالٹ پروگرام یا command شامل کرتی ہے جو **container** شروع ہونے پر چلنی چاہیے اور اس پروگرام کو دیے جانے والے parameters۔ بالکل اسی طرح جیسے command line میں ہوتا۔

جب **container** شروع ہوتا ہے، تو یہ وہ command/پروگرام چلائے گا (اگرچہ آپ اسے override کر کے مختلف command/پروگرام چلا سکتے ہیں)۔

Container تب تک چل رہا ہوتا ہے جب تک **مرکزی process** (command یا پروگرام) چل رہا ہو۔

Container میں عام طور پر ایک **واحد process** ہوتا ہے، لیکن مرکزی process سے subprocesses شروع کرنا بھی ممکن ہے، اور اس طرح آپ کے پاس ایک ہی container میں **متعدد processes** ہوں گے۔

لیکن **کم از کم ایک چلنے والے process** کے بغیر چلنے والا container ممکن نہیں ہے۔ اگر مرکزی process رک جائے، تو container رک جاتا ہے۔

## FastAPI کے لیے Docker Image بنائیں { #build-a-docker-image-for-fastapi }

ٹھیک ہے، آئیے اب کچھ بناتے ہیں! 🚀

میں آپ کو دکھاؤں گا کہ **سرکاری Python** image کی بنیاد پر، FastAPI کے لیے **شروع سے Docker image** کیسے بنائیں۔

یہی وہ ہے جو آپ **زیادہ تر معاملات** میں کرنا چاہیں گے، مثلاً:

* **Kubernetes** یا اسی طرح کے ٹولز استعمال کرتے ہوئے
* **Raspberry Pi** پر چلاتے ہوئے
* کسی cloud service استعمال کرتے ہوئے جو آپ کے لیے container image چلائے، وغیرہ۔

### Package Requirements { #package-requirements }

آپ کے پاس عام طور پر اپنی ایپلیکیشن کے لیے **package requirements** کسی فائل میں ہوں گی۔

یہ بنیادی طور پر اس ٹول پر منحصر ہوگا جو آپ ان requirements کو **انسٹال** کرنے کے لیے استعمال کرتے ہیں۔

سب سے عام طریقہ `requirements.txt` فائل رکھنا ہے جس میں package کے نام اور ان کے ورژن، ہر لائن میں ایک، ہوتے ہیں۔

آپ یقیناً ورژنز کی حدود مقرر کرنے کے لیے وہی خیالات استعمال کریں گے جو آپ نے [FastAPI ورژنز کے بارے میں](versions.md) میں پڑھے۔

مثال کے طور پر، آپ کی `requirements.txt` کچھ ایسی نظر آ سکتی ہے:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

اور آپ عام طور پر ان package dependencies کو `pip` سے انسٹال کریں گے، مثلاً:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | معلومات

package dependencies تعین اور انسٹال کرنے کے لیے دوسرے فارمیٹس اور ٹولز بھی ہیں۔

///

### **FastAPI** کوڈ بنائیں { #create-the-fastapi-code }

* ایک `app` ڈائریکٹری بنائیں اور اس میں داخل ہوں۔
* ایک خالی `__init__.py` فائل بنائیں۔
* ایک `main.py` فائل بنائیں اس کے ساتھ:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

اب اسی پراجیکٹ ڈائریکٹری میں ایک `Dockerfile` فائل بنائیں اس کے ساتھ:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. سرکاری Python base image سے شروع کریں۔

2. موجودہ ورکنگ ڈائریکٹری `/code` مقرر کریں۔

    یہاں ہم `requirements.txt` فائل اور `app` ڈائریکٹری رکھیں گے۔

3. requirements والی فائل کو `/code` ڈائریکٹری میں کاپی کریں۔

    **صرف** requirements والی فائل پہلے کاپی کریں، باقی کوڈ نہیں۔

    چونکہ یہ فائل **اکثر تبدیل نہیں ہوتی**، Docker اسے پہچان لے گا اور اس مرحلے کے لیے **cache** استعمال کرے گا، اگلے مرحلے کے لیے بھی cache فعال رکھتے ہوئے۔

4. requirements فائل میں موجود package dependencies انسٹال کریں۔

    `--no-cache-dir` اختیار `pip` کو بتاتا ہے کہ ڈاؤن لوڈ شدہ packages مقامی طور پر محفوظ نہ کرے، کیونکہ یہ صرف تبھی ہوتا جب `pip` انہی packages کو دوبارہ انسٹال کرنے کے لیے چلایا جاتا، لیکن containers کے ساتھ کام کرتے وقت ایسا نہیں ہوتا۔

    /// note | نوٹ

    `--no-cache-dir` صرف `pip` سے متعلق ہے، اس کا Docker یا containers سے کوئی تعلق نہیں ہے۔

    ///

    `--upgrade` اختیار `pip` کو بتاتا ہے کہ اگر packages پہلے سے انسٹال ہیں تو انہیں اپ گریڈ کرے۔

    چونکہ فائل کاپی کرنے کا پچھلا مرحلہ **Docker cache** کے ذریعے پہچانا جا سکتا ہے، یہ مرحلہ بھی دستیاب ہونے پر **Docker cache استعمال کرے** گا۔

    اس مرحلے میں cache استعمال کرنے سے development کے دوران بار بار image بناتے وقت آپ کا بہت سا **وقت بچے** گا، ہر بار تمام dependencies **ڈاؤن لوڈ اور انسٹال** کرنے کے بجائے۔

5. `./app` ڈائریکٹری کو `/code` ڈائریکٹری کے اندر کاپی کریں۔

    چونکہ اس میں وہ تمام کوڈ ہے جو **سب سے زیادہ تبدیل ہوتا ہے** Docker **cache** آسانی سے اس یا اس کے بعد کے **مراحل** کے لیے استعمال نہیں ہو سکے گا۔

    اس لیے، container image کے build time کو بہتر بنانے کے لیے اسے `Dockerfile` کے **آخر کے قریب** رکھنا ضروری ہے۔

6. `fastapi run` استعمال کرنے کے لیے **command** مقرر کریں، جو نیچے Uvicorn استعمال کرتا ہے۔

    `CMD` strings کی ایک فہرست لیتا ہے، ان میں سے ہر string وہ ہے جو آپ command line میں spaces سے الگ کر کے ٹائپ کرتے۔

    یہ command **موجودہ ورکنگ ڈائریکٹری** سے چلایا جائے گا، وہی `/code` ڈائریکٹری جو آپ نے اوپر `WORKDIR /code` سے مقرر کی۔

/// tip | مشورہ

کوڈ میں ہر نمبر والے بلبلے پر کلک کر کے دیکھیں کہ ہر لائن کیا کرتی ہے۔ 👆

///

/// warning | انتباہ

ہمیشہ `CMD` ہدایت کی **exec form** استعمال کرنا یقینی بنائیں، جیسا کہ نیچے بیان کیا گیا ہے۔

///

#### `CMD` - Exec Form استعمال کریں { #use-cmd-exec-form }

[`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) Docker ہدایت دو شکلوں میں لکھی جا سکتی ہے:

✅ **Exec** form:

```Dockerfile
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```Dockerfile
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

ہمیشہ **exec** form استعمال کرنا یقینی بنائیں تاکہ FastAPI خوبصورتی سے shutdown ہو سکے اور [lifespan events](../advanced/events.md) فعال ہوں۔

آپ اس کے بارے میں مزید [Docker docs for shell and exec form](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form) میں پڑھ سکتے ہیں۔

`docker compose` استعمال کرتے وقت یہ کافی نمایاں ہو سکتا ہے۔ مزید تکنیکی تفصیلات کے لیے Docker Compose FAQ کا یہ حصہ دیکھیں: [Why do my services take 10 seconds to recreate or stop?](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop)۔

#### ڈائریکٹری کا ڈھانچہ { #directory-structure }

اب آپ کے پاس ایسا ڈائریکٹری ڈھانچہ ہونا چاہیے:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### TLS Termination Proxy کے پیچھے { #behind-a-tls-termination-proxy }

اگر آپ اپنا container TLS Termination Proxy (load balancer) جیسے Nginx یا Traefik کے پیچھے چلا رہے ہیں، تو `--proxy-headers` اختیار شامل کریں، یہ Uvicorn کو (FastAPI CLI کے ذریعے) بتائے گا کہ اس proxy کی طرف سے بھیجے گئے headers پر اعتماد کرے جو بتاتے ہیں کہ ایپلیکیشن HTTPS وغیرہ کے پیچھے چل رہی ہے۔

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker Cache { #docker-cache }

اس `Dockerfile` میں ایک اہم چال ہے، ہم پہلے **صرف dependencies والی فائل** کاپی کرتے ہیں، باقی کوڈ نہیں۔ آئیے بتاتے ہیں کہ ایسا کیوں ہے۔

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker اور دوسرے ٹولز ان container images کو **بتدریج** بناتے ہیں، `Dockerfile` کے اوپر سے شروع کرتے ہوئے اور `Dockerfile` کی ہر ہدایت سے بنائی گئی فائلوں کو شامل کرتے ہوئے **ایک پرت دوسری کے اوپر** رکھتے ہیں۔

Docker اور اسی طرح کے ٹولز image بناتے وقت **اندرونی cache** بھی استعمال کرتے ہیں، اگر کوئی فائل آخری بار container image بنانے کے بعد سے تبدیل نہیں ہوئی، تو یہ فائل کو دوبارہ کاپی کرنے اور شروع سے نئی پرت بنانے کے بجائے آخری بار بنائی گئی **وہی پرت دوبارہ استعمال** کرے گا۔

صرف فائلوں کی کاپی سے بچنا ضروری نہیں کہ چیزوں کو بہت بہتر بنائے، لیکن چونکہ اس نے اس مرحلے کے لیے cache استعمال کیا، یہ **اگلے مرحلے کے لیے cache استعمال** کر سکتا ہے۔ مثلاً، یہ dependencies انسٹال کرنے والی ہدایت کے لیے cache استعمال کر سکتا ہے:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Package requirements والی فائل **اکثر تبدیل نہیں ہوتی**۔ تو، صرف وہ فائل کاپی کرنے سے، Docker اس مرحلے کے لیے **cache استعمال** کر سکے گا۔

اور پھر، Docker اگلے مرحلے کے لیے بھی **cache استعمال** کر سکے گا جو ان dependencies کو ڈاؤن لوڈ اور انسٹال کرتا ہے۔ اور یہیں ہم **بہت سا وقت بچاتے** ہیں۔ ✨ ...اور اکتاہٹ سے بچتے ہیں۔ 😪😆

Package dependencies ڈاؤن لوڈ اور انسٹال کرنے میں **منٹ** لگ سکتے ہیں، لیکن **cache** استعمال کرنے میں زیادہ سے زیادہ **سیکنڈ** لگیں گے۔

اور چونکہ آپ development کے دوران بار بار container image بناتے رہیں گے تاکہ آپ کے کوڈ کی تبدیلیاں کام کر رہی ہیں، اس سے بہت زیادہ مجموعی وقت بچتا ہے۔

پھر، `Dockerfile` کے آخر کے قریب، ہم تمام کوڈ کاپی کرتے ہیں۔ چونکہ یہ وہ ہے جو **سب سے زیادہ تبدیل ہوتا ہے**، ہم اسے آخر کے قریب رکھتے ہیں، کیونکہ تقریباً ہمیشہ، اس مرحلے کے بعد کی کوئی بھی چیز cache استعمال نہیں کر سکے گی۔

```Dockerfile
COPY ./app /code/app
```

### Docker Image بنائیں { #build-the-docker-image }

اب جب تمام فائلیں جگہ پر ہیں، آئیے container image بناتے ہیں۔

* پراجیکٹ ڈائریکٹری میں جائیں (جہاں آپ کی `Dockerfile` ہے، آپ کی `app` ڈائریکٹری پر مشتمل)۔
* اپنی FastAPI image بنائیں:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | مشورہ

آخر میں `.` پر دھیان دیں، یہ `./` کے مساوی ہے، یہ Docker کو بتاتا ہے کہ container image بنانے کے لیے کون سی ڈائریکٹری استعمال کرنی ہے۔

اس معاملے میں، یہ وہی موجودہ ڈائریکٹری (`.`) ہے۔

///

### Docker Container شروع کریں { #start-the-docker-container }

* اپنی image کی بنیاد پر container چلائیں:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## اسے چیک کریں { #check-it }

آپ اسے اپنے Docker container کے URL میں چیک کر سکتے ہیں، مثلاً: [http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) یا [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery) (یا مساوی، آپ کے Docker host کا استعمال کرتے ہوئے)۔

آپ کو کچھ ایسا نظر آئے گا:

```JSON
{"item_id": 5, "q": "somequery"}
```

## انٹرایکٹو API دستاویزات { #interactive-api-docs }

اب آپ [http://192.168.99.100/docs](http://192.168.99.100/docs) یا [http://127.0.0.1/docs](http://127.0.0.1/docs) (یا مساوی، آپ کے Docker host کا استعمال کرتے ہوئے) پر جا سکتے ہیں۔

آپ کو خودکار انٹرایکٹو API دستاویزات نظر آئیں گی ([Swagger UI](https://github.com/swagger-api/swagger-ui) کی فراہم کردہ):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## متبادل API دستاویزات { #alternative-api-docs }

اور آپ [http://192.168.99.100/redoc](http://192.168.99.100/redoc) یا [http://127.0.0.1/redoc](http://127.0.0.1/redoc) (یا مساوی، آپ کے Docker host کا استعمال کرتے ہوئے) پر بھی جا سکتے ہیں۔

آپ کو متبادل خودکار دستاویزات نظر آئیں گی ([ReDoc](https://github.com/Rebilly/ReDoc) کی فراہم کردہ):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## واحد فائل FastAPI کے ساتھ Docker Image بنائیں { #build-a-docker-image-with-a-single-file-fastapi }

اگر آپ کی FastAPI واحد فائل ہے، مثلاً `./app` ڈائریکٹری کے بغیر `main.py`، تو آپ کا فائل ڈھانچہ کچھ ایسا ہو سکتا ہے:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

پھر آپ کو بس `Dockerfile` کے اندر فائل کاپی کرنے کے متعلقہ راستے تبدیل کرنے ہوں گے:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. `main.py` فائل کو `/code` ڈائریکٹری میں براہ راست کاپی کریں (بغیر `./app` ڈائریکٹری کے)۔

2. اپنی واحد فائل `main.py` میں ایپلیکیشن چلانے کے لیے `fastapi run` استعمال کریں۔

جب آپ `fastapi run` کو فائل دیتے ہیں تو یہ خود بخود پتا لگا لے گا کہ یہ واحد فائل ہے نہ کہ کسی package کا حصہ اور جانے گا کہ اسے کیسے import کرنا ہے اور آپ کی FastAPI app کو خدمت فراہم کرنی ہے۔ 😎

## Deployment کے تصورات { #deployment-concepts }

آئیے containers کے حوالے سے انہی [Deployment تصورات](concepts.md) کے بارے میں دوبارہ بات کرتے ہیں۔

Containers بنیادی طور پر ایپلیکیشن **بنانے اور deploy کرنے** کے عمل کو آسان بنانے کا ایک ٹول ہیں، لیکن یہ ان **deployment تصورات** کو سنبھالنے کا کوئی خاص طریقہ نافذ نہیں کرتے، اور کئی ممکنہ حکمت عملیاں ہیں۔

**اچھی خبر** یہ ہے کہ ہر مختلف حکمت عملی کے ساتھ تمام deployment تصورات کا احاطہ کرنے کا ایک طریقہ موجود ہے۔ 🎉

آئیے containers کے حوالے سے ان **deployment تصورات** کا جائزہ لیتے ہیں:

* HTTPS
* شروع ہونے پر چلنا
* دوبارہ شروع ہونا
* نقل (چلنے والے processes کی تعداد)
* میموری
* شروع ہونے سے پہلے کے مراحل

## HTTPS { #https }

اگر ہم صرف FastAPI ایپلیکیشن کے لیے **container image** (اور بعد میں چلنے والے **container**) پر توجہ مرکوز کریں، تو HTTPS عام طور پر ایک اور ٹول کے ذریعے **بیرونی طور پر** سنبھالا جائے گا۔

یہ ایک اور container ہو سکتا ہے، مثلاً [Traefik](https://traefik.io/) کے ساتھ، **HTTPS** اور **certificates** کے **خودکار** حصول کو سنبھالتے ہوئے۔

/// tip | مشورہ

Traefik کے Docker، Kubernetes اور دوسروں کے ساتھ integrations ہیں، تو اس کے ساتھ اپنے containers کے لیے HTTPS ترتیب دینا بہت آسان ہے۔

///

متبادل کے طور پر، HTTPS ایک cloud provider کے ذریعے ان کی خدمات میں سے ایک کے طور پر سنبھالا جا سکتا ہے (جبکہ ابھی بھی ایپلیکیشن container میں چل رہی ہو)۔

## شروع ہونے پر چلنا اور دوبارہ شروع ہونا { #running-on-startup-and-restarts }

عام طور پر آپ کے container کو **شروع اور چلانے** کا ذمہ دار ایک اور ٹول ہوتا ہے۔

یہ **Docker** براہ راست ہو سکتا ہے، **Docker Compose**، **Kubernetes**، کوئی **cloud service** وغیرہ۔

زیادہ تر (یا تمام) معاملات میں، شروع ہونے پر container چلانے اور ناکامیوں پر دوبارہ شروع کرنے کو فعال کرنے کا ایک آسان اختیار ہوتا ہے۔ مثلاً Docker میں، یہ command line اختیار `--restart` ہے۔

بغیر containers کے، ایپلیکیشنز کو شروع ہونے پر چلانا اور دوبارہ شروع کرنا مشکل اور پیچیدہ ہو سکتا ہے۔ لیکن جب **containers کے ساتھ** کام کر رہے ہوں تو زیادہ تر معاملات میں یہ فعالیت بطور ڈیفالٹ شامل ہوتی ہے۔ ✨

## نقل - Processes کی تعداد { #replication-number-of-processes }

اگر آپ کے پاس **Kubernetes**، Docker Swarm Mode، Nomad، یا متعدد مشینوں پر تقسیم شدہ containers منظم کرنے کے لیے کوئی اور ملتا جلتا پیچیدہ نظام والی مشینوں کا <dfn title="A group of machines that are configured to be connected and work together in some way.">cluster</dfn> ہے، تو آپ شاید ہر container میں **process manager** (جیسے Uvicorn with workers) استعمال کرنے کے بجائے **cluster کی سطح** پر **نقل سنبھالنا** چاہیں گے۔

ان تقسیم شدہ container management systems جیسے Kubernetes میں عام طور پر آنے والی requests کے لیے **load balancing** کی حمایت کرتے ہوئے **containers کی نقل** سنبھالنے کا کوئی مربوط طریقہ ہوتا ہے۔ سب **cluster کی سطح** پر۔

ان معاملات میں، آپ شاید [اوپر بیان کیے گئے طریقے](#dockerfile) سے **شروع سے Docker image** بنانا چاہیں گے، اپنی dependencies انسٹال کرتے ہوئے، اور متعدد Uvicorn workers استعمال کرنے کے بجائے **ایک واحد Uvicorn process** چلاتے ہوئے۔

### Load Balancer { #load-balancer }

Containers استعمال کرتے وقت، عام طور پر کوئی جزو **مرکزی port پر سن** رہا ہوتا ہے۔ یہ ممکنہ طور پر ایک اور container ہو سکتا ہے جو **HTTPS** سنبھالنے کے لیے **TLS Termination Proxy** بھی ہو یا کوئی ملتا جلتا ٹول۔

چونکہ یہ جزو requests کا **بوجھ** لیتا ہے اور اسے workers میں (امید ہے) **متوازن** طریقے سے تقسیم کرتا ہے، اسے عام طور پر **Load Balancer** بھی کہا جاتا ہے۔

/// tip | مشورہ

HTTPS کے لیے استعمال ہونے والا وہی **TLS Termination Proxy** جزو شاید **Load Balancer** بھی ہوگا۔

///

اور containers کے ساتھ کام کرتے وقت، وہی نظام جو آپ انہیں شروع اور منظم کرنے کے لیے استعمال کرتے ہیں اس میں پہلے سے اندرونی ٹولز ہوں گے جو **نیٹ ورک مواصلت** (مثلاً HTTP requests) اس **load balancer** (جو **TLS Termination Proxy** بھی ہو سکتا ہے) سے آپ کی app والے container(s) تک منتقل کریں۔

### ایک Load Balancer - متعدد Worker Containers { #one-load-balancer-multiple-worker-containers }

**Kubernetes** یا اسی طرح کے تقسیم شدہ container management systems کے ساتھ کام کرتے وقت، ان کے اندرونی نیٹ ورکنگ میکانزم کا استعمال واحد **load balancer** کو جو مرکزی **port** پر سن رہا ہے، مواصلت (requests) ممکنہ طور پر آپ کی app چلانے والے **متعدد containers** تک منتقل کرنے کی اجازت دے گا۔

آپ کی app چلانے والے ان میں سے ہر container میں عام طور پر **صرف ایک process** ہوگا (مثلاً آپ کی FastAPI ایپلیکیشن چلانے والا Uvicorn process)۔ وہ سب **ایک جیسے containers** ہوں گے، وہی چیز چلا رہے ہوں گے، لیکن ہر ایک اپنے process، میموری وغیرہ کے ساتھ۔ اس طرح آپ CPU کے **مختلف cores** میں، یا حتیٰ کہ **مختلف مشینوں** میں **متوازی عمل** سے فائدہ اٹھائیں گے۔

اور **load balancer** والا تقسیم شدہ container system آپ کی app والے ہر container کو **باری باری** requests **تقسیم کرے** گا۔ تو، ہر request آپ کی app چلانے والے متعدد **نقل شدہ containers** میں سے ایک کے ذریعے سنبھالی جا سکتی ہے۔

اور عام طور پر یہ **load balancer** آپ کے cluster میں *دوسری* apps (مثلاً مختلف domain، یا مختلف URL path prefix کے تحت) کی طرف جانے والی requests بھی سنبھال سکے گا، اور وہ مواصلت آپ کے cluster میں چلنے والی *اس دوسری* ایپلیکیشن کے صحیح containers تک منتقل کرے گا۔

### فی Container ایک Process { #one-process-per-container }

اس قسم کے منظرنامے میں، آپ شاید **فی container ایک واحد (Uvicorn) process** رکھنا چاہیں گے، کیونکہ آپ پہلے ہی cluster کی سطح پر نقل سنبھال رہے ہوں گے۔

تو، اس صورت میں، آپ container میں متعدد workers **نہیں** رکھنا چاہیں گے، مثلاً `--workers` command line اختیار کے ساتھ۔ آپ فی container صرف ایک **واحد Uvicorn process** رکھنا چاہیں گے (لیکن شاید متعدد containers)۔

Container کے اندر ایک اور process manager رکھنا (جیسا کہ متعدد workers کے ساتھ ہوگا) صرف **غیر ضروری پیچیدگی** شامل کرے گا جو آپ شاید پہلے ہی اپنے cluster system سے سنبھال رہے ہیں۔

### متعدد Processes والے Containers اور خصوصی صورتیں { #containers-with-multiple-processes-and-special-cases }

یقیناً، ایسی **خصوصی صورتیں** ہیں جہاں آپ ایک **container** میں اندر کئی **Uvicorn worker processes** رکھنا چاہ سکتے ہیں۔

ان معاملات میں، آپ workers کی تعداد مقرر کرنے کے لیے `--workers` command line اختیار استعمال کر سکتے ہیں:

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. یہاں ہم workers کی تعداد 4 مقرر کرنے کے لیے `--workers` command line اختیار استعمال کرتے ہیں۔

یہاں کچھ مثالیں ہیں کہ یہ کب معنی خیز ہو سکتا ہے:

#### ایک سادہ App { #a-simple-app }

اگر آپ کی ایپلیکیشن **اتنی سادہ** ہے کہ اسے **ایک واحد server** پر چلایا جا سکتا ہے، cluster نہیں، تو آپ container میں process manager رکھنا چاہ سکتے ہیں۔

#### Docker Compose { #docker-compose }

آپ **Docker Compose** کے ساتھ **ایک واحد server** (cluster نہیں) پر deploy کر رہے ہو سکتے ہیں، تو آپ کے پاس مشترکہ نیٹ ورک اور **load balancing** کو برقرار رکھتے ہوئے containers کی نقل منظم کرنے کا آسان طریقہ نہ ہو (Docker Compose کے ساتھ)۔

تب آپ **ایک واحد container** میں **process manager** کے ساتھ اندر **کئی worker processes** شروع کرنا چاہ سکتے ہیں۔

---

اصل بات یہ ہے کہ ان میں سے **کوئی بھی** ایسے **پتھر پر لکھے قوانین** نہیں ہیں جن کی آپ کو آنکھیں بند کر کے پیروی کرنی ہے۔ آپ ان خیالات کو **اپنے استعمال کے معاملے کا جائزہ لینے** اور اپنے نظام کے لیے بہترین طریقہ فیصلہ کرنے کے لیے استعمال کر سکتے ہیں، یہ دیکھتے ہوئے کہ ان تصورات کو کیسے منظم کریں:

* سیکیورٹی - HTTPS
* شروع ہونے پر چلنا
* دوبارہ شروع ہونا
* نقل (چلنے والے processes کی تعداد)
* میموری
* شروع ہونے سے پہلے کے مراحل

## میموری { #memory }

اگر آپ **فی container ایک واحد process** چلاتے ہیں تو ان میں سے ہر container (اگر نقل شدہ ہیں تو ایک سے زیادہ) کے ذریعے استعمال ہونے والی میموری کم و بیش واضح، مستحکم اور محدود ہوگی۔

اور پھر آپ اپنے container management system (مثلاً **Kubernetes** میں) کی ترتیبات میں وہی میموری کی حدود اور ضروریات مقرر کر سکتے ہیں۔ اس طرح یہ ان کی ضرورت کی میموری کی مقدار اور cluster کی مشینوں میں دستیاب مقدار کو مدنظر رکھتے ہوئے **دستیاب مشینوں** میں **containers کی نقل** کر سکے گا۔

اگر آپ کی ایپلیکیشن **سادہ** ہے، تو یہ شاید **مسئلہ نہیں** ہوگا، اور آپ کو سخت میموری کی حدود مقرر کرنے کی ضرورت نہیں ہوگی۔ لیکن اگر آپ **بہت زیادہ میموری استعمال** کر رہے ہیں (مثلاً **machine learning** ماڈلز کے ساتھ)، تو آپ کو چیک کرنا چاہیے کہ آپ کتنی میموری استعمال کر رہے ہیں اور **ہر مشین** میں چلنے والے **containers کی تعداد** کو ایڈجسٹ کرنا چاہیے (اور شاید اپنے cluster میں مزید مشینیں شامل کریں)۔

اگر آپ **فی container متعدد processes** چلاتے ہیں تو آپ کو یقینی بنانا ہوگا کہ شروع ہونے والے processes کی تعداد دستیاب سے **زیادہ میموری استعمال** نہ کرے۔

## شروع ہونے سے پہلے کے مراحل اور Containers { #previous-steps-before-starting-and-containers }

اگر آپ containers (مثلاً Docker، Kubernetes) استعمال کر رہے ہیں تو دو اصل طریقے ہیں جو آپ استعمال کر سکتے ہیں۔

### متعدد Containers { #multiple-containers }

اگر آپ کے پاس **متعدد containers** ہیں، شاید ہر ایک **واحد process** چلا رہا ہے (مثلاً **Kubernetes** cluster میں)، تو آپ شاید نقل شدہ worker containers چلانے **سے پہلے** ایک **الگ container** میں **پچھلے مراحل** کا کام ایک واحد container میں، ایک واحد process چلاتے ہوئے کرنا چاہیں گے۔

/// info | معلومات

اگر آپ Kubernetes استعمال کر رہے ہیں، تو یہ شاید ایک [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) ہوگا۔

///

اگر آپ کے استعمال کے معاملے میں ان پچھلے مراحل کو **متعدد بار متوازی طور پر** چلانے میں کوئی مسئلہ نہیں ہے (مثلاً اگر آپ database migrations نہیں چلا رہے، بلکہ صرف چیک کر رہے ہیں کہ ڈیٹابیس تیار ہے یا نہیں)، تو آپ انہیں مرکزی process شروع کرنے سے پہلے ہر container میں بھی رکھ سکتے ہیں۔

### واحد Container { #single-container }

اگر آپ کے پاس سادہ سیٹ اپ ہے، **واحد container** کے ساتھ جو پھر متعدد **worker processes** شروع کرتا ہے (یا صرف ایک process بھی)، تو آپ ان پچھلے مراحل کو اسی container میں، app کے ساتھ process شروع کرنے سے پہلے چلا سکتے ہیں۔

### بنیادی Docker Image { #base-docker-image }

پہلے ایک سرکاری FastAPI Docker image ہوا کرتی تھی: [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)۔ لیکن اب یہ متروک ہے۔ ⛔️

آپ کو شاید یہ بنیادی Docker image (یا کوئی اور ایسی ہی) استعمال **نہیں** کرنی چاہیے۔

اگر آپ **Kubernetes** (یا دوسرے) استعمال کر رہے ہیں اور پہلے سے متعدد **containers** کے ساتھ cluster کی سطح پر **نقل** ترتیب دے رہے ہیں۔ ان معاملات میں، آپ اوپر بیان کیے گئے طریقے سے **شروع سے image بنانا** بہتر ہے: [FastAPI کے لیے Docker Image بنائیں](#build-a-docker-image-for-fastapi)۔

اور اگر آپ کو متعدد workers کی ضرورت ہے تو آپ آسانی سے `--workers` command line اختیار استعمال کر سکتے ہیں۔

/// note | تکنیکی تفصیلات

Docker image اس وقت بنائی گئی تھی جب Uvicorn مردہ workers کو منظم اور دوبارہ شروع کرنے کی حمایت نہیں کرتا تھا، تو Gunicorn کو Uvicorn کے ساتھ استعمال کرنا ضروری تھا، جس نے کافی پیچیدگی شامل کی، صرف اس لیے کہ Gunicorn Uvicorn worker processes کو منظم اور دوبارہ شروع کر سکے۔

لیکن اب جب Uvicorn (اور `fastapi` command) `--workers` استعمال کرنے کی حمایت کرتا ہے، اپنی خود کی بنانے کے بجائے بنیادی Docker image استعمال کرنے کی کوئی وجہ نہیں ہے (یہ تقریباً اتنا ہی کوڈ ہے 😅)۔

///

## Container Image Deploy کریں { #deploy-the-container-image }

Container (Docker) Image ہونے کے بعد اسے deploy کرنے کے کئی طریقے ہیں۔

مثال کے طور پر:

* واحد server پر **Docker Compose** کے ساتھ
* **Kubernetes** cluster کے ساتھ
* Docker Swarm Mode cluster کے ساتھ
* Nomad جیسے دوسرے ٹول کے ساتھ
* cloud service کے ساتھ جو آپ کی container image لے کر deploy کرے

## `uv` کے ساتھ Docker Image { #docker-image-with-uv }

اگر آپ اپنا پراجیکٹ انسٹال اور منظم کرنے کے لیے [uv](https://github.com/astral-sh/uv) استعمال کر رہے ہیں، تو آپ ان کی [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/) کی پیروی کر سکتے ہیں۔

## خلاصہ { #recap }

Container systems (مثلاً **Docker** اور **Kubernetes** کے ساتھ) استعمال کرنا تمام **deployment تصورات** کو سنبھالنا کافی سیدھا بنا دیتا ہے:

* HTTPS
* شروع ہونے پر چلنا
* دوبارہ شروع ہونا
* نقل (چلنے والے processes کی تعداد)
* میموری
* شروع ہونے سے پہلے کے مراحل

زیادہ تر معاملات میں، آپ شاید کوئی بنیادی image استعمال نہیں کرنا چاہیں گے، بلکہ سرکاری Python Docker image کی بنیاد پر **شروع سے container image بنائیں** گے۔

`Dockerfile` میں ہدایات کی **ترتیب** اور **Docker cache** کا خیال رکھ کر آپ اپنی پیداواریت بڑھانے (اور اکتاہٹ سے بچنے) کے لیے **build time کم** کر سکتے ہیں۔ 😎
