# Настройка Swagger UI

Вы можете настроить некоторые дополнительные <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">параметры Swagger UI</a>.

Чтобы их настроить, передайте аргумент `swagger_ui_parameters` при создании объекта приложения `FastAPI()` или в функцию `get_swagger_ui_html()`.

`swagger_ui_parameters` принимает словарь с конфигурациями, передаваемыми непосредственно в Swagger UI.

FastAPI преобразует конфигурации в **JSON**, чтобы они были совместимы с JavaScript, так как это нужно для Swagger UI.

## Отключение подсветки синтаксиса

Например, вы можете отключить подсветку синтаксиса в Swagger UI.

Без изменения настроек, подсветка синтаксиса включена по умолчанию:

<img src="/img/tutorial/extending-openapi/image02.png">

Но вы можете отключить её, установив `syntaxHighlight` в `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...и тогда Swagger UI больше не будет отображать подсветку синтаксиса:

<img src="/img/tutorial/extending-openapi/image03.png">

## Изменение темы

Таким же образом вы можете установить тему подсветки синтаксиса с помощью ключа `"syntaxHighlight.theme"` (обратите внимание, что в нем есть точка):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Эта конфигурация изменит цветовую тему подсветки синтаксиса:

<img src="/img/tutorial/extending-openapi/image04.png">

## Изменение параметров Swagger UI по умолчанию

FastAPI включает некоторые параметры конфигурации по умолчанию, подходящие для большинства случаев использования.

Эти конфигурации по умолчанию включают:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Вы можете переопределить любой из них, установив другое значение в аргументе `swagger_ui_parameters`.

Например, чтобы отключить `deepLinking`, вы можете передать эти настройки в `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Другие параметры Swagger UI

Чтобы узнать о всех возможных конфигурациях, которые вы можете использовать, прочитайте официальную <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">документацию по параметрам Swagger UI</a>.

## Настройки только для JavaScript

Swagger UI также позволяет использовать другие конфигурации, представляющие собой **только для JavaScript** объекты (например, функции JavaScript).

FastAPI также включает эти настройки `presets`, предназначенные только для JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Это объекты **JavaScript**, а не строки, поэтому вы не можете передавать их напрямую из кода Python.

Если вам нужно использовать такие настройки, предназначенные только для JavaScript, вы можете использовать один из методов выше. Переопределите все *операции пути* Swagger UI и вручную напишите любой нужный JavaScript.
