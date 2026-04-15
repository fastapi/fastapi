# Eşzamanlılık ve async / await { #concurrency-and-async-await }

*path operasyon fonksiyonları* için `async def` sözdizimi hakkında detaylar ve asenkron kod, eşzamanlılık (concurrency) ve paralellik üzerine arka plan bilgisi.

## Aceleniz mi var? { #in-a-hurry }

<abbr title="too long; didn't read - çok uzun; okumadım"><strong>TL;DR:</strong></abbr>

Eğer `await` ile çağırmanız gerektiğini söyleyen üçüncü taraf kütüphaneler kullanıyorsanız, örneğin:

```Python
results = await some_library()
```

O zaman *path operasyon fonksiyonlarınızı* aşağıdaki gibi `async def` ile tanımlayın:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Not

`await` yalnızca `async def` ile oluşturulan fonksiyonların içinde kullanılabilir.

///

---

Eğer bir veritabanı, bir API, dosya sistemi vb. ile iletişim kuran ve `await` desteği olmayan bir üçüncü taraf kütüphane kullanıyorsanız (bu şu anda çoğu veritabanı kütüphanesi için geçerlidir), o zaman *path operasyon fonksiyonlarınızı* normal olarak `def` ile tanımlayın:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Uygulamanız (bir şekilde) başka bir şeyle iletişim kurmak ve onun yanıtını beklemek zorunda değilse, içinde `await` kullanmanız gerekmese bile `async def` kullanın.

---

Emin değilseniz, normal `def` kullanın.

---

Not: *path operasyon fonksiyonlarınızda* `def` ve `async def`'i ihtiyacınız kadar karıştırabilirsiniz, her birini sizin için en iyi seçenekle tanımlayın. FastAPI onlar için doğru olanı yapacaktır.

Yukarıdaki durumların herhangi birinde FastAPI yine de asenkron olarak çalışır ve son derece hızlıdır.

Ancak yukarıdaki adımları izleyerek bazı performans optimizasyonları mümkün olur.

## Teknik Detaylar { #technical-details }

Python’un modern sürümleri, **`async` ve `await`** sözdizimiyle, **"coroutines"** denilen bir yapıyı kullanarak **"asenkron kod"** desteğine sahiptir.

Aşağıdaki bölümlerde bu ifadeyi parça parça ele alalım:

* **Asenkron Kod**
* **`async` ve `await`**
* **Coroutine'ler**

## Asenkron Kod { #asynchronous-code }

Asenkron kod, dilin 💬 bilgisayara / programa 🤖 kodun bir noktasında, bir yerde *başka bir şeyin* bitmesini beklemesi gerektiğini söylemesinin bir yoludur. Diyelim ki bu *başka şeye* "slow-file" 📝 diyoruz.

Bu sırada bilgisayar, "slow-file" 📝 biterken gidip başka işler yapabilir.

Sonra bilgisayar / program 🤖, ya tekrar beklediği için ya da o anda elindeki tüm işleri bitirdiğinde fırsat buldukça geri gelir. Ve beklediği görevlerden herhangi biri bittiyse, yapılması gerekenleri yapar.

Ardından, 🤖 ilk biten görevi alır (örneğin bizim "slow-file" 📝) ve onunla yapması gerekenlere devam eder.

Bu "başka bir şeyi beklemek" genelde işlemci ve RAM hızına kıyasla nispeten "yavaş" olan <abbr title="Input and Output - Giriş ve Çıkış">I/O</abbr> işlemlerine atıfta bulunur, örneğin şunları beklemek gibi:

* istemciden verinin ağ üzerinden gelmesi
* programınızın gönderdiği verinin ağ üzerinden istemciye ulaşması
* diskteki bir dosyanın içeriğinin sistem tarafından okunup programınıza verilmesi
* programınızın sisteme verdiği içeriğin diske yazılması
* uzak bir API işlemi
* bir veritabanı işleminin bitmesi
* bir veritabanı sorgusunun sonuç döndürmesi
* vb.

Çalışma süresi çoğunlukla <abbr title="Input and Output - Giriş ve Çıkış">I/O</abbr> işlemlerini beklemekle geçtiğinden, bunlara "I/O bound" işlemler denir.

"Bunun" asenkron" denmesinin sebebi, bilgisayarın / programın yavaş görevle "senkronize" olmak, görev tam bittiği anda orada olup görev sonucunu almak ve işe devam etmek için hiçbir şey yapmadan beklemek zorunda olmamasıdır.

Bunun yerine "asenkron" bir sistem olarak, görev bittiğinde, bilgisayarın / programın o sırada yaptığı işi bitirmesi için biraz (birkaç mikrosaniye) sırada bekleyebilir ve sonra sonuçları almak üzere geri dönüp onlarla çalışmaya devam edebilir.

"Senkron" (asenkronun tersi) için genelde "sıralı" terimi de kullanılır; çünkü bilgisayar / program, farklı bir göreve geçmeden önce tüm adımları sırayla izler, bu adımlar beklemeyi içerse bile.

### Eşzamanlılık ve Burgerler { #concurrency-and-burgers }

Yukarıda anlatılan **asenkron** kod fikrine bazen **"eşzamanlılık"** (concurrency) da denir. **"Paralellik"**ten (parallelism) farklıdır.

**Eşzamanlılık** ve **paralellik**, "aynı anda az çok birden fazla şeyin olması" ile ilgilidir.

Ama *eşzamanlılık* ve *paralellik* arasındaki ayrıntılar oldukça farklıdır.

Farkı görmek için burgerlerle ilgili şu hikayeyi hayal edin:

### Eşzamanlı Burgerler { #concurrent-burgers }

Aşkınla fast food almaya gidiyorsun, kasiyer senden önceki insanların siparişlerini alırken sıraya giriyorsun. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Sonra sıra size geliyor, sen ve aşkın için 2 çok havalı burger sipariş ediyorsun. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Kasiyer, mutfaktaki aşçıya burgerlerini hazırlamaları gerektiğini söylüyor (o an önceki müşterilerin burgerlerini hazırlıyor olsalar bile).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Ödeme yapıyorsun. 💸

Kasiyer sana sıra numaranı veriyor.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Beklerken aşkınla bir masa seçip oturuyorsunuz, uzun uzun sohbet ediyorsunuz (burgerler baya havalı ve hazırlanması biraz zaman alıyor).

Masada aşkınla otururken, burgerleri beklerken, o zamanı aşkının ne kadar harika, tatlı ve zeki olduğuna hayran kalarak geçirebilirsin ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Bekler ve sohbet ederken, ara ara tezgâhtaki numaraya bakıp sıranın size gelip gelmediğini kontrol ediyorsun.

Bir noktada, nihayet sıra size geliyor. Tezgâha gidiyor, burgerleri alıp masaya dönüyorsun.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Aşkınla burgerleri yiyip güzel vakit geçiriyorsunuz. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info | Bilgi

Harika çizimler: [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Bu hikâyede bilgisayar / program 🤖 olduğunu hayal et.

Sıradayken sadece boştasın 😴, sıranı bekliyorsun, çok "üretken" bir şey yapmıyorsun. Ama sorun yok, çünkü kasiyer sadece sipariş alıyor (hazırlamıyor), bu yüzden sıra hızlı ilerliyor.

Sıra sana geldiğinde gerçekten "üretken" işler yapıyorsun: menüyü işliyorsun, ne istediğine karar veriyorsun, aşkının seçimini alıyorsun, ödüyorsun, doğru para ya da kartı verdiğini kontrol ediyorsun, doğru ücretlendirildiğini kontrol ediyorsun, sipariş kalemlerinin doğru olduğunu kontrol ediyorsun, vb.

Ama sonra, burgerlerin hâlâ gelmemiş olsa da, kasiyerle olan işin "duraklatılıyor" ⏸, çünkü burgerlerin hazır olmasını 🕙 beklemen gerekiyor.

Fakat tezgâhtan uzaklaşıp masada sıra numaranla oturduğun için, dikkatinizi 🔀 aşkına çevirebilir, onunla "çalışmaya" ⏯ 🤓 odaklanabilirsin. Yani yine çok "üretken" bir şey yapıyorsun, aşkınla flört etmek gibi 😍.

Ardından kasiyer 💁, tezgâh ekranına numaranı koyarak "burgerleri bitirdim" diyor; ama numara seninki olduğunda çılgınca sıçramıyorsun. Sıra numaran sende, herkesin kendi numarası var; kimse burgerlerini çalamaz.

Bu yüzden aşkının hikâyeyi bitirmesini (mevcut işi ⏯ / işlenen görevi 🤓 bitirmesini) bekliyor, nazikçe gülümsüyor ve burgerleri almaya gittiğini söylüyorsun ⏸.

Sonra tezgâha 🔀 gidip artık bitmiş olan ilk göreve ⏯ dönüyor, burgerleri alıyor, teşekkür ediyor ve masaya getiriyorsun. Tezgâhla etkileşimin bu adımı / görevi böylece bitiyor ⏹. Bu da yeni bir görev olan "burgerleri yemek" 🔀 ⏯ görevini oluşturuyor, ama "burgerleri almak" görevi tamamlandı ⏹.

### Paralel Burgerler { #parallel-burgers }

Şimdi bunların "Eşzamanlı Burgerler" değil, "Paralel Burgerler" olduğunu hayal edelim.

Aşkınla paralel fast food almaya gidiyorsun.

Aynı anda aşçı da olan birden fazla (8 diyelim) kasiyerin, senden önceki insanların siparişlerini aldığı bir sırada bekliyorsun.

Senden önceki herkes, tezgâhtan ayrılmadan önce burgerlerinin hazırlanmasını bekliyor; çünkü 8 kasiyerin her biri bir sonraki siparişe geçmeden önce burgeri hemen gidip hazırlıyor.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Sonunda sıra size geliyor, sen ve aşkın için 2 çok havalı burger siparişi veriyorsun.

Ödüyorsun 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Kasiyer mutfağa gidiyor.

Tezgâhın önünde ayakta 🕙 bekliyorsun; sıra numarası olmadığından, burgerlerini senden önce kimsenin almaması için orada durman gerekiyor.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Sen ve aşkın, kimsenin önünüze geçip burgerler gelince almaması için meşgul olduğunuzdan, aşkına dikkatini veremiyorsun. 😞

Bu "senkron" bir iştir; kasiyer/aşçı 👨‍🍳 ile "senkronize"sin. 🕙 Beklemen ve kasiyer/aşçı 👨‍🍳 burgerleri bitirip sana verdiği anda tam orada olman gerekir; yoksa bir başkası alabilir.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Sonra kasiyer/aşçı 👨‍🍳, uzun süre tezgâhın önünde 🕙 bekledikten sonra nihayet burgerlerinle geri geliyor.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Burgerleri alıyor ve aşkınla masaya gidiyorsun.

Sadece yiyorsunuz ve iş bitiyor. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Vaktin çoğu tezgâhın önünde 🕙 beklemekle geçtiğinden, pek konuşma ya da flört olmadı. 😞

/// info | Bilgi

Harika çizimler: [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Bu paralel burger senaryosunda, ikiniz (sen ve aşkın) iki işlemcili bir bilgisayar / programsınız 🤖; ikiniz de uzun süre tezgâhta "bekleme" işine 🕙 dikkat ⏯ ayırıyorsunuz.

Fast food dükkânında 8 işlemci var (kasiyer/aşçılar). Eşzamanlı burger dükkânında yalnızca 2 kişi olabilir (bir kasiyer ve bir aşçı).

Ama yine de nihai deneyim pek iyi değil. 😞

---

Bu, burgerler için paralel karşılık gelen hikâye olurdu. 🍔

Daha "gerçek hayat" bir örnek için, bir banka hayal edin.

Yakın zamana kadar, bankaların çoğunda birden çok gişe memuru 👨‍💼👨‍💼👨‍💼👨‍💼 ve uzun bir sıra 🕙🕙🕙🕙🕙🕙🕙🕙 vardı.

Tüm gişe memurları bir müşteriyle tüm işi yapar, sonra sıradakiyle 👨‍💼⏯.

Ve sıranı kaybetmemek için uzun süre 🕙 kuyrukta beklemen gerekir.

Muhtemelen, bankada 🏦 işlerini hallederken aşkını 😍 yanında götürmek istemezsin.

### Burger Sonucu { #burger-conclusion }

"Fast food burgerleri ve aşkın" senaryosunda, çok fazla bekleme 🕙 olduğundan, eşzamanlı bir sistem ⏸🔀⏯ çok daha mantıklıdır.

Bu, çoğu web uygulaması için de geçerlidir.

Çok fazla kullanıcı vardır; ancak sunucunuz, iyi olmayan bağlantılarından gelen istekleri 🕙 bekler.

Ve sonra yanıtların geri gelmesini yine 🕙 bekler.

Bu "beklemeler" 🕙 mikrosaniyelerle ölçülür; ama hepsi toplandığında sonuçta oldukça fazla bekleme olur.

Bu yüzden web API’leri için asenkron ⏸🔀⏯ kod kullanmak çok mantıklıdır.

Bu tür asenkronluk, NodeJS’i popüler yapan şeydir (NodeJS paralel olmasa bile) ve Go dilinin gücüdür.

Ve **FastAPI** ile elde ettiğiniz performans seviyesi de budur.

Ayrıca, aynı anda hem paralellik hem de asenkronluk kullanabildiğiniz için, test edilen çoğu NodeJS framework’ünden daha yüksek ve C’ye daha yakın derlenen bir dil olan Go ile başa baş performans elde edersiniz [(hepsi Starlette sayesinde)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### Eşzamanlılık paralellikten daha mı iyi? { #is-concurrency-better-than-parallelism }

Hayır! Hikâyenin özü bu değil.

Eşzamanlılık paralellikten farklıdır. Ve çok fazla bekleme içeren **belirli** senaryolarda daha iyidir. Bu nedenle, genellikle web uygulaması geliştirme için paralellikten çok daha iyidir. Ama her şey için değil.

Bunu dengelemek için, şu kısa hikâyeyi hayal edin:

> Büyük, kirli bir evi temizlemen gerekiyor.

*Evet, tüm hikâye bu kadar*.

---

Hiçbir yerde 🕙 bekleme yok; sadece evin birden fazla yerinde yapılacak çok iş var.

Hamburger örneğindeki gibi dönüşlerle ilerleyebilirsin, önce salon, sonra mutfak; ama hiçbir şey 🕙 beklemediğin için, sadece temizlik yaptığından, dönüşlerin hiçbir etkisi olmaz.

Dönüşlerle ya da dönüşsüz (eşzamanlılık) bitirmek aynı zaman alır ve aynı miktarda iş yapmış olursun.

Ama bu durumda, 8 eski kasiyer/aşçı—yeni temizlikçiyi getirip her birine (artı sana) evin bir bölümünü versen, fazladan yardımla tüm işleri **paralel** yaparak çok daha çabuk bitirebilirdin.

Bu senaryoda, her bir temizlikçi (sen dâhil) birer işlemci olur ve kendi iş payını yapar.

Ve yürütme süresinin çoğu gerçek işten (bekleme yerine) oluştuğu ve bilgisayardaki işi bir <abbr title="Central Processing Unit - Merkezi İşlem Birimi">CPU</abbr> yaptığı için, bu sorunlara "CPU bound" denir.

---

CPU’ya bağlı işlemlerin yaygın örnekleri, karmaşık matematiksel işlem gerektiren iş yükleridir.

Örneğin:

* **Ses** veya **görüntü işleme**.
* **Bilgisayar görüsü**: bir görüntü milyonlarca pikselden oluşur, her pikselin 3 değeri / rengi vardır; işleme genellikle bu pikseller üzerinde aynı anda bir şeyler hesaplamayı gerektirir.
* **Makine Öğrenimi**: genellikle çok sayıda "matris" ve "vektör" çarpımı gerekir. Sayılar içeren devasa bir elektronik tabloyu ve hepsini aynı anda çarpmayı düşünün.
* **Derin Öğrenme**: Makine Öğreniminin bir alt alanıdır, dolayısıyla aynısı geçerlidir. Sadece çarpılacak tek bir sayı tablosu değil, kocaman bir sayı kümesi vardır ve çoğu durumda bu modelleri kurmak ve/veya kullanmak için özel işlemciler kullanırsınız.

### Eşzamanlılık + Paralellik: Web + Makine Öğrenimi { #concurrency-parallelism-web-machine-learning }

**FastAPI** ile web geliştirmede çok yaygın olan eşzamanlılıktan (NodeJS’in başlıca cazibesiyle aynı) yararlanabilirsiniz.

Ama ayrıca **CPU’ya bağlı** iş yükleri (Makine Öğrenimi sistemlerindeki gibi) için paralellik ve çoklu işlemden (paralel çalışan birden çok işlem) de yararlanabilirsiniz.

Buna ek olarak Python’un **Veri Bilimi**, Makine Öğrenimi ve özellikle Derin Öğrenme için ana dil olması, FastAPI’yi Veri Bilimi / Makine Öğrenimi web API’leri ve uygulamaları için çok iyi bir seçenek yapar.

Production’da bu paralelliği nasıl sağlayacağınızı görmek için [Deployment](deployment/index.md) bölümüne bakın.

## `async` ve `await` { #async-and-await }

Python’un modern sürümleri, asenkron kodu tanımlamak için oldukça sezgisel bir yol sunar. Bu sayede kod normal "sıralı" kod gibi görünür ve doğru anlarda sizin yerinize "beklemeyi" yapar.

Sonuçları vermeden önce bekleme gerektiren ve bu yeni Python özelliklerini destekleyen bir işlem olduğunda, şöyle kodlayabilirsiniz:

```Python
burgers = await get_burgers(2)
```

Buradaki kilit nokta `await`. Python’a, sonuçları `burgers` değişkenine koymadan önce `get_burgers(2)` çalışmasının bitmesini 🕙 beklemesi ⏸ gerektiğini söyler. Böylece Python, bu arada başka bir şey 🔀 ⏯ yapabileceğini bilir (ör. başka bir request almak gibi).

`await`’in çalışabilmesi için, bu asenkronluğu destekleyen bir fonksiyonun içinde olması gerekir. Bunu yapmak için fonksiyonu `async def` ile tanımlayın:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Burgerleri yaratmak için bazı asenkron işler yap
    return burgers
```

...`def` yerine:

```Python hl_lines="2"
# Bu asenkron değildir
def get_sequential_burgers(number: int):
    # Burgerleri yaratmak için bazı sıralı işler yap
    return burgers
```

`async def` ile Python, bu fonksiyonun içinde `await` ifadelerinin olabileceğini bilir ve bu fonksiyonun yürütülmesini "duraklatıp" ⏸ başka bir şey yapabileceğini 🔀, sonra geri dönebileceğini anlar.

`async def` fonksiyonunu çağırmak istediğinizde, onu "await" etmeniz gerekir. Yani şu çalışmaz:

```Python
# Bu çalışmaz, çünkü get_burgers şöyle tanımlandı: async def
burgers = get_burgers(2)
```

---

Dolayısıyla, `await` ile çağrılabileceğini söyleyen bir kütüphane kullanıyorsanız, onu kullanan *path operasyon fonksiyonunu* `async def` ile oluşturmanız gerekir, örneğin:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Daha teknik detaylar { #more-technical-details }

`await`’in yalnızca `async def` ile tanımlanan fonksiyonların içinde kullanılabildiğini fark etmiş olabilirsiniz.

Aynı zamanda, `async def` ile tanımlanan fonksiyonların da "await" edilmesi gerekir. Yani `async def` ile tanımlanan fonksiyonlar yalnızca `async def` ile tanımlanan fonksiyonların içinde çağrılabilir.

Peki, tavuk-yumurta meselesi: ilk `async` fonksiyon nasıl çağrılır?

**FastAPI** ile çalışıyorsanız bunu dert etmenize gerek yok; çünkü o "ilk" fonksiyon sizin *path operasyon fonksiyonunuz* olacaktır ve FastAPI doğru olanı yapmasını bilir.

Ama FastAPI olmadan da `async` / `await` kullanmak isterseniz, bunu da yapabilirsiniz.

### Kendi async kodunuzu yazın { #write-your-own-async-code }

Starlette (ve **FastAPI**) [AnyIO](https://anyio.readthedocs.io/en/stable/) üzerine kuruludur; bu sayede Python standart kütüphanesindeki [asyncio](https://docs.python.org/3/library/asyncio-task.html) ve [Trio](https://trio.readthedocs.io/en/stable/) ile uyumludur.

Özellikle, kendi kodunuzda daha gelişmiş desenler gerektiren ileri seviye eşzamanlılık kullanım senaryoları için doğrudan [AnyIO](https://anyio.readthedocs.io/en/stable/) kullanabilirsiniz.

Hatta FastAPI kullanmıyor olsanız bile, yüksek uyumluluk ve avantajları (ör. *structured concurrency*) için [AnyIO](https://anyio.readthedocs.io/en/stable/) ile kendi async uygulamalarınızı yazabilirsiniz.

AnyIO’nun üzerine, tür açıklamalarını biraz iyileştirmek ve daha iyi **otomatik tamamlama**, **satır içi hatalar** vb. elde etmek için ince bir katman olarak başka bir kütüphane daha oluşturdum. Ayrıca **kendi async kodunuzu** anlamanıza ve yazmanıza yardımcı olacak dostça bir giriş ve eğitim içerir: [Asyncer](https://asyncer.tiangolo.com/). Özellikle **async kodu normal** (bloklayan/senkron) **kodla birleştirmeniz** gerektiğinde faydalı olacaktır.

### Asenkron kodun diğer biçimleri { #other-forms-of-asynchronous-code }

`async` ve `await` kullanma tarzı, dilde nispeten yenidir.

Ama asenkron kodla çalışmayı çok daha kolaylaştırır.

Aynı (ya da neredeyse aynı) sözdizimi yakın zamanda modern JavaScript sürümlerine (Tarayıcı ve NodeJS) de eklendi.

Bundan önce, asenkron kodu ele almak oldukça daha karmaşık ve zordu.

Python’un önceki sürümlerinde thread’ler veya [Gevent](https://www.gevent.org/) kullanabilirdiniz. Ama kodu anlamak, hata ayıklamak ve üzerine düşünmek çok daha zordu.

NodeJS / Tarayıcı JavaScript’in önceki sürümlerinde "callback" kullanırdınız. Bu da "callback cehennemi"ne yol açardı.

## Coroutine'ler { #coroutines }

**Coroutine**, bir `async def` fonksiyonunun döndürdüğü şeye verilen süslü isimdir. Python bunun bir fonksiyona benzer bir şey olduğunu, bir noktada başlayıp biteceğini bilir; ama içinde bir `await` olduğunda dahili olarak duraklatılabileceğini ⏸ de bilir.

`async` ve `await` ile asenkron kod kullanmanın bu işlevselliği çoğu zaman "coroutine" kullanmak olarak özetlenir. Go’nun ana kilit özelliği olan "Goroutines" ile karşılaştırılabilir.

## Sonuç { #conclusion }

Yukarıdaki cümleyi tekrar görelim:

> Python’un modern sürümleri, **`async` ve `await`** sözdizimiyle, **"coroutines"** denilen bir yapıyı kullanarak **"asenkron kod"** desteğine sahiptir.

Artık daha anlamlı gelmeli. ✨

Bunların hepsi, FastAPI’ye (Starlette aracılığıyla) güç verir ve böylesine etkileyici bir performansa sahip olmasını sağlar.

## Çok Teknik Detaylar { #very-technical-details }

/// warning | Uyarı

Büyük ihtimalle burayı atlayabilirsiniz.

Bunlar, **FastAPI**’nin altında nasıl çalıştığına dair oldukça teknik ayrıntılardır.

Coroutine’ler, thread’ler, blocking vb. hakkında teknik bilginiz varsa ve FastAPI’nin `async def` ile normal `def` arasındaki farkı nasıl ele aldığını merak ediyorsanız, devam edin.

///

### Path Operasyon Fonksiyonları { #path-operation-functions }

Bir *path operasyon fonksiyonunu* `async def` yerine normal `def` ile tanımladığınızda, (sunucuyu bloklayacağından) doğrudan çağrılmak yerine, harici bir thread pool’da çalıştırılır ve ardından beklenir.

Yukarıda açıklanan şekilde çalışmayan başka bir async framework’ten geliyorsanız ve ufak bir performans kazancı (yaklaşık 100 nanosaniye) için yalnızca hesaplama yapan basit *path operasyon fonksiyonlarını* düz `def` ile tanımlamaya alışkınsanız, **FastAPI**’de etkinin tam tersi olacağını unutmayın. Bu durumlarda, *path operasyon fonksiyonlarınız* bloklayan <abbr title="Input/Output - Giriş/Çıkış: disk okuma veya yazma, ağ iletişimi.">I/O</abbr> yapan kod kullanmadıkça `async def` kullanmak daha iyidir.

Yine de her iki durumda da, **FastAPI**’nin önceki framework’ünüzden [hala daha hızlı](index.md#performance) (ya da en azından karşılaştırılabilir) olması muhtemeldir.

### Bağımlılıklar { #dependencies }

Aynısı [bağımlılıklar](tutorial/dependencies/index.md) için de geçerlidir. Bir bağımlılık `async def` yerine standart bir `def` fonksiyonuysa, harici thread pool’da çalıştırılır.

### Alt-bağımlılıklar { #sub-dependencies }

Birbirini gerektiren birden çok bağımlılık ve [alt-bağımlılık](tutorial/dependencies/sub-dependencies.md) olabilir (fonksiyon tanımlarının parametreleri olarak). Bazıları `async def` ile, bazıları normal `def` ile oluşturulmuş olabilir. Yine de çalışır ve normal `def` ile oluşturulanlar "await" edilmek yerine harici bir thread’de (thread pool’dan) çağrılır.

### Diğer yardımcı fonksiyonlar { #other-utility-functions }

Doğrudan çağırdığınız diğer yardımcı fonksiyonları normal `def` veya `async def` ile tanımlayabilirsiniz ve FastAPI onları çağırma biçiminizi etkilemez.

Bu, FastAPI’nin sizin için çağırdığı fonksiyonların tersidir: *path operasyon fonksiyonları* ve bağımlılıklar.

Yardımcı fonksiyonunuz `def` ile tanımlı normal bir fonksiyonsa, bir thread pool’da değil doğrudan (kodunuzda yazdığınız gibi) çağrılır; fonksiyon `async def` ile tanımlıysa kodunuzda çağırırken onu `await` etmelisiniz.

---

Yine, bunlar muhtemelen özellikle aradığınızda işinize yarayacak çok teknik ayrıntılardır.

Aksi hâlde, yukarıdaki bölümdeki yönergeler yeterlidir: <a href="#in-a-hurry">Aceleniz mi var?</a>.
