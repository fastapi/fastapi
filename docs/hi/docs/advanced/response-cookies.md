# Response Cookies { #response-cookies }

## `Response` parameter का उपयोग करें { #use-a-response-parameter }

आप अपने *path operation function* में `Response` प्रकार का parameter घोषित कर सकते हैं।

और फिर आप उस *temporary* response object में cookies set कर सकते हैं।

{* ../../docs_src/response_cookies/tutorial002_py310.py hl[1, 8:9] *}

और फिर आप अपनी ज़रूरत का कोई भी object return कर सकते हैं, जैसा कि आप सामान्य रूप से करते हैं (एक `dict`, database model, आदि)।

और अगर आपने `response_model` घोषित किया है, तो आपके द्वारा return किए गए object को filter और convert करने के लिए उसका अभी भी उपयोग किया जाएगा।

**FastAPI** उस *temporary* response का उपयोग cookies (साथ ही headers और status code) निकालने के लिए करेगा, और उन्हें final response में डाल देगा जिसमें आपके द्वारा return किया गया value होगा, किसी भी `response_model` द्वारा filter किया हुआ।

आप dependencies में भी `Response` parameter घोषित कर सकते हैं, और उनमें cookies (और headers) set कर सकते हैं।

## सीधे `Response` return करें { #return-a-response-directly }

आप अपने code में सीधे `Response` return करते समय भी cookies बना सकते हैं।

ऐसा करने के लिए, आप [सीधे Response Return करें](response-directly.md) में बताए अनुसार एक response बना सकते हैं।

फिर उसमें Cookies set करें, और फिर उसे return करें:

{* ../../docs_src/response_cookies/tutorial001_py310.py hl[10:12] *}

/// tip | सुझाव

ध्यान रखें कि अगर आप `Response` parameter का उपयोग करने के बजाय सीधे response return करते हैं, तो FastAPI उसे सीधे return करेगा।

इसलिए, आपको यह सुनिश्चित करना होगा कि आपका data सही प्रकार का है। उदाहरण के लिए, अगर आप `JSONResponse` return कर रहे हैं, तो वह JSON के साथ compatible हो।

और यह भी कि आप कोई ऐसा data नहीं भेज रहे हैं जिसे `response_model` द्वारा filter किया जाना चाहिए था।

///

### अधिक जानकारी { #more-info }

/// note | तकनीकी विवरण

आप `from starlette.responses import Response` या `from starlette.responses import JSONResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.responses` `fastapi.responses` के रूप में प्रदान करता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं।

और क्योंकि `Response` का उपयोग अक्सर headers और cookies set करने के लिए किया जा सकता है, **FastAPI** इसे `fastapi.Response` पर भी प्रदान करता है।

///

सभी उपलब्ध parameters और options देखने के लिए, [Starlette में documentation](https://www.starlette.dev/responses/#set-cookie) देखें।
