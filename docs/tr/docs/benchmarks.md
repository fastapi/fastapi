# Kıyaslamalar { #benchmarks }

Bağımsız TechEmpower kıyaslamaları, Uvicorn altında çalışan **FastAPI** uygulamalarının <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">mevcut en hızlı Python frameworklerinden biri</a> olduğunu; yalnızca Starlette ve Uvicorn’un kendilerinin (FastAPI tarafından dahili olarak kullanılır) altında kaldığını gösteriyor.

Ancak kıyaslamaları ve karşılaştırmaları incelerken şunları aklınızda bulundurmalısınız.

## Kıyaslamalar ve Hız { #benchmarks-and-speed }

Kıyaslamaları incelediğinizde, farklı türlerdeki birçok aracın eşdeğer kabul edilerek karşılaştırıldığını görmek yaygındır.

Özellikle, (diğer birçok aracın arasında) Uvicorn, Starlette ve FastAPI’ın birlikte karşılaştırıldığını görebilirsiniz.

Aracın çözdüğü problem ne kadar basitse, elde edeceği performans o kadar iyi olur. Ayrıca kıyaslamaların çoğu, aracın sağladığı ek özellikleri test etmez.

Hiyerarşi şöyledir:

* **Uvicorn**: bir ASGI sunucusu
    * **Starlette**: (Uvicorn’u kullanır) bir web microframework’ü
        * **FastAPI**: (Starlette’i kullanır) API’lar oluşturmak için veri doğrulama vb. çeşitli ek özelliklere sahip bir API microframework’ü

* **Uvicorn**:
    * Sunucunun kendisi dışında çok fazla ekstra kod içermediği için en iyi performansa sahip olacaktır.
    * Doğrudan Uvicorn ile bir uygulama yazmazsınız. Bu, yazdığınız kodun en azından Starlette’in (veya **FastAPI**’ın) sağladığı kodların aşağı yukarı tamamını içermesi gerektiği anlamına gelir. Bunu yaptığınızda, son uygulamanız bir framework kullanmış olmanın getirdiği aynı overhead’e sahip olur; uygulama kodunuzu ve bug’ları en aza indirirsiniz.
    * Uvicorn’u karşılaştırıyorsanız, onu Daphne, Hypercorn, uWSGI vb. Application server’larla karşılaştırın.
* **Starlette**:
    * Uvicorn’dan sonra en iyi performansa sahip olacaktır. Aslında Starlette çalışmak için Uvicorn’u kullanır. Bu yüzden, daha fazla kod çalıştırmak zorunda olduğundan muhtemelen Uvicorn’dan yalnızca "daha yavaş" olabilir.
    * Ancak path’lere göre routing vb. ile basit web uygulamaları oluşturmanız için araçlar sağlar.
    * Starlette’i karşılaştırıyorsanız, Sanic, Flask, Django vb. web framework’leri (veya microframework’ler) ile karşılaştırın.
* **FastAPI**:
    * Starlette’in Uvicorn’u kullanıp ondan daha hızlı olamaması gibi, **FastAPI** da Starlette’i kullanır; dolayısıyla ondan daha hızlı olamaz.
    * FastAPI, Starlette’in üzerine daha fazla özellik ekler. API’lar oluştururken neredeyse her zaman ihtiyaç duyduğunuz veri doğrulama ve serialization gibi özellikler. Ayrıca bunu kullanarak ücretsiz olarak otomatik dokümantasyon elde edersiniz (otomatik dokümantasyon, çalışan uygulamalara overhead bile eklemez; startup’ta üretilir).
    * FastAPI’ı kullanmayıp Starlette’i doğrudan kullansaydınız (veya Sanic, Flask, Responder vb. başka bir aracı), tüm veri doğrulama ve serialization işlerini kendiniz implement etmek zorunda kalırdınız. Bu yüzden, son uygulamanız yine FastAPI kullanılarak oluşturulmuş gibi aynı overhead’e sahip olurdu. Ve çoğu durumda, veri doğrulama ve serialization uygulamalarda yazılan kodun en büyük kısmını oluşturur.
    * Dolayısıyla, FastAPI kullanarak geliştirme süresinden, bug’lardan, kod satırlarından tasarruf edersiniz; ayrıca muhtemelen, onu kullanmasaydınız elde edeceğiniz performansın aynısını (veya daha iyisini) elde edersiniz (çünkü her şeyi kodunuzda implement etmek zorunda kalırdınız).
    * FastAPI’ı karşılaştırıyorsanız, veri doğrulama, serialization ve dokümantasyon sağlayan bir web uygulaması framework’ü (veya araç seti) ile karşılaştırın; örn. Flask-apispec, NestJS, Molten vb. Entegre otomatik veri doğrulama, serialization ve dokümantasyona sahip framework’ler.
