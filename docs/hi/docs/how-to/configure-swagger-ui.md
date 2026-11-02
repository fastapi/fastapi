# Swagger UI configure करें { #configure-swagger-ui }

आप कुछ अतिरिक्त [Swagger UI parameters](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) configure कर सकते हैं।

इन्हें configure करने के लिए, `FastAPI()` app object बनाते समय या `get_swagger_ui_html()` function में `swagger_ui_parameters` argument pass करें।

`swagger_ui_parameters` एक dictionary प्राप्त करता है जिसमें configurations सीधे Swagger UI को pass की जाती हैं।

FastAPI configurations को **JSON** में बदलता है ताकि वे JavaScript के साथ compatible हों, क्योंकि Swagger UI को यही चाहिए।

## Syntax Highlighting disable करें { #disable-syntax-highlighting }

उदाहरण के लिए, आप Swagger UI में syntax highlighting disable कर सकते हैं।

Settings बदले बिना, syntax highlighting default रूप से enabled रहती है:

<img src="/img/tutorial/extending-openapi/image02.png">

लेकिन आप `syntaxHighlight` को `False` पर set करके इसे disable कर सकते हैं:

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...और फिर Swagger UI अब syntax highlighting नहीं दिखाएगा:

<img src="/img/tutorial/extending-openapi/image03.png">

## Theme बदलें { #change-the-theme }

इसी तरह आप key `"syntaxHighlight.theme"` के साथ syntax highlighting theme set कर सकते हैं (ध्यान दें कि इसके बीच में एक dot है):

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

वह configuration syntax highlighting color theme बदल देगी:

<img src="/img/tutorial/extending-openapi/image04.png">

## Default Swagger UI Parameters बदलें { #change-default-swagger-ui-parameters }

FastAPI में ज़्यादातर use cases के लिए उपयुक्त कुछ default configuration parameters शामिल हैं।

इसमें ये default configurations शामिल हैं:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

आप `swagger_ui_parameters` argument में अलग value set करके इनमें से किसी को भी override कर सकते हैं।

उदाहरण के लिए, `deepLinking` disable करने के लिए आप ये settings `swagger_ui_parameters` में pass कर सकते हैं:

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## अन्य Swagger UI Parameters { #other-swagger-ui-parameters }

आप जिन अन्य सभी संभावित configurations का उपयोग कर सकते हैं, उन्हें देखने के लिए आधिकारिक [Swagger UI parameters के docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) पढ़ें।

## केवल JavaScript settings { #javascript-only-settings }

Swagger UI अन्य configurations को **केवल JavaScript** objects (उदाहरण के लिए, JavaScript functions) होने की भी अनुमति देता है।

FastAPI में ये केवल JavaScript `presets` settings भी शामिल हैं:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

ये **JavaScript** objects हैं, strings नहीं, इसलिए आप इन्हें सीधे Python code से pass नहीं कर सकते।

अगर आपको ऐसी केवल JavaScript configurations का उपयोग करना है, तो आप ऊपर दिए गए methods में से किसी एक का उपयोग कर सकते हैं। पूरी Swagger UI *path operation* को override करें और आपको जो भी JavaScript चाहिए उसे manually लिखें।
