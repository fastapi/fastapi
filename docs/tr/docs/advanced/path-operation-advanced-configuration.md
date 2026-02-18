# Path Operation İleri Düzey Yapılandırma { #path-operation-advanced-configuration }

## OpenAPI operationId { #openapi-operationid }

/// warning | Uyarı

OpenAPI konusunda "uzman" değilseniz, muhtemelen buna ihtiyacınız yok.

///

*path operation*’ınızda kullanılacak OpenAPI `operationId` değerini `operation_id` parametresiyle ayarlayabilirsiniz.

Bunun her operation için benzersiz olduğundan emin olmanız gerekir.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py310.py hl[6] *}

### operationId olarak *path operation function* adını kullanma { #using-the-path-operation-function-name-as-the-operationid }

API’lerinizin function adlarını `operationId` olarak kullanmak istiyorsanız, hepsini dolaşıp her *path operation*’ın `operation_id` değerini `APIRoute.name` ile override edebilirsiniz.

Bunu, tüm *path operation*’ları ekledikten sonra yapmalısınız.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py310.py hl[2, 12:21, 24] *}

/// tip | İpucu

`app.openapi()` fonksiyonunu manuel olarak çağırıyorsanız, bunu yapmadan önce `operationId`’leri güncellemelisiniz.

///

/// warning | Uyarı

Bunu yaparsanız, her bir *path operation function*’ın adının benzersiz olduğundan emin olmanız gerekir.

Farklı modüllerde (Python dosyalarında) olsalar bile.

///

## OpenAPI’den Hariç Tutma { #exclude-from-openapi }

Bir *path operation*’ı üretilen OpenAPI şemasından (dolayısıyla otomatik dokümantasyon sistemlerinden) hariç tutmak için `include_in_schema` parametresini kullanın ve `False` yapın:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py310.py hl[6] *}

## Docstring’den İleri Düzey Açıklama { #advanced-description-from-docstring }

OpenAPI için, bir *path operation function*’ın docstring’inden kullanılacak satırları sınırlandırabilirsiniz.

Bir `\f` (escape edilmiş "form feed" karakteri) eklerseniz, **FastAPI** OpenAPI için kullanılan çıktıyı bu noktada **keser**.

Dokümantasyonda görünmez, ancak diğer araçlar (Sphinx gibi) geri kalan kısmı kullanabilir.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Ek Responses { #additional-responses }

Muhtemelen bir *path operation* için `response_model` ve `status_code` tanımlamayı görmüşsünüzdür.

Bu, bir *path operation*’ın ana response’u ile ilgili metadata’yı tanımlar.

Ek response’ları; modelleri, status code’ları vb. ile birlikte ayrıca da tanımlayabilirsiniz.

Dokümantasyonda bununla ilgili ayrı bir bölüm var; [OpenAPI’de Ek Responses](additional-responses.md){.internal-link target=_blank} sayfasından okuyabilirsiniz.

## OpenAPI Extra { #openapi-extra }

Uygulamanızda bir *path operation* tanımladığınızda, **FastAPI** OpenAPI şemasına dahil edilmek üzere o *path operation* ile ilgili metadata’yı otomatik olarak üretir.

/// note | Teknik Detaylar

OpenAPI spesifikasyonunda buna <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Operation Nesnesi</a> denir.

///

Bu, *path operation* hakkında tüm bilgileri içerir ve otomatik dokümantasyonu üretmek için kullanılır.

`tags`, `parameters`, `requestBody`, `responses` vb. alanları içerir.

Bu *path operation*’a özel OpenAPI şeması normalde **FastAPI** tarafından otomatik üretilir; ancak siz bunu genişletebilirsiniz.

/// tip | İpucu

Bu, düşük seviyeli bir genişletme noktasıdır.

Yalnızca ek response’lar tanımlamanız gerekiyorsa, bunu yapmanın daha pratik yolu [OpenAPI’de Ek Responses](additional-responses.md){.internal-link target=_blank} kullanmaktır.

///

Bir *path operation* için OpenAPI şemasını `openapi_extra` parametresiyle genişletebilirsiniz.

### OpenAPI Extensions { #openapi-extensions }

Örneğin bu `openapi_extra`, [OpenAPI Uzantıları](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions) tanımlamak için faydalı olabilir:

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py310.py hl[6] *}

Otomatik API dokümanlarını açtığınızda, extension’ınız ilgili *path operation*’ın en altında görünür.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

Ayrıca ortaya çıkan OpenAPI’yi (API’nizde `/openapi.json`) görüntülerseniz, extension’ınızı ilgili *path operation*’ın bir parçası olarak orada da görürsünüz:

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Özel OpenAPI *path operation* şeması { #custom-openapi-path-operation-schema }

`openapi_extra` içindeki dictionary, *path operation* için otomatik üretilen OpenAPI şemasıyla derinlemesine (deep) birleştirilir.

Böylece otomatik üretilen şemaya ek veri ekleyebilirsiniz.

Örneğin, Pydantic ile FastAPI’nin otomatik özelliklerini kullanmadan request’i kendi kodunuzla okuyup doğrulamaya karar verebilirsiniz; ancak yine de OpenAPI şemasında request’i tanımlamak isteyebilirsiniz.

Bunu `openapi_extra` ile yapabilirsiniz:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py310.py hl[19:36, 39:40] *}

Bu örnekte herhangi bir Pydantic model tanımlamadık. Hatta request body JSON olarak <dfn title="bytes gibi düz bir formattan, ör. bytes, Python nesnelerine dönüştürme">ayrıştırılmıyor</dfn>; doğrudan `bytes` olarak okunuyor ve `magic_data_reader()` fonksiyonu bunu bir şekilde parse etmekten sorumlu oluyor.

Buna rağmen, request body için beklenen şemayı tanımlayabiliriz.

### Özel OpenAPI content type { #custom-openapi-content-type }

Aynı yöntemi kullanarak, Pydantic model ile JSON Schema’yı tanımlayıp bunu *path operation* için özel OpenAPI şeması bölümüne dahil edebilirsiniz.

Ve bunu, request içindeki veri tipi JSON olmasa bile yapabilirsiniz.

Örneğin bu uygulamada, FastAPI’nin Pydantic modellerinden JSON Schema çıkarmaya yönelik entegre işlevselliğini ve JSON için otomatik doğrulamayı kullanmıyoruz. Hatta request content type’ını JSON değil, YAML olarak tanımlıyoruz:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[15:20, 22] *}

Buna rağmen, varsayılan entegre işlevselliği kullanmasak da, YAML olarak almak istediğimiz veri için JSON Schema’yı manuel üretmek üzere bir Pydantic model kullanmaya devam ediyoruz.

Ardından request’i doğrudan kullanıp body’yi `bytes` olarak çıkarıyoruz. Bu da FastAPI’nin request payload’ını JSON olarak parse etmeye çalışmayacağı anlamına gelir.

Sonrasında kodumuzda bu YAML içeriğini doğrudan parse ediyor, ardından YAML içeriğini doğrulamak için yine aynı Pydantic modeli kullanıyoruz:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py310.py hl[24:31] *}

/// tip | İpucu

Burada aynı Pydantic modeli tekrar kullanıyoruz.

Aynı şekilde, başka bir yöntemle de doğrulama yapabilirdik.

///
