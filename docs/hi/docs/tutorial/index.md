# Tutorial - उपयोगकर्ता गाइड { #tutorial-user-guide }

यह tutorial आपको step by step दिखाता है कि **FastAPI** को इसकी अधिकतर features के साथ कैसे उपयोग करें।

हर section धीरे-धीरे पिछले section पर आधारित होता है, लेकिन इसे topics को अलग रखने के लिए संरचित किया गया है, ताकि आप अपनी खास API ज़रूरतों को हल करने के लिए सीधे किसी भी specific topic पर जा सकें।

इसे भविष्य के reference के रूप में काम करने के लिए भी बनाया गया है, ताकि आप वापस आकर ठीक वही देख सकें जिसकी आपको ज़रूरत है।

## code चलाएँ { #run-the-code }

सभी code blocks को copy करके सीधे उपयोग किया जा सकता है (वे वास्तव में tested Python files हैं)।

किसी भी example को चलाने के लिए, code को `main.py` file में copy करें, और `fastapi dev` शुरू करें:

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

यह **बहुत ज़्यादा प्रोत्साहित** किया जाता है कि आप code लिखें या copy करें, उसे edit करें और locally चलाएँ।

इसे अपने editor में उपयोग करना ही वास्तव में आपको FastAPI के लाभ दिखाता है, जैसे आपको कितना कम code लिखना पड़ता है, सभी type checks, autocompletion, आदि।

---

## FastAPI install करें { #install-fastapi }

पहला step FastAPI install करना है।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाएँ, उसे activate करें, और फिर **FastAPI install करें**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | नोट

जब आप `pip install "fastapi[standard]"` के साथ install करते हैं, तो यह कुछ default optional standard dependencies के साथ आता है, जिनमें `fastapi-cloud-cli` शामिल है, जो आपको [FastAPI Cloud](https://fastapicloud.com) पर deploy करने देता है।

अगर आप वे optional dependencies नहीं चाहते, तो इसके बजाय आप `pip install fastapi` install कर सकते हैं।

अगर आप standard dependencies install करना चाहते हैं लेकिन `fastapi-cloud-cli` के बिना, तो आप `pip install "fastapi[standard-no-fastapi-cloud-cli]"` के साथ install कर सकते हैं।

///

/// tip | सुझाव

FastAPI के पास [VS Code के लिए official extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) (और Cursor) है, जो बहुत सारी features देता है, जिनमें path operation explorer, path operation search, tests में CodeLens navigation (tests से definition पर jump करना), और FastAPI Cloud deployment और logs शामिल हैं — सब कुछ आपके editor से।

///

## उन्नत उपयोगकर्ता गाइड { #advanced-user-guide }

एक **उन्नत उपयोगकर्ता गाइड** भी है जिसे आप इस **Tutorial - उपयोगकर्ता गाइड** के बाद पढ़ सकते हैं।

**उन्नत उपयोगकर्ता गाइड** इसी पर आधारित है, वही concepts उपयोग करता है, और आपको कुछ अतिरिक्त features सिखाता है।

लेकिन आपको पहले **Tutorial - उपयोगकर्ता गाइड** पढ़ना चाहिए (जो आप अभी पढ़ रहे हैं)।

इसे इस तरह design किया गया है कि आप सिर्फ **Tutorial - उपयोगकर्ता गाइड** के साथ एक complete application बना सकें, और फिर अपनी ज़रूरतों के अनुसार **उन्नत उपयोगकर्ता गाइड** के कुछ अतिरिक्त ideas का उपयोग करके उसे अलग-अलग तरीकों से extend कर सकें।
