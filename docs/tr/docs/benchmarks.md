# Kıyaslamalar { #benchmarks }

Bağımsız TechEmpower kıyaslamaları, Uvicorn altında çalışan **FastAPI** uygulamalarının <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">mevcut en hızlı Python frameworklerinden biri</a> olduğunu, yalnızca Starlette ve Uvicorn'un kendilerinin altında yer aldığını gösteriyor (FastAPI bunları dahili olarak kullanır).

Fakat kıyaslamaları ve karşılaştırmaları incelerken şunları aklınızda bulundurmalısınız.

## Kıyaslamalar ve Hız { #benchmarks-and-speed }

Kıyaslamalara baktığınızda, farklı türlerdeki birkaç aracın eşdeğermiş gibi karşılaştırıldığını görmek yaygındır.

Özellikle, (diğer birçok araç arasında) Uvicorn, Starlette ve FastAPI'ın birlikte karşılaştırıldığını görebilirsiniz.

Aracın çözdüğü problem ne kadar basitse, elde edeceği performans o kadar iyi olur. Ayrıca kıyaslamaların çoğu, aracın sağladığı ek özellikleri test etmez.

Hiyerarşi şöyledir:

* **Uvicorn**: bir ASGI sunucusu
    * **Starlette**: (Uvicorn'u kullanır) bir web mikroframework'ü
        * **FastAPI**: (Starlette'i kullanır) veri doğrulama vb. ile API'lar oluşturmak için çeşitli ek özelliklere sahip bir API mikroframework'ü

* **Uvicorn**:
    * Sunucunun kendisi dışında çok fazla ekstra kod içermediği için en iyi performansa sahip olacaktır.
    * Uvicorn ile doğrudan bir uygulama yazmazsınız. Bu, kodunuzun en azından Starlette'in (veya **FastAPI**'ın) sağladığı kodun aşağı yukarı tamamını içermesi gerektiği anlamına gelir. Bunu yaparsanız, nihai uygulamanız; bir framework kullanmış olmanın ve uygulama kodunu ve bug'ları en aza indirmenin getirdiği ek yükle aynı ek yüke sahip olur.
    * Uvicorn'u karşılaştırıyorsanız, Daphne, Hypercorn, uWSGI vb. application server'larla karşılaştırın.
* **Starlette**:
    * Uvicorn'dan sonra en iyi performansa sahip olacaktır. Aslında Starlette çalışmak için Uvicorn'u kullanır. Bu yüzden muhtemelen yalnızca daha fazla kod çalıştırmak zorunda kaldığı için Uvicorn'dan "daha yavaş" olabilir.
    * Ancak path tabanlı routing vb. ile basit web uygulamaları oluşturmanız için araçlar sağlar.
    * Starlette'i karşılaştırıyorsanız, Sanic, Flask, Django vb. web framework'lerle (veya mikroframework'lerle) karşılaştırın.
* **FastAPI**:
    * Starlette'in Uvicorn'u kullanıp ondan daha hızlı olamaması gibi, **FastAPI** da Starlette'i kullanır; dolayısıyla ondan daha hızlı olamaz.
    * FastAPI, Starlette'in üzerine daha fazla özellik sağlar. API'lar oluştururken neredeyse her zaman ihtiyaç duyduğunuz veri doğrulama ve <abbr title="serialization - serileştirme">serialization</abbr> gibi özellikler. Ayrıca bunu kullanarak ücretsiz olarak otomatik dokümantasyon elde edersiniz (otomatik dokümantasyon, çalışan uygulamalara ek yük bile getirmez; startup'ta üretilir).
    * FastAPI'ı kullanmayıp Starlette'i doğrudan kullansaydınız (veya Sanic, Flask, Responder vb. başka bir aracı), tüm veri doğrulama ve serialization işlemlerini kendiniz uygulamak zorunda kalırdınız. Dolayısıyla nihai uygulamanız, FastAPI kullanılarak inşa edilmiş olsaydı sahip olacağı ek yükle hâlâ aynı ek yüke sahip olurdu. Ve çoğu durumda, uygulamalarda yazılan en büyük kod miktarı veri doğrulama ve serialization kısmıdır.
    * Bu nedenle FastAPI kullanarak geliştirme süresinden, bug'lardan, kod satırlarından tasarruf edersiniz; ayrıca muhtemelen, onu kullanmasaydınız (tüm bunları kodunuzda kendiniz uygulamak zorunda kalacağınız için) elde edeceğiniz performansın aynısını (veya daha iyisini) elde edersiniz.
    * FastAPI'ı karşılaştırıyorsanız, Flask-apispec, NestJS, Molten vb. veri doğrulama, serialization ve dokümantasyon sağlayan bir web uygulaması framework'ü (veya araç seti) ile karşılaştırın. Entegre otomatik veri doğrulama, serialization ve dokümantasyona sahip framework'ler.
