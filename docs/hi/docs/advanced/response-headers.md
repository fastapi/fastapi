# Response Headers { #response-headers }

## `Response` parameter का उपयोग करें { #use-a-response-parameter }

आप अपने *path operation function* में `Response` प्रकार का parameter घोषित कर सकते हैं (जैसा कि आप cookies के लिए कर सकते हैं)।

और फिर आप उस *अस्थायी* response object में headers सेट कर सकते हैं।

{* ../../docs_src/response_headers/tutorial002_py310.py hl[1, 7:8] *}

और फिर आप अपनी ज़रूरत का कोई भी object return कर सकते हैं, जैसा कि आप सामान्य रूप से करते हैं (एक `dict`, database model, आदि)।

और अगर आपने `response_model` घोषित किया है, तो वह अब भी आपके return किए गए object को filter और convert करने के लिए उपयोग किया जाएगा।

**FastAPI** headers (साथ ही cookies और status code) निकालने के लिए उस *अस्थायी* response का उपयोग करेगा, और उन्हें अंतिम response में डाल देगा जिसमें आपके द्वारा return किया गया value होता है, जिसे किसी भी `response_model` द्वारा filter किया गया होता है।

आप dependencies में भी `Response` parameter घोषित कर सकते हैं, और उनमें headers (और cookies) सेट कर सकते हैं।

## सीधे `Response` return करें { #return-a-response-directly }

जब आप सीधे `Response` return करते हैं, तब भी आप headers जोड़ सकते हैं।

[सीधे Response Return करें](response-directly.md) में वर्णित तरीके से response बनाएँ और headers को एक अतिरिक्त parameter के रूप में पास करें:

{* ../../docs_src/response_headers/tutorial001_py310.py hl[10:12] *}

/// note | तकनीकी विवरण

आप `from starlette.responses import Response` या `from starlette.responses import JSONResponse` का भी उपयोग कर सकते हैं।

**FastAPI** आपकी, developer की, सुविधा के लिए वही `starlette.responses` `fastapi.responses` के रूप में प्रदान करता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं।

और क्योंकि `Response` का उपयोग अक्सर headers और cookies सेट करने के लिए किया जा सकता है, **FastAPI** इसे `fastapi.Response` पर भी प्रदान करता है।

///

## Custom Headers { #custom-headers }

ध्यान रखें कि custom proprietary headers को [`X-` prefix का उपयोग करके](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) जोड़ा जा सकता है।

लेकिन अगर आपके पास custom headers हैं जिन्हें आप चाहते हैं कि browser में कोई client देख सके, तो आपको उन्हें अपनी CORS configurations में जोड़ना होगा ([CORS (Cross-Origin Resource Sharing)](../tutorial/cors.md) में और पढ़ें), इसके लिए [Starlette के CORS docs](https://www.starlette.dev/middleware/#corsmiddleware) में documented parameter `expose_headers` का उपयोग करें।
