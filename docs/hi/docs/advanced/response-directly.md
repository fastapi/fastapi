# सीधे एक Response लौटाएँ { #return-a-response-directly }

जब आप **FastAPI** *path operation* बनाते हैं, तो सामान्यतः आप उससे कोई भी data लौटा सकते हैं: एक `dict`, एक `list`, एक Pydantic model, एक database model, आदि।

अगर आप [Response Model](../tutorial/response-model.md) declare करते हैं, तो FastAPI Pydantic का उपयोग करके data को JSON में serialize करने के लिए उसका उपयोग करेगा।

अगर आप response model declare नहीं करते, तो FastAPI [JSON Compatible Encoder](../tutorial/encoder.md) में समझाए गए `jsonable_encoder` का उपयोग करेगा और उसे एक `JSONResponse` में रखेगा।

आप सीधे एक `JSONResponse` भी बना सकते हैं और उसे लौटा सकते हैं।

/// tip | सुझाव

आम तौर पर सीधे `JSONResponse` लौटाने की तुलना में [Response Model](../tutorial/response-model.md) का उपयोग करने पर performance काफी बेहतर होगी, क्योंकि उस तरीके से यह Rust में Pydantic का उपयोग करके data serialize करता है।

///

## एक `Response` लौटाएँ { #return-a-response }

आप एक `Response` या उसकी कोई भी sub-class लौटा सकते हैं।

/// note | नोट

`JSONResponse` खुद `Response` की एक sub-class है।

///

और जब आप एक `Response` लौटाते हैं, तो **FastAPI** उसे सीधे pass कर देगा।

यह Pydantic models के साथ कोई data conversion नहीं करेगा, contents को किसी भी type में convert नहीं करेगा, आदि।

यह आपको बहुत अधिक **flexibility** देता है। आप कोई भी data type लौटा सकते हैं, किसी भी data declaration या validation को override कर सकते हैं, आदि।

यह आपको बहुत अधिक **responsibility** भी देता है। आपको यह सुनिश्चित करना होगा कि आप जो data लौटा रहे हैं वह सही है, सही format में है, वह serialize किया जा सकता है, आदि।

## `Response` में `jsonable_encoder` का उपयोग करना { #using-the-jsonable-encoder-in-a-response }

क्योंकि **FastAPI** आपके लौटाए गए `Response` में कोई बदलाव नहीं करता, आपको सुनिश्चित करना होगा कि उसके contents इसके लिए तैयार हैं।

उदाहरण के लिए, आप किसी Pydantic model को पहले `dict` में convert किए बिना `JSONResponse` में नहीं रख सकते, जिसमें सभी data types (जैसे `datetime`, `UUID`, आदि) JSON-compatible types में convert किए गए हों।

ऐसे मामलों के लिए, response को pass करने से पहले आप अपने data को convert करने के लिए `jsonable_encoder` का उपयोग कर सकते हैं:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | तकनीकी विवरण

आप `from starlette.responses import JSONResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.responses` `fastapi.responses` के रूप में उपलब्ध कराता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं।

///

## custom `Response` लौटाना { #returning-a-custom-response }

ऊपर दिया गया उदाहरण वे सभी हिस्से दिखाता है जिनकी आपको जरूरत है, लेकिन यह अभी बहुत उपयोगी नहीं है, क्योंकि आप सीधे `item` लौटा सकते थे, और **FastAPI** उसे आपके लिए `JSONResponse` में रख देता, उसे `dict` में convert करता, आदि। यह सब default रूप से होता है।

अब, देखते हैं कि आप इसका उपयोग custom response लौटाने के लिए कैसे कर सकते हैं।

मान लें कि आप एक [XML](https://en.wikipedia.org/wiki/XML) response लौटाना चाहते हैं।

आप अपना XML content एक string में रख सकते हैं, उसे `Response` में रख सकते हैं, और उसे लौटा सकते हैं:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Response Model कैसे काम करता है { #how-a-response-model-works }

जब आप किसी path operation में [Response Model - Return Type](../tutorial/response-model.md) declare करते हैं, तो **FastAPI** Pydantic का उपयोग करके data को JSON में serialize करने के लिए उसका उपयोग करेगा।

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

क्योंकि यह Rust side पर होगा, performance regular Python और `JSONResponse` class के साथ किए जाने की तुलना में काफी बेहतर होगी।

`response_model` या return type का उपयोग करते समय, FastAPI data को convert करने के लिए `jsonable_encoder` का उपयोग नहीं करेगा (जो धीमा होता), और न ही `JSONResponse` class का उपयोग करेगा।

इसके बजाय यह response model (या return type) का उपयोग करके Pydantic के साथ generate किए गए JSON bytes लेता है और JSON के लिए सही media type (`application/json`) के साथ सीधे एक `Response` लौटाता है।

## नोट्स { #notes }

जब आप सीधे एक `Response` लौटाते हैं, तो उसका data अपने-आप validate, convert (serialize), या document नहीं किया जाता।

लेकिन आप फिर भी उसे [OpenAPI में अतिरिक्त Responses](additional-responses.md) में बताए अनुसार document कर सकते हैं।

बाद के sections में आप देख सकते हैं कि automatic data conversion, documentation, आदि रखते हुए इन custom `Response`s का उपयोग/declare कैसे करें।
