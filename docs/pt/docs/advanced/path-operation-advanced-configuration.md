# Configuração Avançada da Operação de Rota { #path-operation-advanced-configuration }

## operationId do OpenAPI { #openapi-operationid }

/// warning | Atenção

Se você não é um "especialista" no OpenAPI, você provavelmente não precisa disso.

///

Você pode definir o `operationId` do OpenAPI que será utilizado na sua *operação de rota* com o parâmetro `operation_id`.

Você (você deveria) ter certeza de que ele é único para cada operação.

{* ../../docs_src/path_operation_advanced_configuration/tutorial001_py39.py hl[6] *}

### Utilizando o nome da *função de operação de rota* como o operationId { #using-the-path-operation-function-name-as-the-operationid }

Se você quiser utilizar o nome das funções da sua API como `operationId`s, você pode iterar sobre todos esses nomes e sobrescrever o `operation_id` de cada *operação de rota* utilizando o `APIRoute.name` dela.

Você (você deveria) fazer isso depois de adicionar todas as suas *operações de rota*.

{* ../../docs_src/path_operation_advanced_configuration/tutorial002_py39.py hl[2, 12:21, 24] *}

/// tip | Dica

Se você chamar `app.openapi()` manualmente, você (você deveria) atualizar os `operationId`s antes disso.

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

Adicionar um `\f` (um caractere de escape "form feed") faz com que o **FastAPI** trunque a saída utilizada pelo OpenAPI até esse ponto.

Ele não será mostrado na documentação, mas outras ferramentas (como o Sphinx) serão capazes de utilizar o resto.

{* ../../docs_src/path_operation_advanced_configuration/tutorial004_py310.py hl[17:27] *}

## Respostas Adicionais { #additional-responses }

Você provavelmente já viu como declarar o `response_model` e `status_code` para uma *operação de rota*.

Isso define os metadados sobre a response principal da *operação de rota*.

Você também pode declarar responses adicionais, com seus modelos, códigos de status, etc.

Existe um capítulo inteiro da nossa documentação sobre isso, você pode ler em [Respostas Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.

## Extras do OpenAPI { #openapi-extra }

Quando você declara uma *operação de rota* na sua aplicação, o **FastAPI** gera automaticamente os metadados relevantes sobre essa *operação de rota* para serem incluídos no esquema do OpenAPI.

/// note | Detalhes Técnicos

Na especificação do OpenAPI, isso é chamado de <a href="https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operation-object" class="external-link" target="_blank">Objeto de Operação</a>.

///

Ele possui toda a informação sobre a *operação de rota* e é usado para gerar a documentação automaticamente.

Ele inclui os atributos `tags`, `parameters`, `requestBody`, `responses`, etc.

Esse esquema OpenAPI específico para uma *operação de rota* normalmente é gerado automaticamente pelo **FastAPI**, mas você também pode estendê-lo.

/// tip | Dica

Esse é um ponto de extensão de baixo nível.

Caso você só precise declarar responses adicionais, uma forma mais conveniente de fazer isso é com [Respostas Adicionais no OpenAPI](additional-responses.md){.internal-link target=_blank}.

///

Você pode estender o esquema do OpenAPI para uma *operação de rota* utilizando o parâmetro `openapi_extra`.

### Extensões do OpenAPI { #openapi-extensions }

Esse parâmetro `openapi_extra` pode ser útil, por exemplo, para declarar [Extensões do OpenAPI](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#specificationExtensions):

{* ../../docs_src/path_operation_advanced_configuration/tutorial005_py39.py hl[6] *}

Se você abrir os documentos criados automaticamente para a API, sua extensão aparecerá no final da *operação de rota* específica.

<img src="/img/tutorial/path-operation-advanced-configuration/image01.png">

E se você olhar o OpenAPI resultante (em `/openapi.json` na sua API), você verá que a sua extensão também faz parte da *operação de rota* específica:

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

O dicionário em `openapi_extra` será mesclado profundamente com o esquema OpenAPI gerado automaticamente para a *operação de rota*.

Assim, você poderia adicionar dados adicionais ao esquema gerado automaticamente.

Por exemplo, você poderia decidir ler e validar a request com seu próprio código, sem usar as funcionalidades automáticas do FastAPI com o Pydantic, mas ainda assim poderia querer definir a request no esquema OpenAPI.

Você pode fazer isso com `openapi_extra`:

{* ../../docs_src/path_operation_advanced_configuration/tutorial006_py39.py hl[19:36, 39:40] *}

Neste exemplo, não declaramos nenhum modelo do Pydantic. Na verdade, o corpo da request nem sequer é <abbr title="converted from some plain format, like bytes, into Python objects - convertido de algum formato simples, como bytes, para objetos Python">parsed</abbr> como JSON, ele é lido diretamente como `bytes`, e a função `magic_data_reader()` seria a responsável por fazer o parsing dele de alguma forma.

Mesmo assim, podemos declarar o esquema esperado para o corpo da request.

### Tipo de conteúdo do OpenAPI personalizado { #custom-openapi-content-type }

Utilizando esse mesmo truque, você poderia usar um modelo Pydantic para definir o JSON Schema que é então incluído na seção do esquema OpenAPI personalizado da *operação de rota*.

E você poderia fazer isso mesmo que o tipo de dados na request não seja JSON.

Por exemplo, nesta aplicação não usamos a funcionalidade integrada do FastAPI para extrair o JSON Schema dos modelos Pydantic nem a validação automática para JSON. Na verdade, estamos declarando o tipo de conteúdo da request como YAML, e não JSON:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[15:20, 22] *}

Mesmo assim, embora não estejamos usando a funcionalidade integrada padrão, ainda estamos usando um modelo Pydantic para gerar manualmente o JSON Schema para os dados que queremos receber em YAML.

Então usamos a request diretamente e extraímos o corpo como `bytes`. Isso significa que o FastAPI nem sequer vai tentar fazer o parsing do payload da request como JSON.

E então no nosso código, fazemos o parsing desse conteúdo YAML diretamente, e então estamos novamente usando o mesmo modelo Pydantic para validar o conteúdo YAML:

{* ../../docs_src/path_operation_advanced_configuration/tutorial007_py39.py hl[24:31] *}

/// tip | Dica

Aqui reutilizamos o mesmo modelo do Pydantic.

Mas da mesma forma, nós poderíamos ter validado de alguma outra forma.

///
