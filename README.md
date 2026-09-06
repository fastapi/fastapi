<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
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

**Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**Source Code**: [https://github.com/fastapi/fastapi](https://github.com/fastapi/fastapi)

---

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

The key features are:

* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic). [One of the fastest Python frameworks available](#performance).
* **Fast to code**: Increase the speed to develop features by about 200% to 300%. *
* **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *
* **Intuitive**: Great editor support. <dfn title="also known as auto-complete, autocompletion, IntelliSense">Completion</dfn> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
* **Robust**: Get production-ready code. With automatic interactive documentation.
* **Standards-based**: Based on (and fully compatible with) the open standards for APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (previously known as Swagger) and [JSON Schema](https://json-schema.org/).

<small>* estimation based on tests conducted by an internal development team, building production applications.</small>

## Sponsors

<!-- sponsors -->
### Keystone Sponsor

<a href="https://fastapicloud.com" target="_blank" title="FastAPI Cloud. By the same team behind FastAPI. You code. We Cloud."><img src="https://fastapi.tiangolo.com/img/sponsors/fastapicloud.png"></a>

### Gold Sponsors

<a href="https://blockbee.io?ref=fastapi" target="_blank" title="BlockBee Cryptocurrency Payment Gateway"><img src="https://fastapi.tiangolo.com/img/sponsors/blockbee.png"></a>
<a href="https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=mainbadge" target="_blank" title="Auth, user management and more for your B2B product"><img src="https://fastapi.tiangolo.com/img/sponsors/propelauth.png"></a>
<a href="https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi" target="_blank" title="Deploy & scale any full-stack web app on Render. Focus on building apps, not infra."><img src="https://fastapi.tiangolo.com/img/sponsors/render.svg"></a>
<a href="https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=badge&utm_campaign=fastapi" target="_blank" title="Cut Code Review Time & Bugs in Half with CodeRabbit"><img src="https://fastapi.tiangolo.com/img/sponsors/coderabbit.png"></a>
<a href="https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source" target="_blank" title="The Gold Standard in Retail Account Linking"><img src="https://fastapi.tiangolo.com/img/sponsors/subtotal.svg"></a>
<a href="https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi" target="_blank" title="Deploy enterprise applications at startup speed"><img src="https://fastapi.tiangolo.com/img/sponsors/railway.png"></a>
<a href="https://serpapi.com/?utm_source=fastapi_website" target="_blank" title="SerpApi: Web Search API"><img src="https://fastapi.tiangolo.com/img/sponsors/serpapi.png"></a>
<a href="https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page" target="_blank" title="Greptile: The AI Code Reviewer"><img src="https://fastapi.tiangolo.com/img/sponsors/greptile.png"></a>

### Silver Sponsors

<a href="https://databento.com/?utm_source=fastapi&utm_medium=sponsor&utm_content=display" target="_blank" title="Pay as you go for market data"><img src="https://fastapi.tiangolo.com/img/sponsors/databento.svg"></a>
<a href="https://www.svix.com/" target="_blank" title="Svix - Webhooks as a service"><img src="https://fastapi.tiangolo.com/img/sponsors/svix.svg"></a>
<a href="https://www.permit.io/blog/implement-authorization-in-fastapi?utm_source=github&utm_medium=referral&utm_campaign=fastapi" target="_blank" title="Fine-Grained Authorization for FastAPI"><img src="https://fastapi.tiangolo.com/img/sponsors/permit.png"></a>
<a href="https://dribia.com/en/" target="_blank" title="Dribia - Data Science within your reach"><img src="https://fastapi.tiangolo.com/img/sponsors/dribia.png"></a>
<a href="https://www.bairesdev.com/" target="_blank" title="BairesDev | Nearshore Software Development & Staff Augmentation Company"><img src="https://fastapi.tiangolo.com/img/sponsors/bairesdev.svg"></a>
<a href="https://tutorcruncher.com/?utm_source=fastapi" target="_blank" title="TutorCruncher"><img src="https://fastapi.tiangolo.com/img/sponsors/tutorcruncher.png"></a>

<!-- /sponsors -->

[Other sponsors](https://fastapi.tiangolo.com/fastapi-people/#sponsors)

## Opinions



<div class="only-github" markdown="1">

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://www.uber.com/us/en/blog/ludwig-v0-2/"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072"><small>(ref)</small></a></div>

---

"_If anyone is looking to build a production Python API, I would highly recommend **FastAPI**. It is **beautifully designed**, **simple to use** and **highly scalable**, it has become a **key component** in our API first development strategy and is driving many automations and services such as our Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/"><small>(ref)</small></a></div>

---

</div>

## FastAPI mini documentary

There's a [FastAPI mini documentary](https://www.youtube.com/watch?v=mpR8ngthqiE) released at the end of 2025, you can watch it online:

<a class="fastapi-feature-banner" href="https://www.youtube.com/watch?v=mpR8ngthqiE"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**, the FastAPI of CLIs

<a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

If you are building a <abbr title="Command Line Interface">CLI</abbr> app to be used in the terminal instead of a web API, check out [**Typer**](https://typer.tiangolo.com/).

**Typer** is FastAPI's little sibling. And it's intended to be the **FastAPI of CLIs**. ⌨️ 🚀

## Requirements

FastAPI stands on the shoulders of giants:

* [Starlette](https://starlette.dev/) for the web parts.
* [Pydantic](https://pydantic.dev/docs/) for the data parts.

## Installation

First, [install `uv`](https://docs.astral.sh/uv/getting-started/installation/), and then add FastAPI to your project:

<div class="termy">

```console
$ uv add "fastapi[standard]"

---> 100%
```

</div>

**Note**: Make sure you put `"fastapi[standard]"` in quotes to ensure it works in all terminals.

If you prefer to use `pip`, install `fastapi[standard]` inside a virtual environment. See the [installation guide](tutorial/#install-fastapi) for the alternative steps.

## Example

### Create it

Create a file `main.py` with:

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
<summary>Or use <code>async def</code>...</summary>

If your code uses `async` / `await`, use `async def`:

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

**Note**:

If you don't know, check the _"In a hurry?"_ section about [`async` and `await` in the docs](https://fastapi.tiangolo.com/async/#in-a-hurry).

</details>

### Run it

Run the server with:

<div class="termy">

```console
$ uv run fastapi dev

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
<summary>About the command <code>fastapi dev</code>...</summary>

The command `fastapi dev` reads your `main.py` file automatically, detects the **FastAPI** app in it, and starts a server using [Uvicorn](https://uvicorn.dev).

By default, `fastapi dev` will start with auto-reload enabled for local development.

You can read more about it in the [FastAPI CLI docs](https://fastapi.tiangolo.com/fastapi-cli/).

</details>

### Check it

Open your browser at [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery).

You will see the JSON response as:

```JSON
{"item_id": 5, "q": "somequery"}
```

You already created an API that:

* Receives HTTP requests in the _paths_ `/` and `/items/{item_id}`.
* Both _paths_ take `GET` <em>operations</em> (also known as HTTP _methods_).
* The _path_ `/items/{item_id}` has a _path parameter_ `item_id` that should be an `int`.
* The _path_ `/items/{item_id}` has an optional `str` _query parameter_ `q`.

### Interactive API docs

Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

And now, go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Redocly/redoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Example upgrade

Now modify the file `main.py` to receive a body from a `PUT` request.

Declare the body using standard Python types, thanks to Pydantic.

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

The `fastapi dev` server should reload automatically.

### Interactive API docs upgrade

Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

* The interactive API documentation will be automatically updated, including the new body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Click on the button "Try it out", it allows you to fill the parameters and directly interact with the API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Then click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade

And now, go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

* The alternative documentation will also reflect the new query parameter and body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap

In summary, you declare **once** the types of parameters, body, etc. as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python**.

For example, for an `int`:

```Python
item_id: int
```

or for a more complex `Item` model:

```Python
item: Item
```

...and with that single declaration you get:

* Editor support, including:
    * Completion.
    * Type checks.
* Validation of data:
    * Automatic and clear errors when the data is invalid.
    * Validation even for deeply nested JSON objects.
* <dfn title="also known as: serialization, parsing, marshalling">Conversion</dfn> of input data: coming from the network to Python data and types. Reading from:
    * JSON.
    * Path parameters.
    * Query parameters.
    * Cookies.
    * Headers.
    * Forms.
    * Files.
* <dfn title="also known as: serialization, parsing, marshalling">Conversion</dfn> of output data: converting from Python data and types to network data (as JSON):
    * Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
    * `datetime` objects.
    * `UUID` objects.
    * Database models.
    * ...and many more.
* Automatic interactive API documentation, including 2 alternative user interfaces:
    * Swagger UI.
    * ReDoc.

---

Coming back to the previous code example, **FastAPI** will:

* Validate that there is an `item_id` in the path for `GET` and `PUT` requests.
* Validate that the `item_id` is of type `int` for `GET` and `PUT` requests.
    * If it is not, the client will see a useful, clear error.
* Check if there is an optional query parameter named `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) for `GET` requests.
    * As the `q` parameter is declared with `= None`, it is optional.
    * Without the `None` it would be required (as is the body in the case with `PUT`).
* For `PUT` requests to `/items/{item_id}`, read the body as JSON:
    * Check that it has a required attribute `name` that should be a `str`.
    * Check that it has a required attribute `price` that has to be a `float`.
    * Check that it has an optional attribute `is_offer`, that should be a `bool`, if present.
    * All this would also work for deeply nested JSON objects.
* Convert from and to JSON automatically.
* Document everything with OpenAPI, that can be used by:
    * Interactive documentation systems.
    * Automatic client code generation systems, for many languages.
* Provide 2 interactive documentation web interfaces directly.

---

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...and see how your editor will auto-complete the attributes and know their types:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

For a more complete example including more features, see the <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Spoiler alert**: the tutorial - user guide includes:

* Declaration of **parameters** from other different places such as: **headers**, **cookies**, **form fields** and **files**.
* How to set **validation constraints** such as `maximum_length` or `regex`.
* A very powerful and easy to use **<dfn title="also known as components, resources, providers, services, injectables">Dependency Injection</dfn>** system.
* Security and authentication, including support for **OAuth2** with **JWT tokens** and **HTTP Basic** auth.
* More advanced (but equally easy) techniques for declaring **deeply nested JSON models** (thanks to Pydantic).
* **GraphQL** integration with [Strawberry](https://strawberry.rocks) and other libraries.
* Many extra features (thanks to Starlette) such as:
    * **WebSockets**
    * extremely easy tests based on HTTPX and `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...and more.

### Deploy your app (optional)

You can optionally deploy your FastAPI app to [FastAPI Cloud](https://fastapicloud.com) with a single command. 🚀

<div class="termy">

```console
$ uv run fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

The CLI will automatically detect your FastAPI application and deploy it to the cloud. If you are not logged in, your browser will open to complete the authentication process.

That's it! Now you can access your app at that URL. ✨

#### About FastAPI Cloud

**[FastAPI Cloud](https://fastapicloud.com)** is built by the same author and team behind **FastAPI**.

It streamlines the process of **building**, **deploying**, and **accessing** an API with minimal effort.

It brings the same **developer experience** of building apps with FastAPI to **deploying** them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the *FastAPI and friends* open source projects. ✨

#### Deploy to other cloud providers

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

## Performance

Independent TechEmpower benchmarks show **FastAPI** applications running under Uvicorn as [one of the fastest Python frameworks available](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), only below Starlette and Uvicorn themselves (used internally by FastAPI). (*)

To understand more about it, see the section [Benchmarks](https://fastapi.tiangolo.com/benchmarks/).

## Dependencies

FastAPI depends on Pydantic and Starlette.

### `standard` Dependencies

When you install FastAPI with `uv add "fastapi[standard]"` it comes with the `standard` group of optional dependencies:

Used by Pydantic:

* [`email-validator`](https://github.com/JoshData/python-email-validator) - for email validation.

Used by Starlette:

* [`httpx`](https://www.python-httpx.org) - Required if you want to use the `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - Required if you want to use the default template configuration.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - Required if you want to support form <dfn title="converting the string that comes from an HTTP request into Python data">"parsing"</dfn>, with `request.form()`.

Used by FastAPI:

* [`uvicorn`](https://uvicorn.dev) - for the server that loads and serves your application. This includes `uvicorn[standard]`, which includes some dependencies (e.g. `uvloop`) needed for high performance serving.
* `fastapi-cli[standard]` - to provide the `fastapi` command.
    * This includes `fastapi-cloud-cli`, which allows you to deploy your FastAPI application to [FastAPI Cloud](https://fastapicloud.com).

### Without `standard` Dependencies

If you don't want to include the `standard` optional dependencies, you can install with `uv add fastapi` instead of `uv add "fastapi[standard]"`.

### Without `fastapi-cloud-cli`

If you want to install FastAPI with the standard dependencies but without the `fastapi-cloud-cli`, you can install with `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

### Additional Optional Dependencies

There are some additional dependencies you might want to install.

Additional optional Pydantic dependencies:

* [`pydantic-settings`](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/) - for settings management.
* [`pydantic-extra-types`](https://github.com/pydantic/pydantic-extra-types) - for extra types to be used with Pydantic.

Additional optional FastAPI dependencies:

* [`orjson`](https://github.com/ijl/orjson) - Required if you want to use `ORJSONResponse`.
* [`ujson`](https://github.com/ultrajson/ultrajson) - Required if you want to use `UJSONResponse`.

## License

This project is licensed under the terms of the MIT license.


## 🌐 Web Resources & Interactive Index
- [BESTIES CHINESE NEW YEAR CELEBRATION](https://quizverses.pages.dev/besties-chinese-new-year-celebration.html)
- [CATEGORY PARTY23](https://quizverses-9d2f2.web.app/category-party23.html)
- [CATEGORY COOKING46](https://studyquests.github.io/category-cooking46.html)
- [MERGE HEROES](https://quizverses.pages.dev/merge-heroes.html)
- [ORGANIZER MASTER](https://quizverses.pages.dev/organizer-master.html)
- [CATEGORY GROW99](https://quizverses.pages.dev/category-grow99.html)
- [TILE MATCH CAFE](https://studyplaying.github.io/tile-match-cafe.html)
- [SCREWDOM 3D](https://studyquests.github.io/screwdom-3d.html)
- [ONLINE PORTAL](https://learnquester.github.io/)
- [DOMINO ADVENTURE](https://studyplaying.github.io/domino-adventure.html)
- [HOOK MASTER MAFIA CITY](https://quizverses.pages.dev/hook-master-mafia-city.html)
- [FOREST GLADE MYSTERIES](https://iskillquest.pages.dev/forest-glade-mysteries.html)
- [BUBBLE SHOOTER NEON](https://studyplayings.pages.dev/bubble-shooter-neon.html)
- [CATEGORY MATCH 3117](https://studyquesthub.web.app/category-match-3117.html)
- [CATEGORY SIMULATION 2](https://studyquests.github.io/category-simulation-2.html)
- [ZOMBIE DRIFT 3D](https://studyplayings.web.app/zombie-drift-3d.html)
- [CAR PARKING STUNT GAMES 2024](https://studyquesthub.web.app/car-parking-stunt-games-2024.html)
- [3D ACRYLIC NAIL NAIL ART GAME](https://studyquests.github.io/3d-acrylic-nail-nail-art-game.html)
- [ASMR BEAUTY TREATMENT](https://quizverses-9d2f2.web.app/asmr-beauty-treatment.html)
- [FORMULA RACING GAMES CAR GAME](https://studyquesthub.web.app/formula-racing-games-car-game.html)
- [BACK 2 SCHOOL MAKEOVER](https://thelearnquesters.pages.dev/back-2-school-makeover.html)
- [GRUKKLE ONSLAUGHT](https://thelearnquesters.pages.dev/grukkle-onslaught.html)
- [KEY QUEST](https://learnquester.pages.dev/key-quest.html)
- [ZOMBIES AND GUNS](https://studyplaying.github.io/zombies-and-guns.html)
- [CATEGORY ESCAPE](https://quizverses.github.io/category-escape.html)
- [WORLD SOCCER](https://studyplayings.web.app/world-soccer.html)
- [FANTASY MADNESS](https://learnquester.pages.dev/fantasy-madness.html)
- [DESERT ROVER SURVIVAL](https://quizverses-9d2f2.web.app/desert-rover-survival.html)
- [ANIMAL MERGE ZOO PARK](https://thelearnquester.web.app/animal-merge-zoo-park.html)
- [CAPYBARA SUIKA](https://studyquests.pages.dev/capybara-suika.html)
- [ELLIE AND FRIENDS ART BLOOM AESTHETIC](https://thelearnquesters.pages.dev/ellie-and-friends-art-bloom-aesthetic.html)
- [PYRAMIDZ](https://thequizzone.pages.dev/pyramidz.html)
- [PING PONG BATTLE TABLE TENNIS](https://thelearnquesters.pages.dev/ping-pong-battle-table-tennis.html)
- [CATEGORY TITANIUMNETWORK PROXIES](https://quizverses-9d2f2.web.app/category-titaniumnetwork-proxies.html)
- [MAGIC BRICK WARS](https://thelearnquesters.pages.dev/magic-brick-wars.html)
- [CATEGORY OBSTACLE299](https://quizverses-9d2f2.web.app/category-obstacle299.html)
- [CLAY CRAFT TYCOON](https://thelearnquesters.pages.dev/clay-craft-tycoon.html)
- [SUPERMARKET SIMULATOR DREAM STORE](https://studyplaying.github.io/supermarket-simulator-dream-store.html)
- [UNPUZZLE MASTER](https://quizverses.pages.dev/unpuzzle-master.html)
- [HORROR FOREST BEAR](https://thelearnquester.web.app/horror-forest-bear.html)
- [CATEGORY BATTLE 3](https://thequizzone.pages.dev/category-battle-3.html)
- [WOOD NUTS MASTER SCREW PUZZLE](https://quizverses.github.io/wood-nuts-master-screw-puzzle.html)
- [BRAIN PUZZLES QUESTS](https://quizverses.github.io/brain-puzzles-quests.html)
- [FLOWER COLLECTION](https://thelearnquesters.pages.dev/flower-collection.html)
- [CATEGORY MOUSE1 699](https://learnquesters.pages.dev/category-mouse1-699.html)
- [STICKMAN FIGHT PRO](https://thelearnquesters.pages.dev/stickman-fight-pro.html)
- [CATEGORY JIGSAW](https://thequizzone.pages.dev/category-jigsaw.html)
- [CATEGORY BATTLE ROYALE25](https://thequizzone.pages.dev/category-battle-royale25.html)
- [IDLE TRADE ROUTES](https://studyplayings.pages.dev/idle-trade-routes.html)
- [VIRTUAL NEKO KITTY COLLECTOR](https://learnquester.pages.dev/virtual-neko-kitty-collector.html)
- [GUN RUSH](https://learnquester.pages.dev/gun-rush.html)
- [KITTY SQUAD WINTER DRESS UP](https://thelearnquester.web.app/kitty-squad-winter-dress-up.html)
- [KING KONG CHAOS](https://quizverses.github.io/king-kong-chaos.html)
- [TRAFFIC RUN PUZZLE](https://studyplayings.web.app/traffic-run-puzzle.html)
- [CATEGORY CAT](https://studyquesthub.web.app/category-cat.html)
- [HEXA TILE TRIO](https://studyquests.github.io/hexa-tile-trio.html)
- [MATH STARS](https://learnquester.pages.dev/math-stars.html)
- [SLAP AND RUN](https://studyplayings.pages.dev/slap-and-run.html)
- [SCHOOLBOY RUNAWAY ROOM ESCAPE](https://learnquester.github.io/schoolboy-runaway-room-escape.html)
- [TRIANGLE WAY](https://learnquester.pages.dev/triangle-way.html)
- [INDEX14](https://learnquesters.pages.dev/index14.html)
- [CATEGORY BOOKMARKLET](https://thequizzone.pages.dev/category-bookmarklet.html)
- [SUMMER AESTHETICS](https://studyplayings.pages.dev/summer-aesthetics.html)
- [EASTER EGGVENTURE](https://studyplayings.web.app/easter-eggventure.html)
- [SHADOWMAN RUNNER](https://studyplayings.pages.dev/shadowman-runner.html)
- [OBBY SURVIVE PARKOUR](https://learnquester.pages.dev/obby-survive-parkour.html)
- [DUCKLINGS](https://learnquester.github.io/ducklings.html)
- [WORDMIX](https://thelearnquester.web.app/wordmix.html)
- [BUBBLE MERGE 2048](https://studyquesthub.web.app/bubble-merge-2048.html)
- [CATEGORY CASUAL 9](https://thelearnquesters.pages.dev/category-casual-9.html)
- [DUCKLINGS](https://quizverses.github.io/ducklings.html)
- [SISYPHUS SIMULATOR](https://studyquests.github.io/sisyphus-simulator.html)
- [CATEGORY RPG80](https://thelearnquesters.pages.dev/category-rpg80.html)
- [MERGE PLANETS](https://studyplayings.pages.dev/merge-planets.html)
- [CATEGORY MONSTER](https://thelearnquesters.pages.dev/category-monster.html)
- [CATEGORY RACING DRIVING 3](https://studyplaying.github.io/category-racing-driving-3.html)
- [CATEGORY TOOLS](https://thelearnquester.web.app/category-tools.html)
- [CATEGORY BIKE 3](https://thequizzone.pages.dev/category-bike-3.html)
- [BUBBLE SHOOTER GO](https://thelearnquesters.pages.dev/bubble-shooter-go.html)
- [ARCHERY MASTER BOW AND ARROW](https://quizverses-9d2f2.web.app/archery-master-bow-and-arrow.html)
- [BATTLE ISLAND 2](https://thelearnquester.web.app/battle-island-2.html)
- [FISHING THE RUSSIAN WAY](https://quizverses-9d2f2.web.app/fishing-the-russian-way.html)
- [PIN PUZZLE SAVE THE SHEEP](https://studyplayings.pages.dev/pin-puzzle-save-the-sheep.html)
- [PURRFECT SCOOPS](https://thelearnquesters.pages.dev/purrfect-scoops.html)
- [CATEGORY BATTLE524](https://thequizzone.pages.dev/category-battle524.html)
- [DTA BEST THIEF](https://studyquesthub.web.app/dta-best-thief.html)
- [JUMP UP 3D BASKETBALL GAME](https://thelearnquesters.pages.dev/jump-up-3d-basketball-game.html)
- [CATEGORY BUILDING179](https://studyquests.github.io/category-building179.html)
- [INDEX17](https://quizverses.github.io/index17.html)
- [CATEGORY CAR](https://thequizzone.pages.dev/category-car.html)
- [CATEGORY AIRPLANE29](https://thelearnquesters.pages.dev/category-airplane29.html)
- [CATEGORY SANDBOX41](https://thequizzone.pages.dev/category-sandbox41.html)
- [DUNGEON MASTER CULT CRAFT](https://thelearnquesters.pages.dev/dungeon-master-cult-craft.html)
- [COUNTRYSIDE DRIVING QUEST](https://learnquesters.pages.dev/countryside-driving-quest.html)
- [BILLYTHEBOX](https://thelearnquester.web.app/billythebox.html)
- [HIDDEN OBJECTS LOST ISLAND 2](https://learnquester.pages.dev/hidden-objects-lost-island-2.html)
- [MINI GRAND THEFT CITY](https://quizverses.github.io/mini-grand-theft-city.html)
- [CATEGORY GOGUARDIAN](https://quizverses-9d2f2.web.app/category-goguardian.html)
- [CATEGORY BLOCK94](https://thequizzone.pages.dev/category-block94.html)
- [TINY FIGHTER UNSTOPPABLE RUN](https://quizverses.github.io/tiny-fighter-unstoppable-run.html)
- [UNBLOCK BALL SLIDE PUZZLE](https://studyplayings.pages.dev/unblock-ball-slide-puzzle.html)
- [CATEGORY DRAGON](https://learnquesters.pages.dev/category-dragon.html)
- [ITALIAN ANIMALS CREATE YOUR OWN BRAINROT](https://studyquests.github.io/italian-animals-create-your-own-brainrot.html)
- [SEAFARING MEMORY CHALLENGE](https://thelearnquester.web.app/seafaring-memory-challenge.html)
- [THE EARTH EVOLUTION](https://learnquesters.pages.dev/the-earth-evolution.html)
- [CATEGORY AVOID](https://thequizzone.pages.dev/category-avoid.html)
- [FASHION STYLIST SALON MAKEOVER](https://studyplaying.github.io/fashion-stylist-salon-makeover.html)
- [MOON LEAGUE SPORTS SEASON](https://learnquester.github.io/moon-league-sports-season.html)
- [COLORSFORMS](https://studyquests.pages.dev/colorsforms.html)
- [CATEGORY PUZZLE 5](https://learnquester.github.io/category-puzzle-5.html)
- [NOOB IN GEOMETRY DASH](https://thelearnquesters.pages.dev/noob-in-geometry-dash.html)
- [CATEGORY TOWER DEFENSE 2](https://studyquests.github.io/category-tower-defense-2.html)
- [CANNONS BLAST 3D](https://studyquesthub.web.app/cannons-blast-3d.html)
- [CATEGORY PREMIUM PERKS74](https://thequizzone.pages.dev/category-premium-perks74.html)
- [FOOTBALL PENALTY 2026](https://studyquests.github.io/football-penalty-2026.html)
- [SWIPETOWN](https://quizverses.github.io/swipetown.html)
- [DEFORM IT](https://learnquester.github.io/deform-it.html)
- [CATEGORY CAN T STOP PLAYING212](https://quizverses.github.io/category-can-t-stop-playing212.html)
- [CATEGORY MOUSE1 707](https://thequizzone.pages.dev/category-mouse1-707.html)
- [HOME ISLAND](https://thelearnquesters.pages.dev/home-island.html)
- [IDLE BATHROOM EMPIRE TYCOON](https://quizverses.github.io/idle-bathroom-empire-tycoon.html)
- [CATEGORY PREMIUM PERKS71](https://quizverses.github.io/category-premium-perks71.html)
- [GRANNY GTA VEGAS](https://studyquests.pages.dev/granny-gta-vegas.html)
- [MAD TRUCK](https://studyquests.github.io/mad-truck.html)
- [UNSCREW WOOD PUZZLE](https://studyquesthub.web.app/unscrew-wood-puzzle.html)
- [RAGDOLL BOB PUZZLE](https://studyplayings.web.app/ragdoll-bob-puzzle.html)
- [MY FARM LIFE](https://quizverses-9d2f2.web.app/my-farm-life.html)
- [CATEGORY MAHJONG CONNECT](https://thequizzone.pages.dev/category-mahjong-connect.html)
- [INDEX12](https://thelearnquesters.pages.dev/index12.html)
- [FLOWER SHOP](https://learnquester.pages.dev/flower-shop.html)
