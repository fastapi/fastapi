# Metadata ve Doküman URL'leri { #metadata-and-docs-urls }

**FastAPI** uygulamanızda çeşitli metadata yapılandırmalarını özelleştirebilirsiniz.

## API için Metadata { #metadata-for-api }

OpenAPI spesifikasyonunda ve otomatik API doküman arayüzlerinde kullanılan şu alanları ayarlayabilirsiniz:

| Parametre | Tip | Açıklama |
|------------|------|-------------|
| `title` | `str` | API'nin başlığı. |
| `summary` | `str` | API'nin kısa özeti. <small>OpenAPI 3.1.0, FastAPI 0.99.0 sürümünden itibaren mevcut.</small> |
| `description` | `str` | API'nin kısa açıklaması. Markdown kullanabilir. |
| `version` | `string` | API'nin sürümü. Bu, OpenAPI'nin değil, kendi uygulamanızın sürümüdür. Örneğin `2.5.0`. |
| `terms_of_service` | `str` | API'nin Kullanım Koşulları (Terms of Service) için bir URL. Verilirse, URL formatında olmalıdır. |
| `contact` | `dict` | Yayınlanan API için iletişim bilgileri. Birden fazla alan içerebilir. <details><summary><code>contact</code> alanları</summary><table><thead><tr><th>Parametre</th><th>Tip</th><th>Açıklama</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>İletişim kişisi/kuruluşunu tanımlayan ad.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>İletişim bilgilerine işaret eden URL. URL formatında OLMALIDIR.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>İletişim kişisi/kuruluşunun e-posta adresi. E-posta adresi formatında OLMALIDIR.</td></tr></tbody></table></details> |
| `license_info` | `dict` | Yayınlanan API için lisans bilgileri. Birden fazla alan içerebilir. <details><summary><code>license_info</code> alanları</summary><table><thead><tr><th>Parametre</th><th>Tip</th><th>Açıklama</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>ZORUNLU</strong> (<code>license_info</code> ayarlanmışsa). API için kullanılan lisans adı.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API için bir <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> lisans ifadesi. <code>identifier</code> alanı, <code>url</code> alanıyla karşılıklı olarak dışlayıcıdır (ikisi aynı anda kullanılamaz). <small>OpenAPI 3.1.0, FastAPI 0.99.0 sürümünden itibaren mevcut.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>API için kullanılan lisansa ait URL. URL formatında OLMALIDIR.</td></tr></tbody></table></details> |

Şu şekilde ayarlayabilirsiniz:

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | İpucu

`description` alanına Markdown yazabilirsiniz; çıktı tarafında render edilir.

///

Bu yapılandırmayla otomatik API dokümanları şöyle görünür:

<img src="/img/tutorial/metadata/image01.png">

## License identifier { #license-identifier }

OpenAPI 3.1.0 ve FastAPI 0.99.0 sürümünden itibaren, `license_info` içinde `url` yerine bir `identifier` da ayarlayabilirsiniz.

Örneğin:

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## Tag'ler için Metadata { #metadata-for-tags }

`openapi_tags` parametresiyle, path operation'larınızı gruplamak için kullandığınız farklı tag'ler adına ek metadata da ekleyebilirsiniz.

Bu parametre, her tag için bir sözlük (dictionary) içeren bir liste alır.

Her sözlük şunları içerebilir:

* `name` (**zorunlu**): *path operation*'larda ve `APIRouter`'larda `tags` parametresinde kullandığınız tag adıyla aynı olan bir `str`.
* `description`: tag için kısa bir açıklama içeren `str`. Markdown içerebilir ve doküman arayüzünde gösterilir.
* `externalDocs`: harici dokümanları tanımlayan bir `dict`:
    * `description`: harici dokümanlar için kısa açıklama içeren `str`.
    * `url` (**zorunlu**): harici dokümantasyonun URL'sini içeren `str`.

### Tag'ler için metadata oluşturun { #create-metadata-for-tags }

`users` ve `items` tag'lerini içeren bir örnekle deneyelim.

Tag'leriniz için metadata oluşturup `openapi_tags` parametresine geçin:

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

Açıklamaların içinde Markdown kullanabileceğinizi unutmayın; örneğin "login" kalın (**login**) ve "fancy" italik (_fancy_) olarak gösterilecektir.

/// tip | İpucu

Kullandığınız tüm tag'ler için metadata eklemek zorunda değilsiniz.

///

### Tag'lerinizi kullanın { #use-your-tags }

*path operation*'larınızı (ve `APIRouter`'ları) farklı tag'lere atamak için `tags` parametresini kullanın:

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// info | Bilgi

Tag'ler hakkında daha fazlası için: [Path Operation Configuration](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Dokümanları kontrol edin { #check-the-docs }

Artık dokümanlara baktığınızda, eklediğiniz tüm metadata gösterilir:

<img src="/img/tutorial/metadata/image02.png">

### Tag sırası { #order-of-tags }

Her tag metadata sözlüğünün listedeki sırası, doküman arayüzünde gösterilecek sırayı da belirler.

Örneğin alfabetik sıralamada `users`, `items`'tan sonra gelirdi; ancak listedeki ilk sözlük olarak `users` metadata'sını eklediğimiz için, dokümanlarda önce o görünür.

## OpenAPI URL'si { #openapi-url }

Varsayılan olarak OpenAPI şeması `/openapi.json` adresinden sunulur.

Ancak bunu `openapi_url` parametresiyle yapılandırabilirsiniz.

Örneğin `/api/v1/openapi.json` adresinden sunulacak şekilde ayarlamak için:

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

OpenAPI şemasını tamamen kapatmak isterseniz `openapi_url=None` ayarlayabilirsiniz; bu, onu kullanan dokümantasyon arayüzlerini de devre dışı bırakır.

## Doküman URL'leri { #docs-urls }

Dahil gelen iki dokümantasyon arayüzünü yapılandırabilirsiniz:

* **Swagger UI**: `/docs` adresinden sunulur.
    * URL'sini `docs_url` parametresiyle ayarlayabilirsiniz.
    * `docs_url=None` ayarlayarak devre dışı bırakabilirsiniz.
* **ReDoc**: `/redoc` adresinden sunulur.
    * URL'sini `redoc_url` parametresiyle ayarlayabilirsiniz.
    * `redoc_url=None` ayarlayarak devre dışı bırakabilirsiniz.

Örneğin Swagger UI'yi `/documentation` adresinden sunup ReDoc'u kapatmak için:

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
