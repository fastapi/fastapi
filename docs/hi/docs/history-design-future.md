# इतिहास, डिज़ाइन और भविष्य { #history-design-and-future }

कुछ समय पहले, [एक **FastAPI** उपयोगकर्ता ने पूछा](https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920):

> इस प्रोजेक्ट का इतिहास क्या है? ऐसा लगता है कि यह कुछ ही हफ्तों में कहीं से भी सीधे शानदार बन गया [...]

यहाँ उस इतिहास का एक छोटा सा हिस्सा है।

## विकल्प { #alternatives }

मैं कई वर्षों से जटिल आवश्यकताओं वाली APIs बना रहा हूँ (Machine Learning, distributed systems, asynchronous jobs, NoSQL databases, आदि), और डेवलपर्स की कई टीमों का नेतृत्व कर चुका हूँ।

इसके हिस्से के रूप में, मुझे कई विकल्पों की जाँच, परीक्षण और उपयोग करना पड़ा।

**FastAPI** का इतिहास काफी हद तक इसके पूर्ववर्तियों का इतिहास है।

जैसा कि [विकल्प](alternatives.md) सेक्शन में कहा गया है:

<blockquote markdown="1">

दूसरों के पिछले काम के बिना **FastAPI** मौजूद नहीं होता।

इससे पहले कई टूल बनाए गए हैं जिन्होंने इसके निर्माण को प्रेरित करने में मदद की है।

मैं कई वर्षों से एक नया framework बनाने से बचता रहा। पहले मैंने **FastAPI** द्वारा कवर किए गए सभी features को कई अलग-अलग frameworks, plug-ins और tools का उपयोग करके हल करने की कोशिश की।

लेकिन किसी बिंदु पर, ऐसा कुछ बनाने के अलावा कोई विकल्प नहीं बचा था जो ये सभी features प्रदान करे, पिछले tools से सर्वोत्तम ideas ले और उन्हें सर्वोत्तम संभव तरीके से जोड़े, साथ ही ऐसी language features का उपयोग करे जो पहले उपलब्ध भी नहीं थीं (Python 3.6+ type hints)।

</blockquote>

## जाँच-पड़ताल { #investigation }

सभी पिछले विकल्पों का उपयोग करके मुझे उन सभी से सीखने, ideas लेने, और उन्हें अपने तथा जिन डेवलपर टीमों के साथ मैंने काम किया है उनके लिए सबसे अच्छे तरीके से मिलाने का अवसर मिला।

उदाहरण के लिए, यह स्पष्ट था कि आदर्श रूप से इसे standard Python type hints पर आधारित होना चाहिए।

साथ ही, सबसे अच्छा तरीका पहले से मौजूद standards का उपयोग करना था।

इसलिए, **FastAPI** की coding शुरू करने से पहले ही, मैंने OpenAPI, JSON Schema, OAuth2 आदि के specs का अध्ययन करने में कई महीने बिताए। उनके संबंध, overlap और differences को समझा।

## डिज़ाइन { #design }

फिर मैंने उस developer "API" को डिज़ाइन करने में कुछ समय लगाया जिसे मैं एक user के रूप में पाना चाहता था (FastAPI का उपयोग करने वाले developer के रूप में)।

मैंने सबसे लोकप्रिय Python editors में कई ideas का परीक्षण किया: PyCharm, VS Code, Jedi आधारित editors।

पिछले [Python Developer Survey](https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools) के अनुसार, यह लगभग 80% users को कवर करता है।

इसका मतलब है कि **FastAPI** को विशेष रूप से उन editors के साथ test किया गया था जिनका उपयोग 80% Python developers करते हैं। और चूँकि अधिकांश अन्य editors भी समान तरीके से काम करते हैं, इसके सभी लाभ लगभग सभी editors के लिए काम करने चाहिए।

इस तरह मैं code duplication को जितना संभव हो उतना कम करने, हर जगह completion पाने, type और error checks आदि के सर्वोत्तम तरीके खोज सका।

सब कुछ इस तरह से किया गया कि सभी developers को सर्वोत्तम development experience मिल सके।

## आवश्यकताएँ { #requirements }

कई विकल्पों का परीक्षण करने के बाद, मैंने तय किया कि मैं इसके लाभों के लिए [**Pydantic**](https://docs.pydantic.dev/) का उपयोग करूँगा।

फिर मैंने इसमें योगदान दिया, ताकि इसे JSON Schema के साथ पूरी तरह compliant बनाया जा सके, constraint declarations को define करने के अलग-अलग तरीकों का समर्थन किया जा सके, और कई editors में tests के आधार पर editor support (type checks, autocompletion) को बेहतर बनाया जा सके।

Development के दौरान, मैंने [**Starlette**](https://www.starlette.dev/) में भी योगदान दिया, जो दूसरी मुख्य आवश्यकता थी।

## Development { #development }

जब तक मैंने **FastAPI** खुद बनाना शुरू किया, तब तक अधिकांश हिस्से पहले से तैयार थे, design तय हो चुका था, requirements और tools तैयार थे, और standards तथा specifications के बारे में ज्ञान स्पष्ट और ताज़ा था।

## भविष्य { #future }

इस बिंदु तक, यह पहले से ही स्पष्ट है कि **FastAPI** अपने ideas के साथ कई लोगों के लिए उपयोगी साबित हो रहा है।

इसे कई use cases के लिए बेहतर उपयुक्त होने के कारण पिछले विकल्पों पर चुना जा रहा है।

कई developers और teams अपने projects के लिए पहले से ही **FastAPI** पर निर्भर हैं (मेरे और मेरी team सहित)।

लेकिन फिर भी, अभी कई improvements और features आने बाकी हैं।

**FastAPI** का भविष्य बहुत उज्ज्वल है।

और [आपकी मदद](help-fastapi.md) की बहुत सराहना की जाती है।
