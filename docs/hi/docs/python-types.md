# Python Types परिचय { #python-types-intro }

Python में वैकल्पिक "type hints" (जिन्हें "type annotations" भी कहा जाता है) का समर्थन है।

ये **"type hints"** या annotations एक विशेष syntax हैं, जो किसी variable का <dfn title="उदाहरण के लिए: str, int, float, bool">type</dfn> घोषित करने की अनुमति देते हैं।

अपने variables के लिए types घोषित करके, editors और tools आपको बेहतर support दे सकते हैं।

यह Python type hints के बारे में बस एक **त्वरित tutorial / refresher** है। इसमें केवल उतना ही शामिल है जितना उन्हें **FastAPI** के साथ उपयोग करने के लिए न्यूनतम रूप से आवश्यक है... जो वास्तव में बहुत कम है।

**FastAPI** पूरी तरह से इन्हीं type hints पर आधारित है, ये इसे कई फायदे और लाभ देते हैं।

लेकिन अगर आप कभी **FastAPI** का उपयोग नहीं भी करते, तब भी इनके बारे में थोड़ा सीखने से आपको लाभ होगा।

/// note | नोट

अगर आप Python expert हैं, और type hints के बारे में पहले से सब कुछ जानते हैं, तो अगले chapter पर जाएँ।

///

## प्रेरणा { #motivation }

आइए एक सरल उदाहरण से शुरू करें:

{* ../../docs_src/python_types/tutorial001_py310.py *}

इस program को call करने पर output आता है:

```
John Doe
```

Function निम्नलिखित करता है:

* एक `first_name` और `last_name` लेता है।
* प्रत्येक के पहले अक्षर को `title()` के साथ upper case में बदलता है।
* उन्हें बीच में एक space के साथ <dfn title="उन्हें एक साथ रखता है, एक के रूप में। एक की सामग्री के बाद दूसरे की सामग्री के साथ।">Concatenate</dfn> करता है।

{* ../../docs_src/python_types/tutorial001_py310.py hl[2] *}

### इसे edit करें { #edit-it }

यह एक बहुत सरल program है।

लेकिन अब कल्पना करें कि आप इसे scratch से लिख रहे थे।

किसी point पर आप function define करना शुरू करते हैं, और आपके parameters तैयार हैं...

लेकिन फिर आपको "वह method जो पहले अक्षर को upper case में बदलता है" call करना है।

क्या वह `upper` था? क्या वह `uppercase` था? `first_uppercase`? `capitalize`?

फिर, आप programmer के पुराने दोस्त, editor autocompletion के साथ कोशिश करते हैं।

आप function का पहला parameter, `first_name`, फिर एक dot (`.`) type करते हैं और फिर completion trigger करने के लिए `Ctrl+Space` दबाते हैं।

लेकिन, दुख की बात है, आपको कुछ भी उपयोगी नहीं मिलता:

<img src="/img/python-types/image01.png">

### Types जोड़ें { #add-types }

आइए पिछले version की एक single line बदलते हैं।

हम ठीक इस fragment को, function के parameters को, इससे बदलेंगे:

```Python
    first_name, last_name
```

इसमें:

```Python
    first_name: str, last_name: str
```

बस इतना ही।

यही "type hints" हैं:

{* ../../docs_src/python_types/tutorial002_py310.py hl[1] *}

यह default values declare करने जैसा नहीं है, जैसा कि इसमें होता:

```Python
    first_name="john", last_name="doe"
```

यह एक अलग चीज़ है।

हम colons (`:`) का उपयोग कर रहे हैं, equals (`=`) का नहीं।

और type hints जोड़ने से सामान्यतः यह नहीं बदलता कि बिना उनके जो होता, वह कैसे होता।

लेकिन अब, कल्पना करें कि आप फिर से उस function को बनाने के बीच में हैं, लेकिन type hints के साथ।

उसी point पर, आप `Ctrl+Space` के साथ autocomplete trigger करने की कोशिश करते हैं और आप देखते हैं:

<img src="/img/python-types/image02.png">

इसके साथ, आप options देखते हुए scroll कर सकते हैं, जब तक आपको वह न मिल जाए जो "पहचाना हुआ लगे":

<img src="/img/python-types/image03.png">

## और प्रेरणा { #more-motivation }

इस function को देखें, इसमें पहले से type hints हैं:

{* ../../docs_src/python_types/tutorial003_py310.py hl[1] *}

क्योंकि editor variables के types जानता है, आपको केवल completion ही नहीं मिलता, आपको error checks भी मिलते हैं:

<img src="/img/python-types/image04.png">

अब आप जानते हैं कि आपको इसे ठीक करना है, `age` को `str(age)` के साथ string में convert करना है:

{* ../../docs_src/python_types/tutorial004_py310.py hl[2] *}

## Types declare करना { #declaring-types }

आपने अभी type hints declare करने की मुख्य जगह देखी। Function parameters के रूप में।

यही वह मुख्य जगह भी है जहाँ आप उन्हें **FastAPI** के साथ उपयोग करेंगे।

### Simple types { #simple-types }

आप सभी standard Python types declare कर सकते हैं, केवल `str` ही नहीं।

आप उदाहरण के लिए उपयोग कर सकते हैं:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py310.py hl[1] *}

### `typing` module { #typing-module }

कुछ अतिरिक्त use cases के लिए, आपको standard library के `typing` module से कुछ चीज़ें import करने की आवश्यकता हो सकती है, उदाहरण के लिए जब आप declare करना चाहते हैं कि किसी चीज़ का "कोई भी type" है, तो आप `typing` से `Any` का उपयोग कर सकते हैं:

```python
from typing import Any


def some_function(data: Any):
    print(data)
```

### Generic types { #generic-types }

कुछ types square brackets में "type parameters" ले सकते हैं, ताकि उनके internal types define किए जा सकें, उदाहरण के लिए "strings की list" को `list[str]` declare किया जाएगा।

जो types type parameters ले सकते हैं उन्हें **Generic types** या **Generics** कहा जाता है।

आप उन्हीं builtin types को generics के रूप में उपयोग कर सकते हैं (square brackets और अंदर types के साथ):

* `list`
* `tuple`
* `set`
* `dict`

#### List { #list }

उदाहरण के लिए, आइए एक variable को `str` की `list` के रूप में define करते हैं।

Variable को उसी colon (`:`) syntax के साथ declare करें।

Type के रूप में, `list` रखें।

क्योंकि list एक ऐसा type है जिसमें कुछ internal types होते हैं, आप उन्हें square brackets में रखते हैं:

{* ../../docs_src/python_types/tutorial006_py310.py hl[1] *}

/// note | नोट

Square brackets में मौजूद उन internal types को "type parameters" कहा जाता है।

इस case में, `str` वह type parameter है जो `list` को pass किया गया है।

///

इसका मतलब है: "variable `items` एक `list` है, और इस list का प्रत्येक item एक `str` है"।

ऐसा करने से, आपका editor list से items process करते समय भी support दे सकता है:

<img src="/img/python-types/image05.png">

Types के बिना, इसे हासिल करना लगभग असंभव है।

ध्यान दें कि variable `item`, list `items` के elements में से एक है।

और फिर भी, editor जानता है कि यह एक `str` है, और उसके लिए support देता है।

#### Tuple और Set { #tuple-and-set }

आप `tuple`s और `set`s declare करने के लिए भी ऐसा ही करेंगे:

{* ../../docs_src/python_types/tutorial007_py310.py hl[1] *}

इसका मतलब है:

* Variable `items_t` 3 items वाला एक `tuple` है, एक `int`, दूसरा `int`, और एक `str`।
* Variable `items_s` एक `set` है, और इसके प्रत्येक item का type `bytes` है।

#### Dict { #dict }

`dict` define करने के लिए, आप 2 type parameters pass करते हैं, commas से separated।

पहला type parameter `dict` की keys के लिए होता है।

दूसरा type parameter `dict` की values के लिए होता है:

{* ../../docs_src/python_types/tutorial008_py310.py hl[1] *}

इसका मतलब है:

* Variable `prices` एक `dict` है:
    * इस `dict` की keys `str` type की हैं (मान लें, प्रत्येक item का नाम)।
    * इस `dict` की values `float` type की हैं (मान लें, प्रत्येक item की price)।

#### Union { #union }

आप declare कर सकते हैं कि कोई variable **कई types** में से कोई भी हो सकता है, उदाहरण के लिए, एक `int` या एक `str`।

इसे define करने के लिए आप दोनों types को separate करने के लिए <dfn title='इसे "bitwise or operator" भी कहा जाता है, लेकिन वह अर्थ यहाँ relevant नहीं है'>vertical bar (`|`)</dfn> का उपयोग करते हैं।

इसे "union" कहा जाता है, क्योंकि variable उन दो type sets के union में कुछ भी हो सकता है।

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

इसका मतलब है कि `item` एक `int` या एक `str` हो सकता है।

#### संभवतः `None` { #possibly-none }

आप declare कर सकते हैं कि किसी value का type, जैसे `str`, हो सकता है, लेकिन वह `None` भी हो सकती है।

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

सिर्फ `str` के बजाय `str | None` का उपयोग करने से editor आपको उन errors को detect करने में मदद करेगा जहाँ आप यह मान रहे हो सकते हैं कि कोई value हमेशा `str` है, जबकि वास्तव में वह `None` भी हो सकती है।

### Classes को types के रूप में { #classes-as-types }

आप किसी class को भी variable के type के रूप में declare कर सकते हैं।

मान लें आपके पास एक class `Person` है, जिसमें एक name है:

{* ../../docs_src/python_types/tutorial010_py310.py hl[1:3] *}

फिर आप किसी variable को `Person` type का declare कर सकते हैं:

{* ../../docs_src/python_types/tutorial010_py310.py hl[6] *}

और फिर, फिर से, आपको पूरा editor support मिलता है:

<img src="/img/python-types/image06.png">

ध्यान दें कि इसका मतलब है "`one_person`, class `Person` का एक **instance** है"।

इसका मतलब यह नहीं है कि "`one_person`, `Person` नाम की **class** है"।

## Pydantic models { #pydantic-models }

[Pydantic](https://docs.pydantic.dev/) data validation करने के लिए एक Python library है।

आप data की "shape" को attributes वाली classes के रूप में declare करते हैं।

और प्रत्येक attribute का एक type होता है।

फिर आप कुछ values के साथ उस class का एक instance create करते हैं और यह values को validate करेगा, उन्हें appropriate type में convert करेगा (अगर ऐसा case है) और आपको पूरे data वाला एक object देगा।

और उस resulting object के साथ आपको पूरा editor support मिलता है।

Official Pydantic docs से एक उदाहरण:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// note | नोट

अधिक जानने के लिए [Pydantic, इसके docs देखें](https://docs.pydantic.dev/)।

///

**FastAPI** पूरी तरह से Pydantic पर आधारित है।

आप यह सब practice में [Tutorial - User Guide](tutorial/index.md) में बहुत अधिक देखेंगे।

## Metadata Annotations के साथ Type Hints { #type-hints-with-metadata-annotations }

Python में एक feature भी है जो `Annotated` का उपयोग करके इन type hints में **अतिरिक्त <dfn title="Data के बारे में data, इस case में, type के बारे में जानकारी, जैसे description।">metadata</dfn>** डालने की अनुमति देता है।

आप `typing` से `Annotated` import कर सकते हैं।

{* ../../docs_src/python_types/tutorial013_py310.py hl[1,4] *}

Python खुद इस `Annotated` के साथ कुछ नहीं करता। और editors और अन्य tools के लिए, type अभी भी `str` है।

लेकिन आप `Annotated` में इस जगह का उपयोग **FastAPI** को अतिरिक्त metadata देने के लिए कर सकते हैं कि आप अपनी application को कैसे behave कराना चाहते हैं।

याद रखने वाली महत्वपूर्ण बात यह है कि `Annotated` को pass किया गया **पहला *type parameter*** ही **actual type** होता है। बाकी सब, अन्य tools के लिए केवल metadata है।

अभी के लिए, आपको बस यह जानना है कि `Annotated` मौजूद है, और यह standard Python है। 😎

बाद में आप देखेंगे कि यह कितना **powerful** हो सकता है।

/// tip | सुझाव

यह तथ्य कि यह **standard Python** है, इसका मतलब है कि आपको अपने editor में, अपने code को analyze और refactor करने वाले tools के साथ, आदि, अभी भी **सबसे अच्छा possible developer experience** मिलेगा। ✨

और यह भी कि आपका code कई अन्य Python tools और libraries के साथ बहुत compatible होगा। 🚀

///

## **FastAPI** में Type hints { #type-hints-in-fastapi }

**FastAPI** इन type hints का लाभ उठाकर कई चीज़ें करता है।

**FastAPI** के साथ आप type hints के साथ parameters declare करते हैं और आपको मिलता है:

* **Editor support**।
* **Type checks**।

...और **FastAPI** उन्हीं declarations का उपयोग करता है:

* **Requirements define** करने के लिए: request path parameters, query parameters, headers, bodies, dependencies, आदि से।
* **Data convert** करने के लिए: request से required type में।
* **Data validate** करने के लिए: प्रत्येक request से आने वाले data को:
    * Data invalid होने पर client को लौटाए जाने वाले **automatic errors** generate करना।
* OpenAPI का उपयोग करके API को **document** करने के लिए:
    * जिसका उपयोग फिर automatic interactive documentation user interfaces द्वारा किया जाता है।

यह सब abstract लग सकता है। चिंता न करें। आप यह सब action में [Tutorial - User Guide](tutorial/index.md) में देखेंगे।

महत्वपूर्ण बात यह है कि standard Python types का उपयोग करके, एक ही जगह पर (अधिक classes, decorators, आदि जोड़ने के बजाय), **FastAPI** आपके लिए बहुत सारा काम कर देगा।

/// note | नोट

अगर आप पहले ही पूरे tutorial से गुजर चुके हैं और types के बारे में और देखने के लिए वापस आए हैं, तो एक अच्छा resource [`mypy` की "cheat sheet"](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html) है।

///
