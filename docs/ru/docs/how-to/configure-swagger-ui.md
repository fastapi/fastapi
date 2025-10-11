# Настройка Swagger UI { #configure-swagger-ui }

Вы можете настроить дополнительные <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">параметры Swagger UI</a>.

Чтобы настроить их, передайте аргумент `swagger_ui_parameters` при создании объекта приложения `FastAPI()` или в функцию `get_swagger_ui_html()`.

`swagger_ui_parameters` принимает словарь с настройками, которые передаются в Swagger UI напрямую.

FastAPI преобразует эти настройки в **JSON**, чтобы они были совместимы с JavaScript, поскольку именно это требуется Swagger UI.

## Отключить подсветку синтаксиса { #disable-syntax-highlighting }

Например, вы можете отключить подсветку синтаксиса в Swagger UI.

Без изменения настроек подсветка синтаксиса включена по умолчанию:

<img src="/img/tutorial/extending-openapi/image02.png">

Но вы можете отключить её, установив `syntaxHighlight` в `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

…и после этого Swagger UI больше не будет показывать подсветку синтаксиса:

<img src="/img/tutorial/extending-openapi/image03.png">

## Изменить тему { #change-the-theme }

Аналогично вы можете задать тему подсветки синтаксиса с ключом "syntaxHighlight.theme" (обратите внимание, что посередине стоит точка):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Эта настройка изменит цветовую тему подсветки синтаксиса:

<img src="/img/tutorial/extending-openapi/image04.png">

## Изменить параметры Swagger UI по умолчанию { #change-default-swagger-ui-parameters }

FastAPI включает некоторые параметры конфигурации по умолчанию, подходящие для большинства случаев.

Это включает следующие настройки по умолчанию:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Вы можете переопределить любую из них, указав другое значение в аргументе `swagger_ui_parameters`.

Например, чтобы отключить `deepLinking`, можно передать такие настройки в `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Другие параметры Swagger UI { #other-swagger-ui-parameters }

Чтобы увидеть все остальные возможные настройки, прочитайте официальную <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">документацию по параметрам Swagger UI</a>.

## Настройки только для JavaScript { #javascript-only-settings }

Swagger UI также допускает другие настройки, которые являются **чисто JavaScript-объектами** (например, JavaScript-функциями).

FastAPI также включает следующие настройки `presets` (только для JavaScript):

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Это объекты **JavaScript**, а не строки, поэтому напрямую передать их из Python-кода нельзя.

Если вам нужны такие настройки только для JavaScript, используйте один из методов выше. Переопределите *операцию пути* Swagger UI и вручную напишите любой необходимый JavaScript.
