# OAuth2 scopes { #oauth2-scopes }

आप **FastAPI** के साथ OAuth2 scopes सीधे उपयोग कर सकते हैं, वे निर्बाध रूप से काम करने के लिए एकीकृत हैं।

यह आपको OAuth2 standard का पालन करते हुए, आपकी OpenAPI application (और API docs) में एक अधिक fine-grained permission system रखने की अनुमति देगा।

Scopes के साथ OAuth2 वह mechanism है जिसे कई बड़े authentication providers, जैसे Facebook, Google, GitHub, Microsoft, X (Twitter), आदि उपयोग करते हैं। वे इसका उपयोग users और applications को विशिष्ट permissions देने के लिए करते हैं।

हर बार जब आप Facebook, Google, GitHub, Microsoft, X (Twitter) के साथ "log in with" करते हैं, वह application scopes के साथ OAuth2 का उपयोग कर रही होती है।

इस section में आप देखेंगे कि अपनी **FastAPI** application में उसी scopes वाले OAuth2 के साथ authentication और authorization को कैसे manage करें।

/// warning | चेतावनी

यह थोड़ा-बहुत advanced section है। यदि आप अभी शुरू कर रहे हैं, तो आप इसे छोड़ सकते हैं।

आपको अनिवार्य रूप से OAuth2 scopes की आवश्यकता नहीं है, और आप authentication और authorization को जैसे चाहें handle कर सकते हैं।

लेकिन scopes के साथ OAuth2 को आपकी API (OpenAPI के साथ) और आपकी API docs में अच्छी तरह integrate किया जा सकता है।

फिर भी, आप उन scopes, या किसी भी अन्य security/authorization requirement को अपने code में अपनी आवश्यकता के अनुसार enforce करते हैं।

कई मामलों में, scopes के साथ OAuth2 overkill हो सकता है।

लेकिन यदि आप जानते हैं कि आपको इसकी आवश्यकता है, या आप curious हैं, तो पढ़ते रहें।

///

## OAuth2 scopes और OpenAPI { #oauth2-scopes-and-openapi }

OAuth2 specification "scopes" को spaces से अलग की गई strings की list के रूप में define करती है।

इनमें से प्रत्येक string का content किसी भी format में हो सकता है, लेकिन उसमें spaces नहीं होने चाहिए।

ये scopes "permissions" को दर्शाते हैं।

OpenAPI में (जैसे API docs), आप "security schemes" define कर सकते हैं।

जब इनमें से कोई security scheme OAuth2 का उपयोग करती है, तो आप scopes declare और उपयोग भी कर सकते हैं।

प्रत्येक "scope" बस एक string है (spaces के बिना)।

वे सामान्यतः विशिष्ट security permissions declare करने के लिए उपयोग किए जाते हैं, उदाहरण के लिए:

* `users:read` या `users:write` आम examples हैं।
* `instagram_basic` Facebook / Instagram द्वारा उपयोग किया जाता है।
* `https://www.googleapis.com/auth/drive` Google द्वारा उपयोग किया जाता है।

/// note | नोट

OAuth2 में "scope" बस एक string है जो required विशिष्ट permission declare करती है।

इससे फर्क नहीं पड़ता कि इसमें `:` जैसे अन्य characters हैं या यह एक URL है।

वे details implementation specific हैं।

OAuth2 के लिए वे बस strings हैं।

///

## Global view { #global-view }

पहले, आइए जल्दी से देखें कि मुख्य **Tutorial - User Guide** में [Password के साथ OAuth2 (और hashing), JWT tokens के साथ Bearer](../../tutorial/security/oauth2-jwt.md) के examples से कौन से parts बदलते हैं। अब OAuth2 scopes का उपयोग करते हुए:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

अब आइए उन बदलावों को step by step review करें।

## OAuth2 Security scheme { #oauth2-security-scheme }

पहला बदलाव यह है कि अब हम OAuth2 security scheme को दो उपलब्ध scopes, `me` और `items`, के साथ declare कर रहे हैं।

`scopes` parameter एक `dict` receive करता है जिसमें प्रत्येक scope key के रूप में और description value के रूप में होती है:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

क्योंकि अब हम उन scopes को declare कर रहे हैं, वे API docs में तब दिखाई देंगे जब आप log-in/authorize करेंगे।

और आप select कर सकेंगे कि आप किन scopes को access देना चाहते हैं: `me` और `items`।

यह वही mechanism है जिसका उपयोग तब होता है जब आप Facebook, Google, GitHub, आदि के साथ log in करते समय permissions देते हैं:

<img src="/img/tutorial/security/image11.png">

## Scopes के साथ JWT token { #jwt-token-with-scopes }

अब, token *path operation* को modify करें ताकि requested scopes return हों।

हम अभी भी वही `OAuth2PasswordRequestForm` उपयोग कर रहे हैं। इसमें `scopes` property शामिल है जिसमें `str` की `list` होती है, और request में received प्रत्येक scope होता है।

और हम scopes को JWT token के part के रूप में return करते हैं।

/// danger | खतरा

सरलता के लिए, यहाँ हम received scopes को सीधे token में जोड़ रहे हैं।

लेकिन आपकी application में, security के लिए, आपको सुनिश्चित करना चाहिए कि आप केवल वे scopes जोड़ें जिन्हें user वास्तव में रख सकता है, या जिन्हें आपने predefine किया है।

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## *path operations* और dependencies में scopes declare करें { #declare-scopes-in-path-operations-and-dependencies }

अब हम declare करते हैं कि `/users/me/items/` के लिए *path operation* को scope `items` required है।

इसके लिए, हम `fastapi` से `Security` import और उपयोग करते हैं।

आप dependencies declare करने के लिए `Security` का उपयोग कर सकते हैं (बिल्कुल `Depends` की तरह), लेकिन `Security` एक parameter `scopes` भी receive करता है जिसमें scopes (strings) की list होती है।

इस case में, हम dependency function `get_current_active_user` को `Security` में pass करते हैं (उसी तरह जैसे हम `Depends` के साथ करते)।

लेकिन हम scopes की एक `list` भी pass करते हैं, इस case में केवल एक scope के साथ: `items` (इसमें और भी हो सकते थे)।

और dependency function `get_current_active_user` sub-dependencies भी declare कर सकता है, न केवल `Depends` के साथ बल्कि `Security` के साथ भी। अपना sub-dependency function (`get_current_user`) और अधिक scope requirements declare करते हुए।

इस case में, इसे scope `me` required है (इसे एक से अधिक scope required हो सकते थे)।

/// note | नोट

आपको अलग-अलग जगहों पर अलग-अलग scopes जोड़ना अनिवार्य नहीं है।

हम यहाँ यह demonstrate करने के लिए कर रहे हैं कि **FastAPI** अलग-अलग levels पर declared scopes को कैसे handle करता है।

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// note | तकनीकी विवरण

`Security` वास्तव में `Depends` का subclass है, और इसमें केवल एक extra parameter है जिसे हम बाद में देखेंगे।

लेकिन `Depends` के बजाय `Security` का उपयोग करके, **FastAPI** जान जाएगा कि यह security scopes declare कर सकता है, उन्हें internally उपयोग कर सकता है, और API को OpenAPI के साथ document कर सकता है।

लेकिन जब आप `fastapi` से `Query`, `Path`, `Depends`, `Security` और अन्य import करते हैं, तो वे वास्तव में functions हैं जो special classes return करते हैं।

///

## `SecurityScopes` का उपयोग करें { #use-securityscopes }

अब dependency `get_current_user` को update करें।

यह वही है जिसका उपयोग ऊपर की dependencies द्वारा किया जाता है।

यहीं हम पहले बनाई गई उसी OAuth2 scheme का उपयोग कर रहे हैं, इसे dependency के रूप में declare करते हुए: `oauth2_scheme`।

क्योंकि इस dependency function की अपनी कोई scope requirements नहीं हैं, हम `oauth2_scheme` के साथ `Depends` उपयोग कर सकते हैं, जब हमें security scopes specify करने की आवश्यकता नहीं है तो हमें `Security` उपयोग करने की आवश्यकता नहीं है।

हम `SecurityScopes` type का एक special parameter भी declare करते हैं, जिसे `fastapi.security` से import किया गया है।

यह `SecurityScopes` class `Request` के समान है (`Request` का उपयोग request object को सीधे प्राप्त करने के लिए किया गया था)।

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## `scopes` का उपयोग करें { #use-the-scopes }

Parameter `security_scopes` का type `SecurityScopes` होगा।

इसमें property `scopes` होगी जिसमें एक list होगी, जिसमें स्वयं और इसे sub-dependency के रूप में उपयोग करने वाली सभी dependencies द्वारा required सभी scopes शामिल होंगे। इसका मतलब है, सभी "dependants"... यह confusing लग सकता है, इसे नीचे फिर से समझाया गया है।

`security_scopes` object (`SecurityScopes` class का) एक `scope_str` attribute भी provide करता है जिसमें एक single string होती है, जिसमें वे scopes spaces से अलग होते हैं (हम इसका उपयोग करेंगे)।

हम एक `HTTPException` बनाते हैं जिसे हम बाद में कई points पर reuse (`raise`) कर सकते हैं।

इस exception में, हम required scopes (यदि कोई हों) को spaces से अलग की गई string के रूप में शामिल करते हैं (`scope_str` का उपयोग करके)। हम scopes वाली उस string को `WWW-Authenticate` header में रखते हैं (यह spec का part है)।

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## `username` और data shape verify करें { #verify-the-username-and-data-shape }

हम verify करते हैं कि हमें `username` मिलता है, और scopes extract करते हैं।

और फिर हम उस data को Pydantic model के साथ validate करते हैं (`ValidationError` exception को catch करते हुए), और यदि JWT token पढ़ने या Pydantic के साथ data validate करने में error मिलता है, तो हम पहले बनाया हुआ `HTTPException` raise करते हैं।

इसके लिए, हम Pydantic model `TokenData` को नई property `scopes` के साथ update करते हैं।

Pydantic के साथ data validate करके हम यह सुनिश्चित कर सकते हैं कि हमारे पास, उदाहरण के लिए, scopes के साथ बिल्कुल `str` की `list` और `username` के साथ `str` है।

उदाहरण के लिए, `dict`, या कुछ और नहीं, क्योंकि यह बाद में किसी point पर application को break कर सकता है, जिससे यह security risk बन सकता है।

हम यह भी verify करते हैं कि हमारे पास उस username वाला user है, और यदि नहीं, तो हम वही exception raise करते हैं जो हमने पहले बनाया था।

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## `scopes` verify करें { #verify-the-scopes }

अब हम verify करते हैं कि इस dependency और सभी dependants (जिसमें *path operations* शामिल हैं) द्वारा required सभी scopes, received token में provided scopes में शामिल हैं, अन्यथा `HTTPException` raise करते हैं।

इसके लिए, हम `security_scopes.scopes` का उपयोग करते हैं, जिसमें इन सभी scopes की `list` `str` के रूप में होती है।

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Dependency tree और scopes { #dependency-tree-and-scopes }

आइए इस dependency tree और scopes को फिर से review करें।

क्योंकि `get_current_active_user` dependency में `get_current_user` sub-dependency के रूप में है, `get_current_active_user` पर declared scope `"me"` required scopes की उस list में शामिल होगा जो `get_current_user` को pass किए गए `security_scopes.scopes` में होती है।

*path operation* स्वयं भी एक scope, `"items"`, declare करता है, इसलिए यह भी `get_current_user` को pass किए गए `security_scopes.scopes` की list में होगा।

Dependencies और scopes की hierarchy इस तरह दिखती है:

* *path operation* `read_own_items` में है:
    * Dependency के साथ required scopes `["items"]`:
    * `get_current_active_user`:
        * Dependency function `get_current_active_user` में है:
            * Dependency के साथ required scopes `["me"]`:
            * `get_current_user`:
                * Dependency function `get_current_user` में है:
                    * स्वयं द्वारा required कोई scopes नहीं।
                    * `oauth2_scheme` का उपयोग करने वाली dependency।
                    * `SecurityScopes` type का एक `security_scopes` parameter:
                        * इस `security_scopes` parameter में property `scopes` है जिसमें ऊपर declared इन सभी scopes वाली `list` है, इसलिए:
                            * *path operation* `read_own_items` के लिए `security_scopes.scopes` में `["me", "items"]` होगा।
                            * *path operation* `read_users_me` के लिए `security_scopes.scopes` में `["me"]` होगा, क्योंकि यह dependency `get_current_active_user` में declared है।
                            * *path operation* `read_system_status` के लिए `security_scopes.scopes` में `[]` (कुछ नहीं) होगा, क्योंकि उसने `scopes` के साथ कोई `Security` declare नहीं किया, और उसकी dependency, `get_current_user`, भी कोई `scopes` declare नहीं करती।

/// tip | सुझाव

यहाँ महत्वपूर्ण और "magic" बात यह है कि प्रत्येक *path operation* के लिए `get_current_user` के पास check करने हेतु `scopes` की अलग list होगी।

यह सब उस specific *path operation* के dependency tree में प्रत्येक *path operation* और प्रत्येक dependency में declared `scopes` पर निर्भर करता है।

///

## `SecurityScopes` के बारे में अधिक details { #more-details-about-securityscopes }

आप `SecurityScopes` का उपयोग किसी भी point पर, और multiple जगहों पर कर सकते हैं, इसका "root" dependency पर होना ज़रूरी नहीं है।

इसमें हमेशा current `Security` dependencies और **उस specific** *path operation* तथा **उस specific** dependency tree के सभी dependants में declared security scopes होंगे।

क्योंकि `SecurityScopes` में dependants द्वारा declared सभी scopes होंगे, आप इसका उपयोग यह verify करने के लिए कर सकते हैं कि token में required scopes हैं, एक central dependency function में, और फिर अलग-अलग *path operations* में अलग-अलग scope requirements declare कर सकते हैं।

उन्हें प्रत्येक *path operation* के लिए independently check किया जाएगा।

## इसे check करें { #check-it }

यदि आप API docs खोलते हैं, तो आप authenticate कर सकते हैं और specify कर सकते हैं कि आप किन scopes को authorize करना चाहते हैं।

<img src="/img/tutorial/security/image11.png">

यदि आप कोई scope select नहीं करते हैं, तो आप "authenticated" होंगे, लेकिन जब आप `/users/me/` या `/users/me/items/` access करने की कोशिश करेंगे तो आपको error मिलेगा कि आपके पास पर्याप्त permissions नहीं हैं। आप फिर भी `/status/` access कर पाएंगे।

और यदि आप scope `me` select करते हैं लेकिन scope `items` नहीं, तो आप `/users/me/` access कर पाएंगे लेकिन `/users/me/items/` नहीं।

ऐसा ही किसी third party application के साथ होगा जो user द्वारा provided token के साथ इन *path operations* में से किसी एक को access करने की कोशिश करती, यह इस पर निर्भर करता है कि user ने application को कितनी permissions दीं।

## Third party integrations के बारे में { #about-third-party-integrations }

इस example में हम OAuth2 "password" flow का उपयोग कर रहे हैं।

यह तब appropriate है जब हम अपनी ही application में log in कर रहे हों, शायद अपने ही frontend के साथ।

क्योंकि हम इस पर भरोसा कर सकते हैं कि यह `username` और `password` receive करे, क्योंकि हम इसे control करते हैं।

लेकिन यदि आप ऐसी OAuth2 application बना रहे हैं जिससे दूसरे connect करेंगे (अर्थात, यदि आप Facebook, Google, GitHub, आदि के बराबर authentication provider बना रहे हैं) तो आपको अन्य flows में से किसी एक का उपयोग करना चाहिए।

सबसे common implicit flow है।

सबसे secure code flow है, लेकिन इसे implement करना अधिक complex है क्योंकि इसमें अधिक steps required हैं। क्योंकि यह अधिक complex है, कई providers अंततः implicit flow suggest करते हैं।

/// note | नोट

यह common है कि प्रत्येक authentication provider अपने flows को अलग तरीके से name करता है, ताकि इसे अपने brand का part बना सके।

लेकिन अंततः, वे वही OAuth2 standard implement कर रहे होते हैं।

///

**FastAPI** में इन सभी OAuth2 authentication flows के लिए utilities `fastapi.security.oauth2` में शामिल हैं।

## Decorator `dependencies` में `Security` { #security-in-decorator-dependencies }

जिस तरह आप decorator के `dependencies` parameter में `Depends` की `list` define कर सकते हैं (जैसा कि [path operation decorators में Dependencies](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md) में समझाया गया है), आप वहाँ `scopes` के साथ `Security` भी उपयोग कर सकते हैं।
