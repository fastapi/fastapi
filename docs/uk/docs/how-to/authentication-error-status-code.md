# Використання старих кодів стану 403 для помилок автентифікації { #use-old-403-authentication-error-status-codes }

До версії FastAPI `0.122.0`, коли вбудовані утиліти безпеки повертали клієнту помилку після невдалої автентифікації, вони використовували код стану HTTP `403 Forbidden`.

Починаючи з FastAPI `0.122.0`, вони використовують більш доречний код стану HTTP `401 Unauthorized` і повертають у відповіді коректний заголовок `WWW-Authenticate`, дотримуючись специфікацій HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Але якщо з певної причини ваші клієнти залежать від старої поведінки, ви можете повернути її, перевизначивши метод `make_not_authenticated_error` у ваших класах безпеки.

Наприклад, ви можете створити підклас `HTTPBearer`, який повертає помилку `403 Forbidden` замість типової `401 Unauthorized`:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | Порада

Зверніть увагу: функція повертає екземпляр винятку, а не піднімає його. Підняття виконується в іншій частині внутрішнього коду.

///
