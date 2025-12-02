# Configuração da Operação de Rota { #path-operation-configuration }

Existem vários parâmetros que você pode passar para o seu *decorador de operação de rota* para configurá-lo.

/// warning | Atenção

Observe que esses parâmetros são passados diretamente para o *decorador de operação de rota*, não para a sua *função de operação de rota*.

///

## Código de Status da Resposta { #response-status-code }

Você pode definir o `status_code` (HTTP) para ser usado na resposta da sua *operação de rota*.

Você pode passar diretamente o código `int`, como `404`.

Mas se você não se lembrar o que cada código numérico significa, pode usar as constantes de atalho em `status`:

{* ../../docs_src/path_operation_configuration/tutorial001_py310.py hl[1,15] *}

Esse código de status será usado na resposta e será adicionado ao esquema OpenAPI.

/// note | Detalhes Técnicos

Você também poderia usar `from starlette import status`.

**FastAPI** fornece o mesmo `starlette.status` como `fastapi.status` apenas como uma conveniência para você, o desenvolvedor. Mas vem diretamente do Starlette.

///

## Tags { #tags }

Você pode adicionar tags para sua *operação de rota*, passe o parâmetro `tags` com uma `list` de `str` (comumente apenas um `str`):

{* ../../docs_src/path_operation_configuration/tutorial002_py310.py hl[15,20,25] *}

Eles serão adicionados ao esquema OpenAPI e usados pelas interfaces de documentação automática:

<img src="/img/tutorial/path-operation-configuration/image01.png">

### Tags com Enums { #tags-with-enums }

Se você tem uma grande aplicação, você pode acabar acumulando **várias tags**, e você gostaria de ter certeza de que você sempre usa a **mesma tag** para *operações de rota* relacionadas.

Nestes casos, pode fazer sentido armazenar as tags em um `Enum`.

**FastAPI** suporta isso da mesma maneira que com strings simples:

{* ../../docs_src/path_operation_configuration/tutorial002b.py hl[1,8:10,13,18] *}

## Resumo e descrição { #summary-and-description }

Você pode adicionar um `summary` e uma `description`:

{* ../../docs_src/path_operation_configuration/tutorial003_py310.py hl[18:19] *}

## Descrição do docstring { #description-from-docstring }

Como as descrições tendem a ser longas e cobrir várias linhas, você pode declarar a descrição da *operação de rota* na <abbr title="uma string de várias linhas como a primeira expressão dentro de uma função (não atribuída a nenhuma variável) usada para documentação">docstring</abbr> da função e o **FastAPI** irá lê-la de lá.

Você pode escrever <a href="https://en.wikipedia.org/wiki/Markdown" class="external-link" target="_blank">Markdown</a> na docstring, ele será interpretado e exibido corretamente (levando em conta a indentação da docstring).

{* ../../docs_src/path_operation_configuration/tutorial004_py310.py hl[17:25] *}

Ela será usada nas documentações interativas:

<img src="/img/tutorial/path-operation-configuration/image02.png">

## Descrição da resposta { #response-description }

Você pode especificar a descrição da resposta com o parâmetro `response_description`:

{* ../../docs_src/path_operation_configuration/tutorial005_py310.py hl[19] *}

/// info | Informação

Note que `response_description` se refere especificamente à resposta, a `description` se refere à *operação de rota* em geral.

///

/// check | Verifique

OpenAPI especifica que cada *operação de rota* requer uma descrição de resposta.

Então, se você não fornecer uma, o **FastAPI** irá gerar automaticamente uma de "Resposta bem-sucedida".

///

<img src="/img/tutorial/path-operation-configuration/image03.png">

## Descontinuar uma *operação de rota* { #deprecate-a-path-operation }

Se você precisar marcar uma *operação de rota* como <abbr title="obsoleta, recomendada não usá-la">descontinuada</abbr>, mas sem removê-la, passe o parâmetro `deprecated`:

{* ../../docs_src/path_operation_configuration/tutorial006.py hl[16] *}

Ela será claramente marcada como descontinuada nas documentações interativas:

<img src="/img/tutorial/path-operation-configuration/image04.png">

Verifique como *operações de rota* descontinuadas e não descontinuadas se parecem:

<img src="/img/tutorial/path-operation-configuration/image05.png">

## Resumindo { #recap }

Você pode configurar e adicionar metadados para suas *operações de rota* facilmente passando parâmetros para os *decoradores de operação de rota*.
