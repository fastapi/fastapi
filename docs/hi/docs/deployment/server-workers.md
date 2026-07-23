# Server Workers - Workers के साथ Uvicorn { #server-workers-uvicorn-with-workers }

आइए पहले वाले deployment concepts को फिर से देखें:

* Security - HTTPS
* startup पर चलना
* Restarts
* **Replication (चल रहे processes की संख्या)**
* Memory
* शुरू करने से पहले के पिछले steps

इस बिंदु तक, docs के सभी tutorials में, आपने शायद एक **server program** चलाया होगा, उदाहरण के लिए, `fastapi` command का उपयोग करके, जो Uvicorn चलाता है, और एक **single process** चलाता है।

Applications deploy करते समय आप शायद **processes की कुछ replication** रखना चाहेंगे ताकि **multiple cores** का लाभ लिया जा सके और अधिक requests handle की जा सकें।

जैसा कि आपने पिछले chapter में [Deployment Concepts](concepts.md) के बारे में देखा, कई strategies हैं जिनका आप उपयोग कर सकते हैं।

यहाँ मैं आपको दिखाऊँगा कि `fastapi` command या सीधे `uvicorn` command का उपयोग करके **worker processes** के साथ **Uvicorn** कैसे उपयोग करें।

/// note | नोट

यदि आप containers का उपयोग कर रहे हैं, उदाहरण के लिए Docker या Kubernetes के साथ, तो मैं आपको इसके बारे में अगले chapter में और बताऊँगा: [Containers में FastAPI - Docker](docker.md)।

विशेष रूप से, **Kubernetes** पर चलते समय आप शायद workers का उपयोग **नहीं** करना चाहेंगे और इसके बजाय **प्रति container एक single Uvicorn process** चलाना चाहेंगे, लेकिन मैं आपको इसके बारे में उस chapter में बाद में बताऊँगा।

///

## Multiple Workers { #multiple-workers }

आप `--workers` command line option के साथ multiple workers शुरू कर सकते हैं:

//// tab | `fastapi`

यदि आप `fastapi` command का उपयोग करते हैं:

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

यदि आप सीधे `uvicorn` command का उपयोग करना पसंद करते हैं:

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

यहाँ एकमात्र नया option `--workers` है, जो Uvicorn को 4 worker processes शुरू करने के लिए कहता है।

आप यह भी देख सकते हैं कि यह प्रत्येक process का **PID** दिखाता है, parent process के लिए `27365` (यह **process manager** है) और प्रत्येक worker process के लिए एक: `27368`, `27369`, `27370`, और `27367`।

## Deployment Concepts { #deployment-concepts }

यहाँ आपने देखा कि application के execution को **parallelize** करने, CPU में **multiple cores** का लाभ लेने, और **अधिक requests** serve करने में सक्षम होने के लिए multiple **workers** का उपयोग कैसे किया जाता है।

ऊपर दी गई deployment concepts की सूची से, workers का उपयोग मुख्य रूप से **replication** वाले हिस्से में मदद करेगा, और थोड़ा बहुत **restarts** में भी, लेकिन आपको अभी भी बाकी चीज़ों का ध्यान रखना होगा:

* **Security - HTTPS**
* **startup पर चलना**
* ***Restarts***
* Replication (चल रहे processes की संख्या)
* **Memory**
* **शुरू करने से पहले के पिछले steps**

## Containers और Docker { #containers-and-docker }

अगले chapter में [Containers में FastAPI - Docker](docker.md) के बारे में मैं कुछ strategies समझाऊँगा जिनका उपयोग आप बाकी **deployment concepts** को handle करने के लिए कर सकते हैं।

मैं आपको दिखाऊँगा कि single Uvicorn process चलाने के लिए **शुरू से अपनी खुद की image कैसे build करें**। यह एक सरल process है और शायद यही आप तब करना चाहेंगे जब आप **Kubernetes** जैसे distributed container management system का उपयोग कर रहे हों।

## Recap { #recap }

आप `fastapi` या `uvicorn` commands के साथ `--workers` CLI option का उपयोग करके multiple worker processes का उपयोग कर सकते हैं, ताकि **multi-core CPUs** का लाभ लिया जा सके और **multiple processes parallel में** चलाए जा सकें।

यदि आप बाकी deployment concepts का खुद ध्यान रखते हुए **अपना खुद का deployment system** setup कर रहे हैं, तो आप इन tools और ideas का उपयोग कर सकते हैं।

Containers (जैसे Docker और Kubernetes) के साथ **FastAPI** के बारे में जानने के लिए अगला chapter देखें। आप देखेंगे कि उन tools में बाकी **deployment concepts** को भी हल करने के सरल तरीके हैं। ✨
