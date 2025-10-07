# Concurrency ve async / await

*path operasyon fonksiyonu* için `async def `sözdizimi,  asenkron kod, eşzamanlılık ve paralellik hakkında bazı ayrıntılar.

## Aceleniz mi var?

<abbr title="too long; didn't read"><strong>TL;DR:</strong></abbr>

Eğer `await` ile çağrılması gerektiğini belirten üçüncü taraf kütüphaneleri kullanıyorsanız, örneğin:

```Python
results = await some_library()
```

O zaman *path operasyon fonksiyonunu* `async def` ile tanımlayın örneğin:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Not

Sadece `async def` ile tanımlanan fonksiyonlar içinde `await` kullanabilirsiniz.

///

---

Eğer bir veritabanı, bir API, dosya sistemi vb. ile iletişim kuran bir üçüncü taraf bir kütüphane kullanıyorsanız ve `await` kullanımını desteklemiyorsa, (bu şu anda çoğu veritabanı kütüphanesi için geçerli bir durumdur), o zaman *path operasyon fonksiyonunuzu* `def` kullanarak normal bir şekilde tanımlayın, örneğin:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Eğer uygulamanız (bir şekilde) başka bir şeyle iletişim kurmak ve onun cevap vermesini beklemek zorunda değilse, `async def` kullanın.

---

Sadece bilmiyorsanız, normal `def` kullanın.

---

**Not**: *path operasyon fonksiyonlarınızda* `def` ve `async def`'i ihtiyaç duyduğunuz gibi karıştırabilir ve her birini sizin için en iyi seçeneği kullanarak tanımlayabilirsiniz. FastAPI onlarla doğru olanı yapacaktır.

Her neyse, yukarıdaki durumlardan herhangi birinde, FastAPI yine de asenkron olarak çalışacak ve son derece hızlı olacaktır.

Ancak yukarıdaki adımları takip ederek, bazı performans optimizasyonları yapılabilecektir.

## Teknik Detaylar

Python'un modern versiyonlarında **`async` ve `await`** sözdizimi ile **"coroutines"**  kullanan **"asenkron kod"** desteğine sahiptir.

Bu ifadeyi aşağıdaki bölümlerde daha da ayrıntılı açıklayalım:

* **Asenkron kod**
* **`async` ve `await`**
* **Coroutines**

## Asenkron kod

Asenkron kod programlama dilinin 💬 bilgisayara / programa 🤖 kodun bir noktasında, *başka bir kodun* bir yerde bitmesini 🤖 beklemesi gerektiğini söylemenin bir yoludur. Bu *başka koda* "slow-file" denir 📝.

Böylece, bu süreçte bilgisayar "slow-file" 📝 tamamlanırken gidip başka işler yapabilir.

Sonra bilgisayar / program 🤖 her fırsatı olduğunda o noktada yaptığı tüm işleri 🤖 bitirene kadar geri dönücek. Ve 🤖 yapması gerekeni yaparak, beklediği görevlerden herhangi birinin bitip bitmediğini görecek.

Ardından, 🤖 bitirmek için ilk görevi alır ("slow-file" 📝) ve onunla ne yapması gerekiyorsa onu devam ettirir.

Bu "başka bir şey için bekle" normalde, aşağıdakileri beklemek gibi (işlemcinin ve RAM belleğinin hızına kıyasla) nispeten "yavaş" olan <abbr title="Input ve Output (Giriş ve Çıkış)">I/O</abbr> işlemlerine atıfta bulunur:

* istemci tarafından ağ üzerinden veri göndermek
* ağ üzerinden istemciye gönderilen veriler
* sistem tarafından okunacak ve programınıza verilecek bir dosya içeriği
* programınızın diske yazılmak üzere sisteme verdiği dosya içerikleri
* uzak bir API işlemi
* bir veritabanı bitirme işlemi
* sonuçları döndürmek için bir veritabanı sorgusu
* vb.

Yürütme süresi çoğunlukla  <abbr title="Input ve Output (Giriş ve Çıkış)">I/O</abbr> işlemleri beklenerek tüketildiğinden bunlara "I/O bağlantılı" işlemler denir.

Buna "asenkron" denir, çünkü bilgisayar/program yavaş görevle "senkronize" olmak zorunda değildir, görevin tam olarak biteceği anı bekler, hiçbir şey yapmadan, görev sonucunu alabilmek ve çalışmaya devam edebilmek için .

Bunun yerine, "asenkron" bir sistem olarak, bir kez bittiğinde,  bilgisayarın / programın yapması gerekeni bitirmesi için biraz (birkaç mikrosaniye) sırada bekleyebilir ve ardından sonuçları almak için geri gelebilir ve onlarla çalışmaya devam edebilir.

"Senkron" ("asenkron"un aksine) için genellikle "sıralı" terimini de kullanırlar, çünkü bilgisayar/program, bu adımlar beklemeyi içerse bile, farklı bir göreve geçmeden önce tüm adımları sırayla izler.


### Eşzamanlılık (Concurrency) ve Burgerler


Yukarıda açıklanan bu **asenkron** kod fikrine bazen **"eşzamanlılık"** da denir. **"Paralellikten"** farklıdır.

**Eşzamanlılık** ve **paralellik**, "aynı anda az ya da çok olan farklı işler" ile ilgilidir.

Ancak *eşzamanlılık* ve *paralellik* arasındaki ayrıntılar oldukça farklıdır.


Farkı görmek için burgerlerle ilgili aşağıdaki hikayeyi hayal edin:

### Eşzamanlı Burgerler

<!-- Cinsiyetten bağımsız olan aşçı emojisi "🧑‍🍳" tarayıcılarda yeterince iyi görüntülenmiyor. Bu yüzden erken "👨‍🍳" ve kadın "👩‍🍳" aşçıları karışık bir şekilde kullanıcağım. -->

Aşkınla beraber 😍 dışarı hamburger yemeye çıktınız 🍔, kasiyer 💁 öndeki insanlardan sipariş alırken siz sıraya girdiniz.

Sıra sizde ve sen aşkın 😍 ve kendin için 2 çılgın hamburger 🍔 söylüyorsun.

Ödemeyi yaptın 💸.

Kasiyer 💁 mutfakdaki aşçıya 👨‍🍳 hamburgerleri 🍔 hazırlaması gerektiğini söyler ve aşçı bunu bilir (o an önceki müşterilerin siparişlerini hazırlıyor olsa bile).

Kasiyer 💁 size bir sıra numarası verir.

Beklerken askınla 😍 bir masaya oturur ve uzun bir süre konuşursunuz(Burgerleriniz çok çılgın olduğundan ve hazırlanması biraz zaman alıyor ✨🍔✨).

Hamburgeri beklerkenki zamanı 🍔, aşkının ne kadar zeki ve tatlı olduğuna hayran kalarak harcayabilirsin ✨😍✨.

Aşkınla 😍 konuşurken arada sıranın size gelip gelmediğini kontrol ediyorsun.

Nihayet sıra size geldi. Tezgaha gidip hamburgerleri 🍔kapıp masaya geri dönüyorsun.

Aşkınla hamburgerlerinizi yiyor 🍔 ve iyi vakit geçiriyorsunuz ✨.

---

Bu hikayedeki bilgisayar / program 🤖 olduğunuzu hayal edin.

Sırada beklerken boştasın 😴, sıranı beklerken herhangi bir "üretim" yapmıyorsun. Ama bu sıra hızlı çünkü kasiyer sadece siparişleri alıyor (onları hazırlamıyor), burada bir sıknıtı yok.

Sonra sıra size geldiğinde gerçekten "üretken" işler yapabilirsiniz 🤓, menüyü oku, ne istediğine larar ver, aşkının seçimini al 😍, öde 💸, doğru kartı çıkart, ödemeyi kontrol et, faturayı kontrol et, siparişin doğru olup olmadığını kontrol et, vb.

Ama hamburgerler 🍔 hazır olmamasına rağmen Kasiyer 💁 ile işiniz "duraklıyor" ⏸, çünkü hamburgerlerin hazır olmasını bekliyoruz 🕙.

Ama tezgahtan uzaklaşıp sıranız gelene kadarmasanıza dönebilir 🔀 ve dikkatinizi aşkınıza 😍 verebilirsiniz vr bunun üzerine "çalışabilirsiniz" ⏯ 🤓. Artık "üretken" birşey yapıyorsunuz 🤓, sevgilinle 😍 flört eder gibi.

Kasiyer 💁  "Hamburgerler hazır !" 🍔 dediğinde ve görüntülenen numara sizin numaranız olduğunda hemen koşup hamburgerlerinizi almaya çalışmıyorsunuz. Biliyorsunuzki kimse sizin hamburgerlerinizi 🍔 çalmayacak çünkü sıra sizin.

Yani Aşkınızın😍 hikayeyi bitirmesini bekliyorsunuz (çalışmayı bitir ⏯ / görev işleniyor.. 🤓), nazikçe gülümseyin ve hamburger yemeye gittiğinizi söyleyin ⏸.

Ardından tezgaha 🔀, şimdi biten ilk göreve ⏯ gidin, Hamburgerleri 🍔 alın, teşekkür edin ve masaya götürün. sayacın bu adımı tamamlanır ⏹. Bu da yeni bir görev olan  "hamburgerleri ye" 🔀 ⏯ görevini başlatırken "hamburgerleri al" ⏹ görevini bitirir.

### Parallel Hamburgerler

Şimdi bunların "Eşzamanlı Hamburger" değil, "Paralel Hamburger" olduğunu düşünelim.

Hamburger 🍔 almak için 😍 aşkınla Paralel fast food'a gidiyorsun.

Birden fazla kasiyer varken (varsayalım 8) sıraya girdiniz👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳 ve sıranız gelene kadar bekliyorsunuz.

Sizden önceki herkez ayrılmadan önce hamburgerlerinin 🍔 hazır olmasını bekliyor 🕙. Çünkü kasiyerlerin her biri bir hamburger hazırlanmadan önce bir sonraki siparişe geçmiiyor.

Sonunda senin sıran, aşkın 😍 ve kendin için 2 hamburger 🍔 siparişi verdiniz.

Ödemeyi yaptınız 💸.

Kasiyer mutfağa gider 👨‍🍳.

Sırada bekliyorsunuz 🕙, kimse sizin burgerinizi 🍔 almaya çalışmıyor çünkü sıra sizin.

Sen ve aşkın 😍 sıranızı korumak ve hamburgerleri almakla o kadar meşgulsünüz ki birbirinize vakit 🕙 ayıramıyorsunuz 😞.

İşte bu "senkron" çalışmadır.  Kasiyer/aşçı 👨‍🍳ile senkron hareket ediyorsunuz. Bu yüzden beklemek 🕙 ve kasiyer/aşçı burgeri 🍔bitirip size getirdiğinde  orda olmak zorundasınız yoksa başka biri alabilir.

Sonra kasiyeri/aşçı 👨‍🍳 nihayet hamburgerlerinizle 🍔, uzun bir süre sonra 🕙 tezgaha  geri geliyor.

Burgerlerinizi 🍔 al ve aşkınla masanıza doğru ilerle 😍.

Sadece burgerini yiyorsun 🍔 ve bitti ⏹.

Bekleyerek çok fazla zaman geçtiğinden 🕙 konuşmaya çok fazla vakit kalmadı 😞.

---

Paralel burger senaryosunda ise,  siz iki işlemcili birer robotsunuz 🤖 (sen ve sevgilin 😍), Beklıyorsunuz 🕙 hem konuşarak güzel vakit geçirirken ⏯ hem de sıranızı bekliyorsunuz 🕙.

Mağazada ise 8 işlemci bulunuyor (Kasiyer/aşçı) 👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳. Eşzamanlı burgerde yalnızca 2 kişi olabiliyordu (bir kasiyer ve bir aşçı) 💁 👨‍🍳.

Ama yine de bu  en iyisi değil 😞.

---

Bu hikaye burgerler 🍔 için paralel.

Bir gerçek hayat örneği verelim. Bir banka hayal edin.

Bankaların çoğunda birkaç kasiyer  👨‍💼👨‍💼👨‍💼👨‍💼  ve uzun bir sıra var 🕙🕙🕙🕙🕙🕙🕙🕙.

Tüm işi sırayla bir müşteri ile yapan tüm kasiyerler 👨‍💼⏯.

Ve uzun süre kuyrukta beklemek 🕙 zorundasın yoksa sıranı kaybedersin.

Muhtemelen ayak işlerı yaparken sevgilini 😍 bankaya 🏦 getirmezsin.

### Burger Sonucu

Bu "aşkınla fast food burgerleri" senaryosunda, çok fazla bekleme olduğu için 🕙, eşzamanlı bir sisteme sahip olmak çok daha mantıklı ⏸🔀⏯.

Web uygulamalarının çoğu için durum böyledir.

Pek çok kullanıcı var, ama sunucunuz pek de iyi olmayan bir bağlantı ile istek atmalarını bekliyor.

Ve sonra yanıtların geri gelmesi için tekrar 🕙 bekliyor

Bu "bekleme" 🕙 mikrosaniye cinsinden ölçülür, yine de, hepsini toplarsak çok fazla bekleme var.

Bu nedenle, web API'leri için asenkron ⏸🔀⏯ kod kullanmak çok daha mantıklı.

Mevcut popüler Python frameworklerinin çoğu (Flask ve Django gibi), Python'daki yeni asenkron özellikler mevcut olmadan önce yazıldı. Bu nedenle, dağıtılma biçimleri paralel yürütmeyi ve yenisi kadar güçlü olmayan eski bir eşzamansız yürütme biçimini destekler.

Asenkron web (ASGI) özelliği, WebSockets için destek eklemek için Django'ya eklenmiş olsa da.

Asenkron çalışabilme NodeJS in popüler olmasının sebebi (paralel olamasa bile) ve Go dilini güçlü yapan özelliktir.

Ve bu **FastAPI** ile elde ettiğiniz performans düzeyiyle aynıdır.

Aynı anda paralellik ve asenkronluğa sahip olabildiğiniz için, test edilen NodeJS çerçevelerinin çoğundan daha yüksek performans elde edersiniz ve C'ye daha yakın derlenmiş bir dil olan Go ile eşit bir performans elde edersiniz <a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(bütün teşekkürler Starlette'e )</a>.

### Eşzamanlılık paralellikten daha mı iyi?

Hayır!  Hikayenin ahlakı bu değil.

Eşzamanlılık paralellikten farklıdır. Ve çok fazla bekleme içeren **belirli** senaryolarda daha iyidir. Bu nedenle, genellikle web uygulamaları için paralellikten çok daha iyidir. Ama her şey için değil.

Yanı, bunu aklınızda oturtmak için aşağıdaki kısa hikayeyi hayal edin:

> Büyük, kirli bir evi temizlemelisin.

*Evet, tüm hikaye bu*.

---

Beklemek yok 🕙. Hiçbir yerde.  Sadece evin birden fazla yerinde yapılacak fazlasıyla iş var.

You could have turns as in the burgers example, first the living room, then the kitchen, but as you are not waiting 🕙 for anything, just cleaning and cleaning, the turns wouldn't affect anything.
Hamburger örneğindeki gibi dönüşleriniz olabilir, önce oturma odası, sonra mutfak, ama hiçbir şey için 🕙 beklemediğinizden, sadece temizlik, temizlik ve temizlik, dönüşler hiçbir şeyi etkilemez.

Sıralı veya sırasız (eşzamanlılık) bitirmek aynı zaman alır ve aynı miktarda işi yaparsınız.

Ama bu durumda, 8 eski kasiyer/aşçı - yeni temizlikçiyi getirebilseydiniz 👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳👩‍🍳👨‍🍳 ve her birini (artı siz) evin bir bölgesini temizlemek için görevlendirseydiniz, ekstra yardımla tüm işleri **paralel** olarak yapabilir ve çok daha erken bitirebilirdiniz.

Bu senaryoda, temizlikçilerin her biri (siz dahil) birer işlemci olacak ve üzerine düşeni yapacaktır.

Yürütme süresinin çoğu (beklemek yerine) iş yapıldığından ve bilgisayardaki iş bir <abbr title="Central Processing Unit">CPU</abbr> tarafından yapıldığından, bu sorunlara "CPU bound" diyorlar".

---

CPU'ya bağlı işlemlerin yaygın örnekleri, karmaşık matematik işlemleri gerektiren işlerdir.

Örneğin:

* **Ses** veya **görüntü işleme**.
* **Bilgisayar görüsü**: bir görüntü milyonlarca pikselden oluşur, her pikselin 3 değeri / rengi vardır, bu pikseller üzerinde aynı anda bir şeyler hesaplamayı gerektiren işleme.
* **Makine Öğrenimi**: Çok sayıda "matris" ve "vektör" çarpımı gerektirir. Sayıları olan ve hepsini aynı anda çarpan büyük bir elektronik tablo düşünün.
* **Derin Öğrenme**: Bu, Makine Öğreniminin bir alt alanıdır, dolayısıyla aynısı geçerlidir. Sadece çarpılacak tek bir sayı tablosu değil, büyük bir sayı kümesi vardır ve çoğu durumda bu modelleri oluşturmak ve/veya kullanmak için özel işlemciler kullanırsınız.

### Eşzamanlılık + Paralellik: Web + Makine Öğrenimi

**FastAPI** ile web geliştirme için çok yaygın olan eşzamanlılıktan yararlanabilirsiniz (NodeJS'in aynı çekiciliği).

Ancak, Makine Öğrenimi sistemlerindekile gibi **CPU'ya bağlı** iş yükleri için paralellik ve çoklu işlemenin (birden çok işlemin paralel olarak çalışması) avantajlarından da yararlanabilirsiniz.

Buna ek olarak Python'un **Veri Bilimi**, Makine Öğrenimi ve özellikle Derin Öğrenme için ana dil olduğu gerçeği, FastAPI'yi Veri Bilimi / Makine Öğrenimi web API'leri ve uygulamaları için çok iyi bir seçenek haline getirir.

Production'da nasıl oldugunu görmek için şu bölüme bakın [Deployment](deployment/index.md){.internal-link target=_blank}.

## `async` ve `await`

Python'un modern sürümleri, asenkron kodu tanımlamanın çok sezgisel bir yoluna sahiptir. Bu, normal "sequentıal" (sıralı) kod gibi görünmesini ve doğru anlarda sizin için "awaıt" ile bekleme yapmasını sağlar.

Sonuçları vermeden önce beklemeyi gerektirecek ve yeni Python özelliklerini destekleyen bir işlem olduğunda aşağıdaki gibi kodlayabilirsiniz:

```Python
burgers = await get_burgers(2)
```

Buradaki `await` anahtari Python'a, sonuçları `burgers` degiskenine atamadan önce `get_burgers(2)` kodunun işini bitirmesini 🕙 beklemesi gerektiğini söyler. Bununla Python, bu ara zamanda başka bir şey 🔀 ⏯ yapabileceğini bilecektir (başka bir istek almak gibi).

 `await`kodunun çalışması için, eşzamansızlığı destekleyen bir fonksiyonun içinde olması gerekir. Bunu da yapmak için fonksiyonu `async def` ile tanımlamamız yeterlidir:

```Python hl_lines="1"
async def get_burgers(number: int):
    # burgerleri oluşturmak için asenkron birkaç iş
    return burgers
```

...`def` yerine:

```Python hl_lines="2"
# bu kod asenkron değil
def get_sequential_burgers(number: int):
    # burgerleri oluşturmak için senkron bırkaç iş
    return burgers
```

`async def` ile Python, bu fonksıyonun içinde, `await` ifadelerinin farkında olması gerektiğini ve çalışma zamanı gelmeden önce bu işlevin yürütülmesini "duraklatabileceğini" ve başka bir şey yapabileceğini 🔀 bilir.

`async def` fonksiyonunu çağırmak istediğinizde, onu "awaıt" ıle kullanmanız gerekir. Yani, bu işe yaramaz:

```Python
# Bu işe yaramaz, çünkü get_burgers, şu şekilde tanımlandı: async def
burgers = get_burgers(2)
```

---

Bu nedenle, size onu `await` ile çağırabileceğinizi söyleyen bir kitaplık kullanıyorsanız, onu `async def` ile tanımlanan *path fonksiyonu* içerisinde kullanmanız gerekir, örneğin:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Daha fazla teknik detay

`await` in yalnızca `async def` ile tanımlanan fonksıyonların içinde kullanılabileceğini fark etmişsinizdir.

Ama aynı zamanda, `async def` ile tanımlanan fonksiyonların "await" ile beklenmesi gerekir. Bu nedenle, "`async def` içeren fonksiyonlar yalnızca "`async def` ile tanımlanan fonksiyonların içinde çağrılabilir.


Yani yumurta mı tavukdan, tavuk mu yumurtadan gibi ilk `async` fonksiyonu nasıl çağırılır?

**FastAPI** ile çalışıyorsanız bunun için endişelenmenize gerek yok, çünkü bu "ilk" fonksiyon sizin *path fonksiyonunuz* olacak ve FastAPI doğru olanı nasıl yapacağını bilecek.

Ancak FastAPI olmadan `async` / `await` kullanmak istiyorsanız, <a href="https://docs.python.org/3/library/asyncio-task.html#coroutine" class="external-link" target="_blank">resmi Python belgelerini kontrol edin</a>.

### Asenkron kodun diğer biçimleri

Bu `async` ve `await` kullanimi oldukça yenidir.

Ancak asenkron kodla çalışmayı çok daha kolay hale getirir.

Aynı sözdizimi (hemen hemen aynı) son zamanlarda JavaScript'in modern sürümlerine de dahil edildi (Tarayıcı ve NodeJS'de).

Ancak bundan önce, asenkron kodu işlemek oldukça karmaşık ve zordu.

Python'un önceki sürümlerinde, threadlerı veya <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a> kullanıyor olabilirdin. Ancak kodu anlamak, hata ayıklamak ve düşünmek çok daha karmaşık olurdu.

NodeJS / Browser JavaScript'in önceki sürümlerinde, "callback" kullanırdınız. Bu da "callbacks cehennemine" yol açar.

## Coroutine'ler

**Coroutine**, bir `async def` fonksiyonu tarafından döndürülen değer için çok süslü bir terimdir. Python bunun bir fonksiyon gibi bir noktada başlayıp biteceğini bilir, ancak içinde bir `await` olduğunda dahili olarak da duraklatılabilir ⏸.

Ancak, `async` ve `await` ile asenkron kod kullanmanın tüm bu işlevselliği, çoğu zaman "Coroutine" kullanmak olarak adlandırılır. Go'nun ana özelliği olan "Goroutines" ile karşılaştırılabilir.

## Sonuç

Aynı ifadeyi yukarıdan görelim:

> Python'ın modern sürümleri, **"async" ve "await"** sözdizimi ile birlikte **"coroutines"** adlı bir özelliği kullanan **"asenkron kod"** desteğine sahiptir.

Şimdi daha mantıklı gelmeli. ✨

FastAPI'ye (Starlette aracılığıyla) güç veren ve bu kadar etkileyici bir performansa sahip olmasını sağlayan şey budur.

## Çok Teknik Detaylar

/// warning

Muhtemelen burayı atlayabilirsiniz.

Bunlar, **FastAPI**'nin altta nasıl çalıştığına dair çok teknik ayrıntılardır.

Biraz teknik bilginiz varsa (co-routines, threads, blocking, vb)ve FastAPI'nin "async def" ile normal "def" arasındaki farkı nasıl işlediğini merak ediyorsanız, devam edin.

///

### Path fonksiyonu

"async def" yerine normal "def" ile bir *yol işlem işlevi* bildirdiğinizde, doğrudan çağrılmak yerine (sunucuyu bloke edeceğinden) daha sonra beklenen harici bir iş parçacığı havuzunda çalıştırılır.

Yukarıda açıklanan şekilde çalışmayan başka bir asenkron framework'den geliyorsanız ve küçük bir performans kazancı (yaklaşık 100 nanosaniye) için  "def" ile *path fonksiyonu* tanımlamaya alışkınsanız, **FastAPI**'de tam tersi olacağını unutmayın. Bu durumlarda, *path fonksiyonu* <abbr title="Input/Output: disk okuma veya yazma, ağ iletişimleri.">G/Ç</abbr> engelleyen durum oluşturmadıkça "async def" kullanmak daha iyidir.

Yine de, her iki durumda da, **FastAPI**'nin önceki frameworkden [hala daha hızlı](index.md#performans){.internal-link target=_blank} (veya en azından karşılaştırılabilir) olma olasılığı vardır.

### Bagımlılıklar

Aynısı bağımlılıklar için de geçerlidir. Bir bağımlılık, "async def" yerine standart bir "def" işleviyse, harici iş parçacığı havuzunda çalıştırılır.

### Alt-bağımlıklar

Birbirini gerektiren (fonksiyonlarin parametreleri olarak) birden fazla bağımlılık ve alt bağımlılıklarınız olabilir, bazıları 'async def' ve bazıları normal 'def' ile oluşturulabilir. Yine de normal 'def' ile oluşturulanlar, "await" kulanilmadan harici bir iş parçacığında (iş parçacığı havuzundan) çağrılır.

### Diğer yardımcı fonksiyonlar

Doğrudan çağırdığınız diğer herhangi bir yardımcı fonksiyonu, normal "def" veya "async def" ile tanimlayabilirsiniz. FastAPI onu çağırma şeklinizi etkilemez.

Bu, FastAPI'nin sizin için çağırdığı fonksiyonlarin tam tersidir: *path fonksiyonu* ve bağımlılıklar.

Yardımcı program fonksiyonunuz 'def' ile normal bir işlevse, bir iş parçacığı havuzunda değil doğrudan (kodunuzda yazdığınız gibi) çağrılır, işlev 'async def' ile oluşturulmuşsa çağırıldığı yerde 'await' ile beklemelisiniz.

---

Yeniden, bunlar, onları aramaya geldiğinizde muhtemelen işinize yarayacak çok teknik ayrıntılardır.

Aksi takdirde, yukarıdaki bölümdeki yönergeleri iyi bilmelisiniz: <a href="#in-a-hurry">Aceleniz mi var?</a>.
