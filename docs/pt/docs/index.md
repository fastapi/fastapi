# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/pt"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, alta performance, fácil de aprender, fácil de codar, pronto para produção</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentação**: <a href="https://fastapi.tiangolo.com/pt" target="_blank">https://fastapi.tiangolo.com</a>

**Código fonte**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI é um moderno e rápido (alta performance) _framework web_ para construção de APIs com Python, baseado nos _type hints_ padrões do Python.

Os recursos chave são:

* **Rápido**: alta performance, equivalente a **NodeJS** e **Go** (graças ao Starlette e Pydantic). [Um dos frameworks mais rápidos disponíveis](#performance).
* **Rápido para codar**: Aumenta a velocidade para desenvolver recursos entre 200% a 300%. *
* **Poucos bugs**: Reduz cerca de 40% de erros induzidos por humanos (desenvolvedores). *
* **Intuitivo**: Grande suporte a _IDEs_. <abbr title="também conhecido como autocompletar, preenchimento automático, IntelliSense">Preenchimento automático</abbr> em todos os lugares. Menos tempo debugando.
* **Fácil**: Projetado para ser fácil de aprender e usar. Menos tempo lendo documentação.
* **Enxuto**: Minimize duplicação de código. Múltiplas funcionalidades para cada declaração de parâmetro. Menos bugs.
* **Robusto**: Tenha código pronto para produção. E com documentação interativa automática.
* **Baseado em padrões**: Baseado em (e totalmente compatível com) os padrões abertos para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (anteriormente conhecido como Swagger) e <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimativas baseadas em testes realizados com equipe interna de desenvolvimento, construindo aplicações em produção.</small>

## Patrocinadores { #sponsors }

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/pt/fastapi-people/#sponsors" class="external-link" target="_blank">Outros patrocinadores</a>

## Opiniões { #opinions }

"*[...] Estou usando **FastAPI** muito esses dias. [...] Estou na verdade planejando utilizar ele em todos os times de **serviços _Machine Learning_ na Microsoft**. Alguns deles estão sendo integrados no _core_ do produto **Windows** e alguns produtos **Office**.*"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Nós adotamos a biblioteca **FastAPI** para iniciar um servidor **REST** que pode ser consultado para obter **previsões**. [para o Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, e Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_A **Netflix** tem o prazer de anunciar o lançamento open-source do nosso framework de orquestração de **gerenciamento de crises**: **Dispatch**! [criado com **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"*Estou extremamente entusiasmado com o **FastAPI**. É tão divertido!*"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcaster</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"*Honestamente, o que você construiu parece super sólido e rebuscado. De muitas formas, eu queria que o **Hug** fosse assim - é realmente inspirador ver alguém que construiu ele.*"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>criador do<a href="https://github.com/hugapi/hug" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"*Se você está procurando aprender um **_framework_ moderno** para construir aplicações _REST_, dê uma olhada no **FastAPI** [...] É rápido, fácil de usar e fácil de aprender [...]*"

"*Nós trocamos nossas **APIs** por **FastAPI** [...] Acredito que vocês gostarão dele [...]*"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>fundadores da <a href="https://explosion.ai" target="_blank">Explosion AI</a> - criadores da <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Se alguém estiver procurando construir uma API Python para produção, eu recomendaria fortemente o **FastAPI**. Ele é **lindamente projetado**, **simples de usar** e **altamente escalável**. Ele se tornou um **componente chave** para a nossa estratégia API first de desenvolvimento e está impulsionando diversas automações e serviços, como o nosso Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, o FastAPI das interfaces de linhas de comando { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Se você estiver construindo uma aplicação <abbr title="Command Line Interface – Interface de Linha de Comando">CLI</abbr> para ser utilizada em um terminal ao invés de uma aplicação web, dê uma olhada no <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** é o irmão menor do FastAPI. E seu propósito é ser o **FastAPI das _CLIs_**. ⌨️ 🚀

## Requisitos { #requirements }

FastAPI está nos ombros de gigantes:

* <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> para as partes web.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> para a parte de dados.

## Instalação { #installation }

Crie e ative um <a href="https://fastapi.tiangolo.com/pt/virtual-environments/" class="external-link" target="_blank">ambiente virtual</a> e então instale o FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Nota**: Certifique-se de que você colocou `"fastapi[standard]"` com aspas, para garantir que funcione em todos os terminais.

## Exemplo { #example }

### Crie { #create-it }

Crie um arquivo `main.py` com:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou use <code>async def</code>...</summary>

Se seu código utiliza `async` / `await`, use `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Nota**:

Se você não sabe, verifique a seção _"Com pressa?"_ sobre <a href="https://fastapi.tiangolo.com/pt/async/#in-a-hurry" target="_blank">`async` e `await` nas docs</a>.

</details>

### Rode { #run-it }

Rode o servidor com:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Sobre o comando <code>fastapi dev main.py</code>...</summary>

O comando `fastapi dev` lê o seu arquivo `main.py`, identifica o aplicativo **FastAPI** nele, e inicia um servidor usando o <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>.

Por padrão, o `fastapi dev` iniciará com *auto-reload* habilitado para desenvolvimento local.

Você pode ler mais sobre isso na <a href="https://fastapi.tiangolo.com/pt/fastapi-cli/" target="_blank">documentação do FastAPI CLI</a>.

</details>

### Verifique { #check-it }

Abra seu navegador em <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Você verá a resposta JSON como:

```JSON
{"item_id": 5, "q": "somequery"}
```

Você acabou de criar uma API que:

* Recebe requisições HTTP nas _rotas_ `/` e `/items/{item_id}`.
* Ambas _rotas_ fazem <em>operações</em> `GET` (também conhecido como _métodos_ HTTP).
* A _rota_ `/items/{item_id}` tem um _parâmetro de rota_ `item_id` que deve ser um `int`.
* A _rota_ `/items/{item_id}` tem um _parâmetro query_ `q` `str` opcional.

### Documentação Interativa da API { #interactive-api-docs }

Agora vá para <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá a documentação automática interativa da API (fornecida por <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentação Alternativa da API { #alternative-api-docs }

E agora, vá para <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Você verá a documentação automática alternativa (fornecida por <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Evoluindo o Exemplo { #example-upgrade }

Agora modifique o arquivo `main.py` para receber um corpo para uma requisição `PUT`.

Declare o corpo utilizando tipos padrão Python, graças ao Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

O servidor `fastapi dev` deverá recarregar automaticamente.

### Evoluindo a Documentação Interativa da API { #interactive-api-docs-upgrade }

Agora vá para <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* A documentação interativa da API será automaticamente atualizada, incluindo o novo corpo:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Clique no botão "Try it out", ele permitirá que você preencha os parâmetros e interaja diretamente com a API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Então clique no botão "Execute", a interface do usuário irá se comunicar com a API, enviar os parâmetros, pegar os resultados e mostrá-los na tela:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Evoluindo a Documentação Alternativa da API { #alternative-api-docs-upgrade }

E agora, vá para <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* A documentação alternativa também irá refletir o novo parâmetro da _query_ e o corpo:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recapitulando { #recap }

Resumindo, você declara **uma vez** os tipos dos parâmetros, corpo etc. como parâmetros de função.

Você faz isso com os tipos padrão do Python moderno.

Você não terá que aprender uma nova sintaxe, métodos ou classes de uma biblioteca específica etc.

Apenas **Python** padrão.

Por exemplo, para um `int`:

```Python
item_id: int
```

ou para um modelo mais complexo, `Item`:

```Python
item: Item
```

...e com essa única declaração você tem:

* Suporte ao Editor, incluindo:
    * Completação.
    * Verificação de tipos.
* Validação de dados:
    * Erros automáticos e claros quando o dado é inválido.
    * Validação até para objetos JSON profundamente aninhados.
* <abbr title="também conhecido como: serialização, parsing, marshalling">Conversão</abbr> de dados de entrada: vindo da rede para dados e tipos Python. Consegue ler:
    * JSON.
    * Parâmetros de rota.
    * Parâmetros de _query_ .
    * _Cookies_.
    * Cabeçalhos.
    * Formulários.
    * Arquivos.
* <abbr title="também conhecido como: serialização, parsing, marshalling">Conversão</abbr> de dados de saída de tipos e dados Python para dados de rede (como JSON):
    * Converte tipos Python (`str`, `int`, `float`, `bool`, `list` etc).
    * Objetos `datetime`.
    * Objetos `UUID`.
    * Modelos de Banco de Dados.
    * ...e muito mais.
* Documentação interativa automática da API, incluindo 2 alternativas de interface de usuário:
    * Swagger UI.
    * ReDoc.

---

Voltando ao código do exemplo anterior, **FastAPI** irá:

* Validar que existe um `item_id` na rota para requisições `GET` e `PUT`.
* Validar que `item_id` é do tipo `int` para requisições `GET` e `PUT`.
    * Se não é validado, o cliente verá um útil, claro erro.
* Verificar se existe um parâmetro de _query_ opcional nomeado como `q` (como em `http://127.0.0.1:8000/items/foo?q=somequery`) para requisições `GET`.
    * Como o parâmetro `q` é declarado com `= None`, ele é opcional.
    * Sem o `None` ele poderia ser obrigatório (como o corpo no caso de `PUT`).
* Para requisições `PUT` para `/items/{item_id}`, lerá o corpo como JSON:
    * Verifica que tem um atributo obrigatório `name` que deve ser `str`.
    * Verifica que tem um atributo obrigatório `price` que deve ser `float`.
    * Verifica que tem an atributo opcional `is_offer`, que deve ser `bool`, se presente.
    * Tudo isso também funciona para objetos JSON profundamente aninhados.
* Converter de e para JSON automaticamente.
* Documentar tudo com OpenAPI, que poderá ser usado por:
    * Sistemas de documentação interativos.
    * Sistemas de clientes de geração de código automáticos, para muitas linguagens.
* Fornecer diretamente 2 interfaces _web_ de documentação interativa.

---

Nós apenas arranhamos a superfície, mas você já tem idéia de como tudo funciona.

Experimente mudar a seguinte linha:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...de:

```Python
        ... "item_name": item.name ...
```

...para:

```Python
        ... "item_price": item.price ...
```

...e veja como seu editor irá auto-completar os atributos e saberá os tipos:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Para um exemplo mais completo incluindo mais recursos, veja <a href="https://fastapi.tiangolo.com/pt/tutorial/">Tutorial - Guia do Usuário</a>.

**Alerta de Spoiler**: o tutorial - guia do usuário inclui:

* Declaração de **parâmetetros** de diferentes lugares como: **cabeçalhos**, **cookies**, **campos de formulários** e **arquivos**.
* Como configurar **Limitações de Validação** como `maximum_length` ou `regex`.
* Um poderoso e fácil de usar sistema de **<abbr title="também conhecido como componentes, recursos, fornecedores, serviços, injetáveis">Injeção de Dependência</abbr>**.
* Segurança e autenticação, incluindo suporte para **OAuth2** com autenticação **JWT tokens** e **HTTP Basic**.
* Técnicas mais avançadas (mas igualmente fáceis) para declaração de **modelos JSON profundamente aninhados** (graças ao Pydantic).
* Integrações **GraphQL** com o <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> e outras bibliotecas.
* Muitos recursos extras (graças ao Starlette) como:
    * **WebSockets**
    * testes extrememamente fáceis baseados em HTTPX e `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...e mais.

## Performance { #performance }

Testes de performance da _Independent TechEmpower_ mostram aplicações **FastAPI** rodando sob Uvicorn como <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">um dos _frameworks_ Python mais rápidos disponíveis</a>, somente atrás de Starlette e Uvicorn (utilizados internamente pelo FastAPI). (*)

Para entender mais sobre performance, veja a seção <a href="https://fastapi.tiangolo.com/pt/benchmarks/" class="internal-link" target="_blank">Comparações</a>.

## Dependências { #dependencies }

O FastAPI depende do Pydantic e do Starlette.

### Dependências `standard` { #standard-dependencies }

Quando você instala o FastAPI com `pip install "fastapi[standard]"`, ele vêm com o grupo `standard` (padrão) de dependências opcionais:

Utilizado pelo Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - para validação de email.

Utilizado pelo Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Obrigatório caso você queira utilizar o `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Obrigatório se você quer utilizar a configuração padrão de templates.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Obrigatório se você deseja suporte a <abbr title="convertendo a string que vem de uma requisição HTTP em dados Python">"parsing"</abbr> de formulário, com `request.form()`.

Utilizado pelo FastAPI:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - para o servidor que carrega e serve a sua aplicação. Isto inclui `uvicorn[standard]`, que inclui algumas dependências (e.g. `uvloop`) necessárias para servir em alta performance.
* `fastapi-cli[standard]` - que disponibiliza o comando `fastapi`.
    * Isso inclui `fastapi-cloud-cli`, que permite implantar sua aplicação FastAPI na <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>.

### Sem as dependências `standard` { #without-standard-dependencies }

Se você não deseja incluir as dependências opcionais `standard`, você pode instalar utilizando `pip install fastapi` ao invés de `pip install "fastapi[standard]"`.

### Sem o `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Se você quiser instalar o FastAPI com as dependências padrão, mas sem o `fastapi-cloud-cli`, você pode instalar com `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Dependências opcionais adicionais { #additional-optional-dependencies }

Existem algumas dependências adicionais que você pode querer instalar.

Dependências opcionais adicionais do Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - para gerenciamento de configurações.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - tipos extras para serem utilizados com o Pydantic.

Dependências opcionais adicionais do FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Obrigatório se você deseja utilizar o `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Obrigatório se você deseja utilizar o `UJSONResponse`.

## Licença { #license }

Esse projeto é licenciado sob os termos da licença MIT.
