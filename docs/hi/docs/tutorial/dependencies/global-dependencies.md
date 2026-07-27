# वैश्विक Dependencies { #global-dependencies }

कुछ प्रकार के applications के लिए आप पूरे application में dependencies जोड़ना चाह सकते हैं।

जिस तरह आप [*path operation decorators* में `dependencies` जोड़ सकते हैं](dependencies-in-path-operation-decorators.md), उसी तरह आप उन्हें `FastAPI` application में भी जोड़ सकते हैं।

उस स्थिति में, वे application की सभी *path operations* पर लागू होंगी:

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}


और [*path operation decorators* में `dependencies` जोड़ने](dependencies-in-path-operation-decorators.md) वाले section की सभी बातें अभी भी लागू होती हैं, लेकिन इस मामले में, app की सभी *path operations* पर।

## *path operations* के समूहों के लिए Dependencies { #dependencies-for-groups-of-path-operations }

बाद में, जब आप बड़े applications को संरचित करने के तरीके के बारे में पढ़ेंगे ([बड़े Applications - कई Files](../../tutorial/bigger-applications.md)), संभवतः कई files के साथ, तो आप सीखेंगे कि *path operations* के एक समूह के लिए एक ही `dependencies` parameter कैसे declare किया जाए।
