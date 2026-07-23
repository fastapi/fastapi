# Containers में FastAPI - Docker { #fastapi-in-containers-docker }

FastAPI applications deploy करते समय एक आम तरीका **Linux container image** बनाना है। यह सामान्यतः [**Docker**](https://www.docker.com/) का उपयोग करके किया जाता है। फिर आप उस container image को कुछ संभावित तरीकों में से किसी एक में deploy कर सकते हैं।

Linux containers का उपयोग करने के कई लाभ हैं, जिनमें **security**, **replicability**, **simplicity**, और अन्य शामिल हैं।

/// tip | टिप

जल्दी में हैं और यह सब पहले से जानते हैं? नीचे दिए गए [`Dockerfile` पर जाएँ 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# यदि Nginx या Traefik जैसे proxy के पीछे चला रहे हैं तो --proxy-headers जोड़ें
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Container क्या है { #what-is-a-container }

Containers (मुख्य रूप से Linux containers) applications को उनकी सभी dependencies और आवश्यक files सहित package करने का एक बहुत **lightweight** तरीका हैं, जबकि उन्हें उसी system में दूसरे containers (दूसरी applications या components) से isolated रखा जाता है।

Linux containers host (machine, virtual machine, cloud server, आदि) के उसी Linux kernel का उपयोग करके चलते हैं। इसका मतलब बस इतना है कि वे बहुत lightweight होते हैं (पूरे operating system को emulate करने वाली full virtual machines की तुलना में)।

इस तरह, containers **कम resources** consume करते हैं, लगभग उतने ही जितने processes को सीधे चलाने में लगते हैं (virtual machine बहुत अधिक consume करेगी)।

Containers के अपने **isolated** running processes (आमतौर पर सिर्फ एक process), file system, और network भी होते हैं, जिससे deployment, security, development, आदि सरल हो जाते हैं।

## Container Image क्या है { #what-is-a-container-image }

एक **container** एक **container image** से चलाया जाता है।

Container image उन सभी files, environment variables, और default command/program का **static** version होता है जो container में मौजूद होना चाहिए। यहाँ **Static** का मतलब है कि container **image** चल नहीं रही है, execute नहीं हो रही है, यह सिर्फ packaged files और metadata है।

"**container image**" जो stored static contents है, उसके विपरीत, "**container**" सामान्यतः running instance को संदर्भित करता है, वह चीज़ जो **execute** हो रही है।

जब **container** start होकर running होता है (**container image** से start किया गया), तो यह files, environment variables, आदि बना या बदल सकता है। वे बदलाव केवल उस container में मौजूद होंगे, लेकिन underlying container image में persist नहीं होंगे (disk पर save नहीं होंगे)।

Container image की तुलना **program** file और contents से की जा सकती है, जैसे `python` और कोई file `main.py`।

और **container** स्वयं (**container image** के विपरीत) image का वास्तविक running instance है, जिसकी तुलना **process** से की जा सकती है। वास्तव में, container केवल तब running होता है जब उसमें **process running** हो (और आमतौर पर यह केवल एक single process होता है)। जब उसमें कोई process running नहीं रहता, तो container stop हो जाता है।

## Container Images { #container-images }

Docker **container images** और **containers** बनाने और manage करने के मुख्य tools में से एक रहा है।

और एक public [Docker Hub](https://hub.docker.com/) है जिसमें कई tools, environments, databases, और applications के लिए पहले से बनी **official container images** हैं।

उदाहरण के लिए, एक official [Python Image](https://hub.docker.com/_/python) है।

और databases जैसी अलग-अलग चीज़ों के लिए कई अन्य images हैं, उदाहरण के लिए:

* [PostgreSQL](https://hub.docker.com/_/postgres)
* [MySQL](https://hub.docker.com/_/mysql)
* [MongoDB](https://hub.docker.com/_/mongo)
* [Redis](https://hub.docker.com/_/redis), आदि।

पहले से बनी container image का उपयोग करके अलग-अलग tools को **combine** और use करना बहुत आसान है। उदाहरण के लिए, नया database try करने के लिए। अधिकतर मामलों में, आप **official images** का उपयोग कर सकते हैं, और उन्हें सिर्फ environment variables से configure कर सकते हैं।

इस तरह, कई मामलों में आप containers और Docker के बारे में सीख सकते हैं और उस knowledge को कई अलग-अलग tools और components के साथ reuse कर सकते हैं।

तो, आप अलग-अलग चीज़ों के साथ **multiple containers** चलाएँगे, जैसे database, Python application, React frontend application वाला web server, और उन्हें उनके internal network के माध्यम से connect करेंगे।

सभी container management systems (जैसे Docker या Kubernetes) में ये networking features integrated होते हैं।

## Containers और Processes { #containers-and-processes }

एक **container image** सामान्यतः अपने metadata में default program या command शामिल करती है जिसे **container** start होने पर run किया जाना चाहिए, और उस program को pass किए जाने वाले parameters। यह बहुत हद तक वैसा ही है जैसा command line में होता।

जब कोई **container** start होता है, तो वह उस command/program को run करेगा (हालाँकि आप इसे override करके कोई अलग command/program run करवा सकते हैं)।

Container तब तक running रहता है जब तक **main process** (command या program) running रहता है।

Container में सामान्यतः **single process** होता है, लेकिन main process से subprocesses start करना भी संभव है, और इस तरह उसी container में **multiple processes** हो सकते हैं।

लेकिन **कम से कम एक running process** के बिना running container होना संभव नहीं है। यदि main process stop हो जाता है, तो container stop हो जाता है।

## FastAPI के लिए Docker Image बनाएँ { #build-a-docker-image-for-fastapi }

ठीक है, अब कुछ बनाते हैं! 🚀

मैं आपको दिखाऊँगा कि **official Python** image पर आधारित FastAPI के लिए **scratch से** **Docker image** कैसे बनाएँ।

यह वही है जो आप **अधिकतर मामलों** में करना चाहेंगे, उदाहरण के लिए:

* **Kubernetes** या समान tools का उपयोग करते समय
* **Raspberry Pi** पर चलाते समय
* ऐसा cloud service उपयोग करते समय जो आपके लिए container image run करेगा, आदि।

### Package Requirements { #package-requirements }

आपकी application के लिए **package requirements** सामान्यतः किसी file में होंगे।

यह मुख्य रूप से उस tool पर निर्भर करेगा जिसका उपयोग आप उन requirements को **install** करने के लिए करते हैं।

इसे करने का सबसे आम तरीका है `requirements.txt` file रखना, जिसमें package names और उनके versions हों, प्रति line एक।

आप versions की ranges set करने के लिए निश्चित रूप से वही ideas उपयोग करेंगे जो आपने [FastAPI versions के बारे में](versions.md) में पढ़े हैं।

उदाहरण के लिए, आपका `requirements.txt` ऐसा दिख सकता है:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

और आप सामान्यतः उन package dependencies को `pip` से install करेंगे, उदाहरण के लिए:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// note | नोट

Package dependencies define और install करने के लिए अन्य formats और tools भी हैं।

///

### **FastAPI** Code बनाएँ { #create-the-fastapi-code }

* एक `app` directory बनाएँ और उसमें enter करें।
* एक खाली file `__init__.py` बनाएँ।
* एक `main.py` file बनाएँ जिसमें हो:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

अब उसी project directory में एक file `Dockerfile` बनाएँ जिसमें हो:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.14

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. Official Python base image से start करें।

2. Current working directory को `/code` पर set करें।

    यही वह जगह है जहाँ हम `requirements.txt` file और `app` directory रखेंगे।

3. Requirements वाली file को `/code` directory में copy करें।

    पहले **केवल** requirements वाली file copy करें, बाकी code नहीं।

    क्योंकि यह file **अक्सर change नहीं होती**, Docker इसे detect करेगा और इस step के लिए **cache** का उपयोग करेगा, जिससे अगले step के लिए भी cache enable हो जाएगा।

4. Requirements file में package dependencies install करें।

    `--no-cache-dir` option `pip` को बताता है कि downloaded packages को locally save न करे, क्योंकि यह केवल तब उपयोगी होता जब `pip` को उन्हीं packages को install करने के लिए फिर से run किया जाना हो, लेकिन containers के साथ काम करते समय ऐसा मामला नहीं है।

    /// note | नोट

    `--no-cache-dir` केवल `pip` से संबंधित है, इसका Docker या containers से कोई संबंध नहीं है।

    ///

    `--upgrade` option `pip` को बताता है कि यदि packages पहले से installed हैं तो उन्हें upgrade करे।

    क्योंकि पिछला step जिसमें file copy की गई थी **Docker cache** द्वारा detect किया जा सकता है, इसलिए यह step भी available होने पर **Docker cache का उपयोग** करेगा।

    इस step में cache का उपयोग development के दौरान image बार-बार build करते समय आपका बहुत **समय** **बचाएगा**, हर बार सभी dependencies को **download और install** करने के बजाय।

5. `./app` directory को `/code` directory के अंदर copy करें।

    क्योंकि इसमें सारा code है, और यही वह चीज़ है जो **सबसे अधिक बार change होती** है, Docker **cache** इस या किसी भी **आगे के steps** के लिए आसानी से उपयोग नहीं होगा।

    इसलिए, container image build times optimize करने के लिए इसे `Dockerfile` के **end के पास** रखना महत्वपूर्ण है।

6. **command** set करें ताकि `fastapi run` उपयोग हो, जो अंदर से Uvicorn का उपयोग करता है।

    `CMD` strings की list लेता है, इन strings में से प्रत्येक वही है जिसे आप command line में spaces से अलग करके type करेंगे।

    यह command **current working directory** से run होगा, वही `/code` directory जिसे आपने ऊपर `WORKDIR /code` से set किया है।

/// tip | टिप

Code में प्रत्येक number bubble पर click करके review करें कि हर line क्या करती है। 👆

///

/// warning | चेतावनी

नीचे समझाए अनुसार, `CMD` instruction का **exec form** **हमेशा** use करना सुनिश्चित करें।

///

#### `CMD` उपयोग करें - Exec Form { #use-cmd-exec-form }

[`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) Docker instruction दो forms में लिखा जा सकता है:

✅ **Exec** form:

```Dockerfile
# ✅ यह करें
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```Dockerfile
# ⛔️ यह न करें
CMD fastapi run app/main.py --port 80
```

यह सुनिश्चित करने के लिए कि FastAPI gracefully shutdown कर सके और [lifespan events](../advanced/events.md) trigger हों, हमेशा **exec** form use करें।

आप इसके बारे में [shell और exec form के लिए Docker docs](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form) में और पढ़ सकते हैं।

`docker compose` का उपयोग करते समय यह काफी noticeable हो सकता है। अधिक technical details के लिए यह Docker Compose FAQ section देखें: [मेरी services को recreate या stop होने में 10 seconds क्यों लगते हैं?](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop).

#### Directory Structure { #directory-structure }

अब आपके पास ऐसी directory structure होनी चाहिए:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### TLS Termination Proxy के पीछे { #behind-a-tls-termination-proxy }

यदि आप अपना container Nginx या Traefik जैसे TLS Termination Proxy (load balancer) के पीछे चला रहे हैं, तो option `--proxy-headers` जोड़ें, यह Uvicorn (FastAPI CLI के माध्यम से) को बताएगा कि उस proxy द्वारा भेजे गए headers पर trust करे, जो उसे बताता है कि application HTTPS के पीछे चल रही है, आदि।

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker Cache { #docker-cache }

इस `Dockerfile` में एक महत्वपूर्ण trick है, हम पहले **केवल dependencies वाली file** copy करते हैं, बाकी code नहीं। मैं आपको बताता हूँ क्यों।

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker और अन्य tools इन container images को **incrementally build** करते हैं, **एक layer के ऊपर दूसरी layer** जोड़ते हुए, `Dockerfile` के top से शुरू करके और `Dockerfile` के प्रत्येक instruction द्वारा बनाई गई कोई भी files जोड़ते हुए।

Docker और समान tools image build करते समय **internal cache** भी use करते हैं, यदि कोई file पिछली बार container image build करने के बाद से change नहीं हुई है, तो वह file को फिर से copy करने और scratch से नई layer बनाने के बजाय पिछली बार बनाई गई **उसी layer को reuse** करेगा।

सिर्फ files copy करने से बचना जरूरी नहीं कि चीज़ों को बहुत बेहतर कर दे, लेकिन क्योंकि उसने उस step के लिए cache use किया, वह **अगले step के लिए cache use** कर सकता है। उदाहरण के लिए, वह उस instruction के लिए cache use कर सकता है जो dependencies install करता है:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Package requirements वाली file **अक्सर change नहीं होगी**। इसलिए, केवल उस file को copy करके, Docker उस step के लिए **cache use** कर पाएगा।

और फिर, Docker उन dependencies को download और install करने वाले **अगले step के लिए cache use** कर पाएगा। और यहीं हम **बहुत समय बचाते हैं**। ✨ ...और इंतज़ार की बोरियत से बचते हैं। 😪😆

Package dependencies को download और install करने में **minutes लग सकते हैं**, लेकिन **cache** का उपयोग करने में अधिकतम **seconds** लगेंगे।

और क्योंकि development के दौरान आप अपने code changes काम कर रहे हैं या नहीं यह check करने के लिए container image बार-बार build करेंगे, इससे बहुत सारा जमा हुआ समय बचेगा।

फिर, `Dockerfile` के end के पास, हम सारा code copy करते हैं। क्योंकि यही वह चीज़ है जो **सबसे अधिक बार change होती** है, हम इसे end के पास रखते हैं, क्योंकि लगभग हमेशा इस step के बाद कुछ भी cache use नहीं कर पाएगा।

```Dockerfile
COPY ./app /code/app
```

### Docker Image Build करें { #build-the-docker-image }

अब जब सभी files अपनी जगह पर हैं, चलिए container image build करते हैं।

* Project directory में जाएँ (जहाँ आपका `Dockerfile` है, जिसमें आपकी `app` directory है)।
* अपनी FastAPI image build करें:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | टिप

अंत में `.` पर ध्यान दें, यह `./` के equivalent है, यह Docker को container image build करने के लिए use की जाने वाली directory बताता है।

इस मामले में, यह वही current directory (`.`) है।

///

### Docker Container Start करें { #start-the-docker-container }

* अपनी image पर आधारित container run करें:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## इसे Check करें { #check-it }

आप इसे अपने Docker container के URL में check कर पाएँगे, उदाहरण के लिए: [http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) या [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery) (या equivalent, अपने Docker host का उपयोग करके)।

आपको कुछ ऐसा दिखेगा:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Interactive API docs { #interactive-api-docs }

अब आप [http://192.168.99.100/docs](http://192.168.99.100/docs) या [http://127.0.0.1/docs](http://127.0.0.1/docs) (या equivalent, अपने Docker host का उपयोग करके) पर जा सकते हैं।

आप automatic interactive API documentation देखेंगे ([Swagger UI](https://github.com/swagger-api/swagger-ui) द्वारा provided):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Alternative API docs { #alternative-api-docs }

और आप [http://192.168.99.100/redoc](http://192.168.99.100/redoc) या [http://127.0.0.1/redoc](http://127.0.0.1/redoc) (या equivalent, अपने Docker host का उपयोग करके) पर भी जा सकते हैं।

आप alternative automatic documentation देखेंगे ([ReDoc](https://github.com/Rebilly/ReDoc) द्वारा provided):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Single-File FastAPI के साथ Docker Image बनाएँ { #build-a-docker-image-with-a-single-file-fastapi }

यदि आपकी FastAPI एक single file है, उदाहरण के लिए, `./app` directory के बिना `main.py`, तो आपकी file structure ऐसी दिख सकती है:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

फिर आपको बस `Dockerfile` के अंदर file copy करने के लिए संबंधित paths बदलने होंगे:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. `main.py` file को सीधे `/code` directory में copy करें (बिना किसी `./app` directory के)।

2. Single file `main.py` में अपनी application serve करने के लिए `fastapi run` use करें।

जब आप file को `fastapi run` में pass करते हैं, तो यह automatically detect करेगा कि यह single file है और किसी package का हिस्सा नहीं है, और यह जान जाएगा कि इसे कैसे import करना है और आपकी FastAPI app को serve करना है। 😎

## Deployment Concepts { #deployment-concepts }

आइए containers के संदर्भ में फिर से उन्हीं कुछ [Deployment Concepts](concepts.md) के बारे में बात करें।

Containers मुख्य रूप से application को **build और deploy** करने की process को सरल बनाने का tool हैं, लेकिन वे इन **deployment concepts** को handle करने के लिए कोई particular approach enforce नहीं करते, और कई संभावित strategies हैं।

**अच्छी खबर** यह है कि हर अलग strategy के साथ सभी deployment concepts को cover करने का एक तरीका है। 🎉

आइए इन **deployment concepts** को containers के संदर्भ में review करें:

* HTTPS
* startup पर Running
* Restarts
* Replication (running processes की संख्या)
* Memory
* Start करने से पहले previous steps

## HTTPS { #https }

यदि हम FastAPI application के लिए सिर्फ **container image** (और बाद में running **container**) पर focus करें, तो HTTPS सामान्यतः किसी अन्य tool द्वारा **externally** handle किया जाएगा।

यह कोई दूसरा container हो सकता है, उदाहरण के लिए [Traefik](https://traefik.io/) के साथ, जो **HTTPS** और **certificates** की **automatic** acquisition handle करता है।

/// tip | टिप

Traefik के Docker, Kubernetes, और अन्य के साथ integrations हैं, इसलिए इसके साथ अपने containers के लिए HTTPS set up और configure करना बहुत आसान है।

///

वैकल्पिक रूप से, HTTPS को किसी cloud provider द्वारा उनकी services में से एक के रूप में handle किया जा सकता है (application अभी भी container में चल रही हो)।

## Startup पर Running और Restarts { #running-on-startup-and-restarts }

सामान्यतः कोई दूसरा tool आपके container को **start और run** करने के लिए charge में होता है।

यह सीधे **Docker**, **Docker Compose**, **Kubernetes**, कोई **cloud service**, आदि हो सकता है।

अधिकतर (या सभी) मामलों में, startup पर container run करने और failures पर restarts enable करने के लिए एक simple option होता है। उदाहरण के लिए, Docker में यह command line option `--restart` है।

Containers का उपयोग किए बिना, applications को startup पर और restarts के साथ run कराना cumbersome और difficult हो सकता है। लेकिन **containers के साथ काम करते समय** अधिकतर मामलों में यह functionality default रूप से शामिल होती है। ✨

## Replication - Processes की संख्या { #replication-number-of-processes }

यदि आपके पास machines का <dfn title="मशीनों का एक समूह जो किसी तरह से connect होने और साथ काम करने के लिए configured हैं।">cluster</dfn> है जिसमें **Kubernetes**, Docker Swarm Mode, Nomad, या multiple machines पर distributed containers manage करने के लिए कोई अन्य similar complex system है, तो आप शायद प्रत्येक container में **process manager** (जैसे workers के साथ Uvicorn) उपयोग करने के बजाय **cluster level** पर **replication handle** करना चाहेंगे।

Kubernetes जैसे distributed container management systems में incoming requests के लिए **load balancing** support करते हुए **containers की replication** handle करने का कोई integrated तरीका सामान्यतः होता है। सब **cluster level** पर।

उन मामलों में, आप शायद ऊपर [समझाए अनुसार](#dockerfile) **scratch से Docker image** build करना चाहेंगे, अपनी dependencies install करके, और multiple Uvicorn workers उपयोग करने के बजाय **single Uvicorn process** run करना चाहेंगे।

### Load Balancer { #load-balancer }

Containers का उपयोग करते समय, आपके पास सामान्यतः कोई component होगा जो **main port पर listening** कर रहा होगा। संभवतः यह कोई दूसरा container हो सकता है जो **HTTPS** handle करने के लिए **TLS Termination Proxy** भी हो, या कोई similar tool।

क्योंकि यह component requests का **load** लेगा और उसे workers में (उम्मीद है) **balanced** तरीके से distribute करेगा, इसे सामान्यतः **Load Balancer** भी कहा जाता है।

/// tip | टिप

HTTPS के लिए उपयोग किया गया वही **TLS Termination Proxy** component शायद **Load Balancer** भी होगा।

///

और containers के साथ काम करते समय, उन्हें start और manage करने के लिए आप जो system use करते हैं, उसमें उस **load balancer** (जो **TLS Termination Proxy** भी हो सकता है) से आपकी app वाले container(s) तक **network communication** (जैसे HTTP requests) transmit करने के internal tools पहले से होंगे।

### One Load Balancer - Multiple Worker Containers { #one-load-balancer-multiple-worker-containers }

**Kubernetes** या similar distributed container management systems के साथ काम करते समय, उनके internal networking mechanisms का उपयोग main **port** पर listening करने वाले single **load balancer** को communication (requests) आपकी app चला रहे संभवतः **multiple containers** तक transmit करने देगा।

आपकी app चला रहे इन containers में से प्रत्येक में सामान्यतः **सिर्फ एक process** होगा (जैसे आपकी FastAPI application चलाने वाला Uvicorn process)। वे सभी **identical containers** होंगे, वही चीज़ चला रहे होंगे, लेकिन प्रत्येक का अपना process, memory, आदि होगा। इस तरह आप CPU के **different cores** में, या यहाँ तक कि **different machines** में **parallelization** का लाभ उठाएँगे।

और **load balancer** वाला distributed container system requests को आपकी app वाले प्रत्येक container तक **बारी-बारी से distribute** करेगा। इसलिए, प्रत्येक request आपकी app चला रहे multiple **replicated containers** में से किसी एक द्वारा handle की जा सकती है।

और सामान्यतः यह **load balancer** आपके cluster में *other* apps पर जाने वाली requests handle कर पाएगा (जैसे अलग domain पर, या अलग URL path prefix के तहत), और उस communication को आपके cluster में चल रही *उस other* application के सही containers तक transmit करेगा।

### प्रति Container एक Process { #one-process-per-container }

इस तरह के scenario में, आप शायद **प्रति container एक single (Uvicorn) process** रखना चाहेंगे, क्योंकि आप पहले से ही cluster level पर replication handle कर रहे होंगे।

तो, इस मामले में, आप container में multiple workers **नहीं** रखना चाहेंगे, उदाहरण के लिए `--workers` command line option के साथ। आप प्रति container बस **single Uvicorn process** रखना चाहेंगे (लेकिन शायद multiple containers)।

Container के अंदर एक और process manager रखना (जैसा multiple workers के साथ होगा) केवल **unnecessary complexity** जोड़ेगा, जिसे आप बहुत संभव है कि अपने cluster system के साथ पहले से संभाल रहे हैं।

### Multiple Processes वाले Containers और Special Cases { #containers-with-multiple-processes-and-special-cases }

बेशक, ऐसे **special cases** हैं जहाँ आप अंदर कई **Uvicorn worker processes** वाला **container** रखना चाह सकते हैं।

उन मामलों में, आप run किए जाने वाले workers की संख्या set करने के लिए `--workers` command line option उपयोग कर सकते हैं:

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. यहाँ हम workers की संख्या 4 पर set करने के लिए `--workers` command line option उपयोग करते हैं।

यहाँ कुछ examples हैं कि यह कब meaningful हो सकता है:

#### एक Simple App { #a-simple-app }

यदि आपकी application **इतनी simple** है कि आप इसे **single server** पर run कर सकते हैं, cluster पर नहीं, तो आप container में process manager चाह सकते हैं।

#### Docker Compose { #docker-compose }

आप **Docker Compose** के साथ **single server** (cluster नहीं) पर deploy कर रहे हो सकते हैं, इसलिए shared network और **load balancing** preserve करते हुए containers की replication (Docker Compose के साथ) manage करने का आसान तरीका आपके पास नहीं होगा।

फिर आप **single container** रखना चाह सकते हैं जिसमें **process manager** अंदर **कई worker processes** start करे।

---

मुख्य बात यह है कि इनमें से **कोई भी** ऐसी **पत्थर पर लिखी rules** नहीं हैं जिन्हें आपको आँख बंद करके follow करना हो। आप इन ideas का उपयोग **अपने use case का evaluate** करने और अपने system के लिए best approach तय करने के लिए कर सकते हैं, यह check करते हुए कि इन concepts को कैसे manage करना है:

* Security - HTTPS
* startup पर Running
* Restarts
* Replication (running processes की संख्या)
* Memory
* Start करने से पहले previous steps

## Memory { #memory }

यदि आप **प्रति container single process** run करते हैं, तो उन containers में से प्रत्येक (यदि replicated हैं तो एक से अधिक) द्वारा consumed memory की quantity कमोबेश well-defined, stable, और limited होगी।

और फिर आप अपने container management system (उदाहरण के लिए **Kubernetes** में) की configurations में वही memory limits और requirements set कर सकते हैं। इस तरह वह उन containers द्वारा आवश्यक memory की मात्रा, और cluster में machines में available मात्रा को ध्यान में रखते हुए **available machines** में **containers replicate** कर पाएगा।

यदि आपकी application **simple** है, तो यह शायद **problem नहीं होगी**, और आपको hard memory limits specify करने की आवश्यकता नहीं हो सकती। लेकिन यदि आप **बहुत memory use** कर रहे हैं (उदाहरण के लिए **machine learning** models के साथ), तो आपको check करना चाहिए कि आप कितनी memory consume कर रहे हैं और **प्रत्येक machine** पर run होने वाले **containers की संख्या** adjust करनी चाहिए (और शायद अपने cluster में और machines add करनी चाहिए)।

यदि आप **प्रति container multiple processes** run करते हैं, तो आपको सुनिश्चित करना होगा कि start किए गए processes की संख्या available memory से **अधिक memory consume** न करे।

## Start करने से पहले Previous Steps और Containers { #previous-steps-before-starting-and-containers }

यदि आप containers (जैसे Docker, Kubernetes) उपयोग कर रहे हैं, तो दो मुख्य approaches हैं जिनका आप उपयोग कर सकते हैं।

### Multiple Containers { #multiple-containers }

यदि आपके पास **multiple containers** हैं, शायद प्रत्येक **single process** run कर रहा है (उदाहरण के लिए, **Kubernetes** cluster में), तो आप replicated worker containers run करने से **पहले**, single container में, single process चलाते हुए, **previous steps** का काम करने वाला **separate container** रखना चाहेंगे।

/// note | नोट

यदि आप Kubernetes उपयोग कर रहे हैं, तो यह शायद [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) होगा।

///

यदि आपके use case में उन previous steps को **parallel में multiple times** run करने में कोई problem नहीं है (उदाहरण के लिए यदि आप database migrations नहीं चला रहे, बल्कि बस check कर रहे हैं कि database अभी ready है या नहीं), तो आप उन्हें हर container में main process start करने से ठीक पहले भी रख सकते हैं।

### Single Container { #single-container }

यदि आपका setup simple है, जिसमें **single container** है जो फिर multiple **worker processes** start करता है (या सिर्फ एक process), तो आप app के साथ process start करने से ठीक पहले, उन previous steps को उसी container में run कर सकते हैं।

### Base Docker Image { #base-docker-image }

एक official FastAPI Docker image हुआ करती थी: [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)। लेकिन अब यह deprecated है। ⛔️

आपको शायद इस base Docker image (या किसी अन्य similar one) का उपयोग **नहीं** करना चाहिए।

यदि आप **Kubernetes** (या अन्य) उपयोग कर रहे हैं और पहले से ही cluster level पर, multiple **containers** के साथ **replication** set कर रहे हैं। उन मामलों में, ऊपर बताए अनुसार **scratch से image build** करना बेहतर है: [FastAPI के लिए Docker Image बनाएँ](#build-a-docker-image-for-fastapi).

और यदि आपको multiple workers की आवश्यकता है, तो आप बस `--workers` command line option उपयोग कर सकते हैं।

/// note | Technical Details

Docker image तब बनाई गई थी जब Uvicorn dead workers को manage और restart करने का support नहीं करता था, इसलिए Uvicorn के साथ Gunicorn का उपयोग करना required था, जिससे काफी complexity जुड़ती थी, सिर्फ इसलिए कि Gunicorn Uvicorn worker processes को manage और restart कर सके।

लेकिन अब जब Uvicorn (और `fastapi` command) `--workers` use करने का support करते हैं, तो अपनी खुद की build करने के बजाय base Docker image उपयोग करने का कोई कारण नहीं है (यह लगभग उतनी ही code की मात्रा है 😅).

///

## Container Image Deploy करें { #deploy-the-container-image }

Container (Docker) Image होने के बाद इसे deploy करने के कई तरीके हैं।

उदाहरण के लिए:

* Single server में **Docker Compose** के साथ
* **Kubernetes** cluster के साथ
* Docker Swarm Mode cluster के साथ
* Nomad जैसे किसी अन्य tool के साथ
* किसी cloud service के साथ जो आपकी container image लेता है और उसे deploy करता है

## `uv` के साथ Docker Image { #docker-image-with-uv }

यदि आप अपने project को install और manage करने के लिए [uv](https://github.com/astral-sh/uv) उपयोग कर रहे हैं, तो आप उनकी [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/) follow कर सकते हैं।

## Recap { #recap }

Container systems (जैसे **Docker** और **Kubernetes** के साथ) का उपयोग करने पर सभी **deployment concepts** handle करना काफी straightforward हो जाता है:

* HTTPS
* startup पर Running
* Restarts
* Replication (running processes की संख्या)
* Memory
* Start करने से पहले previous steps

अधिकतर मामलों में, आप शायद कोई base image use नहीं करना चाहेंगे, और इसके बजाय official Python Docker image पर आधारित **scratch से container image build** करेंगे।

`Dockerfile` में instructions के **order** और **Docker cache** का ध्यान रखकर आप **build times minimize** कर सकते हैं, ताकि आपकी productivity maximize हो (और बोरियत से बचें)। 😎
