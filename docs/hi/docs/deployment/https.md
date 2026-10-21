# HTTPS के बारे में { #about-https }

यह मान लेना आसान है कि HTTPS कोई ऐसी चीज़ है जिसे बस "enabled" किया जाता है या नहीं।

लेकिन यह उससे कहीं ज़्यादा जटिल है।

/// tip | सुझाव

अगर आप जल्दी में हैं या आपको परवाह नहीं है, तो अलग-अलग तकनीकों के साथ सब कुछ setup करने के लिए step by step निर्देशों हेतु अगले sections पर जाएँ।

///

**HTTPS की मूल बातें सीखने** के लिए, एक उपभोक्ता के दृष्टिकोण से, देखें [https://howhttps.works/](https://howhttps.works/)।

अब, एक **developer के दृष्टिकोण** से, HTTPS के बारे में सोचते समय ध्यान रखने योग्य कई बातें यहाँ हैं:

* HTTPS के लिए, **server** के पास **तीसरे पक्ष** द्वारा बनाए गए "certificates" होने चाहिए।
    * वे certificates वास्तव में तीसरे पक्ष से **प्राप्त** किए जाते हैं, "generated" नहीं।
* Certificates की एक **lifespan** होती है।
    * वे **expire** हो जाते हैं।
    * और फिर उन्हें **renew** करना पड़ता है, तीसरे पक्ष से **फिर से प्राप्त** करना पड़ता है।
* connection का encryption **TCP level** पर होता है।
    * यह **HTTP से एक layer नीचे** है।
    * इसलिए, **certificate और encryption** handling **HTTP से पहले** की जाती है।
* **TCP को "domains" के बारे में पता नहीं होता**। केवल IP addresses के बारे में।
    * जिस **विशिष्ट domain** का request किया गया है, उसकी जानकारी **HTTP data** में जाती है।
* **HTTPS certificates** किसी **विशिष्ट domain** को "certify" करते हैं, लेकिन protocol और encryption TCP level पर होते हैं, इस domain को जानने से **पहले** कि किस domain से निपटा जा रहा है।
* **By default**, इसका मतलब होगा कि आपके पास **प्रति IP address केवल एक HTTPS certificate** हो सकता है।
    * इससे कोई फर्क नहीं पड़ता कि आपका server कितना बड़ा है या उस पर मौजूद हर application कितनी छोटी हो सकती है।
    * हालांकि, इसका एक **समाधान** है।
* **TLS** protocol (जो HTTP से पहले, TCP level पर encryption संभालता है) के लिए एक **extension** है जिसे **[<abbr title="Server Name Indication - सर्वर नाम संकेत">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)** कहा जाता है।
    * यह SNI extension एक ही server (एक **single IP address** के साथ) को **कई HTTPS certificates** रखने और **कई HTTPS domains/applications** serve करने की अनुमति देता है।
    * इसे काम करने के लिए, server पर चल रहे, **public IP address** पर listen कर रहे, एक **single** component (program) के पास server में **सभी HTTPS certificates** होने चाहिए।
* सुरक्षित connection प्राप्त करने के **बाद**, communication protocol **अभी भी HTTP** रहता है।
    * contents **encrypted** होते हैं, भले ही उन्हें **HTTP protocol** के साथ भेजा जा रहा हो।

Server (machine, host, आदि) पर **एक program/HTTP server** चलाना और **HTTPS के सभी हिस्सों को manage** करना एक सामान्य practice है: **encrypted HTTPS requests** प्राप्त करना, उसी server में चल रही वास्तविक HTTP application (इस मामले में **FastAPI** application) को **decrypted HTTP requests** भेजना, application से **HTTP response** लेना, उपयुक्त **HTTPS certificate** का उपयोग करके उसे **encrypt** करना और **HTTPS** का उपयोग करके client को वापस भेजना। इस server को अक्सर **[TLS Termination Proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy)** कहा जाता है।

TLS Termination Proxy के रूप में आप जिन options का उपयोग कर सकते हैं, उनमें से कुछ हैं:

* Traefik (जो certificate renewals भी handle कर सकता है)
* Caddy (जो certificate renewals भी handle कर सकता है)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Let's Encrypt से पहले, ये **HTTPS certificates** trusted तीसरे पक्षों द्वारा बेचे जाते थे।

इनमें से किसी certificate को प्राप्त करने की प्रक्रिया कठिन होती थी, काफी paperwork की जरूरत होती थी और certificates काफी महंगे होते थे।

लेकिन फिर **[Let's Encrypt](https://letsencrypt.org/)** बनाया गया।

यह Linux Foundation का एक project है। यह automated तरीके से **मुफ्त में HTTPS certificates** प्रदान करता है। ये certificates सभी standard cryptographic security का उपयोग करते हैं, और short-lived होते हैं (लगभग 3 महीने), इसलिए उनकी कम lifespan के कारण **security वास्तव में बेहतर** होती है।

Domains को सुरक्षित रूप से verify किया जाता है और certificates automatically generate किए जाते हैं। इससे इन certificates के renewal को automate करना भी संभव होता है।

विचार यह है कि इन certificates की acquisition और renewal को automate किया जाए ताकि आपके पास **secure HTTPS, मुफ्त में, हमेशा के लिए** हो सके।

## Developers के लिए HTTPS { #https-for-developers }

यहाँ step by step एक उदाहरण है कि HTTPS API कैसी दिख सकती है, मुख्य रूप से developers के लिए महत्वपूर्ण विचारों पर ध्यान देते हुए।

### Domain Name { #domain-name }

सब कुछ शायद आपके द्वारा कोई **domain name** **प्राप्त** करने से शुरू होगा। फिर, आप इसे DNS server में configure करेंगे (संभवतः आपके उसी cloud provider में)।

आप शायद एक cloud server (एक virtual machine) या कुछ समान प्राप्त करेंगे, और उसके पास एक <dfn title="समय के साथ नहीं बदलता। dynamic नहीं।">स्थिर</dfn> **public IP address** होगा।

DNS server(s) में आप एक record (एक "`A record`") configure करेंगे ताकि **आपका domain** आपके server के public **IP address** की ओर point करे।

आप शायद यह सिर्फ एक बार करेंगे, पहली बार, जब सब कुछ setup कर रहे होंगे।

/// tip | सुझाव

यह Domain Name वाला हिस्सा HTTPS से बहुत पहले का है, लेकिन चूँकि सब कुछ domain और IP address पर निर्भर करता है, इसलिए इसे यहाँ mention करना उचित है।

///

### DNS { #dns }

अब आइए वास्तविक HTTPS parts पर focus करें।

सबसे पहले, browser **DNS servers** से check करेगा कि **domain के लिए IP** क्या है, इस मामले में, `someapp.example.com`।

DNS servers browser को किसी विशिष्ट **IP address** का उपयोग करने के लिए कहेंगे। यह आपके server द्वारा उपयोग किया जाने वाला public IP address होगा, जिसे आपने DNS servers में configure किया है।

<img src="/img/deployment/https/https01.drawio.svg">

### TLS Handshake Start { #tls-handshake-start }

Browser फिर उस IP address से **port 443** (HTTPS port) पर communicate करेगा।

Communication का पहला हिस्सा केवल client और server के बीच connection establish करना और वे कौन-सी cryptographic keys उपयोग करेंगे आदि तय करना है।

<img src="/img/deployment/https/https02.drawio.svg">

TLS connection establish करने के लिए client और server के बीच इस interaction को **TLS handshake** कहा जाता है।

### SNI Extension के साथ TLS { #tls-with-sni-extension }

Server में **केवल एक process** किसी विशिष्ट **IP address** में किसी विशिष्ट **port** पर listen कर सकता है। उसी IP address में दूसरे ports पर अन्य processes listen कर सकते हैं, लेकिन IP address और port के हर combination के लिए केवल एक।

TLS (HTTPS) by default विशिष्ट port `443` का उपयोग करता है। इसलिए हमें इसी port की जरूरत होगी।

क्योंकि इस port पर केवल एक process listen कर सकता है, जो process यह करेगा वह **TLS Termination Proxy** होगा।

TLS Termination Proxy के पास एक या अधिक **TLS certificates** (HTTPS certificates) तक access होगा।

ऊपर चर्चा किए गए **SNI extension** का उपयोग करके, TLS Termination Proxy check करेगा कि इस connection के लिए उपलब्ध TLS (HTTPS) certificates में से किसका उपयोग करना चाहिए, client द्वारा expected domain से match करने वाले certificate का उपयोग करते हुए।

इस मामले में, यह `someapp.example.com` के लिए certificate का उपयोग करेगा।

<img src="/img/deployment/https/https03.drawio.svg">

Client पहले से ही उस entity पर **trust** करता है जिसने वह TLS certificate generate किया है (इस मामले में Let's Encrypt, लेकिन हम इसके बारे में बाद में देखेंगे), इसलिए यह **verify** कर सकता है कि certificate valid है।

फिर, certificate का उपयोग करके, client और TLS Termination Proxy **तय करते हैं कि बाकी TCP communication को कैसे encrypt करना है**। इससे **TLS Handshake** वाला हिस्सा पूरा होता है।

इसके बाद, client और server के पास एक **encrypted TCP connection** होता है, यही TLS प्रदान करता है। और फिर वे उस connection का उपयोग वास्तविक **HTTP communication** शुरू करने के लिए कर सकते हैं।

और **HTTPS** यही है, यह pure (unencrypted) TCP connection के बजाय एक **secure TLS connection** के अंदर साधारण **HTTP** ही है।

/// tip | सुझाव

ध्यान दें कि communication का encryption **TCP level** पर होता है, HTTP level पर नहीं।

///

### HTTPS Request { #https-request }

अब जबकि client और server (विशेष रूप से browser और TLS Termination Proxy) के पास एक **encrypted TCP connection** है, वे **HTTP communication** शुरू कर सकते हैं।

तो, client एक **HTTPS request** भेजता है। यह encrypted TLS connection के माध्यम से बस एक HTTP request है।

<img src="/img/deployment/https/https04.drawio.svg">

### Request को Decrypt करें { #decrypt-the-request }

TLS Termination Proxy सहमत किए गए encryption का उपयोग **request को decrypt** करने के लिए करेगा, और **साधारण (decrypted) HTTP request** को application चलाने वाले process तक transmit करेगा (उदाहरण के लिए FastAPI application चलाने वाले Uvicorn के साथ एक process)।

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP Response { #http-response }

Application request को process करेगी और TLS Termination Proxy को एक **साधारण (unencrypted) HTTP response** भेजेगी।

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS Response { #https-response }

TLS Termination Proxy फिर पहले सहमत cryptography (जो `someapp.example.com` के लिए certificate से शुरू हुई थी) का उपयोग करके **response को encrypt** करेगा, और इसे browser को वापस भेजेगा।

इसके बाद, browser verify करेगा कि response valid है और सही cryptographic key आदि से encrypted है। फिर वह **response को decrypt** करेगा और process करेगा।

<img src="/img/deployment/https/https07.drawio.svg">

Client (browser) को पता होगा कि response सही server से आया है क्योंकि यह उस cryptography का उपयोग कर रहा है जिस पर उन्होंने पहले **HTTPS certificate** का उपयोग करके सहमति की थी।

### Multiple Applications { #multiple-applications }

उसी server (या servers) में, **multiple applications** हो सकती हैं, उदाहरण के लिए, अन्य API programs या database।

केवल एक process विशिष्ट IP और port handle कर सकता है (हमारे उदाहरण में TLS Termination Proxy) लेकिन अन्य applications/processes भी server(s) पर चल सकते हैं, जब तक वे **public IP और port के उसी combination** का उपयोग करने की कोशिश नहीं करते।

<img src="/img/deployment/https/https08.drawio.svg">

इस तरह, TLS Termination Proxy **multiple domains** के लिए, multiple applications के लिए HTTPS और certificates handle कर सकता है, और फिर हर मामले में requests को सही application तक transmit कर सकता है।

### Certificate Renewal { #certificate-renewal }

भविष्य में किसी समय, प्रत्येक certificate **expire** हो जाएगा (इसे प्राप्त करने के लगभग 3 महीने बाद)।

और फिर, कोई दूसरा program होगा (कुछ मामलों में यह दूसरा program होता है, कुछ मामलों में यह वही TLS Termination Proxy हो सकता है) जो Let's Encrypt से बात करेगा, और certificate(s) को renew करेगा।

<img src="/img/deployment/https/https.drawio.svg">

**TLS certificates** किसी **domain name** से **associated** होते हैं, IP address से नहीं।

इसलिए, certificates renew करने के लिए, renewal program को authority (Let's Encrypt) को **prove** करना होगा कि वह वास्तव में उस domain को **"own" और control** करता है।

ऐसा करने के लिए, और अलग-अलग application needs को accommodate करने के लिए, इसे करने के कई तरीके हैं। कुछ लोकप्रिय तरीके हैं:

* **कुछ DNS records modify करें**।
    * इसके लिए, renewal program को DNS provider की APIs support करनी होंगी, इसलिए, आप जिस DNS provider का उपयोग कर रहे हैं, उसके आधार पर यह option हो भी सकता है या नहीं भी।
* Domain से associated public IP address पर (कम से कम certificate acquisition process के दौरान) **server के रूप में चलें**।
    * जैसा कि हमने ऊपर कहा, केवल एक process किसी विशिष्ट IP और port पर listen कर सकता है।
    * यह उन कारणों में से एक है कि जब वही TLS Termination Proxy certificate renewal process का भी ध्यान रखता है तो यह बहुत उपयोगी होता है।
    * अन्यथा, आपको TLS Termination Proxy को momentarily stop करना पड़ सकता है, certificates प्राप्त करने के लिए renewal program start करना पड़ सकता है, फिर उन्हें TLS Termination Proxy के साथ configure करना पड़ सकता है, और फिर TLS Termination Proxy को restart करना पड़ सकता है। यह ideal नहीं है, क्योंकि जिस समय TLS Termination Proxy off होगा, उस दौरान आपकी app(s) available नहीं होंगी।

App को serve करते हुए भी यह पूरा renewal process, उन मुख्य कारणों में से एक है कि आप application server के साथ सीधे TLS certificates (जैसे Uvicorn) का उपयोग करने के बजाय TLS Termination Proxy के साथ **HTTPS handle करने के लिए एक अलग system** रखना चाहेंगे।

## Proxy Forwarded Headers { #proxy-forwarded-headers }

HTTPS handle करने के लिए proxy का उपयोग करते समय, आपका **application server** (उदाहरण के लिए FastAPI CLI के माध्यम से Uvicorn) HTTPS process के बारे में कुछ नहीं जानता, यह **TLS Termination Proxy** के साथ plain HTTP में communicate करता है।

यह **proxy** सामान्यतः request को **application server** तक transmit करने से पहले कुछ HTTP headers on the fly set करेगा, ताकि application server को पता चल सके कि request proxy द्वारा **forwarded** की जा रही है।

/// note | तकनीकी विवरण

Proxy headers हैं:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

फिर भी, क्योंकि **application server** नहीं जानता कि वह trusted **proxy** के पीछे है, by default, वह उन headers पर trust नहीं करेगा।

लेकिन आप **application server** को **proxy** द्वारा भेजे गए *forwarded* headers पर trust करने के लिए configure कर सकते हैं। अगर आप FastAPI CLI का उपयोग कर रहे हैं, तो आप *CLI Option* `--forwarded-allow-ips` का उपयोग करके उसे बता सकते हैं कि उसे किन IPs से आने वाले उन *forwarded* headers पर trust करना चाहिए।

उदाहरण के लिए, अगर **application server** केवल trusted **proxy** से communication receive कर रहा है, तो आप इसे `--forwarded-allow-ips="*"` पर set कर सकते हैं ताकि यह सभी incoming IPs पर trust करे, क्योंकि यह केवल उसी IP से requests receive करेगा जिसका उपयोग **proxy** कर रहा है।

इस तरह application यह जान पाएगी कि उसका अपना public URL क्या है, क्या वह HTTPS का उपयोग कर रही है, domain, आदि।

यह उदाहरण के लिए redirects को ठीक से handle करने में उपयोगी होगा।

/// tip | सुझाव

आप इसके बारे में documentation में और सीख सकते हैं: [Proxy के पीछे - Proxy Forwarded Headers सक्षम करें](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## Recap { #recap }

**HTTPS** होना बहुत महत्वपूर्ण है, और अधिकांश मामलों में काफी **critical** है। HTTPS के आसपास एक developer के रूप में आपको जो ज़्यादातर effort लगाना होता है, वह बस **इन concepts को समझने** और वे कैसे काम करते हैं, इसे समझने के बारे में है।

लेकिन एक बार जब आप **developers के लिए HTTPS** की मूल जानकारी जान लेते हैं, तो आप सब कुछ सरल तरीके से manage करने में मदद के लिए अलग-अलग tools को आसानी से combine और configure कर सकते हैं।

अगले कुछ chapters में, मैं आपको **FastAPI** applications के लिए **HTTPS** setup करने के कई ठोस उदाहरण दिखाऊँगा। 🔒
