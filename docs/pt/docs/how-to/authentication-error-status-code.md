# Usar antigos códigos de status de erro de autenticação 403 { #use-old-403-authentication-error-status-codes }

Antes da versão `0.122.0` do FastAPI, quando os utilitários de segurança integrados retornavam um erro ao cliente após uma falha na autenticação, eles usavam o código de status HTTP `403 Forbidden`.

A partir da versão `0.122.0` do FastAPI, eles usam o código de status HTTP `401 Unauthorized`, mais apropriado, e retornam um cabeçalho `WWW-Authenticate` adequado na response, seguindo as especificações HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Mas, se por algum motivo seus clientes dependem do comportamento antigo, você pode voltar a ele sobrescrevendo o método `make_not_authenticated_error` nas suas classes de segurança.

Por exemplo, você pode criar uma subclasse de `HTTPBearer` que retorne um erro `403 Forbidden` em vez do erro padrão `401 Unauthorized`:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | Dica

Perceba que a função retorna a instância da exceção, ela não a lança. O lançamento é feito no restante do código interno.

///
