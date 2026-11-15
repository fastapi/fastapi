# Gelişmiş Dependency'ler { #advanced-dependencies }

## Parametreli dependency'ler { #parameterized-dependencies }

Şimdiye kadar gördüğümüz tüm dependency'ler sabit bir function ya da class idi.

Ancak, birçok farklı function veya class tanımlamak zorunda kalmadan, dependency üzerinde bazı parametreler ayarlamak isteyebileceğiniz durumlar olabilir.

Örneğin, query parametresi `q`'nun belirli bir sabit içeriği barındırıp barındırmadığını kontrol eden bir dependency istediğimizi düşünelim.

Ama bu sabit içeriği parametreleştirebilmek istiyoruz.

## "Callable" bir instance { #a-callable-instance }

Python'da bir class'ın instance'ını "callable" yapmanın bir yolu vardır.

Class'ın kendisini değil (zaten callable'dır), o class'ın bir instance'ını.

Bunu yapmak için `__call__` adında bir method tanımlarız:

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

Bu durumda, ek parametreleri ve alt-dependency'leri kontrol etmek için **FastAPI**'nin kullanacağı şey bu `__call__` olacaktır; ayrıca daha sonra *path operation function* içindeki parametreye bir değer geçmek için çağrılacak olan da budur.

## Instance'ı parametreleştirme { #parameterize-the-instance }

Ve şimdi, dependency'yi "parametreleştirmek" için kullanacağımız instance parametrelerini tanımlamak üzere `__init__` kullanabiliriz:

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

Bu durumda **FastAPI**, `__init__` ile asla uğraşmaz veya onu önemsemez; onu doğrudan kendi kodumuzda kullanırız.

## Bir instance oluşturma { #create-an-instance }

Bu class'tan bir instance'ı şöyle oluşturabiliriz:

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

Böylece dependency'mizi "parametreleştirmiş" oluruz; artık içinde `"bar"` vardır ve bu değer `checker.fixed_content` attribute'u olarak durur.

## Instance'ı dependency olarak kullanma { #use-the-instance-as-a-dependency }

Sonra `Depends(FixedContentQueryChecker)` yerine `Depends(checker)` içinde bu `checker`'ı kullanabiliriz. Çünkü dependency, class'ın kendisi değil, `checker` instance'ıdır.

Ve dependency çözülürken **FastAPI** bu `checker`'ı şöyle çağırır:

```Python
checker(q="somequery")
```

...ve bunun döndürdüğü her şeyi, *path operation function* içinde `fixed_content_included` parametresine dependency değeri olarak geçirir:

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip | İpucu

Bunların tamamı biraz yapay görünebilir. Ayrıca bunun nasıl faydalı olduğu da henüz çok net olmayabilir.

Bu örnekler bilerek basit tutuldu; ama mekanizmanın nasıl çalıştığını gösteriyor.

Security bölümlerinde, aynı şekilde implement edilmiş yardımcı function'lar bulunuyor.

Buradaki her şeyi anladıysanız, security için kullanılan bu yardımcı araçların arka planda nasıl çalıştığını da zaten biliyorsunuz demektir.

///

## Dependency Eşzamanlılığını Sınırlama { #limit-dependency-concurrency }

Bazı durumlarda, bir dependency'yi aynı anda kaç request'in kullanabileceğini sınırlamak isteyebilirsiniz.

Örneğin, veritabanınızda kullanılabilir bağlantı sayısı sınırlı olabilir. Yeni request'lerin session oluşturmadan önce, başka bir request'in kendi session'ıyla işini bitirmesini beklemesini sağlayabilirsiniz.

Bunu `Depends()` içindeki `max_concurrency` ile yapabilirsiniz.

[SQL veritabanları rehberindeki](../tutorial/sql-databases.md) `SessionDep` alias'ını güncelleyelim:

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

Artık bu dependency aracılığıyla aynı anda en fazla **beş request** açık bir veritabanı session'ına sahip olabilir.

Başka bir request'in session'a ihtiyacı olursa, bu session'lardan biri kapanana kadar bekler.

Beklerken **bir worker thread'i meşgul etmez**, böylece bu thread'ler başka kodları çalıştırabilir.

Değer pozitif bir tam sayı olmalıdır. Varsayılan değer `None`'dır; bu, FastAPI'nin dependency'nin aynı anda kaç kez çalışabileceğini sınırlamadığı anlamına gelir.

### Limiti Route'lar Arasında Paylaşma { #share-the-limit-between-routes }

Bu örnekteki tüm route'lar aynı `SessionDep` alias'ını kullandığından, beş session'lık limiti paylaşır.

Bir limiti paylaşmak için, örneğin buradaki gibi bir `Annotated` alias'ında, **aynı `Depends()` objesini** yeniden kullanın.

Her route için yeni bir `Depends(get_session, max_concurrency=5)` yazarsanız, her birinin kendine ait beş session'lık limiti olur. Hepsi aynı `get_session` function'ını kullansa da bu durum değişmez.

Aynı `SessionDep` başka bir uygulamada yeniden kullanıldığında da, her iki uygulama aynı event loop içinde çalıştığı sürece limit paylaşılır. Buna mount edilmiş uygulamalar da dahildir.

Örneğin, iki uygulama aynı veritabanı bağlantı havuzu için bu `SessionDep`'i kullanıyorsa, bu dependency aracılığıyla toplamda en fazla beş açık session'a sahip olabilir.

Uygulamalar ayrı havuzlar kullanıyor ve bağımsız limitlere ihtiyaç duyuyorsa, her uygulama için ayrı bir `Depends()` objesi oluşturun.

### Yeni Bir Session'a İzin Vermeden Önce Mevcut Session'ı Kapatma { #close-the-session-before-allowing-another-one }

Bu örnekte `get_session`, `yield` kullanır. Çıkış kodu session'ı kapatmayı bitirene kadar session limit kapsamında sayılır.

Bu çıkış kodunun ne zaman çalışacağını dependency'nin `scope` değeri belirler:

* Varsayılan olan `scope="request"` ile, response gönderildikten sonra çalışır.
* `scope="function"` ile, *path operation function* bittikten sonra, response gönderilmeden önce çalışır.

[Erken çıkış ve scope](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) hakkında daha fazla bilgi edinebilirsiniz.

`yield` kullanmayan bir dependency'de çağrı, yalnızca function bitene kadar limit kapsamında sayılır.

WebSocket handler içinde `yield` kullanan bir dependency kullanırsanız, handler sonlanana ve dependency'nin çıkış kodu tamamlanana kadar limit kapsamında sayılır.

/// note | Not

[Önbelleğe alınmış bir dependency değerini](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times) yeniden kullanmak, limit kapsamında tekrar sayılmaz. Farklı tanımlar bu değeri paylaşıyorsa, yalnızca dependency'yi çağıran tanımın limiti kapsamında sayılır.

///

### Uygulamanız İçin Bir Limit Seçme { #choose-a-limit-for-your-application }

Bu session'ların kullanabileceği veritabanı bağlantısı sayısına uygun bir limit seçin.

Uygulamanızın başka bölümleri de bu bağlantıları kullanıyorsa, onlar için de pay bırakın. FastAPI, veritabanı bağlantı havuzunuzun boyutunu bilmez.

Her worker process'in kendi limiti vardır. Örneğin, bu dependency'yi kullanan iki worker process toplamda en fazla on açık session'a sahip olabilir.

/// note | Teknik Detaylar

Limitler her event loop için de ayrıdır. Farklı event loop'larda çalışan uygulamalar, aynı `Depends()` objesini yeniden kullansalar bile limiti paylaşmaz.

///

### Birden Fazla Kaynağa İhtiyaç Duyan Dependency'ler { #dependencies-that-need-more-than-one-resource }

FastAPI, bir dependency'nin limitini uygulamadan önce onun alt-dependency'lerini çalıştırır.

Bu nedenle, veritabanı session'larını sınırlamak için `max_concurrency` değerini session'ın oluşturulduğu `Depends(get_session, ...)` üzerinde ayarlayın.

Bir request, yalnızca request sonunda kapatılacak bir session'ı elinde tutarken başka bir session'a ihtiyaç duyarsa kilitlenebilir.

Örneğin, paylaşılan bir `Depends(get_session, max_concurrency=1, use_cache=False)` objesinin aynı request içinde iki kez kullanıldığını düşünün.

İlk çağrı bir session oluşturur. İkinci çağrı bunun kapanmasını bekler. Ancak request bitene kadar ilk session kapanamaz ve request de ikinci çağrıyı beklemektedir.

İki request de kilitlenebilir: Biri bir session'ı elinde tutup başka bir kaynağı beklerken, diğeri o kaynağı elinde tutup bir session bekliyor olabilir.

Request'leriniz birden fazla kaynağa ihtiyaç duyuyorsa, kaynakları aynı sırayla edinin. FastAPI her limiti ayrı ayrı uygular; bir request'in ihtiyaç duyacağı tüm kaynakları önceden ayırmaz.

## `yield`, `HTTPException`, `except` ve Background Tasks ile Dependency'ler { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Uyarı

Büyük ihtimalle bu teknik detaylara ihtiyacınız yok.

Bu detaylar, özellikle 0.121.0'dan eski bir FastAPI uygulamanız varsa ve `yield` kullanan dependency'lerle ilgili sorunlar yaşıyorsanız faydalıdır.

///

`yield` kullanan dependency'ler; farklı kullanım senaryolarını kapsamak ve bazı sorunları düzeltmek için zaman içinde evrildi. Aşağıda nelerin değiştiğinin bir özeti var.

### `yield` ve `scope` ile dependency'ler { #dependencies-with-yield-and-scope }

0.121.0 sürümünde FastAPI, `yield` kullanan dependency'ler için `Depends(scope="function")` desteğini ekledi.

`Depends(scope="function")` kullanıldığında, `yield` sonrasındaki çıkış kodu, *path operation function* biter bitmez, response client'a geri gönderilmeden önce çalıştırılır.

`Depends(scope="request")` (varsayılan) kullanıldığında ise `yield` sonrasındaki çıkış kodu, response gönderildikten sonra çalıştırılır.

Daha fazlasını [`yield` ile Dependency'ler - Erken çıkış ve `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) dokümantasyonunda okuyabilirsiniz.

### `yield` ve `StreamingResponse` ile dependency'ler, Teknik Detaylar { #dependencies-with-yield-and-streamingresponse-technical-details }

FastAPI 0.118.0 öncesinde, `yield` kullanan bir dependency kullanırsanız, *path operation function* döndükten sonra ama response gönderilmeden hemen önce `yield` sonrasındaki çıkış kodu çalıştırılırdı.

Amaç, response'un ağ üzerinden taşınmasını beklerken gereğinden uzun süre resource tutmaktan kaçınmaktı.

Bu değişiklik aynı zamanda şunu da ifade ediyordu: `StreamingResponse` döndürürseniz, `yield` kullanan dependency'nin çıkış kodu zaten çalışmış olurdu.

Örneğin, `yield` kullanan bir dependency içinde bir veritabanı session'ınız varsa, `StreamingResponse` veri stream ederken bu session'ı kullanamazdı; çünkü `yield` sonrasındaki çıkış kodunda session zaten kapatılmış olurdu.

Bu davranış 0.118.0'da geri alındı ve `yield` sonrasındaki çıkış kodunun, response gönderildikten sonra çalıştırılması sağlandı.

/// note | Not

Aşağıda göreceğiniz gibi, bu davranış 0.106.0 sürümünden önceki davranışa oldukça benzer; ancak köşe durumlar için çeşitli iyileştirmeler ve bug fix'ler içerir.

///

#### Erken Çıkış Kodu için Kullanım Senaryoları { #use-cases-with-early-exit-code }

Bazı özel koşullardaki kullanım senaryoları, response gönderilmeden önce `yield` kullanan dependency'lerin çıkış kodunun çalıştırıldığı eski davranıştan fayda görebilir.

Örneğin, `yield` kullanan bir dependency içinde yalnızca bir kullanıcıyı doğrulamak için veritabanı session'ı kullanan bir kodunuz olduğunu düşünün; ama bu session *path operation function* içinde bir daha hiç kullanılmıyor, yalnızca dependency içinde kullanılıyor **ve** response'un gönderilmesi uzun sürüyor. Mesela veriyi yavaş gönderen bir `StreamingResponse` var, ama herhangi bir nedenle veritabanını kullanmıyor.

Bu durumda veritabanı session'ı, response tamamen gönderilene kadar elde tutulur. Ancak session kullanılmıyorsa, bunu elde tutmak gerekli değildir.

Şöyle görünebilir:

{* ../../docs_src/dependencies/tutorial013.py *}

`Session`'ın otomatik kapatılması olan çıkış kodu şurada:

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

...yavaş veri gönderen response'un gönderimi bittikten sonra çalıştırılır:

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

Ama `generate_stream()` veritabanı session'ını kullanmadığı için, response gönderilirken session'ı açık tutmak aslında gerekli değildir.

SQLModel (veya SQLAlchemy) kullanarak bu spesifik senaryoya sahipseniz, session'a artık ihtiyacınız kalmadıktan sonra session'ı açıkça kapatabilirsiniz:

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

Böylece session veritabanı bağlantısını serbest bırakır ve diğer request'ler bunu kullanabilir.

`yield` kullanan bir dependency'den erken çıkış gerektiren farklı bir kullanım senaryonuz varsa, lütfen kullanım senaryonuzla birlikte ve `yield` kullanan dependency'ler için erken kapatmadan neden fayda göreceğinizi açıklayarak bir [GitHub Discussion Sorusu](https://github.com/fastapi/fastapi/discussions/new?category=questions) oluşturun.

`yield` kullanan dependency'lerde erken kapatma için ikna edici kullanım senaryoları varsa, erken kapatmayı seçmeli (opt-in) hale getiren yeni bir yöntem eklemeyi düşünebilirim.

### `yield` ve `except` ile dependency'ler, Teknik Detaylar { #dependencies-with-yield-and-except-technical-details }

FastAPI 0.110.0 öncesinde, `yield` kullanan bir dependency kullanır, sonra o dependency içinde `except` ile bir exception yakalar ve exception'ı tekrar raise etmezseniz; exception otomatik olarak herhangi bir exception handler'a veya internal server error handler'a raise/forward edilirdi.

Bu davranış 0.110.0 sürümünde değiştirildi. Amaç, handler olmayan (internal server errors) forward edilmiş exception'ların yönetilmemesinden kaynaklanan bellek tüketimini düzeltmek ve bunu normal Python kodunun davranışıyla tutarlı hale getirmekti.

### Background Tasks ve `yield` ile dependency'ler, Teknik Detaylar { #background-tasks-and-dependencies-with-yield-technical-details }

FastAPI 0.106.0 öncesinde, `yield` sonrasında exception raise etmek mümkün değildi; çünkü `yield` kullanan dependency'lerdeki çıkış kodu response gönderildikten *sonra* çalıştırılıyordu. Bu nedenle [Exception Handler'ları](../tutorial/handling-errors.md#install-custom-exception-handlers) zaten çalışmış olurdu.

Bu tasarımın ana sebeplerinden biri, background task'lerin içinde dependency'lerin "yield ettiği" aynı objeleri kullanmaya izin vermekti; çünkü çıkış kodu, background task'ler bittikten sonra çalıştırılıyordu.

Bu davranış FastAPI 0.106.0'da, response'un ağ üzerinde taşınmasını beklerken resource tutmamak amacıyla değiştirildi.

/// tip | İpucu

Ek olarak, bir background task normalde ayrı ele alınması gereken bağımsız bir mantık setidir ve kendi resource'larına sahip olmalıdır (ör. kendi veritabanı bağlantısı).

Bu şekilde muhtemelen daha temiz bir kod elde edersiniz.

///

Bu davranışa güvenerek kod yazdıysanız, artık background task'ler için resource'ları background task'in içinde oluşturmalı ve içeride yalnızca `yield` kullanan dependency'lerin resource'larına bağlı olmayan verileri kullanmalısınız.

Örneğin, aynı veritabanı session'ını kullanmak yerine background task içinde yeni bir veritabanı session'ı oluşturur ve veritabanındaki objeleri bu yeni session ile alırsınız. Ardından, background task function'ına veritabanından gelen objeyi parametre olarak geçirmek yerine, o objenin ID'sini geçirir ve objeyi background task function'ı içinde yeniden elde edersiniz.
