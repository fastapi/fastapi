# Password के साथ OAuth2 (और hashing), JWT tokens के साथ Bearer { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

अब जब हमारे पास पूरा security flow है, तो आइए <abbr title="JSON Web Tokens - JSON वेब टोकन">JWT</abbr> tokens और secure password hashing का उपयोग करके application को वास्तव में secure बनाते हैं।

यह code ऐसा है जिसे आप अपनी application में सच में उपयोग कर सकते हैं, password hashes को अपने database में save कर सकते हैं, आदि।

हम पिछले chapter में जहाँ छोड़ा था, वहीं से शुरू करेंगे और उसे आगे बढ़ाएँगे।

## JWT के बारे में { #about-jwt }

JWT का मतलब है "JSON Web Tokens"।

यह एक JSON object को बिना spaces वाली लंबी dense string में codify करने का standard है। यह ऐसा दिखता है:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

यह encrypted नहीं है, इसलिए कोई भी contents से जानकारी वापस प्राप्त कर सकता है।

लेकिन यह signed है। इसलिए, जब आपको कोई token मिलता है जिसे आपने issue किया था, तो आप verify कर सकते हैं कि उसे आपने ही issue किया था।

इस तरह, आप एक token बना सकते हैं जिसकी expiration, मान लीजिए, 1 week हो। और फिर जब user अगले दिन token के साथ वापस आता है, तो आपको पता होता है कि वह user अभी भी आपके system में logged in है।

एक week के बाद, token expired हो जाएगा और user authorized नहीं होगा और नया token पाने के लिए उसे फिर से sign in करना होगा। और अगर user (या कोई third party) expiration बदलने के लिए token को modify करने की कोशिश करे, तो आप इसे पता लगा पाएँगे, क्योंकि signatures match नहीं होंगे।

अगर आप JWT tokens के साथ प्रयोग करना चाहते हैं और देखना चाहते हैं कि वे कैसे काम करते हैं, तो [https://jwt.io](https://jwt.io/) देखें।

## `PyJWT` install करें { #install-pyjwt }

Python में JWT tokens generate और verify करने के लिए हमें `PyJWT` install करना होगा।

सुनिश्चित करें कि आप एक [virtual environment](../../virtual-environments.md) बनाएँ, उसे activate करें, और फिर `pyjwt` install करें:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// note | नोट

अगर आप RSA या ECDSA जैसे digital signature algorithms का उपयोग करने की योजना बना रहे हैं, तो आपको cryptography library dependency `pyjwt[crypto]` install करनी चाहिए।

आप इसके बारे में [PyJWT Installation docs](https://pyjwt.readthedocs.io/en/latest/installation.html) में और पढ़ सकते हैं।

///

## Password hashing { #password-hashing }

"Hashing" का मतलब है किसी content (इस मामले में password) को bytes के sequence (बस एक string) में बदलना, जो बेकार/असमझ text जैसा दिखता है।

जब भी आप बिल्कुल वही content (बिल्कुल वही password) pass करते हैं, आपको बिल्कुल वही gibberish मिलता है।

लेकिन आप उस gibberish से वापस password में convert नहीं कर सकते।

### Password hashing क्यों उपयोग करें { #why-use-password-hashing }

अगर आपका database चोरी हो जाता है, तो चोर के पास आपके users के plaintext passwords नहीं होंगे, केवल hashes होंगे।

इसलिए, चोर उस password को किसी दूसरे system में उपयोग करने की कोशिश नहीं कर पाएगा (क्योंकि कई users हर जगह वही password उपयोग करते हैं, यह खतरनाक होगा)।

## `pwdlib` install करें { #install-pwdlib }

pwdlib password hashes संभालने के लिए एक शानदार Python package है।

यह कई secure hashing algorithms और उनके साथ काम करने के लिए utilities support करता है।

Recommended algorithm "Argon2" है।

सुनिश्चित करें कि आप एक [virtual environment](../../virtual-environments.md) बनाएँ, उसे activate करें, और फिर Argon2 के साथ pwdlib install करें:

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | सुझाव

`pwdlib` के साथ, आप इसे इस तरह configure भी कर सकते हैं कि यह **Django**, **Flask** security plug-in या कई अन्य द्वारा बनाए गए passwords read कर सके।

तो, उदाहरण के लिए, आप एक database में Django application का वही data FastAPI application के साथ share कर पाएँगे। या उसी database का उपयोग करते हुए धीरे-धीरे Django application को migrate कर पाएँगे।

और आपके users एक ही समय में आपकी Django app या आपकी **FastAPI** app से login कर पाएँगे।

///

## Passwords को hash और verify करें { #hash-and-verify-the-passwords }

`pwdlib` से वे tools import करें जिनकी हमें ज़रूरत है।

Recommended settings के साथ एक PasswordHash instance बनाएँ - इसका उपयोग passwords को hash और verify करने के लिए किया जाएगा।

/// tip | सुझाव

pwdlib bcrypt hashing algorithm को भी support करता है लेकिन legacy algorithms शामिल नहीं करता - outdated hashes के साथ काम करने के लिए passlib library का उपयोग करना recommended है।

उदाहरण के लिए, आप इसका उपयोग किसी दूसरे system (जैसे Django) द्वारा generate किए गए passwords read और verify करने के लिए कर सकते हैं, लेकिन किसी भी नए passwords को Argon2 या Bcrypt जैसे अलग algorithm से hash कर सकते हैं।

और एक ही समय में उन सभी के साथ compatible रह सकते हैं।

///

User से आने वाले password को hash करने के लिए एक utility function बनाएँ।

और एक और utility बनाएँ जो verify करे कि received password stored hash से match करता है या नहीं।

और एक और utility बनाएँ जो authenticate करे और user return करे।

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

जब `authenticate_user` को ऐसे username के साथ call किया जाता है जो database में मौजूद नहीं है, तब भी हम dummy hash के against `verify_password` चलाते हैं।

यह सुनिश्चित करता है कि username valid हो या न हो, endpoint response देने में लगभग समान समय ले, जिससे **timing attacks** रोके जा सकें जिनका उपयोग मौजूदा usernames enumerate करने के लिए किया जा सकता है।

/// note | नोट

अगर आप नए (fake) database `fake_users_db` को check करेंगे, तो आप देखेंगे कि hashed password अब कैसा दिखता है: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`।

///

## JWT tokens संभालें { #handle-jwt-tokens }

Installed modules import करें।

एक random secret key बनाएँ जिसका उपयोग JWT tokens sign करने के लिए किया जाएगा।

Secure random secret key generate करने के लिए command उपयोग करें:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

और output को variable `SECRET_KEY` में copy करें (example वाला उपयोग न करें)।

JWT token sign करने के लिए उपयोग किए गए algorithm के साथ एक variable `ALGORITHM` बनाएँ और इसे `"HS256"` पर set करें।

Token की expiration के लिए एक variable बनाएँ।

एक Pydantic Model define करें जिसका उपयोग response के लिए token endpoint में किया जाएगा।

नया access token generate करने के लिए एक utility function बनाएँ।

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Dependencies update करें { #update-the-dependencies }

`get_current_user` को update करें ताकि वह पहले जैसा ही token receive करे, लेकिन इस बार JWT tokens का उपयोग करते हुए।

Received token को decode करें, verify करें, और current user return करें।

अगर token invalid है, तो तुरंत HTTP error return करें।

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## `/token` *path operation* update करें { #update-the-token-path-operation }

Token की expiration time के साथ एक `timedelta` बनाएँ।

एक वास्तविक JWT access token बनाएँ और उसे return करें।

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### JWT "subject" `sub` के बारे में technical details { #technical-details-about-the-jwt-subject-sub }

JWT specification कहता है कि token के subject के साथ एक key `sub` होती है।

इसका उपयोग करना optional है, लेकिन यही वह जगह है जहाँ आप user की identification रखेंगे, इसलिए हम इसे यहाँ उपयोग कर रहे हैं।

JWT का उपयोग user की पहचान करने और उन्हें आपकी API पर सीधे operations perform करने की अनुमति देने के अलावा अन्य चीज़ों के लिए भी किया जा सकता है।

उदाहरण के लिए, आप एक "car" या एक "blog post" की पहचान कर सकते हैं।

फिर आप उस entity के बारे में permissions जोड़ सकते हैं, जैसे "drive" (car के लिए) या "edit" (blog के लिए)।

और फिर, आप वह JWT token किसी user (या bot) को दे सकते हैं, और वे उन actions को perform करने के लिए इसका उपयोग कर सकते हैं (car drive करना, या blog post edit करना), बिना account की ज़रूरत के, केवल उस JWT token के साथ जिसे आपकी API ने इसके लिए generate किया है।

इन ideas का उपयोग करके, JWT का उपयोग कहीं अधिक sophisticated scenarios के लिए किया जा सकता है।

इन cases में, उन entities में से कई की same ID हो सकती है, मान लीजिए `foo` (एक user `foo`, एक car `foo`, और एक blog post `foo`)।

इसलिए, ID collisions से बचने के लिए, user के लिए JWT token बनाते समय, आप `sub` key के value के आगे prefix जोड़ सकते हैं, जैसे `username:`। इसलिए, इस example में, `sub` का value हो सकता था: `username:johndoe`।

ध्यान रखने वाली महत्वपूर्ण बात यह है कि `sub` key के पास पूरी application में unique identifier होना चाहिए, और यह एक string होना चाहिए।

## इसे check करें { #check-it }

Server run करें और docs पर जाएँ: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)।

आप user interface ऐसा देखेंगे:

<img src="/img/tutorial/security/image07.png">

Application को पहले की तरह ही authorize करें।

Credentials का उपयोग करते हुए:

Username: `johndoe`
Password: `secret`

/// tip | सुझाव

ध्यान दें कि code में कहीं भी plaintext password "`secret`" नहीं है, हमारे पास केवल hashed version है।

///

<img src="/img/tutorial/security/image08.png">

Endpoint `/users/me/` call करें, आपको response इस तरह मिलेगा:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

अगर आप developer tools खोलते हैं, तो आप देख सकते हैं कि भेजे गए data में केवल token शामिल है, password केवल पहले request में user को authenticate करने और वह access token पाने के लिए भेजा जाता है, लेकिन उसके बाद नहीं:

<img src="/img/tutorial/security/image10.png">

/// note | नोट

`Authorization` header पर ध्यान दें, जिसका value `Bearer ` से शुरू होता है।

///

## `scopes` के साथ advanced उपयोग { #advanced-usage-with-scopes }

OAuth2 में "scopes" की धारणा है।

आप उनका उपयोग JWT token में permissions का specific set जोड़ने के लिए कर सकते हैं।

फिर आप यह token सीधे किसी user या third party को दे सकते हैं, ताकि वे restrictions के set के साथ आपकी API से interact कर सकें।

आप बाद में **Advanced User Guide** में सीख सकते हैं कि उनका उपयोग कैसे करें और वे **FastAPI** में कैसे integrated हैं।

## Recap { #recap }

अब तक आपने जो देखा है, उससे आप OAuth2 और JWT जैसे standards का उपयोग करके एक secure **FastAPI** application setup कर सकते हैं।

लगभग किसी भी framework में security संभालना काफ़ी जल्दी एक जटिल विषय बन जाता है।

कई packages जो इसे बहुत सरल बनाते हैं, उन्हें data model, database, और available features के साथ कई compromises करने पड़ते हैं। और इनमें से कुछ packages जो चीज़ों को बहुत अधिक सरल बना देते हैं, उनके अंदर वास्तव में security flaws होते हैं।

---

**FastAPI** किसी भी database, data model या tool के साथ कोई compromise नहीं करता।

यह आपको उन चीज़ों को चुनने की पूरी flexibility देता है जो आपके project के लिए सबसे अच्छी हों।

और आप सीधे कई well maintained और widely used packages जैसे `pwdlib` और `PyJWT` का उपयोग कर सकते हैं, क्योंकि **FastAPI** external packages integrate करने के लिए किसी complex mechanism की मांग नहीं करता।

लेकिन यह आपको process को जितना संभव हो उतना सरल बनाने के लिए tools देता है, बिना flexibility, robustness, या security से compromise किए।

और आप OAuth2 जैसे secure, standard protocols को अपेक्षाकृत simple तरीके से उपयोग और implement कर सकते हैं।

आप **Advanced User Guide** में और सीख सकते हैं कि अधिक fine-grained permission system के लिए OAuth2 "scopes" का उपयोग कैसे करें, इन्हीं standards का पालन करते हुए। Scopes के साथ OAuth2 वह mechanism है जिसका उपयोग कई बड़े authentication providers, जैसे Facebook, Google, GitHub, Microsoft, X (Twitter), आदि करते हैं, ताकि third party applications को अपने users की ओर से उनकी APIs के साथ interact करने के लिए authorize किया जा सके।
