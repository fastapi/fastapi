# Lifespan Olayları { #lifespan-events }

Uygulama **başlamadan** önce çalıştırılması gereken mantığı (kodu) tanımlayabilirsiniz. Bu, bu kodun **bir kez**, uygulama **request almaya başlamadan önce** çalıştırılacağı anlamına gelir.

Benzer şekilde, uygulama **kapanırken** çalıştırılması gereken mantığı (kodu) da tanımlayabilirsiniz. Bu durumda bu kod, muhtemelen **çok sayıda request** işlendi **sonra**, **bir kez** çalıştırılır.

Bu kod, uygulama request almaya **başlamadan** önce ve request’leri işlemeyi **bitirdikten** hemen sonra çalıştığı için, uygulamanın tüm **lifespan**’ını (birazdan "lifespan" kelimesi önemli olacak 😉) kapsar.

Bu yaklaşım, tüm uygulama boyunca kullanacağınız ve request’ler arasında **paylaşılan** **resource**’ları kurmak ve/veya sonrasında bunları **temizlemek** için çok faydalıdır. Örneğin bir veritabanı connection pool’u ya da paylaşılan bir machine learning modelini yüklemek gibi.

## Kullanım Senaryosu { #use-case }

Önce bir **kullanım senaryosu** örneğiyle başlayalım, sonra bunu bununla nasıl çözeceğimize bakalım.

Request’leri işlemek için kullanmak istediğiniz bazı **machine learning modelleriniz** olduğunu hayal edelim. 🤖

Aynı modeller request’ler arasında paylaşılır; yani request başına bir model, kullanıcı başına bir model vb. gibi değil.

Modeli yüklemenin, diskten çok fazla **data** okunması gerektiği için **oldukça uzun sürebildiğini** düşünelim. Dolayısıyla bunu her request için yapmak istemezsiniz.

Modeli modülün/dosyanın en üst seviyesinde yükleyebilirdiniz; ancak bu, basit bir otomatik test çalıştırdığınızda bile **modelin yükleneceği** anlamına gelir. Böyle olunca test, kodun bağımsız bir kısmını çalıştırabilmek için önce modelin yüklenmesini beklemek zorunda kalır ve **yavaş** olur.

Burada çözeceğimiz şey bu: modeli request’ler işlenmeden önce yükleyelim, ama kod yüklenirken değil; yalnızca uygulama request almaya başlamadan hemen önce.

## Lifespan { #lifespan }

Bu *startup* ve *shutdown* mantığını, `FastAPI` uygulamasının `lifespan` parametresi ve bir "context manager" kullanarak tanımlayabilirsiniz (bunun ne olduğunu birazdan göstereceğim).

Önce bir örnekle başlayıp sonra ayrıntılarına bakalım.

Aşağıdaki gibi `yield` kullanan async bir `lifespan()` fonksiyonu oluşturuyoruz:

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

Burada, `yield` öncesinde (sahte) model fonksiyonunu machine learning modellerini içeren dictionary’e koyarak, modeli yükleme gibi maliyetli bir *startup* işlemini simüle ediyoruz. Bu kod, *startup* sırasında, uygulama **request almaya başlamadan önce** çalıştırılır.

Ardından `yield`’den hemen sonra modeli bellekten kaldırıyoruz (unload). Bu kod, uygulama **request’leri işlemeyi bitirdikten sonra**, *shutdown*’dan hemen önce çalıştırılır. Örneğin memory veya GPU gibi resource’ları serbest bırakabilir.

/// tip | İpucu

`shutdown`, uygulamayı **durdurduğunuzda** gerçekleşir.

Belki yeni bir sürüm başlatmanız gerekiyordur, ya da çalıştırmaktan sıkılmışsınızdır. 🤷

///

### Lifespan fonksiyonu { #lifespan-function }

Dikkat edilmesi gereken ilk şey, `yield` içeren async bir fonksiyon tanımlıyor olmamız. Bu, `yield` kullanan Dependencies’e oldukça benzer.

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

Fonksiyonun `yield`’den önceki kısmı, uygulama başlamadan **önce** çalışır.

`yield`’den sonraki kısım ise, uygulama işini bitirdikten **sonra** çalışır.

### Async Context Manager { #async-context-manager }

Bakarsanız, fonksiyon `@asynccontextmanager` ile dekore edilmiş.

Bu da fonksiyonu "**async context manager**" denen şeye dönüştürür.

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Python’da **context manager**, `with` ifadesi içinde kullanabildiğiniz bir yapıdır. Örneğin `open()` bir context manager olarak kullanılabilir:

```Python
with open("file.txt") as file:
    file.read()
```

Python’ın güncel sürümlerinde bir de **async context manager** vardır. Bunu `async with` ile kullanırsınız:

```Python
async with lifespan(app):
    await do_stuff()
```

Yukarıdaki gibi bir context manager veya async context manager oluşturduğunuzda, yaptığı şey şudur: `with` bloğuna girmeden önce `yield`’den önceki kodu çalıştırır, `with` bloğundan çıktıktan sonra da `yield`’den sonraki kodu çalıştırır.

Yukarıdaki kod örneğimizde bunu doğrudan kullanmıyoruz; bunun yerine FastAPI’ye veriyoruz ki o kullansın.

`FastAPI` uygulamasının `lifespan` parametresi bir **async context manager** alır; dolayısıyla oluşturduğumuz yeni `lifespan` async context manager’ını buraya geçebiliriz.

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## Alternatif Events (kullanımdan kaldırıldı) { #alternative-events-deprecated }

/// warning | Uyarı

*startup* ve *shutdown* işlemlerini yönetmenin önerilen yolu, yukarıda anlatıldığı gibi `FastAPI` uygulamasının `lifespan` parametresini kullanmaktır. Bir `lifespan` parametresi sağlarsanız, `startup` ve `shutdown` event handler’ları artık çağrılmaz. Ya tamamen `lifespan` ya da tamamen events; ikisi birden değil.

Muhtemelen bu bölümü atlayabilirsiniz.

///

*startup* ve *shutdown* sırasında çalıştırılacak bu mantığı tanımlamanın alternatif bir yolu daha vardır.

Uygulama başlamadan önce veya uygulama kapanırken çalıştırılması gereken event handler’ları (fonksiyonları) tanımlayabilirsiniz.

Bu fonksiyonlar `async def` ile veya normal `def` ile tanımlanabilir.

### `startup` eventi { #startup-event }

Uygulama başlamadan önce çalıştırılacak bir fonksiyon eklemek için, `"startup"` event’i ile tanımlayın:

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

Bu durumda `startup` event handler fonksiyonu, "database" öğesini (sadece bir `dict`) bazı değerlerle başlatır.

Birden fazla event handler fonksiyonu ekleyebilirsiniz.

Ve tüm `startup` event handler’ları tamamlanmadan uygulamanız request almaya başlamaz.

### `shutdown` eventi { #shutdown-event }

Uygulama kapanırken çalıştırılacak bir fonksiyon eklemek için, `"shutdown"` event’i ile tanımlayın:

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

Burada `shutdown` event handler fonksiyonu, `log.txt` dosyasına `"Application shutdown"` satırını yazar.

/// info | Bilgi

`open()` fonksiyonunda `mode="a"` "append" anlamına gelir; yani satır, önceki içeriği silmeden dosyada ne varsa onun sonuna eklenir.

///

/// tip | İpucu

Dikkat edin, bu örnekte bir dosyayla etkileşen standart Python `open()` fonksiyonunu kullanıyoruz.

Dolayısıyla disk’e yazılmasını beklemeyi gerektiren I/O (input/output) söz konusu.

Ancak `open()` `async` ve `await` kullanmaz.

Bu yüzden event handler fonksiyonunu `async def` yerine standart `def` ile tanımlarız.

///

### `startup` ve `shutdown` birlikte { #startup-and-shutdown-together }

*startup* ve *shutdown* mantığınızın birbiriyle bağlantılı olma ihtimali yüksektir; bir şeyi başlatıp sonra bitirmek, bir resource edinip sonra serbest bırakmak vb. isteyebilirsiniz.

Bunu, ortak mantık veya değişken paylaşmayan ayrı fonksiyonlarda yapmak daha zordur; çünkü değerleri global değişkenlerde tutmanız veya benzer numaralar yapmanız gerekir.

Bu nedenle artık bunun yerine, yukarıda açıklandığı gibi `lifespan` kullanmanız önerilmektedir.

## Teknik Detaylar { #technical-details }

Meraklı nerd’ler için küçük bir teknik detay. 🤓

Altta, ASGI teknik spesifikasyonunda bu, [Lifespan Protokolü](https://asgi.readthedocs.io/en/latest/specs/lifespan.html)’nün bir parçasıdır ve `startup` ile `shutdown` adında event’ler tanımlar.

/// info | Bilgi

Starlette `lifespan` handler’ları hakkında daha fazlasını [Starlette Lifespan dokümanları](https://www.starlette.dev/lifespan/) içinde okuyabilirsiniz.

Ayrıca kodunuzun başka bölgelerinde de kullanılabilecek lifespan state’i nasıl yöneteceğinizi de kapsar.

///

## Alt Uygulamalar { #sub-applications }

🚨 Unutmayın: Bu lifespan event’leri (`startup` ve `shutdown`) yalnızca ana uygulama için çalıştırılır; [Alt Uygulamalar - Mounts](sub-applications.md) için çalıştırılmaz.
