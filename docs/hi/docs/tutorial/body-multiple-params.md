# Body - कई Parameters { #body-multiple-parameters }

अब जबकि हमने देख लिया है कि `Path` और `Query` का उपयोग कैसे करना है, आइए request body declarations के और उन्नत उपयोग देखें।

## `Path`, `Query` और body parameters को मिलाएँ { #mix-path-query-and-body-parameters }

सबसे पहले, बेशक, आप `Path`, `Query` और request body parameter declarations को स्वतंत्र रूप से मिला सकते हैं और **FastAPI** जान जाएगा कि क्या करना है।

और आप body parameters को optional भी declare कर सकते हैं, default को `None` पर सेट करके:

{* ../../docs_src/body_multiple_params/tutorial001_an_py310.py hl[18:20] *}

/// note | नोट

ध्यान दें कि, इस मामले में, body से लिया जाने वाला `item` optional है। क्योंकि इसका default value `None` है।

///

## कई body parameters { #multiple-body-parameters }

पिछले उदाहरण में, *path operations* एक JSON body की अपेक्षा करेंगे जिसमें `Item` के attributes हों, जैसे:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

लेकिन आप कई body parameters भी declare कर सकते हैं, उदाहरण के लिए `item` और `user`:

{* ../../docs_src/body_multiple_params/tutorial002_py310.py hl[20] *}


इस मामले में, **FastAPI** ध्यान देगा कि function में एक से अधिक body parameter हैं (दो parameters हैं जो Pydantic models हैं)।

तो, फिर यह parameter names को body में keys (field names) के रूप में उपयोग करेगा, और ऐसी body की अपेक्षा करेगा:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | नोट

ध्यान दें कि भले ही `item` को पहले की तरह ही declare किया गया था, अब उससे अपेक्षा की जाती है कि वह body के अंदर key `item` के साथ हो।

///

**FastAPI** request से automatic conversion करेगा, ताकि parameter `item` को उसकी विशिष्ट content मिले और `user` के लिए भी यही हो।

यह compound data का validation करेगा, और इसे OpenAPI schema और automatic docs के लिए उसी तरह document करेगा।

## body में एकल values { #singular-values-in-body }

जिस तरह query और path parameters के लिए extra data define करने हेतु `Query` और `Path` हैं, **FastAPI** एक समान `Body` प्रदान करता है।

उदाहरण के लिए, पिछले model को extend करते हुए, आप तय कर सकते हैं कि आप उसी body में `item` और `user` के अलावा एक और key `importance` रखना चाहते हैं।

यदि आप इसे जैसे है वैसे declare करते हैं, क्योंकि यह एक single value है, **FastAPI** मान लेगा कि यह एक query parameter है।

लेकिन आप **FastAPI** को `Body` का उपयोग करके इसे एक और body key के रूप में treat करने का निर्देश दे सकते हैं:

{* ../../docs_src/body_multiple_params/tutorial003_an_py310.py hl[23] *}


इस मामले में, **FastAPI** ऐसी body की अपेक्षा करेगा:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

फिर से, यह data types को convert करेगा, validate करेगा, document करेगा, आदि।

## कई body params और query { #multiple-body-params-and-query }

बेशक, आप जब भी ज़रूरत हो, किसी भी body parameters के अतिरिक्त, extra query parameters भी declare कर सकते हैं।

क्योंकि default रूप से, single values को query parameters के रूप में interpret किया जाता है, आपको स्पष्ट रूप से `Query` जोड़ने की ज़रूरत नहीं है, आप बस ऐसा कर सकते हैं:

```Python
q: str | None = None
```

उदाहरण के लिए:

{* ../../docs_src/body_multiple_params/tutorial004_an_py310.py hl[28] *}


/// note | नोट

`Body` में भी वही सभी extra validation और metadata parameters हैं जो `Query`, `Path` और अन्य में हैं जिन्हें आप बाद में देखेंगे।

///

## एक single body parameter को embed करें { #embed-a-single-body-parameter }

मान लीजिए आपके पास Pydantic model `Item` से केवल एक single `item` body parameter है।

default रूप से, **FastAPI** फिर सीधे उसकी body की अपेक्षा करेगा।

लेकिन यदि आप चाहते हैं कि यह key `item` के साथ JSON की अपेक्षा करे और उसके अंदर model contents हों, जैसा कि यह तब करता है जब आप extra body parameters declare करते हैं, तो आप special `Body` parameter `embed` का उपयोग कर सकते हैं:

```Python
item: Annotated[Item, Body(embed=True)]
```

जैसे कि:

{* ../../docs_src/body_multiple_params/tutorial005_an_py310.py hl[17] *}


इस मामले में **FastAPI** ऐसी body की अपेक्षा करेगा:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

इसके बजाय:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## Recap { #recap }

आप अपनी *path operation function* में कई body parameters जोड़ सकते हैं, भले ही एक request में केवल एक ही body हो सकती है।

लेकिन **FastAPI** इसे handle करेगा, आपको आपके function में सही data देगा, और *path operation* में सही schema को validate और document करेगा।

आप single values को body के हिस्से के रूप में receive करने के लिए भी declare कर सकते हैं।

और आप **FastAPI** को body को एक key में embed करने का निर्देश दे सकते हैं, भले ही केवल एक single parameter declare किया गया हो।
