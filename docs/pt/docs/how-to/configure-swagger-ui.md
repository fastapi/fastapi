# Configure a UI do Swagger { #configure-swagger-ui }

Você pode configurar alguns <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">parâmetros extras da UI do Swagger</a>.

Para configurá-los, passe o argumento `swagger_ui_parameters` ao criar o objeto da aplicação `FastAPI()` ou para a função `get_swagger_ui_html()`.

`swagger_ui_parameters` recebe um dicionário com as configurações passadas diretamente para o Swagger UI.

O FastAPI converte as configurações para **JSON** para torná-las compatíveis com JavaScript, pois é disso que o Swagger UI precisa.

## Desabilitar destaque de sintaxe { #disable-syntax-highlighting }

Por exemplo, você pode desabilitar o destaque de sintaxe na UI do Swagger.

Sem alterar as configurações, o destaque de sintaxe é habilitado por padrão:

<img src="/img/tutorial/extending-openapi/image02.png">

Mas você pode desabilitá-lo definindo `syntaxHighlight` como `False`:

{* ../../docs_src/configure_swagger_ui/tutorial001.py hl[3] *}

...e então o Swagger UI não mostrará mais o destaque de sintaxe:

<img src="/img/tutorial/extending-openapi/image03.png">

## Alterar o tema { #change-the-theme }

Da mesma forma que você pode definir o tema de destaque de sintaxe com a chave `"syntaxHighlight.theme"` (observe que há um ponto no meio):

{* ../../docs_src/configure_swagger_ui/tutorial002.py hl[3] *}

Essa configuração alteraria o tema de cores de destaque de sintaxe:

<img src="/img/tutorial/extending-openapi/image04.png">

## Alterar parâmetros de UI padrão do Swagger { #change-default-swagger-ui-parameters }

O FastAPI inclui alguns parâmetros de configuração padrão apropriados para a maioria dos casos de uso.

Inclui estas configurações padrão:

{* ../../fastapi/openapi/docs.py ln[8:23] hl[17:23] *}

Você pode substituir qualquer um deles definindo um valor diferente no argumento `swagger_ui_parameters`.

Por exemplo, para desabilitar `deepLinking` você pode passar essas configurações para `swagger_ui_parameters`:

{* ../../docs_src/configure_swagger_ui/tutorial003.py hl[3] *}

## Outros parâmetros da UI do Swagger { #other-swagger-ui-parameters }

Para ver todas as outras configurações possíveis que você pode usar, leia a <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">documentação oficial dos parâmetros da UI do Swagger</a>.

## Configurações somente JavaScript { #javascript-only-settings }

A UI do Swagger também permite que outras configurações sejam objetos **somente JavaScript** (por exemplo, funções JavaScript).

O FastAPI também inclui estas configurações `presets` somente para JavaScript:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Esses são objetos **JavaScript**, não strings, então você não pode passá-los diretamente do código Python.

Se você precisar usar configurações somente JavaScript como essas, você pode usar um dos métodos acima. Substitua toda a *operação de rota* do Swagger UI e escreva manualmente qualquer JavaScript que você precisar.
