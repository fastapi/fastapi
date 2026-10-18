# path operation decorators में Dependencies { #dependencies-in-path-operation-decorators }

कुछ मामलों में आपको अपनी *path operation function* के अंदर किसी dependency की return value की वास्तव में ज़रूरत नहीं होती।

या dependency कोई value return नहीं करती।

लेकिन फिर भी आपको उसका execute/solve होना चाहिए।

ऐसे मामलों के लिए, `Depends` के साथ *path operation function* parameter declare करने के बजाय, आप *path operation decorator* में `dependencies` की एक `list` जोड़ सकते हैं।

## *path operation decorator* में `dependencies` जोड़ें { #add-dependencies-to-the-path-operation-decorator }

*path operation decorator* एक optional argument `dependencies` प्राप्त करता है।

यह `Depends()` की एक `list` होनी चाहिए:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

ये dependencies normal dependencies की तरह ही execute/solve होंगी। लेकिन उनकी value (यदि वे कोई return करती हैं) आपकी *path operation function* को pass नहीं की जाएगी।

/// tip | सुझाव

कुछ editors unused function parameters की जाँच करते हैं, और उन्हें errors के रूप में दिखाते हैं।

*path operation decorator* में इन `dependencies` का उपयोग करके आप सुनिश्चित कर सकते हैं कि वे execute हों, साथ ही editor/tooling errors से बच सकें।

यह नए developers के लिए भ्रम से बचने में भी मदद कर सकता है, जो आपके code में unused parameter देखकर सोच सकते हैं कि यह अनावश्यक है।

///

/// note | नोट

इस example में हम बनाए गए custom headers `X-Key` और `X-Token` का उपयोग करते हैं।

लेकिन वास्तविक मामलों में, security implement करते समय, आपको integrated [Security utilities (अगला अध्याय)](../security/index.md) का उपयोग करने से अधिक लाभ मिलेंगे।

///

## Dependencies errors और return values { #dependencies-errors-and-return-values }

आप वही dependency *functions* उपयोग कर सकते हैं जिन्हें आप सामान्य रूप से उपयोग करते हैं।

### Dependency requirements { #dependency-requirements }

वे request requirements (जैसे headers) या अन्य sub-dependencies declare कर सकती हैं:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### Exceptions raise करें { #raise-exceptions }

ये dependencies normal dependencies की तरह ही exceptions `raise` कर सकती हैं:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### Return values { #return-values }

और वे values return कर सकती हैं या नहीं भी कर सकतीं, values का उपयोग नहीं किया जाएगा।

इसलिए, आप एक normal dependency (जो value return करती है) को फिर से उपयोग कर सकते हैं जिसे आप पहले से कहीं और उपयोग करते हैं, और भले ही value का उपयोग न हो, dependency execute होगी:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## *path operations* के समूह के लिए Dependencies { #dependencies-for-a-group-of-path-operations }

बाद में, जब आप बड़े applications को structure करने के बारे में पढ़ेंगे ([बड़े Applications - कई Files](../../tutorial/bigger-applications.md)), संभवतः कई files के साथ, तो आप सीखेंगे कि *path operations* के समूह के लिए एक ही `dependencies` parameter कैसे declare किया जाए।

## Global Dependencies { #global-dependencies }

आगे हम देखेंगे कि पूरे `FastAPI` application में dependencies कैसे जोड़ी जाएँ, ताकि वे हर *path operation* पर लागू हों।
