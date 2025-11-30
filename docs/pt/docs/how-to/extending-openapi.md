# Extendendo o OpenAPI { #extending-openapi }

Existem alguns casos em que pode ser necessário modificar o esquema OpenAPI gerado.

Nesta seção, você verá como fazer isso.

## O processo normal { #the-normal-process }

O processo normal (padrão) é o seguinte:

Uma aplicação (instância) do `FastAPI` possui um método `.openapi()` que deve retornar o esquema OpenAPI.

Como parte da criação do objeto de aplicação, uma *operação de rota* para `/openapi.json` (ou para o que você definir como `openapi_url`) é registrada.

Ela apenas retorna uma resposta JSON com o resultado do método `.openapi()` da aplicação.

Por padrão, o que o método `.openapi()` faz é verificar se a propriedade `.openapi_schema` tem conteúdo e retorná-lo.

Se não tiver, ele gera o conteúdo usando a função utilitária em `fastapi.openapi.utils.get_openapi`.

E essa função `get_openapi()` recebe como parâmetros:

* `title`: O título do OpenAPI, exibido na documentação.
* `version`: A versão da sua API, por exemplo, `2.5.0`.
* `openapi_version`: A versão da especificação OpenAPI utilizada. Por padrão, a mais recente: `3.1.0`.
* `summary`: Um resumo curto da API.
* `description`: A descrição da sua API, que pode incluir markdown e será exibida na documentação.
* `routes`: Uma lista de rotas, que são cada uma das *operações de rota* registradas. Elas são obtidas de `app.routes`.

/// info | Informação

O parâmetro `summary` está disponível no OpenAPI 3.1.0 e superior, suportado pelo FastAPI 0.99.0 e superior.

///

## Sobrescrevendo os padrões { #overriding-the-defaults }

Com as informações acima, você pode usar a mesma função utilitária para gerar o esquema OpenAPI e sobrescrever cada parte que precisar.

Por exemplo, vamos adicionar <a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">Extensão OpenAPI do ReDoc para incluir um logo personalizado</a>.

### **FastAPI** Normal { #normal-fastapi }

Primeiro, escreva toda a sua aplicação **FastAPI** normalmente:

{* ../../docs_src/extending_openapi/tutorial001.py hl[1,4,7:9] *}

### Gerar o esquema OpenAPI { #generate-the-openapi-schema }

Em seguida, use a mesma função utilitária para gerar o esquema OpenAPI, dentro de uma função `custom_openapi()`:

{* ../../docs_src/extending_openapi/tutorial001.py hl[2,15:21] *}

### Modificar o esquema OpenAPI { #modify-the-openapi-schema }

Agora, você pode adicionar a extensão do ReDoc, incluindo um `x-logo` personalizado ao "objeto" `info` no esquema OpenAPI:

{* ../../docs_src/extending_openapi/tutorial001.py hl[22:24] *}

### Armazenar em cache o esquema OpenAPI { #cache-the-openapi-schema }

Você pode usar a propriedade `.openapi_schema` como um "cache" para armazenar o esquema gerado.

Dessa forma, sua aplicação não precisará gerar o esquema toda vez que um usuário abrir a documentação da sua API.

Ele será gerado apenas uma vez, e o mesmo esquema armazenado em cache será utilizado nas próximas requisições.

{* ../../docs_src/extending_openapi/tutorial001.py hl[13:14,25:26] *}

### Sobrescrever o método { #override-the-method }

Agora, você pode substituir o método `.openapi()` pela sua nova função.

{* ../../docs_src/extending_openapi/tutorial001.py hl[29] *}

### Verificar { #check-it }

Uma vez que você acessar <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>, verá que está usando seu logo personalizado (neste exemplo, o logo do **FastAPI**):

<img src="/img/tutorial/extending-openapi/image01.png">
