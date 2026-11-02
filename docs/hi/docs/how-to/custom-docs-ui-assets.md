# कस्टम Docs UI Static Assets (Self-Hosting) { #custom-docs-ui-static-assets-self-hosting }

API docs **Swagger UI** और **ReDoc** का उपयोग करते हैं, और उनमें से प्रत्येक को कुछ JavaScript और CSS files की जरूरत होती है।

Default रूप से, वे files एक <abbr title="Content Delivery Network - सामग्री वितरण नेटवर्क: एक सेवा, जो सामान्यतः कई servers से बनी होती है, जो JavaScript और CSS जैसी static files प्रदान करती है। इसका सामान्य उपयोग उन files को client के करीब वाले server से serve करने के लिए किया जाता है, जिससे performance बेहतर होती है।">CDN</abbr> से serve की जाती हैं।

लेकिन इसे customize करना संभव है, आप कोई विशिष्ट CDN set कर सकते हैं, या files को स्वयं serve कर सकते हैं।

## JavaScript और CSS के लिए कस्टम CDN { #custom-cdn-for-javascript-and-css }

मान लें कि आप कोई अलग <abbr title="Content Delivery Network - सामग्री वितरण नेटवर्क">CDN</abbr> उपयोग करना चाहते हैं, उदाहरण के लिए आप `https://unpkg.com/` उपयोग करना चाहते हैं।

यह उपयोगी हो सकता है अगर, उदाहरण के लिए, आप ऐसे देश में रहते हैं जो कुछ URLs को restrict करता है।

### Automatic docs को disable करें { #disable-the-automatic-docs }

पहला step automatic docs को disable करना है, क्योंकि default रूप से, वे default CDN का उपयोग करते हैं।

उन्हें disable करने के लिए, अपना `FastAPI` app बनाते समय उनके URLs को `None` पर set करें:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### कस्टम docs शामिल करें { #include-the-custom-docs }

अब आप कस्टम docs के लिए *path operations* बना सकते हैं।

आप docs के लिए HTML pages बनाने हेतु FastAPI के internal functions को reuse कर सकते हैं, और उन्हें जरूरी arguments pass कर सकते हैं:

* `openapi_url`: वह URL जहां docs के लिए HTML page आपके API के लिए OpenAPI schema प्राप्त कर सकता है। आप यहां attribute `app.openapi_url` का उपयोग कर सकते हैं।
* `title`: आपके API का title।
* `oauth2_redirect_url`: default उपयोग करने के लिए आप यहां `app.swagger_ui_oauth2_redirect_url` का उपयोग कर सकते हैं।
* `swagger_js_url`: वह URL जहां आपके Swagger UI docs के लिए HTML **JavaScript** file प्राप्त कर सकता है। यह कस्टम CDN URL है।
* `swagger_css_url`: वह URL जहां आपके Swagger UI docs के लिए HTML **CSS** file प्राप्त कर सकता है। यह कस्टम CDN URL है।

और ReDoc के लिए भी इसी तरह...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | सुझाव

`swagger_ui_redirect` के लिए *path operation* तब एक helper है जब आप OAuth2 का उपयोग करते हैं।

यदि आप अपने API को किसी OAuth2 provider के साथ integrate करते हैं, तो आप authenticate कर पाएंगे और प्राप्त credentials के साथ API docs पर वापस आ पाएंगे। और वास्तविक OAuth2 authentication का उपयोग करके उससे interact कर पाएंगे।

Swagger UI आपके लिए इसे behind the scenes handle करेगा, लेकिन इसके लिए इस "redirect" helper की जरूरत होती है।

///

### इसे test करने के लिए एक *path operation* बनाएं { #create-a-path-operation-to-test-it }

अब, यह test करने के लिए कि सब कुछ काम करता है, एक *path operation* बनाएं:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### इसे test करें { #test-it }

अब, आप अपने docs पर [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) जा सकेंगे, और page reload करने पर, यह उन assets को नए CDN से load करेगा।

## Docs के लिए JavaScript और CSS की Self-hosting { #self-hosting-javascript-and-css-for-docs }

JavaScript और CSS की self-hosting उपयोगी हो सकती है अगर, उदाहरण के लिए, आपको चाहिए कि आपका app offline रहने पर भी, खुले Internet access के बिना, या local network में काम करता रहे।

यहां आप देखेंगे कि उन files को स्वयं, उसी FastAPI app में कैसे serve किया जाए, और docs को उनका उपयोग करने के लिए कैसे configure किया जाए।

### Project file structure { #project-file-structure }

मान लें आपके project की file structure ऐसी दिखती है:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

अब उन static files को store करने के लिए एक directory बनाएं।

आपकी नई file structure ऐसी दिख सकती है:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Files download करें { #download-the-files }

Docs के लिए जरूरी static files download करें और उन्हें उस `static/` directory में रखें।

आप शायद प्रत्येक link पर right-click करके "Save link as..." जैसा कोई option select कर सकते हैं।

**Swagger UI** files का उपयोग करता है:

* [`swagger-ui-bundle.js`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js)
* [`swagger-ui.css`](https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css)

और **ReDoc** file का उपयोग करता है:

* [`redoc.standalone.js`](https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js)

उसके बाद, आपकी file structure ऐसी दिख सकती है:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Static files serve करें { #serve-the-static-files }

* `StaticFiles` import करें।
* किसी विशिष्ट path में `StaticFiles()` instance को "Mount" करें।

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### Static files को test करें { #test-the-static-files }

अपना application start करें और [http://127.0.0.1:8000/static/redoc.standalone.js](http://127.0.0.1:8000/static/redoc.standalone.js) पर जाएं।

आपको **ReDoc** के लिए एक बहुत लंबी JavaScript file दिखनी चाहिए।

यह कुछ इस तरह से शुरू हो सकती है:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

यह confirm करता है कि आप अपने app से static files serve कर पा रहे हैं, और आपने docs के लिए static files को सही जगह पर रखा है।

अब हम app को docs के लिए उन static files का उपयोग करने के लिए configure कर सकते हैं।

### Static files के लिए automatic docs को disable करें { #disable-the-automatic-docs-for-static-files }

कस्टम CDN का उपयोग करने जैसा ही, पहला step automatic docs को disable करना है, क्योंकि वे default रूप से CDN का उपयोग करते हैं।

उन्हें disable करने के लिए, अपना `FastAPI` app बनाते समय उनके URLs को `None` पर set करें:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### Static files के लिए कस्टम docs शामिल करें { #include-the-custom-docs-for-static-files }

और कस्टम CDN की तरह ही, अब आप कस्टम docs के लिए *path operations* बना सकते हैं।

फिर से, आप docs के लिए HTML pages बनाने हेतु FastAPI के internal functions को reuse कर सकते हैं, और उन्हें जरूरी arguments pass कर सकते हैं:

* `openapi_url`: वह URL जहां docs के लिए HTML page आपके API के लिए OpenAPI schema प्राप्त कर सकता है। आप यहां attribute `app.openapi_url` का उपयोग कर सकते हैं।
* `title`: आपके API का title।
* `oauth2_redirect_url`: default उपयोग करने के लिए आप यहां `app.swagger_ui_oauth2_redirect_url` का उपयोग कर सकते हैं।
* `swagger_js_url`: वह URL जहां आपके Swagger UI docs के लिए HTML **JavaScript** file प्राप्त कर सकता है। **यह वही है जिसे अब आपका अपना app serve कर रहा है**।
* `swagger_css_url`: वह URL जहां आपके Swagger UI docs के लिए HTML **CSS** file प्राप्त कर सकता है। **यह वही है जिसे अब आपका अपना app serve कर रहा है**।

और ReDoc के लिए भी इसी तरह...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | सुझाव

`swagger_ui_redirect` के लिए *path operation* तब एक helper है जब आप OAuth2 का उपयोग करते हैं।

यदि आप अपने API को किसी OAuth2 provider के साथ integrate करते हैं, तो आप authenticate कर पाएंगे और प्राप्त credentials के साथ API docs पर वापस आ पाएंगे। और वास्तविक OAuth2 authentication का उपयोग करके उससे interact कर पाएंगे।

Swagger UI आपके लिए इसे behind the scenes handle करेगा, लेकिन इसके लिए इस "redirect" helper की जरूरत होती है।

///

### Static files को test करने के लिए एक *path operation* बनाएं { #create-a-path-operation-to-test-static-files }

अब, यह test करने के लिए कि सब कुछ काम करता है, एक *path operation* बनाएं:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### Static Files UI को test करें { #test-static-files-ui }

अब, आप अपना WiFi disconnect कर सकेंगे, अपने docs पर [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) जा सकेंगे, और page reload कर सकेंगे।

और Internet के बिना भी, आप अपने API के docs देख पाएंगे और उससे interact कर पाएंगे।
