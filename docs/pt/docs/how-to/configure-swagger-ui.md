# Configurar Swagger UI

Você pode configurar alguns <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration" class="external-link" target="_blank">parâmetros extras da UI do Swagger</a>.

Para configurá-los, passe o argumento `swagger_ui_parameters` ao criar o objeto de aplicativo `FastAPI()` ou para a função `get_swagger_ui_html()`.

`swagger_ui_parameters` recebe um dicionário com as configurações passadas diretamente para o Swagger UI.

O FastAPI converte as configurações para **JSON** para torná-las compatíveis com JavaScript, pois é disso que o Swagger UI precisa.

## Desabilitar realce de sintaxe

Por exemplo, você pode desabilitar o destaque de sintaxe na UI do Swagger.

Sem alterar as configurações, o destaque de sintaxe é habilitado por padrão:

<img src="/img/tutorial/extending-openapi/image02.png">

Mas você pode desabilitá-lo definindo `syntaxHighlight` como `False`:

```Python hl_lines="3"
{!../../../docs_src/configure_swagger_ui/tutorial001.py!}
```

...e então o Swagger UI não mostrará mais o destaque de sintaxe:

<img src="/img/tutorial/extending-openapi/image03.png">

## Alterar o tema

Da mesma forma que você pode definir o tema de destaque de sintaxe com a chave `"syntaxHighlight.theme"` (observe que há um ponto no meio):

```Python hl_lines="3"
{!../../../docs_src/configure_swagger_ui/tutorial002.py!}
```

Essa configuração alteraria o tema de cores de destaque de sintaxe:

<img src="/img/tutorial/extending-openapi/image04.png">

## Alterar parâmetros de UI padrão do Swagger

O FastAPI inclui alguns parâmetros de configuração padrão apropriados para a maioria dos casos de uso.

Inclui estas configurações padrão:

```Python
{!../../../fastapi/openapi/docs.py[ln:7-23]!}
```

Você pode substituir qualquer um deles definindo um valor diferente no argumento `swagger_ui_parameters`.

Por exemplo, para desabilitar `deepLinking` você pode passar essas configurações para `swagger_ui_parameters`:

```Python hl_lines="3"
{!../../../docs_src/configure_swagger_ui/tutorial003.py!}
```

## Outros parâmetros da UI do Swagger

Para ver todas as outras configurações possíveis que você pode usar, leia a <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration" class="external-link" target="_blank">documentação oficial dos parâmetros da UI do Swagger</a>.

## Configurações somente JavaScript

A interface do usuário do Swagger também permite que outras configurações sejam objetos **somente JavaScript** (por exemplo, funções JavaScript).

O FastAPI também inclui estas configurações de `predefinições` somente para JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Esses são objetos **JavaScript**, não strings, então você não pode passá-los diretamente do código Python.

Se você precisar usar configurações somente JavaScript como essas, você pode usar um dos métodos acima. Sobrescreva todas as *operações de rotas* do Swagger UI e escreva manualmente qualquer JavaScript que você precisar.
