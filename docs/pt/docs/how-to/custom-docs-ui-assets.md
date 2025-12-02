# Recursos Estáticos Personalizados para a UI de Documentação (Hospedagem Própria) { #custom-docs-ui-static-assets-self-hosting }

A documentação da API usa **Swagger UI** e **ReDoc**, e cada um deles precisa de alguns arquivos JavaScript e CSS.

Por padrão, esses arquivos são fornecidos por um <abbr title="Content Delivery Network – Rede de Entrega de Conteúdo: Um serviço, normalmente composto por vários servidores, que fornece arquivos estáticos, como JavaScript e CSS. É comumente usado para providenciar esses arquivos do servidor mais próximo do cliente, melhorando o desempenho.">CDN</abbr>.

Mas é possível personalizá-los, você pode definir um CDN específico ou providenciar os arquivos você mesmo.

## CDN Personalizado para JavaScript e CSS { #custom-cdn-for-javascript-and-css }

Vamos supor que você deseja usar um <abbr title="Content Delivery Network – Rede de Entrega de Conteúdo">CDN</abbr> diferente, por exemplo, você deseja usar `https://unpkg.com/`.

Isso pode ser útil se, por exemplo, você mora em um país que restringe algumas URLs.

### Desativar a documentação automática { #disable-the-automatic-docs }

O primeiro passo é desativar a documentação automática, pois por padrão, ela usa o CDN padrão.

Para desativá-los, defina suas URLs como `None` ao criar sua aplicação FastAPI:

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[8] *}

### Incluir a documentação personalizada { #include-the-custom-docs }

Agora você pode criar as *operações de rota* para a documentação personalizada.

Você pode reutilizar as funções internas do FastAPI para criar as páginas HTML para a documentação e passar os argumentos necessários:

* `openapi_url`: a URL onde a página HTML para a documentação pode obter o esquema OpenAPI para a sua API. Você pode usar aqui o atributo `app.openapi_url`.
* `title`: o título da sua API.
* `oauth2_redirect_url`: você pode usar `app.swagger_ui_oauth2_redirect_url` aqui para usar o padrão.
* `swagger_js_url`: a URL onde a página HTML para a sua documentação do Swagger UI pode obter o arquivo **JavaScript**. Este é o URL do CDN personalizado.
* `swagger_css_url`: a URL onde a página HTML para a sua documentação do Swagger UI pode obter o arquivo **CSS**. Este é o URL do CDN personalizado.

E de forma semelhante para o ReDoc...

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[2:6,11:19,22:24,27:33] *}

/// tip | Dica

A *operação de rota* para `swagger_ui_redirect` é um auxiliar para quando você usa OAuth2.

Se você integrar sua API com um provedor OAuth2, você poderá autenticar e voltar para a documentação da API com as credenciais adquiridas. E interagir com ela usando a autenticação OAuth2 real.

Swagger UI lidará com isso nos bastidores para você, mas ele precisa desse auxiliar de "redirecionamento".

///

### Criar uma *operação de rota* para testar { #create-a-path-operation-to-test-it }

Agora, para poder testar se tudo funciona, crie uma *operação de rota*:

{* ../../docs_src/custom_docs_ui/tutorial001.py hl[36:38] *}

### Teste { #test-it }

Agora, você deve ser capaz de ir para a documentação em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, e recarregar a página, ela carregará esses recursos do novo CDN.

## Hospedagem Própria de JavaScript e CSS para a documentação { #self-hosting-javascript-and-css-for-docs }

Hospedar o JavaScript e o CSS pode ser útil se, por exemplo, você precisa que seu aplicativo continue funcionando mesmo offline, sem acesso aberto à Internet, ou em uma rede local.

Aqui você verá como providenciar esses arquivos você mesmo, na mesma aplicação FastAPI, e configurar a documentação para usá-los.

### Estrutura de Arquivos do Projeto { #project-file-structure }

Vamos supor que a estrutura de arquivos do seu projeto se pareça com isso:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Agora crie um diretório para armazenar esses arquivos estáticos.

Sua nova estrutura de arquivos poderia se parecer com isso:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Baixe os arquivos { #download-the-files }

Baixe os arquivos estáticos necessários para a documentação e coloque-os no diretório `static/`.

Você provavelmente pode clicar com o botão direito em cada link e selecionar uma opção semelhante a `Salvar link como...`.

**Swagger UI** usa os arquivos:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

E o **ReDoc** usa o arquivo:

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

Depois disso, sua estrutura de arquivos deve se parecer com:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Prover os arquivos estáticos { #serve-the-static-files }

* Importe `StaticFiles`.
* "Monte" a instância `StaticFiles()` em um caminho específico.

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[7,11] *}

### Teste os arquivos estáticos { #test-the-static-files }

Inicialize seu aplicativo e vá para <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>.

Você deverá ver um arquivo JavaScript muito longo para o **ReDoc**.

Esse arquivo pode começar com algo como:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

Isso confirma que você está conseguindo fornecer arquivos estáticos do seu aplicativo e que você colocou os arquivos estáticos para a documentação no local correto.

Agora, podemos configurar o aplicativo para usar esses arquivos estáticos para a documentação.

### Desativar a documentação automática para arquivos estáticos { #disable-the-automatic-docs-for-static-files }

Da mesma forma que ao usar um CDN personalizado, o primeiro passo é desativar a documentação automática, pois ela usa o CDN padrão.

Para desativá-los, defina suas URLs como `None` ao criar sua aplicação FastAPI:

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[9] *}

### Incluir a documentação personalizada para arquivos estáticos { #include-the-custom-docs-for-static-files }

E da mesma forma que com um CDN personalizado, agora você pode criar as *operações de rota* para a documentação personalizada.

Novamente, você pode reutilizar as funções internas do FastAPI para criar as páginas HTML para a documentação e passar os argumentos necessários:

* `openapi_url`: a URL onde a página HTML para a documentação pode obter o esquema OpenAPI para a sua API. Você pode usar aqui o atributo `app.openapi_url`.
* `title`: o título da sua API.
* `oauth2_redirect_url`: Você pode usar `app.swagger_ui_oauth2_redirect_url` aqui para usar o padrão.
* `swagger_js_url`: a URL onde a página HTML para a sua documentação do Swagger UI pode obter o arquivo **JavaScript**. **Este é o URL que seu aplicativo está fornecendo**.
* `swagger_css_url`: a URL onde a página HTML para a sua documentação do Swagger UI pode obter o arquivo **CSS**. **Esse é o que seu aplicativo está fornecendo**.

E de forma semelhante para o ReDoc...

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[2:6,14:22,25:27,30:36] *}

/// tip | Dica

A *operação de rota* para `swagger_ui_redirect` é um auxiliar para quando você usa OAuth2.

Se você integrar sua API com um provedor OAuth2, você poderá autenticar e voltar para a documentação da API com as credenciais adquiridas. E, então, interagir com ela usando a autenticação OAuth2 real.

Swagger UI lidará com isso nos bastidores para você, mas ele precisa desse auxiliar de "redirect".

///

### Criar uma *operação de rota* para testar arquivos estáticos { #create-a-path-operation-to-test-static-files }

Agora, para poder testar se tudo funciona, crie uma *operação de rota*:

{* ../../docs_src/custom_docs_ui/tutorial002.py hl[39:41] *}

### Teste a UI de Arquivos Estáticos { #test-static-files-ui }

Agora, você deve ser capaz de desconectar o WiFi, ir para a documentação em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, e recarregar a página.

E mesmo sem Internet, você será capaz de ver a documentação da sua API e interagir com ela.
