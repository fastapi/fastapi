# Data Stream करें { #stream-data }

अगर आप ऐसा data stream करना चाहते हैं जिसे JSON के रूप में संरचित किया जा सके, तो आपको [JSON Lines Stream करें](../tutorial/stream-json-lines.md)।

लेकिन अगर आप **शुद्ध binary data** या strings stream करना चाहते हैं, तो यह आप ऐसे कर सकते हैं।

/// note | नोट

FastAPI 0.134.0 में जोड़ा गया।

///

## उपयोग के मामले { #use-cases }

आप इसका उपयोग तब कर सकते हैं जब आप शुद्ध strings stream करना चाहते हों, उदाहरण के लिए सीधे किसी **AI LLM** service के output से।

आप इसका उपयोग **बड़ी binary files** stream करने के लिए भी कर सकते हैं, जहाँ आप data के प्रत्येक chunk को पढ़ते समय stream करते हैं, बिना पूरे data को एक साथ memory में पढ़े।

आप इसी तरह **video** या **audio** भी stream कर सकते हैं, यह process और send करते समय generate भी किया जा सकता है।

## `yield` के साथ एक `StreamingResponse` { #a-streamingresponse-with-yield }

अगर आप अपने *path operation function* में `response_class=StreamingResponse` declare करते हैं, तो आप data के प्रत्येक chunk को क्रम से भेजने के लिए `yield` का उपयोग कर सकते हैं।

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI data के प्रत्येक chunk को `StreamingResponse` को जैसा है वैसा ही देगा, यह उसे JSON या किसी समान चीज़ में convert करने की कोशिश नहीं करेगा।

### Non-async *path operation functions* { #non-async-path-operation-functions }

आप regular `def` functions (`async` के बिना) का भी उपयोग कर सकते हैं, और उसी तरह `yield` का उपयोग कर सकते हैं।

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### Annotation नहीं { #no-annotation }

Streaming binary data के लिए आपको return type annotation declare करने की वास्तव में आवश्यकता नहीं है।

क्योंकि FastAPI data को Pydantic के साथ JSON में convert करने या किसी भी तरह serialize करने की कोशिश नहीं करेगा, इस मामले में type annotation केवल आपके editor और tools के उपयोग के लिए है, FastAPI इसका उपयोग नहीं करेगा।

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

इसका मतलब यह भी है कि `StreamingResponse` के साथ आपके पास type annotations से स्वतंत्र होकर data bytes को ठीक वैसे produce और encode करने की **स्वतंत्रता** और **ज़िम्मेदारी** है, जैसे उन्हें भेजा जाना चाहिए। 🤓

### Bytes Stream करें { #stream-bytes }

मुख्य उपयोग मामलों में से एक strings के बजाय `bytes` stream करना होगा, और आप निश्चित रूप से ऐसा कर सकते हैं।

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## एक Custom `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

ऊपर के उदाहरणों में, data bytes stream किए गए थे, लेकिन response में `Content-Type` header नहीं था, इसलिए client को पता नहीं था कि उसे किस प्रकार का data मिल रहा है।

आप `StreamingResponse` की एक custom sub-class बना सकते हैं जो `Content-Type` header को उस प्रकार के data पर set करती है जिसे आप stream कर रहे हैं।

उदाहरण के लिए, आप एक `PNGStreamingResponse` बना सकते हैं जो `media_type` attribute का उपयोग करके `Content-Type` header को `image/png` पर set करता है:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

फिर आप अपने *path operation function* में `response_class=PNGStreamingResponse` में इस नई class का उपयोग कर सकते हैं:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### एक File का Simulation करें { #simulate-a-file }

इस उदाहरण में, हम `io.BytesIO` के साथ एक file simulate कर रहे हैं, जो एक file-like object है जो केवल memory में रहता है, लेकिन हमें वही interface उपयोग करने देता है।

उदाहरण के लिए, हम इसके contents consume करने के लिए इस पर iterate कर सकते हैं, जैसे हम किसी file के साथ कर सकते हैं।

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | तकनीकी विवरण

अन्य दो variables, `image_base64` और `binary_image`, Base64 में encoded एक image हैं, और फिर bytes में convert किए गए हैं, ताकि फिर उन्हें `io.BytesIO` को pass किया जा सके।

सिर्फ इसलिए ताकि इस उदाहरण के लिए यह उसी file में रह सके और आप इसे copy करके जैसा है वैसा ही run कर सकें। 🥚

///

`with` block का उपयोग करके, हम यह सुनिश्चित करते हैं कि generator function (`yield` वाला function) पूरा होने के बाद file-like object बंद हो जाए। यानी, response भेजना पूरा होने के बाद।

इस विशिष्ट उदाहरण में यह उतना महत्वपूर्ण नहीं होगा क्योंकि यह एक fake in-memory file है (`io.BytesIO` के साथ), लेकिन एक वास्तविक file के साथ, यह सुनिश्चित करना महत्वपूर्ण होगा कि इसके साथ काम पूरा होने के बाद file बंद हो जाए।

### Files और Async { #files-and-async }

अधिकांश मामलों में, file-like objects default रूप से async और await के साथ compatible नहीं होते।

उदाहरण के लिए, उनके पास `await file.read()` या `async for chunk in file` नहीं होता।

और कई मामलों में, उन्हें पढ़ना एक blocking operation होगा (जो event loop को block कर सकता है), क्योंकि उन्हें disk या network से पढ़ा जाता है।

/// note | नोट

ऊपर दिया गया उदाहरण वास्तव में एक exception है, क्योंकि `io.BytesIO` object पहले से memory में है, इसलिए उसे पढ़ना किसी चीज़ को block नहीं करेगा।

लेकिन कई मामलों में किसी file या file-like object को पढ़ना block करेगा।

///

event loop को block करने से बचने के लिए, आप बस *path operation function* को `async def` के बजाय regular `def` के साथ declare कर सकते हैं, इस तरह FastAPI इसे main loop को block करने से बचाने के लिए threadpool worker पर run करेगा।

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | सुझाव

अगर आपको किसी async function के अंदर से blocking code call करना हो, या किसी blocking function के अंदर से async function call करना हो, तो आप [Asyncer](https://asyncer.tiangolo.com) का उपयोग कर सकते हैं, जो FastAPI की एक sibling library है।

///

### `yield from` { #yield-from }

जब आप किसी चीज़ पर iterate कर रहे हों, जैसे किसी file-like object पर, और फिर प्रत्येक item के लिए `yield` कर रहे हों, तो आप प्रत्येक item को सीधे yield करने और `for` loop को skip करने के लिए `yield from` का भी उपयोग कर सकते हैं।

यह FastAPI के लिए विशेष नहीं है, यह सिर्फ Python है, लेकिन यह जानने लायक एक अच्छा trick है। 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
