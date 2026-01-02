# Дані форми { #form-data }

Якщо вам потрібно отримувати поля форми замість JSON, ви можете використовувати `Form`.

/// info | Інформація

Щоб використовувати форми, спочатку встановіть <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Переконайтеся, що ви створили [віртуальне середовище](../virtual-environments.md){.internal-link target=_blank}, активували його, і потім встановили бібліотеку, наприклад:

```console
$ pip install python-multipart
```

///

## Імпорт `Form` { #import-form }

Імпортуйте `Form` з `fastapi`:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[3] *}

## Оголошення параметрів `Form` { #define-form-parameters }

Створюйте параметри форми так само як ви б створювали `Body` або `Query`:

{* ../../docs_src/request_forms/tutorial001_an_py39.py hl[9] *}

Наприклад, один зі способів використання специфікації OAuth2 (так званий "password flow") вимагає надсилати `username` та `password` як поля форми.

<abbr title="specification">spec</abbr> вимагає, щоб ці поля мали точні назви `username` і `password` та надсилалися у вигляді полів форми, а не JSON.

З `Form` ви можете оголошувати ті ж конфігурації, що і з `Body` (та `Query`, `Path`, `Cookie`), включаючи валідацію, приклади, псевдоніми (наприклад, `user-name` замість `username`) тощо.

/// info | Інформація

`Form` — це клас, який безпосередньо наслідується від `Body`.

///

/// tip | Порада

Щоб оголосити тіло форми, потрібно явно використовувати `Form`, оскільки без нього параметри будуть інтерпретуватися як параметри запиту або тіла (JSON).

///

## Про "поля форми" { #about-form-fields }

HTML-форми (`<form></form>`) надсилають дані на сервер у "спеціальному" кодуванні, яке відрізняється від JSON.

**FastAPI** подбає про те, щоб зчитати ці дані з правильного місця, а не з JSON.

/// note | Технічні деталі

Дані з форм зазвичай кодуються за допомогою "типу медіа" `application/x-www-form-urlencoded`.

Але якщо форма містить файли, вона кодується як `multipart/form-data`. Ви дізнаєтеся про обробку файлів у наступному розділі.

Якщо ви хочете дізнатися більше про ці кодування та поля форм, зверніться до <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> вебдокументації для <code>POST</code></a>.

///

/// warning | Попередження

Ви можете оголосити кілька параметрів `Form` в *операції шляху*, але не можете одночасно оголосити поля `Body`, які ви очікуєте отримати у форматі JSON, оскільки запит матиме тіло, закодоване як `application/x-www-form-urlencoded`, а не `application/json`.

Це не обмеження **FastAPI**, а частина HTTP-протоколу.

///

## Підсумок { #recap }

Використовуйте `Form` для оголошення вхідних параметрів у вигляді даних форми.
