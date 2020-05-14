{!../../../docs/missing-translation.md!}
<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, alta performance, fácil para aprender, rápido para codificar, pronto para produção</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/fastapi" target="_blank">
    <img src="https://travis-ci.com/tiangolo/fastapi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Package version">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Join the chat at https://gitter.im/tiangolo/fastapi">
</a>
</p>
---

**Documentação**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Código fonte**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI é um moderno, rápido (alta performance), framework web para construir APIs com Python 3.6+ baseado em type hints Python padrão.

Os principais recursos são:

* **Rápido**: Desenpenho altíssimo, ao lado de **NodeJS** e **Go** (graças a Starlette e Pydantic). [Uma das estruturas Python mais rápidas disponível](#performance).

* **Rápido para codificar**: Aumente a velocidade para desenvolver recursos em cerca de 200% a 300% *.
* **Menos bugs**: Reduza cerca de 40% dos erros induzidos por humanos (desenvolvedor). *
* **Intuitivo**: Ótimo suporte ao editor. <abbr title = "também conhecido como preenchimento automático, preenchimento automático, IntelliSense"> Conclusão </abbr> em qualquer lugar. Menos tempo de depuração.
* **Fácil**: Projetado para ser fácil de usar e aprender. Menos tempo lendo documentos.
* **Pequeno**: Minimize a duplicação de código. Vários recursos para cada declaração de parâmetro. Menos erros.
* **Robusto**: Obtenha código pronto para produção. Com documentação interativa automática.
* **Baseado em padrões**: Baseado (e totalmente compatível) com padrões abertos para APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (anteriormente conhecido como Swagger) e <a href="http://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* estimativa baseada em testes em uma equipe de desenvolvimento interna, construindo aplicativos de produção.</small>

## Opiniões

"*[...] Eu estou usando muito **FastAPI** nos dias de hoje. [...] estou planejando usá-lo para todos os serviços **ML da minha equipe na Microsoft**. Alguns deles estão sendo integrados ao produto principal **Windows** e alguns produtos **Office**. * "

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"*Estou muito animado com o **FastAPI**. É tão divertido!*"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> - host de podcast</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"*Honestamente, o que você construiu parece super sólido e polido. De muitas maneiras, eu queria te dar um **Hug** (abraço)  - é realmente inspirador ver alguém construindo isso.*"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - criador da <strong><a href="http://www.hug.rest/" target="_blank">Hug</a></strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"*Se você deseja aprender uma **estrutura moderna** para criar APIs REST, confira **FastAPI** [...] É rápido, fácil de usar e fácil de aprender [...] **"

"*Mudamos nossas **APIs** para o **FastAPI**  [...] acho que você vai gostar [...]*"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong>Fundadores da <a href="https://explosion.ai" target="_blank">Explosion AI</a> e criadores da <a href="https://spacy.io" target="_blank">spaCy</a></strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"*Adotamos a biblioteca **FastAPI** para gerar um servidor **REST** que pode ser consultado para obter **previsões**. [para o Ludwig]*"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, e Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, o FastAPI para CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Se você está criando uma <abbr title="Interface de linha de comando">CLI</abbr> para ser usado no terminal em vez de uma API da web, confira <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** é o irmão mais novo da FastAPI. E pretende ser o **FastAPI para CLIs**. ⌨️ 🚀

## Requisitos

Python 3.6+

FastAPI está sobre os ombros dos gigantes:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> para as partes web.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> Para os dados.

## Instalação

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

Você também precisará de um servidor ASGI, para produção como <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> ou <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## Exemplo

### Crie

* Crie um arquivo `main.py`:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ou use <code>async def</code>...</summary>

Se seu código usa `async` / `await`, use `async def`:

```Python hl_lines="7 12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**Nota**:

Se você não souber sobre isso, verifique a seção _"Com pressa?"_ <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` e `await` na documentação.</a>.

</details>

### Rodando

Rode o servidor com:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Sobre o comando <code>uvicorn main:app --reload</code>...</summary>

O comando `uvicorn main:app` se refera a:

* `main`: o arquivo `main.py` (o "módulo" Python).
* `app`: o objeto criado em `main.py` com a linha `app = FastAPI()`.
* `--reload`: faz o servidor reiniciar depois de mudanças no código. Somente em desenvolvimento.

</details>

### Confira

Abra seu navegador em <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Você verá a resposta JSON como:

```JSON
{"item_id": 5, "q": "somequery"}
```

Você já criou uma API que:

* Recebe requisições HTTP nos _paths_ `/` e `/items/{item_id}`.
* Ambos os _paths_ fazem <em>operações</em> `GET` (também conhecido como _método_ HTTP).
* O _path_ `/items/{item_id}` tem como _parametro_ `item_id` que espera um `int`.
* O _path_ `/items/{item_id}` tem um _parâmetro de consulta_ opcional `q` como `str`.

### Documentação Interativa da API

Agora vá para <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá a documentação da API interativa automática (provida por <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentação alternativa da API

Agora, vá para <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Você verá a documentação automática alternativa (provida por <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Atualização do exemplo

Agora modifique o arquivo `main.py` para receber o body de uma requisição `PUT`.

Declare o body usando tipos padrão de Python, graças ao Pydantic.

```Python hl_lines="2  7 8 9 10  23 24 25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

O servidor deve recarregar automaticamente (pois você adicionou `--reload` ao comando `uvicorn` anteriormente).

### Upgrade da documentação interativa da API

Agora vá para <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* A documentação da API interativa será atualizada automaticamente, incluindo o novo corpo:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Clique no botão "Try it out", isso permite que você preencha os parâmetros e interaja diretamente com a API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Em seguida, clique no botão "Execute", a interface do usuário se comunicará com sua API, enviará os parâmetros, obterá os resultados e os mostrará na tela:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Upgrade da documentação alternativa da API

Agora vá para <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* A documentação alternativa também refletirá o novo parâmetro e corpo da consulta:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recapitulando

Em resumo, você declara **uma vez** os tipos de parâmetros, corpo etc. como parâmetros de função.

Você faz isso com os tipos padrão modernos do Python.

Você não precisa aprender uma nova sintaxe, os métodos ou classes de uma biblioteca específica, etc.

Apenas o **Python 3.6 +** padrão.

Por exemplo, para um `int`:

```Python
item_id: int
```

Ou para um modelo mais complexo `Item`:

```Python
item: Item
```

...e com essa sim,ples declaração você tem:

* Suporte a editor, incluindo:
    * Completion.
    * Checagem de tipo.
* Validação de dados:
    * Erros automáticos e limpos quando os dados são inválidos.
    * Validação mesmo para objetos JSON profundamente aninhados.
* <abbr title="also known as: serialization, parsing, marshalling">Conversão</abbr> de dados de entrada: vindo da rede para dados e tipos Python. Leitura de:
    * JSON.
    * Parâmetros de path.
    * Parâmetros de consulta.
    * Cookies.
    * Headers.
    * Formulários.
    * Arquivos.
* <abbr title="also known as: serialization, parsing, marshalling">Conversão</abbr> de dados de saída: convertendo de dados e tipos do Python para dados da rede (como JSON):
    * Converte tipos Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Objetos `datetime`.
    * Objetos `UUID`.
    * Modelos de base de dados.
    * ...e muito mais.
* Documentação interativa automática da API, incluindo 2 interfaces de usuário alternativas:
    * Swagger UI.
    * ReDoc.

---

Voltando ao exemplo de código anterior, **FastAPI** irá:

* Validar se existe um `item_id` no path para requisições `GET` e `PUT`.
* Validar se `item_id` é do tipo `int` para requisições `GET` e `PUT`.
    * Se não estiver, o cliente verá um erro claro e útil. 
* Verificar se existe um parâmetro de consulta opcional chamado`q` (como em `http://127.0.0.1:8000/items/foo?q=somequery`) para requisições `GET`.
    * Se o parâmetro `q` é declarado como `= None`, Isso é opcional.
    * Sem o `None` isso deve ser necessário (como é o body no caso do `PUT`).
* Requisições `PUT` para `/items/{item_id}`, lerá o body como JSON:
    * Verifica se possui um atributo obrigatório `name`, que deve ser `str`. 
    * Verifica se o atributo obrigatório `price` é do tipo `float`.
    * Checa se há um atributo opcional `is_offer`, que deve ser um `bool`, se presente.
    * Tudo isso também funcionaria para objetos JSON profundamente aninhados.
* Converte de e para JSON automaticamente.
* Documenta tudo com OpenAPI, que pode ser usado para:
    * Documentação interativa do sistema.
    * Sistemas de geração automática de código do cliente, para vários idiomas.
* Fornece 2 interfaces da web de documentação interativa diretamente.

---

Acabamos de arranhar a superfície, mas você já tem a ideia de como tudo funciona.

Tente mudar a linha com:

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

...e veja como seu editor concluirá automaticamente os atributos e conhecerá seus tipos:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Para um exemplo mais completo, incluindo mais recursos, veja o <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Guia do usuário.</a>.

**Alerta de spoiler**: o tutorial - guia do usuário inclui:

* Declaração de **parametros** de outros lugares diferentes como: **headers**, **cookies**, **campos de formulário** e **arquivos**.
* Como definir **restições de validação** como `maximum_length` ou `regex`.
* Um sistema de **<abbr title="also known as components, resources, providers, services, injectables">Injeção de dependência</abbr>** muito poderoso e fácil de usar.
* Segurança e autenticação, incluindo suporte a **OAuth2** com **tokens JWT** e autenticação **HTTP Basic**.
* Mais avançadas (mas igualmente fáceis) tecnicas para declarar **modelos JSON profundamente aninhados** (agradecimentos a Pydantic).
* Muitos recursos extras (agradecimentos a Starlette) como:
    * **WebSockets**
    * **GraphQL**
    * Testes extremamente fáceis com `requests` e `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...e mais.

## Performance

Independent TechEmpower benchmarks mostra que aplicações **FastAPI** sob Uvicorn são <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">um dos frameworks Python mais rápidos exixtentes</a>, apenas abaixo de Starlette e Uvicorn (usado internamente pelo FastAPI). (*)

Para saber mais sobre isso, veja a seção <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dependências opcionais

Usado por Pydantic:

* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - para <abbr title="convertendo a string que vem de uma solicitação HTTP em dados Python">"análise"</abbr> mais rápida do JSON.
* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - para validação de email.

Usado por Starlette:

* <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - Necessário se você deseja usar o `TestClient`.
* <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Necessário se você deseja usar o `FileResponse` or `StaticFiles`.
* <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Necessário se você deseja usar a configuração default de template.
* <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Necessário se você deseja dar suporte a <abbr title="convertendo a string que vem de uma solicitação HTTP em dados Python">"análise"</abbr> de formulário , with `request.form()`.
* <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Necessário para suporte a `SessionMiddleware`.
* <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Necessário para suporte ao `SchemaGenerator` do Starlette (você provavelmente não precisa disso com FastAPI).
* <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Necessário para suporte ao `GraphQLApp`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Necessário se você procura usar `UJSONResponse`.

Usado por FastAPI / Starlette:

* <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - para o servidor que carrega e serve seu aplicativo.
* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Necessário se você deseja usar `ORJSONResponse`.

Você pode instalar tudo isso com `pip install fastapi[all]`.

## Licença

Este projeto está licenciado sob os termos da licença MIT.
