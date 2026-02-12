# Налагодження { #debugging }

Ви можете під'єднати дебагер у вашому редакторі коду, наприклад, у Visual Studio Code або PyCharm.

## Виклик `uvicorn` { #call-uvicorn }

У вашому FastAPI-додатку імпортуйте та запустіть `uvicorn` безпосередньо:

{* ../../docs_src/debugging/tutorial001_py39.py hl[1,15] *}

### Про `__name__ == "__main__"` { #about-name-main }

Головна мета використання `__name__ == "__main__"` — це забезпечення виконання певного коду лише тоді, коли ваш файл запускається так:

<div class="termy">

```console
$ python myapp.py
```

</div>

але не виконується, коли інший файл імпортує його, наприклад:

```Python
from myapp import app
```

#### Детальніше { #more-details }

Припустимо, ваш файл називається `myapp.py`.

Якщо ви запустите його так:

<div class="termy">

```console
$ python myapp.py
```

</div>

тоді внутрішня змінна `__name__` у вашому файлі, яка створюється автоматично Python, матиме значення рядка `"__main__"`.

Отже, цей блок коду:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

буде виконаний.

---

Це не станеться, якщо ви імпортуєте цей модуль (файл).

Отже, якщо у вас є інший файл `importer.py` з:

```Python
from myapp import app

# Some more code
```

у цьому випадку автоматично створена змінна `__name__` всередині `myapp.py` не матиме значення `"__main__"`.

Отже, рядок:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

не буде виконано.

/// info | Інформація

Для отримання додаткової інформації дивіться <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">офіційну документацію Python</a>.

///

## Запуск коду з вашим дебагером { #run-your-code-with-your-debugger }

Оскільки ви запускаєте сервер Uvicorn безпосередньо з вашого коду, ви можете запустити вашу Python програму (ваш FastAPI-додаток) безпосередньо з дебагера.

---

Наприклад, у Visual Studio Code ви можете:

* Перейдіть на панель «Debug».
* «Add configuration...».
* Виберіть «Python»
* Запустіть дебагер з опцією "`Python: Current File (Integrated Terminal)`".

Після цього він запустить сервер з вашим кодом **FastAPI**, зупиниться на точках зупину тощо.

Ось як це може виглядати:

<img src="/img/tutorial/debugging/image01.png">

---

Якщо ви використовуєте PyCharm, ви можете:

* Відкрити меню «Run».
* Вибрати опцію «Debug...».
* Потім з'явиться контекстне меню.
* Вибрати файл для налагодження (у цьому випадку, `main.py`).

Після цього він запустить сервер з вашим кодом **FastAPI**, зупиниться на точках зупину тощо.

Ось як це може виглядати:

<img src="/img/tutorial/debugging/image02.png">
