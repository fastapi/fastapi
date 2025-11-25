# Retorno - Altere o Código de Status { #response-change-status-code }

Você provavelmente leu anteriormente que você pode definir um [Código de Status do Retorno](../tutorial/response-status-code.md){.internal-link target=_blank} padrão.

Porém em alguns casos você precisa retornar um código de status diferente do padrão.

## Caso de uso { #use-case }

Por exemplo, imagine que você deseja retornar um código de status HTTP de "OK" `200` por padrão.

Mas se o dado não existir, você quer criá-lo e retornar um código de status HTTP de "CREATED" `201`.

Mas você ainda quer ser capaz de filtrar e converter o dado que você retornará com um `response_model`.

Para estes casos, você pode utilizar um parâmetro `Response`.

## Use um parâmetro `Response` { #use-a-response-parameter }

Você pode declarar um parâmetro do tipo `Response` em sua *função de operação de rota* (assim como você pode fazer para cookies e headers).

E então você pode definir o `status_code` neste objeto de retorno temporal.

{* ../../docs_src/response_change_status_code/tutorial001.py hl[1,9,12] *}

E então você pode retornar qualquer objeto que você precise, como você faria normalmente (um `dict`, um modelo de banco de dados, etc.).

E se você declarar um `response_model`, ele ainda será utilizado para filtrar e converter o objeto que você retornou.

O **FastAPI** utilizará este retorno *temporal* para extrair o código de status (e também cookies e headers), e irá colocá-los no retorno final que contém o valor que você retornou, filtrado por qualquer `response_model`.

Você também pode declarar o parâmetro `Response` nas dependências, e definir o código de status nelas. Mas lembre-se que o último que for definido é o que prevalecerá.
