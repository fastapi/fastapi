# Deployments की अवधारणाएँ { #deployments-concepts }

जब आप एक **FastAPI** application, या वास्तव में किसी भी प्रकार की web API, deploy करते हैं, तो कई अवधारणाएँ होती हैं जिनकी आपको शायद परवाह होगी, और उनका उपयोग करके आप अपनी application को **deploy करने** का **सबसे उपयुक्त** तरीका ढूँढ सकते हैं।

कुछ महत्वपूर्ण अवधारणाएँ हैं:

* सुरक्षा - HTTPS
* startup पर चलना
* Restarts
* Replication (चल रहे processes की संख्या)
* Memory
* शुरू करने से पहले के पिछले steps

हम देखेंगे कि ये **deployments** को कैसे प्रभावित करेंगे।

अंत में, अंतिम उद्देश्य यह है कि आप अपने **API clients को serve** कर सकें, वह भी ऐसे तरीके से जो **सुरक्षित** हो, **disruptions से बचाए**, और **compute resources** (जैसे remote servers/virtual machines) का यथासंभव कुशलता से उपयोग करे। 🚀

मैं यहाँ इन **अवधारणाओं** के बारे में थोड़ा और बताऊँगा, और उम्मीद है कि इससे आपको वह **intuition** मिलेगी जिसकी आपको अपनी API को बहुत अलग-अलग environments में deploy करने का निर्णय लेने के लिए आवश्यकता होगी, संभवतः ऐसे **future** environments में भी जो अभी मौजूद नहीं हैं।

इन अवधारणाओं पर विचार करके, आप **अपनी खुद की APIs** को deploy करने का सबसे अच्छा तरीका **evaluate और design** कर पाएँगे।

अगले chapters में, मैं आपको FastAPI applications deploy करने के लिए अधिक **ठोस recipes** दूँगा।

लेकिन अभी के लिए, आइए इन महत्वपूर्ण **conceptual ideas** को देखें। ये अवधारणाएँ किसी भी अन्य प्रकार की web API पर भी लागू होती हैं। 💡

## सुरक्षा - HTTPS { #security-https }

[HTTPS के बारे में पिछले chapter](https.md) में हमने सीखा कि HTTPS आपकी API के लिए encryption कैसे प्रदान करता है।

हमने यह भी देखा कि HTTPS सामान्यतः आपके application server से **external** एक component, एक **TLS Termination Proxy**, द्वारा प्रदान किया जाता है।

और **HTTPS certificates renew** करने का प्रभारी कुछ होना चाहिए, यह वही component हो सकता है या कुछ अलग भी हो सकता है।

### HTTPS के लिए उदाहरण Tools { #example-tools-for-https }

TLS Termination Proxy के रूप में आप जिन tools का उपयोग कर सकते हैं, उनमें से कुछ हैं:

* Traefik
    * Certificate renewals को अपने-आप संभालता है ✨
* Caddy
    * Certificate renewals को अपने-आप संभालता है ✨
* Nginx
    * Certificate renewals के लिए Certbot जैसे external component के साथ
* HAProxy
    * Certificate renewals के लिए Certbot जैसे external component के साथ
* Nginx जैसे Ingress Controller के साथ Kubernetes
    * Certificate renewals के लिए cert-manager जैसे external component के साथ
* Cloud provider द्वारा उनकी services के हिस्से के रूप में internally संभाला गया (नीचे पढ़ें 👇)

एक और विकल्प यह है कि आप एक **cloud service** का उपयोग कर सकते हैं जो HTTPS setup करने सहित अधिक काम करती है। इसमें कुछ restrictions हो सकती हैं या आपसे अधिक charge लिया जा सकता है, आदि। लेकिन उस स्थिति में, आपको स्वयं TLS Termination Proxy setup नहीं करना पड़ेगा।

अगले chapters में मैं आपको कुछ ठोस उदाहरण दिखाऊँगा।

---

फिर विचार करने के लिए अगले concepts उस program के बारे में हैं जो आपकी वास्तविक API चला रहा है (जैसे Uvicorn)।

## Program और Process { #program-and-process }

हम चल रहे "**process**" के बारे में बहुत बात करेंगे, इसलिए यह स्पष्ट होना उपयोगी है कि इसका क्या अर्थ है, और "**program**" शब्द से इसका क्या अंतर है।

### Program क्या है { #what-is-a-program }

**Program** शब्द का उपयोग आम तौर पर कई चीजों का वर्णन करने के लिए किया जाता है:

* वह **code** जो आप लिखते हैं, **Python files**।
* वह **file** जिसे operating system द्वारा **execute** किया जा सकता है, उदाहरण के लिए: `python`, `python.exe` या `uvicorn`।
* कोई विशेष program जब वह operating system पर **चल रहा** हो, CPU का उपयोग कर रहा हो, और memory में चीजें store कर रहा हो। इसे **process** भी कहा जाता है।

### Process क्या है { #what-is-a-process }

**Process** शब्द सामान्यतः अधिक विशिष्ट तरीके से उपयोग किया जाता है, केवल उस चीज़ के लिए जो operating system में चल रही होती है (जैसे ऊपर के अंतिम point में):

* कोई विशेष program जब वह operating system पर **चल रहा** हो।
    * यह न तो file को refer करता है, न code को, यह **विशेष रूप से** उस चीज़ को refer करता है जिसे operating system द्वारा **execute** और manage किया जा रहा है।
* कोई भी program, कोई भी code, **केवल तभी कुछ कर सकता है** जब उसे **execute** किया जा रहा हो। यानी, जब कोई **process चल रहा** हो।
* Process को आपके द्वारा, या operating system द्वारा **terminate** (या "kill") किया जा सकता है। उस point पर, वह चलना/execute होना बंद कर देता है, और वह **अब कुछ नहीं कर सकता**।
* आपके computer पर चल रही प्रत्येक application के पीछे कोई process होता है, प्रत्येक running program, प्रत्येक window, आदि। और computer चालू होने पर सामान्यतः कई processes **एक ही समय में** चल रहे होते हैं।
* **एक ही program** के **multiple processes** एक ही समय में चल सकते हैं।

यदि आप अपने operating system में "task manager" या "system monitor" (या समान tools) देखते हैं, तो आप उनमें से कई processes चलते हुए देख पाएँगे।

और, उदाहरण के लिए, आप शायद देखेंगे कि एक ही browser program (Firefox, Chrome, Edge, आदि) को चलाने वाले multiple processes हैं। वे सामान्यतः प्रति tab एक process चलाते हैं, साथ में कुछ अन्य extra processes भी।

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

अब जब हम **process** और **program** शब्दों के बीच अंतर जानते हैं, तो deployments के बारे में बात जारी रखते हैं।

## startup पर चलना { #running-on-startup }

अधिकांश मामलों में, जब आप एक web API बनाते हैं, तो आप चाहते हैं कि वह **हमेशा चलती रहे**, बिना interruption के, ताकि आपके clients हमेशा उसे access कर सकें। यह निश्चित रूप से तब तक है जब तक आपके पास कोई विशेष कारण न हो कि आप उसे केवल कुछ स्थितियों में ही चलाना चाहते हैं, लेकिन अधिकांश समय आप चाहते हैं कि वह लगातार चलती रहे और **available** रहे।

### Remote Server में { #in-a-remote-server }

जब आप एक remote server (एक cloud server, एक virtual machine, आदि) setup करते हैं, तो सबसे सरल चीज़ जो आप कर सकते हैं वह है `fastapi run` (जो Uvicorn का उपयोग करता है) या कुछ समान, manually, ठीक उसी तरह जैसे आप local development करते समय करते हैं।

और यह काम करेगा और **development के दौरान** उपयोगी होगा।

लेकिन यदि server से आपका connection खो जाता है, तो **running process** शायद मर जाएगा।

और यदि server restart होता है (उदाहरण के लिए updates के बाद, या cloud provider से migrations के बाद) तो आप शायद **इसे notice नहीं करेंगे**। और इसके कारण, आपको यह भी पता नहीं चलेगा कि आपको process को manually restart करना है। इसलिए, आपकी API बस dead ही रहेगी। 😱

### Startup पर Automatically चलाना { #run-automatically-on-startup }

सामान्यतः, आप शायद चाहेंगे कि server program (जैसे Uvicorn) server startup पर automatically start हो, और किसी **human intervention** की आवश्यकता के बिना, ताकि आपकी API के साथ हमेशा एक process चल रहा हो (जैसे Uvicorn आपकी FastAPI app चला रहा हो)।

### अलग Program { #separate-program }

इसे हासिल करने के लिए, आपके पास सामान्यतः एक **अलग program** होगा जो सुनिश्चित करेगा कि आपकी application startup पर चले। और कई मामलों में, यह यह भी सुनिश्चित करेगा कि अन्य components या applications भी चलें, उदाहरण के लिए, एक database।

### Startup पर चलाने के लिए उदाहरण Tools { #example-tools-to-run-at-startup }

इस काम को करने वाले tools के कुछ उदाहरण हैं:

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* Cloud provider द्वारा उनकी services के हिस्से के रूप में internally संभाला गया
* अन्य...

अगले chapters में मैं आपको अधिक ठोस उदाहरण दूँगा।

## Restarts { #restarts }

यह सुनिश्चित करने जैसा कि आपकी application startup पर चले, आप शायद यह भी सुनिश्चित करना चाहेंगे कि failures के बाद उसे **restart** किया जाए।

### हम गलतियाँ करते हैं { #we-make-mistakes }

हम, मनुष्य के रूप में, हर समय **गलतियाँ** करते हैं। Software में लगभग *हमेशा* अलग-अलग जगहों पर **bugs** छिपे होते हैं। 🐛

और हम developers उन bugs को खोजते हुए और नई features implement करते हुए code को बेहतर बनाते रहते हैं (संभवतः नए bugs भी जोड़ते हुए 😅)।

### छोटे Errors Automatically संभाले जाते हैं { #small-errors-automatically-handled }

FastAPI के साथ web APIs बनाते समय, यदि हमारे code में कोई error है, तो FastAPI सामान्यतः उसे उस single request तक सीमित रखेगा जिसने error trigger किया। 🛡

Client को उस request के लिए **500 Internal Server Error** मिलेगा, लेकिन application पूरी तरह crash होने के बजाय अगली requests के लिए काम करती रहेगी।

### बड़े Errors - Crashes { #bigger-errors-crashes }

फिर भी, ऐसे मामले हो सकते हैं जहाँ हम कुछ code लिखते हैं जो **पूरी application को crash** कर देता है, जिससे Uvicorn और Python crash हो जाते हैं। 💥

और फिर भी, आप शायद नहीं चाहेंगे कि application केवल इसलिए dead रहे क्योंकि एक जगह error था, आप शायद चाहेंगे कि वह कम से कम उन *path operations* के लिए **चलती रहे** जो broken नहीं हैं।

### Crash के बाद Restart { #restart-after-crash }

लेकिन उन मामलों में जहाँ वास्तव में खराब errors running **process** को crash कर देते हैं, आप चाहेंगे कि एक external component process को **restart** करने का प्रभारी हो, कम से कम कुछ बार...

/// tip | सुझाव

...हालाँकि यदि पूरी application बस **तुरंत crash** हो रही है तो शायद उसे हमेशा restart करते रहने का कोई अर्थ नहीं है। लेकिन ऐसे मामलों में, आप शायद इसे development के दौरान, या कम से कम deployment के ठीक बाद notice करेंगे।

तो आइए मुख्य मामलों पर focus करें, जहाँ यह **future** में कुछ विशेष मामलों में पूरी तरह crash हो सकती है, और फिर भी उसे restart करना समझ में आता है।

///

आप शायद चाहेंगे कि आपकी application को restart करने का प्रभारी एक **external component** हो, क्योंकि उस point तक, Uvicorn और Python वाली वही application पहले ही crash हो चुकी होती है, इसलिए उसी app के उसी code में ऐसा कुछ नहीं होता जो इसके बारे में कुछ कर सके।

### Automatically Restart करने के लिए उदाहरण Tools { #example-tools-to-restart-automatically }

अधिकांश मामलों में, वही tool जो **startup पर program चलाने** के लिए उपयोग होता है, automatic **restarts** संभालने के लिए भी उपयोग होता है।

उदाहरण के लिए, इसे ये संभाल सकते हैं:

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* Cloud provider द्वारा उनकी services के हिस्से के रूप में internally संभाला गया
* अन्य...

## Replication - Processes और Memory { #replication-processes-and-memory }

FastAPI application के साथ, Uvicorn चलाने वाले `fastapi` command जैसे server program का उपयोग करते हुए, उसे **एक process** में एक बार चलाना multiple clients को concurrently serve कर सकता है।

लेकिन कई मामलों में, आप एक ही समय में कई worker processes चलाना चाहेंगे।

### Multiple Processes - Workers { #multiple-processes-workers }

यदि आपके पास single process द्वारा handle किए जा सकने से अधिक clients हैं (उदाहरण के लिए यदि virtual machine बहुत बड़ी नहीं है) और server के CPU में **multiple cores** हैं, तो आप एक ही application के साथ **multiple processes** एक ही समय में चला सकते हैं, और सभी requests को उनके बीच distribute कर सकते हैं।

जब आप उसी API program के **multiple processes** चलाते हैं, तो उन्हें आम तौर पर **workers** कहा जाता है।

### Worker Processes और Ports { #worker-processes-and-ports }

Docs [About HTTPS](https.md) से याद करें कि server में port और IP address के एक combination पर केवल एक process listen कर सकता है?

यह अभी भी सही है।

इसलिए, एक ही समय में **multiple processes** रखने में सक्षम होने के लिए, एक **single process port पर listening** होना चाहिए जो फिर communication को किसी तरीके से प्रत्येक worker process तक transmit करे।

### प्रति Process Memory { #memory-per-process }

अब, जब program memory में चीजें load करता है, उदाहरण के लिए, किसी variable में machine learning model, या किसी बड़े file की contents किसी variable में, तो वह सब server की **memory (RAM) का थोड़ा हिस्सा consume** करता है।

और multiple processes सामान्यतः **कोई memory share नहीं करते**। इसका मतलब है कि प्रत्येक running process की अपनी चीजें, variables, और memory होती है। और यदि आप अपने code में बड़ी मात्रा में memory consume कर रहे हैं, तो **प्रत्येक process** उतनी ही memory consume करेगा।

### Server Memory { #server-memory }

उदाहरण के लिए, यदि आपका code **1 GB size** वाला Machine Learning model load करता है, तो जब आप अपनी API के साथ एक process चलाते हैं, तो वह कम से कम 1 GB RAM consume करेगा। और यदि आप **4 processes** (4 workers) start करते हैं, तो प्रत्येक 1 GB RAM consume करेगा। इसलिए कुल मिलाकर, आपकी API **4 GB RAM** consume करेगी।

और यदि आपके remote server या virtual machine में केवल 3 GB RAM है, तो 4 GB से अधिक RAM load करने की कोशिश problems पैदा करेगी। 🚨

### Multiple Processes - एक उदाहरण { #multiple-processes-an-example }

इस उदाहरण में, एक **Manager Process** है जो दो **Worker Processes** start और control करता है।

यह Manager Process शायद IP में **port** पर listen करने वाला होगा। और यह सभी communication को worker processes तक transmit करेगा।

वे worker processes वे होंगे जो आपकी application चला रहे होंगे, वे **request** प्राप्त करने और **response** return करने के लिए मुख्य computations करेंगे, और वे RAM में variables में डाली गई कोई भी चीज़ load करेंगे।

<img src="/img/deployment/concepts/process-ram.drawio.svg">

और निश्चित रूप से, उसी machine पर आपकी application के अलावा शायद **अन्य processes** भी चल रहे होंगे।

एक दिलचस्प detail यह है कि प्रत्येक process द्वारा **उपयोग किए गए CPU** का percentage समय के साथ बहुत **बदल** सकता है, लेकिन **memory (RAM)** सामान्यतः कम या ज्यादा **stable** रहती है।

यदि आपके पास एक API है जो हर बार comparable amount की computations करती है और आपके पास बहुत सारे clients हैं, तो **CPU utilization** शायद *stable भी रहेगा* (लगातार तेजी से ऊपर-नीचे जाने के बजाय)।

### Replication Tools और Strategies के उदाहरण { #examples-of-replication-tools-and-strategies }

इसे हासिल करने के कई approaches हो सकते हैं, और मैं अगले chapters में specific strategies के बारे में अधिक बताऊँगा, उदाहरण के लिए Docker और containers के बारे में बात करते समय।

विचार करने की मुख्य constraint यह है कि **public IP** में **port** को handle करने वाला एक **single** component होना चाहिए। और फिर उसके पास replicated **processes/workers** तक communication **transmit** करने का कोई तरीका होना चाहिए।

यहाँ कुछ संभावित combinations और strategies हैं:

* **Uvicorn** `--workers` के साथ
    * एक Uvicorn **process manager** **IP** और **port** पर listen करेगा, और यह **multiple Uvicorn worker processes** start करेगा।
* **Kubernetes** और अन्य distributed **container systems**
    * **Kubernetes** layer में कुछ **IP** और **port** पर listen करेगा। Replication **multiple containers** रखने से होगी, प्रत्येक में **एक Uvicorn process** चल रहा होगा।
* **Cloud services** जो यह आपके लिए संभालती हैं
    * Cloud service शायद **आपके लिए replication handle** करेगी। यह संभवतः आपको **चलाने के लिए process**, या उपयोग करने के लिए **container image** define करने देगी, किसी भी स्थिति में, यह बहुत संभवतः **एक single Uvicorn process** होगा, और cloud service उसे replicate करने की प्रभारी होगी।

/// tip | सुझाव

यदि **containers**, Docker, या Kubernetes के बारे में इनमें से कुछ items अभी अधिक समझ में नहीं आते हैं तो चिंता न करें।

मैं future chapter में container images, Docker, Kubernetes, आदि के बारे में अधिक बताऊँगा: [Containers में FastAPI - Docker](docker.md)।

///

## शुरू करने से पहले के पिछले Steps { #previous-steps-before-starting }

कई मामले ऐसे होते हैं जहाँ आप अपनी application **start करने से पहले** कुछ steps perform करना चाहते हैं।

उदाहरण के लिए, आप **database migrations** चलाना चाह सकते हैं।

लेकिन अधिकांश मामलों में, आप इन steps को केवल **एक बार** perform करना चाहेंगे।

इसलिए, आप application start करने से पहले उन **previous steps** को perform करने के लिए एक **single process** रखना चाहेंगे।

और आपको यह सुनिश्चित करना होगा कि उन previous steps को चलाने वाला एक ही process हो, *भले ही* बाद में आप application के लिए **multiple processes** (multiple workers) start करें। यदि वे steps **multiple processes** द्वारा चलाए गए, तो वे उन्हें **parallel** में चलाकर काम को **duplicate** कर देंगे, और यदि steps database migration जैसी delicate चीज़ हैं, तो वे एक-दूसरे के साथ conflicts पैदा कर सकते हैं।

बेशक, कुछ मामले ऐसे होते हैं जहाँ previous steps को multiple times चलाने में कोई समस्या नहीं होती, उस स्थिति में इसे handle करना बहुत आसान होता है।

/// tip | सुझाव

साथ ही, ध्यान रखें कि आपके setup पर निर्भर करते हुए, कुछ मामलों में आपकी application start करने से पहले आपको **शायद किसी previous steps की आवश्यकता भी न हो**।

उस स्थिति में, आपको इनमें से किसी भी चीज़ की चिंता नहीं करनी होगी। 🤷

///

### Previous Steps Strategies के उदाहरण { #examples-of-previous-steps-strategies }

यह इस बात पर **बहुत अधिक निर्भर** करेगा कि आप **अपना system कैसे deploy** करते हैं, और यह शायद programs start करने, restarts handle करने, आदि के तरीके से जुड़ा होगा।

यहाँ कुछ संभावित ideas हैं:

* Kubernetes में एक "Init Container" जो आपके app container से पहले चलता है
* एक bash script जो previous steps चलाती है और फिर आपकी application start करती है
    * आपको फिर भी *उस* bash script को start/restart करने, errors detect करने, आदि का तरीका चाहिए होगा।

/// tip | सुझाव

Containers के साथ ऐसा करने के लिए मैं future chapter में अधिक ठोस उदाहरण दूँगा: [Containers में FastAPI - Docker](docker.md)।

///

## Resource Utilization { #resource-utilization }

आपके server(s) एक **resource** हैं, जिन्हें आप अपने programs के साथ consume या **utilize** कर सकते हैं, CPUs पर computation time और उपलब्ध RAM memory का उपयोग करके।

आप system resources का कितना हिस्सा consume/utilize करना चाहते हैं? "बहुत ज्यादा नहीं" सोचना आसान हो सकता है, लेकिन वास्तव में, आप शायद **crash किए बिना जितना संभव हो उतना** consume करना चाहेंगे।

यदि आप 3 servers के लिए भुगतान कर रहे हैं लेकिन उनकी RAM और CPU का केवल थोड़ा सा उपयोग कर रहे हैं, तो आप शायद **पैसा बर्बाद कर रहे हैं** 💸, और शायद **server की electric power बर्बाद कर रहे हैं** 🌎, आदि।

उस स्थिति में, केवल 2 servers रखना और उनके resources (CPU, memory, disk, network bandwidth, आदि) का उच्च percentage उपयोग करना बेहतर हो सकता है।

दूसरी ओर, यदि आपके पास 2 servers हैं और आप उनके **CPU और RAM का 100%** उपयोग कर रहे हैं, तो किसी point पर एक process अधिक memory माँगेगा, और server को disk को "memory" के रूप में उपयोग करना पड़ेगा (जो हजारों गुना धीमा हो सकता है), या वह **crash** भी हो सकता है। या किसी process को कुछ computation करनी हो सकती है और उसे CPU के फिर से free होने तक wait करना पड़ेगा।

इस मामले में, **एक extra server** लेना और उस पर कुछ processes चलाना बेहतर होगा ताकि उन सभी के पास **पर्याप्त RAM और CPU time** हो।

यह भी संभावना है कि किसी कारण से आपकी API के usage में **spike** हो। शायद यह viral हो गई, या शायद कुछ अन्य services या bots इसका उपयोग शुरू कर दें। और आप उन मामलों में safe रहने के लिए extra resources रखना चाह सकते हैं।

आप target करने के लिए एक **arbitrary number** रख सकते हैं, उदाहरण के लिए, resource utilization का **50% से 90% के बीच** कुछ। बात यह है कि ये शायद वे मुख्य चीजें हैं जिन्हें आप measure करना और अपने deployments tweak करने के लिए उपयोग करना चाहेंगे।

आप अपने server में उपयोग किए गए CPU और RAM या प्रत्येक process द्वारा उपयोग की गई मात्रा देखने के लिए `htop` जैसे simple tools का उपयोग कर सकते हैं। या आप अधिक complex monitoring tools का उपयोग कर सकते हैं, जो servers में distributed हो सकते हैं, आदि।

## Recap { #recap }

आपने यहाँ कुछ मुख्य अवधारणाएँ पढ़ी हैं जिन्हें अपनी application को कैसे deploy करना है, यह तय करते समय आपको शायद ध्यान में रखना होगा:

* सुरक्षा - HTTPS
* startup पर चलना
* Restarts
* Replication (चल रहे processes की संख्या)
* Memory
* शुरू करने से पहले के पिछले steps

इन ideas को समझना और उन्हें apply करना आपको अपने deployments configure और tweak करते समय कोई भी decisions लेने के लिए आवश्यक intuition देना चाहिए। 🤓

अगले sections में, मैं आपको उन संभावित strategies के अधिक ठोस उदाहरण दूँगा जिनका आप पालन कर सकते हैं। 🚀
