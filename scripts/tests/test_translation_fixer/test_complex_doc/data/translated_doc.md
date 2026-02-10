# Тестовый инструмент исправления переводов { #test-translation-fixer }

## Блоки кода с комментариями и без комментариев { #code-blocks-with-and-without-comments }

Это тестовая страница для инструмента исправления переводов.

### Блоки кода с комментариями { #code-blocks-with-comments }

Следующие блоки кода содержат комментарии в разных стилях.
Инструмент исправления должен исправлять содержимое, но корректно сохранять комментарии.

```python
# Это пример блока кода на Python
def hello_world():
    # Комментарий с отступом
    print("Hello, world!")  # Печать приветствия
```

```toml
# Это пример блока кода на TOML
title = "TOML Example"  # Заголовок документа
```

```console
// Используйте команду "live" и передайте код языка в качестве аргумента CLI
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

```json
{
    // Это пример блока кода на JSON
    "greeting": "Hello, world!" // Печать приветствия
}
```


### Блоки кода с комментариями, где язык использует другие стили комментариев { #code-blocks-with-different-comment-styles }

Следующие блоки кода содержат комментарии в разных стилях в зависимости от языка.
Инструмент исправления не будет сохранять комментарии в этих блоках.

```json
{
    # Это пример блока кода на JSON
    "greeting": "Hello, world!" # Печать приветствия
}
```

```console
# Это пример блока кода консоли
$ echo "Hello, world!"  # Печать приветствия
```

```toml
// Это пример блока кода на TOML
title = "TOML Example"  // Заголовок документа
```

### Блоки кода с комментариями на неподдерживаемых языках или без указания языка { #code-blocks-with-unsupported-languages }

Следующие блоки кода используют неподдерживаемые языки для сохранения комментариев.
Инструмент исправления не будет сохранять комментарии в этих блоках.

```javascript
// Это пример блока кода на JavaScript
console.log("Hello, world!"); // Печать приветствия
```

```
# Это пример блока кода консоли
$ echo "Hello, world!"  # Печать приветствия
```

```
// Это пример блока кода консоли
$ echo "Hello, world!"  // Печать приветствия
```

### Блоки кода с комментариями, которые не соответствуют шаблону { #code-blocks-with-comments-without-pattern }

Инструмент исправления ожидает комментарии, которые соответствуют определённому шаблону:

- Для комментариев в стиле с решёткой: комментарий начинается с `# ` (решётка, затем пробел) в начале строки или после пробела.
- Для комментариев в стиле со слешами: комментарий начинается с `// ` (два слеша, затем пробел) в начале строки или после пробела.

Если комментарий не соответствует этому шаблону, инструмент исправления не будет его сохранять.

```python
#Объявление функции
def hello_world():# Печать приветствия
    print("Hello, world!")  #Печать приветствия без пробела после решётки
```

```console
//Объявление функции
def hello_world():// Печать приветствия
    print("Hello, world!")  //Печать приветствия без пробела после слешей
```

## Блок кода с четырёхкратными обратными кавычками { #code-blocks-with-quadruple-backticks }

Следующий блок кода содержит четырёхкратные обратные кавычки.

````python
# Функция приветствия
def hello_world():
    print("Hello, world")  # Печать приветствия
````

### Несоответствие обратных кавычек фиксится { #backticks-number-mismatch-is-fixable }

Следующий блок кода имеет тройные обратные кавычки в оригинальном документе, но четырёхкратные обратные кавычки в переведённом документе.
Это будет исправлено инструментом исправления (будет преобразовано в тройные обратные кавычки).

````Python
# Немного кода на Python
````

### Блок кода в тройных обратных кавычка внутри блока кода в четырёхкратных обратных кавычках { #triple-backticks-inside-quadruple-backticks }

Комментарии внутри вложенного блока кода в тройных обратных кавычках НЕ БУДУТ сохранены.

````
Here is a code block with quadruple backticks that contains triple backticks inside:

```python
# Этот комментарий НЕ будет сохранён
def hello_world():
    print("Hello, world")  # Как и этот комментарий
```

````

# Включения кода { #code-includes }

## Простые включения кода { #simple-code-includes }

{* ../../docs_src/python_types/tutorial001_py39.py *}

{* ../../docs_src/python_types/tutorial002_py39.py *}


## Включения кода с подсветкой { #code-includes-with-highlighting }

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

{* ../../docs_src/python_types/tutorial006_py39.py hl[10] *}


## Включения кода с диапазонами строк { #code-includes-with-line-ranges }

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[19:21] *}

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] *}


## Включения кода с диапазонами строк и подсветкой { #code-includes-with-line-ranges-and-highlighting }

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[30:38] hl[31:33] *}

{* ../../docs_src/dependencies/tutorial015_an_py310.py ln[10:15] hl[12:14] *}


## Включения кода с заголовком { #code-includes-with-title }

{* ../../docs_src/bigger_applications/app_an_py39/routers/users.py hl[1,3] title["app/routers/users.py"] *}

{* ../../docs_src/bigger_applications/app_an_py39/internal/admin.py hl[3] title["app/internal/admin.py"] *}

## Включения кода с неизвестными атрибутами { #code-includes-with-unknown-attributes }

{* ../../docs_src/python_types/tutorial001_py39.py unknown[123] *}

## Ещё включения кода для тестирования исправления { #some-more-code-includes-to-test-fixing }

{*    ../../docs_src/dependencies/tutorial013_an_py310.py     ln[19 : 21]    *}

{* ../../docs_src/bigger_applications/app_an_py39/wrong.py hl[3] title["app/internal/admin.py"] *}

{* ../../docs_src/dependencies/tutorial013_an_py310.py ln[1:30] hl[1:10] *}

# Ссылки { #links }

## Ссылки в стиле Markdown { #markdown-style-links }

Это [Markdown-ссылка](https://example.com) на внешний сайт.

Это ссылка с атрибутами: [**FastAPI** генераторы проектов](project-generation.md){.internal-link target=_blank}

Это ссылка на основной сайт FastAPI: [FastAPI](https://fastapi.tiangolo.com) — инструмент должен добавить код языка в URL.

Это ссылка на одну из страниц на сайте FastAPI: [How to](https://fastapi.tiangolo.com/how-to) — инструмент должен добавить код языка в URL.

Ссылка для тестирования неправильного атрибута: [**FastAPI** генераторы проектов](project-generation.md){.external-link} - инструмент должен исправить атрибут.

Ссылка с заголовком: [Пример](http://example.com/ "Сайт для примера") - URL будет исправлен инструментом, заголовок сохранится.

### Markdown ссылки на статические ресурсы { #markdown-link-to-static-assets }

Это ссылки на статические ресурсы:

* [FastAPI Logo](https://fastapi.tiangolo.com/img/fastapi-logo.png)
* [FastAPI CSS](https://fastapi.tiangolo.com/css/fastapi.css)
* [FastAPI JS](https://fastapi.tiangolo.com/js/fastapi.js)

Инструмент НЕ должен добавлять код языка в их URL.

## Ссылки в стиле HTML { #html-style-links }

Это <a href="https://example.com" target="_blank" class="external-link">HTML-ссылка</a> на внешний сайт.

Это <a href="https://fastapi.tiangolo.com">ссылка на основной сайт FastAPI</a> — инструмент должен добавить код языка в URL.

Это <a href="https://fastapi.tiangolo.com/how-to/">ссылка на одну из страниц на сайте FastAPI</a> — инструмент должен добавить код языка в URL.

Ссылка для тестирования неправильного атрибута: <a href="project-generation.md" class="external-link">**FastAPI** генераторы проектов</a> - инструмент должен исправить атрибут.

### HTML ссылки на статические ресурсы { #html-links-to-static-assets }

Это ссылки на статические ресурсы:

* <a href="https://fastapi.tiangolo.com/img/fastapi-logo.png">FastAPI Logo</a>
* <a href="https://fastapi.tiangolo.com/css/fastapi.css">FastAPI CSS</a>
* <a href="https://fastapi.tiangolo.com/js/fastapi.js">FastAPI JS</a>

Инструмент НЕ должен добавлять код языка в их URL.

# Заголовок (с HTML ссылкой на <a href="https://tiangolo.com">tiangolo.com</a>) { #header-5 }

#Не заголовок

```Python
# Также не заголовок
```

Немного текста
