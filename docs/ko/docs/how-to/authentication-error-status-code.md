# 이전 403 인증 오류 상태 코드 사용하기 { #use-old-403-authentication-error-status-codes }

FastAPI 버전 `0.122.0` 이전에는, 통합 보안 유틸리티가 인증 실패 후 클라이언트에 오류를 반환할 때 HTTP 상태 코드 `403 Forbidden`을 사용했습니다.

FastAPI 버전 `0.122.0`부터는 더 적절한 HTTP 상태 코드 `401 Unauthorized`를 사용하며, HTTP 명세인 <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>를 따라 응답에 합리적인 `WWW-Authenticate` 헤더를 반환합니다.

하지만 어떤 이유로든 클라이언트가 이전 동작에 의존하고 있다면, 보안 클래스에서 `make_not_authenticated_error` 메서드를 오버라이드하여 이전 동작으로 되돌릴 수 있습니다.

예를 들어, 기본값인 `401 Unauthorized` 오류 대신 `403 Forbidden` 오류를 반환하는 `HTTPBearer`의 서브클래스를 만들 수 있습니다:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | 팁

함수는 예외를 `raise`하는 것이 아니라 예외 인스턴스를 `return`한다는 점에 유의하세요. 예외를 발생시키는(`raise`) 작업은 내부 코드의 나머지 부분에서 수행됩니다.

///
