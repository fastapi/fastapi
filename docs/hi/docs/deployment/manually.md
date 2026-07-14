# Server को मैन्युअली चलाएँ { #run-a-server-manually }

## `fastapi run` Command का उपयोग करें { #use-the-fastapi-run-command }

संक्षेप में, अपनी FastAPI application serve करने के लिए `fastapi run` का उपयोग करें:

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

यह ज़्यादातर मामलों में काम करेगा। 😎

आप उस command का उपयोग, उदाहरण के लिए, अपनी **FastAPI** app को किसी container में, किसी server में, आदि शुरू करने के लिए कर सकते हैं।

## ASGI Servers { #asgi-servers }

आइए details में थोड़ा और गहराई से देखें।

FastAPI Python web frameworks और servers बनाने के लिए एक standard का उपयोग करता है जिसे <abbr title="Asynchronous Server Gateway Interface - asynchronous server gateway interface">ASGI</abbr> कहा जाता है। FastAPI एक ASGI web framework है।

किसी remote server machine में **FastAPI** application (या कोई भी दूसरी ASGI application) चलाने के लिए आपको मुख्य रूप से एक ASGI server program चाहिए, जैसे **Uvicorn**; यही `fastapi` command में default रूप से आता है।

कई विकल्प हैं, जिनमें शामिल हैं:

* [Uvicorn](https://www.uvicorn.dev/): एक high performance ASGI server।
* [Hypercorn](https://hypercorn.readthedocs.io/): एक ASGI server जो अन्य features के साथ HTTP/2 और Trio के साथ compatible है।
* [Daphne](https://github.com/django/daphne): Django Channels के लिए बनाया गया ASGI server।
* [Granian](https://github.com/emmett-framework/granian): Python applications के लिए एक Rust HTTP server।

## Server Machine और Server Program { #server-machine-and-server-program }

नामों के बारे में ध्यान रखने योग्य एक छोटा-सा detail है। 💡

शब्द "**server**" आमतौर पर remote/cloud computer (physical या virtual machine) और उस machine पर चल रहे program (जैसे Uvicorn), दोनों के लिए उपयोग किया जाता है।

बस ध्यान रखें कि जब आप सामान्य रूप से "server" पढ़ते हैं, तो यह उन दो चीज़ों में से किसी एक को संदर्भित कर सकता है।

Remote machine का संदर्भ देते समय, इसे **server** कहना आम है, लेकिन **machine**, **VM** (virtual machine), **node** भी कहा जाता है। ये सभी किसी प्रकार की remote machine को संदर्भित करते हैं, जो सामान्यतः Linux चला रही होती है, जहाँ आप programs चलाते हैं।

## Server Program Install करें { #install-the-server-program }

जब आप FastAPI install करते हैं, तो यह एक production server, Uvicorn, के साथ आता है, और आप इसे `fastapi run` command से शुरू कर सकते हैं।

लेकिन आप एक ASGI server को मैन्युअली भी install कर सकते हैं।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और फिर आप server application install कर सकते हैं।

उदाहरण के लिए, Uvicorn install करने के लिए:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

किसी भी अन्य ASGI server program के लिए भी इसी तरह की प्रक्रिया लागू होगी।

/// tip | टिप

`standard` जोड़ने पर, Uvicorn कुछ recommended extra dependencies install और use करेगा।

इसमें `uvloop` शामिल है, जो `asyncio` के लिए high-performance drop-in replacement है, और बड़ा concurrency performance boost देता है।

जब आप `pip install "fastapi[standard]"` जैसी किसी command से FastAPI install करते हैं, तो आपको `uvicorn[standard]` भी मिल जाता है।

///

## Server Program चलाएँ { #run-the-server-program }

यदि आपने ASGI server मैन्युअली install किया है, तो आमतौर पर आपको अपनी FastAPI application import कराने के लिए एक खास format में import string पास करनी होगी:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | नोट

Command `uvicorn main:app` इनका संदर्भ देती है:

* `main`: file `main.py` (Python "module")।
* `app`: `main.py` के अंदर `app = FastAPI()` line से बनाया गया object।

यह इसके equivalent है:

```Python
from main import app
```

///

हर alternative ASGI server program की command मिलती-जुलती होगी, आप उनके संबंधित documentation में और पढ़ सकते हैं।

/// warning | चेतावनी

Uvicorn और अन्य servers एक `--reload` option support करते हैं जो development के दौरान उपयोगी होता है।

`--reload` option बहुत अधिक resources consume करता है, अधिक unstable होता है, आदि।

यह **development** के दौरान बहुत मदद करता है, लेकिन आपको इसे **production** में use **नहीं** करना चाहिए।

///

## Deployment Concepts { #deployment-concepts }

ये examples server program (जैसे Uvicorn) चलाते हैं, **एक single process** शुरू करते हैं, जो predefined port (जैसे `80`) पर सभी IPs (`0.0.0.0`) को listen करता है।

यह basic idea है। लेकिन आप शायद कुछ अतिरिक्त चीज़ों का ध्यान रखना चाहेंगे, जैसे:

* Security - HTTPS
* startup पर चलना
* Restarts
* Replication (चल रहे processes की संख्या)
* Memory
* शुरू करने से पहले के previous steps

अगले chapters में मैं आपको इन concepts में से हर एक के बारे में, उनके बारे में कैसे सोचें, और उन्हें handle करने की strategies के साथ कुछ concrete examples के बारे में और बताऊँगा। 🚀
