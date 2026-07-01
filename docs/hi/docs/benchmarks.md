# बेंचमार्क { #benchmarks }

स्वतंत्र TechEmpower बेंचमार्क दिखाते हैं कि Uvicorn के तहत चलने वाले **FastAPI** applications [उपलब्ध सबसे तेज़ Python frameworks में से एक](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7) हैं, केवल Starlette और Uvicorn से नीचे (जिनका उपयोग FastAPI द्वारा अंदरूनी रूप से किया जाता है)।

लेकिन बेंचमार्क और तुलनाएँ देखते समय आपको निम्न बातों को ध्यान में रखना चाहिए।

## बेंचमार्क और गति { #benchmarks-and-speed }

जब आप बेंचमार्क देखते हैं, तो अलग-अलग प्रकार के कई tools को समान मानकर तुलना होते देखना आम है।

विशेष रूप से, Uvicorn, Starlette और FastAPI को साथ में तुलना होते देखना (कई अन्य tools के साथ)।

tool जिस समस्या को जितना सरल हल करता है, उसे उतना ही बेहतर performance मिलेगा। और अधिकांश बेंचमार्क tool द्वारा प्रदान की गई अतिरिक्त features को test नहीं करते।

Hierarchy कुछ इस तरह है:

* **Uvicorn**: एक ASGI server
    * **Starlette**: (Uvicorn का उपयोग करता है) एक web microframework
        * **FastAPI**: (Starlette का उपयोग करता है) APIs बनाने के लिए कई अतिरिक्त features वाला एक API microframework, data validation आदि के साथ।

* **Uvicorn**:
    * इसका performance सबसे अच्छा होगा, क्योंकि इसमें server के अलावा बहुत ज़्यादा extra code नहीं है।
    * आप सीधे Uvicorn में application नहीं लिखेंगे। इसका मतलब होगा कि आपके code में कमोबेश कम से कम वह सारा code शामिल करना पड़ेगा जो Starlette (या **FastAPI**) प्रदान करता है। और यदि आपने ऐसा किया, तो आपके अंतिम application में framework का उपयोग करने और अपने app code और bugs को कम करने जितना ही overhead होगा।
    * यदि आप Uvicorn की तुलना कर रहे हैं, तो इसकी तुलना Daphne, Hypercorn, uWSGI आदि से करें। Application servers से।
* **Starlette**:
    * Uvicorn के बाद इसका performance अगला सबसे अच्छा होगा। वास्तव में, Starlette चलने के लिए Uvicorn का उपयोग करता है। इसलिए, संभवतः यह केवल अधिक code execute करने के कारण Uvicorn से "धीमा" हो सकता है।
    * लेकिन यह आपको simple web applications बनाने के लिए tools प्रदान करता है, paths पर आधारित routing आदि के साथ।
    * यदि आप Starlette की तुलना कर रहे हैं, तो इसकी तुलना Sanic, Flask, Django आदि से करें। Web frameworks (या microframeworks) से।
* **FastAPI**:
    * जिस तरह Starlette Uvicorn का उपयोग करता है और उससे तेज़ नहीं हो सकता, उसी तरह **FastAPI** Starlette का उपयोग करता है, इसलिए यह उससे तेज़ नहीं हो सकता।
    * FastAPI, Starlette के ऊपर और अधिक features प्रदान करता है। ऐसे features जिनकी APIs बनाते समय आपको लगभग हमेशा आवश्यकता होती है, जैसे data validation और serialization। और इसका उपयोग करके, आपको automatic documentation मुफ़्त में मिलती है (automatic documentation running applications में overhead भी नहीं जोड़ती, यह startup पर generate होती है)।
    * यदि आपने FastAPI का उपयोग नहीं किया और सीधे Starlette का उपयोग किया (या कोई अन्य tool, जैसे Sanic, Flask, Responder आदि), तो आपको सारा data validation और serialization स्वयं implement करना पड़ेगा। इसलिए, आपके अंतिम application में फिर भी उतना ही overhead होगा जितना FastAPI का उपयोग करके बनाए जाने पर होता। और कई मामलों में, यह data validation और serialization applications में लिखे गए code का सबसे बड़ा हिस्सा होता है।
    * इसलिए, FastAPI का उपयोग करके आप development time, bugs, code की lines बचाते हैं, और संभवतः आपको वही performance (या बेहतर) मिलेगा जो इसे उपयोग न करने पर मिलता (क्योंकि आपको यह सब अपने code में implement करना पड़ता)।
    * यदि आप FastAPI की तुलना कर रहे हैं, तो इसकी तुलना ऐसे web application framework (या tools के set) से करें जो data validation, serialization और documentation प्रदान करता हो, जैसे Flask-apispec, NestJS, Molten आदि। Integrated automatic data validation, serialization और documentation वाले frameworks से।
