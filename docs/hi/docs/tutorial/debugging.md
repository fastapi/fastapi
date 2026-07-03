# Debugging { #debugging }

आप अपने editor में debugger connect कर सकते हैं, उदाहरण के लिए Visual Studio Code या PyCharm के साथ।

## `uvicorn` को call करें { #call-uvicorn }

अपने FastAPI application में, `uvicorn` को सीधे import करके run करें:

{* ../../docs_src/debugging/tutorial001_py310.py hl[1,15] *}

### `__name__ == "__main__"` के बारे में { #about-name-main }

`__name__ == "__main__"` का मुख्य उद्देश्य ऐसा कुछ code रखना है जो तब execute होता है जब आपकी file को इसके साथ call किया जाता है:

<div class="termy">

```console
$ python myapp.py
```

</div>

लेकिन तब call नहीं होता जब कोई दूसरी file इसे import करती है, जैसे कि:

```Python
from myapp import app
```

#### अधिक विवरण { #more-details }

मान लीजिए आपकी file का नाम `myapp.py` है।

अगर आप इसे इसके साथ run करते हैं:

<div class="termy">

```console
$ python myapp.py
```

</div>

तो आपकी file में Python द्वारा अपने आप बनाई गई internal variable `__name__` का value string `"__main__"` होगा।

तो, यह section:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

run होगा।

---

अगर आप उस module (file) को import करते हैं तो ऐसा नहीं होगा।

तो, अगर आपके पास `importer.py` नाम की कोई दूसरी file है जिसमें यह है:

```Python
from myapp import app

# कुछ और code
```

उस स्थिति में, `myapp.py` के अंदर अपने आप बनाई गई variable `__name__` का value `"__main__"` नहीं होगा।

तो, यह line:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

execute नहीं होगी।

/// note | नोट

अधिक जानकारी के लिए, [आधिकारिक Python docs](https://docs.python.org/3/library/__main__.html) देखें।

///

## अपने debugger के साथ अपना code run करें { #run-your-code-with-your-debugger }

क्योंकि आप Uvicorn server को सीधे अपने code से run कर रहे हैं, आप अपने Python program (अपने FastAPI application) को सीधे debugger से call कर सकते हैं।

---

उदाहरण के लिए, Visual Studio Code में, आप यह कर सकते हैं:

* "Debug" panel पर जाएँ।
* "Add configuration..."।
* "Python" चुनें।
* "`Python: Current File (Integrated Terminal)`" option के साथ debugger run करें।

फिर यह आपके **FastAPI** code के साथ server start करेगा, आपके breakpoints पर रुकेगा, आदि।

यह कुछ ऐसा दिख सकता है:

<img src="/img/tutorial/debugging/image01.png">

---

अगर आप PyCharm का उपयोग करते हैं, तो आप यह कर सकते हैं:

* "Run" menu खोलें।
* "Debug..." option चुनें।
* फिर एक context menu दिखाई देता है।
* debug करने के लिए file चुनें (इस मामले में, `main.py`)।

फिर यह आपके **FastAPI** code के साथ server start करेगा, आपके breakpoints पर रुकेगा, आदि।

यह कुछ ऐसा दिख सकता है:

<img src="/img/tutorial/debugging/image02.png">
