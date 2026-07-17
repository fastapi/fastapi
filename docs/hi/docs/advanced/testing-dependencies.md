# Overrides के साथ Dependencies की Testing { #testing-dependencies-with-overrides }

## Testing के दौरान dependencies को override करना { #overriding-dependencies-during-testing }

कुछ scenarios होते हैं जहाँ आप testing के दौरान किसी dependency को override करना चाह सकते हैं।

आप नहीं चाहते कि original dependency चले (और न ही उसकी कोई sub-dependencies चलें)।

इसके बजाय, आप एक अलग dependency देना चाहते हैं जो केवल tests के दौरान इस्तेमाल होगी (संभवतः केवल कुछ खास tests में), और वह एक ऐसा value देगी जिसे वहाँ इस्तेमाल किया जा सके जहाँ original dependency का value इस्तेमाल किया जाता था।

### Use cases: external service { #use-cases-external-service }

एक उदाहरण यह हो सकता है कि आपके पास एक external authentication provider हो जिसे आपको call करना हो।

आप उसे एक token भेजते हैं और वह एक authenticated user लौटाता है।

यह provider आपसे प्रति request शुल्क ले सकता है, और इसे call करने में tests के लिए एक fixed mock user रखने की तुलना में कुछ अतिरिक्त समय लग सकता है।

आप शायद external provider को एक बार test करना चाहेंगे, लेकिन हर चलने वाले test के लिए उसे call करना जरूरी नहीं होगा।

इस मामले में, आप उस dependency को override कर सकते हैं जो उस provider को call करती है, और अपनी tests के लिए एक custom dependency इस्तेमाल कर सकते हैं जो एक mock user लौटाती है।

### `app.dependency_overrides` attribute का उपयोग करें { #use-the-app-dependency-overrides-attribute }

इन मामलों के लिए, आपकी **FastAPI** application में एक attribute `app.dependency_overrides` होता है, यह एक simple `dict` है।

Testing के लिए किसी dependency को override करने के लिए, आप key के रूप में original dependency (एक function) रखते हैं, और value के रूप में अपना dependency override (दूसरा function) रखते हैं।

और फिर **FastAPI** original dependency की बजाय उस override को call करेगा।

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | सुझाव

आप अपनी **FastAPI** application में कहीं भी इस्तेमाल की गई dependency के लिए dependency override set कर सकते हैं।

Original dependency किसी *path operation function*, किसी *path operation decorator* (जब आप return value का उपयोग नहीं करते), किसी `.include_router()` call आदि में इस्तेमाल हो सकती है।

FastAPI फिर भी उसे override कर पाएगा।

///

फिर आप `app.dependency_overrides` को एक खाली `dict` पर set करके अपने overrides reset कर सकते हैं (उन्हें हटा सकते हैं):

```Python
app.dependency_overrides = {}
```

/// tip | सुझाव

यदि आप किसी dependency को केवल कुछ tests के दौरान override करना चाहते हैं, तो आप test की शुरुआत में (test function के अंदर) override set कर सकते हैं और अंत में (test function के अंत में) उसे reset कर सकते हैं।

///
