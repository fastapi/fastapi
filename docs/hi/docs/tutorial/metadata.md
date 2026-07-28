# Metadata और Docs URLs { #metadata-and-docs-urls }

आप अपनी **FastAPI** application में कई metadata configurations को customize कर सकते हैं।

## API के लिए Metadata { #metadata-for-api }

आप निम्नलिखित fields set कर सकते हैं, जिनका उपयोग OpenAPI specification और automatic API docs UIs में किया जाता है:

| Parameter | Type | विवरण |
|------------|------|-------------|
| `title` | `str` | API का title। |
| `summary` | `str` | API का एक छोटा summary। <small>OpenAPI 3.1.0, FastAPI 0.99.0 से उपलब्ध।</small> |
| `description` | `str` | API का एक छोटा description। यह Markdown का उपयोग कर सकता है। |
| `version` | `str` | API का version। यह आपकी अपनी application का version है, OpenAPI का नहीं। उदाहरण के लिए `2.5.0`। |
| `terms_of_service` | `str` | API के Terms of Service के लिए एक URL। यदि दिया गया हो, तो यह URL होना चाहिए। |
| `contact` | `dict` | exposed API के लिए contact information। इसमें कई fields हो सकते हैं। <details><summary><code>contact</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>विवरण</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>contact person/organization का identifying name।</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>contact information की ओर point करने वाला URL। URL के format में होना चाहिए।</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>contact person/organization का email address। email address के format में होना चाहिए।</td></tr></tbody></table></details> |
| `license_info` | `dict` | exposed API के लिए license information। इसमें कई fields हो सकते हैं। <details><summary><code>license_info</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>विवरण</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>REQUIRED</strong> (यदि <code>license_info</code> set किया गया हो)। API के लिए उपयोग किया गया license name।</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API के लिए एक [SPDX](https://spdx.org/licenses/) license expression। <code>identifier</code> field, <code>url</code> field के साथ mutually exclusive है। <small>OpenAPI 3.1.0, FastAPI 0.99.0 से उपलब्ध।</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>API के लिए उपयोग किए गए license का URL। URL के format में होना चाहिए।</td></tr></tbody></table></details> |

आप इन्हें इस तरह set कर सकते हैं:

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | सुझाव

आप `description` field में Markdown लिख सकते हैं और यह output में render होगा।

///

इस configuration के साथ, automatic API docs इस तरह दिखेंगे:

<img src="/img/tutorial/metadata/image01.png">

## License identifier { #license-identifier }

OpenAPI 3.1.0 और FastAPI 0.99.0 से, आप `license_info` को `url` के बजाय `identifier` के साथ भी set कर सकते हैं।

उदाहरण के लिए:

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## Tags के लिए Metadata { #metadata-for-tags }

आप अपने path operations को group करने के लिए उपयोग किए गए अलग-अलग tags के लिए `openapi_tags` parameter के साथ अतिरिक्त metadata भी जोड़ सकते हैं।

यह प्रत्येक tag के लिए एक dictionary वाली list लेता है।

प्रत्येक dictionary में हो सकता है:

* `name` (**required**): वही tag name वाला `str`, जिसे आप अपने *path operations* और `APIRouter`s में `tags` parameter में उपयोग करते हैं।
* `description`: tag के लिए short description वाला `str`। इसमें Markdown हो सकता है और यह docs UI में दिखाया जाएगा।
* `externalDocs`: external documentation का वर्णन करने वाला `dict`, जिसमें:
    * `description`: external docs के लिए short description वाला `str`।
    * `url` (**required**): external documentation के लिए URL वाला `str`।

### Tags के लिए metadata बनाएँ { #create-metadata-for-tags }

आइए इसे `users` और `items` के tags वाले एक उदाहरण में आज़माते हैं।

अपने tags के लिए metadata बनाएँ और उसे `openapi_tags` parameter में pass करें:

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

ध्यान दें कि आप descriptions के अंदर Markdown का उपयोग कर सकते हैं, उदाहरण के लिए "login" bold (**login**) में दिखेगा और "fancy" italics (_fancy_) में दिखेगा।

/// tip | सुझाव

आपको अपने उपयोग किए गए सभी tags के लिए metadata जोड़ना ज़रूरी नहीं है।

///

### अपने tags का उपयोग करें { #use-your-tags }

अपने *path operations* (और `APIRouter`s) के साथ `tags` parameter का उपयोग करें, ताकि उन्हें अलग-अलग tags में assign किया जा सके:

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// note | नोट

Tags के बारे में और पढ़ें [Path Operation Configuration](path-operation-configuration.md#tags) में।

///

### Docs जाँचें { #check-the-docs }

अब, अगर आप docs जाँचते हैं, तो वे सभी अतिरिक्त metadata दिखाएँगे:

<img src="/img/tutorial/metadata/image02.png">

### Tags का क्रम { #order-of-tags }

हर tag metadata dictionary का क्रम भी docs UI में दिखाए जाने वाले क्रम को define करता है।

उदाहरण के लिए, भले ही `users` alphabetical order में `items` के बाद आता, यह उनसे पहले दिखाया जाता है, क्योंकि हमने उनकी metadata को list में पहली dictionary के रूप में जोड़ा था।

## OpenAPI URL { #openapi-url }

Default रूप से, OpenAPI schema `/openapi.json` पर serve किया जाता है।

लेकिन आप इसे `openapi_url` parameter के साथ configure कर सकते हैं।

उदाहरण के लिए, इसे `/api/v1/openapi.json` पर serve करने के लिए set करने हेतु:

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

यदि आप OpenAPI schema को पूरी तरह disable करना चाहते हैं, तो आप `openapi_url=None` set कर सकते हैं, इससे इसका उपयोग करने वाले documentation user interfaces भी disable हो जाएँगे।

## Docs URLs { #docs-urls }

आप शामिल किए गए दो documentation user interfaces configure कर सकते हैं:

* **Swagger UI**: `/docs` पर serve किया जाता है।
    * आप इसका URL `docs_url` parameter के साथ set कर सकते हैं।
    * आप `docs_url=None` set करके इसे disable कर सकते हैं।
* **ReDoc**: `/redoc` पर serve किया जाता है।
    * आप इसका URL `redoc_url` parameter के साथ set कर सकते हैं।
    * आप `redoc_url=None` set करके इसे disable कर सकते हैं।

उदाहरण के लिए, Swagger UI को `/documentation` पर serve करने के लिए set करना और ReDoc को disable करना:

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
