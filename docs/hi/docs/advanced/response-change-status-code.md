# Response - Status Code बदलें { #response-change-status-code }

आपने शायद पहले पढ़ा होगा कि आप एक default [Response Status Code](../tutorial/response-status-code.md) सेट कर सकते हैं।

लेकिन कुछ मामलों में आपको default से अलग status code लौटाना पड़ता है।

## उपयोग का मामला { #use-case }

उदाहरण के लिए, कल्पना करें कि आप default रूप से "OK" `200` का HTTP status code लौटाना चाहते हैं।

लेकिन अगर data मौजूद नहीं था, तो आप उसे बनाना चाहते हैं, और "CREATED" `201` का HTTP status code लौटाना चाहते हैं।

लेकिन फिर भी आप `response_model` के साथ लौटाए गए data को filter और convert कर पाने में सक्षम रहना चाहते हैं।

ऐसे मामलों के लिए, आप `Response` parameter का उपयोग कर सकते हैं।

## `Response` parameter का उपयोग करें { #use-a-response-parameter }

आप अपनी *path operation function* में `Response` type का parameter घोषित कर सकते हैं (जैसा कि आप cookies और headers के लिए कर सकते हैं)।

और फिर आप उस *temporary* response object में `status_code` सेट कर सकते हैं।

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

और फिर आप अपनी ज़रूरत का कोई भी object लौटा सकते हैं, जैसा कि आप सामान्य रूप से करते हैं (एक `dict`, एक database model, आदि)।

और अगर आपने `response_model` घोषित किया है, तो यह आपके लौटाए गए object को filter और convert करने के लिए अभी भी उपयोग किया जाएगा।

**FastAPI** उस *temporary* response का उपयोग status code (साथ ही cookies और headers) निकालने के लिए करेगा, और उन्हें अंतिम response में डाल देगा जिसमें आपके द्वारा लौटाया गया value होगा, जिसे किसी भी `response_model` द्वारा filter किया गया होगा।

आप dependencies में भी `Response` parameter घोषित कर सकते हैं, और उनमें status code सेट कर सकते हैं। लेकिन ध्यान रखें कि आख़िरी बार जो सेट किया जाएगा, वही प्रभावी होगा।
