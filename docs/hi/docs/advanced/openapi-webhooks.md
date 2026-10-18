# OpenAPI Webhooks { #openapi-webhooks }

ऐसे मामले होते हैं जहाँ आप अपने API **users** को बताना चाहते हैं कि आपकी app कुछ data के साथ (एक request भेजते हुए) *उनकी* app को कॉल कर सकती है, सामान्यतः किसी प्रकार के **event** की **सूचना** देने के लिए।

इसका मतलब है कि आपके users द्वारा आपकी API को requests भेजने की सामान्य प्रक्रिया के बजाय, **आपकी API** (या आपकी app) **उनके system को requests भेज** सकती है (उनकी API, उनकी app को)।

इसे सामान्यतः **webhook** कहा जाता है।

## Webhooks के चरण { #webhooks-steps }

सामान्यतः प्रक्रिया यह होती है कि **आप अपने code में define करते हैं** कि आप कौन-सा message भेजेंगे, यानी **request का body**।

आप यह भी किसी तरीके से define करते हैं कि आपकी app किन **क्षणों** पर वे requests या events भेजेगी।

और **आपके users** किसी तरीके से (उदाहरण के लिए कहीं किसी web dashboard में) वह **URL** define करते हैं जहाँ आपकी app को वे requests भेजनी चाहिए।

Webhooks के लिए URLs को register करने की सारी **logic** और वास्तव में उन requests को भेजने का code आपके ऊपर है। आप इसे **अपने खुद के code** में जैसे चाहें वैसे लिखते हैं।

## **FastAPI** और OpenAPI के साथ webhooks का दस्तावेज़ीकरण { #documenting-webhooks-with-fastapi-and-openapi }

**FastAPI** के साथ, OpenAPI का उपयोग करते हुए, आप इन webhooks के नाम, आपकी app द्वारा भेजे जा सकने वाले HTTP operations के प्रकार (जैसे `POST`, `PUT`, आदि) और आपकी app द्वारा भेजे जाने वाले request **bodies** define कर सकते हैं।

इससे आपके users के लिए आपकी **webhook** requests प्राप्त करने के लिए **अपनी APIs implement करना** बहुत आसान हो सकता है, वे शायद अपने कुछ API code को autogenerate भी कर सकें।

/// note | नोट

Webhooks OpenAPI 3.1.0 और उससे ऊपर में उपलब्ध हैं, और FastAPI `0.99.0` और उससे ऊपर द्वारा समर्थित हैं।

///

## Webhooks वाली app { #an-app-with-webhooks }

जब आप एक **FastAPI** application बनाते हैं, तो एक `webhooks` attribute होता है जिसका उपयोग आप *webhooks* define करने के लिए कर सकते हैं, उसी तरह जैसे आप *path operations* define करते हैं, उदाहरण के लिए `@app.webhooks.post()` के साथ।

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

आप जिन webhooks को define करते हैं वे **OpenAPI** schema और automatic **docs UI** में आ जाएँगे।

/// note | नोट

`app.webhooks` object वास्तव में सिर्फ़ एक `APIRouter` है, वही type जिसका उपयोग आप अपनी app को multiple files के साथ structure करते समय करेंगे।

///

ध्यान दें कि webhooks के साथ आप वास्तव में कोई *path* declare नहीं कर रहे हैं (जैसे `/items/`), वहाँ आप जो text pass करते हैं वह केवल webhook का एक **identifier** है (event का नाम), उदाहरण के लिए `@app.webhooks.post("new-subscription")` में, webhook का नाम `new-subscription` है।

ऐसा इसलिए है क्योंकि उम्मीद की जाती है कि **आपके users** उस वास्तविक **URL path** को किसी और तरीके से define करेंगे जहाँ वे webhook request प्राप्त करना चाहते हैं (जैसे कोई web dashboard)।

### Docs देखें { #check-the-docs }

अब आप अपनी app start कर सकते हैं और [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) पर जा सकते हैं।

आप देखेंगे कि आपके docs में सामान्य *path operations* हैं और अब कुछ **webhooks** भी हैं:

<img src="/img/tutorial/openapi-webhooks/image01.png">
