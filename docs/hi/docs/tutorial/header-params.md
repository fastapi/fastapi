# Header Parameters { #header-parameters }

आप Header parameters को उसी तरह define कर सकते हैं जैसे आप `Query`, `Path` और `Cookie` parameters को define करते हैं।

## `Header` import करें { #import-header }

पहले `Header` import करें:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[3] *}

## `Header` parameters घोषित करें { #declare-header-parameters }

फिर `Path`, `Query` और `Cookie` जैसी ही structure का उपयोग करके header parameters घोषित करें।

आप default value के साथ-साथ सभी अतिरिक्त validation या annotation parameters भी define कर सकते हैं:

{* ../../docs_src/header_params/tutorial001_an_py310.py hl[9] *}

/// note | तकनीकी विवरण

`Header` `Path`, `Query` और `Cookie` की एक "sister" class है। यह भी उसी common `Param` class से inherit करता है।

लेकिन याद रखें कि जब आप `fastapi` से `Query`, `Path`, `Header`, और अन्य import करते हैं, तो वे वास्तव में functions होते हैं जो special classes return करते हैं।

///

/// note | नोट

headers घोषित करने के लिए, आपको `Header` का उपयोग करना होगा, क्योंकि अन्यथा parameters को query parameters के रूप में interpret किया जाएगा।

///

## स्वचालित conversion { #automatic-conversion }

`Header` में `Path`, `Query` और `Cookie` द्वारा दी जाने वाली functionality के ऊपर थोड़ी अतिरिक्त functionality होती है।

अधिकांश standard headers एक "hyphen" character से अलग किए जाते हैं, जिसे "minus symbol" (`-`) भी कहा जाता है।

लेकिन Python में `user-agent` जैसा variable invalid है।

इसलिए, default रूप से, `Header` headers को extract और document करने के लिए parameter names के characters को underscore (`_`) से hyphen (`-`) में convert करेगा।

साथ ही, HTTP headers case-insensitive होते हैं, इसलिए, आप उन्हें standard Python style (जिसे "snake_case" भी कहा जाता है) में declare कर सकते हैं।

इसलिए, Python code में सामान्य रूप से जैसे आप `user_agent` का उपयोग करते हैं, वैसा ही कर सकते हैं, बजाय इसके कि आपको पहले अक्षरों को `User_Agent` की तरह capitalize करना पड़े या कुछ समान करना पड़े।

अगर किसी कारण से आपको underscores से hyphens में automatic conversion disable करना हो, तो `Header` के parameter `convert_underscores` को `False` पर set करें:

{* ../../docs_src/header_params/tutorial002_an_py310.py hl[10] *}

/// warning | चेतावनी

`convert_underscores` को `False` पर set करने से पहले, ध्यान रखें कि कुछ HTTP proxies और servers underscores वाले headers के उपयोग की अनुमति नहीं देते।

///

## Duplicate headers { #duplicate-headers }

duplicate headers receive करना संभव है। इसका मतलब है, कई values वाला वही header।

आप type declaration में list का उपयोग करके ऐसे cases define कर सकते हैं।

आप duplicate header से सभी values Python `list` के रूप में receive करेंगे।

उदाहरण के लिए, `X-Token` का header declare करने के लिए जो एक से अधिक बार आ सकता है, आप लिख सकते हैं:

{* ../../docs_src/header_params/tutorial003_an_py310.py hl[9] *}

यदि आप उस *path operation* के साथ दो HTTP headers भेजते हुए communicate करते हैं, जैसे:

```
X-Token: foo
X-Token: bar
```

response ऐसा होगा:

```JSON
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
```

## Recap { #recap }

`Query`, `Path` और `Cookie` जैसे ही common pattern का उपयोग करते हुए, `Header` के साथ headers declare करें।

और अपनी variables में underscores के बारे में चिंता न करें, **FastAPI** उन्हें convert करने का ध्यान रखेगा।
