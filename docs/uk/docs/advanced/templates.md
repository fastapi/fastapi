# Шаблони { #templates }

Ви можете використовувати з **FastAPI** будь-який рушій шаблонів.

Поширений вибір — Jinja2, той самий, що використовується у Flask та інших інструментах.

Є утиліти для простого налаштування, які ви можете напряму використовувати у своєму застосунку **FastAPI** (надаються Starlette).

## Встановіть залежності { #install-dependencies }

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його та встановили `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Використання `Jinja2Templates` { #using-jinja2templates }

* Імпортуйте `Jinja2Templates`.
* Створіть об’єкт `templates`, який зможете повторно використовувати пізніше.
* Оголосіть параметр `Request` в *операції шляху*, яка повертатиме шаблон.
* Використайте створений `templates`, щоб відрендерити та повернути `TemplateResponse`, передайте назву шаблону, об’єкт запиту та словник «context» (контекст) з парами ключ-значення, які будуть доступні всередині шаблону Jinja2.

{* ../../docs_src/templates/tutorial001_py39.py hl[4,11,15:18] *}

/// note | Примітка

До FastAPI 0.108.0 та Starlette 0.29.0 параметр `name` був першим параметром.

Також до цього, у попередніх версіях, об’єкт `request` передавався як частина пар ключ-значення у контексті для Jinja2.

///

/// tip | Порада

Оголосивши `response_class=HTMLResponse`, інтерфейс документації зможе визначити, що відповідь буде HTML.

///

/// note | Технічні деталі

Ви також можете використати `from starlette.templating import Jinja2Templates`.

**FastAPI** надає той самий `starlette.templating` як `fastapi.templating` просто для зручності для вас, розробника. Але більшість доступних відповідей надходять безпосередньо зі Starlette. Те саме стосується `Request` і `StaticFiles`.

///

## Написання шаблонів { #writing-templates }

Далі ви можете написати шаблон у `templates/item.html`, наприклад:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Значення контексту шаблону { #template-context-values }

У HTML, що містить:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...буде показано `id`, взятий зі словника «context» `dict`, який ви передали:

```Python
{"id": id}
```

Наприклад, з ID `42` це відрендериться як:

```html
Item ID: 42
```

### Аргументи `url_for` у шаблоні { #template-url-for-arguments }

Ви також можете використовувати `url_for()` всередині шаблону; як аргументи він приймає ті самі аргументи, які використовувалися б вашою *функцією операції шляху*.

Отже, фрагмент із:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...згенерує посилання на ту саму URL-адресу, яку обробляла б *функція операції шляху* `read_item(id=id)`.

Наприклад, з ID `42` це відрендериться як:

```html
<a href="/items/42">
```

## Шаблони та статичні файли { #templates-and-static-files }

Ви також можете використовувати `url_for()` всередині шаблону і застосовувати його, наприклад, зі `StaticFiles`, які ви змонтували з `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

У цьому прикладі буде посилання на CSS-файл `static/styles.css` через:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

І оскільки ви використовуєте `StaticFiles`, цей CSS-файл автоматично буде віддаватися вашим застосунком **FastAPI** за URL `/static/styles.css`.

## Докладніше { #more-details }

Докладніше, зокрема про те, як тестувати шаблони, дивіться в <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">документації Starlette про шаблони</a>.
