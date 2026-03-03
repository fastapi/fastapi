# Response Status Code { #response-status-code }

Bir response model tanımlayabildiğiniz gibi, herhangi bir *path operation* içinde `status_code` parametresiyle response için kullanılacak HTTP status code'u da belirtebilirsiniz:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* vb.

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | Not

`status_code`'un, "decorator" metodunun (`get`, `post`, vb.) bir parametresi olduğuna dikkat edin. Tüm parametreler ve body gibi, sizin *path operation function*'ınızın bir parametresi değildir.

///

`status_code` parametresi, HTTP status code'u içeren bir sayı alır.

/// info | Bilgi

Alternatif olarak `status_code`, Python'un <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>'ı gibi bir `IntEnum` da alabilir.

///

Bu sayede:

* Response'da o status code döner.
* OpenAPI şemasında (dolayısıyla kullanıcı arayüzlerinde de) bu şekilde dokümante edilir:

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Not

Bazı response code'lar (bir sonraki bölümde göreceğiz) response'un bir body'ye sahip olmadığını belirtir.

FastAPI bunu bilir ve response body olmadığını söyleyen OpenAPI dokümantasyonunu üretir.

///

## HTTP status code'lar hakkında { #about-http-status-codes }

/// note | Not

HTTP status code'ların ne olduğunu zaten biliyorsanız, bir sonraki bölüme geçin.

///

HTTP'de, response'un bir parçası olarak 3 basamaklı sayısal bir status code gönderirsiniz.

Bu status code'ların tanınmalarını sağlayan bir isimleri de vardır; ancak önemli olan kısım sayıdır.

Kısaca:

* `100 - 199` "Information" içindir. Doğrudan nadiren kullanırsınız. Bu status code'lara sahip response'lar body içeremez.
* **`200 - 299`** "Successful" response'lar içindir. En sık kullanacağınız aralık budur.
    * `200`, varsayılan status code'dur ve her şeyin "OK" olduğunu ifade eder.
    * Başka bir örnek `201` ("Created") olabilir. Genellikle veritabanında yeni bir kayıt oluşturduktan sonra kullanılır.
    * Özel bir durum ise `204` ("No Content")'tür. Client'a döndürülecek içerik olmadığında kullanılır; bu nedenle response body olmamalıdır.
* **`300 - 399`** "Redirection" içindir. Bu status code'lara sahip response'lar, `304` ("Not Modified") hariç, body içerebilir de içermeyebilir de; `304` kesinlikle body içermemelidir.
* **`400 - 499`** "Client error" response'ları içindir. Muhtemelen en sık kullanacağınız ikinci aralık budur.
    * Örneğin `404`, "Not Found" response'u içindir.
    * Client kaynaklı genel hatalar için doğrudan `400` kullanabilirsiniz.
* `500 - 599` server hataları içindir. Neredeyse hiç doğrudan kullanmazsınız. Uygulama kodunuzun bir bölümünde ya da server'da bir şeyler ters giderse, otomatik olarak bu status code'lardan biri döner.

/// tip | İpucu

Her bir status code hakkında daha fazla bilgi almak ve hangi kodun ne için kullanıldığını görmek için <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla Geliştirici Ağı">MDN</abbr> dokümantasyonu: HTTP status code'lar hakkında</a> göz atın.

///

## İsimleri hatırlamak için kısayol { #shortcut-to-remember-the-names }

Önceki örneğe tekrar bakalım:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201`, "Created" için kullanılan status code'dur.

Ancak bu kodların her birinin ne anlama geldiğini ezberlemek zorunda değilsiniz.

`fastapi.status` içindeki kolaylık değişkenlerini (convenience variables) kullanabilirsiniz.

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

Bunlar sadece kolaylık sağlar; aynı sayıyı taşırlar. Ancak bu şekilde editörün autocomplete özelliğiyle kolayca bulabilirsiniz:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Teknik Detaylar

`from starlette import status` da kullanabilirsiniz.

**FastAPI**, geliştirici olarak size kolaylık olsun diye `starlette.status`'u `fastapi.status` olarak da sunar. Ancak bu aslında doğrudan Starlette'den gelir.

///

## Varsayılanı değiştirmek { #changing-the-default }

Daha sonra, [İleri Düzey Kullanıcı Kılavuzu](../advanced/response-change-status-code.md){.internal-link target=_blank} içinde, burada tanımladığınız varsayılanın dışında farklı bir status code nasıl döndüreceğinizi göreceksiniz.
