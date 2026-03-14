# HTTPS کے بارے میں { #about-https }

یہ سوچنا آسان ہے کہ HTTPS کوئی ایسی چیز ہے جو بس "فعال" ہوتی ہے یا نہیں ہوتی۔

لیکن یہ اس سے کہیں زیادہ پیچیدہ ہے۔

/// tip | مشورہ

اگر آپ جلدی میں ہیں یا آپ کو پرواہ نہیں ہے، تو مختلف تکنیکوں کے ساتھ سب کچھ ترتیب دینے کی مرحلہ وار ہدایات کے لیے اگلے حصوں میں جائیں۔

///

**HTTPS کی بنیادی باتیں** جاننے کے لیے، ایک صارف کے نقطہ نظر سے، دیکھیں [https://howhttps.works/](https://howhttps.works/)۔

اب، ایک **developer کے نقطہ نظر** سے، HTTPS کے بارے میں سوچتے وقت ذہن میں رکھنے کی کئی چیزیں ہیں:

* HTTPS کے لیے، **server** کو ایک **تیسری جماعت** کی طرف سے تیار کردہ **"certificates"** رکھنے کی ضرورت ہے۔
    * وہ certificates دراصل تیسری جماعت سے **حاصل** کیے جاتے ہیں، "تیار" نہیں کیے جاتے۔
* Certificates کی ایک **مدت** ہوتی ہے۔
    * وہ **ختم** ہو جاتے ہیں۔
    * اور پھر انہیں **تجدید** کرنے، تیسری جماعت سے **دوبارہ حاصل** کرنے کی ضرورت ہوتی ہے۔
* کنکشن کی encryption **TCP سطح** پر ہوتی ہے۔
    * یہ **HTTP سے نیچے** ایک پرت ہے۔
    * تو، **certificate اور encryption** کی سنبھال **HTTP سے پہلے** ہوتی ہے۔
* **TCP کو "domains" کے بارے میں معلوم نہیں ہوتا**۔ صرف IP ایڈریسز کے بارے میں۔
    * درخواست کیے گئے **مخصوص domain** کی معلومات **HTTP ڈیٹا** میں جاتی ہے۔
* **HTTPS certificates** ایک **مخصوص domain** کی **تصدیق** کرتے ہیں، لیکن protocol اور encryption TCP سطح پر ہوتی ہے، یہ **جاننے سے پہلے** کہ کس domain سے معاملہ ہو رہا ہے۔
* **بطور ڈیفالٹ**، اس کا مطلب یہ ہوگا کہ آپ کے پاس **ہر IP ایڈریس پر صرف ایک HTTPS certificate** ہو سکتا ہے۔
    * اس سے قطع نظر کہ آپ کا server کتنا بڑا ہے یا اس پر موجود ہر ایپلیکیشن کتنی چھوٹی ہے۔
    * تاہم، اس کا ایک **حل** موجود ہے۔
* **TLS** protocol (جو TCP سطح پر، HTTP سے پہلے encryption سنبھالتا ہے) کی ایک **توسیع** ہے جسے **[<abbr title="Server Name Indication">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)** کہتے ہیں۔
    * یہ SNI توسیع ایک واحد server (ایک **واحد IP ایڈریس** کے ساتھ) کو **کئی HTTPS certificates** رکھنے اور **متعدد HTTPS domains/ایپلیکیشنز** کو خدمت فراہم کرنے کی اجازت دیتی ہے۔
    * اس کے کام کرنے کے لیے، server پر چلنے والے ایک **واحد** جزو (پروگرام) کو، جو **عوامی IP ایڈریس** پر سن رہا ہو، server کے **تمام HTTPS certificates** رکھنے ہوں گے۔
* محفوظ کنکشن حاصل کرنے **کے بعد**، مواصلاتی protocol **ابھی بھی HTTP** ہے۔
    * مواد **encrypted** ہوتے ہیں، اگرچہ وہ **HTTP protocol** کے ساتھ بھیجے جا رہے ہوتے ہیں۔

ایک عام طریقہ یہ ہے کہ server (مشین، host وغیرہ) پر **ایک پروگرام/HTTP server** چلایا جائے جو **تمام HTTPS حصوں کا انتظام** کرے: **encrypted HTTPS requests** وصول کرے، **decrypted HTTP requests** اسی server میں چلنے والی اصل HTTP ایپلیکیشن (اس معاملے میں **FastAPI** ایپلیکیشن) کو بھیجے، ایپلیکیشن سے **HTTP response** لے، مناسب **HTTPS certificate** استعمال کرتے ہوئے اسے **encrypt** کرے اور **HTTPS** استعمال کرتے ہوئے واپس صارف کو بھیجے۔ اس server کو اکثر **[TLS Termination Proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy)** کہا جاتا ہے۔

TLS Termination Proxy کے طور پر آپ جو اختیارات استعمال کر سکتے ہیں ان میں سے کچھ یہ ہیں:

* Traefik (جو certificate کی تجدید بھی سنبھال سکتا ہے)
* Caddy (جو certificate کی تجدید بھی سنبھال سکتا ہے)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Let's Encrypt سے پہلے، یہ **HTTPS certificates** قابل اعتماد تیسری جماعتوں کی طرف سے فروخت کیے جاتے تھے۔

ان میں سے ایک certificate حاصل کرنے کا عمل مشکل ہوتا تھا، کافی کاغذی کارروائی درکار ہوتی تھی اور certificates کافی مہنگے ہوتے تھے۔

لیکن پھر **[Let's Encrypt](https://letsencrypt.org/)** بنایا گیا۔

یہ Linux Foundation کا ایک منصوبہ ہے۔ یہ خود بخود طریقے سے **مفت HTTPS certificates** فراہم کرتا ہے۔ یہ certificates تمام معیاری خفیہ سیکیورٹی استعمال کرتے ہیں، اور مختصر مدتی (تقریباً 3 ماہ) ہوتے ہیں، تو اپنی کم مدت کی وجہ سے **سیکیورٹی دراصل بہتر** ہے۔

Domains محفوظ طریقے سے تصدیق شدہ ہوتے ہیں اور certificates خود بخود تیار ہوتے ہیں۔ اس سے ان certificates کی تجدید کو بھی خودکار بنانے کی اجازت ملتی ہے۔

خیال یہ ہے کہ ان certificates کے حصول اور تجدید کو خودکار بنایا جائے تاکہ آپ **محفوظ HTTPS، مفت، ہمیشہ کے لیے** حاصل کر سکیں۔

## Developers کے لیے HTTPS { #https-for-developers }

یہاں ایک مثال ہے کہ ایک HTTPS API کیسی نظر آ سکتی ہے، مرحلہ وار، بنیادی طور پر developers کے لیے اہم خیالات پر توجہ دیتے ہوئے۔

### Domain Name { #domain-name }

یہ سب شاید آپ کے کوئی **domain name حاصل** کرنے سے شروع ہوگا۔ پھر، آپ اسے DNS server میں ترتیب دیں گے (ممکنہ طور پر آپ کا وہی cloud provider)۔

آپ کو شاید ایک cloud server (virtual machine) یا کچھ ایسا ہی ملے گا، اور اس کا ایک <dfn title="Doesn't change over time. Not dynamic.">مقررہ</dfn> **عوامی IP ایڈریس** ہوگا۔

DNS server(s) میں آپ ایک ریکارڈ (ایک "`A record`") ترتیب دیں گے تاکہ **آپ کا domain** آپ کے **server کے عوامی IP ایڈریس** کی طرف اشارہ کرے۔

آپ شاید یہ صرف ایک بار کریں گے، پہلی بار، جب سب کچھ ترتیب دے رہے ہوں۔

/// tip | مشورہ

یہ Domain Name کا حصہ HTTPS سے بہت پہلے ہے، لیکن چونکہ سب کچھ domain اور IP ایڈریس پر منحصر ہے، اس لیے اس کا یہاں ذکر کرنا مناسب ہے۔

///

### DNS { #dns }

اب آئیے تمام اصل HTTPS حصوں پر توجہ مرکوز کریں۔

سب سے پہلے، browser **DNS servers** سے چیک کرے گا کہ **domain کا IP** کیا ہے، اس معاملے میں، `someapp.example.com`۔

DNS servers browser کو کوئی مخصوص **IP ایڈریس** بتائیں گے۔ یہ آپ کے server کا وہ عوامی IP ایڈریس ہوگا جو آپ نے DNS servers میں ترتیب دیا تھا۔

<img src="/img/deployment/https/https01.drawio.svg">

### TLS Handshake کا آغاز { #tls-handshake-start }

browser پھر اس IP ایڈریس سے **port 443** (HTTPS port) پر مواصلت کرے گا۔

مواصلت کا پہلا حصہ صرف client اور server کے درمیان کنکشن قائم کرنا اور خفیہ keys وغیرہ کا فیصلہ کرنا ہے۔

<img src="/img/deployment/https/https02.drawio.svg">

TLS کنکشن قائم کرنے کے لیے client اور server کے درمیان اس تعامل کو **TLS handshake** کہا جاتا ہے۔

### SNI توسیع کے ساتھ TLS { #tls-with-sni-extension }

server میں ایک مخصوص **IP ایڈریس** کے مخصوص **port** پر صرف **ایک process** سن سکتا ہے۔ اسی IP ایڈریس پر دوسرے ports پر دوسرے processes سن سکتے ہیں، لیکن ہر IP ایڈریس اور port کے مجموعے کے لیے صرف ایک۔

TLS (HTTPS) بطور ڈیفالٹ مخصوص port `443` استعمال کرتا ہے۔ تو ہمیں اسی port کی ضرورت ہوگی۔

چونکہ اس port پر صرف ایک process سن سکتا ہے، وہ process جو یہ کرے گا وہ **TLS Termination Proxy** ہوگا۔

TLS Termination Proxy کے پاس ایک یا زیادہ **TLS certificates** (HTTPS certificates) تک رسائی ہوگی۔

اوپر بحث کی گئی **SNI توسیع** کا استعمال کرتے ہوئے، TLS Termination Proxy چیک کرے گا کہ دستیاب TLS (HTTPS) certificates میں سے اسے اس کنکشن کے لیے کون سا استعمال کرنا چاہیے، وہ جو client کی متوقع domain سے مماثل ہو۔

اس معاملے میں، یہ `someapp.example.com` کا certificate استعمال کرے گا۔

<img src="/img/deployment/https/https03.drawio.svg">

client پہلے سے اس ادارے پر **اعتماد** کرتا ہے جس نے وہ TLS certificate تیار کیا (اس معاملے میں Let's Encrypt، لیکن ہم اس کے بارے میں بعد میں بات کریں گے)، تو یہ **تصدیق** کر سکتا ہے کہ certificate درست ہے۔

پھر، certificate کا استعمال کرتے ہوئے، client اور TLS Termination Proxy باقی **TCP مواصلت کو encrypt کرنے کا طریقہ فیصلہ** کرتے ہیں۔ اس سے **TLS Handshake** کا حصہ مکمل ہو جاتا ہے۔

اس کے بعد، client اور server کے پاس ایک **encrypted TCP کنکشن** ہوتا ہے، یہی وہ چیز ہے جو TLS فراہم کرتا ہے۔ اور پھر وہ اس کنکشن کو اصل **HTTP مواصلت** شروع کرنے کے لیے استعمال کر سکتے ہیں۔

اور **HTTPS** یہی ہے، یہ بس سادہ **HTTP** ایک **محفوظ TLS کنکشن** کے اندر ہے خالص (غیر encrypted) TCP کنکشن کے بجائے۔

/// tip | مشورہ

غور کریں کہ مواصلت کی encryption **TCP سطح** پر ہوتی ہے، HTTP سطح پر نہیں۔

///

### HTTPS Request { #https-request }

اب جب client اور server (خاص طور پر browser اور TLS Termination Proxy) کے پاس ایک **encrypted TCP کنکشن** ہے، تو وہ **HTTP مواصلت** شروع کر سکتے ہیں۔

تو، client ایک **HTTPS request** بھیجتا ہے۔ یہ بس ایک encrypted TLS کنکشن کے ذریعے HTTP request ہے۔

<img src="/img/deployment/https/https04.drawio.svg">

### Request کو Decrypt کرنا { #decrypt-the-request }

TLS Termination Proxy طے شدہ encryption کا استعمال کرتے ہوئے **request کو decrypt** کرے گا، اور **سادہ (decrypted) HTTP request** ایپلیکیشن چلانے والے process (مثلاً FastAPI ایپلیکیشن چلانے والے Uvicorn کے ساتھ ایک process) کو منتقل کرے گا۔

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP Response { #http-response }

ایپلیکیشن request پر عمل کرے گی اور TLS Termination Proxy کو ایک **سادہ (غیر encrypted) HTTP response** بھیجے گی۔

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS Response { #https-response }

TLS Termination Proxy پھر پہلے سے طے شدہ خفیہ نگاری (جو `someapp.example.com` کے certificate سے شروع ہوئی تھی) کا استعمال کرتے ہوئے **response کو encrypt** کرے گا، اور اسے واپس browser کو بھیجے گا۔

اس کے بعد، browser تصدیق کرے گا کہ response درست ہے اور صحیح خفیہ key سے encrypted ہے، وغیرہ۔ پھر یہ **response کو decrypt** کرے گا اور اس پر عمل کرے گا۔

<img src="/img/deployment/https/https07.drawio.svg">

client (browser) جانے گا کہ response صحیح server سے آیا ہے کیونکہ یہ وہ خفیہ نگاری استعمال کر رہا ہے جس پر انہوں نے پہلے **HTTPS certificate** استعمال کرتے ہوئے اتفاق کیا تھا۔

### متعدد ایپلیکیشنز { #multiple-applications }

اسی server (یا servers) میں، **متعدد ایپلیکیشنز** ہو سکتی ہیں، مثلاً دوسرے API پروگرامز یا ڈیٹابیس۔

مخصوص IP اور port (ہماری مثال میں TLS Termination Proxy) صرف ایک process سنبھال سکتا ہے لیکن دوسری ایپلیکیشنز/processes بھی server(s) پر چل سکتی ہیں، جب تک کہ وہ **عوامی IP اور port کا وہی مجموعہ** استعمال کرنے کی کوشش نہ کریں۔

<img src="/img/deployment/https/https08.drawio.svg">

اس طرح، TLS Termination Proxy **متعدد domains** کے لیے، متعدد ایپلیکیشنز کے لیے HTTPS اور certificates سنبھال سکتا ہے، اور پھر ہر معاملے میں requests صحیح ایپلیکیشن کو منتقل کر سکتا ہے۔

### Certificate کی تجدید { #certificate-renewal }

مستقبل میں کسی وقت، ہر certificate **ختم** ہو جائے گا (حاصل کرنے کے تقریباً 3 ماہ بعد)۔

اور پھر، ایک اور پروگرام ہوگا (بعض اوقات یہ ایک اور پروگرام ہوتا ہے، بعض اوقات یہ وہی TLS Termination Proxy ہو سکتا ہے) جو Let's Encrypt سے بات کرے گا، اور certificate(s) کی تجدید کرے گا۔

<img src="/img/deployment/https/https.drawio.svg">

**TLS certificates** ایک **domain name سے منسلک** ہوتے ہیں، IP ایڈریس سے نہیں۔

تو، certificates کی تجدید کے لیے، تجدیدی پروگرام کو اتھارٹی (Let's Encrypt) کو **ثابت** کرنا ہوگا کہ یہ واقعی اس domain کا **"مالک" ہے اور اسے کنٹرول** کرتا ہے۔

ایسا کرنے کے لیے، اور مختلف ایپلیکیشن کی ضروریات کو پورا کرنے کے لیے، یہ کئی طریقوں سے کر سکتا ہے۔ کچھ مقبول طریقے یہ ہیں:

* **کچھ DNS records میں ترمیم**۔
    * اس کے لیے، تجدیدی پروگرام کو DNS provider کی APIs کی حمایت کرنی ہوگی، تو، آپ جو DNS provider استعمال کر رہے ہیں اس پر منحصر ہے، یہ اختیار ہو بھی سکتا ہے اور نہیں بھی۔
* domain سے منسلک عوامی IP ایڈریس پر **server کے طور پر چلنا** (کم از کم certificate حصول کے عمل کے دوران)۔
    * جیسا کہ ہم نے اوپر کہا، مخصوص IP اور port پر صرف ایک process سن سکتا ہے۔
    * یہ ان وجوہات میں سے ایک ہے جس کی وجہ سے یہ بہت مفید ہے جب وہی TLS Termination Proxy certificate کی تجدید کے عمل کا بھی خیال رکھے۔
    * ورنہ، آپ کو TLS Termination Proxy کو عارضی طور پر بند کرنا پڑ سکتا ہے، certificates حاصل کرنے کے لیے تجدیدی پروگرام شروع کرنا، پھر انہیں TLS Termination Proxy کے ساتھ ترتیب دینا، اور پھر TLS Termination Proxy کو دوبارہ شروع کرنا۔ یہ مثالی نہیں ہے، کیونکہ TLS Termination Proxy بند ہونے کے دوران آپ کی app(s) دستیاب نہیں ہوں گی۔

یہ سارا تجدید کا عمل، جبکہ ابھی بھی app کو خدمت فراہم کر رہے ہوں، ان اصل وجوہات میں سے ایک ہے جس کی وجہ سے آپ HTTPS سنبھالنے کے لیے TLS Termination Proxy کے ساتھ **الگ نظام** رکھنا چاہیں گے بجائے اس کے کہ TLS certificates کو براہ راست application server (مثلاً Uvicorn) کے ساتھ استعمال کریں۔

## Proxy Forwarded Headers { #proxy-forwarded-headers }

HTTPS سنبھالنے کے لیے proxy استعمال کرتے وقت، آپ کا **application server** (مثلاً FastAPI CLI کے ذریعے Uvicorn) HTTPS کے عمل کے بارے میں کچھ نہیں جانتا، یہ **TLS Termination Proxy** کے ساتھ سادہ HTTP میں مواصلت کرتا ہے۔

یہ **proxy** عام طور پر request کو **application server** کو منتقل کرنے سے پہلے فوری طور پر کچھ HTTP headers مقرر کرتا ہے، تاکہ application server کو بتائے کہ request proxy کے ذریعے **آگے بھیجی** جا رہی ہے۔

/// note | تکنیکی تفصیلات

proxy headers یہ ہیں:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

تاہم، چونکہ **application server** نہیں جانتا کہ یہ ایک قابل اعتماد **proxy** کے پیچھے ہے، بطور ڈیفالٹ، یہ ان headers پر اعتماد نہیں کرے گا۔

لیکن آپ **application server** کو ترتیب دے سکتے ہیں کہ وہ **proxy** کی طرف سے بھیجے گئے *forwarded* headers پر اعتماد کرے۔ اگر آپ FastAPI CLI استعمال کر رہے ہیں، تو آپ *CLI Option* `--forwarded-allow-ips` استعمال کر سکتے ہیں تاکہ اسے بتائیں کہ کن IPs سے آنے والے *forwarded* headers پر اعتماد کرنا ہے۔

مثال کے طور پر، اگر **application server** صرف قابل اعتماد **proxy** سے مواصلت وصول کر رہا ہے، تو آپ اسے `--forwarded-allow-ips="*"` پر سیٹ کر سکتے ہیں تاکہ یہ تمام آنے والی IPs پر اعتماد کرے، کیونکہ اسے صرف **proxy** کے IP سے requests ملیں گی۔

اس طرح ایپلیکیشن جان سکے گی کہ اس کا اپنا عوامی URL کیا ہے، آیا یہ HTTPS استعمال کر رہی ہے، domain، وغیرہ۔

یہ مثال کے طور پر redirects کو صحیح طریقے سے سنبھالنے کے لیے مفید ہوگا۔

/// tip | مشورہ

آپ اس کے بارے میں مزید [Behind a Proxy - Enable Proxy Forwarded Headers](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers) کی دستاویزات میں جان سکتے ہیں

///

## خلاصہ { #recap }

**HTTPS** ہونا بہت اہم ہے، اور زیادہ تر معاملات میں کافی **ضروری** ہے۔ بحیثیت developer HTTPS کے حوالے سے آپ کی زیادہ تر محنت بس **ان تصورات کو سمجھنے** اور یہ جاننے میں لگتی ہے کہ یہ کیسے کام کرتے ہیں۔

لیکن ایک بار جب آپ **developers کے لیے HTTPS** کی بنیادی معلومات جان لیں تو آپ آسانی سے مختلف ٹولز کو ملا اور ترتیب دے سکتے ہیں تاکہ سب کچھ آسان طریقے سے منظم ہو سکے۔

اگلے چند ابواب میں، میں آپ کو **FastAPI** ایپلیکیشنز کے لیے **HTTPS** ترتیب دینے کی کئی ٹھوس مثالیں دکھاؤں گا۔ 🔒
