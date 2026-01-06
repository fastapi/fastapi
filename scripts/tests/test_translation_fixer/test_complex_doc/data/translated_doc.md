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

## Ссылки в стиле HTML { #html-style-links }

Это <a href="https://example.com" target="_blank" class="external-link">HTML-ссылка</a> на внешний сайт.

Это <a href="https://fastapi.tiangolo.com">ссылка на основной сайт FastAPI</a> — инструмент должен добавить код языка в URL.

Это <a href="https://fastapi.tiangolo.com/how-to/">ссылка на одну из страниц на сайте FastAPI</a> — инструмент должен добавить код языка в URL.

# Заголовок (с HTML ссылкой на <a href="https://tiangolo.com">tiangolo.com</a>) { #header-5 }

#Не заголовок

```Python
# Также не заголовок
```

Немного текста
