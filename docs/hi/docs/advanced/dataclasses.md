# Dataclasses का उपयोग { #using-dataclasses }

FastAPI **Pydantic** के ऊपर बनाया गया है, और मैंने आपको दिखाया है कि requests और responses घोषित करने के लिए Pydantic models का उपयोग कैसे करें।

लेकिन FastAPI उसी तरह [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) का उपयोग भी support करता है:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

यह अभी भी **Pydantic** की वजह से support किया जाता है, क्योंकि इसमें [`dataclasses` के लिए internal support](https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel) है।

इसलिए, ऊपर दिए गए code में भी, जो Pydantic का स्पष्ट रूप से उपयोग नहीं करता, FastAPI उन standard dataclasses को Pydantic की अपनी तरह की dataclasses में बदलने के लिए Pydantic का उपयोग कर रहा है।

और निश्चित रूप से, यह इन्हें भी support करता है:

* data validation
* data serialization
* data documentation, आदि।

यह Pydantic models की तरह ही काम करता है। और अंदर से यह वास्तव में उसी तरह, Pydantic का उपयोग करके हासिल किया जाता है।

/// note | नोट

ध्यान रखें कि dataclasses वह सब कुछ नहीं कर सकतीं जो Pydantic models कर सकते हैं।

इसलिए, आपको अभी भी Pydantic models का उपयोग करना पड़ सकता है।

लेकिन अगर आपके पास बहुत सारी dataclasses पहले से मौजूद हैं, तो FastAPI का उपयोग करके web API को power देने के लिए उनका उपयोग करने की यह एक अच्छी तरकीब है। 🤓

///

## `response_model` में Dataclasses { #dataclasses-in-response-model }

आप `response_model` parameter में भी `dataclasses` का उपयोग कर सकते हैं:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

dataclass अपने आप Pydantic dataclass में बदल जाएगी।

इस तरह, उसका schema API docs के user interface में दिखाई देगा:

<img src="/img/tutorial/dataclasses/image01.png">

## Nested Data Structures में Dataclasses { #dataclasses-in-nested-data-structures }

आप nested data structures बनाने के लिए `dataclasses` को अन्य type annotations के साथ भी जोड़ सकते हैं।

कुछ मामलों में, आपको अभी भी Pydantic के `dataclasses` वाले version का उपयोग करना पड़ सकता है। उदाहरण के लिए, अगर automatically generated API documentation में errors हों।

उस स्थिति में, आप standard `dataclasses` को बस `pydantic.dataclasses` से बदल सकते हैं, जो एक drop-in replacement है:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. हम अभी भी standard `dataclasses` से `field` import करते हैं।

2. `pydantic.dataclasses`, `dataclasses` के लिए एक drop-in replacement है।

3. `Author` dataclass में `Item` dataclasses की एक list शामिल है।

4. `Author` dataclass को `response_model` parameter के रूप में उपयोग किया गया है।

5. आप request body के रूप में dataclasses के साथ अन्य standard type annotations का उपयोग कर सकते हैं।

    इस मामले में, यह `Item` dataclasses की एक list है।

6. यहाँ हम एक dictionary return कर रहे हैं जिसमें `items` है, जो dataclasses की एक list है।

    FastAPI अभी भी data को JSON में <dfn title="data को ऐसे format में बदलना जिसे भेजा जा सके">serialize करने</dfn> में सक्षम है।

7. यहाँ `response_model`, `Author` dataclasses की list के type annotation का उपयोग कर रहा है।

    फिर से, आप `dataclasses` को standard type annotations के साथ जोड़ सकते हैं।

8. ध्यान दें कि यह *path operation function* `async def` की बजाय सामान्य `def` का उपयोग करता है।

    हमेशा की तरह, FastAPI में आप आवश्यकता के अनुसार `def` और `async def` को जोड़ सकते हैं।

    अगर आपको यह याद दिलाने की आवश्यकता है कि किसे कब उपयोग करना है, तो [`async` और `await`](../async.md#in-a-hurry) के docs में _"जल्दी में हैं?"_ section देखें।

9. यह *path operation function* dataclasses return नहीं कर रहा है (हालाँकि कर सकता था), बल्कि internal data वाली dictionaries की list return कर रहा है।

    FastAPI response को बदलने के लिए `response_model` parameter (जिसमें dataclasses शामिल हैं) का उपयोग करेगा।

आप जटिल data structures बनाने के लिए `dataclasses` को कई अलग-अलग combinations में अन्य type annotations के साथ जोड़ सकते हैं।

अधिक विशिष्ट विवरण देखने के लिए ऊपर दिए गए in-code annotation tips देखें।

## और जानें { #learn-more }

आप `dataclasses` को अन्य Pydantic models के साथ भी जोड़ सकते हैं, उनसे inherit कर सकते हैं, उन्हें अपने models में शामिल कर सकते हैं, आदि।

अधिक जानने के लिए, [dataclasses के बारे में Pydantic docs](https://docs.pydantic.dev/latest/concepts/dataclasses/) देखें।

## Version { #version }

यह FastAPI version `0.67.0` से उपलब्ध है। 🔖
