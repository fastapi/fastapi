# Arka Plan Görevleri { #background-tasks }

Response döndürüldükten *sonra* çalıştırılacak arka plan görevleri tanımlayabilirsiniz.

Bu, request’ten sonra yapılması gereken; ancak client’ın response’u almadan önce tamamlanmasını beklemesine gerek olmayan işlemler için kullanışlıdır.

Örneğin:

* Bir işlem gerçekleştirdikten sonra gönderilen email bildirimleri:
    * Bir email server’a bağlanmak ve email göndermek genellikle "yavaş" olduğundan (birkaç saniye), response’u hemen döndürüp email bildirimini arka planda gönderebilirsiniz.
* Veri işleme:
    * Örneğin, yavaş bir süreçten geçmesi gereken bir dosya aldığınızı düşünün; "Accepted" (HTTP 202) response’u döndürüp dosyayı arka planda işleyebilirsiniz.

## `BackgroundTasks` Kullanımı { #using-backgroundtasks }

Önce `BackgroundTasks`’i import edin ve *path operation function*’ınızda `BackgroundTasks` tip bildirimi olan bir parametre tanımlayın:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI**, sizin için `BackgroundTasks` tipinde bir obje oluşturur ve onu ilgili parametre olarak geçirir.

## Bir Görev Fonksiyonu Oluşturun { #create-a-task-function }

Arka plan görevi olarak çalıştırılacak bir fonksiyon oluşturun.

Bu, parametre alabilen standart bir fonksiyondur.

`async def` de olabilir, normal `def` de olabilir; **FastAPI** bunu doğru şekilde nasıl ele alacağını bilir.

Bu örnekte görev fonksiyonu bir dosyaya yazacaktır (email göndermeyi simüle ediyor).

Ve yazma işlemi `async` ve `await` kullanmadığı için fonksiyonu normal `def` ile tanımlarız:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## Arka Plan Görevini Ekleyin { #add-the-background-task }

*Path operation function*’ınızın içinde, görev fonksiyonunuzu `.add_task()` metodu ile *background tasks* objesine ekleyin:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` şu argümanları alır:

* Arka planda çalıştırılacak bir görev fonksiyonu (`write_notification`).
* Görev fonksiyonuna sırayla geçirilecek argümanlar (`email`).
* Görev fonksiyonuna geçirilecek keyword argümanlar (`message="some notification"`).

## Dependency Injection { #dependency-injection }

`BackgroundTasks` kullanımı dependency injection sistemiyle de çalışır; `BackgroundTasks` tipinde bir parametreyi birden fazla seviyede tanımlayabilirsiniz: bir *path operation function* içinde, bir dependency’de (dependable), bir sub-dependency’de, vb.

**FastAPI** her durumda ne yapılacağını ve aynı objenin nasıl yeniden kullanılacağını bilir; böylece tüm arka plan görevleri birleştirilir ve sonrasında arka planda çalıştırılır:

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

Bu örnekte, response gönderildikten *sonra* mesajlar `log.txt` dosyasına yazılacaktır.

Request’te bir query varsa, log’a bir arka plan göreviyle yazılır.

Ardından *path operation function* içinde oluşturulan başka bir arka plan görevi, `email` path parametresini kullanarak bir mesaj yazar.

## Teknik Detaylar { #technical-details }

`BackgroundTasks` sınıfı doğrudan <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>’dan gelir.

`fastapi` üzerinden import edebilmeniz ve yanlışlıkla `starlette.background` içindeki alternatif `BackgroundTask`’i (sonunda `s` olmadan) import etmemeniz için FastAPI’nin içine doğrudan import/eklenmiştir.

Sadece `BackgroundTasks` (ve `BackgroundTask` değil) kullanarak, bunu bir *path operation function* parametresi olarak kullanmak ve gerisini **FastAPI**’nin sizin için halletmesini sağlamak mümkündür; tıpkı `Request` objesini doğrudan kullanırken olduğu gibi.

FastAPI’de `BackgroundTask`’i tek başına kullanmak hâlâ mümkündür; ancak bu durumda objeyi kendi kodunuzda oluşturmanız ve onu içeren bir Starlette `Response` döndürmeniz gerekir.

Daha fazla detayı <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">Starlette’in Background Tasks için resmi dokümantasyonunda</a> görebilirsiniz.

## Dikkat Edilmesi Gerekenler { #caveat }

Yoğun arka plan hesaplamaları yapmanız gerekiyorsa ve bunun aynı process tarafından çalıştırılmasına şart yoksa (örneğin memory, değişkenler vb. paylaşmanız gerekmiyorsa), <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a> gibi daha büyük araçları kullanmak size fayda sağlayabilir.

Bunlar genellikle daha karmaşık konfigurasyonlar ve RabbitMQ veya Redis gibi bir mesaj/iş kuyruğu yöneticisi gerektirir; ancak arka plan görevlerini birden fazla process’te ve özellikle birden fazla server’da çalıştırmanıza olanak tanırlar.

Ancak aynı **FastAPI** app’i içindeki değişkenlere ve objelere erişmeniz gerekiyorsa veya küçük arka plan görevleri (email bildirimi göndermek gibi) yapacaksanız, doğrudan `BackgroundTasks` kullanabilirsiniz.

## Özet { #recap }

Arka plan görevleri eklemek için *path operation function*’larda ve dependency’lerde parametre olarak `BackgroundTasks`’i import edip kullanın.
