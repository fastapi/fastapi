# Metadados e Urls de Documentos { #metadata-and-docs-urls }

Você pode personalizar várias configurações de metadados na sua aplicação **FastAPI**.

## Metadados para API { #metadata-for-api }

Você pode definir os seguintes campos que são usados na especificação OpenAPI e nas interfaces automáticas de documentação da API:

| Parâmetro | Tipo | Descrição |
|------------|------|-------------|
| `title` | `str` | O título da API. |
| `summary` | `str` | Um breve resumo da API. <small>Disponível desde OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | Uma breve descrição da API. Pode usar Markdown. |
| `version` | `string` | A versão da API. Esta é a versão da sua aplicação, não do OpenAPI. Por exemplo, `2.5.0`. |
| `terms_of_service` | `str` | Uma URL para os Termos de Serviço da API. Se fornecido, deve ser uma URL. |
| `contact` | `dict` | As informações de contato da API exposta. Pode conter vários campos. <details><summary>Campos de <code>contact</code></summary><table><thead><tr><th>Parâmetro</th><th>Tipo</th><th>Descrição</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>O nome identificador da pessoa/organização de contato.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>A URL que aponta para as informações de contato. DEVE estar no formato de uma URL.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>O endereço de e-mail da pessoa/organização de contato. DEVE estar no formato de um endereço de e-mail.</td></tr></tbody></table></details> |
| `license_info` | `dict` | As informações de licença para a API exposta. Ela pode conter vários campos. <details><summary>Campos de <code>license_info</code></summary><table><thead><tr><th>Parâmetro</th><th>Tipo</th><th>Descrição</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>OBRIGATÓRIO</strong> (se um <code>license_info</code> for definido). O nome da licença usada para a API.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>Uma expressão de licença <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> para a API. O campo <code>identifier</code> é mutuamente exclusivo do campo <code>url</code>. <small>Disponível desde OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>Uma URL para a licença usada para a API. DEVE estar no formato de uma URL.</td></tr></tbody></table></details> |

Você pode defini-los da seguinte maneira:

{* ../../docs_src/metadata/tutorial001.py hl[3:16,19:32] *}

/// tip | Dica

Você pode escrever Markdown no campo `description` e ele será renderizado na saída.

///

Com essa configuração, a documentação automática da API se pareceria com:

<img src="/img/tutorial/metadata/image01.png">

## Identificador de Licença { #license-identifier }

Desde o OpenAPI 3.1.0 e FastAPI 0.99.0, você também pode definir o license_info com um identifier em vez de uma url.

Por exemplo:

{* ../../docs_src/metadata/tutorial001_1.py hl[31] *}

## Metadados para tags { #metadata-for-tags }

Você também pode adicionar metadados adicionais para as diferentes tags usadas para agrupar suas operações de rota com o parâmetro `openapi_tags`.

Ele recebe uma lista contendo um dicionário para cada tag.

Cada dicionário pode conter:

* `name` (**obrigatório**): uma `str` com o mesmo nome da tag que você usa no parâmetro `tags` nas suas *operações de rota* e `APIRouter`s.
* `description`: uma `str` com uma breve descrição da tag. Pode conter Markdown e será exibido na interface de documentação.
* `externalDocs`: um `dict` descrevendo a documentação externa com:
    * `description`: uma `str` com uma breve descrição da documentação externa.
    * `url` (**obrigatório**): uma `str` com a URL da documentação externa.

### Criar Metadados para tags { #create-metadata-for-tags }

Vamos tentar isso em um exemplo com tags para `users` e `items`.

Crie metadados para suas tags e passe-os para o parâmetro `openapi_tags`:

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

Observe que você pode usar Markdown dentro das descrições. Por exemplo, "login" será exibido em negrito (**login**) e "fancy" será exibido em itálico (_fancy_).

/// tip | Dica

Você não precisa adicionar metadados para todas as tags que você usa.

///

### Use suas tags { #use-your-tags }

Use o parâmetro `tags` com suas *operações de rota* (e `APIRouter`s) para atribuí-los a diferentes tags:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info | Informação

Leia mais sobre tags em [Configuração de operação de rota](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Cheque os documentos { #check-the-docs }

Agora, se você verificar a documentação, ela exibirá todos os metadados adicionais:

<img src="/img/tutorial/metadata/image02.png">

### Ordem das tags { #order-of-tags }

A ordem de cada dicionário de metadados de tag também define a ordem exibida na interface de documentação.

Por exemplo, embora `users` apareça após `items` em ordem alfabética, ele é exibido antes deles, porque adicionamos seus metadados como o primeiro dicionário na lista.

## URL da OpenAPI { #openapi-url }

Por padrão, o esquema OpenAPI é servido em `/openapi.json`.

Mas você pode configurá-lo com o parâmetro `openapi_url`.

Por exemplo, para defini-lo para ser servido em `/api/v1/openapi.json`:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

Se você quiser desativar completamente o esquema OpenAPI, pode definir `openapi_url=None`, o que também desativará as interfaces de documentação que o utilizam.

## URLs da Documentação { #docs-urls }

Você pode configurar as duas interfaces de documentação incluídas:

* **Swagger UI**: acessível em `/docs`.
    * Você pode definir sua URL com o parâmetro `docs_url`.
    * Você pode desativá-la definindo `docs_url=None`.
* **ReDoc**: acessível em `/redoc`.
    * Você pode definir sua URL com o parâmetro `redoc_url`.
    * Você pode desativá-la definindo `redoc_url=None`.

Por exemplo, para definir o Swagger UI para ser servido em `/documentation` e desativar o ReDoc:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
