# Body - Fields { #body-fields }

जिस तरह आप *path operation function* के parameters में `Query`, `Path` और `Body` के साथ अतिरिक्त validation और metadata घोषित कर सकते हैं, उसी तरह आप Pydantic के `Field` का उपयोग करके Pydantic models के अंदर validation और metadata घोषित कर सकते हैं।

## `Field` import करें { #import-field }

सबसे पहले, आपको इसे import करना होगा:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}


/// warning | चेतावनी

ध्यान दें कि `Field` को सीधे `pydantic` से import किया जाता है, `fastapi` से नहीं, जैसे बाकी सभी (`Query`, `Path`, `Body`, आदि) किए जाते हैं।

///

## model attributes घोषित करें { #declare-model-attributes }

फिर आप model attributes के साथ `Field` का उपयोग कर सकते हैं:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field` उसी तरह काम करता है जैसे `Query`, `Path` और `Body`, इसमें वही सभी parameters आदि होते हैं।

/// note | तकनीकी विवरण

वास्तव में, `Query`, `Path` और अन्य जिन्हें आप आगे देखेंगे, एक सामान्य `Param` class के subclasses के objects बनाते हैं, जो स्वयं Pydantic की `FieldInfo` class का subclass है।

और Pydantic का `Field` भी `FieldInfo` का एक instance लौटाता है।

`Body` भी सीधे `FieldInfo` के subclass के objects लौटाता है। और कुछ अन्य भी हैं जिन्हें आप बाद में देखेंगे, जो `Body` class के subclasses हैं।

याद रखें कि जब आप `fastapi` से `Query`, `Path` और अन्य import करते हैं, तो वे वास्तव में functions होते हैं जो विशेष classes लौटाते हैं।

///

/// tip | सुझाव

ध्यान दें कि type, default value और `Field` वाले हर model के attribute की संरचना *path operation function* के parameter जैसी ही होती है, बस `Path`, `Query` और `Body` की जगह `Field` होता है।

///

## अतिरिक्त जानकारी जोड़ें { #add-extra-information }

आप `Field`, `Query`, `Body` आदि में अतिरिक्त जानकारी घोषित कर सकते हैं। और यह जनरेट किए गए JSON Schema में शामिल होगी।

आप docs में आगे examples घोषित करना सीखते समय अतिरिक्त जानकारी जोड़ने के बारे में और जानेंगे।

/// warning | चेतावनी

`Field` को दिए गए अतिरिक्त keys आपके application के परिणामी OpenAPI schema में भी मौजूद होंगे।
क्योंकि ये keys जरूरी नहीं कि OpenAPI specification का हिस्सा हों, इसलिए कुछ OpenAPI tools, उदाहरण के लिए [OpenAPI validator](https://validator.swagger.io/), आपके जनरेट किए गए schema के साथ काम नहीं कर सकते।

///

## Recap { #recap }

आप model attributes के लिए अतिरिक्त validations और metadata घोषित करने के लिए Pydantic के `Field` का उपयोग कर सकते हैं।

आप अतिरिक्त JSON Schema metadata पास करने के लिए extra keyword arguments का भी उपयोग कर सकते हैं।
