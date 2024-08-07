# Utilizando o Request diretamente

Até agora você declarou as partes da requisição que você precisa utilizando os seus tipos.

Obtendo dados de:

* Os parâmetros das rotas.
* Cabeçalhos (*Headers*).
* Cookies.
* etc.

E ao fazer isso, o **FastAPI** está validando as informações, convertendo-as e gerando documentação para a sua API automaticamente.

Porém há situações em que você possa precisar acessar o objeto `Request` diretamente.

## Detalhes sobre o objeto `Request`

Como o **FastAPI** é na verdade o **Starlette** por baixo, com camadas de diversas funcionalidades por cima, você pode utilizar o objeto <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">`Request`</a> do Starlette diretamente quando precisar.

Isso significaria também que se você obtiver informações do objeto `Request` diretamente (ler o corpo da requisição por exemplo), as informações não serão validadas, convertidas ou documentadas (com o OpenAPI, para a interface de usuário automática da API) pelo FastAPI.

Embora qualquer outro parâmetro declarado normalmente (o corpo da requisição com um modelo Pydantic, por exemplo) ainda seria validado, convertido, anotado, etc.

Mas há situações específicas onde é útil utilizar o objeto `Request`.

## Utilize o objeto `Request` diretamente

Vamos imaginar que você deseja obter o endereço de IP/host do cliente dentro da sua *função de operação de rota*.

Para isso você precisa acessar a requisição diretamente.

```Python hl_lines="1  7-8"
{!../../../docs_src/using_request_directly/tutorial001.py!}
```

Ao declarar o parâmetro com o tipo sendo um `Request` em sua *função de operação de rota*, o **FastAPI** saberá como passar o `Request` neste parâmetro.

/// tip | "Dica"

Note que neste caso, nós estamos declarando o parâmetro da rota ao lado do parâmetro da requisição.

Assim, o parâmetro da rota será extraído, validado, convertido para o tipo especificado e anotado com OpenAPI.

Do mesmo jeito, você pode declarar qualquer outro parâmetro normalmente, e além disso, obter o `Request` também.

///

## Documentação do `Request`

Você pode ler mais sobre os detalhes do objeto <a href="https://www.starlette.io/requests/" class="external-link" target="_blank">`Request` no site da documentação oficial do Starlette.</a>.

/// note | "Detalhes Técnicos"

Você também pode utilizar `from starlette.requests import Request`.

O **FastAPI** fornece isso diretamente apenas como uma conveniência para você, o desenvolvedor. Mas ele vem diretamente do Starlette.

///
