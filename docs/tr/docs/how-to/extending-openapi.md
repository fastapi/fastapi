# OpenAPI'yi Genişletme { #extending-openapi }

Oluşturulan OpenAPI şemasını değiştirmeniz gereken bazı durumlar olabilir.

Bu bölümde bunun nasıl yapılacağını göreceksiniz.

## Normal Süreç { #the-normal-process }

Normal (varsayılan) süreç şöyledir.

Bir `FastAPI` uygulamasının (instance) OpenAPI şemasını döndürmesi beklenen bir `.openapi()` metodu vardır.

Uygulama nesnesi oluşturulurken, `/openapi.json` (ya da `openapi_url` için ne ayarladıysanız o) için bir *path operation* kaydedilir.

Bu path operation, uygulamanın `.openapi()` metodunun sonucunu içeren bir JSON response döndürür.

Varsayılan olarak `.openapi()` metodunun yaptığı şey, `.openapi_schema` özelliğinde içerik olup olmadığını kontrol etmek ve varsa onu döndürmektir.

Eğer yoksa, `fastapi.openapi.utils.get_openapi` konumundaki yardımcı (utility) fonksiyonu kullanarak şemayı üretir.

Ve `get_openapi()` fonksiyonu şu parametreleri alır:

* `title`: Dokümanlarda gösterilen OpenAPI başlığı.
* `version`: API'nizin sürümü, örn. `2.5.0`.
* `openapi_version`: Kullanılan OpenAPI specification sürümü. Varsayılan olarak en günceli: `3.1.0`.
* `summary`: API'nin kısa özeti.
* `description`: API'nizin açıklaması; markdown içerebilir ve dokümanlarda gösterilir.
* `routes`: route'ların listesi; bunların her biri kayıtlı *path operations*'lardır. `app.routes` içinden alınırlar.

/// info | Bilgi

`summary` parametresi OpenAPI 3.1.0 ve üzeri sürümlerde vardır; FastAPI 0.99.0 ve üzeri tarafından desteklenmektedir.

///

## Varsayılanları Ezme { #overriding-the-defaults }

Yukarıdaki bilgileri kullanarak aynı yardımcı fonksiyonla OpenAPI şemasını üretebilir ve ihtiyacınız olan her parçayı override edebilirsiniz.

Örneğin, <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">özel bir logo eklemek için ReDoc'un OpenAPI extension'ını</a> ekleyelim.

### Normal **FastAPI** { #normal-fastapi }

Önce, tüm **FastAPI** uygulamanızı her zamanki gibi yazın:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### OpenAPI Şemasını Üretme { #generate-the-openapi-schema }

Ardından, bir `custom_openapi()` fonksiyonunun içinde aynı yardımcı fonksiyonu kullanarak OpenAPI şemasını üretin:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### OpenAPI Şemasını Değiştirme { #modify-the-openapi-schema }

Artık OpenAPI şemasındaki `info` "object"'ine özel bir `x-logo` ekleyerek ReDoc extension'ını ekleyebilirsiniz:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### OpenAPI Şemasını Cache'leme { #cache-the-openapi-schema }

Ürettiğiniz şemayı saklamak için `.openapi_schema` özelliğini bir "cache" gibi kullanabilirsiniz.

Böylece bir kullanıcı API docs'larınızı her açtığında uygulamanız şemayı tekrar tekrar üretmek zorunda kalmaz.

Şema yalnızca bir kez üretilecektir; sonraki request'ler için de aynı cache'lenmiş şema kullanılacaktır.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### Metodu Override Etme { #override-the-method }

Şimdi `.openapi()` metodunu yeni fonksiyonunuzla değiştirebilirsiniz.

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### Kontrol Edin { #check-it }

<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> adresine gittiğinizde, özel logonuzu kullandığınızı göreceksiniz (bu örnekte **FastAPI**'nin logosu):

<img src="/img/tutorial/extending-openapi/image01.png">
