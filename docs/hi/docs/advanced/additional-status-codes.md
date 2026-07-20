# अतिरिक्त Status Codes { #additional-status-codes }

default रूप से, **FastAPI** responses को `JSONResponse` का उपयोग करके return करेगा, जिसमें आपके *path operation* से return किया गया content उस `JSONResponse` के अंदर रखा जाएगा।

यह default status code या वह status code उपयोग करेगा जो आपने अपने *path operation* में set किया है।

## अतिरिक्त status codes { #additional-status-codes_1 }

अगर आप मुख्य status code के अलावा अतिरिक्त status codes return करना चाहते हैं, तो आप सीधे `Response`, जैसे `JSONResponse`, return करके और अतिरिक्त status code को सीधे set करके ऐसा कर सकते हैं।

उदाहरण के लिए, मान लीजिए कि आप एक ऐसा *path operation* रखना चाहते हैं जो items को update करने की अनुमति देता है, और सफल होने पर HTTP status code 200 "OK" return करता है।

लेकिन आप यह भी चाहते हैं कि यह नए items को स्वीकार करे। और जब items पहले मौजूद नहीं थे, तो यह उन्हें बनाता है, और HTTP status code 201 "Created" return करता है।

ऐसा करने के लिए, `JSONResponse` import करें, और अपना content वहीं सीधे return करें, साथ में अपनी पसंद का `status_code` set करें:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | चेतावनी

जब आप सीधे `Response` return करते हैं, जैसे ऊपर के उदाहरण में, तो वह सीधे return किया जाएगा।

इसे किसी model आदि के साथ serialize नहीं किया जाएगा।

सुनिश्चित करें कि इसमें वही data है जो आप चाहते हैं, और values valid JSON हैं (अगर आप `JSONResponse` उपयोग कर रहे हैं)।

///

/// note | तकनीकी विवरण

आप `from starlette.responses import JSONResponse` भी उपयोग कर सकते हैं।

**FastAPI** आपकी सुविधा के लिए, developer के रूप में, वही `starlette.responses` `fastapi.responses` के रूप में प्रदान करता है। लेकिन उपलब्ध अधिकांश responses सीधे Starlette से आते हैं। `status` के साथ भी यही है।

///

## OpenAPI और API docs { #openapi-and-api-docs }

अगर आप अतिरिक्त status codes और responses सीधे return करते हैं, तो वे OpenAPI schema (API docs) में शामिल नहीं होंगे, क्योंकि FastAPI के पास पहले से यह जानने का तरीका नहीं है कि आप क्या return करने वाले हैं।

लेकिन आप इसे अपने code में document कर सकते हैं, उपयोग करके: [अतिरिक्त Responses](additional-responses.md)।
