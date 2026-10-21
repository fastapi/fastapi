# HTTP Basic Auth { #http-basic-auth }

सबसे सरल मामलों के लिए, आप HTTP Basic Auth का उपयोग कर सकते हैं।

HTTP Basic Auth में, application एक header की अपेक्षा करता है जिसमें username और password होता है।

अगर उसे यह नहीं मिलता, तो यह HTTP 401 "Unauthorized" error लौटाता है।

और `WWW-Authenticate` header लौटाता है जिसका value `Basic` होता है, और एक optional `realm` parameter होता है।

यह browser को username और password के लिए integrated prompt दिखाने को कहता है।

फिर, जब आप वह username और password टाइप करते हैं, तो browser उन्हें header में अपने-आप भेज देता है।

## Simple HTTP Basic Auth { #simple-http-basic-auth }

* `HTTPBasic` और `HTTPBasicCredentials` import करें।
* `HTTPBasic` का उपयोग करके एक "`security` scheme" बनाएँ।
* अपने *path operation* में dependency के साथ उस `security` का उपयोग करें।
* यह `HTTPBasicCredentials` type का एक object लौटाता है:
    * इसमें भेजे गए `username` और `password` होते हैं।

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

जब आप पहली बार URL खोलने की कोशिश करते हैं (या docs में "Execute" button पर क्लिक करते हैं), तो browser आपसे आपका username और password पूछेगा:

<img src="/img/tutorial/security/image12.png">

## Username जाँचें { #check-the-username }

यहाँ एक अधिक complete example है।

यह जाँचने के लिए dependency का उपयोग करें कि username और password सही हैं या नहीं।

इसके लिए, username और password जाँचने के लिए Python standard module [`secrets`](https://docs.python.org/3/library/secrets.html) का उपयोग करें।

`secrets.compare_digest()` को `bytes` या ऐसा `str` लेना होता है जिसमें केवल ASCII characters (English वाले) हों, इसका मतलब है कि यह `á` जैसे characters के साथ काम नहीं करेगा, जैसे `Sebastián` में।

इसे handle करने के लिए, हम पहले `username` और `password` को UTF-8 से encode करके `bytes` में convert करते हैं।

फिर हम `secrets.compare_digest()` का उपयोग करके यह सुनिश्चित कर सकते हैं कि `credentials.username` `"stanleyjobson"` है, और `credentials.password` `"swordfish"` है।

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

यह इसके समान होगा:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # कोई error लौटाएँ
    ...
```

लेकिन `secrets.compare_digest()` का उपयोग करने से यह "timing attacks" नाम के attacks के एक type के विरुद्ध सुरक्षित रहेगा।

### Timing Attacks { #timing-attacks }

लेकिन "timing attack" क्या होता है?

मान लीजिए कुछ attackers username और password का अनुमान लगाने की कोशिश कर रहे हैं।

और वे username `johndoe` और password `love123` के साथ एक request भेजते हैं।

तब आपकी application में Python code कुछ इस तरह के बराबर होगा:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

लेकिन जैसे ही Python `johndoe` में पहले `j` की तुलना `stanleyjobson` में पहले `s` से करता है, यह `False` लौटा देगा, क्योंकि उसे पहले से पता है कि ये दोनों strings समान नहीं हैं, यह सोचते हुए कि "बाकी अक्षरों की तुलना करके और computation खर्च करने की जरूरत नहीं है"। और आपकी application कहेगी "Incorrect username or password"।

लेकिन फिर attackers username `stanleyjobsox` और password `love123` के साथ कोशिश करते हैं।

और आपका application code कुछ ऐसा करता है:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python को यह समझने से पहले कि दोनों strings समान नहीं हैं, `stanleyjobsox` और `stanleyjobson` दोनों में पूरे `stanleyjobso` की तुलना करनी पड़ेगी। इसलिए "Incorrect username or password" का reply वापस देने में कुछ extra microseconds लगेंगे।

#### जवाब देने में लगा समय attackers की मदद करता है { #the-time-to-answer-helps-the-attackers }

उस समय, यह देखकर कि server ने "Incorrect username or password" response भेजने में कुछ microseconds ज्यादा लिए, attackers जान जाएँगे कि उन्होंने _कुछ_ सही पाया है, शुरुआती अक्षरों में से कुछ सही थे।

और फिर वे यह जानते हुए फिर कोशिश कर सकते हैं कि यह शायद `johndoe` की तुलना में `stanleyjobsox` से ज्यादा मिलता-जुलता है।

#### एक "professional" attack { #a-professional-attack }

बेशक, attackers यह सब हाथ से नहीं करेंगे, वे इसे करने के लिए एक program लिखेंगे, संभवतः प्रति सेकंड हजारों या लाखों tests के साथ। और उन्हें एक समय में बस एक extra सही अक्षर मिलेगा।

लेकिन ऐसा करते हुए, कुछ minutes या hours में attackers ने हमारी application की "help" से सही username और password का अनुमान लगा लिया होगा, सिर्फ जवाब देने में लगे समय का उपयोग करके।

#### इसे `secrets.compare_digest()` से ठीक करें { #fix-it-with-secrets-compare-digest }

लेकिन हमारे code में हम वास्तव में `secrets.compare_digest()` का उपयोग कर रहे हैं।

संक्षेप में, `stanleyjobsox` की तुलना `stanleyjobson` से करने में उतना ही समय लगेगा जितना `johndoe` की तुलना `stanleyjobson` से करने में लगता है। और password के लिए भी वही।

इस तरह, अपने application code में `secrets.compare_digest()` का उपयोग करके, यह security attacks की इस पूरी range के विरुद्ध सुरक्षित रहेगा।

### Error लौटाएँ { #return-the-error }

यह detect करने के बाद कि credentials incorrect हैं, status code 401 (वही जो तब लौटाया जाता है जब कोई credentials provide नहीं किए जाते) के साथ एक `HTTPException` लौटाएँ और browser को login prompt फिर से दिखाने के लिए `WWW-Authenticate` header जोड़ें:

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
