# Middleware (Промежуточный слой) { #middleware }

Вы можете добавить промежуточный слой (middleware) в **FastAPI** приложение.

"Middleware" это функция, которая выполняется с каждым запросом до его обработки какой-либо конкретной *операцией пути*.
А также с каждым ответом перед его возвращением.


* Она принимает каждый поступающий **запрос**.
* Может что-то сделать с этим **запросом** или выполнить любой нужный код.
* Затем передает **запрос** для последующей обработки (какой-либо *операцией пути*).
* Получает **ответ** (от *операции пути*).
* Может что-то сделать с этим **ответом** или выполнить любой нужный код.
* И возвращает **ответ**.

/// note | Технические детали

Если у вас есть зависимости с `yield`, то код выхода (код после `yield`) будет выполняться *после* middleware.

Если были какие‑либо фоновые задачи (рассматриваются в разделе [Фоновые задачи](background-tasks.md){.internal-link target=_blank}, вы увидите это позже), они будут запущены *после* всех middleware.

///

## Создание middleware { #create-a-middleware }

Для создания middleware используйте декоратор `@app.middleware("http")`.

Функция middleware получает:

* `request` (объект запроса).
* Функцию `call_next`, которая получает `request` в качестве параметра.
    * Эта функция передаёт `request` соответствующей *операции пути*.
    * Затем она возвращает ответ `response`, сгенерированный *операцией пути*.
* Также имеется возможность видоизменить `response`, перед тем как его вернуть.

{* ../../docs_src/middleware/tutorial001.py hl[8:9,11,14] *}

/// tip | Примечание

Имейте в виду, что можно добавлять свои собственные заголовки <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">при помощи префикса 'X-'</a>.

Если же вы хотите добавить собственные заголовки, которые клиент сможет увидеть в браузере, то вам потребуется добавить их в настройки CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}), используя параметр `expose_headers`, см. документацию <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>.

///

/// note | Технические детали

Вы также можете использовать `from starlette.requests import Request`.

**FastAPI** предоставляет такой доступ для удобства разработчиков. Но, на самом деле, это `Request` из Starlette.

///

### До и после `response` { #before-and-after-the-response }

Вы можете добавить код, использующий `request` до передачи его какой-либо *операции пути*.

А также после формирования `response`, до того, как вы его вернёте.

Например, вы можете добавить собственный заголовок `X-Process-Time`, содержащий время в секундах, необходимое для обработки запроса и генерации ответа:

{* ../../docs_src/middleware/tutorial001.py hl[10,12:13] *}

/// tip | Примечание

Мы используем <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> вместо `time.time()` для обеспечения большей точности наших примеров. 🤓

///

## Порядок выполнения нескольких middleware { #multiple-middleware-execution-order }

Когда вы добавляете несколько middleware с помощью декоратора `@app.middleware()` или метода `app.add_middleware()`, каждое новое middleware оборачивает приложение, формируя стек. Последнее добавленное middleware — самое внешнее (*outermost*), а первое — самое внутреннее (*innermost*).

На пути обработки запроса сначала выполняется самое внешнее middleware.

На пути формирования ответа оно выполняется последним.

Например:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

Это приводит к следующему порядку выполнения:

* **Запрос**: MiddlewareB → MiddlewareA → маршрут

* **Ответ**: маршрут → MiddlewareA → MiddlewareB

Такое стековое поведение обеспечивает предсказуемый и управляемый порядок выполнения middleware.

## Другие middleware { #other-middlewares }

О других middleware вы можете узнать больше в разделе [Advanced User Guide: Advanced Middleware](../advanced/middleware.md){.internal-link target=_blank}.

В следующем разделе вы можете прочитать, как настроить <abbr title="Cross-Origin Resource Sharing – совместное использование ресурсов между источниками">CORS</abbr> с помощью middleware.
