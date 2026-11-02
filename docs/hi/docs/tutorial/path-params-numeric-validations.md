# Path Parameters और संख्यात्मक Validations { #path-parameters-and-numeric-validations }

जिस तरह आप `Query` के साथ query parameters के लिए अधिक validations और metadata घोषित कर सकते हैं, उसी तरह आप `Path` के साथ path parameters के लिए उसी प्रकार की validations और metadata घोषित कर सकते हैं।

## `Path` import करें { #import-path }

सबसे पहले, `fastapi` से `Path` import करें, और `Annotated` import करें:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// note | नोट

FastAPI ने version 0.95.0 में `Annotated` के लिए support जोड़ा था (और इसकी सिफारिश करना शुरू किया था)।

अगर आपके पास पुराना version है, तो `Annotated` का उपयोग करने की कोशिश करते समय आपको errors मिलेंगे।

`Annotated` का उपयोग करने से पहले सुनिश्चित करें कि आप [FastAPI version को Upgrade करें](../deployment/versions.md#upgrading-the-fastapi-versions) कम से कम 0.95.1 तक।

///

## Metadata घोषित करें { #declare-metadata }

आप `Query` के लिए जैसे सभी parameters घोषित करते हैं, वैसे ही यहाँ भी कर सकते हैं।

उदाहरण के लिए, path parameter `item_id` के लिए `title` metadata value घोषित करने के लिए आप लिख सकते हैं:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | नोट

एक path parameter हमेशा required होता है क्योंकि उसे path का हिस्सा होना होता है। भले ही आपने इसे `None` के साथ घोषित किया हो या कोई default value सेट की हो, इससे कुछ भी प्रभावित नहीं होगा, यह फिर भी हमेशा required रहेगा।

///

## Parameters को अपनी ज़रूरत के अनुसार क्रम दें { #order-the-parameters-as-you-need }

/// tip | सुझाव

यदि आप `Annotated` का उपयोग करते हैं, तो यह शायद उतना महत्वपूर्ण या ज़रूरी नहीं है।

///

मान लें कि आप query parameter `q` को required `str` के रूप में घोषित करना चाहते हैं।

और आपको उस parameter के लिए कुछ और घोषित करने की ज़रूरत नहीं है, इसलिए वास्तव में आपको `Query` का उपयोग करने की ज़रूरत नहीं है।

लेकिन आपको फिर भी `item_id` path parameter के लिए `Path` का उपयोग करना होगा। और किसी कारण से आप `Annotated` का उपयोग नहीं करना चाहते।

यदि आप किसी ऐसे value को, जिसके पास "default" है, ऐसे value से पहले रखते हैं जिसके पास "default" नहीं है, तो Python शिकायत करेगा।

लेकिन आप उनका क्रम बदल सकते हैं, और बिना default वाले value (query parameter `q`) को पहले रख सकते हैं।

**FastAPI** के लिए इससे फर्क नहीं पड़ता। यह parameters को उनके नामों, types और default declarations (`Query`, `Path`, आदि) से पहचान लेगा, इसे क्रम से कोई फर्क नहीं पड़ता।

तो, आप अपनी function इस तरह घोषित कर सकते हैं:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

लेकिन ध्यान रखें कि यदि आप `Annotated` का उपयोग करते हैं, तो आपको यह समस्या नहीं होगी, क्योंकि आप `Query()` या `Path()` के लिए function parameter default values का उपयोग नहीं कर रहे हैं।

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## Parameters को अपनी ज़रूरत के अनुसार क्रम दें, tricks { #order-the-parameters-as-you-need-tricks }

/// tip | सुझाव

यदि आप `Annotated` का उपयोग करते हैं, तो यह शायद उतना महत्वपूर्ण या ज़रूरी नहीं है।

///

यहाँ एक **छोटी trick** है जो काम आ सकती है, लेकिन आपको इसकी अक्सर ज़रूरत नहीं पड़ेगी।

यदि आप चाहते हैं कि:

* `q` query parameter को बिना `Query` और बिना किसी default value के घोषित करें
* path parameter `item_id` को `Path` का उपयोग करके घोषित करें
* उन्हें अलग क्रम में रखें
* `Annotated` का उपयोग न करें

...तो Python में इसके लिए एक छोटी विशेष syntax है।

function के पहले parameter के रूप में `*` पास करें।

Python उस `*` के साथ कुछ नहीं करेगा, लेकिन उसे पता चल जाएगा कि उसके बाद आने वाले सभी parameters को keyword arguments (key-value pairs) के रूप में call किया जाना चाहिए, जिन्हें <abbr title="From: K-ey W-ord Arg-uments - से: K-ey W-ord Arg-uments"><code>kwargs</code></abbr> भी कहा जाता है। भले ही उनके पास default value न हो।

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### `Annotated` के साथ बेहतर { #better-with-annotated }

ध्यान रखें कि यदि आप `Annotated` का उपयोग करते हैं, तो चूँकि आप function parameter default values का उपयोग नहीं कर रहे हैं, आपको यह समस्या नहीं होगी, और शायद आपको `*` का उपयोग करने की ज़रूरत नहीं पड़ेगी।

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## Number validations: greater than or equal { #number-validations-greater-than-or-equal }

`Query` और `Path` (और अन्य जिन्हें आप बाद में देखेंगे) के साथ आप number constraints घोषित कर सकते हैं।

यहाँ, `ge=1` के साथ, `item_id` को `1` से "`g`reater than or `e`qual" integer number होना होगा।

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## Number validations: greater than और less than or equal { #number-validations-greater-than-and-less-than-or-equal }

यही बात इन पर भी लागू होती है:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## Number validations: floats, greater than और less than { #number-validations-floats-greater-than-and-less-than }

Number validations `float` values के लिए भी काम करती हैं।

यहीं पर <abbr title="greater than - इससे अधिक"><code>gt</code></abbr> घोषित कर पाना महत्वपूर्ण हो जाता है, सिर्फ <abbr title="greater than or equal - इससे अधिक या बराबर"><code>ge</code></abbr> नहीं। क्योंकि इसके साथ आप, उदाहरण के लिए, यह require कर सकते हैं कि कोई value `0` से अधिक होनी चाहिए, भले ही वह `1` से कम हो।

तो, `0.5` एक valid value होगा। लेकिन `0.0` या `0` नहीं होंगे।

और यही बात <abbr title="less than - इससे कम"><code>lt</code></abbr> के लिए भी है।

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## Recap { #recap }

`Query`, `Path` (और अन्य जिन्हें आपने अभी तक नहीं देखा है) के साथ आप metadata और string validations उसी तरह घोषित कर सकते हैं जैसे [Query Parameters और String Validations](query-params-str-validations.md) के साथ।

और आप numeric validations भी घोषित कर सकते हैं:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// note | नोट

`Query`, `Path`, और अन्य classes जिन्हें आप बाद में देखेंगे, एक common `Param` class की subclasses हैं।

वे सभी अतिरिक्त validation और metadata के लिए वही parameters साझा करती हैं जिन्हें आपने देखा है।

///

/// note | तकनीकी विवरण

जब आप `fastapi` से `Query`, `Path` और अन्य import करते हैं, तो वे वास्तव में functions होते हैं।

जब उन्हें call किया जाता है, तो वे उसी नाम की classes के instances return करते हैं।

तो, आप `Query` import करते हैं, जो एक function है। और जब आप इसे call करते हैं, तो यह `Query` नाम की class का एक instance return करता है।

ये functions इसलिए हैं (classes को सीधे उपयोग करने के बजाय) ताकि आपका editor उनके types के बारे में errors mark न करे।

इस तरह आप उन errors को ignore करने के लिए custom configurations जोड़े बिना अपने सामान्य editor और coding tools का उपयोग कर सकते हैं।

///
