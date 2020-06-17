# Primi Passi

Il più semplice file con FastAPI potrebbe essere questo:

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
    * `--reload`: riavvia il server automaticamente ad ogni modifica del codice. Usalo solo durante la fase di sviluppo.

Nell'output c'è questa riga:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

La riga mostra l'URL dove è ospitata localmente la tua app sulla tua macchina.

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

**FastAPI** genera uno "schema" della tua API usando **OpenAPI**, standard per definire le API.

#### "Schema"

Uno "schema" è la definizione o descrizione di qualcosa. Non si tratta della descrizione del codice, è qualcosa di più astratto.

####"Schema" dell'API

In questo caso, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> è la specifica che stabilisce come definire lo schema della tua API.

La definizione di questo schema riguarda anche i percorsi dell'API, i possibili parametri che possono accettare, e così via.

#### Lo "schema" dei dati

Il termine "schema" potrebbe anche riguardare la struttura di certi dati, come i contenuti JSON.

In quel caso, potrebbe riguardare gli attributi JSON, e i tipi dei loro valori, ecc.

#### Schema OpenAPI e JSON

OpenAPI definisce uno schema per la tua API. E questo schema include le definizioni (o "schemas") dei dati inviati e ricevuti dalla tua API usando lo **Schema JSON**, lo standard per gli schemi JSON.

#### Controlla `openapi.json`

Se sei curioso dello schema OpenAPI, FastAPI genera automaticamente un file JSON (lo "schema") con una descrizione di tutte le tue API.

Lo puoi trovare al seguente indirizzo: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

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

Lo schema OpenAPI è ciò su cui sono basati i due sistemi di documentazione interattiva adottati dal framework.

E ci sono dozzine di alternative, tutte basate su OpenAPI. È facile adattare una qualsiasi alternativa alla tua applicazione con **FastAPI**.

Puoi anche usare lo schema OpenAPI per generare il codice automaticamente per i client che comunicano con la tua API. Per esempio, le applicazioni web, mobile o IoT.

## Ricapitolando, passo dopo passo

### Passo 1: import `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` è una classe in Python che ti fornisce tutto quello che serve per progettare la tua API.

!!! note "Dettagli Tecnici"
    `FastAPI` è una classe che eredita direttamente da `Starlette`.

    Puoi quindi usare tutte le funzionalità di <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> anche con `FastAPI`.

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

Quindi, se crei un'app così:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

E aggiori il file `main.py`, allora dovresti chiamare `uvicorn` in questo modo:

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

Con il protocollo HTTP puoi comunicare con ogni path usando uno (o più) di questi "methods".

---

Quando progetti API, normalmente puoi usare uno dei metodi HTTP per portare a termine una determinata azione.

Normalmente si usa:

* `POST`: per creare dati.
* `GET`: per leggere dati.
* `PUT`: per aggiornare dati.
* `DELETE`: per eliminare dati.

Quindi, all'interno di OpenAPI, ogni metodo HTTP è chiamato "operation".

Li andremo a chiamare "**operations**".

#### Definisci un *path operation decorator*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` dice a **FastAPI** che la funzione sottostante è resposabile delle richieste che:

* specificano il percorso `/`
* usano una <abbr title="un metodo HTTP GET"><code>get</code> operation</abbr>

!!! info "`@decorator` Info"
    La sintassi `@something` in Python è chiamata <abbr title="in italiano: decoratore">"decorator"</abbr>.

    La metti sopra una funzione. Come se fosse un bel cappellino di decorazione (forse è da lì che proviene il nome).

    Un "decorator" prende la funzione sottostante e la usa per farci qualcosa.

    Nel nostor caso, questo decoratore dice a **FastAPI** che la funzione sottostante corrisponde al path **path** `/` con una **operation** `get`.

    È quindi il "**path operation decorator**".

Puoi anche usare altre operazioni:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

E anche queste meno comuni:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    Sei libero di una usare qualsiasi operazione (metodo HTTP).

    **FastAPI** doesn't enforce any specific meaning.

    Le informazioni qui sono presentate come linee guida, non come requisiti specifici.

    Per esempio, quando usi GraphQL normalmente esegue tutte le azioni usando solo operazioni `POST`.

### Passo 4: definisci la **path operation function**

Questa è la nostra "**path operation function**":

* **path**: is `/`.
* **operation**: is `get`.
* **function**: is the function below the "decorator" (below `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Questa è una funzione Python.

Sarà chiamata da **FastAPI** ogni volta che riceverà la richiesta all'URL "`/`" usando un'operazione `GET`.

In questo caso, è una funzione `async`.

---

Puoi anche definirla come una funzione normale usando `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! Suggerimento
    Se non sai quale sia la differenza, consulta [Async: *"In a hurry?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

### Passo 5: return the content

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Puoi restituire un `dict`, `list`, valori singoli come `str`, `int`, ecc.

Puoi anche restituire i modelli Pydantic (li vedremo tra poco).

Ci sono anche tanti altri oggetti e modelli che saranno automaticamente convertiti in JSON (inclusi gli ORM, ecc). Prova a usare i tuoi oggetti preferiti, è molto probabile che saranno supportati.

## Ricapitolando

* Importa `FastAPI`.
* Crea un'istanza `app`.
* Scrivi un **path operation decorator** (come `@app.get("/")`).
* Scrivi una **path operation function** (come `def root(): ...` sopra).
* Esegui il server di sviluppo (per esempio con `uvicorn main:app --reload`).
