# Environment Variables { #environment-variables }

/// tip | مشورہ

اگر آپ پہلے سے جانتے ہیں کہ "environment variables" کیا ہیں اور انہیں کیسے استعمال کرتے ہیں، تو آزادانہ طور پر اسے چھوڑ دیں۔

///

ایک environment variable (جسے "**env var**" بھی کہا جاتا ہے) ایک ایسا variable ہے جو Python code سے **باہر**، **operating system** میں رہتا ہے، اور آپ کا Python code (یا دوسرے programs بھی) اسے پڑھ سکتے ہیں۔

Environment variables application **settings** کو سنبھالنے، Python کی **installation** کے حصے کے طور پر وغیرہ کے لیے مفید ہو سکتے ہیں۔

## Env Vars بنائیں اور استعمال کریں { #create-and-use-env-vars }

آپ **shell (terminal)** میں environment variables **بنا** سکتے ہیں اور استعمال کر سکتے ہیں، Python کی ضرورت کے بغیر:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Python میں env vars پڑھیں { #read-env-vars-in-python }

آپ Python سے **باہر**، terminal میں (یا کسی اور طریقے سے) بھی environment variables بنا سکتے ہیں، اور پھر **Python میں انہیں پڑھ** سکتے ہیں۔

مثال کے طور پر آپ کے پاس `main.py` فائل ہو سکتی ہے:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | مشورہ

[`os.getenv()`](https://docs.python.org/3.8/library/os.html#os.getenv) کا دوسرا argument واپس کرنے کے لیے default value ہے۔

اگر فراہم نہ کیا جائے تو بطور default یہ `None` ہے، یہاں ہم استعمال کرنے کے لیے default value `"World"` فراہم کر رہے ہیں۔

///

پھر آپ اس Python program کو call کر سکتے ہیں:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

چونکہ environment variables code سے باہر سیٹ ہو سکتے ہیں، لیکن code کے ذریعے پڑھے جا سکتے ہیں، اور باقی فائلوں کے ساتھ (`git` میں commit) محفوظ نہیں ہونے چاہئیں، ان کو configurations یا **settings** کے لیے استعمال کرنا عام ہے۔

آپ ایک environment variable صرف کسی **خاص program invocation** کے لیے بھی بنا سکتے ہیں، جو صرف اس program کے لیے دستیاب ہو، اور صرف اس کے دورانیے کے لیے۔

ایسا کرنے کے لیے، اسے program سے ٹھیک پہلے، اسی لائن پر بنائیں:

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | مشورہ

آپ اس کے بارے میں مزید [The Twelve-Factor App: Config](https://12factor.net/config) پر پڑھ سکتے ہیں۔

///

## Types اور Validation { #types-and-validation }

یہ environment variables صرف **text strings** کو ہی سنبھال سکتے ہیں، کیونکہ وہ Python سے باہر ہیں اور دوسرے programs اور باقی system (اور مختلف operating systems جیسے Linux، Windows، macOS) کے ساتھ compatible ہونی چاہئیں۔

اس کا مطلب ہے کہ Python میں environment variable سے پڑھی جانے والی **کوئی بھی value** ایک **`str`** ہوگی، اور کسی مختلف type میں تبدیلی یا کوئی validation code میں کرنا ہوگا۔

آپ application **settings** سنبھالنے کے لیے environment variables استعمال کرنے کے بارے میں مزید [Advanced User Guide - Settings and Environment Variables](./advanced/settings.md) میں سیکھیں گے۔

## `PATH` Environment Variable { #path-environment-variable }

ایک **خاص** environment variable ہے جسے **`PATH`** کہتے ہیں جو operating systems (Linux، macOS، Windows) چلانے کے لیے programs تلاش کرنے میں استعمال کرتا ہے۔

Variable `PATH` کی value ایک لمبی string ہے جو directories پر مشتمل ہے جو Linux اور macOS پر colon `:` سے اور Windows پر semicolon `;` سے الگ ہوتی ہیں۔

مثال کے طور پر، `PATH` environment variable اس طرح نظر آ سکتا ہے:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

اس کا مطلب ہے کہ system کو ان directories میں programs تلاش کرنے چاہئیں:

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

اس کا مطلب ہے کہ system کو ان directories میں programs تلاش کرنے چاہئیں:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

جب آپ terminal میں کوئی **command** ٹائپ کرتے ہیں، تو operating system `PATH` environment variable میں درج **ہر directory** میں program **تلاش کرتا ہے**۔

مثال کے طور پر، جب آپ terminal میں `python` ٹائپ کرتے ہیں، تو operating system اس فہرست کی **پہلی directory** میں `python` نامی program تلاش کرتا ہے۔

اگر مل جائے تو وہ اسے **استعمال کرے گا**۔ ورنہ **دوسری directories** میں تلاش جاری رکھتا ہے۔

### Python install کرنا اور `PATH` کو اپڈیٹ کرنا { #installing-python-and-updating-the-path }

جب آپ Python install کرتے ہیں، تو آپ سے پوچھا جا سکتا ہے کہ کیا آپ `PATH` environment variable کو اپڈیٹ کرنا چاہتے ہیں۔

//// tab | Linux, macOS

فرض کریں آپ Python install کرتے ہیں اور یہ `/opt/custompython/bin` directory میں آتا ہے۔

اگر آپ `PATH` environment variable اپڈیٹ کرنے پر ہاں کہیں، تو installer `/opt/custompython/bin` کو `PATH` environment variable میں شامل کر دے گا۔

یہ اس طرح نظر آ سکتا ہے:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

اس طرح، جب آپ terminal میں `python` ٹائپ کریں گے، تو system `/opt/custompython/bin` (آخری directory) میں Python program تلاش کرے گا اور اسے استعمال کرے گا۔

////

//// tab | Windows

فرض کریں آپ Python install کرتے ہیں اور یہ `C:\opt\custompython\bin` directory میں آتا ہے۔

اگر آپ `PATH` environment variable اپڈیٹ کرنے پر ہاں کہیں، تو installer `C:\opt\custompython\bin` کو `PATH` environment variable میں شامل کر دے گا۔

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

اس طرح، جب آپ terminal میں `python` ٹائپ کریں گے، تو system `C:\opt\custompython\bin` (آخری directory) میں Python program تلاش کرے گا اور اسے استعمال کرے گا۔

////

تو اگر آپ ٹائپ کریں:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

System `/opt/custompython/bin` میں `python` program **تلاش** کرے گا اور اسے چلائے گا۔

یہ تقریباً اس کے مساوی ہوگا:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

System `C:\opt\custompython\bin\python` میں `python` program **تلاش** کرے گا اور اسے چلائے گا۔

یہ تقریباً اس کے مساوی ہوگا:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

یہ معلومات [Virtual Environments](virtual-environments.md) کے بارے میں سیکھتے وقت مفید ہوں گی۔

## نتیجہ { #conclusion }

اس کے ساتھ آپ کو اس بات کی بنیادی سمجھ ہونی چاہیے کہ **environment variables** کیا ہیں اور Python میں انہیں کیسے استعمال کرنا ہے۔

آپ ان کے بارے میں مزید [Wikipedia for Environment Variable](https://en.wikipedia.org/wiki/Environment_variable) پر بھی پڑھ سکتے ہیں۔

بہت سے معاملات میں یہ فوری طور پر واضح نہیں ہوتا کہ environment variables کیسے مفید اور قابل اطلاق ہوں گے۔ لیکن جب آپ development کر رہے ہوتے ہیں تو یہ بہت سے مختلف منظرناموں میں سامنے آتے رہتے ہیں، تو ان کے بارے میں جاننا اچھا ہے۔

مثال کے طور پر، اگلے سیکشن [Virtual Environments](virtual-environments.md) میں آپ کو یہ معلومات کی ضرورت ہوگی۔
