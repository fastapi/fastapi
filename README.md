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
- [CAT EVOLUTION 2](https://quizverses.github.io/cat-evolution-2.html)
- [INDEX33](https://quizverses.github.io/index33.html)
- [MEGA ESCAPE CAR PARKING PUZZLE](https://studyquesthub.web.app/mega-escape-car-parking-puzzle.html)
- [CATEGORY MERGE 2](https://themindzone.pages.dev/category-merge-2.html)
- [BLOSSOM](https://quizverses.pages.dev/blossom.html)
- [HIT BALL](https://studyquests.github.io/hit-ball.html)
- [FUNNY FRUITS MERGE AND GATHER WATERMELON](https://studyquests.pages.dev/funny-fruits-merge-and-gather-watermelon.html)
- [TERMS](https://cryptotify.github.io/terms.html)
- [MURDER CASE CLUE 3D](https://quizverses.pages.dev/murder-case-clue-3d.html)
- [WITCHY SISTERS RELAX PUZZLE](https://quizverses-9d2f2.web.app/witchy-sisters-relax-puzzle.html)
- [INDEX11](https://quizverses.pages.dev/index11.html)
- [BODY CARE SIMULATOR](https://quizverses.pages.dev/body-care-simulator.html)
- [ITALIAN BRAINROT CLICKER](https://studyquesthub.web.app/italian-brainrot-clicker.html)
- [CATEGORY SOCCER](https://studyquesthub.web.app/category-soccer.html)
- [TEACHER SIMULATOR](https://quizverses.pages.dev/teacher-simulator.html)
- [INDEX14](https://quizverses.pages.dev/index14.html)
- [STEAL A FISH](https://studyquests.github.io/steal-a-fish.html)
- [PRIVACY](https://cryptotify.web.app/privacy.html)
- [SMART DOTS RELOADED](https://quizverses.pages.dev/smart-dots-reloaded.html)
- [HAPPY GLASS GAME](https://quizverses.pages.dev/happy-glass-game.html)
- [DEADLY PARKOUR](https://learnquester.pages.dev/deadly-parkour.html)
- [CHRISTMAS SORTING](https://studyquests.github.io/christmas-sorting.html)
- [CATEGORY SIMULATION 3](https://studyplayings.web.app/category-simulation-3.html)
- [HOTEL MANAGER](https://studyplaying.github.io/hotel-manager.html)
- [SAVE HER TOUR](https://quizverses.pages.dev/save-her-tour.html)
- [COLOR CONQUEST TERRITORY WAR](https://quizverses.github.io/color-conquest-territory-war.html)
- [WINTER GIFTS](https://studyplaying.github.io/winter-gifts.html)
- [BURGER CAFE COOKING GAMES FOR KIDS](https://studyplaying.github.io/burger-cafe-cooking-games-for-kids.html)
- [DRILL QUEST](https://studyplaying.github.io/drill-quest.html)
- [CATEGORY COLLECT566](https://quizverses.github.io/category-collect566.html)
- [BARRY PRISON HIDE AND SEEK](https://studyquests.github.io/barry-prison-hide-and-seek.html)
- [BLOCK PARKOUR TRIALS](https://quizverses.github.io/block-parkour-trials.html)
- [CAPYBARA BLOCK DROP](https://learnquester.github.io/capybara-block-drop.html)
- [MATCH MASTER](https://studyplaying.github.io/match-master.html)
- [TYPE SPRINT](https://studyquests.github.io/type-sprint.html)
- [SURVIVAL ON RAFT MULTIPLAYER](https://studyquesthub.web.app/survival-on-raft-multiplayer.html)
- [SWORDEDIO SPIN AND RUB](https://studyquests.github.io/swordedio-spin-and-rub.html)
- [CATEGORY MINECRAFT81](https://studyplaying.github.io/category-minecraft81.html)
- [PACKING LINE](https://quizverses-9d2f2.web.app/packing-line.html)
- [OBBY POGO PARKOUR](https://quizverses.github.io/obby-pogo-parkour.html)
- [SPRING MAGIC ENCHANTED WARDROBE](https://studyplaying.github.io/spring-magic-enchanted-wardrobe.html)
- [CATEGORY UNBLOCKED](https://quizverses.pages.dev/category-unblocked.html)
- [CATEGORY CARTOON76](https://studyquesthub.web.app/category-cartoon76.html)
- [PLAYGROUND PARKOUR](https://studyquesthub.web.app/playground-parkour.html)
- [IS IT RIGHT](https://quizverses.pages.dev/is-it-right.html)
- [PANDA ADVENTURE](https://studyquests.github.io/panda-adventure.html)
- [PAPERWARIO](https://studyquests.github.io/paperwario.html)
- [CATEGORY RPG80](https://studyplaying.github.io/category-rpg80.html)
- [OVERTIDE IO](https://studyquests.github.io/overtide-io.html)
- [MY DOGY VIRTUAL PET](https://thelearnquester.web.app/my-dogy-virtual-pet.html)
- [HILL STATION BUS SIMULATOR](https://studyquests.github.io/hill-station-bus-simulator.html)
- [SUDOKU BRAIN BLOCKS](https://quizverses.github.io/sudoku-brain-blocks.html)
- [CATEGORY PUZZLE 8](https://studyplaying.github.io/category-puzzle-8.html)
- [CATEGORY BUBBLE SHOOTER27](https://studyquesthub.web.app/category-bubble-shooter27.html)
- [MARBLE PUZZLE QUEST](https://learnquester.github.io/marble-puzzle-quest.html)
- [DELICIOUS EMILYS NEW BEGINNING VALENTINES EDITION](https://quizverses.github.io/delicious-emilys-new-beginning-valentines-edition.html)
- [BUILD AND RUN](https://quizverses.pages.dev/build-and-run.html)
- [SLIDEE](https://learnquester.github.io/slidee.html)
- [RESCUE RIFT](https://studyquests.github.io/rescue-rift.html)
- [SAFE MERGE](https://learnquester.github.io/safe-merge.html)
- [SUPERMARKET CASHIER SIMULATOR](https://learnquester.github.io/supermarket-cashier-simulator.html)
- [SOLITAIRE DELUXE EDITION](https://studyplaying.github.io/solitaire-deluxe-edition.html)
- [CRAZYSTEVEIO](https://quizverses.github.io/crazysteveio.html)
- [BUBBLE MANIA SHOOTER](https://quizverses.github.io/bubble-mania-shooter.html)
- [DAILY CHESS PUZZLE](https://studyplayings.web.app/daily-chess-puzzle.html)
- [FAST LAP](https://studyplayings.web.app/fast-lap.html)
- [INDEX13](https://learnquester.github.io/index13.html)
- [CAT EVOLUTION](https://quizverses.pages.dev/cat-evolution.html)
- [ONET MONSTER BOOK](https://quizverses.pages.dev/onet-monster-book.html)
- [CATEGORY BATTLE524](https://thelearnquester.web.app/category-battle524.html)
- [UNICORN PRINCESS DRESS UP](https://quizverses-9d2f2.web.app/unicorn-princess-dress-up.html)
- [DEATH BALL](https://quizverses.github.io/death-ball.html)
- [CATEGORY CARDS](https://thelearnquester.web.app/category-cards.html)
- [CREEPY DRESS UP](https://learnquester.github.io/creepy-dress-up.html)
- [REAL FLIGHT SIMULATOR](https://quizverses.pages.dev/real-flight-simulator.html)
- [ART PUZZLE MASTER](https://studyplaying.github.io/art-puzzle-master.html)
- [YARN FEVER UNRAVEL PUZZLE](https://quizverses.github.io/yarn-fever-unravel-puzzle.html)
- [CATEGORY GOGUARDIAN](https://thelearnquester.web.app/category-goguardian.html)
- [TANK BATTLE WAR COMMANDER](https://studyplayings.pages.dev/tank-battle-war-commander.html)
- [PRIVACY](https://brainquests-fb2c5.web.app/privacy.html)
- [POWERWASH SIMULATOR 3D WASH](https://quizverses.github.io/powerwash-simulator-3d-wash.html)
- [DRAW BRIDGE CHALLENGE](https://quizverses.pages.dev/draw-bridge-challenge.html)
- [STICKMAN ZOMBIE VS STICKMAN HERO](https://learnquester.github.io/stickman-zombie-vs-stickman-hero.html)
- [SUV TRAFFIC RACER](https://studyquesthub.web.app/suv-traffic-racer.html)
- [CATEGORY COLOR197](https://thelearnquester.web.app/category-color197.html)
- [CATEGORY FASHION105](https://quizverses.github.io/category-fashion105.html)
- [LEGEND OF FIREBALL](https://learnquester.github.io/legend-of-fireball.html)
- [MONSTERELLA FANTASY MAKEUP](https://quizverses.github.io/monsterella-fantasy-makeup.html)
- [JETSTREAM ESCAPE](https://learnquester.github.io/jetstream-escape.html)
- [CHICKZ STACK](https://studyplayings.pages.dev/chickz-stack.html)
- [COLOR 3D BUMP IT UP](https://quizverses-9d2f2.web.app/color-3d-bump-it-up.html)
- [CATEGORY CONTROLLER](https://thelearnquester.web.app/category-controller.html)
- [ZOMBIE SURVIVAL](https://studyplayings.pages.dev/zombie-survival.html)
- [ITALIAN BRAINROT OBBY PARKOUR](https://studyquesthub.web.app/italian-brainrot-obby-parkour.html)
- [STACK TOWER PRO](https://learnquester.github.io/stack-tower-pro.html)
- [EVERYTHING IS IN PLACE RARE FINDS](https://learnquester.github.io/everything-is-in-place-rare-finds.html)
- [DOTS MASTER](https://studyplaying.github.io/dots-master.html)
- [CATEGORY CARTOON76](https://themindzone.pages.dev/category-cartoon76.html)
- [JUST DICE RANDOM TOWER DEFENCE](https://studyquesthub.web.app/just-dice-random-tower-defence.html)
- [DRAW TO SMASH ZOMBIE](https://thequizzone.pages.dev/draw-to-smash-zombie.html)
- [DRIVER MASTER SIMULATOR](https://quizverses.pages.dev/driver-master-simulator.html)
- [COE SNAKE](https://themindplays.pages.dev/coe-snake.html)
- [GT DRIFT MOST WANTED](https://studyquests.github.io/gt-drift-most-wanted.html)
- [PYRAMIDZ2](https://thelearnquesters.pages.dev/pyramidz2.html)
- [SWEET MATCH](https://thelearnquesters.pages.dev/sweet-match.html)
- [SISYPHUS SIMULATOR](https://themindzone.pages.dev/sisyphus-simulator.html)
- [PRIVACY](https://brainquests.onrender.com/privacy.html)
- [HYDRO RACING 3D](https://quizverses.pages.dev/hydro-racing-3d.html)
- [MERGE PIXEL](https://themindzone.pages.dev/merge-pixel.html)
- [GRANNY 2 ASYLUM HORROR HOUSE](https://themindzone.pages.dev/granny-2-asylum-horror-house.html)
- [SQUID GAME PLAYGROUND SHOOTER](https://thelearnquesters.pages.dev/squid-game-playground-shooter.html)
- [PET TILE MASTER](https://studyplayings.pages.dev/pet-tile-master.html)
- [MAGIC KINGDOM HEX MATCH](https://themindzone.pages.dev/magic-kingdom-hex-match.html)
- [CATEGORY SIMULATION 4](https://iskillquest.pages.dev/category-simulation-4.html)
- [CATEGORY CASUAL 14](https://thequizzone.pages.dev/category-casual-14.html)
- [CATEGORY COLOR197](https://thequizzone.pages.dev/category-color197.html)
- [CATEGORY CLASSIC98](https://thelearnquester.web.app/category-classic98.html)
- [INDEX27](https://iskillquest.pages.dev/index27.html)
- [FROG KNIGHT](https://themindzone.pages.dev/frog-knight.html)
- [CATEGORY CONTROLLER 3](https://thequizzone.pages.dev/category-controller-3.html)
- [CATEGORY FPS 2](https://iskillquest.pages.dev/category-fps-2.html)
- [CATEGORY FPS](https://studyquesthub.web.app/category-fps.html)
- [RIDE SHOOTER](https://learnquester.github.io/ride-shooter.html)
- [3D KID SLIDING PUZZLE](https://thequizzone.pages.dev/3d-kid-sliding-puzzle.html)
- [LET THE TRAIN GO](https://theskillquest.pages.dev/let-the-train-go.html)
- [CATEGORY FREE RAGDOLL GAMES](https://thelearnquesters.pages.dev/category-free-ragdoll-games.html)
- [COOKIE MONSTER](https://themindzone.pages.dev/cookie-monster.html)
- [IDLE DAIRY FARM TYCOON](https://theskillquest.pages.dev/idle-dairy-farm-tycoon.html)
- [FOREST GLADE MYSTERIES](https://quizverses.github.io/forest-glade-mysteries.html)
- [STICK HERO BATTLE](https://themindzone.pages.dev/stick-hero-battle.html)
