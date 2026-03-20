# Container'larda FastAPI - Docker { #fastapi-in-containers-docker }

FastAPI uygulamalarını deploy ederken yaygın bir yaklaşım, bir **Linux container image** oluşturmaktır. Bu genellikle [**Docker**](https://www.docker.com/) kullanılarak yapılır. Ardından bu container image'ı birkaç farklı yöntemden biriyle deploy edebilirsiniz.

Linux container'ları kullanmanın **güvenlik**, **tekrarlanabilirlik**, **basitlik** gibi birçok avantajı vardır.

/// tip | İpucu

Aceleniz var ve bunları zaten biliyor musunuz? Aşağıdaki [`Dockerfile`'a atlayın 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Dockerfile Önizleme 👀</summary>

```Dockerfile
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## Container Nedir { #what-is-a-container }

Container'lar (özellikle Linux container'ları), bir uygulamayı tüm bağımlılıkları ve gerekli dosyalarıyla birlikte paketlemenin, aynı sistemdeki diğer container'lardan (diğer uygulama ya da bileşenlerden) izole tutarken yapılan, çok **hafif** bir yoludur.

Linux container'ları, host'un (makine, sanal makine, cloud server vb.) aynı Linux kernel'ini kullanarak çalışır. Bu da, tüm bir işletim sistemini emüle eden tam sanal makinelere kıyasla çok daha hafif oldukları anlamına gelir.

Bu sayede container'lar **az kaynak** tüketir; süreçleri doğrudan çalıştırmaya benzer bir seviyede (bir sanal makine çok daha fazla tüketirdi).

Container'ların ayrıca kendi **izole** çalışan process'leri (çoğunlukla tek bir process), dosya sistemi ve ağı vardır. Bu da deployment, güvenlik, geliştirme vb. süreçleri kolaylaştırır.

## Container Image Nedir { #what-is-a-container-image }

Bir **container**, bir **container image**'dan çalıştırılır.

Container image; bir container içinde bulunması gereken tüm dosyaların, environment variable'ların ve varsayılan komut/programın **statik** bir sürümüdür. Buradaki **statik**, container **image**'ının çalışmadığı, execute edilmediği; sadece paketlenmiş dosyalar ve metadata olduğu anlamına gelir.

Depolanmış statik içerik olan "**container image**"ın aksine, "**container**" normalde çalışan instance'ı, yani **execute edilen** şeyi ifade eder.

**Container** başlatılıp çalıştığında (bir **container image**'dan başlatılır), dosyalar oluşturabilir/değiştirebilir, environment variable'ları değiştirebilir vb. Bu değişiklikler sadece o container içinde kalır; alttaki container image'da kalıcı olmaz (diske kaydedilmez).

Bir container image, **program** dosyası ve içeriklerine benzetilebilir; örn. `python` ve `main.py` gibi bir dosya.

Ve **container**'ın kendisi (container image'a karşıt olarak) image'ın gerçek çalışan instance'ıdır; bir **process**'e benzer. Hatta bir container, yalnızca içinde **çalışan bir process** varken çalışır (ve genelde tek process olur). İçinde çalışan process kalmayınca container durur.

## Container Image'lar { #container-images }

Docker, **container image** ve **container** oluşturup yönetmek için kullanılan başlıca araçlardan biri olmuştur.

Ayrıca birçok araç, ortam, veritabanı ve uygulama için önceden hazırlanmış **resmi container image**'ların bulunduğu herkese açık bir [Docker Hub](https://hub.docker.com/) vardır.

Örneğin, resmi bir [Python Image](https://hub.docker.com/_/python) bulunur.

Ve veritabanları gibi farklı şeyler için de birçok image vardır; örneğin:

* [PostgreSQL](https://hub.docker.com/_/postgres)
* [MySQL](https://hub.docker.com/_/mysql)
* [MongoDB](https://hub.docker.com/_/mongo)
* [Redis](https://hub.docker.com/_/redis), vb.

Hazır bir container image kullanarak farklı araçları **birleştirmek** ve birlikte kullanmak çok kolaydır. Örneğin yeni bir veritabanını denemek için. Çoğu durumda **resmi image**'ları kullanıp sadece environment variable'lar ile yapılandırmanız yeterlidir.

Bu şekilde, çoğu zaman container'lar ve Docker hakkında öğrendiklerinizi farklı araç ve bileşenlerde tekrar kullanabilirsiniz.

Dolayısıyla; veritabanı, Python uygulaması, React frontend uygulaması olan bir web server gibi farklı şeyler için **birden fazla container** çalıştırır ve bunları internal network üzerinden birbirine bağlarsınız.

Docker veya Kubernetes gibi tüm container yönetim sistemlerinde bu ağ özellikleri entegre olarak bulunur.

## Container'lar ve Process'ler { #containers-and-processes }

Bir **container image** normalde metadata içinde, **container** başlatıldığında çalıştırılacak varsayılan program/komutu ve o programa geçirilecek parametreleri içerir. Bu, komut satırında yazacağınız şeye çok benzer.

Bir **container** başlatıldığında bu komutu/programı çalıştırır (ancak isterseniz bunu override edip başka bir komut/program çalıştırabilirsiniz).

Bir container, **ana process** (komut/program) çalıştığı sürece çalışır.

Container'larda normalde **tek bir process** olur. Ancak ana process içinden subprocess'ler başlatmak da mümkündür; böylece aynı container içinde **birden fazla process** olur.

Ama **en az bir çalışan process olmadan** çalışan bir container olamaz. Ana process durursa container da durur.

## FastAPI için Docker Image Oluşturalım { #build-a-docker-image-for-fastapi }

Tamam, şimdi bir şeyler inşa edelim! 🚀

Resmi **Python** image'ını temel alarak, FastAPI için **sıfırdan** bir **Docker image** nasıl oluşturulur göstereceğim.

Bu, örneğin şu durumlarda **çoğu zaman** yapmak isteyeceğiniz şeydir:

* **Kubernetes** veya benzeri araçlar kullanırken
* **Raspberry Pi** üzerinde çalıştırırken
* Container image'ınızı sizin için çalıştıran bir cloud servisi kullanırken, vb.

### Paket Gereksinimleri { #package-requirements }

Uygulamanızın **paket gereksinimleri** genelde bir dosyada yer alır.

Bu, gereksinimleri **yüklemek** için kullandığınız araca göre değişir.

En yaygın yöntem, paket adları ve versiyonlarının satır satır yazıldığı bir `requirements.txt` dosyasına sahip olmaktır.

Versiyon aralıklarını belirlemek için elbette [FastAPI sürümleri hakkında](versions.md) bölümünde okuduğunuz fikirleri kullanırsınız.

Örneğin `requirements.txt` şöyle görünebilir:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

Ve bu bağımlılıkları normalde `pip` ile yüklersiniz, örneğin:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | Bilgi

Paket bağımlılıklarını tanımlamak ve yüklemek için başka formatlar ve araçlar da vardır.

///

### **FastAPI** Kodunu Oluşturun { #create-the-fastapi-code }

* Bir `app` dizini oluşturun ve içine girin.
* Boş bir `__init__.py` dosyası oluşturun.
* Aşağıdakilerle bir `main.py` dosyası oluşturun:

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

Şimdi aynı proje dizininde `Dockerfile` adlı bir dosya oluşturun ve içine şunları yazın:

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

1. Resmi Python base image'ından başlayın.

2. Geçerli çalışma dizinini `/code` olarak ayarlayın.

    `requirements.txt` dosyasını ve `app` dizinini buraya koyacağız.

3. Gereksinimleri içeren dosyayı `/code` dizinine kopyalayın.

    Önce kodun tamamını değil, **sadece** gereksinim dosyasını kopyalayın.

    Bu dosya **çok sık değişmediği** için Docker bunu tespit eder ve bu adımda **cache** kullanır; böylece bir sonraki adım için de cache devreye girer.

4. Gereksinim dosyasındaki paket bağımlılıklarını yükleyin.

    `--no-cache-dir` seçeneği, indirilen paketlerin yerel olarak kaydedilmemesini `pip`'e söyler. Bu kayıt, `pip` aynı paketleri tekrar yüklemek için yeniden çalıştırılacaksa işe yarar; ancak container'larla çalışırken genelde bu durum geçerli değildir.

    /// note | Not

    `--no-cache-dir` yalnızca `pip` ile ilgilidir; Docker veya container'larla ilgili değildir.

    ///

    `--upgrade` seçeneği, paketler zaten yüklüyse `pip`'e onları yükseltmesini söyler.

    Bir önceki adım (dosyayı kopyalama) **Docker cache** tarafından tespit edilebildiği için, bu adım da uygun olduğunda **Docker cache'i kullanır**.

    Bu adımda cache kullanmak, geliştirme sırasında image'ı tekrar tekrar build ederken size çok **zaman** kazandırır; her seferinde bağımlılıkları **indirip yüklemek** zorunda kalmazsınız.

5. `./app` dizinini `/code` dizininin içine kopyalayın.

    Burada en sık değişen şey olan kodun tamamı bulunduğundan, bu adım (ve genelde bundan sonraki adımlar) için Docker **cache**'i kolay kolay kullanılamaz.

    Bu yüzden, container image build sürelerini optimize etmek için bunu `Dockerfile`'ın **sonlarına yakın** koymak önemlidir.

6. Altta Uvicorn kullanan `fastapi run` komutunu **command** olarak ayarlayın.

    `CMD` bir string listesi alır; bu string'lerin her biri komut satırında boşlukla ayrılmış şekilde yazacağınız parçaları temsil eder.

    Bu komut, yukarıda `WORKDIR /code` ile ayarladığınız `/code` dizininden çalıştırılır.

/// tip | İpucu

Kod içindeki her numara balonuna tıklayarak her satırın ne yaptığını gözden geçirin. 👆

///

/// warning | Uyarı

Aşağıda açıklandığı gibi `CMD` talimatının **her zaman** **exec form**'unu kullandığınızdan emin olun.

///

#### `CMD` Kullanımı - Exec Form { #use-cmd-exec-form }

[`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) Docker talimatı iki formda yazılabilir:

✅ **Exec** form:

```Dockerfile
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```Dockerfile
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

FastAPI'nin düzgün şekilde kapanabilmesi ve [lifespan event](../advanced/events.md)'lerinin tetiklenmesi için her zaman **exec** formunu kullanın.

Detaylar için [shell ve exec form için Docker dokümanlarına](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form) bakabilirsiniz.

Bu durum `docker compose` kullanırken oldukça belirgin olabilir. Daha teknik detaylar için şu Docker Compose FAQ bölümüne bakın: [Hizmetlerimin yeniden oluşturulması veya durması neden 10 saniye sürüyor?](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop).

#### Dizin Yapısı { #directory-structure }

Artık dizin yapınız şöyle olmalı:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### TLS Termination Proxy Arkasında { #behind-a-tls-termination-proxy }

Container'ınızı Nginx veya Traefik gibi bir TLS Termination Proxy (load balancer) arkasında çalıştırıyorsanız `--proxy-headers` seçeneğini ekleyin. Bu, Uvicorn'a (FastAPI CLI üzerinden) uygulamanın HTTPS arkasında çalıştığını söyleyen proxy header'larına güvenmesini söyler.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker Cache { #docker-cache }

Bu `Dockerfile` içinde önemli bir numara var: önce kodun geri kalanını değil, **sadece bağımlılık dosyasını** kopyalıyoruz. Nedenini anlatayım.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker ve benzeri araçlar bu container image'larını **artımlı (incremental)** olarak **build** eder; `Dockerfile`'ın en üstünden başlayıp her talimatın oluşturduğu dosyaları ekleyerek **katman katman (layer)** ilerler.

Docker ve benzeri araçlar image build ederken ayrıca bir **internal cache** kullanır. Son build'den beri bir dosya değişmediyse, dosyayı tekrar kopyalayıp sıfırdan yeni bir layer oluşturmak yerine, daha önce oluşturulan **aynı layer**'ı yeniden kullanır.

Sadece dosya kopyalamayı azaltmak her zaman büyük fark yaratmaz. Ancak o adımda cache kullanıldığı için, **bir sonraki adımda da cache kullanılabilir**. Örneğin bağımlılıkları yükleyen şu talimat için:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Paket gereksinimleri dosyası **sık sık değişmez**. Bu yüzden sadece bu dosyayı kopyalayınca, Docker bu adımda **cache** kullanabilir.

Sonra Docker, bağımlılıkları indirip yükleyen **bir sonraki adımda** da cache kullanabilir. Asıl **çok zaman kazandığımız** yer de burasıdır. ✨ ...ve beklerken sıkılmayı engeller. 😪😆

Bağımlılıkları indirip yüklemek **dakikalar sürebilir**, fakat **cache** kullanmak en fazla **saniyeler** alır.

Geliştirme sırasında kod değişikliklerinizin çalıştığını kontrol etmek için container image'ı tekrar tekrar build edeceğinizden, bu ciddi birikimli zaman kazancı sağlar.

Sonra `Dockerfile`'ın sonlarına doğru tüm kodu kopyalarız. En sık değişen kısım bu olduğu için sona koyarız; çünkü neredeyse her zaman bu adımdan sonra gelen adımlar cache kullanamaz.

```Dockerfile
COPY ./app /code/app
```

### Docker Image'ını Build Edin { #build-the-docker-image }

Tüm dosyalar hazır olduğuna göre container image'ı build edelim.

* Proje dizinine gidin (`Dockerfile`'ınızın olduğu ve `app` dizininizi içeren dizin).
* FastAPI image'ınızı build edin:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | İpucu

Sondaki `.` ifadesine dikkat edin; `./` ile aynı anlama gelir ve Docker'a container image build etmek için hangi dizini kullanacağını söyler.

Bu örnekte, mevcut dizindir (`.`).

///

### Docker Container'ını Başlatın { #start-the-docker-container }

* Image'ınızdan bir container çalıştırın:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## Kontrol Edin { #check-it }

Docker container'ınızın URL'inden kontrol edebilmelisiniz. Örneğin: [http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) veya [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery) (ya da Docker host'unuzu kullanarak eşdeğeri).

Şuna benzer bir şey görürsünüz:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Etkileşimli API Dokümanları { #interactive-api-docs }

Şimdi [http://192.168.99.100/docs](http://192.168.99.100/docs) veya [http://127.0.0.1/docs](http://127.0.0.1/docs) adresine gidebilirsiniz (ya da Docker host'unuzla eşdeğeri).

Otomatik etkileşimli API dokümantasyonunu görürsünüz ( [Swagger UI](https://github.com/swagger-api/swagger-ui) tarafından sağlanır):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Alternatif API Dokümanları { #alternative-api-docs }

Ayrıca [http://192.168.99.100/redoc](http://192.168.99.100/redoc) veya [http://127.0.0.1/redoc](http://127.0.0.1/redoc) adresine de gidebilirsiniz (ya da Docker host'unuzla eşdeğeri).

Alternatif otomatik dokümantasyonu görürsünüz ([ReDoc](https://github.com/Rebilly/ReDoc) tarafından sağlanır):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Tek Dosyalık FastAPI ile Docker Image Oluşturma { #build-a-docker-image-with-a-single-file-fastapi }

FastAPI uygulamanız tek bir dosyaysa; örneğin `./app` dizini olmadan sadece `main.py` varsa, dosya yapınız şöyle olabilir:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Bu durumda `Dockerfile` içinde dosyayı kopyaladığınız path'leri buna göre değiştirmeniz yeterlidir:

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

1. `main.py` dosyasını doğrudan `/code` dizinine kopyalayın (herhangi bir `./app` dizini olmadan).

2. Tek dosya olan `main.py` içindeki uygulamanızı sunmak için `fastapi run` kullanın.

Dosyayı `fastapi run`'a verdiğinizde, bunun bir package'ın parçası değil tek bir dosya olduğunu otomatik olarak algılar; nasıl import edip FastAPI uygulamanızı nasıl serve edeceğini bilir. 😎

## Deployment Kavramları { #deployment-concepts }

Aynı [Deployment Kavramları](concepts.md)nı bu kez container'lar açısından tekrar konuşalım.

Container'lar, bir uygulamayı **build etme ve deploy etme** sürecini basitleştiren bir araçtır. Ancak bu **deployment kavramları**nı ele almak için belirli bir yaklaşımı zorunlu kılmazlar; birkaç farklı strateji mümkündür.

**İyi haber** şu: Hangi stratejiyi seçerseniz seçin, deployment kavramlarının tamamını kapsayacak bir yol vardır. 🎉

Bu **deployment kavramları**nı container'lar açısından gözden geçirelim:

* HTTPS
* Startup'ta çalıştırma
* Restart'lar
* Replication (çalışan process sayısı)
* Memory
* Başlatmadan önceki adımlar

## HTTPS { #https }

Bir FastAPI uygulamasının sadece **container image**'ına (ve sonra çalışan **container**'a) odaklanırsak, HTTPS genellikle **haricen** başka bir araçla ele alınır.

Örneğin [Traefik](https://traefik.io/) kullanan başka bir container olabilir; **HTTPS** ve **sertifika**ların **otomatik** alınmasını o yönetebilir.

/// tip | İpucu

Traefik; Docker, Kubernetes ve diğerleriyle entegre çalışır. Bu sayede container'larınız için HTTPS'i kurup yapılandırmak oldukça kolaydır.

///

Alternatif olarak HTTPS, bir cloud provider'ın sunduğu servislerden biri tarafından da yönetilebilir (uygulama yine container içinde çalışırken).

## Startup'ta Çalıştırma ve Restart'lar { #running-on-startup-and-restarts }

Container'ınızı **başlatıp çalıştırmaktan** sorumlu genellikle başka bir araç olur.

Bu; doğrudan **Docker**, **Docker Compose**, **Kubernetes**, bir **cloud service** vb. olabilir.

Çoğu (veya tüm) durumda, container'ı startup'ta çalıştırmayı ve hata durumlarında restart'ları etkinleştirmeyi sağlayan basit bir seçenek vardır. Örneğin Docker'da bu, `--restart` komut satırı seçeneğidir.

Container kullanmadan, uygulamaları startup'ta çalıştırmak ve restart mekanizması eklemek zahmetli ve zor olabilir. Ancak **container'larla çalışırken** çoğu zaman bu işlevler varsayılan olarak hazır gelir. ✨

## Replication - Process Sayısı { #replication-number-of-processes }

Eğer bir <dfn title="Bir şekilde birbirine bağlanacak ve birlikte çalışacak şekilde yapılandırılmış makineler grubu.">küme</dfn> (cluster) olarak yapılandırılmış makineler grubunuz varsa ve bunları **Kubernetes**, Docker Swarm Mode, Nomad veya benzeri, birden çok makinede dağıtık container'ları yöneten karmaşık bir sistemle yönetiyorsanız, replication'ı her container içinde bir **process manager** (ör. worker'lı Uvicorn) kullanarak yönetmek yerine, muhtemelen **küme seviyesinde (cluster level)** ele almak istersiniz.

Kubernetes gibi dağıtık container yönetim sistemleri, gelen request'ler için **load balancing** desteği sunarken aynı zamanda **container replication**'ını yönetmek için entegre mekanizmalara sahiptir. Hepsi **cluster seviyesinde**.

Bu tür durumlarda, yukarıda [anlatıldığı gibi](#dockerfile) bağımlılıkları yükleyip **sıfırdan bir Docker image** build etmek ve birden fazla Uvicorn worker kullanmak yerine **tek bir Uvicorn process** çalıştırmak istersiniz.

### Load Balancer { #load-balancer }

Container'lar kullanırken, genellikle ana port'ta dinleyen bir bileşen olur. Bu, **HTTPS**'i ele almak için bir **TLS Termination Proxy** olan başka bir container da olabilir ya da benzeri bir araç olabilir.

Bu bileşen request'lerin **yükünü** alıp worker'lar arasında (umarım) **dengeli** şekilde dağıttığı için yaygın olarak **Load Balancer** diye de adlandırılır.

/// tip | İpucu

HTTPS için kullanılan aynı **TLS Termination Proxy** bileşeni muhtemelen bir **Load Balancer** olarak da çalışır.

///

Container'larla çalışırken, onları başlatıp yönettiğiniz sistem; bu **load balancer**'dan (aynı zamanda **TLS Termination Proxy** de olabilir) uygulamanızın bulunduğu container(lar)a **network communication**'ı (ör. HTTP request'leri) iletmek için zaten dahili araçlar sunar.

### Tek Load Balancer - Çoklu Worker Container { #one-load-balancer-multiple-worker-containers }

**Kubernetes** veya benzeri dağıtık container yönetim sistemleriyle çalışırken, dahili ağ mekanizmaları sayesinde ana **port**'u dinleyen tek bir **load balancer**, uygulamanızı çalıştıran muhtemelen **birden fazla container**'a request'leri iletebilir.

Uygulamanızı çalıştıran bu container'ların her birinde normalde **tek bir process** olur (ör. FastAPI uygulamanızı çalıştıran bir Uvicorn process). Hepsi aynı şeyi çalıştıran **özdeş container**'lardır; ancak her birinin kendi process'i, memory'si vb. vardır. Böylece CPU'nun **farklı core**'larında, hatta **farklı makinelerde** paralelleştirmeden yararlanırsınız.

Load balancer'lı dağıtık sistem, request'leri uygulamanızın bulunduğu container'ların her birine sırayla **dağıtır**. Böylece her request, uygulamanızın birden fazla **replicated container**'ından biri tarafından işlenebilir.

Ve bu **load balancer** normalde cluster'ınızdaki *diğer* uygulamalara giden request'leri de (ör. farklı bir domain ya da farklı bir URL path prefix altında) yönetebilir ve iletişimi o *diğer* uygulamanın doğru container'larına iletir.

### Container Başına Tek Process { #one-process-per-container }

Bu senaryoda, replication'ı zaten cluster seviyesinde yaptığınız için, muhtemelen **container başına tek bir (Uvicorn) process** istersiniz.

Dolayısıyla bu durumda container içinde `--workers` gibi bir komut satırı seçeneğiyle çoklu worker istemezsiniz. Container başına sadece **tek bir Uvicorn process** istersiniz (ama muhtemelen birden fazla container).

Container içine ekstra bir process manager koymak (çoklu worker gibi) çoğu zaman zaten cluster sisteminizle çözdüğünüz şeye ek **gereksiz karmaşıklık** katar.

### Birden Fazla Process'li Container'lar ve Özel Durumlar { #containers-with-multiple-processes-and-special-cases }

Elbette bazı **özel durumlarda** bir container içinde birden fazla **Uvicorn worker process** çalıştırmak isteyebilirsiniz.

Bu durumlarda çalıştırmak istediğiniz worker sayısını `--workers` komut satırı seçeneğiyle ayarlayabilirsiniz:

```{ .dockerfile .annotate }
FROM python:3.14

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. Burada worker sayısını 4 yapmak için `--workers` komut satırı seçeneğini kullanıyoruz.

Bunun mantıklı olabileceği birkaç örnek:

#### Basit Bir Uygulama { #a-simple-app }

Uygulamanız tek bir server üzerinde (cluster değil) çalışacak kadar **basitse**, container içinde bir process manager isteyebilirsiniz.

#### Docker Compose { #docker-compose }

**Docker Compose** ile **tek bir server**'a (cluster değil) deploy ediyor olabilirsiniz. Bu durumda, paylaşılan ağı ve **load balancing**'i koruyarak container replication'ını (Docker Compose ile) yönetmenin kolay bir yolu olmayabilir.

Bu durumda, tek bir container içinde **bir process manager** ile **birden fazla worker process** başlatmak isteyebilirsiniz.

---

Ana fikir şu: Bunların **hiçbiri** körü körüne uymanız gereken **değişmez kurallar** değildir. Bu fikirleri, kendi kullanım senaryonuzu **değerlendirmek** ve sisteminiz için en iyi yaklaşımı seçmek için kullanabilirsiniz. Şu kavramları nasıl yöneteceğinize bakarak karar verin:

* Güvenlik - HTTPS
* Startup'ta çalıştırma
* Restart'lar
* Replication (çalışan process sayısı)
* Memory
* Başlatmadan önceki adımlar

## Memory { #memory }

**Container başına tek process** çalıştırırsanız, her container'ın tüketeceği memory miktarı aşağı yukarı tanımlı, stabil ve sınırlı olur (replication varsa birden fazla container için).

Sonra aynı memory limit ve gereksinimlerini container yönetim sisteminizin (ör. **Kubernetes**) konfigürasyonlarında belirleyebilirsiniz. Böylece sistem; ihtiyaç duyulan memory miktarını ve cluster'daki makinelerde mevcut memory'yi dikkate alarak **uygun makinelerde container'ları replicate edebilir**.

Uygulamanız **basitse**, muhtemelen bu **bir sorun olmaz** ve katı memory limitleri belirlemeniz gerekmeyebilir. Ancak **çok memory kullanıyorsanız** (ör. **machine learning** modelleriyle), ne kadar memory tükettiğinizi kontrol edip **her makinede** çalışacak **container sayısını** ayarlamalısınız (ve gerekirse cluster'a daha fazla makine eklemelisiniz).

**Container başına birden fazla process** çalıştırırsanız, başlatılan process sayısının mevcut olandan **fazla memory tüketmediğinden** emin olmanız gerekir.

## Başlatmadan Önceki Adımlar ve Container'lar { #previous-steps-before-starting-and-containers }

Container kullanıyorsanız (örn. Docker, Kubernetes), temelde iki yaklaşım vardır.

### Birden Fazla Container { #multiple-containers }

**Birden fazla container**'ınız varsa ve muhtemelen her biri **tek process** çalıştırıyorsa (ör. bir **Kubernetes** cluster'ında), replication yapılan worker container'lar çalışmadan **önce**, **başlatmadan önceki adımlar**ın işini yapan **ayrı bir container** kullanmak isteyebilirsiniz (tek container, tek process).

/// info | Bilgi

Kubernetes kullanıyorsanız, bu muhtemelen bir [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) olur.

///

Kullanım senaryonuzda bu adımları **paralel olarak birden fazla kez** çalıştırmak sorun değilse (örneğin veritabanı migration çalıştırmıyor, sadece veritabanı hazır mı diye kontrol ediyorsanız), o zaman her container'da ana process başlamadan hemen önce de çalıştırabilirsiniz.

### Tek Container { #single-container }

Basit bir kurulumda; **tek bir container** olup onun içinde birden fazla **worker process** (ya da sadece bir process) başlatıyorsanız, bu adımları aynı container içinde, uygulama process'ini başlatmadan hemen önce çalıştırabilirsiniz.

### Base Docker Image { #base-docker-image }

Eskiden resmi bir FastAPI Docker image'ı vardı: [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker). Ancak artık kullanımdan kaldırıldı (deprecated). ⛔️

Muhtemelen bu base Docker image'ını (veya benzeri başka bir image'ı) kullanmamalısınız.

**Kubernetes** (veya diğerleri) kullanıyor ve cluster seviyesinde birden fazla **container** ile **replication** ayarlıyorsanız, bu durumda yukarıda anlatıldığı gibi **sıfırdan bir image build etmek** daha iyi olur: [FastAPI için Docker Image Oluşturalım](#build-a-docker-image-for-fastapi).

Ve birden fazla worker gerekiyorsa, sadece `--workers` komut satırı seçeneğini kullanabilirsiniz.

/// note | Teknik Detaylar

Bu Docker image, Uvicorn dead worker'ları yönetmeyi ve yeniden başlatmayı desteklemediği dönemde oluşturulmuştu. Bu yüzden Uvicorn ile birlikte Gunicorn kullanmak gerekiyordu; sırf Gunicorn, Uvicorn worker process'lerini yönetip yeniden başlatsın diye oldukça fazla karmaşıklık ekleniyordu.

Ancak artık Uvicorn (ve `fastapi` komutu) `--workers` kullanımını desteklediğine göre, kendi image'ınızı build etmek yerine bir base Docker image kullanmanın bir nedeni kalmadı (kod miktarı da hemen hemen aynı 😅).

///

## Container Image'ı Deploy Etme { #deploy-the-container-image }

Bir Container (Docker) Image'ınız olduktan sonra bunu deploy etmenin birkaç yolu vardır.

Örneğin:

* Tek bir server'da **Docker Compose** ile
* Bir **Kubernetes** cluster'ı ile
* Docker Swarm Mode cluster'ı ile
* Nomad gibi başka bir araçla
* Container image'ınızı alıp deploy eden bir cloud servisiyle

## `uv` ile Docker Image { #docker-image-with-uv }

Projenizi yüklemek ve yönetmek için [uv](https://github.com/astral-sh/uv) kullanıyorsanız, onların [uv Docker rehberini](https://docs.astral.sh/uv/guides/integration/docker/) takip edebilirsiniz.

## Özet { #recap }

Container sistemleri (örn. **Docker** ve **Kubernetes** ile) kullanınca tüm **deployment kavramları**nı ele almak oldukça kolaylaşır:

* HTTPS
* Startup'ta çalıştırma
* Restart'lar
* Replication (çalışan process sayısı)
* Memory
* Başlatmadan önceki adımlar

Çoğu durumda bir base image kullanmak istemezsiniz; bunun yerine resmi Python Docker image'ını temel alarak **sıfırdan bir container image** build edersiniz.

`Dockerfile` içindeki talimatların **sırasına** ve **Docker cache**'ine dikkat ederek **build sürelerini minimize edebilir**, üretkenliğinizi artırabilirsiniz (ve beklerken sıkılmayı önlersiniz). 😎
