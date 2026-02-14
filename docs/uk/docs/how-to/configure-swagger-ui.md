# Налаштуйте Swagger UI { #configure-swagger-ui }

Ви можете налаштувати додаткові <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">параметри Swagger UI</a>.

Щоб їх налаштувати, передайте аргумент `swagger_ui_parameters` під час створення об’єкта додатка `FastAPI()` або до функції `get_swagger_ui_html()`.

`swagger_ui_parameters` отримує словник із налаштуваннями, що передаються безпосередньо до Swagger UI.

FastAPI перетворює ці налаштування на **JSON**, щоб зробити їх сумісними з JavaScript, оскільки саме це потрібно Swagger UI.

## Вимкніть підсвітку синтаксису { #disable-syntax-highlighting }

Наприклад, ви можете вимкнути підсвітку синтаксису в Swagger UI.

Без змін у налаштуваннях підсвітка синтаксису увімкнена за замовчуванням:

<img src="/img/tutorial/extending-openapi/image02.png">

Але ви можете вимкнути її, встановивши `syntaxHighlight` у `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...після цього Swagger UI більше не показуватиме підсвітку синтаксису:

<img src="/img/tutorial/extending-openapi/image03.png">

## Змініть тему { #change-the-theme }

Так само ви можете задати тему підсвітки синтаксису ключем `"syntaxHighlight.theme"` (зверніть увагу, що посередині є крапка):

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

Це налаштування змінить колірну тему підсвітки синтаксису:

<img src="/img/tutorial/extending-openapi/image04.png">

## Змініть параметри Swagger UI за замовчуванням { #change-default-swagger-ui-parameters }

FastAPI містить деякі параметри конфігурації за замовчуванням, що підходять для більшості випадків.

Вони включають такі типові налаштування:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

Ви можете переписати будь-яке з них, задавши інше значення в аргументі `swagger_ui_parameters`.

Наприклад, щоб вимкнути `deepLinking`, ви можете передати такі налаштування до `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## Інші параметри Swagger UI { #other-swagger-ui-parameters }

Щоб побачити всі можливі налаштування, які ви можете використовувати, прочитайте офіційну <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">документацію щодо параметрів Swagger UI</a>.

## Налаштування лише для JavaScript { #javascript-only-settings }

Swagger UI також дозволяє інші налаштування як об’єкти, що є тільки для **JavaScript** (наприклад, функції JavaScript).

FastAPI також включає такі налаштування `presets`, що є лише для JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Це об’єкти **JavaScript**, а не строки, тому ви не можете передати їх безпосередньо з коду Python.

Якщо вам потрібно використати такі налаштування лише для JavaScript, скористайтеся одним із методів вище. Повністю перепишіть операцію шляху Swagger UI та вручну напишіть потрібний JavaScript.
