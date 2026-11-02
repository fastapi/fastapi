# Current User प्राप्त करें { #get-current-user }

पिछले अध्याय में security system (जो dependency injection system पर आधारित है) *path operation function* को `str` के रूप में एक `token` दे रहा था:

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

लेकिन वह अभी भी इतना उपयोगी नहीं है।

आइए इसे हमें current user देने वाला बनाते हैं।

## एक user model बनाएँ { #create-a-user-model }

पहले, एक Pydantic user model बनाते हैं।

जिस तरह हम bodies declare करने के लिए Pydantic का उपयोग करते हैं, उसी तरह हम इसे कहीं और भी उपयोग कर सकते हैं:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:16] *}

## एक `get_current_user` dependency बनाएँ { #create-a-get-current-user-dependency }

आइए एक dependency `get_current_user` बनाएँ।

याद है कि dependencies की sub-dependencies हो सकती हैं?

`get_current_user` के पास उसी `oauth2_scheme` के साथ एक dependency होगी जिसे हमने पहले बनाया था।

ठीक वैसे ही जैसे हम पहले सीधे *path operation* में कर रहे थे, हमारी नई dependency `get_current_user` sub-dependency `oauth2_scheme` से `str` के रूप में एक `token` प्राप्त करेगी:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## user प्राप्त करें { #get-the-user }

`get_current_user` हमारे द्वारा बनाई गई एक (fake) utility function का उपयोग करेगी, जो token को `str` के रूप में लेती है और हमारा Pydantic `User` model लौटाती है:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## current user inject करें { #inject-the-current-user }

तो अब हम *path operation* में अपने `get_current_user` के साथ वही `Depends` उपयोग कर सकते हैं:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

ध्यान दें कि हम `current_user` का type Pydantic model `User` के रूप में declare करते हैं।

यह function के अंदर completion और type checks में हमारी मदद करेगा।

/// tip | टिप

आपको याद होगा कि request bodies भी Pydantic models के साथ declare की जाती हैं।

यहाँ **FastAPI** confuse नहीं होगा क्योंकि आप `Depends` का उपयोग कर रहे हैं।

///

/// tip | टिप

जिस तरह यह dependency system design किया गया है, वह हमें अलग-अलग dependencies (अलग-अलग "dependables") रखने देता है जो सभी एक `User` model लौटाती हैं।

हम केवल एक dependency तक सीमित नहीं हैं जो उस type का data लौटा सकती है।

///

## अन्य models { #other-models }

अब आप *path operation functions* में सीधे current user प्राप्त कर सकते हैं और `Depends` का उपयोग करके **Dependency Injection** स्तर पर security mechanisms संभाल सकते हैं।

और आप security requirements के लिए कोई भी model या data उपयोग कर सकते हैं (इस मामले में, Pydantic model `User`)।

लेकिन आप किसी विशेष data model, class या type का उपयोग करने तक सीमित नहीं हैं।

क्या आप अपने model में `id` और `email` रखना चाहते हैं और कोई `username` नहीं रखना चाहते? बिल्कुल। आप इन्हीं tools का उपयोग कर सकते हैं।

क्या आप केवल एक `str` रखना चाहते हैं? या केवल एक `dict`? या सीधे database class model instance? सब कुछ उसी तरह काम करता है।

असल में आपके application में login करने वाले users नहीं हैं, बल्कि robots, bots, या अन्य systems हैं, जिनके पास बस एक access token है? फिर भी, सब कुछ उसी तरह काम करता है।

बस अपने application के लिए जिस भी प्रकार का model, जिस भी प्रकार की class, जिस भी प्रकार का database चाहिए, उसका उपयोग करें। **FastAPI** dependency injection system के साथ आपकी ज़रूरतें पूरी करता है।

## Code size { #code-size }

यह example verbose लग सकता है। ध्यान रखें कि हम security, data models, utility functions और *path operations* को उसी file में मिला रहे हैं।

लेकिन यहाँ मुख्य बात है।

security और dependency injection से जुड़ी चीज़ें एक बार लिखी जाती हैं।

और आप इसे जितना चाहें उतना complex बना सकते हैं। फिर भी, यह केवल एक बार, एक ही जगह पर, पूरी flexibility के साथ लिखा जाता है।

लेकिन आपके पास उसी security system का उपयोग करने वाले हजारों endpoints (*path operations*) हो सकते हैं।

और वे सभी (या उनका कोई भी हिस्सा जिसे आप चाहें) इन dependencies या आपके द्वारा बनाई गई किसी भी अन्य dependencies को फिर से उपयोग करने का लाभ उठा सकते हैं।

और ये सभी हजारों *path operations* सिर्फ 3 lines जितने छोटे हो सकते हैं:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Recap { #recap }

अब आप अपने *path operation function* में सीधे current user प्राप्त कर सकते हैं।

हम पहले ही आधे रास्ते तक पहुँच चुके हैं।

हमें बस user/client के लिए एक *path operation* जोड़ना है ताकि वह वास्तव में `username` और `password` भेज सके।

वह आगे आता है।
