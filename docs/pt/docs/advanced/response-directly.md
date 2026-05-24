# Retornando uma Resposta Diretamente { #return-a-response-directly }

Quando você cria uma *operação de rota* no **FastAPI**, normalmente você pode retornar qualquer dado: um `dict`, uma `list`, um modelo do Pydantic, um modelo do banco de dados, etc.

Se você declarar um [Modelo de resposta](../tutorial/response-model.md), o FastAPI irá usá-lo para serializar os dados para JSON, usando o Pydantic.

Se você não declarar um modelo de resposta, o FastAPI usará o `jsonable_encoder` explicado em [Codificador Compatível com JSON](../tutorial/encoder.md) e o colocará em uma `JSONResponse`.

Você também pode criar uma `JSONResponse` diretamente e retorná-la.

/// tip | Dica

Normalmente você terá um desempenho muito melhor usando um [Modelo de resposta](../tutorial/response-model.md) do que retornando uma `JSONResponse` diretamente, pois assim ele serializa os dados usando o Pydantic, em Rust.

///

## Retornando uma `Response` { #return-a-response }

Você pode retornar uma `Response` ou qualquer subclasse dela.

/// info | Informação

A própria `JSONResponse` é uma subclasse de `Response`.

///

E quando você retorna uma `Response`, o **FastAPI** vai repassá-la diretamente.

Ele não fará conversões de dados com modelos do Pydantic, não converterá o conteúdo para nenhum tipo, etc.

Isso te dá bastante flexibilidade. Você pode retornar qualquer tipo de dado, sobrescrever qualquer declaração e validação nos dados, etc.

Isso também te dá muita responsabilidade. Você precisa garantir que os dados retornados estão corretos, no formato correto, que podem ser serializados, etc.

## Utilizando o `jsonable_encoder` em uma `Response` { #using-the-jsonable-encoder-in-a-response }

Como o **FastAPI** não realiza nenhuma mudança na `Response` que você retorna, você precisa garantir que o conteúdo dela está pronto para uso.

Por exemplo, você não pode colocar um modelo do Pydantic em uma `JSONResponse` sem antes convertê-lo em um `dict` com todos os tipos de dados (como `datetime`, `UUID`, etc) convertidos para tipos compatíveis com JSON.

Para esses casos, você pode usar o `jsonable_encoder` para converter seus dados antes de repassá-los para a resposta:

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | Detalhes Técnicos

Você também pode utilizar `from starlette.responses import JSONResponse`.

**FastAPI** utiliza a mesma `starlette.responses` como `fastapi.responses` apenas como uma conveniência para você, desenvolvedor. Mas maior parte das respostas disponíveis vem diretamente do Starlette.

///

## Retornando uma `Response` personalizada { #returning-a-custom-response }

O exemplo acima mostra todas as partes que você precisa, mas ainda não é muito útil, já que você poderia ter retornado o `item` diretamente, e o **FastAPI** colocaria em uma `JSONResponse` para você, convertendo em um `dict`, etc. Tudo isso por padrão.

Agora, vamos ver como você pode usar isso para retornar uma resposta personalizada.

Vamos dizer que você quer retornar uma resposta [XML](https://en.wikipedia.org/wiki/XML).

Você pode colocar o seu conteúdo XML em uma string, colocar em uma `Response`, e retorná-lo:

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Como funciona um Modelo de resposta { #how-a-response-model-works }

Quando você declara um [Modelo de resposta - Tipo de retorno](../tutorial/response-model.md) em uma operação de rota, o **FastAPI** irá usá-lo para serializar os dados para JSON, usando o Pydantic.

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

Como isso acontece no lado do Rust, o desempenho será muito melhor do que se fosse feito com Python comum e a classe `JSONResponse`.

Ao usar um `response_model` ou tipo de retorno, o FastAPI não usará o `jsonable_encoder` para converter os dados (o que seria mais lento) nem a classe `JSONResponse`.

Em vez disso, ele pega os bytes JSON gerados com o Pydantic usando o modelo de resposta (ou tipo de retorno) e retorna uma `Response` com o media type correto para JSON diretamente (`application/json`).

## Notas { #notes }

Quando você retorna uma `Response` diretamente os dados não são validados, convertidos (serializados) ou documentados automaticamente.

Mas você ainda pode documentar como descrito em [Respostas adicionais no OpenAPI](additional-responses.md).

Você pode ver nas próximas seções como usar/declarar essas `Responses` customizadas enquanto mantém a conversão e documentação automática dos dados.
