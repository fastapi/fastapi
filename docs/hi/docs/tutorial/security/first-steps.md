# सुरक्षा - पहले कदम { #security-first-steps }

मान लें कि आपका **backend** API किसी domain में है।

और आपका **frontend** किसी दूसरे domain में है या उसी domain के किसी अलग path में है (या किसी mobile application में)।

और आप चाहते हैं कि frontend, **username** और **password** का उपयोग करके backend के साथ authenticate कर सके।

हम इसे **FastAPI** के साथ बनाने के लिए **OAuth2** का उपयोग कर सकते हैं।

लेकिन आपको केवल वे छोटी-छोटी जानकारियाँ खोजने के लिए पूरी लंबी specification पढ़ने में समय न लगाना पड़े।

आइए सुरक्षा संभालने के लिए **FastAPI** द्वारा दिए गए tools का उपयोग करें।

## यह कैसा दिखता है { #how-it-looks }

आइए पहले बस code का उपयोग करें और देखें कि यह कैसे काम करता है, और फिर हम वापस आकर समझेंगे कि क्या हो रहा है।

## `main.py` बनाएँ { #create-main-py }

उदाहरण को एक file `main.py` में copy करें:

{* ../../docs_src/security/tutorial001_an_py310.py *}

## इसे चलाएँ { #run-it }

/// note | नोट

[`python-multipart`](https://github.com/Kludex/python-multipart) package **FastAPI** के साथ अपने-आप install हो जाता है जब आप `pip install "fastapi[standard]"` command चलाते हैं।

हालाँकि, अगर आप `pip install fastapi` command का उपयोग करते हैं, तो `python-multipart` package default रूप से शामिल नहीं होता।

इसे manually install करने के लिए, सुनिश्चित करें कि आप एक [virtual environment](../../virtual-environments.md) बनाएँ, उसे activate करें, और फिर इसे इस तरह install करें:

```console
$ pip install python-multipart
```

ऐसा इसलिए है क्योंकि **OAuth2**, `username` और `password` भेजने के लिए "form data" का उपयोग करता है।

///

उदाहरण को इस तरह चलाएँ:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## इसे जाँचें { #check-it }

Interactive docs पर जाएँ: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

आपको कुछ ऐसा दिखाई देगा:

<img src="/img/tutorial/security/image01.png">

/// tip | Authorize बटन!

आपके पास पहले से ही एक चमकदार नया "Authorize" बटन है।

और आपकी *path operation* के ऊपर-दाएँ कोने में एक छोटा-सा lock है जिस पर आप click कर सकते हैं।

///

और अगर आप उस पर click करते हैं, तो आपके पास `username` और `password` (और अन्य optional fields) type करने के लिए एक छोटा authorization form होगा:

<img src="/img/tutorial/security/image02.png">

/// note | नोट

आप form में क्या type करते हैं, इससे कोई फर्क नहीं पड़ता, यह अभी काम नहीं करेगा। लेकिन हम वहाँ तक पहुँचेंगे।

///

यह निश्चित रूप से final users के लिए frontend नहीं है, लेकिन यह आपके पूरे API को interactively document करने के लिए एक शानदार automatic tool है।

इसे frontend team द्वारा उपयोग किया जा सकता है (जो आप खुद भी हो सकते हैं)।

इसे third party applications और systems द्वारा उपयोग किया जा सकता है।

और इसे आप खुद भी उसी application को debug, check और test करने के लिए उपयोग कर सकते हैं।

## `password` flow { #the-password-flow }

अब थोड़ा पीछे चलते हैं और समझते हैं कि यह सब क्या है।

`password` "flow", OAuth2 में परिभाषित उन तरीकों ("flows") में से एक है, जिनका उपयोग security और authentication संभालने के लिए किया जाता है।

OAuth2 को इस तरह design किया गया था कि backend या API उस server से independent हो सके जो user को authenticate करता है।

लेकिन इस case में, वही **FastAPI** application API और authentication दोनों संभालेगा।

तो, आइए इसे उस simplified दृष्टिकोण से review करें:

* User frontend में `username` और `password` type करता है, और `Enter` दबाता है।
* Frontend (जो user के browser में चल रहा है) उस `username` और `password` को हमारे API के एक specific URL पर भेजता है (`tokenUrl="token"` के साथ declare किया गया)।
* API उस `username` और `password` को check करता है, और एक "token" के साथ respond करता है (हमने अभी तक इनमें से कुछ भी implement नहीं किया है)।
    * एक "token" बस कुछ content वाली string है जिसका उपयोग हम बाद में इस user को verify करने के लिए कर सकते हैं।
    * सामान्यतः, token को कुछ समय बाद expire होने के लिए set किया जाता है।
        * इसलिए, user को बाद में किसी समय फिर से log in करना होगा।
        * और अगर token चोरी हो जाता है, तो risk कम होता है। यह किसी permanent key जैसा नहीं है जो हमेशा काम करेगी (अधिकांश cases में)।
* Frontend उस token को अस्थायी रूप से कहीं store करता है।
* User frontend web app के किसी दूसरे section में जाने के लिए frontend में click करता है।
* Frontend को API से कुछ और data fetch करने की आवश्यकता होती है।
    * लेकिन उस specific endpoint के लिए इसे authentication चाहिए।
    * इसलिए, हमारे API के साथ authenticate करने के लिए, यह `Authorization` header भेजता है जिसकी value `Bearer ` plus token होती है।
    * अगर token में `foobar` है, तो `Authorization` header का content होगा: `Bearer foobar`.

## **FastAPI** का `OAuth2PasswordBearer` { #fastapis-oauth2passwordbearer }

**FastAPI** इन security features को implement करने के लिए abstraction के अलग-अलग levels पर कई tools देता है।

इस उदाहरण में हम **OAuth2** का उपयोग करने जा रहे हैं, **Password** flow के साथ, **Bearer** token का उपयोग करते हुए। हम यह `OAuth2PasswordBearer` class का उपयोग करके करते हैं।

/// note | नोट

"bearer" token एकमात्र विकल्प नहीं है।

लेकिन हमारे use case के लिए यह सबसे अच्छा है।

और यह अधिकांश use cases के लिए सबसे अच्छा हो सकता है, जब तक कि आप OAuth2 expert न हों और ठीक-ठीक न जानते हों कि कोई दूसरा विकल्प आपकी आवश्यकताओं के लिए बेहतर क्यों है।

उस case में, **FastAPI** आपको इसे बनाने के लिए tools भी देता है।

///

जब हम `OAuth2PasswordBearer` class का instance बनाते हैं तो हम `tokenUrl` parameter pass करते हैं। इस parameter में वह URL होता है जिसका उपयोग client (user के browser में चल रहा frontend) token पाने के लिए `username` और `password` भेजने में करेगा।

{* ../../docs_src/security/tutorial001_an_py310.py hl[8] *}

/// tip | सुझाव

यहाँ `tokenUrl="token"` एक relative URL `token` को refer करता है जिसे हमने अभी तक बनाया नहीं है। क्योंकि यह relative URL है, यह `./token` के equivalent है।

क्योंकि हम relative URL का उपयोग कर रहे हैं, अगर आपका API `https://example.com/` पर स्थित था, तो यह `https://example.com/token` को refer करेगा। लेकिन अगर आपका API `https://example.com/api/v1/` पर स्थित था, तो यह `https://example.com/api/v1/token` को refer करेगा।

Relative URL का उपयोग करना महत्वपूर्ण है ताकि यह सुनिश्चित हो सके कि आपका application [Proxy के पीछे](../../advanced/behind-a-proxy.md) जैसे advanced use case में भी काम करता रहे।

///

यह parameter उस endpoint / *path operation* को create नहीं करता, बल्कि declare करता है कि URL `/token` वही होगा जिसका उपयोग client को token पाने के लिए करना चाहिए। उस जानकारी का उपयोग OpenAPI में किया जाता है, और फिर interactive API documentation systems में।

हम जल्द ही वास्तविक path operation भी बनाएँगे।

/// note | नोट

अगर आप बहुत strict "Pythonista" हैं, तो आपको parameter name `tokenUrl` की style `token_url` के बजाय पसंद न आए।

ऐसा इसलिए है क्योंकि यह OpenAPI spec जैसा ही name उपयोग कर रहा है। ताकि अगर आपको इनमें से किसी भी security scheme के बारे में और अधिक जाँच करनी हो, तो आप बस इसे copy और paste करके इसके बारे में और जानकारी खोज सकें।

///

`oauth2_scheme` variable `OAuth2PasswordBearer` का instance है, लेकिन यह एक "callable" भी है।

इसे इस तरह call किया जा सकता है:

```Python
oauth2_scheme(some, parameters)
```

तो, इसे `Depends` के साथ उपयोग किया जा सकता है।

### इसका उपयोग करें { #use-it }

अब आप उस `oauth2_scheme` को `Depends` के साथ dependency में pass कर सकते हैं।

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

यह dependency एक `str` प्रदान करेगी जिसे *path operation function* के parameter `token` को assign किया जाता है।

**FastAPI** जान जाएगा कि यह OpenAPI schema (और automatic API docs) में "security scheme" define करने के लिए इस dependency का उपयोग कर सकता है।

/// note | तकनीकी विवरण

**FastAPI** जान जाएगा कि यह OpenAPI में security scheme define करने के लिए `OAuth2PasswordBearer` class (जो dependency में declare की गई है) का उपयोग कर सकता है क्योंकि यह `fastapi.security.oauth2.OAuth2` से inherit करती है, जो बदले में `fastapi.security.base.SecurityBase` से inherit करती है।

OpenAPI (और automatic API docs) के साथ integrate होने वाली सभी security utilities `SecurityBase` से inherit करती हैं, इसी तरह **FastAPI** जान सकता है कि उन्हें OpenAPI में कैसे integrate करना है।

///

## यह क्या करता है { #what-it-does }

यह request में उस `Authorization` header को खोजेगा, check करेगा कि value `Bearer ` plus कोई token है या नहीं, और token को `str` के रूप में return करेगा।

अगर इसे `Authorization` header नहीं दिखता, या value में `Bearer ` token नहीं है, तो यह सीधे 401 status code error (`UNAUTHORIZED`) के साथ respond करेगा।

Error return करने के लिए आपको यह भी check करने की आवश्यकता नहीं है कि token मौजूद है या नहीं। आप निश्चिंत हो सकते हैं कि अगर आपकी function execute होती है, तो उस token में एक `str` होगा।

आप इसे अभी interactive docs में आज़मा सकते हैं:

<img src="/img/tutorial/security/image03.png">

हम अभी token की validity verify नहीं कर रहे हैं, लेकिन यह पहले से ही एक शुरुआत है।

## Recap { #recap }

तो, केवल 3 या 4 अतिरिक्त lines में, आपके पास पहले से ही security का कुछ primitive form है।
