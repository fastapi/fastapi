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

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[12] *}

Bu durumda, ek parametreleri ve alt-dependency'leri kontrol etmek için **FastAPI**'nin kullanacağı şey bu `__call__` olacaktır; ayrıca daha sonra *path operation function* içindeki parametreye bir değer geçmek için çağrılacak olan da budur.

## Instance'ı parametreleştirme { #parameterize-the-instance }

Ve şimdi, dependency'yi "parametreleştirmek" için kullanacağımız instance parametrelerini tanımlamak üzere `__init__` kullanabiliriz:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[9] *}

Bu durumda **FastAPI**, `__init__` ile asla uğraşmaz veya onu önemsemez; onu doğrudan kendi kodumuzda kullanırız.

## Bir instance oluşturma { #create-an-instance }

Bu class'tan bir instance'ı şöyle oluşturabiliriz:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[18] *}

Böylece dependency'mizi "parametreleştirmiş" oluruz; artık içinde `"bar"` vardır ve bu değer `checker.fixed_content` attribute'u olarak durur.

## Instance'ı dependency olarak kullanma { #use-the-instance-as-a-dependency }

Sonra `Depends(FixedContentQueryChecker)` yerine `Depends(checker)` içinde bu `checker`'ı kullanabiliriz. Çünkü dependency, class'ın kendisi değil, `checker` instance'ıdır.

Ve dependency çözülürken **FastAPI** bu `checker`'ı şöyle çağırır:

```Python
checker(q="somequery")
```

...ve bunun döndürdüğü her şeyi, *path operation function* içinde `fixed_content_included` parametresine dependency değeri olarak geçirir:

{* ../../docs_src/dependencies/tutorial011_an_py310.py hl[22] *}

/// tip | İpucu

Bunların tamamı biraz yapay görünebilir. Ayrıca bunun nasıl faydalı olduğu da henüz çok net olmayabilir.

Bu örnekler bilerek basit tutuldu; ama mekanizmanın nasıl çalıştığını gösteriyor.

Security bölümlerinde, aynı şekilde implement edilmiş yardımcı function'lar bulunuyor.

Buradaki her şeyi anladıysanız, security için kullanılan bu yardımcı araçların arka planda nasıl çalıştığını da zaten biliyorsunuz demektir.

///

## `yield`, `HTTPException`, `except` ve Background Tasks ile Dependency'ler { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Uyarı

Büyük ihtimalle bu teknik detaylara ihtiyacınız yok.

Bu detaylar, özellikle 0.121.0'dan eski bir FastAPI uygulamanız varsa ve `yield` kullanan dependency'lerle ilgili sorunlar yaşıyorsanız faydalıdır.

///

`yield` kullanan dependency'ler; farklı kullanım senaryolarını kapsamak ve bazı sorunları düzeltmek için zaman içinde evrildi. Aşağıda nelerin değiştiğinin bir özeti var.

### `yield` ve `scope` ile dependency'ler { #dependencies-with-yield-and-scope }

0.121.0 sürümünde FastAPI, `Depends(scope="function")` desteğini ekledi.

`Depends(scope="function")` kullanıldığında, `yield` sonrasındaki çıkış kodu, *path operation function* biter bitmez, response client'a geri gönderilmeden önce çalıştırılır.

`Depends(scope="request")` (varsayılan) kullanıldığında ise `yield` sonrasındaki çıkış kodu, response gönderildikten sonra çalıştırılır.

Daha fazlasını [`yield` ile Dependency'ler - Erken çıkış ve `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope) dokümantasyonunda okuyabilirsiniz.

### `yield` ve `StreamingResponse` ile dependency'ler, Teknik Detaylar { #dependencies-with-yield-and-streamingresponse-technical-details }

FastAPI 0.118.0 öncesinde, `yield` kullanan bir dependency kullanırsanız, *path operation function* döndükten sonra ama response gönderilmeden hemen önce `yield` sonrasındaki çıkış kodu çalıştırılırdı.

Amaç, response'un ağ üzerinden taşınmasını beklerken gereğinden uzun süre resource tutmaktan kaçınmaktı.

Bu değişiklik aynı zamanda şunu da ifade ediyordu: `StreamingResponse` döndürürseniz, `yield` kullanan dependency'nin çıkış kodu zaten çalışmış olurdu.

Örneğin, `yield` kullanan bir dependency içinde bir veritabanı session'ınız varsa, `StreamingResponse` veri stream ederken bu session'ı kullanamazdı; çünkü `yield` sonrasındaki çıkış kodunda session zaten kapatılmış olurdu.

Bu davranış 0.118.0'da geri alındı ve `yield` sonrasındaki çıkış kodunun, response gönderildikten sonra çalıştırılması sağlandı.

/// info | Bilgi

Aşağıda göreceğiniz gibi, bu davranış 0.106.0 sürümünden önceki davranışa oldukça benzer; ancak köşe durumlar için çeşitli iyileştirmeler ve bug fix'ler içerir.

///

#### Erken Çıkış Kodu için Kullanım Senaryoları { #use-cases-with-early-exit-code }

Bazı özel koşullardaki kullanım senaryoları, response gönderilmeden önce `yield` kullanan dependency'lerin çıkış kodunun çalıştırıldığı eski davranıştan fayda görebilir.

Örneğin, `yield` kullanan bir dependency içinde yalnızca bir kullanıcıyı doğrulamak için veritabanı session'ı kullanan bir kodunuz olduğunu düşünün; ama bu session *path operation function* içinde bir daha hiç kullanılmıyor, yalnızca dependency içinde kullanılıyor **ve** response'un gönderilmesi uzun sürüyor. Mesela veriyi yavaş gönderen bir `StreamingResponse` var, ama herhangi bir nedenle veritabanını kullanmıyor.

Bu durumda veritabanı session'ı, response tamamen gönderilene kadar elde tutulur. Ancak session kullanılmıyorsa, bunu elde tutmak gerekli değildir.

Şöyle görünebilir:

{* ../../docs_src/dependencies/tutorial013_an_py310.py *}

`Session`'ın otomatik kapatılması olan çıkış kodu şurada:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

...yavaş veri gönderen response'un gönderimi bittikten sonra çalıştırılır:

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

Ama `generate_stream()` veritabanı session'ını kullanmadığı için, response gönderilirken session'ı açık tutmak aslında gerekli değildir.

SQLModel (veya SQLAlchemy) kullanarak bu spesifik senaryoya sahipseniz, session'a artık ihtiyacınız kalmadıktan sonra session'ı açıkça kapatabilirsiniz:

{* ../../docs_src/dependencies/tutorial014_an_py310.py ln[24:28] hl[28] *}

Böylece session veritabanı bağlantısını serbest bırakır ve diğer request'ler bunu kullanabilir.

`yield` kullanan bir dependency'den erken çıkış gerektiren farklı bir kullanım senaryonuz varsa, lütfen kullanım senaryonuzla birlikte ve `yield` kullanan dependency'ler için erken kapatmadan neden fayda göreceğinizi açıklayarak bir <a href="https://github.com/fastapi/fastapi/discussions/new?category=questions" class="external-link" target="_blank">GitHub Discussion Sorusu</a> oluşturun.

`yield` kullanan dependency'lerde erken kapatma için ikna edici kullanım senaryoları varsa, erken kapatmayı seçmeli (opt-in) hale getiren yeni bir yöntem eklemeyi düşünebilirim.

### `yield` ve `except` ile dependency'ler, Teknik Detaylar { #dependencies-with-yield-and-except-technical-details }

FastAPI 0.110.0 öncesinde, `yield` kullanan bir dependency kullanır, sonra o dependency içinde `except` ile bir exception yakalar ve exception'ı tekrar raise etmezseniz; exception otomatik olarak herhangi bir exception handler'a veya internal server error handler'a raise/forward edilirdi.

Bu davranış 0.110.0 sürümünde değiştirildi. Amaç, handler olmayan (internal server errors) forward edilmiş exception'ların yönetilmemesinden kaynaklanan bellek tüketimini düzeltmek ve bunu normal Python kodunun davranışıyla tutarlı hale getirmekti.

### Background Tasks ve `yield` ile dependency'ler, Teknik Detaylar { #background-tasks-and-dependencies-with-yield-technical-details }

FastAPI 0.106.0 öncesinde, `yield` sonrasında exception raise etmek mümkün değildi; çünkü `yield` kullanan dependency'lerdeki çıkış kodu response gönderildikten *sonra* çalıştırılıyordu. Bu nedenle [Exception Handler'ları](../tutorial/handling-errors.md#install-custom-exception-handlers){.internal-link target=_blank} zaten çalışmış olurdu.

Bu tasarımın ana sebeplerinden biri, background task'lerin içinde dependency'lerin "yield ettiği" aynı objeleri kullanmaya izin vermekti; çünkü çıkış kodu, background task'ler bittikten sonra çalıştırılıyordu.

Bu davranış FastAPI 0.106.0'da, response'un ağ üzerinde taşınmasını beklerken resource tutmamak amacıyla değiştirildi.

/// tip | İpucu

Ek olarak, bir background task normalde ayrı ele alınması gereken bağımsız bir mantık setidir ve kendi resource'larına sahip olmalıdır (ör. kendi veritabanı bağlantısı).

Bu şekilde muhtemelen daha temiz bir kod elde edersiniz.

///

Bu davranışa güvenerek kod yazdıysanız, artık background task'ler için resource'ları background task'in içinde oluşturmalı ve içeride yalnızca `yield` kullanan dependency'lerin resource'larına bağlı olmayan verileri kullanmalısınız.

Örneğin, aynı veritabanı session'ını kullanmak yerine background task içinde yeni bir veritabanı session'ı oluşturur ve veritabanındaki objeleri bu yeni session ile alırsınız. Ardından, background task function'ına veritabanından gelen objeyi parametre olarak geçirmek yerine, o objenin ID'sini geçirir ve objeyi background task function'ı içinde yeniden elde edersiniz.
