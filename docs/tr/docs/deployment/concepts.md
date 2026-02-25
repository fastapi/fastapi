# Deployment Kavramları { #deployments-concepts }

Bir **FastAPI** uygulamasını (hatta genel olarak herhangi bir web API'yi) deploy ederken, muhtemelen önemseyeceğiniz bazı kavramlar vardır. Bu kavramları kullanarak, **uygulamanızı deploy etmek** için **en uygun** yöntemi bulabilirsiniz.

Önemli kavramlardan bazıları şunlardır:

* Güvenlik - HTTPS
* Startup'ta çalıştırma
* Yeniden başlatmalar
* Replikasyon (çalışan process sayısı)
* Bellek
* Başlatmadan önceki adımlar

Bunların **deployment**'ları nasıl etkilediğine bakalım.

Nihai hedef, **API client**'larınıza **güvenli** bir şekilde hizmet verebilmek, **kesintileri** önlemek ve **hesaplama kaynaklarını** (ör. uzak server'lar/sanal makineler) olabildiğince verimli kullanmaktır. 🚀

Burada bu **kavramlar** hakkında biraz daha bilgi vereceğim. Böylece, çok farklı ortamlarda—hatta bugün var olmayan **gelecekteki** ortamlarda bile—API'nizi nasıl deploy edeceğinize karar verirken ihtiyaç duyacağınız **sezgiyi** kazanmış olursunuz.

Bu kavramları dikkate alarak, **kendi API**'leriniz için en iyi deployment yaklaşımını **değerlendirebilir ve tasarlayabilirsiniz**.

Sonraki bölümlerde, FastAPI uygulamalarını deploy etmek için daha **somut tarifler** (recipes) paylaşacağım.

Ama şimdilik, bu önemli **kavramsal fikirleri** inceleyelim. Bu kavramlar diğer tüm web API türleri için de geçerlidir. 💡

## Güvenlik - HTTPS { #security-https }

[HTTPS hakkındaki önceki bölümde](https.md){.internal-link target=_blank} HTTPS'in API'niz için nasıl şifreleme sağladığını öğrenmiştik.

Ayrıca HTTPS'in genellikle uygulama server'ınızın **dışında** yer alan bir bileşen tarafından sağlandığını, yani bir **TLS Termination Proxy** ile yapıldığını da görmüştük.

Ve **HTTPS sertifikalarını yenilemekten** sorumlu bir şey olmalıdır; bu aynı bileşen olabileceği gibi farklı bir bileşen de olabilir.

### HTTPS için Örnek Araçlar { #example-tools-for-https }

TLS Termination Proxy olarak kullanabileceğiniz bazı araçlar:

* Traefik
    * Sertifika yenilemelerini otomatik yönetir ✨
* Caddy
    * Sertifika yenilemelerini otomatik yönetir ✨
* Nginx
    * Sertifika yenilemeleri için Certbot gibi harici bir bileşenle
* HAProxy
    * Sertifika yenilemeleri için Certbot gibi harici bir bileşenle
* Nginx gibi bir Ingress Controller ile Kubernetes
    * Sertifika yenilemeleri için cert-manager gibi harici bir bileşenle
* Bir cloud provider tarafından servislerinin parçası olarak içeride yönetilmesi (aşağıyı okuyun 👇)

Bir diğer seçenek de, HTTPS kurulumunu da dahil olmak üzere işin daha büyük kısmını yapan bir **cloud service** kullanmaktır. Bunun bazı kısıtları olabilir veya daha pahalı olabilir vb. Ancak bu durumda TLS Termination Proxy'yi kendiniz kurmak zorunda kalmazsınız.

Sonraki bölümlerde bazı somut örnekler göstereceğim.

---

Sonraki kavramlar, gerçek API'nizi çalıştıran programla (ör. Uvicorn) ilgilidir.

## Program ve Process { #program-and-process }

Çalışan "**process**" hakkında çok konuşacağız. Bu yüzden ne anlama geldiğini ve "**program**" kelimesinden farkının ne olduğunu netleştirmek faydalı.

### Program Nedir { #what-is-a-program }

**Program** kelimesi günlük kullanımda birçok şeyi anlatmak için kullanılır:

* Yazdığınız **code**, yani **Python dosyaları**.
* İşletim sistemi tarafından **çalıştırılabilen** **dosya**, örn: `python`, `python.exe` veya `uvicorn`.
* İşletim sistemi üzerinde **çalışır durumdayken** CPU kullanan ve bellekte veri tutan belirli bir program. Buna **process** de denir.

### Process Nedir { #what-is-a-process }

**Process** kelimesi genellikle daha spesifik kullanılır; yalnızca işletim sistemi üzerinde çalışan şeye (yukarıdaki son madde gibi) işaret eder:

* İşletim sistemi üzerinde **çalışır durumda** olan belirli bir program.
    * Bu; dosyayı ya da code'u değil, işletim sistemi tarafından **çalıştırılan** ve yönetilen şeyi ifade eder.
* Herhangi bir program, herhangi bir code, **yalnızca çalıştırılırken** bir şey yapabilir. Yani bir **process çalışıyorken**.
* Process siz tarafından veya işletim sistemi tarafından **sonlandırılabilir** (ya da "killed" edilebilir). O anda çalışması/çalıştırılması durur ve artık **hiçbir şey yapamaz**.
* Bilgisayarınızda çalışan her uygulamanın arkasında bir process vardır; çalışan her program, her pencere vb. Bilgisayar açıkken normalde **aynı anda** birçok process çalışır.
* Aynı anda **aynı programın birden fazla process**'i çalışabilir.

İşletim sisteminizdeki "task manager" veya "system monitor" (ya da benzeri araçlar) ile bu process'lerin birçoğunu çalışır halde görebilirsiniz.

Örneğin muhtemelen aynı browser programını (Firefox, Chrome, Edge vb.) çalıştıran birden fazla process göreceksiniz. Genelde her tab için bir process, üstüne bazı ek process'ler çalıştırırlar.

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

Artık **process** ve **program** arasındaki farkı bildiğimize göre, deployment konusuna devam edelim.

## Startup'ta Çalıştırma { #running-on-startup }

Çoğu durumda bir web API oluşturduğunuzda, client'larınızın her zaman erişebilmesi için API'nizin kesintisiz şekilde **sürekli çalışıyor** olmasını istersiniz. Elbette sadece belirli durumlarda çalışmasını istemenizin özel bir sebebi olabilir; ancak çoğunlukla onu sürekli açık ve **kullanılabilir** halde tutarsınız.

### Uzak Bir Server'da { #in-a-remote-server }

Uzak bir server (cloud server, sanal makine vb.) kurduğunuzda, yapabileceğiniz en basit şey; local geliştirme sırasında yaptığınız gibi, manuel olarak `fastapi run` (Uvicorn'u kullanır) veya benzeri bir komutla çalıştırmaktır.

Bu yöntem çalışır ve **geliştirme sırasında** faydalıdır.

Ancak server'a olan bağlantınız koparsa, **çalışan process** muhtemelen ölür.

Ve server yeniden başlatılırsa (örneğin update'lerden sonra ya da cloud provider'ın migration'larından sonra) bunu muhtemelen **fark etmezsiniz**. Dolayısıyla process'i manuel yeniden başlatmanız gerektiğini de bilmezsiniz. Sonuçta API'niz ölü kalır. 😱

### Startup'ta Otomatik Çalıştırma { #run-automatically-on-startup }

Genellikle server programının (ör. Uvicorn) server açılışında otomatik başlamasını ve herhangi bir **insan müdahalesi** gerektirmeden API'nizi çalıştıran bir process'in sürekli ayakta olmasını istersiniz (ör. FastAPI uygulamanızı çalıştıran Uvicorn).

### Ayrı Bir Program { #separate-program }

Bunu sağlamak için genellikle startup'ta uygulamanızın çalıştığından emin olacak **ayrı bir program** kullanırsınız. Pek çok durumda bu program, örneğin bir veritabanı gibi diğer bileşenlerin/uygulamaların da çalıştığından emin olur.

### Startup'ta Çalıştırmak için Örnek Araçlar { #example-tools-to-run-at-startup }

Bu işi yapabilen araçlara örnekler:

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* Bir cloud provider tarafından servislerinin parçası olarak içeride yönetilmesi
* Diğerleri...

Sonraki bölümlerde daha somut örnekler vereceğim.

## Yeniden Başlatmalar { #restarts }

Uygulamanızın startup'ta çalıştığından emin olmaya benzer şekilde, hatalardan sonra **yeniden başlatıldığından** da emin olmak istersiniz.

### Hata Yaparız { #we-make-mistakes }

Biz insanlar sürekli **hata** yaparız. Yazılımın neredeyse *her zaman* farklı yerlerinde gizli **bug**'lar vardır. 🐛

Ve biz geliştiriciler bu bug'ları buldukça ve yeni özellikler ekledikçe code'u iyileştiririz (muhtemelen yeni bug'lar da ekleyerek 😅).

### Küçük Hatalar Otomatik Yönetilir { #small-errors-automatically-handled }

FastAPI ile web API geliştirirken, code'umuzda bir hata olursa FastAPI genellikle bunu hatayı tetikleyen tek request ile sınırlar. 🛡

Client o request için **500 Internal Server Error** alır; ancak uygulama tamamen çöküp durmak yerine sonraki request'ler için çalışmaya devam eder.

### Daha Büyük Hatalar - Çökmeler { #bigger-errors-crashes }

Yine de bazı durumlarda, yazdığımız bir code **tüm uygulamayı çökertip** Uvicorn ve Python'ın crash olmasına neden olabilir. 💥

Böyle bir durumda, tek bir noktadaki hata yüzünden uygulamanın ölü kalmasını istemezsiniz; bozuk olmayan *path operations* en azından çalışmaya devam etsin istersiniz.

### Crash Sonrası Yeniden Başlatma { #restart-after-crash }

Ancak çalışan **process**'i çökerten gerçekten kötü hatalarda, process'i **yeniden başlatmaktan** sorumlu harici bir bileşen istersiniz; en azından birkaç kez...

/// tip | İpucu

...Yine de uygulama **hemen crash oluyorsa**, onu sonsuza kadar yeniden başlatmaya çalışmanın pek anlamı yoktur. Böyle durumları büyük ihtimalle geliştirme sırasında ya da en geç deploy'dan hemen sonra fark edersiniz.

O yüzden ana senaryoya odaklanalım: Gelecekte bazı özel durumlarda tamamen çökebilir ve yine de yeniden başlatmak mantıklıdır.

///

Uygulamanızı yeniden başlatmakla görevli bileşenin **harici bir bileşen** olmasını istersiniz. Çünkü o noktada Uvicorn ve Python ile birlikte aynı uygulama zaten crash olmuştur; aynı app'in içindeki aynı code'un bunu düzeltmek için yapabileceği bir şey kalmaz.

### Otomatik Yeniden Başlatma için Örnek Araçlar { #example-tools-to-restart-automatically }

Çoğu durumda, **startup'ta programı çalıştırmak** için kullanılan aracın aynısı otomatik **restart**'ları yönetmek için de kullanılır.

Örneğin bu şunlarla yönetilebilir:

* Docker
* Kubernetes
* Docker Compose
* Docker in Swarm Mode
* Systemd
* Supervisor
* Bir cloud provider tarafından servislerinin parçası olarak içeride yönetilmesi
* Diğerleri...

## Replikasyon - Process'ler ve Bellek { #replication-processes-and-memory }

FastAPI uygulamasında, Uvicorn'u çalıştıran `fastapi` komutu gibi bir server programı kullanırken, uygulamayı **tek bir process** içinde bir kez çalıştırmak bile aynı anda birden fazla client'a hizmet verebilir.

Ancak birçok durumda, aynı anda birden fazla worker process çalıştırmak istersiniz.

### Birden Fazla Process - Worker'lar { #multiple-processes-workers }

Tek bir process'in karşılayabileceğinden daha fazla client'ınız varsa (örneğin sanal makine çok büyük değilse) ve server CPU'sunda **birden fazla core** varsa, aynı uygulamayla **birden fazla process** çalıştırıp tüm request'leri bunlara dağıtabilirsiniz.

Aynı API programının **birden fazla process**'ini çalıştırdığınızda, bunlara genellikle **worker** denir.

### Worker Process'ler ve Port'lar { #worker-processes-and-ports }

[HTTPS hakkındaki dokümanda](https.md){.internal-link target=_blank} bir server'da aynı port ve IP adresi kombinasyonunu yalnızca tek bir process'in dinleyebileceğini hatırlıyor musunuz?

Bu hâlâ geçerli.

Dolayısıyla **aynı anda birden fazla process** çalıştırabilmek için, **port** üzerinde dinleyen **tek bir process** olmalı ve bu process iletişimi bir şekilde worker process'lere aktarmalıdır.

### Process Başına Bellek { #memory-per-process }

Program belleğe bir şeyler yüklediğinde—örneğin bir değişkende bir machine learning modelini veya büyük bir dosyanın içeriğini tutmak gibi—bunların hepsi server'ın **belleğini (RAM)** tüketir.

Ve birden fazla process normalde **belleği paylaşmaz**. Yani her çalışan process'in kendi verileri, değişkenleri ve belleği vardır. Code'unuz çok bellek tüketiyorsa, **her process** buna denk bir miktar bellek tüketir.

### Server Belleği { #server-memory }

Örneğin code'unuz **1 GB** boyutunda bir Machine Learning modelini yüklüyorsa, API'niz tek process ile çalışırken en az 1 GB RAM tüketir. **4 process** (4 worker) başlatırsanız her biri 1 GB RAM tüketir. Yani toplamda API'niz **4 GB RAM** tüketir.

Uzak server'ınız veya sanal makineniz yalnızca 3 GB RAM'e sahipse, 4 GB'tan fazla RAM yüklemeye çalışmak sorun çıkarır. 🚨

### Birden Fazla Process - Bir Örnek { #multiple-processes-an-example }

Bu örnekte, iki adet **Worker Process** başlatıp kontrol eden bir **Manager Process** vardır.

Bu Manager Process büyük ihtimalle IP üzerindeki **port**'u dinleyen süreçtir ve tüm iletişimi worker process'lere aktarır.

Worker process'ler uygulamanızı çalıştıran process'lerdir; bir **request** alıp bir **response** döndürmek için asıl hesaplamaları yaparlar ve sizin RAM'de değişkenlere koyduğunuz her şeyi yüklerler.

<img src="/img/deployment/concepts/process-ram.drawio.svg">

Elbette aynı makinede, uygulamanız dışında da muhtemelen **başka process**'ler çalışır.

İlginç bir detay: Her process'in kullandığı **CPU** yüzdesi zaman içinde çok **değişken** olabilir; ancak **bellek (RAM)** genellikle az çok **stabil** kalır.

Eğer API'niz her seferinde benzer miktarda hesaplama yapıyorsa ve çok sayıda client'ınız varsa, **CPU kullanımı** da muhtemelen *stabil olur* (hızlı hızlı sürekli yükselip alçalmak yerine).

### Replikasyon Araçları ve Stratejileri Örnekleri { #examples-of-replication-tools-and-strategies }

Bunu başarmak için farklı yaklaşımlar olabilir. Sonraki bölümlerde, örneğin Docker ve container'lar konuşurken, belirli stratejileri daha detaylı anlatacağım.

Dikkate almanız gereken ana kısıt şudur: **public IP** üzerindeki **port**'u yöneten **tek** bir bileşen olmalı. Sonrasında bu bileşenin, replikasyonla çoğaltılmış **process/worker**'lara iletişimi **aktarmanın** bir yoluna sahip olması gerekir.

Olası kombinasyonlar ve stratejiler:

* `--workers` ile **Uvicorn**
    * Bir Uvicorn **process manager** **IP** ve **port** üzerinde dinler ve **birden fazla Uvicorn worker process** başlatır.
* **Kubernetes** ve diğer dağıtık **container sistemleri**
    * **Kubernetes** katmanında bir şey **IP** ve **port** üzerinde dinler. Replikasyon, her birinde **tek bir Uvicorn process** çalışan **birden fazla container** ile yapılır.
* Bunu sizin yerinize yapan **cloud service**'ler
    * Cloud service muhtemelen **replikasyonu sizin yerinize yönetir**. Size çalıştırılacak **bir process** veya kullanılacak bir **container image** tanımlama imkânı verebilir; her durumda büyük ihtimalle **tek bir Uvicorn process** olur ve bunu çoğaltmaktan cloud service sorumlu olur.

/// tip | İpucu

**Container**, Docker veya Kubernetes ile ilgili bazı maddeler şimdilik çok anlamlı gelmiyorsa dert etmeyin.

Container image'ları, Docker, Kubernetes vb. konuları ilerideki bir bölümde daha detaylı anlatacağım: [Container'larda FastAPI - Docker](docker.md){.internal-link target=_blank}.

///

## Başlatmadan Önceki Adımlar { #previous-steps-before-starting }

Uygulamanızı **başlatmadan önce** bazı adımlar yapmak isteyeceğiniz birçok durum vardır.

Örneğin **database migrations** çalıştırmak isteyebilirsiniz.

Ancak çoğu durumda, bu adımları yalnızca **bir kez** çalıştırmak istersiniz.

Bu yüzden, uygulamayı başlatmadan önce bu **ön adımları** çalıştıracak **tek bir process** olmasını istersiniz.

Ve daha sonra uygulamanın kendisi için **birden fazla process** (birden fazla worker) başlatsanız bile, bu ön adımları çalıştıranın *yine* tek process olduğundan emin olmalısınız. Bu adımlar **birden fazla process** tarafından çalıştırılsaydı, işi **paralel** şekilde tekrarlarlardı. Adımlar database migration gibi hassas bir şeyse, birbirleriyle çakışıp çatışma çıkarabilirler.

Elbette bazı durumlarda ön adımları birden fazla kez çalıştırmak sorun değildir; bu durumda yönetmesi çok daha kolay olur.

/// tip | İpucu

Ayrıca, kurulumunuza bağlı olarak bazı durumlarda uygulamanızı başlatmadan önce **hiç ön adıma ihtiyaç duymayabilirsiniz**.

Bu durumda bunların hiçbirini düşünmeniz gerekmez. 🤷

///

### Ön Adımlar için Strateji Örnekleri { #examples-of-previous-steps-strategies }

Bu konu, **sisteminizi nasıl deploy ettiğinize** çok bağlıdır ve muhtemelen programları nasıl başlattığınız, restart'ları nasıl yönettiğiniz vb. ile bağlantılıdır.

Bazı olası fikirler:

* Kubernetes'te, app container'ınızdan önce çalışan bir "Init Container"
* Ön adımları çalıştırıp sonra uygulamanızı başlatan bir bash script
    * Yine de o bash script'i başlatmak/restart etmek, hataları tespit etmek vb. için bir mekanizmaya ihtiyacınız olur.

/// tip | İpucu

Bunu container'larla nasıl yapabileceğinize dair daha somut örnekleri ilerideki bir bölümde anlatacağım: [Container'larda FastAPI - Docker](docker.md){.internal-link target=_blank}.

///

## Kaynak Kullanımı { #resource-utilization }

Server(lar)ınız bir **kaynaktır**. Programlarınızla CPU'lardaki hesaplama zamanını ve mevcut RAM belleğini tüketebilir veya **kullanabilirsiniz**.

Sistem kaynaklarının ne kadarını tüketmek/kullanmak istersiniz? "Az" demek kolaydır; ancak pratikte hedef genellikle **çökmeden mümkün olduğunca fazla** kullanmaktır.

3 server için para ödüyor ama onların RAM ve CPU'sunun yalnızca küçük bir kısmını kullanıyorsanız, muhtemelen **para israf ediyorsunuz** 💸 ve muhtemelen **elektrik tüketimini** de gereksiz yere artırıyorsunuz 🌎 vb.

Bu durumda 2 server ile devam edip onların kaynaklarını (CPU, bellek, disk, ağ bant genişliği vb.) daha yüksek oranlarda kullanmak daha iyi olabilir.

Öte yandan, 2 server'ınız var ve CPU ile RAM'in **%100**'ünü kullanıyorsanız, bir noktada bir process daha fazla bellek ister; server diski "bellek" gibi kullanmak zorunda kalır (binlerce kat daha yavaş olabilir) ya da hatta **crash** edebilir. Ya da bir process bir hesaplama yapmak ister ve CPU tekrar boşalana kadar beklemek zorunda kalır.

Bu senaryoda **bir server daha** eklemek ve bazı process'leri orada çalıştırmak daha iyi olur; böylece hepsinin **yeterli RAM'i ve CPU zamanı** olur.

Ayrıca, herhangi bir sebeple API'nizde bir kullanım **spike**'ı olma ihtimali de vardır. Belki viral olur, belki başka servisler veya bot'lar kullanmaya başlar. Bu durumlarda güvende olmak için ekstra kaynak isteyebilirsiniz.

Hedef olarak **keyfi bir sayı** belirleyebilirsiniz; örneğin kaynak kullanımını **%50 ile %90 arasında** tutmak gibi. Önemli olan, bunların muhtemelen ölçmek isteyeceğiniz ve deployment'larınızı ayarlamak için kullanacağınız ana metrikler olmasıdır.

Server'ınızda CPU ve RAM kullanımını veya her process'in ne kadar kullandığını görmek için `htop` gibi basit araçları kullanabilirsiniz. Ya da server'lar arasında dağıtık çalışan daha karmaşık monitoring araçları kullanabilirsiniz.

## Özet { #recap }

Uygulamanızı nasıl deploy edeceğinize karar verirken aklınızda tutmanız gereken ana kavramların bazılarını okudunuz:

* Güvenlik - HTTPS
* Startup'ta çalıştırma
* Yeniden başlatmalar
* Replikasyon (çalışan process sayısı)
* Bellek
* Başlatmadan önceki adımlar

Bu fikirleri ve nasıl uygulayacağınızı anlamak, deployment'larınızı yapılandırırken ve ince ayar yaparken ihtiyaç duyacağınız sezgiyi kazanmanızı sağlamalıdır. 🤓

Sonraki bölümlerde, izleyebileceğiniz stratejilere dair daha somut örnekler paylaşacağım. 🚀
