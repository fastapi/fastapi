# Использование старых статус-кодов ошибок аутентификации 403 { #use-old-403-authentication-error-status-codes }

До версии FastAPI `0.122.0`, когда встроенные утилиты безопасности возвращали ошибку клиенту после неудачной аутентификации, они использовали HTTP статус-код `403 Forbidden`.

Начиная с версии FastAPI `0.122.0`, используется более подходящий HTTP статус-код `401 Unauthorized`, и в ответе возвращается имеющий смысл HTTP-заголовок `WWW-Authenticate` в соответствии со спецификациями HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Но если по какой-то причине ваши клиенты зависят от старого поведения, вы можете вернуть его, переопределив метод `make_not_authenticated_error` в ваших Security-классах.

Например, вы можете создать подкласс `HTTPBearer`, который будет возвращать ошибку `403 Forbidden` вместо стандартной `401 Unauthorized`:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | Совет

Обратите внимание, что функция возвращает экземпляр исключения, не вызывает его. Выброс выполняется остальным внутренним кодом.

///
