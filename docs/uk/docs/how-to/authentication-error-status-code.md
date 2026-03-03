# Використовуйте старі коди статусу помилки автентифікації 403 { #use-old-403-authentication-error-status-codes }

До версії FastAPI `0.122.0`, коли інтегровані засоби безпеки повертали клієнту помилку після невдалої автентифікації, вони використовували HTTP код статусу `403 Forbidden`.

Починаючи з версії FastAPI `0.122.0`, вони використовують більш доречний HTTP код статусу `401 Unauthorized` і повертають змістовний заголовок `WWW-Authenticate` у відповіді, відповідно до специфікацій HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Але якщо з якоїсь причини ваші клієнти залежать від старої поведінки, ви можете повернутися до неї, переписавши метод `make_not_authenticated_error` у ваших класах безпеки.

Наприклад, ви можете створити підклас `HTTPBearer`, який повертатиме помилку `403 Forbidden` замість типового `401 Unauthorized`:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | Порада

Зверніть увагу, що функція повертає екземпляр винятку, вона не породжує його. Породження відбувається в іншій частині внутрішнього коду.

///
