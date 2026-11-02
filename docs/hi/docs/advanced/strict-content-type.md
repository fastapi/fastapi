# सख्त Content-Type जाँच { #strict-content-type-checking }

default रूप से, **FastAPI** JSON request bodies के लिए सख्त `Content-Type` header जाँच का उपयोग करता है, इसका मतलब है कि body को JSON के रूप में parse करने के लिए JSON requests में वैध `Content-Type` header (जैसे `application/json`) **होना ही चाहिए**।

## CSRF जोखिम { #csrf-risk }

यह default व्यवहार एक बहुत विशिष्ट परिस्थिति में **Cross-Site Request Forgery (CSRF)** हमलों के एक वर्ग से सुरक्षा प्रदान करता है।

ये हमले इस बात का फायदा उठाते हैं कि browsers scripts को बिना कोई CORS preflight check किए requests भेजने देते हैं, जब वे:

* `Content-Type` header नहीं रखते (जैसे `Blob` body के साथ `fetch()` का उपयोग करना)
* और कोई authentication credentials नहीं भेजते।

इस प्रकार का हमला मुख्य रूप से तब relevant होता है जब:

* application स्थानीय रूप से चल रही हो (जैसे `localhost` पर) या किसी internal network में
* और application में कोई authentication न हो, वह यह मानती हो कि उसी network से आने वाली कोई भी request भरोसेमंद हो सकती है।

## उदाहरण हमला { #example-attack }

कल्पना करें कि आप एक local AI agent चलाने का तरीका बनाते हैं।

यह यहाँ एक API प्रदान करता है

```
http://localhost:8000/v1/agents/multivac
```

यहाँ एक frontend भी है

```
http://localhost:8000
```

/// tip | सुझाव

ध्यान दें कि दोनों का host समान है।

///

फिर frontend का उपयोग करके आप AI agent से अपनी ओर से काम करवा सकते हैं।

क्योंकि यह **स्थानीय रूप से** चल रहा है, और खुले internet पर नहीं है, आप **कोई authentication setup न करने** का निर्णय लेते हैं, बस local network तक access पर भरोसा करते हुए।

फिर आपके users में से कोई इसे install करके locally चला सकता है।

फिर वे कोई malicious website खोल सकते हैं, जैसे कुछ इस तरह

```
https://evilhackers.example.com
```

और वह malicious website `Blob` body के साथ `fetch()` का उपयोग करके local API पर requests भेजती है

```
http://localhost:8000/v1/agents/multivac
```

भले ही malicious website और local app का host अलग हो, browser CORS preflight request trigger नहीं करेगा क्योंकि:

* यह बिना किसी authentication के चल रहा है, इसे कोई credentials भेजने की जरूरत नहीं है।
* browser को लगता है कि यह JSON नहीं भेज रहा है (`Content-Type` header गायब होने के कारण)।

फिर malicious website local AI agent से user के ex-boss को गुस्से भरे messages भेजवा सकती है... या उससे भी बुरा। 😅

## खुला Internet { #open-internet }

अगर आपकी app खुले internet पर है, तो आप "network पर भरोसा" नहीं करेंगे और किसी को भी बिना authentication के privileged requests भेजने नहीं देंगे।

Attackers सीधे आपकी API पर requests भेजने के लिए script चला सकते हैं, browser interaction की कोई जरूरत नहीं, इसलिए आप शायद पहले से ही किसी भी privileged endpoints को secure कर रहे होंगे।

उस स्थिति में **यह हमला / जोखिम आप पर लागू नहीं होता**।

यह जोखिम और हमला मुख्य रूप से तब relevant होता है जब app **local network** पर चलती है और वही **एकमात्र मानी गई सुरक्षा** होती है।

## Content-Type के बिना Requests की अनुमति देना { #allowing-requests-without-content-type }

अगर आपको ऐसे clients को support करना है जो `Content-Type` header नहीं भेजते, तो आप `strict_content_type=False` set करके strict checking disable कर सकते हैं:

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

इस setting के साथ, जिन requests में `Content-Type` header नहीं होगा, उनकी body JSON के रूप में parse की जाएगी, जो FastAPI के पुराने versions जैसा ही व्यवहार है।

/// note | नोट

यह व्यवहार और configuration FastAPI 0.132.0 में जोड़ा गया था।

///
