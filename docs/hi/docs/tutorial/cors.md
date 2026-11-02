# CORS (Cross-Origin Resource Sharing) { #cors-cross-origin-resource-sharing }

[CORS या "Cross-Origin Resource Sharing"](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) उन स्थितियों को संदर्भित करता है जब browser में चल रहे frontend में JavaScript code होता है जो backend से communicate करता है, और backend frontend से अलग "origin" में होता है।

## Origin { #origin }

एक origin protocol (`http`, `https`), domain (`myapp.com`, `localhost`, `localhost.tiangolo.com`), और port (`80`, `443`, `8080`) का combination होता है।

तो, ये सभी अलग-अलग origins हैं:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

भले ही वे सभी `localhost` में हों, वे अलग-अलग protocols या ports का उपयोग करते हैं, इसलिए वे अलग-अलग "origins" हैं।

## Steps { #steps }

तो, मान लें कि आपके browser में `http://localhost:8080` पर एक frontend चल रहा है, और उसका JavaScript `http://localhost` पर चल रहे backend से communicate करने की कोशिश कर रहा है (क्योंकि हम port specify नहीं करते, browser default port `80` मान लेगा)।

फिर, browser `:80`-backend को एक HTTP `OPTIONS` request भेजेगा, और अगर backend इस अलग origin (`http://localhost:8080`) से communication को authorize करने वाले उचित headers भेजता है, तो `:8080`-browser frontend में JavaScript को अपना request `:80`-backend को भेजने देगा।

इसे हासिल करने के लिए, `:80`-backend के पास "allowed origins" की एक list होनी चाहिए।

इस मामले में, `:8080`-frontend के सही ढंग से काम करने के लिए list में `http://localhost:8080` शामिल होना चाहिए।

## Wildcards { #wildcards }

यह भी possible है कि list को `"*"` (एक "wildcard") के रूप में declare किया जाए, यह बताने के लिए कि सभी allowed हैं।

लेकिन यह केवल कुछ प्रकार के communication को allow करेगा, उन सभी चीज़ों को छोड़कर जिनमें credentials शामिल हैं: Cookies, Authorization headers जैसे कि Bearer Tokens के साथ उपयोग किए जाने वाले, आदि।

इसलिए, सब कुछ सही ढंग से काम करे, इसके लिए allowed origins को स्पष्ट रूप से specify करना बेहतर है।

## `CORSMiddleware` का उपयोग करें { #use-corsmiddleware }

आप `CORSMiddleware` का उपयोग करके इसे अपनी **FastAPI** application में configure कर सकते हैं।

* `CORSMiddleware` import करें।
* allowed origins की एक list बनाएँ (strings के रूप में)।
* इसे अपनी **FastAPI** application में "middleware" के रूप में जोड़ें।

आप यह भी specify कर सकते हैं कि आपका backend allow करता है या नहीं:

* Credentials (Authorization headers, Cookies, आदि)।
* Specific HTTP methods (`POST`, `PUT`) या wildcard `"*"` के साथ सभी methods।
* Specific HTTP headers या wildcard `"*"` के साथ सभी headers।

{* ../../docs_src/cors/tutorial001_py310.py hl[2,6:11,13:19] *}


`CORSMiddleware` implementation द्वारा उपयोग किए जाने वाले default parameters default रूप से restrictive होते हैं, इसलिए browsers को Cross-Domain context में उनका उपयोग करने की permission देने के लिए आपको particular origins, methods, या headers को स्पष्ट रूप से enable करना होगा।

निम्नलिखित arguments supported हैं:

* `allow_origins` - origins की एक list जिन्हें cross-origin requests करने की permission होनी चाहिए। जैसे `['https://example.org', 'https://www.example.org']`। आप किसी भी origin को allow करने के लिए `['*']` का उपयोग कर सकते हैं।
* `allow_origin_regex` - origins के against match करने के लिए एक regex string जिन्हें cross-origin requests करने की permission होनी चाहिए। जैसे `'https://.*\.example\.org'`।
* `allow_methods` - HTTP methods की एक list जिन्हें cross-origin requests के लिए allowed होना चाहिए। Defaults to `['GET']`। आप सभी standard methods को allow करने के लिए `['*']` का उपयोग कर सकते हैं।
* `allow_headers` - HTTP request headers की एक list जिन्हें cross-origin requests के लिए supported होना चाहिए। Defaults to `[]`। आप सभी headers को allow करने के लिए `['*']` का उपयोग कर सकते हैं। `Accept`, `Accept-Language`, `Content-Language` और `Content-Type` headers हमेशा [simple CORS requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests) के लिए allowed होते हैं।
* `allow_credentials` - indicate करता है कि cookies cross-origin requests के लिए supported होनी चाहिए। Defaults to `False`.

    अगर `allow_credentials` को `True` पर set किया गया है, तो `allow_origins`, `allow_methods` और `allow_headers` में से किसी को भी `['*']` पर set नहीं किया जा सकता। उन सभी को [explicitly specified](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards) होना चाहिए।

* `expose_headers` - indicate करता है कि कौन से response headers browser के लिए accessible बनाए जाने चाहिए। Defaults to `[]`।
* `max_age` - browsers के लिए CORS responses को cache करने का maximum समय seconds में set करता है। Defaults to `600`।

middleware दो particular प्रकार के HTTP request का response देता है...

### CORS preflight requests { #cors-preflight-requests }

ये `Origin` और `Access-Control-Request-Method` headers वाले कोई भी `OPTIONS` request होते हैं।

इस मामले में middleware incoming request को intercept करेगा और appropriate CORS headers के साथ respond करेगा, और informational purposes के लिए या तो `200` या `400` response देगा।

### Simple requests { #simple-requests }

`Origin` header वाला कोई भी request। इस मामले में middleware request को सामान्य रूप से pass through करेगा, लेकिन response पर appropriate CORS headers शामिल करेगा।

## अधिक जानकारी { #more-info }

<abbr title="Cross-Origin Resource Sharing - क्रॉस-ओरिजिन रिसोर्स शेयरिंग">CORS</abbr> के बारे में अधिक जानकारी के लिए, [Mozilla CORS documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) देखें।

/// note | तकनीकी विवरण

आप `from starlette.middleware.cors import CORSMiddleware` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, `fastapi.middleware` में कई middlewares provide करता है। लेकिन available middlewares में से अधिकांश सीधे Starlette से आते हैं।

///
