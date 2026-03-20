# HTTPS Hakkında { #about-https }

HTTPS’in sadece "açık" ya da "kapalı" olan bir şey olduğunu düşünmek kolaydır.

Ancak bundan çok daha karmaşıktır.

/// tip | İpucu

Aceleniz varsa veya çok da önemsemiyorsanız, her şeyi farklı tekniklerle adım adım kurmak için sonraki bölümlere geçin.

///

Bir kullanıcı gözüyle **HTTPS’in temellerini öğrenmek** için [https://howhttps.works/](https://howhttps.works/) adresine bakın.

Şimdi de **geliştirici perspektifinden**, HTTPS hakkında düşünürken akılda tutulması gereken birkaç nokta:

* HTTPS için **server**’ın, **üçüncü bir taraf** tarafından verilen **"sertifikalara"** sahip olması gerekir.
    * Bu sertifikalar aslında üçüncü tarafça "üretilmez", üçüncü taraftan **temin edilir**.
* Sertifikaların bir **geçerlilik süresi** vardır.
    * Süresi **dolar**.
    * Sonrasında **yenilenmeleri**, üçüncü taraftan **yeniden temin edilmeleri** gerekir.
* Bağlantının şifrelenmesi **TCP seviyesinde** gerçekleşir.
    * Bu, **HTTP’nin bir katman altıdır**.
    * Dolayısıyla **sertifika ve şifreleme** işlemleri **HTTP’den önce** yapılır.
* **TCP "domain"leri bilmez**. Yalnızca IP adreslerini bilir.
    * İstenen **spesifik domain** bilgisi **HTTP verisinin** içindedir.
* **HTTPS sertifikaları** belirli bir **domain**’i "sertifikalandırır"; ancak protokol ve şifreleme TCP seviyesinde, hangi domain ile çalışıldığı **henüz bilinmeden** gerçekleşir.
* **Varsayılan olarak** bu, IP adresi başına yalnızca **bir HTTPS sertifikası** olabileceği anlamına gelir.
    * Server’ınız ne kadar büyük olursa olsun ya da üzerindeki her uygulama ne kadar küçük olursa olsun.
    * Ancak bunun bir **çözümü** vardır.
* **TLS** protokolüne (TCP seviyesinde, HTTP’den önce şifrelemeyi yapan) eklenen **[<abbr title="Server Name Indication - Sunucu Adı Belirtimi">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)** adlı bir **extension** vardır.
    * Bu SNI extension’ı, tek bir server’ın (tek bir **IP adresiyle**) **birden fazla HTTPS sertifikası** kullanmasına ve **birden fazla HTTPS domain/uygulama** sunmasına izin verir.
    * Bunun çalışması için server üzerinde, **public IP adresini** dinleyen tek bir bileşenin (programın) server’daki **tüm HTTPS sertifikalarına** sahip olması gerekir.
* Güvenli bir bağlantı elde edildikten **sonra**, iletişim protokolü **hâlâ HTTP**’dir.
    * İçerikler, **HTTP protokolü** ile gönderiliyor olsa bile **şifrelenmiştir**.

Yaygın yaklaşım, server’da (makine, host vb.) çalışan **tek bir program/HTTP server** bulundurup **HTTPS ile ilgili tüm kısımları** yönetmektir: **şifreli HTTPS request**’leri almak, aynı server’da çalışan gerçek HTTP uygulamasına (bu örnekte **FastAPI** uygulaması) **şifresi çözülmüş HTTP request**’leri iletmek, uygulamadan gelen **HTTP response**’u almak, uygun **HTTPS sertifikası** ile **şifrelemek** ve **HTTPS** ile client’a geri göndermek. Bu server’a çoğu zaman **[TLS Termination Proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy)** denir.

TLS Termination Proxy olarak kullanabileceğiniz seçeneklerden bazıları:

* Traefik (sertifika yenilemelerini de yönetebilir)
* Caddy (sertifika yenilemelerini de yönetebilir)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Let's Encrypt’ten önce bu **HTTPS sertifikaları**, güvenilen üçüncü taraflar tarafından satılırdı.

Bu sertifikalardan birini temin etme süreci zahmetliydi, epey evrak işi gerektirirdi ve sertifikalar oldukça pahalıydı.

Sonra **[Let's Encrypt](https://letsencrypt.org/)** ortaya çıktı.

Linux Foundation’ın bir projesidir. **HTTPS sertifikalarını ücretsiz** ve otomatik bir şekilde sağlar. Bu sertifikalar tüm standart kriptografik güvenliği kullanır ve kısa ömürlüdür (yaklaşık 3 ay). Bu yüzden, ömürleri kısa olduğu için **güvenlik aslında daha iyidir**.

Domain’ler güvenli şekilde doğrulanır ve sertifikalar otomatik üretilir. Bu sayede sertifikaların yenilenmesini otomatikleştirmek de mümkün olur.

Amaç, bu sertifikaların temin edilmesi ve yenilenmesini otomatikleştirerek **ücretsiz, kalıcı olarak güvenli HTTPS** sağlamaktır.

## Geliştiriciler İçin HTTPS { #https-for-developers }

Burada, bir HTTPS API’nin adım adım nasıl görünebileceğine dair, özellikle geliştiriciler için önemli fikirlere odaklanan bir örnek var.

### Domain Adı { #domain-name }

Muhtemelen her şey, bir **domain adı** **temin etmenizle** başlar. Sonra bunu bir DNS server’ında (muhtemelen aynı cloud provider’ınızda) yapılandırırsınız.

Muhtemelen bir cloud server (virtual machine) ya da benzeri bir şey alırsınız ve bunun <dfn title="Zamanla değişmeyen. Dinamik olmayan.">sabit</dfn> bir **public IP adresi** olur.

DNS server(lar)ında, bir kaydı ("`A record`") **domain**’inizi server’ınızın **public IP adresine** yönlendirecek şekilde yapılandırırsınız.

Bunu büyük olasılıkla ilk kurulumda, sadece bir kez yaparsınız.

/// tip | İpucu

Bu Domain Adı kısmı HTTPS’ten çok daha önce gelir. Ancak her şey domain ve IP adresine bağlı olduğu için burada bahsetmeye değer.

///

### DNS { #dns }

Şimdi gerçek HTTPS parçalarına odaklanalım.

Önce tarayıcı, bu örnekte `someapp.example.com` olan domain için **IP**’nin ne olduğunu **DNS server**’larına sorar.

DNS server’ları tarayıcıya belirli bir **IP adresini** kullanmasını söyler. Bu, DNS server’larında yapılandırdığınız ve server’ınızın kullandığı public IP adresidir.

<img src="/img/deployment/https/https01.drawio.svg">

### TLS Handshake Başlangıcı { #tls-handshake-start }

Tarayıcı daha sonra bu IP adresiyle **443 portu** (HTTPS portu) üzerinden iletişim kurar.

İletişimin ilk kısmı, client ile server arasında bağlantıyı kurmak ve hangi kriptografik anahtarların kullanılacağına karar vermek vb. içindir.

<img src="/img/deployment/https/https02.drawio.svg">

Client ile server arasındaki, TLS bağlantısını kurmaya yönelik bu etkileşime **TLS handshake** denir.

### SNI Extension’ı ile TLS { #tls-with-sni-extension }

Server’da, belirli bir **IP adresindeki** belirli bir **portu** dinleyen **yalnızca bir process** olabilir. Aynı IP adresinde başka portları dinleyen başka process’ler olabilir, ancak IP+port kombinasyonu başına yalnızca bir tane olur.

TLS (HTTPS) varsayılan olarak `443` portunu kullanır. Yani ihtiyaç duyacağımız port budur.

Bu portu yalnızca bir process dinleyebileceği için, bunu yapacak process **TLS Termination Proxy** olur.

TLS Termination Proxy, bir ya da daha fazla **TLS sertifikasına** (HTTPS sertifikası) erişebilir.

Yukarıda bahsettiğimiz **SNI extension**’ını kullanarak TLS Termination Proxy, bu bağlantı için elindeki TLS (HTTPS) sertifikalarından hangisini kullanacağını kontrol eder; client’ın beklediği domain ile eşleşen sertifikayı seçer.

Bu örnekte `someapp.example.com` sertifikasını kullanır.

<img src="/img/deployment/https/https03.drawio.svg">

Client, bu TLS sertifikasını üreten kuruluşa zaten **güvenir** (bu örnekte Let's Encrypt; birazdan ona da geleceğiz). Bu sayede sertifikanın geçerli olduğunu **doğrulayabilir**.

Ardından client ve TLS Termination Proxy, sertifikayı kullanarak **TCP iletişiminin geri kalanını nasıl şifreleyeceklerine** karar verir. Böylece **TLS Handshake** kısmı tamamlanır.

Bundan sonra client ve server arasında **şifreli bir TCP bağlantısı** vardır; TLS’in sağladığı şey budur. Sonra bu bağlantıyı kullanarak gerçek **HTTP iletişimini** başlatabilirler.

Ve **HTTPS** de tam olarak budur: şifrelenmemiş bir TCP bağlantısı yerine, **güvenli bir TLS bağlantısının içinde** düz **HTTP**’dir.

/// tip | İpucu

Şifrelemenin HTTP seviyesinde değil, **TCP seviyesinde** gerçekleştiğine dikkat edin.

///

### HTTPS Request { #https-request }

Artık client ile server (özellikle tarayıcı ile TLS Termination Proxy) arasında **şifreli bir TCP bağlantısı** olduğuna göre, **HTTP iletişimi** başlayabilir.

Dolayısıyla client bir **HTTPS request** gönderir. Bu, şifreli bir TLS bağlantısı üzerinden giden bir HTTP request’tir.

<img src="/img/deployment/https/https04.drawio.svg">

### Request’in Şifresini Çözme { #decrypt-the-request }

TLS Termination Proxy, üzerinde anlaşılan şifrelemeyi kullanarak **request’in şifresini çözer** ve **düz (şifresi çözülmüş) HTTP request**’i uygulamayı çalıştıran process’e iletir (ör. FastAPI uygulamasını çalıştıran Uvicorn process’i).

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP Response { #http-response }

Uygulama request’i işler ve TLS Termination Proxy’ye **düz (şifrelenmemiş) bir HTTP response** gönderir.

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS Response { #https-response }

TLS Termination Proxy daha sonra response’u, daha önce üzerinde anlaşılan kriptografi ile (başlangıcı `someapp.example.com` sertifikasına dayanan) **şifreler** ve tarayıcıya geri gönderir.

Sonrasında tarayıcı response’un geçerli olduğunu ve doğru kriptografik anahtarla şifrelendiğini doğrular vb. Ardından **response’un şifresini çözer** ve işler.

<img src="/img/deployment/https/https07.drawio.svg">

Client (tarayıcı), response’un doğru server’dan geldiğini bilir; çünkü daha önce **HTTPS sertifikası** ile üzerinde anlaştıkları kriptografiyi kullanmaktadır.

### Birden Fazla Uygulama { #multiple-applications }

Aynı server’da (veya server’larda) örneğin başka API programları ya da bir veritabanı gibi **birden fazla uygulama** olabilir.

Belirli IP ve port kombinasyonunu yalnızca bir process yönetebilir (örneğimizde TLS Termination Proxy). Ancak diğer uygulamalar/process’ler, aynı **public IP + port kombinasyonunu** kullanmaya çalışmadıkları sürece server(lar)da çalışabilir.

<img src="/img/deployment/https/https08.drawio.svg">

Bu şekilde TLS Termination Proxy, birden fazla uygulama için **birden fazla domain**’in HTTPS ve sertifika işlerini yönetebilir ve her durumda request’leri doğru uygulamaya iletebilir.

### Sertifika Yenileme { #certificate-renewal }

Gelecekte bir noktada, her sertifikanın süresi **dolar** (temin edildikten yaklaşık 3 ay sonra).

Ardından başka bir program (bazı durumlarda ayrı bir programdır, bazı durumlarda aynı TLS Termination Proxy olabilir) Let's Encrypt ile konuşup sertifika(ları) yeniler.

<img src="/img/deployment/https/https.drawio.svg">

**TLS sertifikaları** bir IP adresiyle değil, **domain adıyla ilişkilidir**.

Bu yüzden sertifikaları yenilemek için, yenileme programı otoriteye (Let's Encrypt) gerçekten o domain’i **"sahiplendiğini" ve kontrol ettiğini** **kanıtlamalıdır**.

Bunu yapmak ve farklı uygulama ihtiyaçlarını karşılamak için birden fazla yöntem vardır. Yaygın yöntemlerden bazıları:

* Bazı **DNS kayıtlarını değiştirmek**.
    * Bunun için yenileme programının DNS provider API’lerini desteklemesi gerekir. Dolayısıyla kullandığınız DNS provider’a bağlı olarak bu seçenek mümkün de olabilir, olmayabilir de.
* Domain ile ilişkili public IP adresinde **server olarak çalışmak** (en azından sertifika temin sürecinde).
    * Yukarıda söylediğimiz gibi, belirli bir IP ve portu yalnızca bir process dinleyebilir.
    * Bu, aynı TLS Termination Proxy’nin sertifika yenileme sürecini de yönetmesinin neden çok faydalı olduğunun sebeplerinden biridir.
    * Aksi halde TLS Termination Proxy’yi kısa süreliğine durdurmanız, sertifikaları temin etmek için yenileme programını başlatmanız, sonra bunları TLS Termination Proxy ile yapılandırmanız ve ardından TLS Termination Proxy’yi tekrar başlatmanız gerekebilir. Bu ideal değildir; çünkü TLS Termination Proxy kapalıyken uygulama(lar)ınıza erişilemez.

Uygulamayı servis etmeye devam ederken tüm bu yenileme sürecini yönetebilmek, TLS sertifikalarını doğrudan uygulama server’ıyla (örn. Uvicorn) kullanmak yerine, TLS Termination Proxy ile HTTPS’i yönetecek **ayrı bir sistem** istemenizin başlıca nedenlerinden biridir.

## Proxy Forwarded Headers { #proxy-forwarded-headers }

HTTPS’i bir proxy ile yönetirken, **application server**’ınız (örneğin FastAPI CLI üzerinden Uvicorn) HTTPS süreci hakkında hiçbir şey bilmez; **TLS Termination Proxy** ile düz HTTP üzerinden iletişim kurar.

Bu **proxy** normalde request’i **application server**’a iletmeden önce, request’in proxy tarafından **forward** edildiğini application server’a bildirmek için bazı HTTP header’larını anlık olarak ekler.

/// note | Teknik Detaylar

Proxy header’ları şunlardır:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

Buna rağmen **application server**, güvenilen bir **proxy** arkasında olduğunu bilmediği için varsayılan olarak bu header’lara güvenmez.

Ancak **application server**’ı, **proxy**’nin gönderdiği *forwarded* header’larına güvenecek şekilde yapılandırabilirsiniz. FastAPI CLI kullanıyorsanız, hangi IP’lerden gelen *forwarded* header’lara güvenmesi gerektiğini söylemek için *CLI Option* `--forwarded-allow-ips` seçeneğini kullanabilirsiniz.

Örneğin **application server** yalnızca güvenilen **proxy**’den iletişim alıyorsa, yalnızca **proxy**’nin kullandığı IP’den request alacağı için `--forwarded-allow-ips="*"` ayarlayıp gelen tüm IP’lere güvenmesini sağlayabilirsiniz.

Bu sayede uygulama kendi public URL’inin ne olduğunu, HTTPS kullanıp kullanmadığını, domain’i vb. bilebilir.

Bu, örneğin redirect’leri doğru şekilde yönetmek için faydalıdır.

/// tip | İpucu

Bununla ilgili daha fazlasını [Bir Proxy Arkasında - Proxy Forwarded Headers'ı Etkinleştir](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers) dokümantasyonunda öğrenebilirsiniz.

///

## Özet { #recap }

**HTTPS** kullanmak çok önemlidir ve çoğu durumda oldukça **kritiktir**. Geliştirici olarak HTTPS etrafında harcadığınız çabanın büyük kısmı, aslında **bu kavramları** ve nasıl çalıştıklarını **anlamaktır**.

Ancak **geliştiriciler için HTTPS**’in temel bilgilerini öğrendikten sonra, her şeyi basitçe yönetmek için farklı araçları kolayca birleştirip yapılandırabilirsiniz.

Sonraki bölümlerin bazılarında, **FastAPI** uygulamaları için **HTTPS**’i nasıl kuracağınıza dair birkaç somut örnek göstereceğim. 🔒
