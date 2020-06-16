# Primi Passi

Il più semplice script con FastAPI potrebbe essere questo:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Copialo in un file chiamato `main.py`.

Carica il programma su un server:

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

!!! nota
    Vediamo in dettaglio il comando `uvicorn main:app`:

    * `main`: il file `main.py` (il "modulo" Python).
    * `app`: l'oggetto creato all'interno di `main.py` con la riga `app = FastAPI()`.
    * `--reload`: riavvia il server automaticamente ad ogni modifica del codice. Usalo solo durante il sviluppo.

Nell'output c'è questa riga:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

La riga mostra l'URL dove è disponibile la tua app sulla tua macchina.

### Testalo

Apri il browser all'indirizzo <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Vedrai la seguente risposta JSON:

```JSON
{"message": "Hello World"}
```

### Documentazione API interattiva

Adesso vai su <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vedrai la documentazione dell'API interattiva generata automaticamente (offerta da <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentazione API interattiva alternativa

Adesso vai su <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vedrai una documentazione dell'API alternativa (offerta da <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** genera uno "schema" con la tua API usando lo standard **OpenAPI** standard per definire le API.

#### "Schema"

Uno "schema" è la definizione o descrizione di qualcosa. Non si tratta della descrizione del codice, è qualcosa di più astratto.

####"Schema" dell'API

In questo caso, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> è la specifica che stabilisce come definire lo schema della tua API.

La definizione di questo schema riguarda anche i percorsi dell'API, i possibili parametri che possono accettare, e così via.

#### Lo "schema" dei dati

Il termine "schema" potrebbe anche riguardare la struttura di certi dati, come i contenuti JSON.

In quel caso, potrebbe riguardare gli attributi JSON, e i loro tipi di valori, ecc.

#### Schema OpenAPI e JSON

OpenAPI definisce uno schema per la tua API. E quello schema include le definizioni (o "schemas") dei dati inviati e ricevuti dalla tua API usando lo **Schema JSON**, lo standard per gli schemi JSON.

#### Controlla `openapi.json`

Se sei curioso dello schema OpenAPI, FastAPI genera automaticamente un file JSON (lo "schema") con una descrizione di tutte le tue API.

Lo puoi vedere al seguente indirizzo: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Vedrai un file JSON che inizia circa così:

```JSON
{
    "openapi": "3.0.2",
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

#### A cosa serve OpenAPI

Lo schema OpenAPI è ciò su cui sono basati i due sistemi di documentazione interattiva inclusi.

E ci sono dozzine di alternative, tutte basate su OpenAPI. È facile adattare una qualsiasi alternativa alla tua applicazione con **FastAPI**.

Puoi anche usare lo schema OpenAPI per generare il codice automaticamente per i client che comunicano con la tua API. Per esempio, le applicazioni web, mobile o IoT.

## Riassumendo, passo a passo

### Passo 1: import `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` è una classe in Python che ti fornisce tutto quello che serve per progettare la tua API.

!!! note "Dettagli Tecnici"
    `FastAPI` è una classe che eredita direttamente da `Starlette`.

    Puoi usare tutte le funzionalità di <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> anche con `FastAPI`.

### Passo 2: crea una "istanza" di `FastAPI`

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Qui la variabile `app` è una "istanza" della classe `FastAPI`.

Useremo questa variabile per creare l'API.

Questa `app` è la stessa che abbiamo specificato con il comando `uvicorn`:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Se crei un'app in questo modo:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

E aggiori il file `main.py`, allora dovresti chiamare `uvicorn` così:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Passo 3: crea un *path operation*

#### Path

Qui <abbr title="in italiano: percorso">"path"</abbr> si riferisce all'ultima parte di un URL che inizia con `/`.

Quindi, in questo URL:

```
https://example.com/items/foo
```

...il path è:

```
/items/foo
```

!!! info
    Un "path" è anche comunemente chiamato "endpoint" o "route".

Quando progetti una API, il "path" è il modo principale per separare "concerns" e "resources".

#### Operation

Qui "operation" si riferisce a uno dei <abbr title="in italiano: metodi HTTP">"HTTP methods"</abbr>.

Per esempio:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...ma anche:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Con il protocollo HTTP, puoi comunicare a ogni path usando uno (o più) di questi "methods".

---

Quando progetti API, normalmente puoi usare uno dei HTTP methods per compiere una certa azione.

Normalmente si usa:

* `POST`: per creare dati.
* `GET`: per leggere dati.
* `PUT`: per aggiornare dati.
* `DELETE`: per eliminare dati.

Quindi, in OpenAPI, ogni metodo HTTP è chiamato "operation".

Li andremo a chiamare "**operations**".

#### Definisci un *path operation decorator*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` dice a **FastAPI** that the function right below is in charge of handling requests that go to:

* il percorso `/`
* using a <abbr title="an HTTP GET method"><code>get</code> operation</abbr>

!!! info "`@decorator` Info"
    That `@something` syntax in Python is called a "decorator".

    You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

    A "decorator" takes the function below and does something with it.

    In our case, this decorator tells **FastAPI** that the function below corresponds to the **path** `/` with an **operation** `get`.

    It is the "**path operation decorator**".

You can also use the other operations:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

And the more exotic ones:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    You are free to use each operation (HTTP method) as you wish.

    **FastAPI** doesn't enforce any specific meaning.

    The information here is presented as a guideline, not a requirement.

    For example, when using GraphQL you normally perform all the actions using only `POST` operations.

### Step 4: define the **path operation function**

This is our "**path operation function**":

* **path**: is `/`.
* **operation**: is `get`.
* **function**: is the function below the "decorator" (below `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Questa è una funzione Python.

It will be called by **FastAPI** whenever it receives a request to the URL "`/`" using a `GET` operation.

In questo caso, è una funzione `async`.

---

You could also define it as a normal function instead of `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! Suggerimento
    Se non sai quale sia la differenza, consulta [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Passo 5: return the content

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

You can return a `dict`, `list`, singular values as `str`, `int`, etc.

You can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using your favorite ones, it's highly probable that they are already supported.

## Riassumendo

* Importa `FastAPI`.
* Crea un'istanza `app`.
* Scrivi un **path operation decorator** (come `@app.get("/")`).
* Scrivi una **path operation function** (come `def root(): ...` sopra).
* Esegui il server di sviluppo (per esempio con `uvicorn main:app --reload`).
