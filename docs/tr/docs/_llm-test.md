# LLM test dosyası { #llm-test-file }

Bu doküman, dokümantasyonu çeviren <abbr title="Large Language Model - Büyük Dil Modeli">LLM</abbr>'nin `scripts/translate.py` içindeki `general_prompt`'u ve `docs/{language code}/llm-prompt.md` içindeki dile özel prompt'u anlayıp anlamadığını test eder. Dile özel prompt, `general_prompt`'a eklenir.

Buraya eklenen testler, dile özel prompt'ları tasarlayan herkes tarafından görülecektir.

Şu şekilde kullanın:

* Dile özel bir prompt bulundurun: `docs/{language code}/llm-prompt.md`.
* Bu dokümanın hedeflediğiniz dile sıfırdan yeni bir çevirisini yapın (örneğin `translate.py` içindeki `translate-page` komutu). Bu, çeviriyi `docs/{language code}/docs/_llm-test.md` altında oluşturur.
* Çeviride her şeyin yolunda olup olmadığını kontrol edin.
* Gerekirse dile özel prompt'u, genel prompt'u veya İngilizce dokümanı iyileştirin.
* Ardından çeviride kalan sorunları elle düzeltin; böylece iyi bir çeviri elde edin.
* İyi çeviri yerindeyken yeniden çeviri yapın. İdeal sonuç, LLM'nin artık çeviride hiçbir değişiklik yapmamasıdır. Bu da genel prompt'un ve dile özel prompt'un olabilecek en iyi hâle geldiği anlamına gelir (bazen rastgele gibi görünen birkaç değişiklik yapabilir; çünkü <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLM'ler deterministik algoritmalar değildir</a>).

Testler:

## Code snippets { #code-snippets }

//// tab | Test

Bu bir code snippet: `foo`. Bu da başka bir code snippet: `bar`. Bir tane daha: `baz quux`.

////

//// tab | Bilgi

Code snippet'lerin içeriği olduğu gibi bırakılmalıdır.

`scripts/translate.py` içindeki genel prompt'ta `### Content of code snippets` bölümüne bakın.

////

## Alıntılar { #quotes }

//// tab | Test

Dün bir arkadaşım şunu yazdı: "If you spell incorrectly correctly, you have spelled it incorrectly". Ben de şunu yanıtladım: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".

/// note | Not

LLM muhtemelen bunu yanlış çevirecektir. Yeniden çeviri yapıldığında düzeltilmiş çeviriyi koruyup korumadığı önemlidir.

///

////

//// tab | Bilgi

Prompt tasarlayan kişi, düz tırnakları tipografik tırnaklara dönüştürüp dönüştürmemeyi seçebilir. Olduğu gibi bırakmak da uygundur.

Örneğin `docs/de/llm-prompt.md` içindeki `### Quotes` bölümüne bakın.

////

## Code snippet'lerde alıntılar { #quotes-in-code-snippets }

//// tab | Test

`pip install "foo[bar]"`

Code snippet'lerde string literal örnekleri: `"this"`, `'that'`.

Code snippet'lerde string literal için zor bir örnek: `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Bilgi

... Ancak code snippet'lerin içindeki tırnaklar olduğu gibi kalmalıdır.

////

## Code block'lar { #code-blocks }

//// tab | Test

Bir Bash code örneği...

```bash
# Evrene bir selam yazdır
echo "Hello universe"
```

...ve bir console code örneği...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...ve bir başka console code örneği...

```console
// "Code" adında bir dizin oluştur
$ mkdir code
// O dizine geç
$ cd code
```

...ve bir Python code örneği...

```Python
wont_work()  # This won't work 😱
works(foo="bar")  # This works 🎉
```

...ve hepsi bu.

////

//// tab | Bilgi

Code block'ların içindeki code değiştirilmemelidir; tek istisna yorumlardır (comments).

`scripts/translate.py` içindeki genel prompt'ta `### Content of code blocks` bölümüne bakın.

////

## Sekmeler ve renkli kutular { #tabs-and-colored-boxes }

//// tab | Test

/// info | Bilgi
Bazı metin
///

/// note | Not
Bazı metin
///

/// note | Teknik Detaylar
Bazı metin
///

/// check | Ek bilgi
Bazı metin
///

/// tip | İpucu
Bazı metin
///

/// warning | Uyarı
Bazı metin
///

/// danger | Tehlike
Bazı metin
///

////

//// tab | Bilgi

Sekmelerin ve `Info`/`Note`/`Warning`/vb. blokların başlığı, dikey çizgiden (`|`) sonra çeviri olarak eklenmelidir.

`scripts/translate.py` içindeki genel prompt'ta `### Special blocks` ve `### Tab blocks` bölümlerine bakın.

////

## Web ve internal link'ler { #web-and-internal-links }

//// tab | Test

Link metni çevrilmelidir, link adresi değişmeden kalmalıdır:

* [Yukarıdaki başlığa link](#code-snippets)
* [Internal link](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Harici link</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Bir stile bağlantı</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Bir betiğe bağlantı</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Bir görsele bağlantı</a>

Link metni çevrilmelidir, link adresi çeviriye işaret etmelidir:

* <a href="https://fastapi.tiangolo.com/tr/" class="external-link" target="_blank">FastAPI link</a>

////

//// tab | Bilgi

Link'ler çevrilmelidir, ancak adresleri değişmeden kalmalıdır. Bir istisna, FastAPI dokümantasyonunun sayfalarına verilen mutlak link'lerdir. Bu durumda link, çeviriye işaret etmelidir.

`scripts/translate.py` içindeki genel prompt'ta `### Links` bölümüne bakın.

////

## HTML "abbr" öğeleri { #html-abbr-elements }

//// tab | Test

Burada HTML "abbr" öğeleriyle sarılmış bazı şeyler var (bazıları uydurma):

### abbr tam bir ifade verir { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - İşleri Bitirme">GTD</abbr>
* <abbr title="less than - küçüktür"><code>lt</code></abbr>
* <abbr title="XML Web Token">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - Paralel Sunucu Gateway Interface">PSGI</abbr>

### abbr tam bir ifade ve bir açıklama verir { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Mozilla Geliştirici Ağı: Firefox ekibi tarafından yazılmış, geliştiricilere yönelik dokümantasyon">MDN</abbr>
* <abbr title="Input/Output - Girdi/Çıktı: disk okuma ya da yazma, ağ iletişimi.">I/O</abbr>.

////

//// tab | Bilgi

"abbr" öğelerinin "title" attribute'ları belirli talimatlara göre çevrilir.

Çeviriler, LLM'nin kaldırmaması gereken kendi "abbr" öğelerini ekleyebilir. Örneğin İngilizce kelimeleri açıklamak için.

`scripts/translate.py` içindeki genel prompt'ta `### HTML abbr elements` bölümüne bakın.

////

## HTML "dfn" öğeleri { #html-dfn-elements }

* <dfn title="Bir şekilde birbirine bağlanacak ve birlikte çalışacak şekilde yapılandırılmış makinelerden oluşan bir grup.">küme</dfn>
* <dfn title="Girdi ve çıktı katmanları arasında çok sayıda gizli katman içeren yapay sinir ağlarını kullanan; böylece kapsamlı bir iç yapı geliştiren bir makine öğrenmesi yöntemi">Derin Öğrenme</dfn>

## Başlıklar { #headings }

//// tab | Test

### Bir web uygulaması geliştirin - bir öğretici { #develop-a-webapp-a-tutorial }

Merhaba.

### Type hint'ler ve -annotation'lar { #type-hints-and-annotations }

Tekrar merhaba.

### Super- ve subclass'lar { #super-and-subclasses }

Tekrar merhaba.

////

//// tab | Bilgi

Başlıklarla ilgili tek katı kural, LLM'nin süslü parantezler içindeki hash kısmını değiştirmemesidir; böylece link'ler bozulmaz.

`scripts/translate.py` içindeki genel prompt'ta `### Headings` bölümüne bakın.

Dile özel bazı talimatlar için örneğin `docs/de/llm-prompt.md` içindeki `### Headings` bölümüne bakın.

////

## Dokümanlarda kullanılan terimler { #terms-used-in-the-docs }

//// tab | Test

* siz
* sizin

* örn.
* vb.

* `foo` bir `int` olarak
* `bar` bir `str` olarak
* `baz` bir `list` olarak

* Tutorial - Kullanıcı kılavuzu
* İleri Düzey Kullanıcı Kılavuzu
* SQLModel dokümanları
* API dokümanları
* otomatik dokümanlar

* Veri Bilimi
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO formatı
* JSON Schema standardı
* JSON schema
* schema tanımı
* Password Flow
* Mobil

* deprecated
* designed
* invalid
* on the fly
* standard
* default
* case-sensitive
* case-insensitive

* uygulamayı serve etmek
* sayfayı serve etmek

* app
* application

* request
* response
* error response

* path operation
* path operation decorator
* path operation function

* body
* request body
* response body
* JSON body
* form body
* file body
* function body

* parameter
* body parameter
* path parameter
* query parameter
* cookie parameter
* header parameter
* form parameter
* function parameter

* event
* startup event
* server'ın startup'ı
* shutdown event
* lifespan event

* handler
* event handler
* exception handler
* handle etmek

* model
* Pydantic model
* data model
* database model
* form model
* model object

* class
* base class
* parent class
* subclass
* child class
* sibling class
* class method

* header
* headers
* authorization header
* `Authorization` header
* forwarded header

* dependency injection system
* dependency
* dependable
* dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* env var
* environment variable
* `PATH`
* `PATH` variable

* authentication
* authentication provider
* authorization
* authorization form
* authorization provider
* kullanıcı authenticate olur
* sistem kullanıcıyı authenticate eder

* CLI
* command line interface

* server
* client

* cloud provider
* cloud service

* geliştirme
* geliştirme aşamaları

* dict
* dictionary
* enumeration
* enum
* enum member

* encoder
* decoder
* encode etmek
* decode etmek

* exception
* raise etmek

* expression
* statement

* frontend
* backend

* GitHub discussion
* GitHub issue

* performance
* performance optimization

* return type
* return value

* security
* security scheme

* task
* background task
* task function

* template
* template engine

* type annotation
* type hint

* server worker
* Uvicorn worker
* Gunicorn Worker
* worker process
* worker class
* workload

* deployment
* deploy etmek

* SDK
* software development kit

* `APIRouter`
* `requirements.txt`
* Bearer Token
* breaking change
* bug
* button
* callable
* code
* commit
* context manager
* coroutine
* database session
* disk
* domain
* engine
* fake X
* HTTP GET method
* item
* library
* lifespan
* lock
* middleware
* mobile application
* module
* mounting
* network
* origin
* override
* payload
* processor
* property
* proxy
* pull request
* query
* RAM
* remote machine
* status code
* string
* tag
* web framework
* wildcard
* return etmek
* validate etmek

////

//// tab | Bilgi

Bu, dokümanlarda görülen (çoğunlukla) teknik terimlerin eksiksiz ve normatif olmayan bir listesidir. Prompt tasarlayan kişi için, LLM'nin hangi terimlerde desteğe ihtiyaç duyduğunu anlamada yardımcı olabilir. Örneğin iyi bir çeviriyi sürekli daha zayıf bir çeviriye geri alıyorsa. Ya da sizin dilinizde bir terimi çekimlemekte (conjugating/declinating) zorlanıyorsa.

Örneğin `docs/de/llm-prompt.md` içindeki `### List of English terms and their preferred German translations` bölümüne bakın.

////
