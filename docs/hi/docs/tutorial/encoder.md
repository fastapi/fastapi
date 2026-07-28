# JSON संगत Encoder { #json-compatible-encoder }

कुछ मामलों में आपको किसी data type (जैसे Pydantic model) को JSON के साथ संगत किसी चीज़ (जैसे `dict`, `list`, आदि) में convert करने की ज़रूरत पड़ सकती है।

उदाहरण के लिए, अगर आपको इसे database में store करना हो।

इसके लिए, **FastAPI** एक `jsonable_encoder()` function प्रदान करता है।

## `jsonable_encoder` का उपयोग करना { #using-the-jsonable-encoder }

कल्पना करें कि आपके पास एक database `fake_db` है जो केवल JSON संगत data ही स्वीकार करता है।

उदाहरण के लिए, यह `datetime` objects स्वीकार नहीं करता, क्योंकि वे JSON के साथ संगत नहीं होते।

इसलिए, एक `datetime` object को [ISO format](https://en.wikipedia.org/wiki/ISO_8601) में data रखने वाले `str` में convert करना होगा।

इसी तरह, यह database Pydantic model (attributes वाला एक object) स्वीकार नहीं करेगा, केवल एक `dict`।

इसके लिए आप `jsonable_encoder` का उपयोग कर सकते हैं।

यह एक object, जैसे Pydantic model, प्राप्त करता है और JSON संगत version लौटाता है:

{* ../../docs_src/encoder/tutorial001_py310.py hl[4,21] *}

इस उदाहरण में, यह Pydantic model को `dict` में और `datetime` को `str` में convert करेगा।

इसे call करने का परिणाम कुछ ऐसा होता है जिसे Python standard [`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps) के साथ encode किया जा सकता है।

यह JSON format में data रखने वाला कोई बड़ा `str` (string के रूप में) return नहीं करता। यह एक Python standard data structure (जैसे `dict`) return करता है, जिसमें values और sub-values होती हैं जो सभी JSON के साथ संगत होती हैं।

/// note | नोट

`jsonable_encoder` वास्तव में **FastAPI** द्वारा internally data convert करने के लिए उपयोग किया जाता है। लेकिन यह कई अन्य scenarios में भी उपयोगी है।

///
