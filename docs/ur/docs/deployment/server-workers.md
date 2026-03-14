# Server Workers - Uvicorn with Workers { #server-workers-uvicorn-with-workers }

آئیے پہلے سے ان deployment تصورات کو دوبارہ دیکھتے ہیں:

* سیکیورٹی - HTTPS
* شروع ہونے پر چلنا
* دوبارہ شروع ہونا
* **نقل (چلنے والے processes کی تعداد)**
* میموری
* شروع ہونے سے پہلے کے مراحل

اب تک، دستاویزات کے تمام ٹیوٹوریلز کے ساتھ، آپ شاید ایک **server پروگرام** چلا رہے تھے، مثلاً `fastapi` command استعمال کرتے ہوئے جو Uvicorn چلاتا ہے، ایک **واحد process** میں۔

ایپلیکیشنز deploy کرتے وقت آپ شاید **متعدد cores** سے فائدہ اٹھانے اور زیادہ requests سنبھالنے کے لیے **processes کی نقل** رکھنا چاہیں گے۔

جیسا کہ آپ نے [Deployment تصورات](concepts.md) کے پچھلے باب میں دیکھا، اس کے لیے متعدد حکمت عملیاں ہیں۔

یہاں میں آپ کو دکھاؤں گا کہ `fastapi` command یا `uvicorn` command براہ راست استعمال کرتے ہوئے **worker processes** کے ساتھ **Uvicorn** کیسے استعمال کریں۔

/// info | معلومات

اگر آپ containers استعمال کر رہے ہیں، مثلاً Docker یا Kubernetes کے ساتھ، تو میں اگلے باب میں اس کے بارے میں مزید بتاؤں گا: [FastAPI in Containers - Docker](docker.md)۔

خاص طور پر، **Kubernetes** پر چلاتے وقت آپ شاید workers استعمال **نہیں** کرنا چاہیں گے بلکہ **ہر container میں ایک واحد Uvicorn process** چلائیں گے، لیکن میں اس کے بارے میں اس باب میں بعد میں بتاؤں گا۔

///

## متعدد Workers { #multiple-workers }

آپ `--workers` command line اختیار کے ساتھ متعدد workers شروع کر سکتے ہیں:

//// tab | `fastapi`

اگر آپ `fastapi` command استعمال کرتے ہیں:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

اگر آپ `uvicorn` command براہ راست استعمال کرنا چاہیں:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

یہاں واحد نیا اختیار `--workers` ہے جو Uvicorn کو 4 worker processes شروع کرنے کو کہتا ہے۔

آپ یہ بھی دیکھ سکتے ہیں کہ یہ ہر process کا **PID** دکھاتا ہے، parent process (یہ **process manager** ہے) کے لیے `27365` اور ہر worker process کے لیے ایک: `27368`، `27369`، `27370`، اور `27367`۔

## Deployment کے تصورات { #deployment-concepts }

یہاں آپ نے دیکھا کہ ایپلیکیشن کے عمل کو **متوازی** بنانے، CPU میں **متعدد cores** سے فائدہ اٹھانے، اور **زیادہ requests** فراہم کرنے کے قابل ہونے کے لیے متعدد **workers** کیسے استعمال کریں۔

اوپر کی deployment تصورات کی فہرست سے، workers استعمال کرنا بنیادی طور پر **نقل** کے حصے میں مدد کرے گا، اور تھوڑا سا **دوبارہ شروع ہونے** میں، لیکن آپ کو ابھی بھی باقیوں کا خیال رکھنا ہوگا:

* **سیکیورٹی - HTTPS**
* **شروع ہونے پر چلنا**
* ***دوبارہ شروع ہونا***
* نقل (چلنے والے processes کی تعداد)
* **میموری**
* **شروع ہونے سے پہلے کے مراحل**

## Containers اور Docker { #containers-and-docker }

[FastAPI in Containers - Docker](docker.md) کے بارے میں اگلے باب میں میں آپ کو کچھ حکمت عملیاں بتاؤں گا جو آپ دوسرے **deployment تصورات** سنبھالنے کے لیے استعمال کر سکتے ہیں۔

میں آپ کو دکھاؤں گا کہ ایک واحد Uvicorn process چلانے کے لیے **شروع سے اپنی خود کی image کیسے بنائیں**۔ یہ ایک آسان عمل ہے اور شاید یہی وہ چیز ہے جو آپ **Kubernetes** جیسے تقسیم شدہ container management system استعمال کرتے وقت کرنا چاہیں گے۔

## خلاصہ { #recap }

آپ **multi-core CPUs** سے فائدہ اٹھانے اور **متوازی طور پر متعدد processes** چلانے کے لیے `fastapi` یا `uvicorn` commands کے ساتھ `--workers` CLI اختیار استعمال کر سکتے ہیں۔

آپ ان ٹولز اور خیالات کو استعمال کر سکتے ہیں اگر آپ خود deployment تصورات کا خیال رکھتے ہوئے **اپنا خود کا deployment system** ترتیب دے رہے ہیں۔

containers (مثلاً Docker اور Kubernetes) کے ساتھ **FastAPI** کے بارے میں جاننے کے لیے اگلا باب دیکھیں۔ آپ دیکھیں گے کہ ان ٹولز میں دوسرے **deployment تصورات** کو بھی حل کرنے کے آسان طریقے ہیں۔ ✨
