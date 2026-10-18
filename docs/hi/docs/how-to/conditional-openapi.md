# सशर्त OpenAPI { #conditional-openapi }

अगर आपको ज़रूरत हो, तो आप environment के आधार पर OpenAPI को सशर्त रूप से configure करने के लिए settings और environment variables का उपयोग कर सकते हैं, और इसे पूरी तरह disable भी कर सकते हैं।

## security, APIs, और docs के बारे में { #about-security-apis-and-docs }

production में अपनी documentation user interfaces को छिपाना आपकी API को सुरक्षित करने का तरीका *नहीं होना चाहिए*।

इससे आपकी API में कोई अतिरिक्त security नहीं जुड़ती, *path operations* अभी भी वहीं उपलब्ध रहेंगी जहाँ वे हैं।

अगर आपके code में कोई security flaw है, तो वह अभी भी मौजूद रहेगा।

documentation को छिपाना बस यह समझना अधिक कठिन बना देता है कि आपकी API के साथ कैसे interact किया जाए, और production में इसे debug करना आपके लिए अधिक कठिन बना सकता है। इसे बस [Security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity) का एक रूप माना जा सकता है।

अगर आप अपनी API को secure करना चाहते हैं, तो कई बेहतर चीज़ें हैं जो आप कर सकते हैं, उदाहरण के लिए:

* सुनिश्चित करें कि आपके request bodies और responses के लिए अच्छी तरह defined Pydantic models हैं।
* dependencies का उपयोग करके कोई भी required permissions और roles configure करें।
* plaintext passwords कभी store न करें, केवल password hashes store करें।
* pwdlib और JWT tokens आदि जैसे जाने-माने cryptographic tools implement और use करें।
* जहाँ ज़रूरत हो, OAuth2 scopes के साथ अधिक granular permission controls जोड़ें।
* ...आदि।

फिर भी, आपके पास कोई बहुत विशिष्ट use case हो सकता है जहाँ आपको सच में किसी environment (जैसे production) के लिए या environment variables से मिली configurations के आधार पर API docs को disable करने की ज़रूरत हो।

## settings और env vars से सशर्त OpenAPI { #conditional-openapi-from-settings-and-env-vars }

आप अपनी generated OpenAPI और docs UIs को configure करने के लिए आसानी से वही Pydantic settings use कर सकते हैं।

उदाहरण के लिए:

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

यहाँ हम setting `openapi_url` को उसी default `"/openapi.json"` के साथ declare करते हैं।

और फिर `FastAPI` app बनाते समय हम इसका उपयोग करते हैं।

फिर आप environment variable `OPENAPI_URL` को empty string पर set करके OpenAPI (UI docs सहित) को disable कर सकते हैं, जैसे:

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

फिर अगर आप `/openapi.json`, `/docs`, या `/redoc` URLs पर जाते हैं, तो आपको बस इस तरह का `404 Not Found` error मिलेगा:

```JSON
{
    "detail": "Not Found"
}
```
