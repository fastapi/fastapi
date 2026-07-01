# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - कमांड लाइन इंटरफ़ेस">CLI</abbr>** एक command line program है जिसका उपयोग आप अपनी FastAPI app को serve करने, अपने FastAPI project को manage करने, और भी बहुत कुछ करने के लिए कर सकते हैं।

जब आप FastAPI install करते हैं (जैसे `pip install "fastapi[standard]"` के साथ), तो इसके साथ एक command line program आता है जिसे आप terminal में run कर सकते हैं।

Development के लिए अपनी FastAPI app run करने के लिए, आप `fastapi dev` command का उपयोग कर सकते हैं:

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

/// tip | सुझाव

Production के लिए आप `fastapi dev` के बजाय `fastapi run` का उपयोग करेंगे। 🚀

///

Internally, **FastAPI CLI** [Uvicorn](https://www.uvicorn.dev), एक high-performance, production-ready, ASGI server का उपयोग करता है। 😎

`fastapi` CLI run करने के लिए FastAPI app को automatically detect करने की कोशिश करेगा, यह मानते हुए कि यह `main.py` file में `app` नाम का object है (या कुछ अन्य variants में से कोई एक)।

लेकिन आप उपयोग की जाने वाली app को स्पष्ट रूप से configure कर सकते हैं।

## `pyproject.toml` में app `entrypoint` configure करें { #configure-the-app-entrypoint-in-pyproject-toml }

आप `pyproject.toml` file में अपनी app कहाँ स्थित है, इसे इस तरह configure कर सकते हैं:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

वह `entrypoint` `fastapi` command को बताएगा कि उसे app को इस तरह import करना चाहिए:

```python
from main import app
```

यदि आपका code इस तरह structured था:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

तो आप `entrypoint` को इस तरह set करेंगे:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

जो इसके equivalent होगा:

```python
from backend.main import app
```

### Path के साथ या `--entrypoint` CLI option के साथ `fastapi dev` { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

आप file path को `fastapi dev` command में भी pass कर सकते हैं, और यह उपयोग करने के लिए FastAPI app object का अनुमान लगा लेगा:

```console
$ fastapi dev main.py
```

या, आप `--entrypoint` option को `fastapi dev` command में भी pass कर सकते हैं:

```console
$ fastapi dev --entrypoint main:app
```

लेकिन जब भी आप `fastapi` command call करें, तो आपको हर बार सही path\entrypoint pass करना याद रखना होगा।

इसके अलावा, अन्य tools शायद इसे find न कर पाएं, उदाहरण के लिए [VS Code Extension](editor-support.md) या [FastAPI Cloud](https://fastapicloud.com), इसलिए `pyproject.toml` में `entrypoint` का उपयोग करने की सलाह दी जाती है।

## `fastapi dev` { #fastapi-dev }

`fastapi dev` run करने से development mode शुरू होता है।

Default रूप से, **auto-reload** enabled होता है, जब आप अपने code में changes करते हैं तो server automatically reload हो जाता है। यह resource-intensive है और disabled होने की तुलना में कम stable हो सकता है। आपको इसे केवल development के लिए use करना चाहिए। यह IP address `127.0.0.1` पर भी listen करता है, जो आपकी machine के खुद से ही (`localhost`) communicate करने के लिए IP है।

## `fastapi run` { #fastapi-run }

`fastapi run` execute करने से FastAPI production mode में start होता है।

Default रूप से, **auto-reload** disabled होता है। यह IP address `0.0.0.0` पर भी listen करता है, जिसका मतलब है सभी available IP addresses; इस तरह यह machine से communicate कर सकने वाले किसी भी व्यक्ति के लिए publicly accessible होगा। सामान्यतः आप production में इसे इसी तरह run करेंगे, उदाहरण के लिए, किसी container में।

अधिकांश cases में आपके पास ऊपर HTTPS handle करने वाला एक "termination proxy" होगा (और होना चाहिए), यह इस बात पर depend करेगा कि आप अपनी application कैसे deploy करते हैं; आपका provider आपके लिए यह कर सकता है, या आपको इसे खुद set up करना पड़ सकता है।

/// tip | सुझाव

आप इसके बारे में [deployment documentation](deployment/index.md) में अधिक जान सकते हैं।

///
