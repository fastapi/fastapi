# Шаблоны { #templates }

Вы можете использовать любой шаблонизатор вместе с **FastAPI**.

Часто выбирают Jinja2 — тот же, что используется во Flask и других инструментах.

Есть утилиты для простой настройки, которые вы можете использовать прямо в своем приложении **FastAPI** (предоставляются Starlette).

## Установка зависимостей { #install-dependencies }

Убедитесь, что вы создали [виртуальное окружение](../virtual-environments.md){.internal-link target=_blank}, активировали его и установили `jinja2`:

<div class="termy">

```console
$ pip install jinja2

---> 100%
```

</div>

## Использование `Jinja2Templates` { #using-jinja2templates }

- Импортируйте `Jinja2Templates`.
- Создайте объект `templates`, который сможете переиспользовать позже.
- Объявите параметр `Request` в *операции пути*, которая будет возвращать шаблон.
- Используйте созданный `templates`, чтобы отрендерить и вернуть `TemplateResponse`; передайте имя шаблона, объект `request` и словарь «context» с парами ключ-значение для использования внутри шаблона Jinja2.

{* ../../docs_src/templates/tutorial001.py hl[4,11,15:18] *}

/// note | Примечание

До FastAPI 0.108.0, Starlette 0.29.0, `name` был первым параметром.

Также раньше, в предыдущих версиях, объект `request` передавался как часть пар ключ-значение в контексте для Jinja2.

///

/// tip | Совет

Если указать `response_class=HTMLResponse`, интерфейс документации сможет определить, что ответ будет в формате HTML.

///

/// note | Технические детали

Можно также использовать `from starlette.templating import Jinja2Templates`.

**FastAPI** предоставляет тот же `starlette.templating` как `fastapi.templating` просто для удобства разработчика. Но большинство доступных ответов приходят напрямую из Starlette. Так же и с `Request` и `StaticFiles`.

///

## Написание шаблонов { #writing-templates }

Затем вы можете создать шаблон в `templates/item.html`, например:

```jinja hl_lines="7"
{!../../docs_src/templates/templates/item.html!}
```

### Значения контекста шаблона { #template-context-values }

В HTML, который содержит:

{% raw %}

```jinja
Item ID: {{ id }}
```

{% endraw %}

...будет показан `id`, взятый из переданного вами «context» `dict`:

```Python
{"id": id}
```

Например, для ID `42` это отрендерится как:

```html
Item ID: 42
```

### Аргументы `url_for` в шаблоне { #template-url-for-arguments }

Вы также можете использовать `url_for()` внутри шаблона — он принимает те же аргументы, что использовались бы вашей *функцией-обработчиком пути*.

Таким образом, фрагмент:

{% raw %}

```jinja
<a href="{{ url_for('read_item', id=id) }}">
```

{% endraw %}

...сгенерирует ссылку на тот же URL, который обрабатывается *функцией-обработчиком пути* `read_item(id=id)`.

Например, для ID `42` это отрендерится как:

```html
<a href="/items/42">
```

## Шаблоны и статические файлы { #templates-and-static-files }

Вы также можете использовать `url_for()` внутри шаблона, например, с `StaticFiles`, которые вы монтировали с `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

В этом примере будет создана ссылка на CSS-файл `static/styles.css` с помощью:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

И, так как вы используете `StaticFiles`, этот CSS-файл будет автоматически «отдаваться» вашим приложением **FastAPI** по URL `/static/styles.css`.

## Подробнее { #more-details }

Больше подробностей, включая то, как тестировать шаблоны, смотрите в <a href="https://www.starlette.dev/templates/" class="external-link" target="_blank">документации Starlette по шаблонам</a>.
