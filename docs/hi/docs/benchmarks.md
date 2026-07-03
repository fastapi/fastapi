# Benchmarks { #benchmarks }

स्वतंत्र TechEmpower benchmarks दिखाते हैं कि Uvicorn के अंतर्गत चलने वाले **FastAPI** applications [उपलब्ध सबसे तेज़ Python frameworks में से एक](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7) हैं, केवल Starlette और Uvicorn स्वयं से नीचे (जिनका उपयोग FastAPI द्वारा internally किया जाता है)।

लेकिन benchmarks और comparisons देखते समय आपको निम्न बातों को ध्यान में रखना चाहिए।

## Benchmarks और speed { #benchmarks-and-speed }

जब आप benchmarks देखते हैं, तो अलग-अलग प्रकार के कई tools को equivalent मानकर compare होते देखना आम बात है।

विशेष रूप से, Uvicorn, Starlette और FastAPI को एक साथ compare होते देखना (कई अन्य tools के साथ)।

Tool जितनी सरल समस्या हल करता है, उसे उतनी ही बेहतर performance मिलेगी। और अधिकांश benchmarks, tool द्वारा प्रदान की जाने वाली अतिरिक्त features को test नहीं करते।

Hierarchy इस प्रकार है:

* **Uvicorn**: एक ASGI server
    * **Starlette**: (Uvicorn का उपयोग करता है) एक web microframework
        * **FastAPI**: (Starlette का उपयोग करता है) APIs बनाने के लिए कई अतिरिक्त features वाला एक API microframework, जिसमें data validation आदि शामिल हैं।

* **Uvicorn**:
    * इसकी performance सबसे अच्छी होगी, क्योंकि इसमें server स्वयं के अलावा बहुत अधिक extra code नहीं होता।
    * आप सीधे Uvicorn में application नहीं लिखेंगे। इसका मतलब होगा कि आपके code में कमोबेश, कम से कम, Starlette (या **FastAPI**) द्वारा प्रदान किया गया सारा code शामिल करना पड़ेगा। और यदि आपने ऐसा किया, तो आपके final application में framework का उपयोग करने और अपने app code तथा bugs को कम करने जितना ही overhead होगा।
    * यदि आप Uvicorn की तुलना कर रहे हैं, तो इसकी तुलना Daphne, Hypercorn, uWSGI आदि से करें। Application servers से।
* **Starlette**:
    * Uvicorn के बाद इसकी performance अगली सबसे अच्छी होगी। वास्तव में, Starlette चलने के लिए Uvicorn का उपयोग करता है। इसलिए, संभवतः यह केवल अधिक code execute करने के कारण Uvicorn से "धीमा" हो सकता है।
    * लेकिन यह आपको simple web applications बनाने के लिए tools देता है, जैसे paths पर आधारित routing आदि।
    * यदि आप Starlette की तुलना कर रहे हैं, तो इसकी तुलना Sanic, Flask, Django आदि से करें। Web frameworks (या microframeworks) से।
* **FastAPI**:
    * जैसे Starlette, Uvicorn का उपयोग करता है और उससे तेज़ नहीं हो सकता, वैसे ही **FastAPI**, Starlette का उपयोग करता है, इसलिए यह उससे तेज़ नहीं हो सकता।
    * FastAPI, Starlette के ऊपर और features प्रदान करता है। ऐसे features जिनकी आपको APIs बनाते समय लगभग हमेशा आवश्यकता होती है, जैसे data validation और serialization। और इसका उपयोग करके आपको automatic documentation मुफ्त में मिलती है (automatic documentation running applications में overhead भी नहीं जोड़ती, यह startup पर generate होती है)।
    * यदि आपने FastAPI का उपयोग नहीं किया और सीधे Starlette (या कोई अन्य tool, जैसे Sanic, Flask, Responder आदि) का उपयोग किया, तो आपको सभी data validation और serialization स्वयं implement करने पड़ेंगे। इसलिए, आपके final application में फिर भी उतना ही overhead होगा जितना FastAPI का उपयोग करके बनाए जाने पर होता। और कई मामलों में, यह data validation और serialization applications में लिखे गए code का सबसे बड़ा हिस्सा होता है।
    * इसलिए, FastAPI का उपयोग करके आप development time, bugs और lines of code बचाते हैं, और संभवतः आपको वही performance (या बेहतर) मिलेगी जो आपको इसे उपयोग न करने पर मिलती (क्योंकि तब आपको यह सब अपने code में implement करना पड़ता)।
    * यदि आप FastAPI की तुलना कर रहे हैं, तो इसकी तुलना ऐसे web application framework (या tools के set) से करें जो data validation, serialization और documentation प्रदान करता हो, जैसे Flask-apispec, NestJS, Molten आदि। ऐसे frameworks जिनमें integrated automatic data validation, serialization और documentation हो।
