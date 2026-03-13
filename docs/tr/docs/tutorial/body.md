# Request Body { #request-body }

Bir client'ten (örneğin bir tarayıcıdan) API'nize veri göndermeniz gerektiğinde, bunu **request body** olarak gönderirsiniz.

Bir **request** body, client'in API'nize gönderdiği veridir. Bir **response** body ise API'nizin client'e gönderdiği veridir.

API'niz neredeyse her zaman bir **response** body göndermek zorundadır. Ancak client'lerin her zaman **request body** göndermesi gerekmez; bazen sadece bir path isterler, belki birkaç query parametresiyle birlikte, ama body göndermezler.

Bir **request** body tanımlamak için, tüm gücü ve avantajlarıyla <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> modellerini kullanırsınız.

/// info | Bilgi

Veri göndermek için şunlardan birini kullanmalısınız: `POST` (en yaygını), `PUT`, `DELETE` veya `PATCH`.

`GET` request'i ile body göndermek, spesifikasyonlarda tanımsız bir davranıştır; yine de FastAPI bunu yalnızca çok karmaşık/uç kullanım senaryoları için destekler.

Önerilmediği için Swagger UI ile etkileşimli dokümanlar, `GET` kullanırken body için dokümantasyonu göstermez ve aradaki proxy'ler bunu desteklemeyebilir.

///

## Pydantic'in `BaseModel`'ini import edin { #import-pydantics-basemodel }

Önce, `pydantic` içinden `BaseModel`'i import etmeniz gerekir:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Veri modelinizi oluşturun { #create-your-data-model }

Sonra veri modelinizi, `BaseModel`'den kalıtım alan bir class olarak tanımlarsınız.

Tüm attribute'lar için standart Python type'larını kullanın:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}


Query parametrelerini tanımlarken olduğu gibi, bir model attribute'ü default bir değere sahipse zorunlu değildir. Aksi halde zorunludur. Sadece opsiyonel yapmak için `None` kullanın.

Örneğin, yukarıdaki model şu şekilde bir JSON "`object`" (veya Python `dict`) tanımlar:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...`description` ve `tax` opsiyonel olduğu için (default değerleri `None`), şu JSON "`object`" da geçerli olur:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Parametre olarak tanımlayın { #declare-it-as-a-parameter }

Bunu *path operation*'ınıza eklemek için, path ve query parametrelerini tanımladığınız şekilde tanımlayın:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...ve type'ını, oluşturduğunuz model olan `Item` olarak belirtin.

## Sonuçlar { #results }

Sadece bu Python type tanımıyla, **FastAPI** şunları yapar:

* Request'in body'sini JSON olarak okur.
* İlgili type'lara dönüştürür (gerekirse).
* Veriyi doğrular (validate eder).
    * Veri geçersizse, tam olarak nerede ve hangi verinin hatalı olduğunu söyleyen, anlaşılır bir hata döndürür.
* Aldığı veriyi `item` parametresi içinde size verir.
    * Fonksiyonda bunun type'ını `Item` olarak tanımladığınız için, tüm attribute'lar ve type'ları için editor desteğini (tamamlama vb.) de alırsınız.
* Modeliniz için <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> tanımları üretir; projeniz için anlamlıysa bunları başka yerlerde de kullanabilirsiniz.
* Bu şemalar üretilen OpenAPI şemasının bir parçası olur ve otomatik dokümantasyon <abbr title="User Interfaces - Kullanıcı Arayüzleri">UIs</abbr> tarafından kullanılır.

## Otomatik dokümanlar { #automatic-docs }

Modellerinizin JSON Schema'ları, OpenAPI tarafından üretilen şemanın bir parçası olur ve etkileşimli API dokümanlarında gösterilir:

<img src="/img/tutorial/body/image01.png">

Ayrıca, ihtiyaç duyan her *path operation* içindeki API dokümanlarında da kullanılır:

<img src="/img/tutorial/body/image02.png">

## Editor desteği { #editor-support }

Editor'ünüzde, fonksiyonunuzun içinde her yerde type hint'leri ve tamamlama (completion) alırsınız (Pydantic modeli yerine `dict` alsaydınız bu olmazdı):

<img src="/img/tutorial/body/image03.png">

Yanlış type işlemleri için hata kontrolleri de alırsınız:

<img src="/img/tutorial/body/image04.png">

Bu bir tesadüf değil; tüm framework bu tasarımın etrafında inşa edildi.

Ayrıca, bunun tüm editor'lerle çalışacağından emin olmak için herhangi bir implementasyon yapılmadan önce tasarım aşamasında kapsamlı şekilde test edildi.

Hatta bunu desteklemek için Pydantic'in kendisinde bile bazı değişiklikler yapıldı.

Önceki ekran görüntüleri <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a> ile alınmıştır.

Ancak <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> ve diğer Python editor'lerinin çoğunda da aynı editor desteğini alırsınız:

<img src="/img/tutorial/body/image05.png">

/// tip | İpucu

Editor olarak <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> kullanıyorsanız, <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> kullanabilirsiniz.

Pydantic modelleri için editor desteğini şu açılardan iyileştirir:

* auto-completion
* type checks
* refactoring
* searching
* inspections

///

## Modeli kullanın { #use-the-model }

Fonksiyonun içinde model nesnesinin tüm attribute'larına doğrudan erişebilirsiniz:

{* ../../docs_src/body/tutorial002_py310.py *}

## Request body + path parametreleri { #request-body-path-parameters }

Path parametrelerini ve request body'yi aynı anda tanımlayabilirsiniz.

**FastAPI**, path parametreleriyle eşleşen fonksiyon parametrelerinin **path'ten alınması** gerektiğini ve Pydantic model olarak tanımlanan fonksiyon parametrelerinin **request body'den alınması** gerektiğini anlayacaktır.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}


## Request body + path + query parametreleri { #request-body-path-query-parameters }

**body**, **path** ve **query** parametrelerini aynı anda da tanımlayabilirsiniz.

**FastAPI** bunların her birini tanır ve veriyi doğru yerden alır.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Fonksiyon parametreleri şu şekilde tanınır:

* Parametre, **path** içinde de tanımlıysa path parametresi olarak kullanılır.
* Parametre **tekil bir type**'taysa (`int`, `float`, `str`, `bool` vb.), **query** parametresi olarak yorumlanır.
* Parametre bir **Pydantic model** type'ı olarak tanımlandıysa, request **body** olarak yorumlanır.

/// note | Not

FastAPI, `q` değerinin zorunlu olmadığını `= None` default değerinden anlayacaktır.

`str | None`, FastAPI tarafından bu değerin zorunlu olmadığını belirlemek için kullanılmaz; FastAPI bunun zorunlu olmadığını `= None` default değeri olduğu için bilir.

Ancak type annotation'larını eklemek, editor'ünüzün size daha iyi destek vermesini ve hataları yakalamasını sağlar.

///

## Pydantic olmadan { #without-pydantic }

Pydantic modellerini kullanmak istemiyorsanız, **Body** parametrelerini de kullanabilirsiniz. [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank} dokümanına bakın.
