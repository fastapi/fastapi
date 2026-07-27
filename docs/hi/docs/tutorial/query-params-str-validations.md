# Query Parameters और String Validations { #query-parameters-and-string-validations }

**FastAPI** आपको अपने parameters के लिए अतिरिक्त जानकारी और validation declare करने देता है।

इस application को example के रूप में लेते हैं:

{* ../../docs_src/query_params_str_validations/tutorial001_py310.py hl[7] *}

query parameter `q` का type `str | None` है, इसका मतलब है कि यह type `str` का है लेकिन `None` भी हो सकता है, और वास्तव में, default value `None` है, इसलिए FastAPI जान जाएगा कि यह required नहीं है।

/// note | नोट

FastAPI जान जाएगा कि `q` की value required नहीं है क्योंकि default value `= None` है।

`str | None` होने से आपका editor आपको बेहतर support दे पाएगा और errors detect कर पाएगा।

///

## अतिरिक्त validation { #additional-validation }

हम यह enforce करने जा रहे हैं कि भले ही `q` optional हो, जब भी यह provide किया जाए, **इसकी length 50 characters से अधिक न हो**।

### `Query` और `Annotated` import करें { #import-query-and-annotated }

इसे हासिल करने के लिए, पहले import करें:

* `fastapi` से `Query`
* `typing` से `Annotated`

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[1,3] *}

/// note | नोट

FastAPI ने version 0.95.0 में `Annotated` के लिए support जोड़ा (और इसकी recommendation शुरू की)।

अगर आपके पास पुराना version है, तो `Annotated` use करने की कोशिश करने पर आपको errors मिलेंगे।

`Annotated` use करने से पहले सुनिश्चित करें कि आप [FastAPI version Upgrade करें](../deployment/versions.md#upgrading-the-fastapi-versions) कम से कम 0.95.1 तक।

///

## `q` parameter के type में `Annotated` use करें { #use-annotated-in-the-type-for-the-q-parameter }

याद है मैंने आपको पहले बताया था कि [Python Types Intro](../python-types.md#type-hints-with-metadata-annotations) में `Annotated` का उपयोग आपके parameters में metadata जोड़ने के लिए किया जा सकता है?

अब इसे FastAPI के साथ use करने का समय है। 🚀

हमारे पास यह type annotation था:

```Python
q: str | None = None
```

हम इसे `Annotated` के साथ wrap करेंगे, तो यह बन जाता है:

```Python
q: Annotated[str | None] = None
```

इन दोनों versions का मतलब एक ही है, `q` एक parameter है जो `str` या `None` हो सकता है, और default रूप से, यह `None` है।

अब मज़ेदार चीज़ों पर चलते हैं। 🎉

## `q` parameter में `Annotated` में `Query` जोड़ें { #add-query-to-annotated-in-the-q-parameter }

अब जब हमारे पास यह `Annotated` है जहाँ हम अधिक जानकारी रख सकते हैं (इस case में कुछ अतिरिक्त validation), `Annotated` के अंदर `Query` जोड़ें, और parameter `max_length` को `50` पर set करें:

{* ../../docs_src/query_params_str_validations/tutorial002_an_py310.py hl[9] *}

ध्यान दें कि default value अभी भी `None` है, इसलिए parameter अभी भी optional है।

लेकिन अब, `Annotated` के अंदर `Query(max_length=50)` होने से, हम FastAPI को बता रहे हैं कि हम चाहते हैं कि इस value के लिए **अतिरिक्त validation** हो, हम चाहते हैं कि इसमें अधिकतम 50 characters हों। 😎

/// tip | टिप

यहाँ हम `Query()` use कर रहे हैं क्योंकि यह एक **query parameter** है। बाद में हम `Path()`, `Body()`, `Header()`, और `Cookie()` जैसे अन्य देखेंगे, जो `Query()` जैसे ही arguments accept करते हैं।

///

FastAPI अब:

* data को **Validate** करेगा यह सुनिश्चित करते हुए कि max length 50 characters है
* जब data valid नहीं होगा तो client के लिए **clear error** दिखाएगा
* OpenAPI schema *path operation* में parameter को **Document** करेगा (ताकि यह **automatic docs UI** में दिखाई दे)

## Alternative (पुराना): default value के रूप में `Query` { #alternative-old-query-as-the-default-value }

FastAPI के पिछले versions (<dfn title="2023-03 से पहले">0.95.0</dfn> से पहले) में आपको अपने parameter की default value के रूप में `Query` use करना required था, बजाय इसे `Annotated` में रखने के, इसकी अच्छी संभावना है कि आपको आसपास ऐसा code दिखेगा, इसलिए मैं आपको इसे समझाऊंगा।

/// tip | टिप

नए code के लिए और जब भी संभव हो, ऊपर समझाए अनुसार `Annotated` use करें। इसके कई फायदे हैं (नीचे समझाए गए हैं) और कोई नुकसान नहीं। 🍰

///

इस तरह आप अपने function parameter की default value के रूप में `Query()` use करेंगे, parameter `max_length` को 50 पर set करते हुए:

{* ../../docs_src/query_params_str_validations/tutorial002_py310.py hl[7] *}

चूँकि इस case में (`Annotated` use किए बिना) हमें function में default value `None` को `Query()` से replace करना होता है, अब हमें parameter `Query(default=None)` के साथ default value set करनी होगी, यह उस default value को define करने का वही उद्देश्य पूरा करता है (कम से कम FastAPI के लिए)।

तो:

```Python
q: str | None = Query(default=None)
```

...parameter को optional बनाता है, `None` की default value के साथ, बिल्कुल इसके समान:


```Python
q: str | None = None
```

लेकिन `Query` version इसे स्पष्ट रूप से query parameter के रूप में declare करता है।

फिर, हम `Query` को और parameters pass कर सकते हैं। इस case में, `max_length` parameter जो strings पर apply होता है:

```Python
q: str | None = Query(default=None, max_length=50)
```

यह data को validate करेगा, data valid न होने पर clear error दिखाएगा, और OpenAPI schema *path operation* में parameter को document करेगा।

### default value के रूप में या `Annotated` में `Query` { #query-as-the-default-value-or-in-annotated }

ध्यान रखें कि `Annotated` के अंदर `Query` use करते समय आप `Query` के लिए `default` parameter use नहीं कर सकते।

इसके बजाय, function parameter की वास्तविक default value use करें। अन्यथा, यह inconsistent होगा।

उदाहरण के लिए, इसकी अनुमति नहीं है:

```Python
q: Annotated[str, Query(default="rick")] = "morty"
```

...क्योंकि यह clear नहीं है कि default value `"rick"` होनी चाहिए या `"morty"`।

तो, आप use करेंगे (preferably):

```Python
q: Annotated[str, Query()] = "rick"
```

...या पुराने code bases में आपको मिलेगा:

```Python
q: str = Query(default="rick")
```

### `Annotated` के फायदे { #advantages-of-annotated }

function parameters में default value के बजाय **`Annotated` use करने की recommendation है**, यह कई कारणों से **बेहतर** है। 🤓

**function parameter** की **default** value ही **वास्तविक default** value है, यह सामान्य रूप से Python के साथ अधिक intuitive है। 😌

आप उसी function को FastAPI के बिना **अन्य जगहों** पर **call** कर सकते हैं, और यह **उम्मीद के अनुसार काम** करेगा। अगर कोई **required** parameter है (बिना default value के), तो आपका **editor** आपको error के साथ बता देगा, **Python** भी required parameter pass किए बिना इसे run करने पर complain करेगा।

जब आप `Annotated` use नहीं करते और इसके बजाय **(पुराना) default value style** use करते हैं, अगर आप उस function को FastAPI के बिना **अन्य जगहों** पर call करते हैं, तो आपको function को सही से काम कराने के लिए arguments pass करना **याद रखना** होगा, अन्यथा values आपकी अपेक्षा से अलग होंगी (जैसे `str` के बजाय `QueryInfo` या कुछ similar)। और आपका editor complain नहीं करेगा, और Python भी उस function को run करते समय complain नहीं करेगा, केवल तब जब अंदर के operations error दें।

क्योंकि `Annotated` में एक से अधिक metadata annotation हो सकते हैं, अब आप उसी function को अन्य tools के साथ भी use कर सकते हैं, जैसे [Typer](https://typer.tiangolo.com/)। 🚀

## और validations जोड़ें { #add-more-validations }

आप parameter `min_length` भी जोड़ सकते हैं:

{* ../../docs_src/query_params_str_validations/tutorial003_an_py310.py hl[10] *}

## regular expressions जोड़ें { #add-regular-expressions }

आप एक <dfn title="एक regular expression, regex या regexp characters का ऐसा sequence है जो strings के लिए search pattern define करता है।">regular expression</dfn> `pattern` define कर सकते हैं जिससे parameter match करना चाहिए:

{* ../../docs_src/query_params_str_validations/tutorial004_an_py310.py hl[11] *}

यह specific regular expression pattern check करता है कि received parameter value:

* `^`: निम्न characters से शुरू होती है, पहले कोई characters नहीं हैं।
* `fixedquery`: exact value `fixedquery` रखती है।
* `$`: वहीं समाप्त होती है, `fixedquery` के बाद कोई और characters नहीं हैं।

अगर आप इन सभी **"regular expression"** ideas से खोया हुआ महसूस करते हैं, तो चिंता न करें। यह कई लोगों के लिए कठिन topic है। आप अभी regular expressions की जरूरत के बिना भी बहुत कुछ कर सकते हैं।

अब आप जानते हैं कि जब भी आपको इनकी जरूरत हो, आप इन्हें **FastAPI** में use कर सकते हैं।

## Default values { #default-values }

बेशक, आप `None` के अलावा default values use कर सकते हैं।

मान लीजिए कि आप `q` query parameter को `3` की `min_length` और `"fixedquery"` की default value के साथ declare करना चाहते हैं:

{* ../../docs_src/query_params_str_validations/tutorial005_an_py310.py hl[9] *}

/// note | नोट

`None` सहित किसी भी type की default value होना parameter को optional (not required) बनाता है।

///

## Required parameters { #required-parameters }

जब हमें अधिक validations या metadata declare करने की जरूरत नहीं होती, तो हम default value declare न करके ही `q` query parameter को required बना सकते हैं, जैसे:

```Python
q: str
```

इसके बजाय:

```Python
q: str | None = None
```

लेकिन अब हम इसे `Query` के साथ declare कर रहे हैं, उदाहरण के लिए ऐसे:

```Python
q: Annotated[str | None, Query(min_length=3)] = None
```

तो, जब आपको `Query` use करते हुए किसी value को required के रूप में declare करना हो, तो आप बस default value declare न करें:

{* ../../docs_src/query_params_str_validations/tutorial006_an_py310.py hl[9] *}

### Required, `None` हो सकता है { #required-can-be-none }

आप declare कर सकते हैं कि parameter `None` accept कर सकता है, लेकिन फिर भी यह required है। यह clients को value भेजने के लिए मजबूर करेगा, भले ही value `None` हो।

ऐसा करने के लिए, आप declare कर सकते हैं कि `None` एक valid type है लेकिन बस default value declare न करें:

{* ../../docs_src/query_params_str_validations/tutorial006c_an_py310.py hl[9] *}

## Query parameter list / multiple values { #query-parameter-list-multiple-values }

जब आप query parameter को स्पष्ट रूप से `Query` के साथ define करते हैं तो आप इसे values की list receive करने के लिए भी declare कर सकते हैं, या दूसरे शब्दों में, multiple values receive करने के लिए।

उदाहरण के लिए, query parameter `q` declare करने के लिए जो URL में कई बार आ सकता है, आप लिख सकते हैं:

{* ../../docs_src/query_params_str_validations/tutorial011_an_py310.py hl[9] *}

फिर, ऐसे URL के साथ:

```
http://localhost:8000/items/?q=foo&q=bar
```

आप multiple `q` *query parameters* की values (`foo` और `bar`) को अपने *path operation function* के अंदर Python `list` में, *function parameter* `q` में receive करेंगे।

तो, उस URL का response होगा:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

/// tip | टिप

ऊपर के example की तरह, `list` type वाला query parameter declare करने के लिए, आपको स्पष्ट रूप से `Query` use करना होगा, अन्यथा इसे request body के रूप में interpret किया जाएगा।

///

interactive API docs accordingly update होंगे, ताकि multiple values allow हो सकें:

<img src="/img/tutorial/query-params-str-validations/image02.png">

### Defaults के साथ Query parameter list / multiple values { #query-parameter-list-multiple-values-with-defaults }

अगर कोई values provide नहीं की गई हैं, तो आप values की default `list` भी define कर सकते हैं:

{* ../../docs_src/query_params_str_validations/tutorial012_an_py310.py hl[9] *}

अगर आप यहाँ जाते हैं:

```
http://localhost:8000/items/
```

`q` का default होगा: `["foo", "bar"]` और आपका response होगा:

```JSON
{
  "q": [
    "foo",
    "bar"
  ]
}
```

#### केवल `list` use करना { #using-just-list }

आप `list[str]` के बजाय सीधे `list` भी use कर सकते हैं:

{* ../../docs_src/query_params_str_validations/tutorial013_an_py310.py hl[9] *}

/// note | नोट

ध्यान रखें कि इस case में, FastAPI list की contents check नहीं करेगा।

उदाहरण के लिए, `list[int]` check (और document) करेगा कि list की contents integers हैं। लेकिन केवल `list` ऐसा नहीं करेगा।

///

## अधिक metadata declare करें { #declare-more-metadata }

आप parameter के बारे में अधिक जानकारी जोड़ सकते हैं।

वह जानकारी generated OpenAPI में शामिल होगी और documentation user interfaces और external tools द्वारा use की जाएगी।

/// note | नोट

ध्यान रखें कि अलग-अलग tools में OpenAPI support के अलग-अलग levels हो सकते हैं।

उनमें से कुछ अभी declare की गई सारी extra information नहीं दिखा सकते, हालांकि अधिकतर cases में, missing feature पहले से ही development के लिए planned है।

///

आप एक `title` जोड़ सकते हैं:

{* ../../docs_src/query_params_str_validations/tutorial007_an_py310.py hl[10] *}

और एक `description`:

{* ../../docs_src/query_params_str_validations/tutorial008_an_py310.py hl[14] *}

## Alias parameters { #alias-parameters }

कल्पना करें कि आप parameter को `item-query` बनाना चाहते हैं।

जैसे:

```
http://127.0.0.1:8000/items/?item-query=foobaritems
```

लेकिन `item-query` valid Python variable name नहीं है।

सबसे निकटतम `item_query` होगा।

लेकिन आपको अभी भी यह exactly `item-query` ही चाहिए...

तब आप एक `alias` declare कर सकते हैं, और वही alias parameter value खोजने के लिए use किया जाएगा:

{* ../../docs_src/query_params_str_validations/tutorial009_an_py310.py hl[9] *}

## Parameters को deprecate करना { #deprecating-parameters }

अब मान लीजिए कि आपको यह parameter अब पसंद नहीं है।

आपको इसे कुछ समय के लिए वहीं छोड़ना होगा क्योंकि clients इसे use कर रहे हैं, लेकिन आप चाहते हैं कि docs इसे स्पष्ट रूप से <dfn title="obsolete, इसका उपयोग न करने की recommendation है">deprecated</dfn> के रूप में दिखाएँ।

फिर parameter `deprecated=True` को `Query` में pass करें:

{* ../../docs_src/query_params_str_validations/tutorial010_an_py310.py hl[19] *}

docs इसे इस तरह दिखाएँगे:

<img src="/img/tutorial/query-params-str-validations/image01.png">

## OpenAPI से parameters exclude करें { #exclude-parameters-from-openapi }

generated OpenAPI schema से query parameter exclude करने के लिए (और इस प्रकार, automatic documentation systems से), `Query` के parameter `include_in_schema` को `False` पर set करें:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}

## Custom Validation { #custom-validation }

ऐसे cases हो सकते हैं जहाँ आपको कुछ **custom validation** करना पड़े जो ऊपर दिखाए गए parameters से नहीं किया जा सकता।

ऐसे cases में, आप एक **custom validator function** use कर सकते हैं जो normal validation के बाद apply होता है (जैसे value के `str` होने की validation के बाद)।

आप इसे `Annotated` के अंदर [Pydantic के `AfterValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator) का उपयोग करके हासिल कर सकते हैं।

/// tip | टिप

Pydantic में [`BeforeValidator`](https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator) और अन्य भी हैं। 🤓

///

उदाहरण के लिए, यह custom validator check करता है कि item ID किसी <abbr title="International Standard Book Number - अंतर्राष्ट्रीय मानक पुस्तक संख्या">ISBN</abbr> book number के लिए `isbn-` से शुरू होती है या किसी <abbr title="Internet Movie Database - इंटरनेट मूवी डेटाबेस: फिल्मों के बारे में जानकारी वाली एक वेबसाइट">IMDB</abbr> movie URL ID के लिए `imdb-` से:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py hl[5,16:19,24] *}

/// note | नोट

यह Pydantic version 2 या उससे ऊपर के साथ available है। 😎

///

/// tip | टिप

अगर आपको किसी भी प्रकार की validation करनी है जिसके लिए किसी **external component** से communicate करना required है, जैसे database या कोई अन्य API, तो आपको इसके बजाय **FastAPI Dependencies** use करनी चाहिए, आप इनके बारे में बाद में सीखेंगे।

ये custom validators उन चीज़ों के लिए हैं जिन्हें request में provide किए गए **सिर्फ** **उसी data** से check किया जा सकता है।

///

### उस Code को समझें { #understand-that-code }

महत्वपूर्ण बात बस **`Annotated` के अंदर एक function के साथ `AfterValidator` use करना** है। आप चाहें तो इस part को skip कर सकते हैं। 🤸

---

लेकिन अगर आप इस specific code example के बारे में curious हैं और अभी भी entertained हैं, तो यहाँ कुछ extra details हैं।

#### `value.startswith()` के साथ String { #string-with-value-startswith }

क्या आपने ध्यान दिया? `value.startswith()` use करने वाली string tuple ले सकती है, और यह tuple की हर value check करेगी:

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[16:19] hl[17] *}

#### एक Random Item { #a-random-item }

`data.items()` के साथ हमें tuples वाला एक <dfn title="ऐसी चीज़ जिस पर हम for loop से iterate कर सकते हैं, जैसे list, set, आदि।">iterable object</dfn> मिलता है जिसमें हर dictionary item के लिए key और value होती है।

हम इस iterable object को `list(data.items())` के साथ proper `list` में convert करते हैं।

फिर `random.choice()` के साथ हम list से एक **random value** प्राप्त कर सकते हैं, तो हमें `(id, name)` वाला tuple मिलता है। यह कुछ ऐसा होगा `("imdb-tt0371724", "The Hitchhiker's Guide to the Galaxy")`।

फिर हम tuple की **उन दो values को assign** करते हैं variables `id` और `name` को।

तो, अगर user ने item ID provide नहीं की, तब भी उन्हें एक random suggestion receive होगा।

...हम यह सब **एक single simple line** में करते हैं। 🤯 क्या आपको Python पसंद नहीं है? 🐍

{* ../../docs_src/query_params_str_validations/tutorial015_an_py310.py ln[22:30] hl[29] *}

## Recap { #recap }

आप अपने parameters के लिए अतिरिक्त validations और metadata declare कर सकते हैं।

Generic validations और metadata:

* `alias`
* `title`
* `description`
* `deprecated`

Strings के लिए specific validations:

* `min_length`
* `max_length`
* `pattern`

`AfterValidator` का उपयोग करके custom validations।

इन examples में आपने देखा कि `str` values के लिए validations कैसे declare करें।

अगले chapters देखें ताकि आप सीख सकें कि numbers जैसे अन्य types के लिए validations कैसे declare करें।
