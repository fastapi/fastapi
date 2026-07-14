# Lifespan Events { #lifespan-events }

आप ऐसी logic (code) define कर सकते हैं जिसे application के **starts up** होने से पहले execute किया जाना चाहिए। इसका मतलब है कि यह code application के **requests receive करना शुरू करने से पहले**, **एक बार** execute होगा।

उसी तरह, आप ऐसी logic (code) define कर सकते हैं जिसे application के **shutting down** होने पर execute किया जाना चाहिए। इस मामले में, यह code संभवतः **कई requests** handle करने के **बाद**, **एक बार** execute होगा।

क्योंकि यह code application के requests लेना **शुरू** करने से पहले, और requests handle करना **पूरा** करने के तुरंत बाद execute होता है, यह पूरी application **lifespan** को cover करता है (शब्द "lifespan" थोड़ी देर में महत्वपूर्ण होगा 😉)।

यह उन **resources** को setup करने के लिए बहुत उपयोगी हो सकता है जिनकी आपको पूरी app में जरूरत होती है, और जो requests के बीच **shared** होते हैं, और/या जिन्हें आपको बाद में **clean up** करना होता है। उदाहरण के लिए, database connection pool, या कोई shared machine learning model load करना।

## Use Case { #use-case }

आइए एक उदाहरण **use case** से शुरू करते हैं और फिर देखते हैं कि इसे इससे कैसे solve किया जाए।

मान लीजिए कि आपके पास कुछ **machine learning models** हैं जिन्हें आप requests handle करने के लिए use करना चाहते हैं। 🤖

वही models requests के बीच shared हैं, इसलिए, यह हर request के लिए एक model, या हर user के लिए एक model या ऐसा कुछ नहीं है।

मान लीजिए कि model load करने में **काफी समय लग सकता है**, क्योंकि उसे disk से बहुत सारा **data** read करना होता है। इसलिए आप इसे हर request के लिए नहीं करना चाहते।

आप इसे module/file के top level पर load कर सकते हैं, लेकिन इसका मतलब यह भी होगा कि अगर आप सिर्फ एक simple automated test run कर रहे हैं, तब भी यह **model load** करेगा, और फिर वह test **slow** होगा क्योंकि code के किसी independent part को run कर पाने से पहले उसे model load होने का इंतजार करना पड़ेगा।

यही हम solve करेंगे, चलिए model को requests handle होने से पहले load करते हैं, लेकिन केवल application के requests receive करना शुरू करने से ठीक पहले, code load होते समय नहीं।

## Lifespan { #lifespan }

आप `FastAPI` app के `lifespan` parameter और एक "context manager" (मैं अभी दिखाऊंगा कि यह क्या है) का use करके यह *startup* और *shutdown* logic define कर सकते हैं।

आइए एक उदाहरण से शुरू करते हैं और फिर इसे detail में देखते हैं।

हम `yield` के साथ एक async function `lifespan()` इस तरह create करते हैं:

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

यहां हम `yield` से पहले machine learning models वाली dictionary में (fake) model function रखकर model load करने वाली महंगी *startup* operation को simulate कर रहे हैं। यह code application के **requests लेना शुरू करने से पहले**, *startup* के दौरान execute होगा।

और फिर, `yield` के तुरंत बाद, हम model unload करते हैं। यह code application के **requests handle करना पूरा करने के बाद**, *shutdown* से ठीक पहले execute होगा। उदाहरण के लिए, यह memory या GPU जैसे resources release कर सकता है।

/// tip | सुझाव

`shutdown` तब होगा जब आप application को **stop** कर रहे होंगे।

शायद आपको कोई नया version start करना हो, या आप इसे चलाते-चलाते बस थक गए हों। 🤷

///

### Lifespan function { #lifespan-function }

ध्यान देने वाली पहली चीज यह है कि हम `yield` के साथ एक async function define कर रहे हैं। यह `yield` वाली Dependencies से बहुत मिलता-जुलता है।

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

function का पहला हिस्सा, `yield` से पहले वाला, application start होने से **पहले** execute होगा।

और `yield` के बाद वाला हिस्सा application के finish हो जाने के **बाद** execute होगा।

### Async Context Manager { #async-context-manager }

अगर आप check करें, तो function को `@asynccontextmanager` से decorate किया गया है।

यह function को "**async context manager**" नाम की चीज में convert करता है।

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Python में एक **context manager** ऐसी चीज है जिसे आप `with` statement में use कर सकते हैं, उदाहरण के लिए, `open()` को context manager की तरह use किया जा सकता है:

```Python
with open("file.txt") as file:
    file.read()
```

Python के नए versions में, एक **async context manager** भी है। आप इसे `async with` के साथ use करेंगे:

```Python
async with lifespan(app):
    await do_stuff()
```

जब आप ऊपर की तरह कोई context manager या async context manager create करते हैं, तो यह क्या करता है कि `with` block में enter करने से पहले, यह `yield` से पहले वाला code execute करेगा, और `with` block से exit करने के बाद, यह `yield` के बाद वाला code execute करेगा।

ऊपर हमारे code example में, हम इसे सीधे use नहीं करते, बल्कि FastAPI को pass करते हैं ताकि वह इसे use कर सके।

`FastAPI` app का `lifespan` parameter एक **async context manager** लेता है, इसलिए हम अपना नया `lifespan` async context manager उसे pass कर सकते हैं।

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## Alternative Events (deprecated) { #alternative-events-deprecated }

/// warning | चेतावनी

*startup* और *shutdown* को handle करने का recommended तरीका ऊपर बताए गए अनुसार `FastAPI` app के `lifespan` parameter का use करना है। अगर आप `lifespan` parameter provide करते हैं, तो `startup` और `shutdown` event handlers अब call नहीं किए जाएंगे। यह पूरा `lifespan` होगा या पूरे events, दोनों नहीं।

आप शायद यह हिस्सा skip कर सकते हैं।

///

इस logic को *startup* के दौरान और *shutdown* के दौरान execute करने के लिए define करने का एक alternative तरीका है।

आप event handlers (functions) define कर सकते हैं जिन्हें application के starts up होने से पहले, या application के shutting down होने पर execute किया जाना चाहिए।

इन functions को `async def` या normal `def` के साथ declare किया जा सकता है।

### `startup` event { #startup-event }

application start होने से पहले run होने वाला function add करने के लिए, इसे event `"startup"` के साथ declare करें:

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

इस मामले में, `startup` event handler function items "database" (बस एक `dict`) को कुछ values के साथ initialize करेगा।

आप एक से अधिक event handler function add कर सकते हैं।

और आपकी application requests receive करना तब तक शुरू नहीं करेगी जब तक सभी `startup` event handlers complete नहीं हो जाते।

### `shutdown` event { #shutdown-event }

application के shutting down होने पर run होने वाला function add करने के लिए, इसे event `"shutdown"` के साथ declare करें:

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

यहां, `shutdown` event handler function एक text line `"Application shutdown"` को `log.txt` file में write करेगा।

/// note | नोट

`open()` function में, `mode="a"` का मतलब "append" होता है, इसलिए, line उस file में जो भी है उसके बाद add की जाएगी, पिछले contents को overwrite किए बिना।

///

/// tip | सुझाव

ध्यान दें कि इस मामले में हम एक standard Python `open()` function use कर रहे हैं जो एक file के साथ interact करता है।

इसलिए, इसमें I/O (input/output) शामिल है, जिसके लिए चीजों के disk पर write होने का "waiting" करना पड़ता है।

लेकिन `open()` `async` और `await` use नहीं करता।

इसलिए, हम event handler function को `async def` के बजाय standard `def` के साथ declare करते हैं।

///

### `startup` और `shutdown` साथ में { #startup-and-shutdown-together }

इस बात की काफी संभावना है कि आपके *startup* और *shutdown* की logic connected हो, आप शायद कुछ start करना और फिर उसे finish करना, कोई resource acquire करना और फिर उसे release करना, आदि चाहें।

इसे अलग-अलग functions में करना, जो logic या variables को साथ में share नहीं करते, अधिक कठिन है क्योंकि आपको values को global variables या इसी तरह की tricks में store करना पड़ेगा।

इसी वजह से, अब इसके बजाय ऊपर explain किए गए `lifespan` को use करने की recommendation है।

## Technical Details { #technical-details }

जिज्ञासु nerds के लिए बस एक technical detail। 🤓

अंदर से, ASGI technical specification में, यह [Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html) का हिस्सा है, और यह `startup` और `shutdown` नाम के events define करता है।

/// note | नोट

आप Starlette `lifespan` handlers के बारे में [Starlette की Lifespan docs](https://www.starlette.dev/lifespan/) में और पढ़ सकते हैं।

इसमें यह भी शामिल है कि lifespan state को कैसे handle किया जाए जिसे आपके code के अन्य areas में use किया जा सकता है।

///

## Sub Applications { #sub-applications }

🚨 ध्यान रखें कि ये lifespan events (startup और shutdown) केवल main application के लिए execute होंगे, [Sub Applications - Mounts](sub-applications.md) के लिए नहीं।
