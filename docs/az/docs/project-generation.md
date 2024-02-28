# Proyekt Yaradılması - Şablon

Bu şablonu istifadə edə bilərsiniz, çünki bu sizə əvvəlcədən qurulmuş tənzimləmələri, təhlükəsizlik, verilənlər bazası və bəzi API nöqtələrini təqdim edir.

Siz öz ehtiyac və tələblərinizə uyğun olaraq tənzimləmələri yeniləməli və uyğunlaşdırmalısınız, amma bu sizin proyektiniz üçün yaxşı bir başlanğıc nöqtəsi ola bilər.

## Full Stack FastAPI PostgreSQL

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-postgresql</a>

### Full Stack FastAPI PostgreSQL - Xüsusiyyətlər

* Tam **Docker** inteqrasiyası (Docker əsaslı).
* Docker Swarm Mode quraşdırılması.
* Lokal təkmilləşdirmə üçün **Docker Compose** inteqrasiya və optimallaşdırma.
* Uvicorn və Gunicorn istifadə edərək **İstehsal üçün hazır** Python veb serveri.
* Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend:
    * **Sürətli**: NodeJS və Go ilə müqayisə oluna bilən çox yüksək performans (Starlette və Pydantic sayəsində).
    İntuitiv: . Hər yerdə tamamlama. Sazlama üçün daha az vaxt.
    * **İntuitiv**: Əla redaktor dəstəyi. <abbr title="avtomatik tamamlama, IntelliSense kimi də bilinir">Tamamlama</abbr> hər yerdə. Sazlama üçün daha az vaxt sərfi.
    * **Asan**: İstifadəsi və öyrənilməsi asan olaraq üçün nəzərdə tutulmuşdur. Sənədləri oxumaq üçün daha az vaxt sərfi.
    * **Möhkəm**: Avtomatik interaktiv sənədlərlə istehsala hazır kod.
    * **Standartlara əsaslanan**: "API"lar üçün açıq standartlara (və tam uyğun) əsaslanır: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> and <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Sxema</a>.
    * Avtomatik doğrulama, seriallaşdırma, interaktiv sənədlər, OAuth2 JWT tokenləri ilə autentifikasiya və <a href="https://fastapi.tiangolo.com/features/" class="external-link" target="_blank">**bir çox digər xüsusiyyətlər**</a>
    Standart olaraq təhlükəsiz parol hashing
* Standart olaraq **təhlükəsiz şifrə** "hash"ləmə.
* **JWT token** identifikasiyası.
* **SQLAlchemy** modelləri (Flask uzantılarından asılı olmayaraq, onlar birbaşa Celery "worker"ləri ilə istifadə oluna bilər).
* İstifadəçilər üçün əsas başlanğıc modelləri (lazım olduqda dəyişdirilə və silinə bilən).
* **Alembic** miqrasiyalar.
* **CORS** (Cross Origin Resource Sharing).
* "Backend"dən modelləri və kodu import və istifadə edə bilən **Celery** "worker"ləri.
* **Pytest** əsasında REST backend testləri, Docker ilə inteqrasiya edilmiş, beləliklə siz verilənlər bazasından asılı olmayaraq "API"ı tamamilə test edə bilərsiniz. "Docker"də işlədiyi üçün, o hər dəfə sıfırdan məlumat bazası yarada bilir (bunun üçün ElasticSearch, MongoDB, CouchDB, və ya istədiyiniz bir şey istifadə edə və "API"ın işlədiyini test edə bilərsiniz).
* Atom Hydrogen və ya Visual Studio Code Jupyter kimi uzantılarla uzaqdan və ya "Docker"də təkmilləşdirmə üçün **Jupyter Kernels** ilə asan Python inteqrasiyası.
* **Vue** frontend:
    * Vue CLI ilə yaradılıb.
    * **JWT Authentication** dəstəyi.
    * Giriş səhifəsi.
    * Giriş etdikdən sonra, əsas idarə paneli səhifəsi.
    * İdarə panelində istifadə yaratma və düzəliş etmə.
    * İstifadəçinin özünü redaktə etməsi.
    * **Vuex**.
    * **Vue-router**.
    * Əla material dizayn komponentləri üçün **Vuetify**.
    * **TypeScript**.
    * **Nginx** əsasında Docker server (Vue-router ilə kodlama üçün konfiqurasiya).
    * Docker multi-stage qurulma, ona görə də tərtib edilmiş kodu yadda saxlamağa ehtiyac yoxdur.
    * Qurulma zamanı Frontend testlərinin işləməsi (istəyə bağlı olaraq söndürülə bilər).
    * Mümkün qədər modullaşdırılmışdır, lakin siz Vue CLI ilə yenidən yarada və istədiyiniz qədər istifadə edə bilərsiniz.

* PostgreSQL verilənlər bazası üçün **PGAdmin**, PHPMyAdmin və "MySQL"dən asanlıqla istifadə etmək üçün onu dəyişdirə bilərsiniz
* Celery işlərinin monitorinqi üçün **Flower**.
* **Traefik** ilə frontend və backend arasında yük balansı, beləliklə sizin eyni domen altında, lakin müxtəlif konteynerlərdə olan frontend və backend tətbiqiniz ola bilər.
* Traefik inteqrasiyası, o cümlədən Let's Encrypt **HTTPS** sertifikatlarının avtomatik yaradılması.
* GitLab **CI** (davamlı inteqrasiya), o cümlədən frontend və backend testi.

## Full Stack FastAPI Couchbase

GitHub: <a href="https://github.com/tiangolo/full-stack-fastapi-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-fastapi-couchbase</a>

⚠️ **XƏBƏRDARLIQ** ⚠️

Əgər siz sıfırdan yeni bir proyekt başladırsınızsa, buradakı alternativləri yoxlayın.

Məsələn, <a href="https://github.com/tiangolo/full-stack-fastapi-postgresql" class="external-link" target="_blank">Full Stack FastAPI PostgreSQL</a> proyekt yaradıcısı daha yaxşı bir alternativ ola bilər, çünki aktiv olaraq idarə olunur, istifadə olunur və ona bütün yeni xüsusiyyətlər və təkmilləşmələr daxildir.

Əgər siz Couchbase ilə proyekt yaratmaq istəyirsinizsə, siz bu şablonu istifadə edə bilərsiniz və bu yəqin ki, sizə kömək edəcək. Amma əgər sizin artıq bu şablonla yaradılmış proyektiniz varsa, o da yaxşı işləyəcək və siz yəqin ki, onu öz tələblərinizə uyğunlaşdırmışsınız.

Bu barədə daha çox məlumat əldə etmək üçün repoya aid sənədlərə baxa bilərsiniz.

## Full Stack FastAPI MongoDB

...vaxtımın mövcudluğuna və digər faktorlara bağlı olaraq daha sonra gələ bilər. 😅 🎉

## spaCy və FastAPI ilə Maşın Öyrənmə modelləri

GitHub: <a href="https://github.com/microsoft/cookiecutter-spacy-fastapi" class="external-link" target="_blank">https://github.com/microsoft/cookiecutter-spacy-fastapi</a>

### spaCy və FastAPI ilə Maşın Öyrənmə modelləri - Xüsusiyyətlər

* **spaCy** NER model inteqrasiyası.
* **Azure Cognitive Search** daxili sorğu formatı.
* Uvicorn və Gunicorn istifadə edərək **İstehsal üçün hazır** Python veb serveri.
* **Azure DevOps** Kubernetes (AKS) CI/CD daxili quraşdırılması.
* **Çoxdilli** Layihənin qurulması zamanı "spaCy"nin daxili dillərindən birinin asanlıqla seçilməsi.
* Yalnız spaCy deyil, digər model "framework"lərə (Pytorch, Tensorflow) **asanlıqla genişləndiriləbilən** olması.
