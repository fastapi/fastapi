# Código de Status da Resposta

Do mesmo modo que você pode especificar um modelo de resposta, você também pode definir o código de status HTTP utilizado para a resposta com o parâmetro `status_code` em qualquer uma das *operações de caminho*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

!!! observação
    Note que `status_code` é um parâmetro do método "decorador" (`get`, `post`, etc). Não da sua *função de operação de caminho*, como todos os parâmetros e corpo.

O parâmetro `status_code` recebe um número com o código de status HTTP.

!!! informação
    O `status_code` alternativamente, também pode receber um `IntEnum`, assim como em Python <a href="https://docs.python.org/3/library/http.html#http.HTTPStatus" class="external-link" target="_blank">`http.HTTPStatus`</a>.

Assim:

* Esse código de status será retornado na resposta.
* Será documentado como no esquema da OpenAPI (e, portanto, nas interfaces do usuário):

<img src="/img/tutorial/response-status-code/image01.png">

!!! observação
    Alguns códigos de status (ver na próxima seção) indicam que a resposta não possui um corpo.

    FastAPI sabe disso, e irá produzir documentação OpenAPI que afirma que não há corpo de resposta.

## Sobre códigos de status HTTP

!!! observação
    Se você já sabe o que são códigos de status HTTP, pule para a próxima seção.

Em HTTP, você envia um código de status numérico de 3 dígitos como parte da resposta.

Esses códigos de status têm um nome associado para reconhecê-los, mas o importante é o número.

Resumidamente:

* `100` e acima são para "Informações". Você raramente os usa diretamente. As respostas com esses códigos de status não podem ter um corpo.
* **`200`** e acima são para respostas "Bem-sucedidas". Estes são os que você mais usaria.
    * `200` é o código de status padrão, o que significa que tudo estava "OK".
    * Outro exemplo seria `201`, "Criado". É comumente usado após a criação de um novo registro no banco de dados.
    * Um caso especial é `204`, "Sem conteúdo". Essa resposta é usada quando não há conteúdo para retornar ao cliente e, portanto, a resposta não deve ter um corpo.
* **`300`** e acima são para "Redirecionamento". As respostas com esses códigos de status podem ou não ter um corpo, exceto `304`, "Não modificado", que não deve ter um.
* **`400`** e acima são para respostas "Erro do cliente". Este é o segundo tipo que você provavelmente mais usaria.
    * Um exemplo é `404`, para uma resposta "Não encontrado".
    * Para erros genéricos do cliente, você pode usar apenas `400`.
* `500` e acima são para erros do servidor. Você quase nunca os usa diretamente. Quando algo der errado em alguma parte do código do seu aplicativo ou servidor, ele retornará automaticamente um desses códigos de status.

!!! Dica
    Para saber mais sobre cada código de status e qual código serve para quê, verifique o <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> documentação sobre códigos de status HTTP</a>.

## Atalho para lembrar os nomes

Vamos ver o exemplo anterior novamente:

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

`201` é o código de status para "Criado".

Mas você não precisa memorizar o que cada um desses códigos significa.

Você pode usar as variáveis de conveniência de `fastapi.status`.

```Python hl_lines="1  6"
{!../../../docs_src/response_status_code/tutorial002.py!}
```

Eles são apenas uma conveniência, eles possuem o mesmo número, mas dessa forma você pode usar o autocomplete do editor para encontrá-los:

<img src="/img/tutorial/response-status-code/image02.png">

!!! observação "Detalhes Técnicos"
    Você também pode usar `from starlette import status`.

    **FastAPI** fornece o mesmo `starlette.status` que `fastapi.status` apenas para conveniência para você, o desenvolvedor. Mas vem diretamente da Starlette.

## Alterando o padrão

Mais tarde, no [Guia do Usuário Avançado](../advanced/response-change-status-code.md){.internal-link target=_blank}, você verá como retornar um código de status diferente do padrão que você está declarando aqui.
