# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/pt"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, alta performance, fácil de aprender, rápido para codar, pronto para produção</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentação**: [https://fastapi.tiangolo.com/pt](https://fastapi.tiangolo.com/pt)

**Código fonte**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI é um framework web moderno e rápido (alta performance) para construção de APIs com Python, baseado nos type hints padrões do Python.

Os recursos chave são:

* **Rápido**: alta performance, equivalente a **NodeJS** e **Go** (graças ao Starlette e Pydantic). [Um dos frameworks Python mais rápidos disponíveis](#performance).
* **Rápido para codar**: Aumenta a velocidade para desenvolver recursos entre 200% a 300%. *
* **Poucos bugs**: Reduz cerca de 40% de erros induzidos por humanos (desenvolvedores). *
* **Intuitivo**: Grande suporte a editores. <dfn title="também conhecido como: autocompletar, preenchimento automático, IntelliSense">Completação</dfn> em todos os lugares. Menos tempo debugando.
* **Fácil**: Projetado para ser fácil de aprender e usar. Menos tempo lendo docs.
* **Enxuto**: Minimize duplicação de código. Múltiplas funcionalidades para cada declaração de parâmetro. Menos bugs.
* **Robusto**: Tenha código pronto para produção. E com documentação interativa automática.
* **Baseado em padrões**: Baseado em (e totalmente compatível com) os padrões abertos para APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (anteriormente conhecido como Swagger) e [JSON Schema](https://json-schema.org/).

<small>* estimativas baseadas em testes realizados com equipe interna de desenvolvimento, construindo aplicações em produção.</small>

## Patrocinadores { #sponsors }

<!-- sponsors -->

### Patrocinador Keystone { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Patrocinadores Ouro e Prata { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

[Outros patrocinadores](https://fastapi.tiangolo.com/pt/fastapi-people/#sponsors)

## Opiniões { #opinions }

"_[...] Estou usando **FastAPI** muito esses dias. [...] Estou na verdade planejando utilizar ele em todos os times de **serviços ML na Microsoft**. Alguns deles estão sendo integrados no _core_ do produto **Windows** e alguns produtos **Office**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_Nós adotamos a biblioteca **FastAPI** para iniciar um servidor **REST** que pode ser consultado para obter **previsões**. [para o Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, e Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_A **Netflix** tem o prazer de anunciar o lançamento open-source do nosso framework de orquestração de **gerenciamento de crises**: **Dispatch**! [criado com **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_Estou muito entusiasmado com o **FastAPI**. É tão divertido!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong>[Python Bytes](https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855) apresentador do podcast</strong> <a href="https://x.com/brianokken/status/1112220079972728832"><small>(ref)</small></a></div>

---

"_Honestamente, o que você construiu parece super sólido e refinado. De muitas formas, é o que eu queria que o **Hug** fosse - é realmente inspirador ver alguém construir isso._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong>criador do [Hug](https://github.com/hugapi/hug)</strong> <a href="https://news.ycombinator.com/item?id=19455465"><small>(ref)</small></a></div>

---

"_Se você está procurando aprender um **framework moderno** para construir APIs REST, dê uma olhada no **FastAPI** [...] É rápido, fácil de usar e fácil de aprender [...]_"

"_Nós trocamos nossas **APIs** por **FastAPI** [...] Acredito que você gostará dele [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>fundadores da [Explosion AI](https://explosion.ai) - criadores da [spaCy](https://spacy.io)</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680"><small>(ref)</small></a></div>

---

"_Se alguém estiver procurando construir uma API Python para produção, eu recomendaria fortemente o **FastAPI**. Ele é **lindamente projetado**, **simples de usar** e **altamente escalável**, e se tornou um **componente chave** para a nossa estratégia de desenvolvimento API first, impulsionando diversas automações e serviços, como o nosso Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

## Mini documentário do FastAPI { #fastapi-mini-documentary }

Há um [mini documentário do FastAPI](https://www.youtube.com/watch?v=mpR8ngthqiE) lançado no fim de 2025, você pode assisti-lo online:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, o FastAPI das interfaces de linhas de comando { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Se você estiver construindo uma aplicação <abbr title="Command Line Interface - Interface de Linha de Comando">CLI</abbr> para ser utilizada no terminal ao invés de uma API web, dê uma olhada no [**Typer**](https://typer.tiangolo.com/).

**Typer** é o irmão menor do FastAPI. E seu propósito é ser o **FastAPI das CLIs**. ⌨️ 🚀

## Requisitos { #requirements }

FastAPI está nos ombros de gigantes:

* [Starlette](https://www.starlette.dev/) para as partes web.
* [Pydantic](https://docs.pydantic.dev/) para a parte de dados.

## Instalação { #installation }

Crie e ative um [ambiente virtual](https://fastapi.tiangolo.com/pt/virtual-environments/) e então instale o FastAPI:

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
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou use <code>async def</code>...</summary>

Se seu código utiliza `async` / `await`, use `async def`:

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**Nota**:

Se você não sabe, verifique a seção _"Com pressa?"_ sobre [`async` e `await` nas docs](https://fastapi.tiangolo.com/pt/async/#in-a-hurry).

</details>

### Rode { #run-it }

Rode o servidor com:

<div class="termy">

```console
$ fastapi dev

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
<summary>Sobre o comando <code>fastapi dev</code>...</summary>

O comando `fastapi dev` lê automaticamente o seu arquivo `main.py`, detecta a aplicação **FastAPI** nele e inicia um servidor usando o [Uvicorn](https://www.uvicorn.dev).

Por padrão, o `fastapi dev` iniciará com auto-reload habilitado para desenvolvimento local.

Você pode ler mais sobre isso na [documentação do FastAPI CLI](https://fastapi.tiangolo.com/pt/fastapi-cli/).

</details>

### Verifique { #check-it }

Abra seu navegador em [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

Você verá a resposta JSON como:

```JSON
{"item_id": 5, "q": "somequery"}
```

Você acabou de criar uma API que:

* Recebe requisições HTTP nos _paths_ `/` e `/items/{item_id}`.
* Ambos _paths_ fazem <em>operações</em> `GET` (também conhecido como _métodos_ HTTP).
* O _path_ `/items/{item_id}` tem um _parâmetro de path_ `item_id` que deve ser um `int`.
* O _path_ `/items/{item_id}` tem um _parâmetro query_ `q` `str` opcional.

### Documentação Interativa da API { #interactive-api-docs }

Agora vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Você verá a documentação automática interativa da API (fornecida por [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentação Alternativa da API { #alternative-api-docs }

E agora, vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Você verá a documentação automática alternativa (fornecida por [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Evoluindo o Exemplo { #example-upgrade }

Agora modifique o arquivo `main.py` para receber um corpo de uma requisição `PUT`.

Declare o corpo utilizando tipos padrão Python, graças ao Pydantic.

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

O servidor `fastapi dev` deverá recarregar automaticamente.

### Evoluindo a Documentação Interativa da API { #interactive-api-docs-upgrade }

Agora vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* A documentação interativa da API será automaticamente atualizada, incluindo o novo corpo:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Clique no botão "Try it out", ele permitirá que você preencha os parâmetros e interaja diretamente com a API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Então clique no botão "Execute", a interface do usuário irá se comunicar com a API, enviar os parâmetros, pegar os resultados e mostrá-los na tela:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Evoluindo a Documentação Alternativa da API { #alternative-api-docs-upgrade }

E agora, vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

* A documentação alternativa também irá refletir o novo parâmetro query e o corpo:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recapitulando { #recap }

Resumindo, você declara **uma vez** os tipos dos parâmetros, corpo etc. como parâmetros de função.

Você faz isso com os tipos padrão do Python moderno.

Você não terá que aprender uma nova sintaxe, os métodos ou classes de uma biblioteca específica etc.

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
* <dfn title="também conhecido como: serialização, parsing, marshalling">Conversão</dfn> de dados de entrada: vindo da rede para dados e tipos Python. Consegue ler:
    * JSON.
    * Parâmetros de path.
    * Parâmetros query.
    * Cookies.
    * Cabeçalhos.
    * Formulários.
    * Arquivos.
* <dfn title="também conhecido como: serialização, parsing, marshalling">Conversão</dfn> de dados de saída: convertendo de tipos e dados Python para dados de rede (como JSON):
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

* Validar que existe um `item_id` no path para requisições `GET` e `PUT`.
* Validar que `item_id` é do tipo `int` para requisições `GET` e `PUT`.
    * Se não for, o cliente verá um erro útil e claro.
* Verificar se existe um parâmetro query opcional nomeado como `q` (como em `http://127.0.0.1:8000/items/foo?q=somequery`) para requisições `GET`.
    * Como o parâmetro `q` é declarado com `= None`, ele é opcional.
    * Sem o `None` ele seria obrigatório (como o corpo no caso de `PUT`).
* Para requisições `PUT` para `/items/{item_id}`, lerá o corpo como JSON:
    * Verifica que tem um atributo obrigatório `name` que deve ser `str`.
    * Verifica que tem um atributo obrigatório `price` que tem que ser um `float`.
    * Verifica que tem um atributo opcional `is_offer`, que deve ser um `bool`, se presente.
    * Tudo isso também funcionaria para objetos JSON profundamente aninhados.
* Converter de e para JSON automaticamente.
* Documentar tudo com OpenAPI, que poderá ser usado por:
    * Sistemas de documentação interativos.
    * Sistemas de clientes de geração de código automáticos, para muitas linguagens.
* Fornecer diretamente 2 interfaces web de documentação interativa.

---

Nós apenas arranhamos a superfície, mas você já tem ideia de como tudo funciona.

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

Para um exemplo mais completo incluindo mais recursos, veja o <a href="https://fastapi.tiangolo.com/pt/tutorial/">Tutorial - Guia do Usuário</a>.

**Alerta de Spoiler**: o tutorial - guia do usuário inclui:

* Declaração de **parâmetros** de diferentes lugares como: **cabeçalhos**, **cookies**, **campos de formulários** e **arquivos**.
* Como configurar **limitações de validação** como `maximum_length` ou `regex`.
* Um poderoso e fácil de usar sistema de **<dfn title="também conhecido como: componentes, recursos, provedores, serviços, injetáveis">Injeção de Dependência</dfn>**.
* Segurança e autenticação, incluindo suporte para **OAuth2** com autenticação com **JWT tokens** e **HTTP Basic**.
* Técnicas mais avançadas (mas igualmente fáceis) para declaração de **modelos JSON profundamente aninhados** (graças ao Pydantic).
* Integrações **GraphQL** com o [Strawberry](https://strawberry.rocks) e outras bibliotecas.
* Muitos recursos extras (graças ao Starlette) como:
    * **WebSockets**
    * testes extremamente fáceis baseados em HTTPX e `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...e mais.

### Implemente sua aplicação (opcional) { #deploy-your-app-optional }

Você pode opcionalmente implantar sua aplicação FastAPI na [FastAPI Cloud](https://fastapicloud.com), vá e entre na lista de espera se ainda não o fez. 🚀

Se você já tem uma conta na **FastAPI Cloud** (nós convidamos você da lista de espera 😉), pode implantar sua aplicação com um único comando.

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

É isso! Agora você pode acessar sua aplicação nesse URL. ✨

#### Sobre a FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** é construída pelo mesmo autor e equipe por trás do **FastAPI**.

Ela simplifica o processo de **construir**, **implantar** e **acessar** uma API com esforço mínimo.

Traz a mesma **experiência do desenvolvedor** de construir aplicações com FastAPI para **implantá-las** na nuvem. 🎉

A FastAPI Cloud é a principal patrocinadora e financiadora dos projetos open source do ecossistema *FastAPI and friends*. ✨

#### Implante em outros provedores de nuvem { #deploy-to-other-cloud-providers }

FastAPI é open source e baseado em padrões. Você pode implantar aplicações FastAPI em qualquer provedor de nuvem que escolher.

Siga os tutoriais do seu provedor de nuvem para implantar aplicações FastAPI com eles. 🤓

## Performance { #performance }

Testes de performance independentes do TechEmpower mostram aplicações **FastAPI** rodando sob Uvicorn como [um dos frameworks Python mais rápidos disponíveis](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), somente atrás de Starlette e Uvicorn (utilizados internamente pelo FastAPI). (*)

Para entender mais sobre isso, veja a seção [Comparações](https://fastapi.tiangolo.com/pt/benchmarks/).

## Dependências { #dependencies }

O FastAPI depende do Pydantic e do Starlette.

### Dependências `standard` { #standard-dependencies }

Quando você instala o FastAPI com `pip install "fastapi[standard]"`, ele vem com o grupo `standard` de dependências opcionais:

Utilizado pelo Pydantic:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - para validação de email.

Utilizado pelo Starlette:

* [`httpx`](https://www.python-httpx.org) - Obrigatório caso você queira utilizar o `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - Obrigatório se você quer utilizar a configuração padrão de templates.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - Obrigatório se você deseja suporte a <dfn title="convertendo a string que vem de uma requisição HTTP em dados Python">"parsing"</dfn> de formulário, com `request.form()`.

Utilizado pelo FastAPI:

* [`uvicorn`](https://www.uvicorn.dev) - para o servidor que carrega e serve a sua aplicação. Isto inclui `uvicorn[standard]`, que inclui algumas dependências (e.g. `uvloop`) necessárias para servir em alta performance.
* `fastapi-cli[standard]` - que disponibiliza o comando `fastapi`.
    * Isso inclui `fastapi-cloud-cli`, que permite implantar sua aplicação FastAPI na [FastAPI Cloud](https://fastapicloud.com).

### Sem as dependências `standard` { #without-standard-dependencies }

Se você não deseja incluir as dependências opcionais `standard`, você pode instalar utilizando `pip install fastapi` ao invés de `pip install "fastapi[standard]"`.

### Sem o `fastapi-cloud-cli` { #without-fastapi-cloud-cli }

Se você quiser instalar o FastAPI com as dependências padrão, mas sem o `fastapi-cloud-cli`, você pode instalar com `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

### Dependências opcionais adicionais { #additional-optional-dependencies }

Existem algumas dependências adicionais que você pode querer instalar.

Dependências opcionais adicionais do Pydantic:

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - para gerenciamento de configurações.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/) - para tipos extras a serem utilizados com o Pydantic.

Dependências opcionais adicionais do FastAPI:

* [`orjson`](https://github.com/ijl/orjson) - Obrigatório se você deseja utilizar o `ORJSONResponse`.
* [`ujson`](https://github.com/esnme/ultrajson) - Obrigatório se você deseja utilizar o `UJSONResponse`.

## Licença { #license }

Esse projeto é licenciado sob os termos da licença MIT.
