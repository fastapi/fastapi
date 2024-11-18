# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>Framework FastAPI, alt rendiment, fàcil d'aprendre, ràpid de programar, preparat per a producció</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/fastapi/fastapi/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/fastapi/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/fastapi/fastapi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentació**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Codi Font**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---
FastAPI és un framework web modern i ràpid (d’alt rendiment) per construir APIs amb Python, basat en les anotacions de tipus estàndard de Python.

Les seves característiques principals són:

* **Rapidesa**: Alt rendiment, comparable amb **NodeJS** i **Go** (gràcies a Starlette i Pydantic). [Un dels frameworks de Python més ràpids](#rendiment).

* **Ràpid de programar**: Incrementa la velocitat de desenvolupament entre un 200% i un 300%. *
* **Menys errors**: Redueix els errors humans (de programador) aproximadament un 40%.*
* **Intuïtiu**: Gran suport als editors amb <abbr title="conegut en anglès com auto-complete, autocompletion, IntelliSense, completion">autocompletat</abbr> a tot arreu. Es perd menys temps <abbr title="cercant i corregint errors">depanant</abbr>.
* **Fàcil**: Està dissenyat per ser fàcil d'utilitzar i d'aprendre, dedicant menys temps a llegir documentació.
* **Curt**: Minimitza la duplicació de codi. Múltiples funcionalitats amb cada declaració de paràmetres. Menys errors.
* **Robust**: Crea codi preparat per a producció amb documentació automàtica i interactiva.
* **Basat en estàndards**: Basat i totalment compatible amb els estàndards oberts per a APIs: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (anteriorment conegut com Swagger) i <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* Aquesta estimació està basada en proves amb un equip de desenvolupament intern construint aplicacions preparades per a producció.</small>

## Sponsors

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

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Altres patrocinadors</a>

## Opinions

"_[...] I'm using **FastAPI** a ton these days. [...] I'm actually planning to use it for all of my team's **ML services at Microsoft**. Some of them are getting integrated into the core **Windows** product and some **Office** products._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_We adopted the **FastAPI** library to spawn a **REST** server that can be queried to obtain **predictions**. [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** is pleased to announce the open-source release of our **crisis management** orchestration framework: **Dispatch**! [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_I’m over the moon excited about **FastAPI**. It’s so fun!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Honestly, what you've built looks super solid and polished. In many ways, it's what I wanted **Hug** to be - it's really inspiring to see someone build that._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_If you're looking to learn one **modern framework** for building REST APIs, check out **FastAPI** [...] It's fast, easy to use and easy to learn [...]_"

"_We've switched over to **FastAPI** for our **APIs** [...] I think you'll like it [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, el FastAPI de les CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Si estàs construint una aplicació de <abbr title="Interfície de línia de comandes">CLI</abbr> per ser utilitzada al terminal en comptes d'una API web, fes un cop d'ull a <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

**Typer** és el germà petit de FastAPI. Està dissenyat per ser el **FastAPI de les CLIs**. ⌨️ 🚀

## Requisits

FastAPI es basa en les espatlles de gegants:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> per a les parts web.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> per a les parts de dades.

## Instal·lació

Crea i activa un <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">entorn virtual</a> i després instal·la FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Nota**: Assegura't de posar `"fastapi[standard]"` ntre cometes per garantir que funcioni en tots els terminals.

## Exemple

### Crea-ho

* Crea un fitxer `main.py` amb:

```Python
from fastapi import FastAPI
from typing import Union

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>O utilitzar <code>async def</code>...</summary>

Si el teu codi utilitza `async` / `await`, fes servir `async def`:

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

Si no ho saps, revisa la secció "Amb pressa?" sobre <a href="https://fastapi.tiangolo.com/ca/async/#con-prisa" target="_blank">async i await a la documentació</a>.

</details>

### Executa-ho

Executa el servidor amb:

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
<summary>Sobre l'ordre <code>fastapi dev main.py</code>...</summary>

L'ordre `fastapi dev` llegeix el teu fitxer `main.py`, detecta l'aplicació **FastAPI** que hi ha i inicia un servidor utilitzant <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Per defecte, `fastapi dev` s'iniciarà amb l'auto-reload habilitat per al desenvolupament local.

Pots llegir més sobre això a la <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">documentació de la CLI de FastAPI</a>.

</details>

### Revisa-ho

Obre el teu navegador a <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Veuràs la resposta en format JSON com:

```JSON
{"item_id": 5, "q": "somequery"}
```

Ja has creat una API que:

* Rep sol·licituds HTTP en els _paths_ `/` i `/items/{item_id}`.
* Ambdós _paths_ accepten <em>operacions</em> `GET` (també conegudes com a _methods_ HTTP).
* El _path_ `/items/{item_id}` té un _path parameter_ `item_id` que hauria de ser un `int`.
* El _path_ `/items/{item_id}` té un _query parameter_ `q` opcional de tipus `str`.

### Documentació interactiva de l'API

Ara ves a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Veureu la documentació automàtica i interactiva de l'API (proporcionada per <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentació alternativa de l'API

Ara ves a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Ara veuràs la documentació automàtica alternativa (proporcionada per <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Millora de l'exemple

Ara modifica el fitxer `main.py` per rebre un body d'una sol·licitud `PUT`.

Declara el body utilitzant tipus estàndard de Python, gràcies a Pydantic.

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

El servidor `fastapi dev` hauria de recarregar-se automàticament.

### Actualització de documents de l'API interactiva

Ara ves a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* La documentació interactiva de l'API s'actualitzarà automàticament, incloent-hi el nou body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Fes clic al botó "Try it out", que et permet omplir els paràmetres i interactuar directament amb l'API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Després, fes clic al botó "Execute". La interfície d'usuari es comunicarà amb la teva API, enviarà els paràmetres, obtindrà els resultats i els mostrarà a la pantalla:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Actualització de la documentació alternativa de l'API

I ara, ves a <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* La documentació alternativa també reflectirà el nou paràmetre de consulta i el body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Resum

En resum, declares **una sola vegada** els tipus de paràmetres, body, etc., com a paràmetres de funció.

Ho fas amb tipus moderns estàndard de Python.

No necessites aprendre una nova sintaxi, ni els mètodes o classes d’una biblioteca específica, etc.

Només **Python** estàndard.

Per exemple, per un `int`:

```Python
item_id: int
```

o per a un model més complex com `Item`

```Python
item: Item
```

...i amb aquesta única declaració obtens:

* Suport de l'editor, incloent:
    * Autocompletat.
    * Comprovacions de tipus.
* Validació de dades:
    * Errors automàtics i clars quan les dades són invàlides.
    * Validació fins i tot per a objectes JSON profundament imbricats.
* <abbr title="també conegut com: serialització, parsing, marshalling">Conversió</abbr> de dades d'entrada: des de la xarxa fins a dades i tipus de Python. Llegint de:
    * JSON.
    * Paràmetres de path.
    * Paràmetres de consulta.
    * Cookies.
    * Headers.
    * Formularis.
    * Fitxers.
* <abbr title="també conegut com: serialització, parsing, marshalling">Conversió</abbr> de dades de sortida: convertint de dades i tipus de Python a dades de xarxa (com JSON):
    * Converteix tipus de Python (`str`, `int`, `float`, `bool`, `list`, etc).
    * Objectes `datetime`.
    * Objectes `UUID`.
    * Models de bases de dades.
    * ...i molts més.
* Documentació automàtica i interactiva de l'API, incloent 2 interfícies d'usuari alternatives:
    * Swagger UI.
    * ReDoc.

---

Tornant a l'exemple de codi anterior, **FastAPI** farà el següent:

* Validarà que hi ha un `item_id`  al path per a les sol·licituds `GET` i `PUT`.
* Validarà que el `item_id` és de tipus `int` per a les sol·licituds `GET` i `PUT`.
    * Si no ho és, el client veurà un error clar i útil.
* Comprovarà si hi ha un paràmetre de consulta opcional anomenat `q` (com en `http://127.0.0.1:8000/items/foo?q=somequery`) per a les sol·licituds `GET`.
    * Com que el paràmetre `q` està declarat amb `= None` és opcional.
    * Sense el `None` seria obligatori (com ho és el body en el cas de `PUT`).
* Per a les sol·licituds `PUT` a `/items/{item_id}` llegirà el body com JSON:
    * Comprovarà que té un atribut requerit `name`que ha de ser un `str`.
    * Comprovarà que té un atribut requerit `price` que ha de ser un `float`.
    * Comprovarà que té un atribut opcional `is_offer`, que ha de ser un `bool`si està present.
    * Tot això també funcionaria per a objectes JSON profundament imbricats.
* Convertirà automàticament de i cap a JSON.
* Documentarà tot amb OpenAPI, que pot ser utilitzat per:
    * Sistemes de documentació interactiva.
    * Sistemes de generació automàtica de codi client, per a molts llenguatges.
* Proporcionarà directament 2 interfícies web de documentació interactiva.

---

Només hem començat a gratar la superfície, però ja tens una idea de com funciona tot plegat.

Prova de canviar la línia amb:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...de:

```Python
        ... "item_name": item.name ...
```

...a:

```Python
        ... "item_price": item.price ...
```

...i observa com el teu editor autocompletarà els atributs i reconeixerà els seus tipus:

![soporte de editor](https://fastapi.tiangolo.com/img/vscode-completion.png)

Per a un exemple més complet que inclogui més funcionalitats, consulta el <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - Guia d'Usuari</a>.

**Spoiler alert**: el tutorial - guia d'usuari inclou:

Declaració de **paràmetres** des de diferents llocs com: **headers**, **cookies**, **camps de formulari** i **fitxers**.
* Com establir **restriccions de validació** com `maximum_length` o `regex`.
* Un sistema de <abbr title="també conegut com components, recursos, proveïdors, serveis, injectables">Dependency Injection</abbr> molt potent i fàcil d'utilitzar.
* Seguretat i autenticació, incloent suport per a **OAuth2** amb **JWT tokens** i **HTTP Basic** auth.
* Tècniques més avançades (però igualment fàcils) per declarar **models JSON profundament imbricats** (gràcies a Pydantic).
* Integració amb **GraphQL** utilitzant <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> i altres biblioteques.
* Moltes funcionalitats extres (gràcies a Starlette) com:
    * **WebSockets**
    * proves extremadament fàcils basades en HTTPX i `pytest`
    * **CORS**
    * **Sessions amb Cookies**
    * ...i molt més.

## Rendiment

Els benchmarks independents de TechEmpower mostren que les aplicacions de FastAPI executades amb Uvicorn són <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">un dels frameworks de Python més ràpids disponibles</a>, només per darrere de Starlette i Uvicorn (utilitzats internament per FastAPI). (*)

Per entendre'n més, consulta la secció <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Dependències

FastAPI depèn de Pydantic i Starlette.

### Dependències `standard`

Quan instal·les FastAPI amb `pip install "fastapi[standard]"`, inclou el grup de dependències opcionals `standard`:

Utilitzat per Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - per a la validació de correus electrònics.

Utilitzat per Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Necessari si vols utilitzar el `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Necessari si vols utilitzar la configuració de plantilles per defecte.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Necessari si vols donar suport al <abbr title="convertir la cadena que prové d'una sol·licitud HTTP en dades de Python">"parsing"</abbr> de formularis, amb `request.form()`.

Utilitzat per FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - per al servidor que carrega i serveix la teva aplicació. Això inclou `uvicorn[standard]`, que inclou algunes dependències (per exemple, `uvloop`) necessàries per a un servei d'alt rendiment.
* `fastapi-cli` - per proporcionar l'ordre `fastapi`.

### Sense les dependències `standard`

Si no vols incloure les dependències opcionals `standard`, pots instal·lar amb `pip install fastapi` en lloc de `pip install "fastapi[standard]"`.

### Dependències opcionals addicionals

Hi ha algunes dependències addicionals que podries voler instal·lar.

Dependències opcionals addicionals de Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - per a la gestió de configuracions.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - per a tipus addicionals que es poden utilitzar amb Pydantic.

Dependències opcionals addicionals de FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Necessari si vols utilitzar `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Necessari si vols utilitzar `UJSONResponse`.

## Llicència

Aquest projecte està llicenciat sota els termes de la llicència MIT.
