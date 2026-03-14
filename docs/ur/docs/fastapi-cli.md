# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface">CLI</abbr>** ایک command line program ہے جسے آپ اپنی FastAPI app serve کرنے، اپنا FastAPI project منظم کرنے، اور مزید کاموں کے لیے استعمال کر سکتے ہیں۔

جب آپ FastAPI install کرتے ہیں (مثلاً `pip install "fastapi[standard]"` سے)، تو یہ ایک command line program کے ساتھ آتا ہے جسے آپ terminal میں چلا سکتے ہیں۔

اپنی FastAPI app کو development کے لیے چلانے کے لیے، آپ `fastapi dev` command استعمال کر سکتے ہیں:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | مشورہ

Production کے لیے آپ `fastapi dev` کی بجائے `fastapi run` استعمال کریں گے۔ 🚀

///

اندرونی طور پر، **FastAPI CLI** [Uvicorn](https://www.uvicorn.dev) استعمال کرتا ہے، ایک اعلیٰ performance والا، production-ready، ASGI server۔ 😎

`fastapi` CLI خودکار طور پر چلانے والی FastAPI app کو detect کرنے کی کوشش کرے گا، یہ فرض کرتے ہوئے کہ یہ `main.py` فائل میں `app` نامی object ہے (یا کچھ دوسرے متبادل)۔

لیکن آپ واضح طور پر استعمال کرنے والی app configure کر سکتے ہیں۔

## `pyproject.toml` میں app کا `entrypoint` configure کریں { #configure-the-app-entrypoint-in-pyproject-toml }

آپ `pyproject.toml` فائل میں اپنی app کی جگہ configure کر سکتے ہیں جیسے:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

یہ `entrypoint`، `fastapi` command کو بتائے گا کہ اسے app اس طرح import کرنی چاہیے:

```python
from main import app
```

اگر آپ کا code اس طرح ترتیب دیا گیا ہے:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

تو آپ `entrypoint` اس طرح سیٹ کریں گے:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

جو اس کے مساوی ہوگا:

```python
from backend.main import app
```

### path کے ساتھ `fastapi dev` { #fastapi-dev-with-path }

آپ `fastapi dev` command کو فائل کا path بھی دے سکتے ہیں، اور یہ استعمال کرنے والی FastAPI app object کا اندازہ لگائے گا:

```console
$ fastapi dev main.py
```

لیکن آپ کو ہر بار `fastapi` command call کرتے وقت صحیح path یاد رکھنا ہوگا۔

اس کے علاوہ، دوسرے tools شاید اسے تلاش نہ کر سکیں، مثلاً [VS Code Extension](editor-support.md) یا [FastAPI Cloud](https://fastapicloud.com)، تو `pyproject.toml` میں `entrypoint` استعمال کرنا تجویز کیا جاتا ہے۔

## `fastapi dev` { #fastapi-dev }

`fastapi dev` چلانے سے development mode شروع ہوتا ہے۔

بطور default، **auto-reload** فعال ہوتا ہے، جب آپ اپنے code میں تبدیلیاں کرتے ہیں تو server خودکار طور پر دوبارہ لوڈ ہوتا ہے۔ یہ وسائل کا زیادہ استعمال کرتا ہے اور غیر فعال ہونے کی نسبت کم مستحکم ہو سکتا ہے۔ آپ کو اسے صرف development کے لیے استعمال کرنا چاہیے۔ یہ IP address `127.0.0.1` پر بھی سنتا ہے، جو آپ کی مشین کا خود سے بات چیت کرنے کا IP ہے (`localhost`)۔

## `fastapi run` { #fastapi-run }

`fastapi run` چلانے سے FastAPI production mode میں شروع ہوتا ہے۔

بطور default، **auto-reload** غیر فعال ہوتا ہے۔ یہ IP address `0.0.0.0` پر سنتا ہے، یعنی تمام دستیاب IP addresses، اس طرح یہ ہر اس شخص کے لیے عوامی طور پر قابل رسائی ہوگا جو مشین سے بات چیت کر سکتا ہے۔ عام طور پر آپ اسے production میں اسی طرح چلائیں گے، مثلاً container میں۔

زیادہ تر معاملات میں آپ کے پاس ایک "termination proxy" ہوگا جو آپ کے لیے HTTPS سنبھالتا ہے، یہ آپ کی application کو deploy کرنے کے طریقے پر منحصر ہے، آپ کا provider شاید یہ آپ کے لیے کرے، یا آپ کو خود سیٹ اپ کرنا ہوگا۔

/// tip | مشورہ

آپ اس کے بارے میں مزید [deployment documentation](deployment/index.md) میں سیکھ سکتے ہیں۔

///
