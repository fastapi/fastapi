# Server کو دستی طور پر چلائیں { #run-a-server-manually }

## `fastapi run` Command استعمال کریں { #use-the-fastapi-run-command }

مختصراً، اپنی FastAPI ایپلیکیشن کو چلانے کے لیے `fastapi run` استعمال کریں:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

یہ زیادہ تر معاملات میں کام کرے گا۔ 😎

آپ اس command کو مثلاً اپنی **FastAPI** app کو container میں، server میں وغیرہ شروع کرنے کے لیے استعمال کر سکتے ہیں۔

## ASGI Servers { #asgi-servers }

آئیے تفصیلات میں تھوڑا گہرائی میں جائیں۔

FastAPI ایک معیار استعمال کرتا ہے جو Python web frameworks اور servers بنانے کے لیے ہے جسے <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr> کہتے ہیں۔ FastAPI ایک ASGI web framework ہے۔

remote server machine پر **FastAPI** ایپلیکیشن (یا کوئی بھی ASGI ایپلیکیشن) چلانے کے لیے آپ کو بنیادی طور پر ایک ASGI server پروگرام جیسے **Uvicorn** کی ضرورت ہے، یہ وہ ہے جو `fastapi` command میں بطور ڈیفالٹ آتا ہے۔

کئی متبادل ہیں، بشمول:

* [Uvicorn](https://www.uvicorn.dev/): ایک اعلیٰ کارکردگی والا ASGI server۔
* [Hypercorn](https://hypercorn.readthedocs.io/): HTTP/2 اور Trio کے ساتھ ہم آہنگ ایک ASGI server اور دیگر خصوصیات۔
* [Daphne](https://github.com/django/daphne): Django Channels کے لیے بنایا گیا ASGI server۔
* [Granian](https://github.com/emmett-framework/granian): Python ایپلیکیشنز کے لیے ایک Rust HTTP server۔
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit ایک ہلکا اور ورسٹائل web application runtime ہے۔

## Server Machine اور Server Program { #server-machine-and-server-program }

ناموں کے بارے میں ایک چھوٹی سی بات ذہن میں رکھنے کی ہے۔ 💡

"**server**" کا لفظ عام طور پر remote/cloud کمپیوٹر (فزیکل یا virtual machine) اور اس مشین پر چلنے والے پروگرام (مثلاً Uvicorn) دونوں کے لیے استعمال ہوتا ہے۔

بس ذہن میں رکھیں کہ جب آپ عمومی طور پر "server" پڑھیں تو اس سے ان دو چیزوں میں سے کوئی ایک مراد ہو سکتی ہے۔

remote machine کا حوالہ دیتے وقت، اسے عام طور پر **server** کہا جاتا ہے، لیکن **machine**، **VM** (virtual machine)، **node** بھی کہتے ہیں۔ یہ سب کسی قسم کی remote machine کا حوالہ دیتے ہیں، عام طور پر Linux چلاتی ہوئی، جہاں آپ پروگرامز چلاتے ہیں۔

## Server Program انسٹال کریں { #install-the-server-program }

جب آپ FastAPI انسٹال کرتے ہیں، تو یہ ایک production server، Uvicorn، کے ساتھ آتا ہے، اور آپ اسے `fastapi run` command سے شروع کر سکتے ہیں۔

لیکن آپ ASGI server کو دستی طور پر بھی انسٹال کر سکتے ہیں۔

اس بات کو یقینی بنائیں کہ آپ [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر آپ server ایپلیکیشن انسٹال کر سکتے ہیں۔

مثال کے طور پر، Uvicorn انسٹال کرنے کے لیے:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

کسی بھی دوسرے ASGI server پروگرام پر بھی اسی طرح کا عمل لاگو ہوگا۔

/// tip | مشورہ

`standard` شامل کرنے سے، Uvicorn کچھ تجویز کردہ اضافی dependencies انسٹال اور استعمال کرے گا۔

اس میں `uvloop` شامل ہے، `asyncio` کا اعلیٰ کارکردگی والا متبادل، جو بڑی concurrency کارکردگی میں اضافہ فراہم کرتا ہے۔

جب آپ FastAPI کو `pip install "fastapi[standard]"` جیسی کسی چیز سے انسٹال کرتے ہیں تو آپ کو `uvicorn[standard]` بھی مل جاتا ہے۔

///

## Server Program چلائیں { #run-the-server-program }

اگر آپ نے ASGI server دستی طور پر انسٹال کیا ہے، تو آپ کو عام طور پر اپنی FastAPI ایپلیکیشن import کرنے کے لیے ایک خاص فارمیٹ میں import string دینی ہوگی:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | نوٹ

`uvicorn main:app` command کا مطلب ہے:

* `main`: فائل `main.py` (Python "module")۔
* `app`: وہ آبجیکٹ جو `main.py` کے اندر `app = FastAPI()` لائن سے بنایا گیا۔

یہ اس کے مساوی ہے:

```Python
from main import app
```

///

ہر متبادل ASGI server پروگرام کی ایک مماثل command ہوگی، آپ ان کی متعلقہ دستاویزات میں مزید پڑھ سکتے ہیں۔

/// warning | انتباہ

Uvicorn اور دوسرے servers ایک `--reload` اختیار فراہم کرتے ہیں جو development کے دوران مفید ہے۔

`--reload` اختیار بہت زیادہ وسائل استعمال کرتا ہے، زیادہ غیر مستحکم ہے، وغیرہ۔

یہ **development** کے دوران بہت مدد کرتا ہے، لیکن آپ کو **production** میں اسے استعمال **نہیں کرنا** چاہیے۔

///

## Deployment کے تصورات { #deployment-concepts }

یہ مثالیں server پروگرام (مثلاً Uvicorn) کو **ایک واحد process** شروع کرتے ہوئے چلاتی ہیں، تمام IPs (`0.0.0.0`) پر ایک پہلے سے طے شدہ port (مثلاً `80`) پر سنتے ہوئے۔

یہ بنیادی خیال ہے۔ لیکن آپ شاید کچھ اضافی چیزوں کا خیال رکھنا چاہیں گے، جیسے:

* سیکیورٹی - HTTPS
* شروع ہونے پر چلنا
* دوبارہ شروع ہونا
* نقل (چلنے والے processes کی تعداد)
* میموری
* شروع ہونے سے پہلے کے مراحل

میں آپ کو اگلے ابواب میں ان میں سے ہر تصور کے بارے میں مزید بتاؤں گا، ان کے بارے میں سوچنے کا طریقہ، اور انہیں سنبھالنے کی حکمت عملیوں کی کچھ ٹھوس مثالیں۔ 🚀
