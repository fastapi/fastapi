# Python Types का परिचय { #python-types-intro }

Python में वैकल्पिक "type hints" (जिन्हें "type annotations" भी कहा जाता है) का सपोर्ट है।

ये **"type hints"** या annotations एक विशेष syntax हैं जो किसी variable का <dfn title="उदाहरण के लिए: str, int, float, bool">टाइप</dfn> घोषित करने की सुविधा देते हैं।

अपने variables के लिए types घोषित करने से editors और tools आपको बेहतर सहायता दे सकते हैं।

यह Python type hints के बारे में बस एक **त्वरित tutorial / refresher** है। इसमें केवल उतना ही शामिल है जितना **FastAPI** के साथ उनका उपयोग करने के लिए आवश्यक है... जो वास्तव में बहुत कम है।

**FastAPI** पूरी तरह से इन type hints पर आधारित है, ये इसे कई फायदे और लाभ देते हैं।

लेकिन अगर आप कभी **FastAPI** का उपयोग न भी करें, तब भी इनके बारे में थोड़ा सीखने से आपको लाभ होगा।

/// note | नोट

यदि आप Python expert हैं, और आप type hints के बारे में सब कुछ पहले से जानते हैं, तो अगले chapter पर जाएँ।

///

## प्रेरणा { #motivation }

आइए एक सरल उदाहरण से शुरू करें:

{* ../../docs_src/python_types/tutorial001_py310.py *}

इस program को call करने पर output मिलता है:

```
John Doe
```

यह function निम्नलिखित करता है:

* एक `first_name` और `last_name` लेता है।
* `title()` के साथ प्रत्येक के पहले अक्षर को upper case में बदलता है।
* उन्हें बीच में एक space के साथ <dfn title="उन्हें एक साथ रखता है, एक के रूप में। एक की सामग्री के बाद दूसरे की सामग्री के साथ।">जोड़ता</dfn> है।

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### इसे edit करें { #edit-it }

यह एक बहुत सरल program है।

लेकिन अब कल्पना करें कि आप इसे शुरुआत से लिख रहे थे।

किसी समय आप function define करना शुरू करते हैं, और आपके parameters तैयार हैं...

लेकिन फिर आपको "वह method जो पहले अक्षर को upper case में बदलता है" call करना होता है।

क्या वह `upper` था? क्या वह `uppercase` था? `first_uppercase`? `capitalize`?

फिर, आप programmer के पुराने दोस्त, editor autocompletion, को आज़माते हैं।

आप function का पहला parameter, `first_name`, type करते हैं, फिर एक dot (`.`) और फिर completion trigger करने के लिए `Ctrl+Space` दबाते हैं।

लेकिन, दुख की बात है, आपको कुछ भी उपयोगी नहीं मिलता:

<img src="/img/python-types/image01.png">

### Types जोड़ें { #add-types }

आइए पिछले version की एक ही line को modify करें।

हम exactly इस fragment, function के parameters, को बदलेंगे:

```Python
    first_name, last_name
```

से:

```Python
    first_name: str, last_name: str
```

बस इतना ही।

ये "type hints" हैं:

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

यह default values घोषित करने जैसा नहीं है, जैसा कि इसमें होता:

```Python
    first_name="john", last_name="doe"
```

यह एक अलग चीज़ है।

हम colons (`:`) का उपयोग कर रहे हैं, equals (`=`) का नहीं।

और type hints जोड़ने से सामान्यतः यह नहीं बदलता कि उनके बिना जो होता, उससे क्या होगा।

लेकिन अब, कल्पना करें कि आप फिर से वही function बना रहे हैं, लेकिन type hints के साथ।

उसी point पर, आप `Ctrl+Space` के साथ autocomplete trigger करने की कोशिश करते हैं और आप देखते हैं:

<img src="/img/python-types/image02.png">

इसके साथ, आप options देखते हुए scroll कर सकते हैं, जब तक आपको वह option न मिल जाए जो "जाना-पहचाना लगे":

<img src="/img/python-types/image03.png">

## और प्रेरणा { #more-motivation }

इस function को देखें, इसमें पहले से type hints हैं:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

क्योंकि editor variables के types जानता है, आपको केवल completion ही नहीं मिलता, बल्कि error checks भी मिलते हैं:

<img src="/img/python-types/image04.png">

अब आप जानते हैं कि आपको इसे ठीक करना है, `age` को `str(age)` के साथ string में convert करना है:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Types घोषित करना { #declaring-types }

आपने type hints घोषित करने की मुख्य जगह अभी देखी। Function parameters के रूप में।

यह वही मुख्य जगह भी है जहाँ आप उन्हें **FastAPI** के साथ उपयोग करेंगे।

### Simple types { #simple-types }

आप सभी standard Python types घोषित कर सकते हैं, केवल `str` ही नहीं।

उदाहरण के लिए, आप उपयोग कर सकते हैं:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` module { #typing-module }

कुछ अतिरिक्त use cases के लिए, आपको standard library के `typing` module से कुछ चीज़ें import करनी पड़ सकती हैं, उदाहरण के लिए जब आप घोषित करना चाहते हैं कि किसी चीज़ का "कोई भी type" हो सकता है, तो आप `typing` से `Any` उपयोग कर सकते हैं:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic types { #generic-types }

कुछ types square brackets में "type parameters" ले सकते हैं, ताकि उनके internal types define किए जा सकें, उदाहरण के लिए "strings की list" को `list[str]` घोषित किया जाएगा।

इन types को जो type parameters ले सकते हैं, **Generic types** या **Generics** कहा जाता है।

आप उन्हीं builtin types को generics के रूप में उपयोग कर सकते हैं (square brackets और अंदर types के साथ):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

उदाहरण के लिए, आइए एक variable को `str` की `list` के रूप में define करें।

Variable को उसी colon (`:`) syntax के साथ declare करें।

Type के रूप में, `list` रखें।

क्योंकि list एक ऐसा type है जिसमें कुछ internal types होते हैं, आप उन्हें square brackets में रखते हैं:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// note | नोट

Square brackets में मौजूद उन internal types को "type parameters" कहा जाता है।

इस मामले में, `str` वह type parameter है जो `list` को pass किया गया है।

///

इसका अर्थ है: "variable `items` एक `list` है, और इस list का प्रत्येक item एक `str` है"।

ऐसा करने से, आपका editor list से items process करते समय भी support दे सकता है:

<img src="/img/python-types/image05.png">

Types के बिना, यह हासिल करना लगभग असंभव है।

ध्यान दें कि variable `item`, list `items` के elements में से एक है।

और फिर भी, editor जानता है कि यह एक `str` है, और उसके लिए support प्रदान करता है।

#### Tuple और Set { #tuple-and-set }

आप `tuple`s और `set`s घोषित करने के लिए भी यही करेंगे:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

इसका अर्थ है:

* Variable `items_t` एक `tuple` है जिसमें 3 items हैं, एक `int`, दूसरा `int`, और एक `str`।
* Variable `items_s` एक `set` है, और उसके प्रत्येक item का type `bytes` है।

#### Dict { #dict }

`dict` define करने के लिए, आप 2 type parameters pass करते हैं, commas से अलग किए हुए।

पहला type parameter `dict` की keys के लिए होता है।

दूसरा type parameter `dict` की values के लिए होता है:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

इसका अर्थ है:

* Variable `prices` एक `dict` है:
    * इस `dict` की keys `str` type की हैं (मान लें, प्रत्येक item का नाम)।
    * इस `dict` की values `float` type की हैं (मान लें, प्रत्येक item की price)।

#### Union { #union }

आप घोषित कर सकते हैं कि कोई variable **कई types** में से कोई भी हो सकता है, उदाहरण के लिए, एक `int` या एक `str`।

इसे define करने के लिए आप दोनों types को अलग करने के लिए <dfn title='इसे "bitwise or operator" भी कहा जाता है, लेकिन वह अर्थ यहाँ प्रासंगिक नहीं है'>vertical bar (`|`)</dfn> का उपयोग करते हैं।

इसे "union" कहा जाता है, क्योंकि variable उन दो type sets के union में कुछ भी हो सकता है।

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

इसका अर्थ है कि `item` एक `int` या एक `str` हो सकता है।

#### संभवतः `None` { #possibly-none }

आप घोषित कर सकते हैं कि किसी value का कोई type हो सकता है, जैसे `str`, लेकिन वह `None` भी हो सकती है।

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

सिर्फ `str` के बजाय `str | None` का उपयोग करने से editor आपको ऐसी errors detect करने में मदद करेगा जहाँ आप मान रहे हों कि कोई value हमेशा `str` है, जबकि वह वास्तव में `None` भी हो सकती है।

### Classes को types के रूप में { #classes-as-types }

आप किसी class को variable के type के रूप में भी घोषित कर सकते हैं।

मान लें आपके पास `Person` class है, जिसमें एक name है:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

फिर आप किसी variable को `Person` type का घोषित कर सकते हैं:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

और फिर, आपको फिर से पूरा editor support मिलता है:

<img src="/img/python-types/image06.png">

ध्यान दें कि इसका अर्थ है "`one_person`, `Person` class का एक **instance** है"।

इसका अर्थ यह नहीं है कि "`one_person`, `Person` नाम की **class** है"।

## Pydantic models { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/) data validation करने के लिए एक Python library है।

आप data की "shape" को attributes वाली classes के रूप में declare करते हैं।

और प्रत्येक attribute का एक type होता है।

फिर आप उस class का एक instance कुछ values के साथ बनाते हैं और यह values को validate करेगा, उन्हें उपयुक्त type में convert करेगा (यदि ऐसा मामला हो) और आपको सभी data वाला एक object देगा।

और उस resulting object के साथ आपको पूरा editor support मिलता है।

Official Pydantic docs से एक उदाहरण:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// note | नोट

अधिक जानने के लिए [Pydantic, इसकी docs देखें](https://docs.pydantic.dev/)।

///

**FastAPI** पूरी तरह से Pydantic पर आधारित है।

आप यह सब व्यवहार में [Tutorial - User Guide](tutorial/index.md) में बहुत अधिक देखेंगे।

## Metadata Annotations के साथ Type Hints { #type-hints-with-metadata-annotations }

Python में एक feature भी है जो `Annotated` का उपयोग करके इन type hints में **अतिरिक्त <dfn title="data के बारे में data, इस मामले में, type के बारे में जानकारी, जैसे कोई description।">metadata</dfn>** डालने की अनुमति देता है।

आप `typing` से `Annotated` import कर सकते हैं।

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python स्वयं इस `Annotated` के साथ कुछ नहीं करता। और editors तथा अन्य tools के लिए, type अब भी `str` ही है।

लेकिन आप `Annotated` में इस space का उपयोग **FastAPI** को इस बारे में अतिरिक्त metadata देने के लिए कर सकते हैं कि आप अपनी application का व्यवहार कैसा चाहते हैं।

याद रखने वाली महत्वपूर्ण बात यह है कि `Annotated` को आप जो **पहला *type parameter*** pass करते हैं, वही **actual type** है। बाकी सब अन्य tools के लिए metadata है।

अभी के लिए, आपको बस यह जानना है कि `Annotated` मौजूद है, और यह standard Python है। 😎

बाद में आप देखेंगे कि यह कितना **powerful** हो सकता है।

/// tip | सुझाव

यह तथ्य कि यह **standard Python** है, इसका मतलब है कि आपको अपने editor में, अपने code को analyze और refactor करने के लिए उपयोग किए जाने वाले tools आदि के साथ, अब भी **सबसे अच्छा संभव developer experience** मिलेगा। ✨

और यह भी कि आपका code कई अन्य Python tools और libraries के साथ बहुत compatible रहेगा। 🚀

///

## **FastAPI** में Type hints { #type-hints-in-fastapi }

**FastAPI** इन type hints का लाभ उठाकर कई काम करता है।

**FastAPI** के साथ आप parameters को type hints के साथ declare करते हैं और आपको मिलता है:

* **Editor support**।
* **Type checks**।

...और **FastAPI** उन्हीं declarations का उपयोग करता है:

* **Requirements define** करने के लिए: request path parameters, query parameters, headers, bodies, dependencies, आदि से।
* **Data convert** करने के लिए: request से required type में।
* **Data validate** करने के लिए: प्रत्येक request से आने वाला:
    * Data invalid होने पर client को लौटाई जाने वाली **automatic errors** generate करना।
* OpenAPI का उपयोग करके API को **Document** करने के लिए:
    * जिसे फिर automatic interactive documentation user interfaces द्वारा उपयोग किया जाता है।

यह सब abstract लग सकता है। चिंता न करें। आप यह सब [Tutorial - User Guide](tutorial/index.md) में action में देखेंगे।

महत्वपूर्ण बात यह है कि standard Python types का उपयोग करके, एक ही जगह पर (अधिक classes, decorators आदि जोड़ने के बजाय), **FastAPI** आपके लिए बहुत सारा काम कर देगा।

/// note | नोट

यदि आप पहले ही पूरा tutorial पढ़ चुके हैं और types के बारे में और देखने के लिए वापस आए हैं, तो एक अच्छा resource [`mypy` की "cheat sheet"](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html) है।

///
