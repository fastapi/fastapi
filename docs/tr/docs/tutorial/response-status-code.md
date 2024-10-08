# Yanıt Durum Kodu

Yanıt modeli belirlediğiniz gibi HTTP durum kodunu belirleyebilirsiniz. Bu, *yol operasyonlarından* herhangi birinde `status_code` parametresi ile yapılır:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* vb.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

!!! note "Not"
    Burada `status_code`'un "dekoratör" metodunun (`get`, `post`, vb) bir parametresi olduğuna dikkat edin. `status_code` *yol operasyonu fonksiyonunuzun* aldığı parametrelerden farklıdır.

`status_code` parametresi, HTTP durum kodu ile bir sayı alır.

!!! info "Bilgi"
    `statuc_code` ayrıca Python'ın <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>'ü gibi bir `IntEnum` de alabilir.

Bu şekilde:

* Yanıtta bu durum kodunu döndürür.
* Durum kodu dokümantasyonda belirtilir ve kullanıcı arayüzünde gösterilir.

<img src="/img/tutorial/response-status-code/image01.png">

!!! note "Not"
    Bazı yanıt durum kodları (bir sonraki bölüme bakın) yanıtın bir gövdesi olmadığını belirtir.

    FastAPI bunu bilir ve OpenAPI dokümantasyonu oluştururken yanıt gövdesi olmadığını belirtir.

## HTTP Durum Kodları Hakkında

!!! note "Not"
    Eğer HTTP durum kodlarını zaten biliyorsanız, bir sonraki bölüme atlayın.

HTTP ile, yanıtın bir parçası olarak 3 haneli bir sayısal durum kodu gönderilir.

Bu durum kodlarına tanınabilirlik sağlamak için bir isim atanmıştır, ancak önemli olan sayılardır.

Özetlemek gerekirse:

* `100` ve üstü "Bilgi" içindir. Bunları nadiren kullanırsınız. Bu durum kodlarına sahip yanıtların bir gövdesi olamaz.
* **`200`** ve üstü "Başarılı" yanıtlar içindir. Bunları en çok kullanacağınız türdür.
    * `200` her şeyin "yolunda" olduğu belirten varsayılan durum kodudur.
    * `201` ise "Oluşturuldu" anlamına gelen bir diğer durum kodudur. Genellikle veritabanında yeni bir kayıt oluşturulduktan sonra kullanılır.
    * `204` ise "İçerik Yok" anlamına gelir. Bu yanıt, istemciye döndürülecek içeriğin olmadığı durumlarda kullanılır ve bu nedenle yanıtın bir gövdesi olmamalıdır.
* **`300`** ve üstü "Yönlendirme" içindir. Bu durum kodlarına sahip yanıtların bir gövdesi olabilir veya olmayabilir ancak `304`, "Değiştirilmedi" için durum farklıdır ve bir gövdesi olmamalıdır.
* **`400`** ve üstü "İstemci hatası" yanıtları içindir. Bunlar muhtemelen en sık kullanacağınız ikinci türdür.
    * `404` ilgili kaynağın "bulunamadı"ğını belirten bir örnektir.
    * İstemciden gelen genel hatalar için sadece `400` kullanabilirsiniz.
* `500` ve üstü "Sunucu hatası" içindir. Bunları neredeyse hiçbir zaman doğrudan kullanmazsınız. Uygulama kodunda veya sunucuda bir şeyler yolunda gitmediğinde, otomatik olarak bu durum kodlarından birini döndürecektir.

!!! tip "İpucu"
    Her bir durum kodu ve hangi kodun ne anlama geldiği hakkında daha fazla bilgi edinmek için, <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr>'ün HTTP durum kodları hakkında dokümantasyonunu</a> inceleyebilirsiniz.

## İsimleri Hatırlamak İçin Kısayol

Önceki örneğe bir daha bakalım:

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

`201` "oluşturuldu" anlamına gelen bir durum kodudur.

Ancak bu kodların her birinin ne anlama geldiğini ezberlemeniz gerekmez.

`fastapi.status` ile gelen kolaylık değişkenlerini kullanabilirsiniz.

```Python hl_lines="1  6"
{!../../../docs_src/response_status_code/tutorial002.py!}
```

Bunlar sadece bir kolaylık, aynı numarayı tutarlar, ancak bu şekilde editörün otomatik tamamlama özelliğini kullanarak onları bulabilirsiniz:

<img src="/img/tutorial/response-status-code/image02.png">

!!! note "Teknik Detaylar"
    Projenize dahil etmek için `from starlette import status` kullanabilirsiniz.

    **FastAPI**, geliştiricilere kolaylık sağlamak amacıyla `starlette.status`'ü `fastapi.status` olarak sağlar. Ancak `status` aslında doğrudan Starlette'den gelir.

## Varsayılanı Değiştirme

[Gelişmiş Kullanıcı Rehberi](../advanced/response-change-status-code.md){.internal-link target=_blank} sayfasında, burada belirttiğiniz varsayılan durum kodundan farklı bir durum kodu döndürmenin nasıl yapılacağını göreceksiniz.
