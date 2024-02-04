# Xüsusiyyətlər

## FastAPI xüsusiyyətləri

**FastAPI** sizə aşağıdakıları təmin edir:

### Açıq standartlara əsaslanır

* API yaratmaq işlərində <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI </strong></a> buna <abbr title="also known as: endpoints, routes">path </abbr> <abbr title=" HTTP metodları olaraq bilinən, POST, GET, PUT, DELETE">əməliyyatları, </abbr>parametrləri, body tələbi, təhlükəsizlik kim şeylər daxildir.
* Avtomatik olaraq data modelinin <a href="http://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema </strong></a> ile birlikdə sənədləşməsi(OpenAPI özü onsuz JSON Schema əsasındadır).
* Diqqətli iş nəticəsində yuxarıda göstərilən standartlara uyğun bir framework yaratdıq. Standartları tortun üzərinə sonradan əlavə edilən çiyələk kimi görmədik.
* Bu həmçinin bir çox dildə istifadə oluna biləcək **client code generator** istifadəsinə də icazə verir.

### Avtomatik sənədləşmə

OpenAPI standartlarına əsaslanan bir framework olaraq, developerlərin birdən çox seçimi var, defolt olaraq gələn 2 fərqli interaktiv API sənədləşməsi və veb istifadəçi interfeysi var.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI </strong></a> sizə interaktiv olaraq brauzerdən API-ya çağırış etməyə və sınaqdan keçirməyə imkan verir.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc </strong></a> ilə alternativ API sənədləşməsi.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Sadəcə müasir Python

Tamamilə standartlar **Python 3.8**'nın type hintlərinə əsaslanır (Pydantic'in sayəsində). Yeni bir sintaksis öyrənməyə ehtiyyac yoxdur. Sadəcə müasir Python.

Əgər Python type hintlərini bilmirsinizsə vəya bir xatırlatmaya ehtiyyacınız varsa (FastAPI istifadə etməsən belə) bu iki dəqiqəlik kiçik məlumatlandırıcı məzmuna göz ata bilərsiz: [Python Types](python-types.md){.internal-link target=_blank}.

Standart Python'u typelarını istifadə edərək yazırsız:

```Python
from typing import List, Dict
from datetime import date

from pydantic import BaseModel

# Dəyişəni str olarak tanıdın
# və o funksiya üçün super bir editor dəstəyi alın
def main(user_id: str):
    return user_id


# Pydantic modeli
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Sonrasında bu formada istifadə edə bilərsiz.

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` mənası:

    `second_user_data` içində olan key-value -ları birbaşa olaraq key-value arqumentləri kimi ötürür , etdiyin şey buna bərabər olacaq:`User(id=4, name="Mary", joined="2018-11-30")`

### Editor dəstəyi

Bütün framework istifadəsi asan və intuitiv olmaq üçün hazırlanmışdır, qəbul edilmiş bütün qərarlar developerlə ən yaxşı inkişaf təcrübəsini yaşatmaq üçün, bir çox editorlarda sınaqdan keçirilmişdir.

Python developerləri arasında son sorğuda, açıq ara <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">Ən çox istifadə edilən xüsusiyyət "avtomatik tamamlama" idi.</a>.

Bütün **FastAPI** frameworkü avto-tamamlama baxımından developeri məmnun etmək üçün hazırlandı. Avtomatik tamamlama hər yerdə işləyir.

Çox nadir hallarda sənədləşməyə qayıdıb baxacaqsınız.

Editorun sizə necə kömək etdiyinə baxın:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code </a> ilə:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm </a> ilə:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Daha əvvəl qeyri-mümkün hesab edə biləcəyiniz kodda belə avto tamamlama görəcəksiniz. Nümunə olaraq `price` JSON body içində (nested bir JSON body də ola bilərdi.) birbaşa olaraq request-dən gəlir, bu vəziyyətdə belə avto-tammalama iş görür.

Artıq key adlarını səhv yazmayın, sənədləşməyə dönüb dəlilər kimi yuxarı aşağı səyfədə gəzmək ve ən sonunda `username` mi yoxsa `user_name` mi isitfadə etdim kimi suallar yoxdur.

### Qısa

Hər şey üçün məntiqli bird defolt var. Parametrlərini istəyə uyğun olarak dəyişib, API'nı istədiyin kimi dəyişə bilərsiz.

Defolt olaraq hamısı **işləyir**.

### Doğrulama

* Deməy olar ki bütün (ya da hamısı?) Python **data typeları** için doğrulama, əhatə etdikləri:

  * JSON obyektləri(`dict`).
  * JSON array (`list`) item type'ı tanıdarkən.
  * String (`str`) parametri, minimum ve maksimum uzunluq kimi məhdudiyyətlər edərkən.
  * Nömrələr (`int`, `float`) maksimum ve kimi məhdudiyyətlər edərkən.
* Bunlar kimi ən eqzotik typelarla belə doğrulama edə bilərsiniz.:

  * URL.
  * Email.
  * UUID.
  * ...ve digərləri.

Bütün yoxlama tədbirləri çox güclü kitabxana sayəsində həyata keçirilir, **Pydantic**.

### Təhlükəsizlik ve autentifikasiya

Təhlükəsizlik və autentifikasiya verilənlər bazası və məlumat modellərinə zərər vermədən inteqrasiya oluna bilər.

Bütün təhlükəsizlik sxemləri OpenAPI-də müəyyən edilmişdir, bunlara daxildir:

* HTTP Basic.
* **OAuth2** (ve **JWT tokenləri ilə** birlikdə). Bu dərslik məzmununu yoxlaya bilərsiniz [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API açarları:
  * Headerlar.
  * Query parametrləri.
  * Cookies, vs.

Bütün təhlükəsizlik xüsusiyyətləri Starlette-dən gəlir (**session cookies'de** daxil olmaqla).

Bütün təkrar istifadə edilə bilən alətlər və komponentlər kimi, rahatlıqla sistemlərinizə, data storelarınıza, əlaqəli və NoSQL databaselərinizə inteqrasiya edə biləcəyiniz şəkildə hazırlandı.

### Dependency injection

FastAPI-nin istifadəsi inanılmaz dərəcədə asan, lakin inanılmaz dərəcədə güclü  <abbr title='"components", "resources", "services", "providers" olaraq da bilinən'><strong>Dependency Injection </strong></abbr> sistemi var.

* Dependencylərin belə dependencies-i olabilər, FastAPI bunun  üçün **graph of "dependency"** yaradır.
* Bütün bunlar **avtomatik olaraq** FastAPI tərəfindən həlledilir.
* Daxil olan məlumatlardan asılı olaraq bütün öhdəliklərin fərqli tələbləri ola bilər, əlavə path əməliyyatlarının məhdudiyyətləri və avtomatik sənədləşməsi də ayrıca edilir.
* **Avtomatik doğrulama** hətta path əməliyyat parametrləri daxilində göstərilən tələblər üçün də edilə bilər.
* Mürəkkəb autentifikasiya sistemlərinə dəstək, **verilənlər bazası əlaqələri** və s.
* **Güzəşt yoxdur** heç bir şeydən güzəştə getmədən, databaselər, frontendlər vs. Bütün hamısının asanlıqla inteqrasiya edilə bilər.

### Limitsiz "plug-inlər"

Başqa sözlə, plug-inlərə ehtiyaccımız yoxdur, import edip birbaşa istifadə etməyə başlaya bilərik.

Bütün inteqrasiyalar istifadəsi asan olmaq üzərə (çətinlikləri ilə birlikdə) hazırlandı, siz bir "plug-in" yaradıb 2 sətir kod ilə, *path əməliyyatlarında* istifadə etdiyiniz eyni sintaksis və struktur ilə kodunuza inteqrasiya edebilərsiz.

### Sınaq edildi

* 100% <abbr title="Kodun nə qədərinin test edildiyi">sınaq əhatəsi </abbr>.
* 100% <abbr title="Python type annotationlar, editor və xarici alətlər sizə daha yaxşı dəstək verə bilər">typeları tanıdılmış </abbr> koda bazası.
* İstehsal mühitində olan proqramlarda istifadə olunur.

## Starlette xüsusiyyətləri

**FastAPI**, <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette </strong></a> ilə tam uyğun gəlir(və ona əsaslanır). Yəni FastAPI üzərinə əlavə edəcəyiniz istenilən Starlette kodu da işliyəcəkdir.

`FastAPI` əlsində  `Starlette`-nin bir sub-class-ıdır. Yəni, siz Starlette-i bilirsinizsə və ya istifadə edirsinizsə, funksionallığın əksəriyyəti eyni şəkildə işləyir.

**FastAPI** ilə siz həmçinin **Starlette**-in bütün xüsusiyyətlərinə sahib olacaqsınız. (FastAPI əslində Starlette-in steroid basmış halıdır):

* Həqiqətən də cidd təsir edici performansa sahibdir. Python-un isə en sürətli frameworklərindən bir dənəsi, <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS** ve **Go** ilə bərabər performansa sahibdir.</a>.
* **WebSocket** dəstəyi.
* **GraphQL** dəstəyi.
* İsditafədə halında olan arxa plan tapşırıqları.
* Başlatma ve söndrümə hadisələri(startup and shutdown).
* Sınaq serveri HTTPX üzərində quruldu.
* **CORS**, GZip, Statik fayllar, Streaming responseları.
* **Session and Cookie** dəstəyi.
* 100% test əhatəsi.
* 100% type annotated kod bazası.

## Pydantic xüsusiyyətləri

**FastAPI** <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic </strong></a> ilə tam uyğundur ve üzərinə qurulub. Yani FastAPI üzərinə nəsə əlavə etsəniz hansısa bir Pydantic kodu da işliyəcəkdir

Bunlara həmçinin Pydantic əsasında qurulmuş əlavə kitabxanlar, databaselər üçün <abbr title="Object-Relational Mapper">ORM </abbr>  , <abbr title="Object-Document Mapper">ODM </abbr>  daxildir.

Bu həm də o deməkdir ki, bir çox hallarda siz obyekti requestdən database-ə hər şey avtomatik olaraq yoxlanılmış şəkildə köçürə bilərsiniz.

Eynilə, siz obyekti verilənlər bazasından **birbaşa request-ə** tam doğrulanmış formada göndərə bilərsiniz.

**FastAPI** ilə siz **Pydantic**-in bütün xüsusiyyətlərinə sahib olacaqsınız (çünki FastAPI data nəzarətini Pydantic-in üzərində qurduğu üçün):

* **Baş ağrısı yoxdur**:
  * Fərqli bir sintaksis öyrənməyə ehtiyac yoxdur,
  * Python typelarını necə istifadə edəcəyinizi bilirsinizsə, Pydantic-dən necə istifadə edəcəyinizi də bilirsiniz.
* İstifadə etdiyiniz development əlatləri ilə yaxşı işləyir **<abbr title="Integrated Development Environment, kod editörüne benzer">IDE </abbr>/<abbr title="Code errorlarınızı inceleyen program">linter </abbr>/brain**:
  * Pydantic'in məlumat strukturları(data structures) əslində sadəcə sizin müəyyən etdiyiniz classlardır; Buna görə də, təsdiqlənmiş məlumatlarınızla avtomatik tamamlama, linting və mypy istifadə edərək heç bir problem olmadan işləyə bilərsiniz.
* **Sürətli**:
  * <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">Benchmarklarda </a>, Pydantic bütün digər sınaqdan keçmiş kitabxanalardan daha sürətlidir.
* **Ən kompleks** **strukturları** belə doğrula(validate):
  * İerarxik Pydantic-in modellərinin istifadəsi ilə birlikdə, Python `typing`’s `List` və  `Dict`, vs kimi şeyləri doğrula.
  * Doğrulayıcılar hətta ən mürəkkəb məlumat sxemlərini təmiz və asanlıqla müəyyən etməyə imkan verir, hamısı JSON sxemləri kimi sənədləşdirilir.
  * Pydantic JSON obyektinin nə qədər iç-içə olmasından asılı olmayaraq onu doğrulayır və göstərir.
* **Genişlədilə bilinir**:
  * Pydantic sizə fərdiləşdirilmiş data typler-ı müəyyən etməyə imkan verir və doğrulamaları genişləndirməyə və validator dekoratoru ilə öz doğrulayıcılarınızı yazmağa imkan verir.
* 100% test əhatəsi.
