# Тестування { #testing }

Завдяки <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a> тестувати застосунки **FastAPI** просто й приємно.

Воно базується на <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, який, своєю чергою, спроєктований на основі Requests, тож він дуже знайомий та інтуїтивно зрозумілий.

З його допомогою ви можете використовувати <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> безпосередньо з **FastAPI**.

## Використання `TestClient` { #using-testclient }

/// info | Інформація

Щоб використовувати `TestClient`, спочатку встановіть <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його, а потім встановили `httpx`, наприклад:

```console
$ pip install httpx
```

///

Імпортуйте `TestClient`.

Створіть `TestClient`, передавши йому ваш застосунок **FastAPI**.

Створюйте функції з іменами, що починаються з `test_` (це стандартна угода для `pytest`).

Використовуйте об'єкт `TestClient` так само як і `httpx`.

Записуйте прості `assert`-вирази зі стандартними виразами Python, які потрібно перевірити (це також стандарт для `pytest`).

{* ../../docs_src/app_testing/tutorial001_py39.py hl[2,12,15:18] *}

/// tip | Порада

Зверніть увагу, що тестові функції — це звичайні `def`, а не `async def`.

Виклики клієнта також звичайні, без використання `await`.

Це дозволяє використовувати `pytest` без зайвих ускладнень.

///

/// note | Технічні деталі

Ви також можете використовувати `from starlette.testclient import TestClient`.

**FastAPI** надає той самий `starlette.testclient` під назвою `fastapi.testclient` просто для зручності для вас, розробника. Але він безпосередньо походить із Starlette.

///

/// tip | Порада

Якщо ви хочете викликати `async`-функції у ваших тестах, окрім відправлення запитів до вашого застосунку FastAPI (наприклад, асинхронні функції роботи з базою даних), перегляньте [Async Tests](../advanced/async-tests.md){.internal-link target=_blank} у розширеному керівництві.

///

## Розділення тестів { #separating-tests }

У реальному застосунку ваші тести, ймовірно, будуть в окремому файлі.

Також ваш застосунок **FastAPI** може складатися з кількох файлів/модулів тощо.

### Файл застосунку **FastAPI** { #fastapi-app-file }

Припустимо, у вас є структура файлів, описана в розділі [Bigger Applications](bigger-applications.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

У файлі `main.py` знаходиться ваш застосунок **FastAPI**:


{* ../../docs_src/app_testing/app_a_py39/main.py *}

### Файл тестування { #testing-file }

Ви можете створити файл `test_main.py` з вашими тестами. Він може знаходитися в тому ж пакеті Python (у тій самій директорії з файлом `__init__.py`):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Оскільки цей файл знаходиться в тому ж пакеті, ви можете використовувати відносний імпорт, щоб імпортувати об'єкт `app`  із модуля `main` (`main.py`):

{* ../../docs_src/app_testing/app_a_py39/test_main.py hl[3] *}


...і написати код для тестів так само як і раніше.

## Тестування: розширений приклад { #testing-extended-example }

Тепер розширимо цей приклад і додамо більше деталей, щоб побачити, як тестувати різні частини.

### Розширений файл застосунку **FastAPI** { #extended-fastapi-app-file }

Залишимо ту саму структуру файлів:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Припустимо, що тепер файл `main.py` із вашим застосунком **FastAPI** містить інші **операції шляху**.

Він має `GET`-операцію, яка може повертати помилку.

Він має `POST`-операцію, яка може повертати кілька помилок.

Обидві *операції шляху* вимагають заголовок `X-Token`.

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### Розширений тестовий файл { #extended-testing-file }

Потім ви можете оновити `test_main.py`, додавши розширені тести:

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


Коли вам потрібно передати клієнту інформацію в запиті, але ви не знаєте, як це зробити, ви можете пошукати (Google), як це зробити в `httpx`, або навіть як це зробити з `requests`, оскільки дизайн HTTPX базується на дизайні Requests.

Далі ви просто повторюєте ці ж дії у ваших тестах.

Наприклад:

* Щоб передати *path* або *query* параметр, додайте його безпосередньо до URL.
* Щоб передати тіло JSON, передайте Python-об'єкт (наприклад, `dict`) у параметр `json`.
* Якщо потрібно надіслати *Form Data* замість JSON, використовуйте параметр `data`.
* Щоб передати заголовки *headers*, використовуйте `dict` у параметрі `headers`.
* Для *cookies* використовуйте `dict` у параметрі `cookies`.

Докладніше про передачу даних у бекенд (за допомогою `httpx` або `TestClient`) можна знайти в <a href="https://www.python-httpx.org" class="external-link" target="_blank">документації HTTPX</a>.

/// info | Інформація

Зверніть увагу, що `TestClient` отримує дані, які можна конвертувати в JSON, а не Pydantic-моделі.

Якщо у вас є Pydantic-модель у тесті, і ви хочете передати її дані в застосунок під час тестування, ви можете використати `jsonable_encoder`, описаний у розділі [JSON Compatible Encoder](encoder.md){.internal-link target=_blank}.

///

## Запуск { #run-it }

Після цього вам потрібно встановити `pytest`.

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його і встановили необхідні пакети, наприклад:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Він автоматично знайде файли та тести, виконає їх і повідомить вам результати.

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
