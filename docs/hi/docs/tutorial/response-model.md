# Response Model - Return Type { #response-model-return-type }

आप response के लिए उपयोग किए जाने वाले type को *path operation function* के **return type** को annotate करके declare कर सकते हैं।

आप **type annotations** का उपयोग उसी तरह कर सकते हैं जैसे आप function **parameters** में input data के लिए करते हैं, आप Pydantic models, lists, dictionaries, scalar values जैसे integers, booleans, आदि का उपयोग कर सकते हैं।

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

FastAPI इस return type का उपयोग इनके लिए करेगा:

* लौटाए गए data को **Validate** करना।
    * अगर data invalid है (जैसे कि कोई field missing है), तो इसका मतलब है कि *आपके* app code में गड़बड़ी है, वह वह data return नहीं कर रहा जो उसे करना चाहिए, और यह incorrect data return करने के बजाय server error return करेगा। इस तरह आप और आपके clients सुनिश्चित हो सकते हैं कि उन्हें expected data और data shape मिलेगा।
* OpenAPI *path operation* में response के लिए एक **JSON Schema** जोड़ना।
    * इसका उपयोग **automatic docs** द्वारा किया जाएगा।
    * इसका उपयोग automatic client code generation tools द्वारा भी किया जाएगा।
* Pydantic का उपयोग करके लौटाए गए data को JSON में **Serialize** करना, जो **Rust** में लिखा गया है, इसलिए यह **बहुत तेज़** होगा।

लेकिन सबसे महत्वपूर्ण:

* यह output data को return type में defined data तक **limit और filter** करेगा।
    * यह **security** के लिए विशेष रूप से महत्वपूर्ण है, हम नीचे इसका और अधिक देखेंगे।

## `response_model` Parameter { #response-model-parameter }

कुछ cases ऐसे होते हैं जहाँ आपको ऐसा data return करना होता है या आप ऐसा करना चाहते हैं जो type द्वारा declare किए गए data से बिल्कुल मेल नहीं खाता।

उदाहरण के लिए, आप **dictionary return** करना या database object return करना चाह सकते हैं, लेकिन **उसे Pydantic model के रूप में declare** करना चाह सकते हैं। इस तरह Pydantic model आपके द्वारा लौटाए गए object (जैसे dictionary या database object) के लिए सभी data documentation, validation, आदि करेगा।

अगर आपने return type annotation जोड़ा, तो tools और editors एक (सही) error के साथ शिकायत करेंगे कि आपका function ऐसा type (जैसे dict) return कर रहा है जो आपके द्वारा declare किए गए type (जैसे Pydantic model) से अलग है।

ऐसे cases में, आप return type के बजाय *path operation decorator* parameter `response_model` का उपयोग कर सकते हैं।

आप किसी भी *path operations* में `response_model` parameter का उपयोग कर सकते हैं:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* आदि।

{* ../../docs_src/response_model/tutorial001_py310.py hl[17,22,24:27] *}

/// note | नोट

ध्यान दें कि `response_model` "decorator" method (`get`, `post`, आदि) का parameter है। यह आपके *path operation function* का parameter नहीं है, जैसे सभी parameters और body होते हैं।

///

`response_model` वही type receive करता है जिसे आप Pydantic model field के लिए declare करेंगे, इसलिए यह Pydantic model हो सकता है, लेकिन यह, जैसे कि `List[Item]` की तरह Pydantic models की `list` भी हो सकता है।

FastAPI इस `response_model` का उपयोग सभी data documentation, validation, आदि के लिए करेगा और output data को इसके type declaration में **convert और filter** भी करेगा।

/// tip | सुझाव

अगर आपके editor, mypy, आदि में strict type checks हैं, तो आप function return type को `Any` के रूप में declare कर सकते हैं।

इस तरह आप editor को बताते हैं कि आप जानबूझकर कुछ भी return कर रहे हैं। लेकिन FastAPI फिर भी `response_model` के साथ data documentation, validation, filtering, आदि करेगा।

///

### `response_model` Priority { #response-model-priority }

अगर आप return type और `response_model` दोनों declare करते हैं, तो `response_model` को priority मिलेगी और FastAPI द्वारा इसका उपयोग किया जाएगा।

इस तरह आप अपने functions में सही type annotations जोड़ सकते हैं, भले ही आप response model से अलग type return कर रहे हों, ताकि editor और mypy जैसे tools उनका उपयोग कर सकें। और फिर भी FastAPI `response_model` का उपयोग करके data validation, documentation, आदि कर सकता है।

आप उस *path operation* के लिए response model बनाना disable करने के लिए `response_model=None` का भी उपयोग कर सकते हैं, आपको ऐसा तब करना पड़ सकता है जब आप उन चीज़ों के लिए type annotations जोड़ रहे हों जो valid Pydantic fields नहीं हैं, आप नीचे के sections में से एक में इसका उदाहरण देखेंगे।

## वही input data return करें { #return-the-same-input-data }

यहाँ हम एक `UserIn` model declare कर रहे हैं, इसमें plaintext password होगा:

{* ../../docs_src/response_model/tutorial002_py310.py hl[7,9] *}

/// note | नोट

`EmailStr` का उपयोग करने के लिए, पहले [`email-validator`](https://github.com/JoshData/python-email-validator) install करें।

सुनिश्चित करें कि आप एक [virtual environment](../virtual-environments.md) बनाते हैं, उसे activate करते हैं, और फिर इसे install करते हैं, उदाहरण के लिए:

```console
$ pip install email-validator
```

या इसके साथ:

```console
$ pip install "pydantic[email]"
```

///

और हम इस model का उपयोग अपने input को declare करने और उसी model का उपयोग अपने output को declare करने के लिए कर रहे हैं:

{* ../../docs_src/response_model/tutorial002_py310.py hl[16] *}

अब, जब भी कोई browser password के साथ user बना रहा होगा, API response में वही password return करेगी।

इस case में, यह problem नहीं हो सकती, क्योंकि password भेजने वाला वही user है।

लेकिन अगर हम उसी model का उपयोग किसी और *path operation* के लिए करते हैं, तो हम अपने user के passwords हर client को भेज सकते हैं।

/// danger | खतरा

कभी भी किसी user का plain password store न करें या उसे इस तरह response में न भेजें, जब तक कि आप सभी caveats नहीं जानते और यह नहीं जानते कि आप क्या कर रहे हैं।

///

## Output model जोड़ें { #add-an-output-model }

इसके बजाय हम plaintext password के साथ एक input model और उसके बिना एक output model बना सकते हैं:

{* ../../docs_src/response_model/tutorial003_py310.py hl[9,11,16] *}

यहाँ, भले ही हमारा *path operation function* वही input user return कर रहा है जिसमें password शामिल है:

{* ../../docs_src/response_model/tutorial003_py310.py hl[24] *}

...हमने `response_model` को अपना model `UserOut` declare किया है, जिसमें password शामिल नहीं है:

{* ../../docs_src/response_model/tutorial003_py310.py hl[22] *}

इसलिए, **FastAPI** output model में declare न किए गए सभी data को filter out करने का ध्यान रखेगा (Pydantic का उपयोग करके)।

### `response_model` या Return Type { #response-model-or-return-type }

इस case में, क्योंकि दोनों models अलग हैं, अगर हमने function return type को `UserOut` के रूप में annotate किया, तो editor और tools शिकायत करेंगे कि हम invalid type return कर रहे हैं, क्योंकि वे अलग classes हैं।

इसीलिए इस उदाहरण में हमें इसे `response_model` parameter में declare करना पड़ता है।

...लेकिन इसे कैसे overcome किया जाए, यह देखने के लिए नीचे पढ़ना जारी रखें।

## Return Type और Data Filtering { #return-type-and-data-filtering }

आइए पिछले उदाहरण से आगे बढ़ते हैं। हम **function को एक type के साथ annotate** करना चाहते थे, लेकिन हम function से ऐसा कुछ return कर पाना चाहते थे जिसमें वास्तव में **अधिक data** शामिल हो।

हम चाहते हैं कि FastAPI response model का उपयोग करके data को **filter** करता रहे। ताकि भले ही function अधिक data return करे, response में केवल वही fields शामिल हों जो response model में declare किए गए हैं।

पिछले उदाहरण में, क्योंकि classes अलग थीं, हमें `response_model` parameter का उपयोग करना पड़ा। लेकिन इसका मतलब यह भी है कि हमें function return type check करने वाले editor और tools से support नहीं मिलता।

लेकिन अधिकतर cases में जहाँ हमें ऐसा कुछ करना होता है, हम चाहते हैं कि model बस इस उदाहरण की तरह कुछ data को **filter/remove** करे।

और उन cases में, हम classes और inheritance का उपयोग करके function **type annotations** का लाभ उठा सकते हैं ताकि editor और tools में बेहतर support मिले, और फिर भी FastAPI **data filtering** मिल सके।

{* ../../docs_src/response_model/tutorial003_01_py310.py hl[7:10,13:14,18] *}

इसके साथ, हमें editors और mypy से tooling support मिलता है क्योंकि यह code types के संदर्भ में सही है, लेकिन हमें FastAPI से data filtering भी मिलती है।

यह कैसे काम करता है? आइए इसे देखें। 🤓

### Type Annotations और Tooling { #type-annotations-and-tooling }

पहले देखते हैं कि editors, mypy और अन्य tools इसे कैसे देखेंगे।

`BaseUser` में base fields हैं। फिर `UserIn`, `BaseUser` से inherit करता है और `password` field जोड़ता है, इसलिए इसमें दोनों models के सभी fields शामिल होंगे।

हम function return type को `BaseUser` के रूप में annotate करते हैं, लेकिन वास्तव में हम `UserIn` instance return कर रहे हैं।

Editor, mypy, और अन्य tools इस पर शिकायत नहीं करेंगे क्योंकि typing terms में, `UserIn`, `BaseUser` का subclass है, जिसका मतलब है कि जब expected कुछ भी `BaseUser` हो, तो यह एक *valid* type है।

### FastAPI Data Filtering { #fastapi-data-filtering }

अब, FastAPI के लिए, यह return type देखेगा और सुनिश्चित करेगा कि आप जो return करते हैं उसमें **केवल** वही fields शामिल हों जो type में declare किए गए हैं।

FastAPI internally Pydantic के साथ कई चीज़ें करता है ताकि यह सुनिश्चित हो सके कि class inheritance के वही rules returned data filtering के लिए उपयोग न किए जाएँ, नहीं तो आप expected से कहीं अधिक data return कर सकते हैं।

इस तरह, आप दोनों दुनिया का best पा सकते हैं: **tooling support** के साथ type annotations और **data filtering**।

## इसे docs में देखें { #see-it-in-the-docs }

जब आप automatic docs देखते हैं, तो आप check कर सकते हैं कि input model और output model दोनों का अपना JSON Schema होगा:

<img src="/img/tutorial/response-model/image01.png">

और दोनों models interactive API documentation के लिए उपयोग किए जाएँगे:

<img src="/img/tutorial/response-model/image02.png">

## अन्य Return Type Annotations { #other-return-type-annotations }

ऐसे cases हो सकते हैं जहाँ आप कुछ ऐसा return करते हैं जो valid Pydantic field नहीं है और आप उसे function में annotate करते हैं, केवल tooling (editor, mypy, आदि) द्वारा दिए गए support को पाने के लिए।

### सीधे Response Return करें { #return-a-response-directly }

सबसे common case होगा [advanced docs में बाद में समझाए अनुसार सीधे Response return करना](../advanced/response-directly.md)।

{* ../../docs_src/response_model/tutorial003_02_py310.py hl[8,10:11] *}

यह simple case FastAPI द्वारा automatically handle किया जाता है क्योंकि return type annotation `Response` class (या उसका subclass) है।

और tools भी खुश होंगे क्योंकि `RedirectResponse` और `JSONResponse` दोनों `Response` के subclasses हैं, इसलिए type annotation सही है।

### Response Subclass Annotate करें { #annotate-a-response-subclass }

आप type annotation में `Response` के subclass का भी उपयोग कर सकते हैं:

{* ../../docs_src/response_model/tutorial003_03_py310.py hl[8:9] *}

यह भी काम करेगा क्योंकि `RedirectResponse`, `Response` का subclass है, और FastAPI इस simple case को automatically handle करेगा।

### Invalid Return Type Annotations { #invalid-return-type-annotations }

लेकिन जब आप कोई अन्य arbitrary object return करते हैं जो valid Pydantic type नहीं है (जैसे database object) और आप उसे function में उसी तरह annotate करते हैं, तो FastAPI उस type annotation से Pydantic response model बनाने की कोशिश करेगा, और fail हो जाएगा।

ऐसा ही होगा अगर आपके पास अलग-अलग types के बीच <dfn title='कई types के बीच union का मतलब है "इनमें से कोई भी type".'>union</dfn> जैसा कुछ हो जहाँ उनमें से एक या अधिक valid Pydantic types नहीं हैं, उदाहरण के लिए यह fail होगा 💥:

{* ../../docs_src/response_model/tutorial003_04_py310.py hl[8] *}

...यह fail होता है क्योंकि type annotation Pydantic type नहीं है और केवल एक single `Response` class या subclass भी नहीं है, यह `Response` और `dict` के बीच union (दोनों में से कोई भी) है।

### Response Model Disable करें { #disable-response-model }

ऊपर दिए गए उदाहरण से आगे बढ़ते हुए, आप शायद default data validation, documentation, filtering, आदि नहीं चाहते हों जो FastAPI द्वारा किया जाता है।

लेकिन आप शायद function में return type annotation फिर भी रखना चाहते हों ताकि editors और type checkers (जैसे mypy) जैसे tools से support मिल सके।

इस case में, आप `response_model=None` set करके response model generation disable कर सकते हैं:

{* ../../docs_src/response_model/tutorial003_05_py310.py hl[7] *}

इससे FastAPI response model generation skip कर देगा और इस तरह आप अपनी जरूरत के किसी भी return type annotations का उपयोग कर सकते हैं, बिना इसके कि वह आपकी FastAPI application को प्रभावित करे। 🤓

## Response Model encoding parameters { #response-model-encoding-parameters }

आपके response model में default values हो सकते हैं, जैसे:

{* ../../docs_src/response_model/tutorial004_py310.py hl[9,11:12] *}

* `description: Union[str, None] = None` (या Python 3.10 में `str | None = None`) का default `None` है।
* `tax: float = 10.5` का default `10.5` है।
* `tags: List[str] = []` का default खाली list है: `[]`।

लेकिन अगर वे वास्तव में store नहीं किए गए थे तो आप उन्हें result से omit करना चाह सकते हैं।

उदाहरण के लिए, अगर आपके पास NoSQL database में कई optional attributes वाले models हैं, लेकिन आप default values से भरे बहुत लंबे JSON responses नहीं भेजना चाहते।

### `response_model_exclude_unset` parameter का उपयोग करें { #use-the-response-model-exclude-unset-parameter }

आप *path operation decorator* parameter `response_model_exclude_unset=True` set कर सकते हैं:

{* ../../docs_src/response_model/tutorial004_py310.py hl[22] *}

और वे default values response में शामिल नहीं होंगे, केवल वास्तव में set किए गए values ही शामिल होंगे।

तो, अगर आप ID `foo` वाले item के लिए उस *path operation* को request भेजते हैं, तो response (default values शामिल किए बिना) होगा:

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

/// note | नोट

आप इसका भी उपयोग कर सकते हैं:

* `response_model_exclude_defaults=True`
* `response_model_exclude_none=True`

जैसा कि `exclude_defaults` और `exclude_none` के लिए [Pydantic docs](https://docs.pydantic.dev/1.10/usage/exporting_models/#modeldict) में बताया गया है।

///

#### Defaults वाले fields के लिए values वाला data { #data-with-values-for-fields-with-defaults }

लेकिन अगर आपके data में model के default values वाले fields के लिए values हैं, जैसे ID `bar` वाला item:

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

तो वे response में शामिल होंगे।

#### Defaults जैसे ही values वाला data { #data-with-the-same-values-as-the-defaults }

अगर data में default values जैसे ही values हैं, जैसे ID `baz` वाला item:

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI इतना smart है (दरअसल, Pydantic इतना smart है) कि यह समझ सके कि, भले ही `description`, `tax`, और `tags` के values defaults जैसे ही हैं, उन्हें explicitly set किया गया था (defaults से लिए जाने के बजाय)।

इसलिए, वे JSON response में शामिल होंगे।

/// tip | सुझाव

ध्यान दें कि default values कुछ भी हो सकते हैं, केवल `None` नहीं।

वे list (`[]`), `10.5` का `float`, आदि हो सकते हैं।

///

### `response_model_include` और `response_model_exclude` { #response-model-include-and-response-model-exclude }

आप *path operation decorator* parameters `response_model_include` और `response_model_exclude` का भी उपयोग कर सकते हैं।

वे include करने के लिए attributes के नामों वाला `str` का `set` लेते हैं (बाकी को omit करते हुए) या exclude करने के लिए (बाकी को include करते हुए)।

अगर आपके पास केवल एक Pydantic model है और आप output से कुछ data remove करना चाहते हैं, तो इसे quick shortcut के रूप में उपयोग किया जा सकता है।

/// tip | सुझाव

लेकिन फिर भी इन parameters के बजाय, multiple classes का उपयोग करते हुए, ऊपर दिए गए ideas का उपयोग करने की recommendation है।

ऐसा इसलिए है क्योंकि आपके app के OpenAPI (और docs) में generated JSON Schema फिर भी complete model के लिए ही होगा, भले ही आप कुछ attributes omit करने के लिए `response_model_include` या `response_model_exclude` का उपयोग करें।

यह `response_model_by_alias` पर भी लागू होता है जो इसी तरह काम करता है।

///

{* ../../docs_src/response_model/tutorial005_py310.py hl[29,35] *}

/// tip | सुझाव

Syntax `{"name", "description"}` उन दो values के साथ एक `set` बनाता है।

यह `set(["name", "description"])` के equivalent है।

///

#### `set`s के बजाय `list`s का उपयोग करना { #using-lists-instead-of-sets }

अगर आप `set` का उपयोग करना भूल जाते हैं और इसके बजाय `list` या `tuple` का उपयोग करते हैं, तो FastAPI फिर भी उसे `set` में convert कर देगा और यह सही तरह काम करेगा:

{* ../../docs_src/response_model/tutorial006_py310.py hl[29,35] *}

## Recap { #recap }

Response models define करने और खासकर private data को filter out करना सुनिश्चित करने के लिए *path operation decorator* के parameter `response_model` का उपयोग करें।

केवल explicitly set किए गए values return करने के लिए `response_model_exclude_unset` का उपयोग करें।
