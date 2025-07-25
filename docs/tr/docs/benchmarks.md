# Kıyaslamalar

Bağımsız TechEmpower kıyaslamaları gösteriyor ki <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">en hızlı Python frameworklerinden birisi</a> olan Uvicorn ile çalıştırılan **FastAPI** uygulamaları, sadece Starlette ve Uvicorn'dan daha düşük sıralamada (FastAPI bu frameworklerin üzerine kurulu) yer alıyor. (*)

Fakat kıyaslamaları ve karşılaştırmaları incelerken şunları aklınızda bulundurmalısınız.

## Kıyaslamalar ve Hız

Kıyaslamaları incelediğinizde, farklı özelliklere sahip araçların eşdeğer olarak karşılaştırıldığını yaygın bir şekilde görebilirsiniz.

Özellikle, (diğer birçok araç arasında) Uvicorn, Starlette ve FastAPI'ın birlikte karşılaştırıldığını görebilirsiniz.

Aracın çözdüğü problem ne kadar basitse, performansı o kadar iyi olacaktır. Ancak kıyaslamaların çoğu, aracın sağladığı ek özellikleri test etmez.

Hiyerarşi şöyledir:

* **Uvicorn**: bir ASGI sunucusu
    * **Starlette**: (Uvicorn'u kullanır) bir web mikroframeworkü
        * **FastAPI**: (Starlette'i kullanır) veri doğrulama vb. çeşitli ek özelliklere sahip, API oluşturmak için kullanılan bir API mikroframeworkü

* **Uvicorn**:
    * Sunucunun kendisi dışında ekstra bir kod içermediği için en iyi performansa sahip olacaktır.
    * Doğrudan Uvicorn ile bir uygulama yazmazsınız. Bu, yazdığınız kodun en azından Starlette tarafından sağlanan tüm kodu (veya **FastAPI**) az çok içermesi gerektiği anlamına gelir. Eğer bunu yaptıysanız, son uygulamanız bir framework kullanmak ve uygulama kodlarını ve hataları en aza indirmekle aynı ek yüke sahip olacaktır.
    * Eğer Uvicorn'u karşılaştırıyorsanız, Daphne, Hypercorn, uWSGI, vb. uygulama sunucuları ile karşılaştırın.
* **Starlette**:
    * Uvicorn'dan sonraki en iyi performansa sahip olacaktır. İşin aslı, Starlette çalışmak için Uvicorn'u kullanıyor. Dolayısıyla, daha fazla kod çalıştırmaası gerektiğinden muhtemelen Uvicorn'dan sadece "daha yavaş" olabilir.
    * Ancak yol bazlı yönlendirme vb. basit web uygulamaları oluşturmak için araçlar sağlar.
    * Eğer Starlette'i karşılaştırıyorsanız, Sanic, Flask, Django, vb. frameworkler (veya mikroframeworkler) ile karşılaştırın.
* **FastAPI**:
    * Starlette'in Uvicorn'u kullandığı ve ondan daha hızlı olamayacağı gibi, **FastAPI**'da Starlette'i kullanır, dolayısıyla ondan daha hızlı olamaz.
    * FastAPI, Starlette'e ek olarak daha fazla özellik sunar. Bunlar veri doğrulama ve <abbr title="Dönüşüm: serialization, parsing, marshalling olarak da biliniyor">dönüşümü</abbr> gibi API'lar oluştururken neredeyse ve her zaman ihtiyaç duyduğunuz özelliklerdir. Ve bunu kullanarak, ücretsiz olarak otomatik dokümantasyon elde edersiniz (otomatik dokümantasyon çalışan uygulamalara ek yük getirmez, başlangıçta oluşturulur).
    * FastAPI'ı kullanmadıysanız ve Starlette'i doğrudan kullandıysanız (veya başka bir araç, Sanic, Flask, Responder, vb.) tüm veri doğrulama ve dönüştürme araçlarını kendiniz geliştirmeniz gerekir. Dolayısıyla, son uygulamanız FastAPI kullanılarak oluşturulmuş gibi hâlâ aynı ek yüke sahip olacaktır. Çoğu durumda, uygulamalarda yazılan kodun büyük bir kısmını veri doğrulama ve dönüştürme kodları oluşturur.
    * Dolayısıyla, FastAPI'ı kullanarak geliştirme süresinden, hatalardan, kod satırlarından tasarruf edersiniz ve kullanmadığınız durumda (birçok özelliği geliştirmek zorunda kalmakla birlikte) muhtemelen aynı performansı (veya daha iyisini) elde ederdiniz.
    * Eğer FastAPI'ı karşılaştırıyorsanız, Flask-apispec, NestJS, Molten, vb. gibi veri doğrulama, dönüştürme ve dokümantasyon sağlayan bir web uygulaması frameworkü ile (veya araç setiyle) karşılaştırın.
