# Parametri di percorso

È possibile dichiarare i <abbr title="path parameters">"parametri di percorso"</abbr> o le "variabili" con la stessa sintassi usata nelle <abbr title="format strings">*stringhe formattatrici*</abbr> di Python:

```Python hl_lines="6 7"
{!../../../docs_src/path_params/tutorial001.py!}
```

Il valore del parametro di percorso `item_id` verrà passato alla tua funzione sotto forma dell'argomento `item_id`.

Quindi, se esegui questo esempio e vai su <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vedrai la seguente risposta:

```JSON
{"item_id":"foo"}
```

## Path parameters con tipi

Puoi dichiarare il tipo di un parametro di percorso nella funzione usando le annotazioni di tipo *standard* di Python:

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

In questo caso, `item_id` è dichiarato come un <abbr title="numero intero">`int`</abbr>.

!!! check
    Questo permetterà all'editor di testo di aiutarti dentro la tua funzione, con di eventuali errori, autocompletamento, ecc.

## <abbr title="anche nota come: serializzazione, parsing, marshalling">Conversione</abbr> dei dati

Se esegui questo esempio e apri il browser su <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, vedrai la seguente risposta:

```JSON
{"item_id":3}
```

!!! check
    Nota che il valore ricevuto (e restituito) dalla tua funzione è `3`, un `int`, non una stringa `"3"`.

    Di conseguenza, con quella dichiarazione di tipo, **FastAPI** ti dà *automatic request <abbr title="convertire la stringa che proviene da una richiesta HTTP in dati Python">"parsing"</abbr>*.

## Validazione dei dati

Se vai con il tuo browser su <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, vedrai il seguente errore HTTP:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

perché il parametro di percorso `item_id` ha il valore `"foo"`, che non è un `int`.

Lo stesso errore si sarebbe presentato se avessi passato un `float` invece che un int, per esempio con: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check
    Abbiamo visto che con la semplice dichiarazione di tipo in Python, **FastAPI** è in grado di validare i dati.

    Nota che l'errore ti fa anche vedere esattamente il punto in cui la validazione è fallita.

    Questo è incredibilmente utile durante lo sviluppo e il debug del codice che interagisce con le API.

## Documentazione

E quando si apre il browser a <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, vedrai una documentazione dell'API automatica e interattiva come questa:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-params/image01.png">

!!! check
    Anche in questo caso, proprio con la stessa dichiarazione di tipo Python, **FastAPI** fornisce una documentazione automatica e interattiva (integrando Swagger UI).

    Si noti che il parametro di percorso è dichiarato come un numero intero.

## Vantaggi basati sugli standard, documentazione alternativa

E poiché lo schema generato è dello standard <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" class="external-link" target="_blank">OpenAPI</a>, ci sono molti strumenti compatibili.

Per questo motivo, **FastAPI** fornisce una documentazione API alternativa (utilizzando ReDoc), alla quale si può accedere all'indirizzo <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-params/image02.png">

Allo stesso modo, ci sono molti strumenti compatibili. Inclusi gli strumenti per la generazione di codice per molti linguaggi di programmazione.

## Pydantic

La convalida di tutti i dati viene eseguita dietro le quinte da <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>.

È possibile utilizzare lo stesso tipo di dichiarazione con `str`, `float`, `bool` e molti altri tipi di dati complessi.

Molti di questi sono esaminati nei prossimi capitoli del tutorial.

## L'ordine ha importanza

Quando si creano *path operations*, si possono trovare situazioni in cui si ha un percorso fisso.

Supponiamo che il percorso `/users/me` serva per ottenere dati sull'utente corrente.

E poi abbiamo anche un percorso `/users/{user_id}` per ottenere i dati di un utente dato il suo ID.

Poiché le *path operations* sono valutate in ordine, è necessario assicurarsi che il percorso `/users/me` sia dichiarato prima di `/users/{user_id}`:

```Python hl_lines="6 11"
{!../../../docs_src/path_params/tutorial003.py!}
```

Altrimenti, il percorso `/users/{user_id}`, che è simile a quello `/users/me`, "penserebbe" di ricevere un parametro `user_id` con valore `"me"`.

## Valori predefiniti

Se hai una *path operation* che riceve un parametro di percorso, e vorresti definire i possibili valori che il parametro di percorso può accettare, puoi usare un <abbr title="Enumerazione, in inglese enumeration">`Enum`</abbr>.

### Crea una classe `Enum`

Importa `Enum` e crea una sottoclasse che eredita da `str` e da `Enum`.

Ereditando da `str` la documentazione dell'API sarà in grado di desumere che i valori devono essere di tipo `string` e sarà in grado di funzionare correttamente.

Poi, definisci degli attributi di classe con valori fissi, che saranno i valori validi disponibili:

```Python hl_lines="1 6 7 8 9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info
    Gli <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">enumeratori (o enums) sono disponibili in Python</a> dalla versione 3.4.

!!! tip
    Se te lo stai chiedendo, "AlexNet", "ResNet", e "LeNet" sono semplicemente i nomi di <abbr title="Technically, Deep Learning model architectures">modelli</abbr> di Machine Learning.

### Dichiara un parametro di percorso

Successivamente, crea un parametro di percorso con un'annotazione di tipo usando la classe enum che hai creato (`ModelName`):

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Controlla la documentazione

Poiché i valori disponibili per il parametro di percorso sono predefiniti, la documentazione interattiva è in grado di mostrarli bene:

<img src="https://fastapi.tiangolo.com/img/tutorial/path-params/image03.png">

### Lavorare con le *enumerazioni* di Python

Il valore del parametro di percorso sarà un <abbr title="In inglese: enumeration member">*membro dell'enumerazione*</abbr>.

#### Compara i *membri dell'enumerazione*

Puoi compararlo con i membri dell'enumerazione definiti all'interno di `ModelName`:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### Ottieni il *valore dell'enumerazione*

Puoi ottenere il valore dell'enumerazione (una `str` in questo caso) usando `model_name.value`, o in generale, `your_enum_member.value`:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip
    È possibile accedere al valore `"lenet"` con `ModelName.lenet.value`.

#### Restituisci i *membri dell'enumerazione*

Puoi restituire i membri dell'enumerazione dal tuo *path operation*, persino nidificati in una struttura JSON (per esempio un `dict`).

Saranno convertiti nei loro valori corrispondenti (stringhe in questo caso) prima di essere restituiti al client:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

Nel tuo client riceverai una risposta JSON come questa:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Path parameters containing paths

Let's say you have a *path operation* with a path `/files/{file_path}`.

But you need `file_path` itself to contain a *path*, like `home/johndoe/myfile.txt`.

So, the URL for that file would be something like: `/files/home/johndoe/myfile.txt`.

### OpenAPI support

OpenAPI doesn't support a way to declare a *path parameter* to contain a *path* inside, as that could lead to scenarios that are difficult to test and define.

Nevertheless, you can still do it in **FastAPI**, using one of the internal tools from Starlette.

And the docs would still work, although not adding any documentation telling that the parameter should contain a path.

### Path convertor

Using an option directly from Starlette you can declare a *path parameter* containing a *path* using a URL like:

```
/files/{file_path:path}
```

In this case, the name of the parameter is `file_path`, and the last part, `:path`, tells it that the parameter should match any *path*.

So, you can use it with:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip
    You could need the parameter to contain `/home/johndoe/myfile.txt`, with a leading slash (`/`).

    In that case, the URL would be: `/files//home/johndoe/myfile.txt`, with a double slash (`//`) between `files` and `home`.

## Recap

With **FastAPI**, by using short, intuitive and standard Python type declarations, you get:

* Editor support: error checks, autocompletion, etc.
* Data "<abbr title="converting the string that comes from an HTTP request into Python data">parsing</abbr>"
* Data validation
* API annotation and automatic documentation

And you only have to declare them once.

That's probably the main visible advantage of **FastAPI** compared to alternative frameworks (apart from the raw performance).
