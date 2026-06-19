# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - कमांड लाइन इंटरफ़ेस">CLI</abbr>** एक command line प्रोग्राम है जिसका उपयोग आप अपने FastAPI ऐप को serve करने, अपने FastAPI प्रोजेक्ट को manage करने, और भी बहुत कुछ करने के लिए कर सकते हैं।

जब आप FastAPI इंस्टॉल करते हैं (जैसे `pip install "fastapi[standard]"` के साथ), तो इसके साथ एक command line प्रोग्राम आता है जिसे आप terminal में चला सकते हैं।

डेवलपमेंट के लिए अपना FastAPI ऐप चलाने के लिए, आप `fastapi dev` command का उपयोग कर सकते हैं:

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

प्रोडक्शन के लिए आप `fastapi dev` की जगह `fastapi run` का उपयोग करेंगे। 🚀

///

आंतरिक रूप से, **FastAPI CLI** [Uvicorn](https://www.uvicorn.dev) का उपयोग करता है, जो एक high-performance, production-ready, ASGI server है। 😎

`fastapi` CLI चलाने के लिए FastAPI ऐप को अपने-आप detect करने की कोशिश करेगा, यह मानते हुए कि यह `main.py` फ़ाइल में `app` नाम का object है (या कुछ अन्य variants में से कोई एक)।

लेकिन आप उपयोग किए जाने वाले ऐप को स्पष्ट रूप से configure कर सकते हैं।

## ऐप `entrypoint` को `pyproject.toml` में configure करें { #configure-the-app-entrypoint-in-pyproject-toml }

आप `pyproject.toml` फ़ाइल में यह configure कर सकते हैं कि आपका ऐप कहाँ स्थित है, जैसे:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

वह `entrypoint` `fastapi` command को बताएगा कि उसे ऐप को इस तरह import करना चाहिए:

```python
from main import app
```

अगर आपका code इस तरह structured था:

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

जो इसके बराबर होगा:

```python
from backend.main import app
```

### path के साथ या `--entrypoint` CLI option के साथ `fastapi dev` { #fastapi-dev-with-path-or-with-entrypoint-cli-option }

आप `fastapi dev` command को file path भी pass कर सकते हैं, और यह उपयोग किए जाने वाले FastAPI app object का अनुमान लगा लेगा:

```console
$ fastapi dev main.py
```

या, आप `fastapi dev` command को `--entrypoint` option भी pass कर सकते हैं:

```console
$ fastapi dev --entrypoint main:app
```

लेकिन आपको हर बार `fastapi` command call करते समय सही path\entrypoint pass करना याद रखना होगा।

इसके अतिरिक्त, अन्य tools इसे ढूँढने में सक्षम नहीं हो सकते हैं, उदाहरण के लिए [VS Code एक्सटेंशन](editor-support.md) या [FastAPI Cloud](https://fastapicloud.com), इसलिए `pyproject.toml` में `entrypoint` का उपयोग करने की सिफारिश की जाती है।

## `fastapi dev` { #fastapi-dev }

`fastapi dev` चलाने से development mode शुरू होता है।

Default रूप से, **auto-reload** enabled होता है, जो आपके code में changes करने पर server को अपने-आप reload कर देता है। यह resource-intensive है और disabled होने की तुलना में कम stable हो सकता है। आपको इसे केवल development के लिए ही उपयोग करना चाहिए। यह IP address `127.0.0.1` पर भी listen करता है, जो आपकी machine का खुद से ही communicate करने वाला IP है (`localhost`)।

## `fastapi run` { #fastapi-run }

`fastapi run` execute करने से FastAPI production mode में शुरू होता है।

Default रूप से, **auto-reload** disabled होता है। यह IP address `0.0.0.0` पर भी listen करता है, जिसका मतलब सभी available IP addresses है, इस तरह यह उस machine से communicate कर सकने वाले किसी भी व्यक्ति के लिए publicly accessible होगा। आम तौर पर आप production में इसे इसी तरह चलाएँगे, उदाहरण के लिए, एक container में।

अधिकतर मामलों में आपके पास ऊपर से HTTPS handle करने वाला "termination proxy" होगा (और होना चाहिए), यह इस पर निर्भर करेगा कि आप अपना application कैसे deploy करते हैं, आपका provider आपके लिए यह कर सकता है, या आपको इसे खुद set up करने की ज़रूरत हो सकती है।

/// tip | सुझाव

आप इसके बारे में [deployment documentation](deployment/index.md) में और जान सकते हैं।

///
