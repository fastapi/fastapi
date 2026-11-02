# Dependencies के रूप में Classes { #classes-as-dependencies }

**Dependency Injection** system में और गहराई में जाने से पहले, पिछले उदाहरण को बेहतर बनाते हैं।

## पिछले उदाहरण से एक `dict` { #a-dict-from-the-previous-example }

पिछले उदाहरण में, हम अपनी dependency ("dependable") से एक `dict` return कर रहे थे:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

लेकिन फिर हमें *path operation function* के parameter `commons` में एक `dict` मिलता है।

और हम जानते हैं कि editors `dict`s के लिए ज़्यादा support (जैसे completion) नहीं दे सकते, क्योंकि वे उनकी keys और value types नहीं जान सकते।

हम इससे बेहतर कर सकते हैं...

## Dependency किससे बनती है { #what-makes-a-dependency }

अब तक आपने dependencies को functions के रूप में declare होते देखा है।

लेकिन dependencies declare करने का यही एकमात्र तरीका नहीं है (हालाँकि शायद यह अधिक common होगा)।

मुख्य बात यह है कि dependency एक "callable" होनी चाहिए।

Python में "**callable**" वह कोई भी चीज़ है जिसे Python एक function की तरह "call" कर सकता है।

तो, अगर आपके पास कोई object `something` है (जो शायद function _न_ हो) और आप उसे इस तरह "call" (execute) कर सकते हैं:

```Python
something()
```

या

```Python
something(some_argument, some_keyword_argument="foo")
```

तो वह एक "callable" है।

## Dependencies के रूप में Classes { #classes-as-dependencies_1 }

आप ध्यान दे सकते हैं कि Python class का instance बनाने के लिए भी आप वही syntax उपयोग करते हैं।

उदाहरण के लिए:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

इस case में, `fluffy` class `Cat` का एक instance है।

और `fluffy` बनाने के लिए, आप `Cat` को "call" कर रहे हैं।

इसलिए, Python class भी एक **callable** है।

फिर, **FastAPI** में, आप Python class को dependency के रूप में उपयोग कर सकते हैं।

FastAPI वास्तव में यह check करता है कि वह एक "callable" (function, class या कुछ और) है और उसमें parameters defined हैं।

अगर आप **FastAPI** में dependency के रूप में कोई "callable" pass करते हैं, तो यह उस "callable" के parameters को analyze करेगा, और उन्हें *path operation function* के parameters की तरह ही process करेगा। इसमें sub-dependencies भी शामिल हैं।

यह उन callables पर भी लागू होता है जिनमें कोई parameters नहीं होते। ठीक वैसे ही जैसे बिना parameters वाले *path operation functions* के लिए होता।

फिर, हम ऊपर वाली dependency "dependable" `common_parameters` को class `CommonQueryParams` में बदल सकते हैं:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Class का instance बनाने के लिए उपयोग की गई `__init__` method पर ध्यान दें:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...इसमें वही parameters हैं जो हमारे पिछले `common_parameters` में थे:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

यही parameters **FastAPI** dependency को "solve" करने के लिए उपयोग करेगा।

दोनों cases में, इसमें होगा:

* एक optional `q` query parameter जो `str` है।
* एक `skip` query parameter जो `int` है, जिसका default `0` है।
* एक `limit` query parameter जो `int` है, जिसका default `100` है।

दोनों cases में data converted, validated, OpenAPI schema पर documented, आदि किया जाएगा।

## इसका उपयोग करें { #use-it }

अब आप इस class का उपयोग करके अपनी dependency declare कर सकते हैं।

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** `CommonQueryParams` class को call करता है। यह उस class का एक "instance" बनाता है और वह instance आपके function को parameter `commons` के रूप में pass किया जाएगा।

## Type annotation बनाम `Depends` { #type-annotation-vs-depends }

ध्यान दें कि ऊपर के code में हम `CommonQueryParams` को दो बार कैसे लिखते हैं:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

आखिरी `CommonQueryParams`, इसमें:

```Python
... Depends(CommonQueryParams)
```

...वही है जिसे **FastAPI** वास्तव में यह जानने के लिए उपयोग करेगा कि dependency क्या है।

FastAPI इसी से declared parameters extract करेगा और वास्तव में इसी को call करेगा।

---

इस case में, पहला `CommonQueryParams`, इसमें:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons: CommonQueryParams ...
```

////

...का **FastAPI** के लिए कोई विशेष अर्थ नहीं है। FastAPI इसे data conversion, validation, आदि के लिए उपयोग नहीं करेगा। (क्योंकि वह इसके लिए `Depends(CommonQueryParams)` का उपयोग कर रहा है)।

आप वास्तव में सिर्फ यह लिख सकते हैं:

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons = Depends(CommonQueryParams)
```

////

...जैसे:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

लेकिन type declare करने को प्रोत्साहित किया जाता है क्योंकि इस तरह आपका editor जान पाएगा कि parameter `commons` के रूप में क्या pass होगा, और फिर यह code completion, type checks, आदि में आपकी मदद कर सकता है:

<img src="/img/tutorial/dependencies/image02.png">

## Shortcut { #shortcut }

लेकिन आप देखते हैं कि यहाँ कुछ code repetition हो रहा है, `CommonQueryParams` को दो बार लिखते हुए:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** ऐसे cases के लिए एक shortcut प्रदान करता है, जहाँ dependency *specifically* एक class है जिसे **FastAPI** class का instance बनाने के लिए "call" करेगा।

उन specific cases के लिए, आप यह कर सकते हैं:

यह लिखने के बजाय:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...आप लिखते हैं:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | सुझाव

संभव हो तो `Annotated` version का उपयोग करना बेहतर है।

///

```Python
commons: CommonQueryParams = Depends()
```

////

आप dependency को parameter के type के रूप में declare करते हैं, और `Depends(CommonQueryParams)` के अंदर पूरी class को *फिर से* लिखने के बजाय, आप बिना किसी parameter के `Depends()` का उपयोग करते हैं।

फिर वही उदाहरण इस तरह दिखेगा:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...और **FastAPI** जान जाएगा कि क्या करना है।

/// tip | सुझाव

अगर यह मददगार से ज़्यादा confusing लगता है, तो इसे अनदेखा करें, आपको इसकी *ज़रूरत* नहीं है।

यह सिर्फ एक shortcut है। क्योंकि **FastAPI** आपको code repetition कम करने में मदद करने की परवाह करता है।

///
