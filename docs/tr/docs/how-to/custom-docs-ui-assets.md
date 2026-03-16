# Özel Docs UI Statik Varlıkları (Self-Hosting) { #custom-docs-ui-static-assets-self-hosting }

API dokümanları **Swagger UI** ve **ReDoc** kullanır ve bunların her biri bazı JavaScript ve CSS dosyalarına ihtiyaç duyar.

Varsayılan olarak bu dosyalar bir <abbr title="Content Delivery Network - İçerik Dağıtım Ağı: Genellikle JavaScript ve CSS gibi statik dosyaları sunan, çoğunlukla birden fazla sunucudan oluşan bir servis. Bu dosyaları istemciye daha yakın bir sunucudan sunarak performansı artırmak için yaygın şekilde kullanılır.">CDN</abbr> üzerinden servis edilir.

Ancak bunu özelleştirmek mümkündür; belirli bir CDN ayarlayabilir veya dosyaları kendiniz servis edebilirsiniz.

## JavaScript ve CSS için Özel CDN { #custom-cdn-for-javascript-and-css }

Diyelim ki farklı bir <abbr title="Content Delivery Network - İçerik Dağıtım Ağı">CDN</abbr> kullanmak istiyorsunuz; örneğin `https://unpkg.com/` kullanmak istiyorsunuz.

Bu, örneğin bazı URL'leri kısıtlayan bir ülkede yaşıyorsanız faydalı olabilir.

### Otomatik dokümanları devre dışı bırakın { #disable-the-automatic-docs }

İlk adım, otomatik dokümanları devre dışı bırakmaktır; çünkü varsayılan olarak bunlar varsayılan CDN'i kullanır.

Bunları devre dışı bırakmak için `FastAPI` uygulamanızı oluştururken URL'lerini `None` olarak ayarlayın:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### Özel dokümanları ekleyin { #include-the-custom-docs }

Şimdi özel dokümanlar için *path operation*'ları oluşturabilirsiniz.

Dokümanlar için HTML sayfalarını üretmek üzere FastAPI'nin dahili fonksiyonlarını yeniden kullanabilir ve gerekli argümanları iletebilirsiniz:

* `openapi_url`: Dokümanların HTML sayfasının API'niz için OpenAPI şemasını alacağı URL. Burada `app.openapi_url` niteliğini kullanabilirsiniz.
* `title`: API'nizin başlığı.
* `oauth2_redirect_url`: varsayılanı kullanmak için burada `app.swagger_ui_oauth2_redirect_url` kullanabilirsiniz.
* `swagger_js_url`: Swagger UI dokümanlarınızın HTML'inin **JavaScript** dosyasını alacağı URL. Bu, özel CDN URL'idir.
* `swagger_css_url`: Swagger UI dokümanlarınızın HTML'inin **CSS** dosyasını alacağı URL. Bu, özel CDN URL'idir.

ReDoc için de benzer şekilde...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | İpucu

`swagger_ui_redirect` için olan *path operation*, OAuth2 kullandığınızda yardımcı olması için vardır.

API'nizi bir OAuth2 sağlayıcısıyla entegre ederseniz kimlik doğrulaması yapabilir, aldığınız kimlik bilgileriyle API dokümanlarına geri dönebilir ve gerçek OAuth2 kimlik doğrulamasını kullanarak onunla etkileşime geçebilirsiniz.

Swagger UI bunu arka planda sizin için yönetir, ancak bu "redirect" yardımcısına ihtiyaç duyar.

///

### Test etmek için bir *path operation* oluşturun { #create-a-path-operation-to-test-it }

Şimdi her şeyin çalıştığını test edebilmek için bir *path operation* oluşturun:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### Test edin { #test-it }

Artık <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresinden dokümanlarınıza gidebilmeli ve sayfayı yenilediğinizde bu varlıkların yeni CDN'den yüklendiğini görebilmelisiniz.

## Dokümanlar için JavaScript ve CSS'i Self-Hosting ile barındırma { #self-hosting-javascript-and-css-for-docs }

JavaScript ve CSS'i self-hosting ile barındırmak, örneğin uygulamanızın İnternet erişimi olmadan (offline), açık İnternet olmadan veya bir lokal ağ içinde bile çalışmaya devam etmesi gerekiyorsa faydalı olabilir.

Burada bu dosyaları aynı FastAPI uygulamasında nasıl kendiniz servis edeceğinizi ve dokümanların bunları kullanacak şekilde nasıl yapılandırılacağını göreceksiniz.

### Proje dosya yapısı { #project-file-structure }

Diyelim ki projenizin dosya yapısı şöyle:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Şimdi bu statik dosyaları saklamak için bir dizin oluşturun.

Yeni dosya yapınız şöyle olabilir:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Dosyaları indirin { #download-the-files }

Dokümanlar için gereken statik dosyaları indirin ve `static/` dizinine koyun.

Muhtemelen her bir linke sağ tıklayıp "Save link as..." benzeri bir seçenek seçebilirsiniz.

**Swagger UI** şu dosyaları kullanır:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

**ReDoc** ise şu dosyayı kullanır:

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

Bundan sonra dosya yapınız şöyle görünebilir:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Statik dosyaları servis edin { #serve-the-static-files }

* `StaticFiles` içe aktarın.
* Belirli bir path'te bir `StaticFiles()` instance'ını "mount" edin.

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### Statik dosyaları test edin { #test-the-static-files }

Uygulamanızı başlatın ve <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a> adresine gidin.

**ReDoc** için çok uzun bir JavaScript dosyası görmelisiniz.

Şuna benzer bir şekilde başlayabilir:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

Bu, uygulamanızdan statik dosyaları servis edebildiğinizi ve dokümanlar için statik dosyaları doğru yere koyduğunuzu doğrular.

Şimdi uygulamayı, dokümanlar için bu statik dosyaları kullanacak şekilde yapılandırabiliriz.

### Statik dosyalar için otomatik dokümanları devre dışı bırakın { #disable-the-automatic-docs-for-static-files }

Özel CDN kullanırken olduğu gibi, ilk adım otomatik dokümanları devre dışı bırakmaktır; çünkü bunlar varsayılan olarak CDN kullanır.

Bunları devre dışı bırakmak için `FastAPI` uygulamanızı oluştururken URL'lerini `None` olarak ayarlayın:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### Statik dosyalar için özel dokümanları ekleyin { #include-the-custom-docs-for-static-files }

Özel CDN'de olduğu gibi, artık özel dokümanlar için *path operation*'ları oluşturabilirsiniz.

Yine FastAPI'nin dahili fonksiyonlarını kullanarak dokümanlar için HTML sayfalarını oluşturabilir ve gerekli argümanları geçebilirsiniz:

* `openapi_url`: Dokümanların HTML sayfasının API'niz için OpenAPI şemasını alacağı URL. Burada `app.openapi_url` niteliğini kullanabilirsiniz.
* `title`: API'nizin başlığı.
* `oauth2_redirect_url`: varsayılanı kullanmak için burada `app.swagger_ui_oauth2_redirect_url` kullanabilirsiniz.
* `swagger_js_url`: Swagger UI dokümanlarınızın HTML'inin **JavaScript** dosyasını alacağı URL. **Artık bunu sizin kendi uygulamanız servis ediyor**.
* `swagger_css_url`: Swagger UI dokümanlarınızın HTML'inin **CSS** dosyasını alacağı URL. **Artık bunu sizin kendi uygulamanız servis ediyor**.

ReDoc için de benzer şekilde...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | İpucu

`swagger_ui_redirect` için olan *path operation*, OAuth2 kullandığınızda yardımcı olması için vardır.

API'nizi bir OAuth2 sağlayıcısıyla entegre ederseniz kimlik doğrulaması yapabilir, aldığınız kimlik bilgileriyle API dokümanlarına geri dönebilir ve gerçek OAuth2 kimlik doğrulamasını kullanarak onunla etkileşime geçebilirsiniz.

Swagger UI bunu arka planda sizin için yönetir, ancak bu "redirect" yardımcısına ihtiyaç duyar.

///

### Statik dosyaları test etmek için bir *path operation* oluşturun { #create-a-path-operation-to-test-static-files }

Şimdi her şeyin çalıştığını test edebilmek için bir *path operation* oluşturun:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### Statik Dosyalar UI'ını Test Edin { #test-static-files-ui }

Artık WiFi bağlantınızı kesip <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> adresindeki dokümanlarınıza gidebilmeli ve sayfayı yenileyebilmelisiniz.

Ve İnternet olmasa bile API dokümanlarınızı görebilir ve onunla etkileşime geçebilirsiniz.
