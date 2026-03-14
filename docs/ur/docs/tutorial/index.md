# ٹیوٹوریل - صارف گائیڈ { #tutorial-user-guide }

یہ ٹیوٹوریل آپ کو **FastAPI** کی زیادہ تر خصوصیات کے ساتھ قدم بہ قدم استعمال کرنا سکھاتا ہے۔

ہر حصہ پچھلے حصوں پر بتدریج بنتا ہے، لیکن یہ موضوعات کے لحاظ سے الگ الگ ترتیب دیا گیا ہے، تاکہ آپ اپنی مخصوص API ضروریات کو پورا کرنے کے لیے براہ راست کسی بھی مخصوص حصے پر جا سکیں۔

یہ مستقبل کے حوالے کے طور پر بھی کام کرنے کے لیے بنایا گیا ہے تاکہ آپ واپس آ کر بالکل وہی دیکھ سکیں جو آپ کو چاہیے۔

## کوڈ چلائیں { #run-the-code }

تمام کوڈ بلاکس کو کاپی کر کے براہ راست استعمال کیا جا سکتا ہے (یہ دراصل ٹیسٹ شدہ Python فائلیں ہیں)۔

کوئی بھی مثال چلانے کے لیے، کوڈ کو `main.py` فائل میں کاپی کریں، اور `fastapi dev` شروع کریں:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

آپ سے **انتہائی گزارش** ہے کہ کوڈ لکھیں یا کاپی کریں، اسے ایڈٹ کریں اور مقامی طور پر چلائیں۔

اسے اپنے ایڈیٹر میں استعمال کرنے سے آپ کو FastAPI کے فوائد واقعی نظر آئیں گے، جیسے کہ کتنا کم کوڈ لکھنا پڑتا ہے، تمام type checks، autocompletion وغیرہ۔

---

## FastAPI انسٹال کریں { #install-fastapi }

پہلا قدم FastAPI انسٹال کرنا ہے۔

یقینی بنائیں کہ آپ ایک [virtual environment](../virtual-environments.md) بنائیں، اسے فعال کریں، اور پھر **FastAPI انسٹال کریں**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | نوٹ

جب آپ `pip install "fastapi[standard]"` کے ساتھ انسٹال کرتے ہیں تو یہ کچھ پہلے سے طے شدہ اختیاری معیاری dependencies کے ساتھ آتا ہے، بشمول `fastapi-cloud-cli`، جو آپ کو [FastAPI Cloud](https://fastapicloud.com) پر deploy کرنے کی اجازت دیتا ہے۔

اگر آپ وہ اختیاری dependencies نہیں چاہتے، تو آپ اس کی بجائے `pip install fastapi` انسٹال کر سکتے ہیں۔

اگر آپ معیاری dependencies چاہتے ہیں لیکن `fastapi-cloud-cli` کے بغیر، تو آپ `pip install "fastapi[standard-no-fastapi-cloud-cli]"` کے ساتھ انسٹال کر سکتے ہیں۔

///

/// tip | مشورہ

FastAPI کی [VS Code کے لیے سرکاری ایکسٹینشن](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) (اور Cursor) موجود ہے، جو بہت سی خصوصیات فراہم کرتی ہے، بشمول path operation ایکسپلورر، path operation تلاش، ٹیسٹس میں CodeLens نیویگیشن (ٹیسٹس سے ڈیفینیشن پر جائیں)، اور FastAPI Cloud deployment اور لاگز، سب کچھ آپ کے ایڈیٹر سے۔

///

## ایڈوانسڈ صارف گائیڈ { #advanced-user-guide }

ایک **ایڈوانسڈ صارف گائیڈ** بھی ہے جسے آپ اس **ٹیوٹوریل - صارف گائیڈ** کے بعد پڑھ سکتے ہیں۔

**ایڈوانسڈ صارف گائیڈ** اسی پر بنتا ہے، انہی تصورات کو استعمال کرتا ہے، اور آپ کو کچھ اضافی خصوصیات سکھاتا ہے۔

لیکن آپ کو پہلے **ٹیوٹوریل - صارف گائیڈ** (جو آپ ابھی پڑھ رہے ہیں) پڑھنا چاہیے۔

یہ اس طرح ڈیزائن کیا گیا ہے کہ آپ صرف **ٹیوٹوریل - صارف گائیڈ** سے ایک مکمل ایپلیکیشن بنا سکتے ہیں، اور پھر اسے مختلف طریقوں سے بڑھا سکتے ہیں، اپنی ضروریات کے مطابق، **ایڈوانسڈ صارف گائیڈ** سے کچھ اضافی خیالات استعمال کر کے۔
