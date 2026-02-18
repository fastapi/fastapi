# Підключення WSGI - Flask, Django та інші { #including-wsgi-flask-django-others }

Ви можете монтувати застосунки WSGI, як ви бачили в [Підзастосунки - монтування](sub-applications.md){.internal-link target=_blank}, [За представником](behind-a-proxy.md){.internal-link target=_blank}.

Для цього ви можете використати `WSGIMiddleware` і обгорнути ним ваш застосунок WSGI, наприклад Flask, Django тощо.

## Використання `WSGIMiddleware` { #using-wsgimiddleware }

/// info | Інформація

Для цього потрібно встановити `a2wsgi`, наприклад за допомогою `pip install a2wsgi`.

///

Потрібно імпортувати `WSGIMiddleware` з `a2wsgi`.

Потім обгорніть застосунок WSGI (напр., Flask) цим проміжним програмним забезпеченням.

І змонтуйте його під певним шляхом.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Примітка

Раніше рекомендувалося використовувати `WSGIMiddleware` з `fastapi.middleware.wsgi`, але тепер його визнано застарілим.

Замість цього радимо використовувати пакет `a2wsgi`. Використання залишається таким самим.

Просто переконайтеся, що у вас встановлено пакет `a2wsgi`, і імпортуйте `WSGIMiddleware` коректно з `a2wsgi`.

///

## Перевірте { #check-it }

Тепер кожен запит за шляхом `/v1/` оброблятиметься застосунком Flask.

А решта - **FastAPI**.

Якщо ви запустите це й перейдете на <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, ви побачите відповідь від Flask:

```txt
Hello, World from Flask!
```

А якщо ви перейдете на <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, ви побачите відповідь від FastAPI:

```JSON
{
    "message": "Hello World"
}
```
