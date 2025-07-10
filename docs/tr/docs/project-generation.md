# Proje oluşturma - Şablonlar

Başlamak için bir proje oluşturucu kullanabilirsiniz, çünkü sizin için önceden yapılmış birçok başlangıç ​​kurulumu, güvenlik, veritabanı ve temel API endpoinlerini içerir.

Bir proje oluşturucu, her zaman kendi ihtiyaçlarınıza göre güncellemeniz ve uyarlamanız gereken esnek bir kuruluma sahip olacaktır, ancak bu, projeniz için iyi bir başlangıç ​​noktası olabilir.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Özellikler

* Full **Docker** entegrasyonu (Docker based).
* Docker Swarm Mode ile deployment.
* **Docker Compose** entegrasyonu ve lokal geliştirme için optimizasyon.
* Uvicorn ve Gunicorn ile **Production ready** Python web server'ı.
* Python <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend:
    * **Hızlı**: **NodeJS** ve **Go** ile eşit, çok yüksek performans (Starlette ve Pydantic'e teşekkürler).
    * **Sezgisel**: Editor desteğı. <abbr title="auto-complete, IntelliSense gibi isimlerle de bilinir">Otomatik tamamlama</abbr>. Daha az debugging.
    * **Kolay**: Kolay öğrenip kolay kullanmak için tasarlandı. Daha az döküman okuma daha çok iş.
    * **Kısa**: Minimum kod tekrarı. Her parametre bildiriminde birden çok özellik.
    * **Güçlü**: Production-ready. Otomatik interaktif dökümantasyon.
    * **Standartlara dayalı**: API'ler için açık standartlara dayanır (ve tamamen uyumludur): <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> ve <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Şeması</a>.
    * <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**Birçok diger özelliği**</a> dahili otomatik doğrulama, serialization, interaktif dokümantasyon, OAuth2 JWT token ile authentication, vb.
* **Güvenli şifreleme** .
* **JWT token** kimlik doğrulama.
* **SQLAlchemy** models (Flask dan bağımsızdır. Celery worker'ları ile kullanılabilir).
* Kullanıcılar için temel başlangıç ​​modeli (gerektiği gibi değiştirin ve kaldırın).
* **Alembic** migration.
* **CORS** (Cross Origin Resource Sharing).
* **Celery** worker'ları ile backend içerisinden seçilen işleri çalıştırabilirsiniz.
* **Pytest**'e dayalı, Docker ile entegre REST backend testleri ile veritabanından bağımsız olarak tam API etkileşimini test edebilirsiniz. Docker'da çalıştığı için her seferinde sıfırdan yeni bir veri deposu oluşturabilir (böylece ElasticSearch, MongoDB, CouchDB veya ne istersen kullanabilirsin ve sadece API'nin çalışıp çalışmadığını test edebilirsin).
* Atom Hydrogen veya Visual Studio Code Jupyter gibi uzantılarla uzaktan veya Docker içi geliştirme için **Jupyter Çekirdekleri** ile kolay Python entegrasyonu.
* **Vue** ile frontend:
    * Vue CLI ile oluşturulmuş.
    * Dahili **JWT kimlik doğrulama**.
    * Dahili Login.
    * Login sonrası, Kontrol paneli.
    * Kullanıcı oluşturma ve düzenleme kontrol paneli
    * Kendi kendine kullanıcı sürümü.
    * **Vuex**.
    * **Vue-router**.
    * **Vuetify** güzel material design kompanentleri için.
    * **TypeScript**.
    * **Nginx** tabanlı Docker sunucusu (Vue-router için yapılandırılmış).
    * Docker ile multi-stage yapı, böylece kodu derlemeniz, kaydetmeniz veya işlemeniz gerekmez.
    * Derleme zamanında Frontend testi (devre dışı bırakılabilir).
    * Mümkün olduğu kadar modüler yapılmıştır, bu nedenle kutudan çıktığı gibi çalışır, ancak Vue CLI ile yeniden oluşturabilir veya ihtiyaç duyduğunuz şekilde oluşturabilir ve istediğinizi yeniden kullanabilirsiniz.
* **PGAdmin** PostgreSQL database admin tool'u, PHPMyAdmin ve MySQL ile kolayca değiştirilebilir.
* **Flower** ile Celery job'larını monitörleme.
* **Traefik** ile backend ve frontend arasında yük dengeleme, böylece her ikisini de aynı domain altında, path ile ayrılmış, ancak farklı kapsayıcılar tarafından sunulabilirsiniz.
* Let's Encrypt **HTTPS** sertifikalarının otomatik oluşturulması dahil olmak üzere Traefik entegrasyonu.
* GitLab **CI** (sürekli entegrasyon), backend ve frontend testi dahil.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **UYARI** ⚠️

Sıfırdan bir projeye başlıyorsanız alternatiflerine bakın.

Örneğin,  <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a> daha iyi bir alternatif olabilir, aktif olarak geliştiriliyor ve kullanılıyor. Ve yeni özellik ve ilerlemelere sahip.

İsterseniz Couchbase tabanlı generator'ı kullanmakta özgürsünüz, hala iyi çalışıyor olmalı ve onunla oluşturulmuş bir projeniz varsa bu da sorun değil (ve muhtemelen zaten ihtiyaçlarınıza göre güncellediniz).

Bununla ilgili daha fazla bilgiyi repo belgelerinde okuyabilirsiniz.

## Full Stack FastAPI MongoDB

... müsaitliğime ve diğer faktörlere bağlı olarak daha sonra gelebilir. 😅 🎉

## Machine Learning modelleri, spaCy ve FastAPI

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### Machine Learning modelleri, spaCy ve FastAPI - Features

* **spaCy** NER model entegrasyonu.
* **Azure Cognitive Search** yerleşik istek biçimi.
* Uvicorn ve Gunicorn ile **Production ready** Python web server'ı.
* Dahili **Azure DevOps** Kubernetes (AKS) CI/CD deployment.
* **Multilingual**, Proje kurulumu sırasında spaCy'nin yerleşik dillerinden birini kolayca seçin.
* **Esnetilebilir** diğer frameworkler (Pytorch, Tensorflow) ile de çalışır sadece spaCy değil.
