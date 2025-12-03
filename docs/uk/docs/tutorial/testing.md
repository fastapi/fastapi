# Тестування

Тестування **FastAPI**  додатків є простим та ефективним завдяки бібліотеці <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>, яка базується на <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>.
Оскільки HTTPX розроблений на основі Requests, його API є інтуїтивно зрозумілим для тих, хто вже знайомий з Requests.

З його допомогою Ви можете використовувати <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> безпосередньо з **FastAPI**.

## Використання `TestClient`

/// info | Інформація

Щоб використовувати `TestClient`, спочатку встановіть <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Переконайтеся, що Ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його, а потім встановили саму бібліотеку, наприклад:

```console
$ pip install httpx
```

///

Імпортуйте `TestClient`.

Створіть `TestClient`, передавши йому Ваш застосунок **FastAPI**.

Створюйте функції з іменами, що починаються з `test_` (це стандартна угода для `pytest`).

Використовуйте об'єкт `TestClient` так само як і `httpx`.

Записуйте прості `assert`-вирази зі стандартними виразами Python, які потрібно перевірити (це також стандарт для `pytest`).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}


/// tip | Порада

Зверніть увагу, що тестові функції — це звичайні `def`, а не `async def`.

Виклики клієнта також звичайні, без використання `await`.

Це дозволяє використовувати `pytest` без зайвих ускладнень.

///

/// note | Технічні деталі

Ви також можете використовувати `from starlette.testclient import TestClient`.

**FastAPI** надає той самий `starlette.testclient` під назвою `fastapi.testclient` для зручності розробників, але він безпосередньо походить із Starlette.

///

/// tip | Порада

Якщо Вам потрібно викликати `async`-функції у ваших тестах, окрім відправлення запитів до FastAPI-застосунку (наприклад, асинхронні функції роботи з базою даних), перегляньте [Асинхронні тести](../advanced/async-tests.md){.internal-link target=_blank} у розширеному керівництві.

///

## Розділення тестів

У реальному застосунку Ваші тести, ймовірно, будуть в окремому файлі.

Також Ваш **FastAPI**-застосунок може складатися з кількох файлів або модулів тощо.

### Файл застосунку **FastAPI**

Припустимо, у Вас є структура файлів, описана в розділі [Більші застосунки](bigger-applications.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```
У файлі `main.py` знаходиться Ваш застосунок **FastAPI** :

{* ../../docs_src/app_testing/main.py *}

### Файл тестування

Ви можете створити файл `test_main.py` з Вашими тестами. Він може знаходитися в тому ж пакеті Python (у тій самій директорії з файлом `__init__.py`):


``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Оскільки цей файл знаходиться в тому ж пакеті, Ви можете використовувати відносний імпорт, щоб імпортувати об'єкт `app`  із модуля `main` (`main.py`):

{* ../../docs_src/app_testing/test_main.py hl[3] *}


...і написати код для тестів так само як і раніше.

## Тестування: розширений приклад

Тепер розширимо цей приклад і додамо більше деталей, щоб побачити, як тестувати різні частини.

### Розширений файл застосунку **FastAPI**

Залишимо ту саму структуру файлів:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Припустимо, що тепер файл `main.py` із Вашим **FastAPI**-застосунком містить додаткові операції шляху (**path operations**).

Він має `GET`-операцію, яка може повертати помилку.

Він має `POST`-операцію, яка може повертати кілька помилок.

Обидві операції шляху вимагають заголовок `X-Token`.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Порада

Бажано використовувати версію з `Annotated`, якщо це можливо

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Порада

Бажано використовувати версію з `Annotated`, якщо це можливо

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### Розширений тестовий файл

Потім Ви можете оновити `test_main.py`, додавши розширені тести:

{* ../../docs_src/app_testing/app_b/test_main.py *}

Коли Вам потрібно передати клієнту інформацію в запиті, але Ви не знаєте, як це зробити, Ви можете пошукати (наприклад, у Google) спосіб реалізації в `httpx`, або навіть у `requests`, оскільки HTTPX розроблений на основі дизайну Requests.

Далі Ви просто повторюєте ці ж дії у ваших тестах.

Наприклад:

* Щоб передати *path* або *query* параметр, додайте його безпосередньо до URL.
* Щоб передати тіло JSON, передайте Python-об'єкт (наприклад, `dict`) у параметр `json`.
* Якщо потрібно надіслати *Form Data* замість JSON, використовуйте параметр `data`.
* Щоб передати заголовки *headers*, використовуйте `dict` у параметрі `headers`.
* Для *cookies* використовуйте `dict` у параметрі `cookies`.

Докладніше про передачу даних у бекенд (за допомогою `httpx` або `TestClient`) можна знайти в <a href="https://www.python-httpx.org" class="external-link" target="_blank">документації HTTPX</a>.

/// info | Інформація

Зверніть увагу, що `TestClient` отримує дані, які можна конвертувати в JSON, а не Pydantic-моделі.
Якщо у Вас є Pydantic-модель у тесті, і Ви хочете передати її дані в додаток під час тестування, Ви можете використати `jsonable_encoder`, описаний у розділі [JSON Compatible Encoder](encoder.md){.internal-link target=_blank}.

///

## Запуск тестів

Після цього вам потрібно встановити `pytest`.

Переконайтеся, що Ви створили [віртуальне середовище]{.internal-link target=_blank}, активували його і встановили необхідні пакети, наприклад:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

`pytest` автоматично знайде файли з тестами, виконає їх і надасть вам результати.

Запустіть тести за допомогою:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
