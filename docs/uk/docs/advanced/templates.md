# Шаблони { #templates }

Ви можете використовувати будь-який рушій шаблонів з **FastAPI**.

Поширений вибір - Jinja2, той самий, що використовується у Flask та інших інструментах.

Є утиліти для простої конфігурації, які ви можете використовувати безпосередньо у вашому застосунку **FastAPI** (надає Starlette).

## Встановіть залежності { #install-dependencies }

Переконайтеся, що ви створили [віртуальне оточення](../virtual-environments.md){.internal-link target=_blank}, активували його та встановили `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Використання `Jinja2Templates` { #using-jinja2templates }

- Імпортуйте `Jinja2Templates`.
- Створіть об'єкт `templates`, який ви зможете перевикористовувати.
- Оголосіть параметр `Request` в *операції шляху*, яка повертатиме шаблон.
- Використайте створені `templates`, щоб зрендерити та повернути `TemplateResponse`; передайте назву шаблону, об'єкт `request` і словник «контекст» з парами ключ-значення, які будуть використані всередині шаблону Jinja2.

{* ../../docs_src/templates/tutorial001_py310.py hl[4,11,15:18] *}

/// note | Примітка

До FastAPI 0.108.0, Starlette 0.29.0, параметр `name` був першим.

Також раніше, у попередніх версіях, об'єкт `request` передавався як частина пар ключ-значення в контексті для Jinja2.

///

/// tip | Порада

Якщо вказати `response_class=HTMLResponse`, інтерфейс документації знатиме, що відповідь буде HTML.

///

/// note | Технічні деталі

Можна також використати `from starlette.templating import Jinja2Templates`.

**FastAPI** надає той самий `starlette.templating` як `fastapi.templating` просто для зручності для вас, розробника. Але більшість доступних відповідей надходять безпосередньо зі Starlette. Так само з `Request` і `StaticFiles`.

///

## Створення шаблонів { #writing-templates }

Потім ви можете написати шаблон у `templates/item.html`, наприклад:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Значення контексту шаблону { #template-context-values }

У HTML, який містить:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...буде показано `id`, взятий із «контексту» `dict`, який ви передали:

```Python
{"id": id}
```

Наприклад, з ID `42` це буде відображено як:

```html
Item ID: 42
```

### Аргументи `url_for` у шаблоні { #template-url-for-arguments }

Ви також можете використовувати `url_for()` у шаблоні - вона приймає ті самі аргументи, що й ваша *функція операції шляху*.

Тож фрагмент:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...згенерує посилання на той самий URL, який оброблятиме *функція операції шляху* `read_item(id=id)`.

Наприклад, з ID `42` це буде відображено як:

```html
<a href="/items/42">
```

## Шаблони і статичні файли { #templates-and-static-files }

Ви також можете використовувати `url_for()` у шаблоні, наприклад з `StaticFiles`, які ви змонтували з `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

У цьому прикладі це посилатиметься на файл CSS у `static/styles.css` за допомогою:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

І оскільки ви використовуєте `StaticFiles`, цей файл CSS буде автоматично обслуговуватись вашим застосунком **FastAPI** за URL `/static/styles.css`.

## Детальніше { #more-details }

Докладніше, зокрема як тестувати шаблони, дивіться <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">документацію Starlette щодо шаблонів</a>.
