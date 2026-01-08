# Recursos Estáticos Personalizados para la Docs UI (self hosting) { #custom-docs-ui-static-assets-self-hosting }

La documentación de la API utiliza **Swagger UI** y **ReDoc**, y cada uno de estos necesita algunos archivos JavaScript y CSS.

Por defecto, esos archivos se sirven desde un <abbr title="Content Delivery Network – Red de entrega de contenidos: Un servicio, normalmente compuesto de varios servidores, que proporciona archivos estáticos, como JavaScript y CSS. Se usa comúnmente para servir esos archivos desde el servidor más cercano al cliente, mejorando el rendimiento.">CDN</abbr>.

Pero es posible personalizarlo, puedes establecer un CDN específico, o servir los archivos tú mismo.

## CDN Personalizado para JavaScript y CSS { #custom-cdn-for-javascript-and-css }

Digamos que quieres usar un <abbr title="Content Delivery Network – Red de entrega de contenidos">CDN</abbr> diferente, por ejemplo, quieres usar `https://unpkg.com/`.

Esto podría ser útil si, por ejemplo, vives en un país que restringe algunas URLs.

### Desactiva la documentación automática { #disable-the-automatic-docs }

El primer paso es desactivar la documentación automática, ya que por defecto, esos usan el CDN por defecto.

Para desactivarlos, establece sus URLs en `None` cuando crees tu aplicación de `FastAPI`:

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[8] *}

### Incluye la documentación personalizada { #include-the-custom-docs }

Ahora puedes crear las *path operations* para la documentación personalizada.

Puedes reutilizar las funciones internas de FastAPI para crear las páginas HTML para la documentación, y pasarles los argumentos necesarios:

* `openapi_url`: la URL donde la página HTML para la documentación puede obtener el OpenAPI esquema de tu API. Puedes usar aquí el atributo `app.openapi_url`.
* `title`: el título de tu API.
* `oauth2_redirect_url`: puedes usar `app.swagger_ui_oauth2_redirect_url` aquí para usar el valor por defecto.
* `swagger_js_url`: la URL donde el HTML para tu documentación de Swagger UI puede obtener el archivo **JavaScript**. Esta es la URL personalizada del CDN.
* `swagger_css_url`: la URL donde el HTML para tu documentación de Swagger UI puede obtener el archivo **CSS**. Esta es la URL personalizada del CDN.

Y de manera similar para ReDoc...

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[2:6,11:19,22:24,27:33] *}

/// tip | Consejo

La *path operation* para `swagger_ui_redirect` es una herramienta cuando utilizas OAuth2.

Si integras tu API con un proveedor OAuth2, podrás autenticarte y regresar a la documentación de la API con las credenciales adquiridas. E interactuar con ella usando la autenticación real de OAuth2.

Swagger UI lo manejará detrás de escena para ti, pero necesita este auxiliar de "redirección".

///

### Crea una *path operation* para probarlo { #create-a-path-operation-to-test-it }

Ahora, para poder probar que todo funciona, crea una *path operation*:

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[36:38] *}

### Pruébalo { #test-it }

Ahora, deberías poder ir a tu documentación en <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, y recargar la página, cargará esos recursos desde el nuevo CDN.

## self hosting de JavaScript y CSS para la documentación { #self-hosting-javascript-and-css-for-docs }

El self hosting de JavaScript y CSS podría ser útil si, por ejemplo, necesitas que tu aplicación siga funcionando incluso offline, sin acceso a Internet, o en una red local.

Aquí verás cómo servir esos archivos tú mismo, en la misma aplicación de FastAPI, y configurar la documentación para usarla.

### Estructura de archivos del proyecto { #project-file-structure }

Supongamos que la estructura de archivos de tu proyecto se ve así:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Ahora crea un directorio para almacenar esos archivos estáticos.

Tu nueva estructura de archivos podría verse así:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Descarga los archivos { #download-the-files }

Descarga los archivos estáticos necesarios para la documentación y ponlos en ese directorio `static/`.

Probablemente puedas hacer clic derecho en cada enlace y seleccionar una opción similar a `Guardar enlace como...`.

**Swagger UI** utiliza los archivos:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

Y **ReDoc** utiliza el archivo:

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

Después de eso, tu estructura de archivos podría verse así:

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

### Sirve los archivos estáticos { #serve-the-static-files }

* Importa `StaticFiles`.
* "Monta" una instance de `StaticFiles()` en un path específico.

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[7,11] *}

### Prueba los archivos estáticos { #test-the-static-files }

Inicia tu aplicación y ve a <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>.

Deberías ver un archivo JavaScript muy largo de **ReDoc**.

Podría comenzar con algo como:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

Eso confirma que puedes servir archivos estáticos desde tu aplicación, y que colocaste los archivos estáticos para la documentación en el lugar correcto.

Ahora podemos configurar la aplicación para usar esos archivos estáticos para la documentación.

### Desactiva la documentación automática para archivos estáticos { #disable-the-automatic-docs-for-static-files }

Igual que cuando usas un CDN personalizado, el primer paso es desactivar la documentación automática, ya que esos usan el CDN por defecto.

Para desactivarlos, establece sus URLs en `None` cuando crees tu aplicación de `FastAPI`:

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[9] *}

### Incluye la documentación personalizada para archivos estáticos { #include-the-custom-docs-for-static-files }

Y de la misma manera que con un CDN personalizado, ahora puedes crear las *path operations* para la documentación personalizada.

Nuevamente, puedes reutilizar las funciones internas de FastAPI para crear las páginas HTML para la documentación, y pasarles los argumentos necesarios:

* `openapi_url`: la URL donde la página HTML para la documentación puede obtener el OpenAPI esquema de tu API. Puedes usar aquí el atributo `app.openapi_url`.
* `title`: el título de tu API.
* `oauth2_redirect_url`: puedes usar `app.swagger_ui_oauth2_redirect_url` aquí para usar el valor por defecto.
* `swagger_js_url`: la URL donde el HTML para tu documentación de Swagger UI puede obtener el archivo **JavaScript**. **Este es el que tu propia aplicación está sirviendo ahora**.
* `swagger_css_url`: la URL donde el HTML para tu documentación de Swagger UI puede obtener el archivo **CSS**. **Este es el que tu propia aplicación está sirviendo ahora**.

Y de manera similar para ReDoc...

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[2:6,14:22,25:27,30:36] *}

/// tip | Consejo

La *path operation* para `swagger_ui_redirect` es una herramienta cuando utilizas OAuth2.

Si integras tu API con un proveedor OAuth2, podrás autenticarte y regresar a la documentación de la API con las credenciales adquiridas. Y interactuar con ella usando la autenticación real de OAuth2.

Swagger UI lo manejará detrás de escena para ti, pero necesita este auxiliar de "redirección".

///

### Crea una *path operation* para probar archivos estáticos { #create-a-path-operation-to-test-static-files }

Ahora, para poder probar que todo funciona, crea una *path operation*:

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[39:41] *}

### Prueba la UI de Archivos Estáticos { #test-static-files-ui }

Ahora, deberías poder desconectar tu WiFi, ir a tu documentación en <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, y recargar la página.

E incluso sin Internet, podrás ver la documentación de tu API e interactuar con ella.
