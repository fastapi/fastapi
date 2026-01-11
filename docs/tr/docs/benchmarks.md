# Kıyaslamalar { #benchmarks }

Bağımsız TechEmpower kıyaslamaları, Uvicorn altında çalışan **FastAPI** uygulamalarının <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">mevcut en hızlı Python frameworklerinden biri</a> olduğunu, sadece Starlette ve Uvicorn'un kendisinin (FastAPI tarafından dahili olarak kullanılır) altında yer aldığını gösteriyor. (*)

Fakat kıyaslamaları ve karşılaştırmaları incelerken şunları aklınızda bulundurmalısınız.

## Kıyaslamalar ve Hız { #benchmarks-and-speed }

Kıyaslamaları incelediğinizde, farklı türlerdeki çeşitli araçların eşdeğer olarak karşılaştırıldığını görmek yaygındır.

Özellikle, (diğer birçok aracın arasında) Uvicorn, Starlette ve FastAPI'ın birlikte karşılaştırıldığını görmek.

Aracın çözdüğü problem ne kadar basitse, performansı o kadar iyi olacaktır. Ve kıyaslamaların çoğu, aracın sağladığı ek özellikleri test etmez.

Hiyerarşi şöyledir:

* **Uvicorn**: bir ASGI sunucusu
    * **Starlette**: (Uvicorn'u kullanır) bir web microframework'ü
        * **FastAPI**: (Starlette'i kullanır) veri doğrulama vb. ile, API'lar oluşturmak için çeşitli ek özelliklere sahip bir API microframework'ü

* **Uvicorn**:
    * Sunucunun kendisi dışında çok fazla ekstra kodu olmadığı için en iyi performansa sahip olacaktır.
    * Uvicorn'da doğrudan bir uygulama yazmazsınız. Bu, kodunuzun en azından Starlette'in (veya **FastAPI**'ın) sağladığı tüm kodu az çok içermesi gerektiği anlamına gelir. Ve eğer bunu yaptıysanız, nihai uygulamanız bir framework kullanmanın ve uygulama kodunuzu ve bug'ları en aza indirmenin aynı ek yüküne sahip olacaktır.
    * Uvicorn'u karşılaştırıyorsanız, onu Daphne, Hypercorn, uWSGI, vb. application server'lara karşı karşılaştırın.
* **Starlette**:
    * Uvicorn'dan sonra bir sonraki en iyi performansa sahip olacaktır. Aslında, Starlette çalışmak için Uvicorn'u kullanır. Dolayısıyla, daha fazla kod çalıştırmak zorunda olduğundan muhtemelen Uvicorn'dan yalnızca "daha yavaş" olabilir.
    * Ancak path'lere dayalı routing, vb. ile basit web uygulamaları oluşturmanız için size araçlar sağlar.
    * Starlette'i karşılaştırıyorsanız, Sanic, Flask, Django, vb. web frameworkleri (veya microframeworkler) ile karşılaştırın.
* **FastAPI**:
    * Starlette'in Uvicorn'u kullanıp ondan daha hızlı olamamasıyla aynı şekilde, **FastAPI** Starlette'i kullanır, dolayısıyla ondan daha hızlı olamaz.
    * FastAPI, Starlette'in üzerine daha fazla özellik sağlar. Veri doğrulama ve serialization gibi, API'lar oluştururken neredeyse her zaman ihtiyaç duyduğunuz özellikler. Ve bunu kullanarak, ücretsiz olarak otomatik dokümantasyon elde edersiniz (otomatik dokümantasyon çalışan uygulamalara ek yük bile getirmez, başlangıçta üretilir).
    * FastAPI'ı kullanmadıysanız ve Starlette'i doğrudan kullandıysanız (veya Sanic, Flask, Responder, vb. gibi başka bir araç) tüm veri doğrulama ve serialization'ı kendiniz uygulamak zorunda kalırdınız. Dolayısıyla, nihai uygulamanız FastAPI kullanılarak oluşturulmuş gibi hâlâ aynı ek yüke sahip olacaktır. Ve birçok durumda, bu veri doğrulama ve serialization, uygulamalarda yazılan kodun en büyük kısmıdır.
    * Dolayısıyla, FastAPI'ı kullanarak geliştirme süresinden, bug'lardan, kod satırlarından tasarruf edersiniz ve muhtemelen onu kullanmadığınız durumda elde edeceğiniz performansın aynısını (veya daha iyisini) elde edersiniz (çünkü her şeyi kodunuzda uygulamak zorunda kalırdınız).
    * FastAPI'ı karşılaştırıyorsanız, veri doğrulama, serialization ve dokümantasyon sağlayan bir web uygulaması framework'ü (veya araç seti) ile, Flask-apispec, NestJS, Molten, vb. gibi, entegre otomatik veri doğrulama, serialization ve dokümantasyona sahip frameworklerle karşılaştırın.
