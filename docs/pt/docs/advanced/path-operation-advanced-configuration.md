# Configuração Avançada da Operação de Rota { #path-operation-advanced-configuration }

## operationId do OpenAPI { #openapi-operationid }

/// warning | Atenção

Se você não é um "especialista" no OpenAPI, você provavelmente não precisa disso.

///

Você pode definir o `operationId` do OpenAPI que será utilizado na sua *operação de rota* com o parâmetro `operation_id`.

Você deveria ter certeza que ele é único para cada operação.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### Utilizando o nome da *função de operação de rota* como o operationId { #using-the-path-operation-function-name-as-the-operationid }

Se você quiser utilizar o nome das funções da sua API como `operationId`s, você pode iterar sobre todos esses nomes e sobrescrever o `operation_id` em  cada *operação de rota* utilizando o `APIRoute.name` dela.

Você deveria fazer isso depois de adicionar todas as suas *operações de rota*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | Dica

Se você chamar `app.openapi()` manualmente, você deveria atualizar os `operationId`s antes dessa chamada.

///

/// warning | Atenção

Se você fizer isso, você tem que ter certeza de que cada uma das suas *funções de operação de rota* tem um nome único.

Mesmo que elas estejam em módulos (arquivos Python) diferentes.

///

## Excluir do OpenAPI { #exclude-from-openapi }

Para excluir uma *operação de rota* do esquema OpenAPI gerado (e por consequência, dos sistemas de documentação automáticos), utilize o parâmetro `include_in_schema` e defina ele como `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003_py39.py hl[6] *}

## Descrição avançada a partir de docstring { #advanced-description-from-docstring }

Você pode limitar as linhas utilizadas a partir da docstring de uma *função de operação de rota* para o OpenAPI.

Adicionar um `\f` (um caractere de escape para "form feed") faz com que o **FastAPI** trunque a saída usada para o OpenAPI até esse ponto.

Ele não será mostrado na documentação, mas outras ferramentas (como o Sphinx) serão capazes de utilizar o resto.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Respostas Adicionais { #additional-responses }

Você provavelmente já viu como declarar o `response_model` e `status_code` para uma *operação de rota*.

Isso define os metadados sobre a resposta principal da *operação de rota*.

Você também pode declarar respostas adicionais, com seus modelos, códigos de status, etc.

Existe um capítulo inteiro da nossa documentação sobre isso, você pode ler em [Retornos Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.

## Extras do OpenAPI { #openapi-extra }

Quando você declara uma *operação de rota* na sua aplicação, o **FastAPI** irá gerar os metadados relevantes da *operação de rota* automaticamente para serem incluídos no esquema do OpenAPI.

/// note | Detalhes Técnicos

Na especificação do OpenAPI, isso é chamado de um <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Objeto de Operação</a>.

///

Ele possui toda a informação sobre a *operação de rota* e é usado para gerar a documentação automaticamente.

Ele inclui os atributos `tags`, `parameters`, `requestBody`, `responses`, etc.

Esse esquema específico para uma *operação de rota* normalmente é gerado automaticamente pelo **FastAPI**, mas você também pode estender ele.

/// tip | Dica

Esse é um ponto de extensão de baixo nível.

Caso você só precise declarar respostas adicionais, uma forma conveniente de fazer isso é com [Retornos Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Você pode estender o esquema do OpenAPI para uma *operação de rota* utilizando o parâmetro `openapi_extra`.

### Extensões do OpenAPI { #openapi-extensions }

Esse parâmetro `openapi_extra` pode ser útil, por exemplo, para declarar [Extensões do OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

Se você abrir os documentos criados automaticamente para a API, sua extensão aparecerá no final da *operação de rota* específica.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

E se você olhar o esquema OpenAPI resultante (na rota `/openapi.json` da sua API), você verá que a sua extensão também faz parte da *operação de rota* específica:

```JSON hl_lines="22"
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "x-aperture-labs-portal": "blue"
            }
        }
    }
}
```

### Esquema de *operação de rota* do OpenAPI personalizado { #custom-openapi-path-operation-schema }

O dicionário em `openapi_extra` vai ser mesclado profundamente com o esquema OpenAPI gerado automaticamente para a *operação de rota*.

Então, você pode adicionar dados extras ao esquema gerado automaticamente.

Por exemplo, você poderia decidir ler e validar a requisição com seu próprio código, sem usar as funcionalidades automáticas do FastAPI com o Pydantic, mas ainda assim querer definir a requisição no esquema OpenAPI.

Você pode fazer isso com `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

Nesse exemplo, nós não declaramos nenhum modelo do Pydantic. Na verdade, o corpo da requisição não está nem mesmo <abbr title="converted from some plain format, like bytes, into Python objects - convertido de algum formato simples, como bytes, em objetos Python">analisado</abbr> como JSON, ele é lido diretamente como `bytes`, e a função `magic_data_reader()` seria a responsável por analisar ele de alguma forma.

De toda forma, nós podemos declarar o esquema esperado para o corpo da requisição.

### Tipo de conteúdo do OpenAPI personalizado { #custom-openapi-content-type }

Utilizando esse mesmo truque, você pode usar um modelo Pydantic para definir o JSON Schema que é então incluído na seção do esquema personalizado do OpenAPI na *operação de rota*.

E você pode fazer isso até mesmo quando o tipo de dados na requisição não é JSON.

Por exemplo, nesta aplicação nós não usamos a funcionalidade integrada ao FastAPI de extrair o JSON Schema dos modelos Pydantic nem a validação automática para JSON. Na verdade, estamos declarando o tipo de conteúdo da requisição como YAML, em vez de JSON:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

Entretanto, mesmo que não utilizemos a funcionalidade integrada por padrão, ainda estamos usando um modelo Pydantic para gerar um JSON Schema manualmente para os dados que queremos receber em YAML.

Então utilizamos a requisição diretamente e extraímos o corpo como `bytes`. Isso significa que o FastAPI não vai sequer tentar analisar o payload da requisição como JSON.

E então no nosso código, nós analisamos o conteúdo YAML diretamente e, em seguida, estamos usando novamente o mesmo modelo Pydantic para validar o conteúdo YAML:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | Dica

Aqui reutilizamos o mesmo modelo do Pydantic.

Mas da mesma forma, nós poderíamos ter validado de alguma outra forma.

///
