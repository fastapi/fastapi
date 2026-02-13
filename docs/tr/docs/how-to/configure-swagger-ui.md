# Swagger UI'yi Yapılandırın { #configure-swagger-ui }

Bazı ek <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI parametrelerini</a> yapılandırabilirsiniz.

Bunları yapılandırmak için, `FastAPI()` uygulama nesnesini oluştururken ya da `get_swagger_ui_html()` fonksiyonuna `swagger_ui_parameters` argümanını verin.

`swagger_ui_parameters`, Swagger UI'ye doğrudan iletilecek yapılandırmaları içeren bir `dict` alır.

FastAPI, Swagger UI'nin ihtiyaç duyduğu şekilde JavaScript ile uyumlu olsun diye bu yapılandırmaları **JSON**'a dönüştürür.

## Syntax Highlighting'i Devre Dışı Bırakın { #disable-syntax-highlighting }

Örneğin, Swagger UI'de syntax highlighting'i devre dışı bırakabilirsiniz.

Ayarları değiştirmeden bırakırsanız, syntax highlighting varsayılan olarak etkindir:

<img src="/img/tutorial/extending-openapi/image02.png">

Ancak `syntaxHighlight` değerini `False` yaparak devre dışı bırakabilirsiniz:

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...ve ardından Swagger UI artık syntax highlighting'i göstermeyecektir:

<img src="/img/tutorial/extending-openapi/image03.png">

## Temayı Değiştirin { #change-the-theme }

Aynı şekilde, `"syntaxHighlight.theme"` anahtarıyla (ortasında bir nokta olduğuna dikkat edin) syntax highlighting temasını ayarlayabilirsiniz:

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

Bu yapılandırma, syntax highlighting renk temasını değiştirir:

<img src="/img/tutorial/extending-openapi/image04.png">

## Varsayılan Swagger UI Parametrelerini Değiştirin { #change-default-swagger-ui-parameters }

FastAPI, çoğu kullanım senaryosu için uygun bazı varsayılan yapılandırma parametreleriyle gelir.

Şu varsayılan yapılandırmaları içerir:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

`swagger_ui_parameters` argümanında farklı bir değer vererek bunların herhangi birini ezebilirsiniz (override).

Örneğin `deepLinking`'i devre dışı bırakmak için `swagger_ui_parameters`'a şu ayarları geçebilirsiniz:

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## Diğer Swagger UI Parametreleri { #other-swagger-ui-parameters }

Kullanabileceğiniz diğer tüm olası yapılandırmaları görmek için, resmi <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">Swagger UI parametreleri dokümantasyonunu</a> okuyun.

## Yalnızca JavaScript Ayarları { #javascript-only-settings }

Swagger UI ayrıca bazı yapılandırmaların **yalnızca JavaScript** nesneleri olmasına izin verir (örneğin JavaScript fonksiyonları).

FastAPI, bu yalnızca JavaScript olan `presets` ayarlarını da içerir:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Bunlar string değil, **JavaScript** nesneleridir; dolayısıyla bunları Python kodundan doğrudan geçemezsiniz.

Böyle yalnızca JavaScript yapılandırmalarına ihtiyacınız varsa, yukarıdaki yöntemlerden birini kullanabilirsiniz: Swagger UI'nin tüm *path operation*'larını override edin ve ihtiyaç duyduğunuz JavaScript'i elle yazın.
