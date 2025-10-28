# Retornando uma Resposta Diretamente { #return-a-response-directly }

Quando você cria uma *operação de rota* no **FastAPI** você pode retornar qualquer dado nela: um dicionário (`dict`), uma lista (`list`), um modelo do Pydantic ou do seu banco de dados, etc.

Por padrão, o **FastAPI** irá converter automaticamente o valor do retorno para JSON utilizando o `jsonable_encoder` explicado em [JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank}.

Então, por baixo dos panos, ele incluiria esses dados compatíveis com JSON (e.g. um `dict`) dentro de uma `JSONResponse` que é utilizada para enviar uma resposta para o cliente.

Mas você pode retornar a `JSONResponse` diretamente nas suas *operações de rota*.

Pode ser útil para retornar cabeçalhos e cookies personalizados, por exemplo.

## Retornando uma `Response` { #return-a-response }

Na verdade, você pode retornar qualquer `Response` ou subclasse dela.

/// tip | Dica

A própria `JSONResponse` é uma subclasse de `Response`.

///

E quando você retorna uma `Response`, o **FastAPI** vai repassá-la diretamente.

Ele não vai fazer conversões de dados com modelos do Pydantic, não irá converter a tipagem de nenhum conteúdo, etc.

Isso te dá bastante flexibilidade. Você pode retornar qualquer tipo de dado, sobrescrever qualquer declaração e validação nos dados, etc.

## Utilizando o `jsonable_encoder` em uma `Response` { #using-the-jsonable-encoder-in-a-response }

Como o **FastAPI** não realiza nenhuma mudança na `Response` que você retorna, você precisa garantir que o conteúdo dela está pronto para uso.

Por exemplo, você não pode colocar um modelo do Pydantic em uma `JSONResponse` sem antes convertê-lo em um `dict` com todos os tipos de dados (como `datetime`, `UUID`, etc) convertidos para tipos compatíveis com JSON.

Para esses casos, você pode usar o `jsonable_encoder` para converter seus dados antes de repassá-los para a resposta:

{* ../../docs_src/response_directly/tutorial001.py hl[6:7,21:22] *}

/// note | Detalhes Técnicos

Você também pode utilizar `from starlette.responses import JSONResponse`.

**FastAPI** utiliza a mesma `starlette.responses` como `fastapi.responses` apenas como uma conveniência para você, desenvolvedor. Mas maior parte das respostas disponíveis vem diretamente do Starlette.

///

## Retornando uma `Response` personalizada { #returning-a-custom-response }

O exemplo acima mostra todas as partes que você precisa, mas ainda não é muito útil, já que você poderia ter retornado o `item` diretamente, e o **FastAPI** colocaria em uma `JSONResponse` para você, convertendo em um `dict`, etc. Tudo isso por padrão.

Agora, vamos ver como você pode usar isso para retornar uma resposta personalizada.

Vamos dizer que você quer retornar uma resposta <a href="https://en.wikipedia.org/wiki/XML" class="external-link" target="_blank">XML</a>.

Você pode colocar o seu conteúdo XML em uma string, colocar em uma `Response`, e retorná-lo:

{* ../../docs_src/response_directly/tutorial002.py hl[1,18] *}

## Notas { #notes }

Quando você retorna uma `Response` diretamente os dados não são validados, convertidos (serializados) ou documentados automaticamente.

Mas você ainda pode documentar como descrito em [Retornos Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.

Você pode ver nas próximas seções como usar/declarar essas `Responses` customizadas enquanto mantém a conversão e documentação automática dos dados.
