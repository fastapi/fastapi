# Налаштування Swagger UI { #configure-swagger-ui }

Ви можете налаштувати деякі додаткові <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">параметри Swagger UI</a>.

Щоб налаштувати їх, передайте аргумент `swagger_ui_parameters` під час створення об’єкта застосунку `FastAPI()` або у функцію `get_swagger_ui_html()`.

`swagger_ui_parameters` приймає словник із конфігураціями, які передаються безпосередньо в Swagger UI.

FastAPI перетворює конфігурації на **JSON**, щоб зробити їх сумісними з JavaScript, адже саме це потрібно Swagger UI.

## Вимкнення підсвічування синтаксису { #disable-syntax-highlighting }

Наприклад, ви можете вимкнути підсвічування синтаксису в Swagger UI.

Без зміни налаштувань підсвічування синтаксису увімкнено за замовчуванням:

<img src="/img/tutorial/extending-openapi/image02.png">

Але ви можете вимкнути його, встановивши `syntaxHighlight` у `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001_py39.py hl[3] *}

...і тоді Swagger UI більше не показуватиме підсвічування синтаксису:

<img src="/img/tutorial/extending-openapi/image03.png">

## Зміна теми { #change-the-theme }

Так само ви можете встановити тему підсвічування синтаксису ключем `"syntaxHighlight.theme"` (зверніть увагу, що посередині є крапка):

{* ../../docs_src/configure_swagger_ui/tutorial002_py39.py hl[3] *}

Ця конфігурація змінить колірну тему підсвічування синтаксису:

<img src="/img/tutorial/extending-openapi/image04.png">

## Зміна параметрів Swagger UI за замовчуванням { #change-default-swagger-ui-parameters }

FastAPI містить деякі стандартні параметри конфігурації, придатні для більшості випадків використання.

Він включає такі конфігурації за замовчуванням:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

Ви можете перевизначити будь-яку з них, встановивши інше значення в аргументі `swagger_ui_parameters`.

Наприклад, щоб вимкнути `deepLinking`, ви можете передати такі налаштування в `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003_py39.py hl[3] *}

## Інші параметри Swagger UI { #other-swagger-ui-parameters }

Щоб переглянути всі інші можливі конфігурації, які ви можете використати, прочитайте офіційну <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">документацію з параметрів Swagger UI</a>.

## Налаштування лише для JavaScript { #javascript-only-settings }

Swagger UI також дозволяє інші конфігурації у вигляді об’єктів, що є **лише для JavaScript** (наприклад, функції JavaScript).

FastAPI також включає ці налаштування `presets`, що є лише для JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Це об’єкти **JavaScript**, а не рядки, тож ви не можете передати їх напряму з Python-коду.

Якщо вам потрібно використати конфігурації лише для JavaScript, подібні до цих, ви можете застосувати один із методів вище: перевизначити всі операції шляху Swagger UI та вручну написати потрібний вам JavaScript.
