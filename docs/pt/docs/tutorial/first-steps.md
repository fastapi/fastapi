# Primeiros Passos { #first-steps }

O arquivo FastAPI mais simples pode se parecer com:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Copie o conteúdo para um arquivo `main.py`.

Execute o servidor ao vivo:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Na saída, há uma linha com algo como:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Essa linha mostra a URL onde a sua aplicação está sendo servida, na sua máquina local.

### Confira { #check-it }

Abra o seu navegador em [http://127.0.0.1:8000](http://127.0.0.1:8000).

Você verá essa resposta em JSON:

```JSON
{"message": "Hello World"}
```

### Documentação Interativa de APIs { #interactive-api-docs }

Agora vá para [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Você verá a documentação interativa automática da API (fornecida por [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentação Alternativa de APIs { #alternative-api-docs }

E agora, vá para [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Você verá a documentação alternativa automática (fornecida por [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

O **FastAPI** gera um "*schema*" com toda a sua API usando o padrão **OpenAPI** para definir APIs.

#### "*Schema*" { #schema }

Um "*schema*" é uma definição ou descrição de algo. Não o código que o implementa, mas apenas uma descrição abstrata.

#### API "*schema*" { #api-schema }

Nesse caso, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) é uma especificação que determina como definir um *schema* da sua API.

Esta definição de *schema* inclui os paths da sua API, os parâmetros possíveis que eles usam, etc.

#### "*Schema*" de dados { #data-schema }

O termo "*schema*" também pode se referir à forma de alguns dados, como um conteúdo JSON.

Nesse caso, significaria os atributos JSON e os tipos de dados que eles possuem, etc.

#### OpenAPI e JSON Schema { #openapi-and-json-schema }

OpenAPI define um *schema* de API para sua API. E esse *schema* inclui definições (ou "*schemas*") dos dados enviados e recebidos por sua API usando **JSON Schema**, o padrão para *schemas* de dados JSON.

#### Verifique o `openapi.json` { #check-the-openapi-json }

Se você está curioso(a) sobre a aparência do *schema* bruto OpenAPI, o FastAPI gera automaticamente um JSON (*schema*) com as descrições de toda a sua API.

Você pode ver isso diretamente em: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

Ele mostrará um JSON começando com algo como:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### Para que serve o OpenAPI { #what-is-openapi-for }

O *schema* OpenAPI é o que possibilita os dois sistemas de documentação interativos mostrados.

E existem dezenas de alternativas, todas baseadas em OpenAPI. Você pode facilmente adicionar qualquer uma dessas alternativas à sua aplicação criada com **FastAPI**.

Você também pode usá-lo para gerar código automaticamente para clientes que se comunicam com sua API. Por exemplo, aplicativos front-end, móveis ou IoT.

### Configure o `entrypoint` da aplicação em `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Você pode configurar onde sua aplicação está localizada em um arquivo `pyproject.toml`, assim:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Esse `entrypoint` dirá ao comando `fastapi` que ele deve importar a aplicação assim:

```python
from main import app
```

Se o seu código estiver estruturado assim:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Então você definiria o `entrypoint` como:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

o que seria equivalente a:

```python
from backend.main import app
```

### `fastapi dev` com path { #fastapi-dev-with-path }

Você também pode passar o path do arquivo para o comando `fastapi dev`, e ele vai deduzir o objeto de aplicação FastAPI a ser usado:

```console
$ fastapi dev main.py
```

Mas você teria que lembrar de passar o path correto toda vez que chamar o comando `fastapi`.

Além disso, outras ferramentas podem não conseguir encontrá-la, por exemplo, a [Extensão do VS Code](../editor-support.md) ou a [FastAPI Cloud](https://fastapicloud.com), então é recomendado usar o `entrypoint` no `pyproject.toml`.

### Faça o deploy da sua aplicação (opcional) { #deploy-your-app-optional }

Você pode, opcionalmente, fazer o deploy da sua aplicação FastAPI na [FastAPI Cloud](https://fastapicloud.com); acesse e entre na lista de espera, se ainda não entrou. 🚀

Se você já tem uma conta na **FastAPI Cloud** (nós convidamos você da lista de espera 😉), pode fazer o deploy da sua aplicação com um único comando.

Antes do deploy, certifique-se de que está autenticado:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Em seguida, faça o deploy da sua aplicação:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

É isso! Agora você pode acessar sua aplicação nessa URL. ✨

## Recapitulando, passo a passo { #recap-step-by-step }

### Passo 1: importe `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` é uma classe Python que fornece todas as funcionalidades para sua API.

/// note | Detalhes Técnicos

`FastAPI` é uma classe que herda diretamente de `Starlette`.

Você pode usar todas as funcionalidades do [Starlette](https://www.starlette.dev/) com `FastAPI` também.

///

### Passo 2: crie uma "instância" de `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Aqui, a variável `app` será uma "instância" da classe `FastAPI`.

Este será o principal ponto de interação para criar toda a sua API.

### Passo 3: crie uma operação de rota { #step-3-create-a-path-operation }

#### Path { #path }

"Path" aqui se refere à última parte da URL, começando do primeiro `/`.

Então, em uma URL como:

```
https://example.com/items/foo
```

...o path seria:

```
/items/foo
```

/// info | Informação

Um "path" também é comumente chamado de "endpoint" ou de "rota".

///

Ao construir uma API, o "path" é a principal forma de separar "preocupações" e "recursos".

#### Operação { #operation }

"Operação" aqui se refere a um dos "métodos" HTTP.

Um dos:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...e os mais exóticos:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

No protocolo HTTP, você pode se comunicar com cada path usando um (ou mais) desses "métodos".

---

Ao construir APIs, você normalmente usa esses métodos HTTP para executar uma ação específica.

Normalmente você usa:

* `POST`: para criar dados.
* `GET`: para ler dados.
* `PUT`: para atualizar dados.
* `DELETE`: para deletar dados.

Portanto, no OpenAPI, cada um dos métodos HTTP é chamado de "operação".

Vamos chamá-los de "**operações**" também.

#### Defina um decorador de operação de rota { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

O `@app.get("/")` diz ao **FastAPI** que a função logo abaixo é responsável por tratar as requisições que vão para:

* o path `/`
* usando uma <dfn title="um método HTTP GET"><code>get</code> operação</dfn>

/// info | Informações sobre `@decorator`

Essa sintaxe `@alguma_coisa` em Python é chamada de "decorador".

Você o coloca em cima de uma função. Como um chapéu decorativo (acho que é daí que vem o termo).

Um "decorador" pega a função abaixo e faz algo com ela.

Em nosso caso, este decorador informa ao **FastAPI** que a função abaixo corresponde ao **path** `/` com uma **operação** `get`.

É o "**decorador de operação de rota**".

///

Você também pode usar as outras operações:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

E os mais exóticos:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Dica

Você está livre para usar cada operação (método HTTP) como desejar.

O **FastAPI** não impõe nenhum significado específico.

As informações aqui são apresentadas como uma orientação, não uma exigência.

Por exemplo, ao usar GraphQL, você normalmente executa todas as ações usando apenas operações `POST`.

///

### Passo 4: defina a **função de operação de rota** { #step-4-define-the-path-operation-function }

Esta é a nossa "**função de operação de rota**":

* **path**: é `/`.
* **operação**: é `get`.
* **função**: é a função abaixo do "decorador" (abaixo do `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

Esta é uma função Python.

Ela será chamada pelo **FastAPI** sempre que receber uma requisição para a URL "`/`" usando uma operação `GET`.

Neste caso, é uma função `async`.

---

Você também pode defini-la como uma função normal em vez de `async def`:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | Nota

Se você não sabe a diferença, verifique o [Async: *"Com pressa?"*](../async.md#in-a-hurry).

///

### Passo 5: retorne o conteúdo { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

Você pode retornar um `dict`, `list` e valores singulares como `str`, `int`, etc.

Você também pode devolver modelos Pydantic ( você verá mais sobre isso mais tarde).

Existem muitos outros objetos e modelos que serão convertidos automaticamente para JSON (incluindo ORMs, etc). Tente usar seus favoritos, é altamente provável que já sejam compatíveis.

### Passo 6: Faça o deploy { #step-6-deploy-it }

Faça o deploy da sua aplicação para a **[FastAPI Cloud](https://fastapicloud.com)** com um comando: `fastapi deploy`. 🎉

#### Sobre o FastAPI Cloud { #about-fastapi-cloud }

A **[FastAPI Cloud](https://fastapicloud.com)** é construída pelo mesmo autor e equipe por trás do **FastAPI**.

Ela simplifica o processo de **construir**, **fazer deploy** e **acessar** uma API com o mínimo de esforço.

Traz a mesma **experiência do desenvolvedor** de criar aplicações com FastAPI para **fazer o deploy** delas na nuvem. 🎉

A FastAPI Cloud é a principal patrocinadora e financiadora dos projetos open source do ecossistema *FastAPI and friends*. ✨

#### Faça o deploy em outros provedores de nuvem { #deploy-to-other-cloud-providers }

FastAPI é open source e baseado em padrões. Você pode fazer deploy de aplicações FastAPI em qualquer provedor de nuvem que preferir.

Siga os tutoriais do seu provedor de nuvem para fazer deploy de aplicações FastAPI com eles. 🤓

## Recapitulando { #recap }

* Importe `FastAPI`.
* Crie uma instância do `app`.
* Escreva um **decorador de operação de rota** usando decoradores como `@app.get("/")`.
* Defina uma **função de operação de rota**; por exemplo, `def root(): ...`.
* Execute o servidor de desenvolvimento usando o comando `fastapi dev`.
* Opcionalmente, faça o deploy da sua aplicação com `fastapi deploy`.
