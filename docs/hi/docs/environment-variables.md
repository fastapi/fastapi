# Environment Variables { #environment-variables }

/// tip | टिप

अगर आप पहले से जानते हैं कि "environment variables" क्या होते हैं और उनका उपयोग कैसे करना है, तो आप इसे छोड़ सकते हैं।

///

एक environment variable (जिसे "**env var**" भी कहा जाता है) एक variable है जो Python code के **बाहर**, **ऑपरेटिंग सिस्टम** में रहता है, और जिसे आपका Python code (या दूसरे programs भी) पढ़ सकते हैं।

Environment variables application **settings** संभालने, Python की **installation** के हिस्से के रूप में, आदि में उपयोगी हो सकते हैं।

## Env Vars बनाएं और उपयोग करें { #create-and-use-env-vars }

आप Python की ज़रूरत के बिना, **shell (terminal)** में environment variables **बना** और उपयोग कर सकते हैं:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// आप MY_NAME नाम का env var ऐसे बना सकते हैं
$ export MY_NAME="Wade Wilson"

// फिर आप इसे दूसरे programs के साथ उपयोग कर सकते हैं, जैसे
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// MY_NAME नाम का env var बनाएं
$ $Env:MY_NAME = "Wade Wilson"

// इसे दूसरे programs के साथ उपयोग करें, जैसे
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Python में env vars पढ़ें { #read-env-vars-in-python }

आप Python के **बाहर**, terminal में (या किसी भी दूसरे तरीके से) environment variables बना सकते हैं, और फिर **उन्हें Python में पढ़** सकते हैं।

उदाहरण के लिए, आपके पास `main.py` नाम की file हो सकती है जिसमें:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | टिप

[`os.getenv()`](https://docs.python.org/3.8/library/os.html#os.getenv) का दूसरा argument लौटाने के लिए default value है।

अगर यह दिया नहीं गया है, तो default रूप से यह `None` होता है, यहाँ हम उपयोग करने के लिए default value के रूप में `"World"` देते हैं।

///

फिर आप उस Python program को call कर सकते हैं:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// यहाँ हमने अभी env var set नहीं किया है
$ python main.py

// क्योंकि हमने env var set नहीं किया, हमें default value मिलती है

Hello World from Python

// लेकिन अगर हम पहले एक environment variable बनाते हैं
$ export MY_NAME="Wade Wilson"

// और फिर program को फिर से call करते हैं
$ python main.py

// अब यह environment variable पढ़ सकता है

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// यहाँ हमने अभी env var set नहीं किया है
$ python main.py

// क्योंकि हमने env var set नहीं किया, हमें default value मिलती है

Hello World from Python

// लेकिन अगर हम पहले एक environment variable बनाते हैं
$ $Env:MY_NAME = "Wade Wilson"

// और फिर program को फिर से call करते हैं
$ python main.py

// अब यह environment variable पढ़ सकता है

Hello Wade Wilson from Python
```

</div>

////

क्योंकि environment variables code के बाहर set किए जा सकते हैं, लेकिन code द्वारा पढ़े जा सकते हैं, और उन्हें बाकी files के साथ store (`git` में commit) करने की ज़रूरत नहीं होती, इसलिए configurations या **settings** के लिए उनका उपयोग करना आम है।

आप किसी **specific program invocation** के लिए भी एक environment variable बना सकते हैं, जो केवल उसी program के लिए उपलब्ध होता है, और केवल उसकी अवधि तक।

ऐसा करने के लिए, program से ठीक पहले, उसी line पर इसे बनाएं:

<div class="termy">

```console
// इस program call के लिए line में MY_NAME नाम का env var बनाएं
$ MY_NAME="Wade Wilson" python main.py

// अब यह environment variable पढ़ सकता है

Hello Wade Wilson from Python

// इसके बाद env var मौजूद नहीं रहता
$ python main.py

Hello World from Python
```

</div>

/// tip | टिप

आप इसके बारे में [The Twelve-Factor App: Config](https://12factor.net/config) पर और पढ़ सकते हैं।

///

## Types और Validation { #types-and-validation }

ये environment variables केवल **text strings** को ही संभाल सकते हैं, क्योंकि ये Python से बाहरी होते हैं और इन्हें दूसरे programs तथा बाकी system (और अलग-अलग ऑपरेटिंग सिस्टम, जैसे Linux, Windows, और macOS) के साथ compatible होना होता है।

इसका मतलब है कि Python में environment variable से पढ़ा गया **कोई भी value** **`str` होगा**, और किसी अलग type में कोई भी conversion या कोई भी validation code में करना होगा।

आप [Advanced User Guide - Settings and Environment Variables](./advanced/settings.md) में **application settings** संभालने के लिए environment variables के उपयोग के बारे में और सीखेंगे।

## `PATH` Environment Variable { #path-environment-variable }

**`PATH`** नाम का एक **special** environment variable होता है जिसका उपयोग ऑपरेटिंग सिस्टम (Linux, macOS, Windows) चलाने के लिए programs खोजने में करते हैं।

`PATH` variable का value एक लंबी string होती है जो Linux और macOS पर colon `:` से, और Windows पर semicolon `;` से अलग की गई directories से बनी होती है।

उदाहरण के लिए, `PATH` environment variable ऐसा दिख सकता है:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

इसका मतलब है कि system को इन directories में programs ढूंढने चाहिए:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

इसका मतलब है कि system को इन directories में programs ढूंढने चाहिए:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

जब आप terminal में कोई **command** type करते हैं, तो ऑपरेटिंग सिस्टम `PATH` environment variable में listed **उनमें से प्रत्येक directory** में program को **ढूंढता है**।

उदाहरण के लिए, जब आप terminal में `python` type करते हैं, तो ऑपरेटिंग सिस्टम उस list की **पहली directory** में `python` नाम का program ढूंढता है।

अगर उसे यह मिल जाता है, तो वह **इसे उपयोग** करेगा। नहीं तो वह **दूसरी directories** में ढूंढना जारी रखता है।

### Python install करना और `PATH` update करना { #installing-python-and-updating-the-path }

जब आप Python install करते हैं, तो आपसे पूछा जा सकता है कि क्या आप `PATH` environment variable को update करना चाहते हैं।

//// tab | Linux, macOS

मान लें कि आप Python install करते हैं और वह `/opt/custompython/bin` directory में जाता है।

अगर आप `PATH` environment variable को update करने के लिए yes कहते हैं, तो installer `/opt/custompython/bin` को `PATH` environment variable में जोड़ देगा।

यह ऐसा दिख सकता है:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

इस तरह, जब आप terminal में `python` type करते हैं, तो system Python program को `/opt/custompython/bin` (आखिरी directory) में ढूंढेगा और उसी का उपयोग करेगा।

////

//// tab | Windows

मान लें कि आप Python install करते हैं और वह `C:\opt\custompython\bin` directory में जाता है।

अगर आप `PATH` environment variable को update करने के लिए yes कहते हैं, तो installer `C:\opt\custompython\bin` को `PATH` environment variable में जोड़ देगा।

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

इस तरह, जब आप terminal में `python` type करते हैं, तो system Python program को `C:\opt\custompython\bin` (आखिरी directory) में ढूंढेगा और उसी का उपयोग करेगा।

////

तो, अगर आप type करते हैं:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

System `/opt/custompython/bin` में `python` program को **ढूंढेगा** और उसे चलाएगा।

यह लगभग ऐसा type करने के बराबर होगा:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

System `C:\opt\custompython\bin\python` में `python` program को **ढूंढेगा** और उसे चलाएगा।

यह लगभग ऐसा type करने के बराबर होगा:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

यह जानकारी [Virtual Environments](virtual-environments.md) के बारे में सीखते समय उपयोगी होगी।

## निष्कर्ष { #conclusion }

इससे आपको यह basic समझ मिल जानी चाहिए कि **environment variables** क्या होते हैं और Python में उनका उपयोग कैसे करना है।

आप इनके बारे में [Wikipedia for Environment Variable](https://en.wikipedia.org/wiki/Environment_variable) में भी और पढ़ सकते हैं।

कई मामलों में तुरंत यह बहुत स्पष्ट नहीं होता कि environment variables कैसे उपयोगी और applicable होंगे। लेकिन जब आप developing कर रहे होते हैं, तो ये कई अलग-अलग scenarios में बार-बार सामने आते हैं, इसलिए इनके बारे में जानना अच्छा है।

उदाहरण के लिए, अगले section में, [Virtual Environments](virtual-environments.md) के बारे में, आपको इस जानकारी की ज़रूरत होगी।
