# Cookie Parameters { #cookie-parameters }

आप `Cookie` parameters को उसी तरह define कर सकते हैं जैसे आप `Query` और `Path` parameters define करते हैं।

## `Cookie` import करें { #import-cookie }

पहले `Cookie` import करें:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` parameters declare करें { #declare-cookie-parameters }

फिर cookie parameters को `Path` और `Query` जैसी ही structure का उपयोग करके declare करें।

आप default value के साथ-साथ सभी extra validation या annotation parameters भी define कर सकते हैं:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | तकनीकी विवरण

`Cookie`, `Path` और `Query` की एक "sister" class है। यह भी उसी common `Param` class से inherit करती है।

लेकिन याद रखें कि जब आप `fastapi` से `Query`, `Path`, `Cookie` और अन्य चीज़ें import करते हैं, तो वे वास्तव में ऐसे functions होते हैं जो special classes return करते हैं।

///

/// note | नोट

Cookies declare करने के लिए, आपको `Cookie` का उपयोग करना होगा, क्योंकि अन्यथा parameters को query parameters के रूप में interpret किया जाएगा।

///

/// note | नोट

ध्यान रखें कि, क्योंकि **browsers cookies को** विशेष तरीकों से और पर्दे के पीछे handle करते हैं, वे **JavaScript** को उन्हें आसानी से access करने की अनुमति **नहीं** देते।

यदि आप `/docs` पर **API docs UI** में जाते हैं, तो आप अपनी *path operations* के लिए cookies की **documentation** देख पाएँगे।

लेकिन भले ही आप **data भरें** और "Execute" पर click करें, क्योंकि docs UI **JavaScript** के साथ काम करता है, cookies भेजी नहीं जाएँगी, और आपको ऐसा **error** message दिखेगा जैसे आपने कोई values लिखी ही नहीं हों।

///

## Recap { #recap }

`Query` और `Path` जैसे ही common pattern का उपयोग करके, `Cookie` के साथ cookies declare करें।
