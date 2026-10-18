# Advanced Dependencies { #advanced-dependencies }

## Parameterized dependencies { #parameterized-dependencies }

अब तक हमने जो भी dependencies देखी हैं, वे एक निश्चित function या class हैं।

लेकिन ऐसे मामले हो सकते हैं जहाँ आप dependency पर parameters सेट कर पाना चाहें, बिना कई अलग-अलग functions या classes declare किए।

कल्पना करें कि हम एक ऐसी dependency रखना चाहते हैं जो जाँचती है कि query parameter `q` में कुछ निश्चित content है या नहीं।

लेकिन हम उस निश्चित content को parameterize कर पाना चाहते हैं।

## एक "callable" instance { #a-callable-instance }

Python में किसी class के instance को "callable" बनाने का एक तरीका है।

खुद class को नहीं (जो पहले से ही callable होती है), बल्कि उस class के एक instance को।

ऐसा करने के लिए, हम एक method `__call__` declare करते हैं:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

इस मामले में, यही `__call__` है जिसे **FastAPI** अतिरिक्त parameters और sub-dependencies की जाँच के लिए उपयोग करेगा, और बाद में आपकी *path operation function* में parameter को value पास करने के लिए यही call किया जाएगा।

## Instance को parameterize करें { #parameterize-the-instance }

और अब, हम `__init__` का उपयोग करके instance के parameters declare कर सकते हैं जिन्हें हम dependency को "parameterize" करने के लिए उपयोग कर सकते हैं:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

इस मामले में, **FastAPI** कभी भी `__init__` को छुएगा या उसकी परवाह नहीं करेगा, हम इसे सीधे अपने code में उपयोग करेंगे।

## एक instance बनाएँ { #create-an-instance }

हम इस class का एक instance इस तरह बना सकते हैं:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

और इस तरह हम अपनी dependency को "parameterize" कर पाते हैं, जिसमें अब `"bar"` उसके अंदर है, attribute `checker.fixed_content` के रूप में।

## Instance को dependency के रूप में उपयोग करें { #use-the-instance-as-a-dependency }

फिर, हम `Depends(FixedContentQueryChecker)` के बजाय इस `checker` को `Depends(checker)` में उपयोग कर सकते हैं, क्योंकि dependency class खुद नहीं, बल्कि instance `checker` है।

और dependency को solve करते समय, **FastAPI** इस `checker` को इस तरह call करेगा:

```Python
checker(q="somequery")
```

...और जो भी यह return करेगा उसे हमारी *path operation function* में dependency की value के रूप में parameter `fixed_content_included` में पास करेगा:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | सुझाव

यह सब थोड़ा बनावटी लग सकता है। और अभी यह बहुत स्पष्ट नहीं हो सकता कि यह कैसे उपयोगी है।

ये उदाहरण जानबूझकर सरल रखे गए हैं, लेकिन दिखाते हैं कि यह सब कैसे काम करता है।

Security वाले chapters में utility functions हैं जिन्हें इसी तरीके से implement किया गया है।

अगर आपने यह सब समझ लिया है, तो आप पहले से जानते हैं कि security के लिए वे utility tools अंदर से कैसे काम करते हैं।

///

## `yield`, `HTTPException`, `except` और Background Tasks वाली Dependencies { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | चेतावनी

सबसे अधिक संभावना है कि आपको इन तकनीकी विवरणों की आवश्यकता नहीं है।

ये विवरण मुख्य रूप से तब उपयोगी हैं जब आपके पास 0.121.0 से पुरानी FastAPI application थी और आपको `yield` वाली dependencies के साथ समस्याएँ आ रही हैं।

///

`yield` वाली dependencies समय के साथ अलग-अलग use cases को संभालने और कुछ समस्याएँ ठीक करने के लिए विकसित हुई हैं, यहाँ बदले हुए व्यवहार का सारांश है।

### `yield` और `scope` वाली Dependencies { #dependencies-with-yield-and-scope }

Version 0.121.0 में, FastAPI ने `yield` वाली dependencies के लिए `Depends(scope="function")` का support जोड़ा।

`Depends(scope="function")` का उपयोग करने पर, `yield` के बाद का exit code *path operation function* के समाप्त होते ही, response client को वापस भेजे जाने से पहले execute होता है।

और `Depends(scope="request")` (default) का उपयोग करने पर, `yield` के बाद का exit code response भेजे जाने के बाद execute होता है।

आप इसके बारे में docs में [Dependencies with `yield` - Early exit and `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) में अधिक पढ़ सकते हैं।

### `yield` और `StreamingResponse` वाली Dependencies, तकनीकी विवरण { #dependencies-with-yield-and-streamingresponse-technical-details }

FastAPI 0.118.0 से पहले, यदि आप `yield` वाली dependency उपयोग करते थे, तो यह *path operation function* के return करने के बाद लेकिन response भेजने से ठीक पहले exit code run करती थी।

इरादा यह था कि आवश्यक से अधिक समय तक resources को पकड़े रखने से बचा जाए, response के network से गुजरने की प्रतीक्षा करते हुए।

इस बदलाव का अर्थ यह भी था कि यदि आपने `StreamingResponse` return किया, तो `yield` वाली dependency का exit code पहले ही run हो चुका होता।

उदाहरण के लिए, यदि आपके पास `yield` वाली dependency में database session था, तो `StreamingResponse` data stream करते समय उस session का उपयोग नहीं कर पाता क्योंकि `yield` के बाद वाले exit code में session पहले ही बंद हो चुका होता।

यह व्यवहार 0.118.0 में revert कर दिया गया, ताकि `yield` के बाद का exit code response भेजे जाने के बाद execute हो।

/// note | ध्यान दें

जैसा कि आप नीचे देखेंगे, यह version 0.106.0 से पहले के व्यवहार से बहुत मिलता-जुलता है, लेकिन कई सुधारों और corner cases के लिए bug fixes के साथ।

///

#### Early Exit Code वाले Use Cases { #use-cases-with-early-exit-code }

कुछ specific conditions वाले use cases हैं जिन्हें response भेजने से पहले `yield` वाली dependencies का exit code run करने के पुराने व्यवहार से लाभ हो सकता है।

उदाहरण के लिए, कल्पना करें कि आपके पास ऐसा code है जो `yield` वाली dependency में database session का उपयोग केवल user verify करने के लिए करता है, लेकिन database session फिर *path operation function* में कभी उपयोग नहीं होता, केवल dependency में उपयोग होता है, **और** response भेजे जाने में लंबा समय लेता है, जैसे `StreamingResponse` जो data धीरे-धीरे भेजता है, लेकिन किसी कारण से database का उपयोग नहीं करता।

इस मामले में, database session तब तक पकड़ा रहेगा जब तक response भेजना समाप्त नहीं हो जाता, लेकिन यदि आप इसका उपयोग नहीं करते हैं, तो इसे पकड़े रखना आवश्यक नहीं होगा।

यह इस तरह दिख सकता है:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

Exit code, यानी `Session` का automatic closing, यहाँ:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...response द्वारा slow data भेजना समाप्त करने के बाद run होगा:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

लेकिन क्योंकि `generate_stream()` database session का उपयोग नहीं करता, response भेजते समय session को खुला रखना वास्तव में आवश्यक नहीं है।

यदि आपके पास SQLModel (या SQLAlchemy) का उपयोग करते हुए यह specific use case है, तो आप session को तब explicit रूप से बंद कर सकते हैं जब आपको इसकी आगे आवश्यकता न हो:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

इस तरह session database connection release कर देगा, ताकि अन्य requests उसका उपयोग कर सकें।

यदि आपके पास कोई अलग use case है जिसे `yield` वाली dependency से early exit करने की आवश्यकता है, तो कृपया अपने specific use case और dependencies with `yield` के लिए early closing से आपको क्यों लाभ होगा, इसके साथ एक [GitHub Discussion Question](https://github.com/fastapi/fastapi/discussions/new?category=questions) बनाएँ।

यदि dependencies with `yield` में early closing के लिए compelling use cases होते हैं, तो मैं early closing में opt in करने का नया तरीका जोड़ने पर विचार करूँगा।

### `yield` और `except` वाली Dependencies, तकनीकी विवरण { #dependencies-with-yield-and-except-technical-details }

FastAPI 0.110.0 से पहले, यदि आप `yield` वाली dependency उपयोग करते थे, और फिर उस dependency में `except` के साथ exception capture करते थे, और exception को फिर से raise नहीं करते थे, तो exception automatic रूप से किसी भी exception handlers या internal server error handler को raise/forward कर दिया जाता था।

यह version 0.110.0 में बदला गया ताकि handler के बिना forwarded exceptions (internal server errors) से होने वाली unhandled memory consumption ठीक की जा सके, और इसे regular Python code के व्यवहार के साथ consistent बनाया जा सके।

### Background Tasks और `yield` वाली Dependencies, तकनीकी विवरण { #background-tasks-and-dependencies-with-yield-technical-details }

FastAPI 0.106.0 से पहले, `yield` के बाद exceptions raise करना संभव नहीं था, `yield` वाली dependencies में exit code response भेजे जाने के *बाद* execute होता था, इसलिए [Exception Handlers](../tutorial/handling-errors.md#install-custom-exception-handlers) पहले ही run हो चुके होते।

इसे मुख्य रूप से इस तरह design किया गया था ताकि dependencies द्वारा "yielded" किए गए उन्हीं objects को background tasks के अंदर उपयोग किया जा सके, क्योंकि exit code background tasks के समाप्त होने के बाद execute होता था।

यह FastAPI 0.106.0 में बदला गया, इस इरादे से कि response के network से गुजरने की प्रतीक्षा करते समय resources को पकड़े न रखा जाए।

/// tip | सुझाव

इसके अतिरिक्त, background task सामान्यतः logic का एक independent set होता है जिसे अलग से संभाला जाना चाहिए, अपने स्वयं के resources के साथ (जैसे उसका अपना database connection)।

इसलिए, इस तरह आपके पास शायद अधिक साफ़ code होगा।

///

यदि आप इस व्यवहार पर निर्भर थे, तो अब आपको background tasks के लिए resources background task के अंदर ही बनाने चाहिए, और internally केवल ऐसा data उपयोग करना चाहिए जो `yield` वाली dependencies के resources पर निर्भर न हो।

उदाहरण के लिए, उसी database session का उपयोग करने के बजाय, आप background task के अंदर एक नया database session बनाएँगे, और इस नए session का उपयोग करके database से objects प्राप्त करेंगे। और फिर database से object को background task function में parameter के रूप में पास करने के बजाय, आप उस object की ID पास करेंगे और फिर background task function के अंदर object को फिर से प्राप्त करेंगे।
