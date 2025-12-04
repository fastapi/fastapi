# Configuração Avançada da Operação de Rota { #path-operation-advanced-configuration }

## operationId do OpenAPI { #openapi-operationid }

/// warning | Atenção

Se você não é um "especialista" no OpenAPI, você provavelmente não precisa disso.

///

Você pode definir o `operationId` do OpenAPI que será utilizado na sua *operação de rota* com o parâmetro `operation_id`.

Você precisa ter certeza que ele é único para cada operação.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001.py hl[6] *}

### Utilizando o nome da *função de operação de rota* como o operationId { #using-the-path-operation-function-name-as-the-operationid }

Se você quiser utilizar o nome das funções da sua API como `operationId`s, você pode iterar sobre todos esses nomes e sobrescrever o `operationId` em  cada *operação de rota* utilizando o `APIRoute.name` dela.

Você deve fazer isso depois de adicionar todas as suas *operações de rota*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002.py hl[2, 12:21, 24] *}

/// tip | Dica

Se você chamar `app.openapi()` manualmente, os `operationId`s devem ser atualizados antes dessa chamada.

///

/// warning | Atenção

Se você fizer isso, você tem que ter certeza de que cada uma das suas *funções de operação de rota* tem um nome único.

Mesmo que elas estejam em módulos (arquivos Python) diferentes.

///

## Excluir do OpenAPI { #exclude-from-openapi }

Para excluir uma *operação de rota* do esquema OpenAPI gerado (e por consequência, dos sistemas de documentação automáticos), utilize o parâmetro `include_in_schema` e defina ele como `False`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial003.py hl[6] *}

## Descrição avançada a partir de docstring { #advanced-description-from-docstring }

Você pode limitar as linhas utilizadas a partir de uma docstring de uma *função de operação de rota* para o OpenAPI.

Adicionar um `\f` (um caractere de escape para alimentação de formulário) faz com que o **FastAPI** restrinja a saída utilizada pelo OpenAPI até esse ponto.

Ele não será mostrado na documentação, mas outras ferramentas (como o Sphinx) serão capazes de utilizar o resto do texto.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004.py hl[19:29] *}

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

{* ../../docs_src/path_operation_advanced_configuration/tutorial005.py hl[6] *}

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

O dicionário em `openapi_extra` vai ter todos os seus níveis mesclados dentro do esquema OpenAPI gerado automaticamente para a *operação de rota*.

Então, você pode adicionar dados extras para o esquema gerado automaticamente.

Por exemplo, você poderia optar por ler e validar a requisição com seu próprio código, sem utilizar funcionalidades automatizadas do FastAPI com o Pydantic, mas você ainda pode quere definir a requisição no esquema OpenAPI.

Você pode fazer isso com `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006.py hl[19:36, 39:40] *}

Nesse exemplo, nós não declaramos nenhum modelo do Pydantic. Na verdade, o corpo da requisição não está nem mesmo <abbr title="convertido de um formato plano, como bytes, para objetos Python">analisado</abbr> como JSON, ele é lido diretamente como `bytes` e a função `magic_data_reader()` seria a responsável por analisar ele de alguma forma.

De toda forma, nós podemos declarar o esquema esperado para o corpo da requisição.

### Tipo de conteúdo do OpenAPI personalizado { #custom-openapi-content-type }

Utilizando esse mesmo truque, você pode utilizar um modelo Pydantic para definir o JSON Schema que é então incluído na seção do esquema personalizado do OpenAPI na *operação de rota*.

E você pode fazer isso até mesmo quando os dados da requisição não seguem o formato JSON.

Por exemplo, nesta aplicação nós não usamos a funcionalidade integrada ao FastAPI de extrair o JSON Schema dos modelos Pydantic nem a validação automática do JSON. Na verdade, estamos declarando o tipo do conteúdo da requisição como YAML, em vez de JSON:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[17:22, 24] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[17:22, 24] *}

////

/// info | Informação

Na versão 1 do Pydantic, o método para obter o JSON Schema de um modelo é `Item.schema()`, na versão 2 do Pydantic, o método é `Item.model_json_schema()`.

///

Entretanto, mesmo que não utilizemos a funcionalidade integrada por padrão, ainda estamos usando um modelo Pydantic para gerar um JSON Schema manualmente para os dados que queremos receber no formato YAML.

Então utilizamos a requisição diretamente, e extraímos o corpo como `bytes`. Isso significa que o FastAPI não vai sequer tentar analisar o corpo da requisição como JSON.

E então no nosso código, nós analisamos o conteúdo YAML diretamente, e estamos utilizando o mesmo modelo Pydantic para validar o conteúdo YAML:

//// tab | Pydantic v2

{* ../../docs_src/path_operation_advanced_configuration/tutorial007.py hl[26:33] *}

////

//// tab | Pydantic v1

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_pv1.py hl[26:33] *}

////

/// info | Informação

Na versão 1 do Pydantic, o método para analisar e validar um objeto era `Item.parse_obj()`, na versão 2 do Pydantic, o método é chamado de `Item.model_validate()`.

///

/// tip | Dica

Aqui reutilizamos o mesmo modelo do Pydantic.

Mas da mesma forma, nós poderíamos ter validado de alguma outra forma.

///
