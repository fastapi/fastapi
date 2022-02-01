# Introduzione ai Tipi in Python

**Python 3.6+** supporta opzionalmente i <abbr title="anche chiamati annotazioni di tipo">"type hints"</abbr>.

I **"type hints"** sono una nuova sintassi (introdotta in Python 3.6+) che permette di dichiarare il <abbr title="per esempio: str, int, float, bool">tipo</abbr> di una variabile.

Dichiarando i tipi delle tue variabili, gli editor di testo e altri strumenti possono darti una mano con il tuo lavoro di sviluppo.

Questo è solo un **breve tutorial / ripasso** sui *type hints* di Python. Copre solamente il minimo necessario per imparare ad usarli con **FastAPI**... Quindi molto poco.

**FastAPI** è interamente basato sui *type hints* per i numerosi vantaggi che essi offrono.

Ma anche se non hai mai usato o mai userai **FastAPI**, ti sarà utile capire cosa siano.

!!! nota
    Se sei un esperto di Python, e quindi saprai tutto sui *type hints*, puoi passare al capitolo successivo.

## Motivazione 

Iniziamo con un semplice esempio:

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

Il risultato di questo programma è il seguente:

```
John Doe
```

La funzione fa questo:

* Prende `first_name` e `last_name`.
* Converte la prima lettera di entrambi in maiuscolo con `title()`.
* Li <abbr title="Li unisce in una singola entità. Inserisce prima i contenuti della prima, poi dell'altra. In inglese: *concatenate*">concatena</abbr> inserendo uno spazio in mezzo.

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### Modifichiamolo

È un programma molto semplice.

Ma adesso immagina che tu lo stia scrivendo da zero.

A un certo punto inizi a definire la funzione e i parametri...

Però poi ti serve chiamare "quel metodo che trasforma la prima lettera in maiuscolo".

È `upper`? Oppure `uppercase`? `first_uppercase`? `capitalize`?

Quindi provi a consultare il caro amico di ogni programmatore: l'autocompletamento dell'editor di testo.

Digiti il primo parametro della funzione, `first_name`, poi un punto (`.`) e premi `Ctrl+Spazio` per innescare il completamento automatico.

Purtroppo, non compare nulla di utile:

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### Aggiungi i tipi

Modifichiamo l'ultimo programma aggiungendo le annotazioni di tipo.

Cambieremo esattamente questa parte, i parametri della funzione, da:

```Python
    first_name, last_name
```

a:

```Python
    first_name: str, last_name: str
```

Solo questo.

Questi sono i "type hints":

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

Attenzione che non è uguale a dichiarare i valori di default dei parametri della funzione:
```Python
    first_name="john", last_name="doe"
```

È una cosa diversa.

Usiamo i due puntini (`:`), non l'uguale (`=`).

E aggiungere le annotazioni di tipo normalmente non cambia il comportamento di un programma.

Adesso immagina che stai ancora creando quella funzione, ma ora con i *type hints*.

Allo stesso punto di prima, provi ad attivare l'autocompletamento con `Ctrl+Spazio` e vedi:

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

In questo modo puoi vedere la lista delle opzioni fino a quando trovi quella che sembra più giusta:

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## Altri vantaggi

Osserva questa funzione, puoi vedere che ha già le annotazioni di tipo:

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

Siccome l'editor di testo conosce i tipi delle variabili, non solo puoi beneficiare dell'autocompletamento, ma anche del controllo degli errori:

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

Adesso che sai che devi correggerlo, converti `age` in una stringa con `str(age)`:

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## Dichiarare i tipi

Hai appena imparato dove generalmente si usano le annotazioni di tipo: i parametri di una funzione.

Questo è anche l'utilizzo principale delle annotazioni di tipo in **FastAPI**.

### Tipi semplici

Puoi dichiarare tutti i tipi *standard* di Python, non solo `str`.

Puoi usare, per esempio:

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### Tipi generici con tipi di parametri

Ci sono alcune strutture dati che contengono altri valori, come `dict`, `list`, `set` and `tuple`. E i valori interni possono contenere a loro volta altri tipi.

Per dichiarare questi tipi e i tipi interni, puoi usare il modulo standard di Python chiamato `typing`.

Esiste specificamente per supportare questi *type hints*.

#### `List`

Per esempio, definiamo una variabile `list` di `str`.

Dal modulo `typing`, importiamo `List` (con la `L` maiuscola):

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

Dichiara la variabile con la sintassi dei due puntini (`:`).

Per il tipo, specifica `List`.

Siccome una lista è un tipo che contiene a sua volta tipi interni, li inserisci all'interno delle parentesi quadre:

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! Suggerimento
    Questi tipi interni all'interno delle parentesi quadre sono chiamati <abbr title="anche chiamati tipi di parametri">"type parameters"</abbr>.

    In questo caso, `str` è il tipo di parametro passato alla `List`.

Significa che: "la variabile `items` è una `list`, e ciascuno dei valori all'interno della lista è `str`".

Scrivendo questo, il tuo editor di testo può aiutarti anche quando iteri gli elementi di una lista:

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

Senza i tipi, è difficile ottenere un aiuto simile.

Nota che la variabile `item` è uno degli elementi della lista `items`.

L'editor capisce che è una `str`, e ti fornisce funzionalità aggiuntive.

#### `Tuple` e `Set`

Allo stesso modo puoi dichiarare `tuple` e `set`:

```Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial007.py!}
```

Questo vuol dire che:

* La variabile `items_t` è un `tuple` con 3 elementi, un `int`, un altro `int`, e una `str`.
* La variabile `items_s` è un `set`, e ognuno dei suoi elementi è di tipo `bytes`.

#### `Dict`

Per definire un `dict`, puoi passare 2 tipi di parametri, separati da virgole.

Il primo tipo di parametro è per le chiavi del `dict`.

Il secondo tipo di parametro è per i valori del `dict`:

```Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial008.py!}
```

Questo significa che:

* La variabile `prices` è un `dict`:
    * Le chiavi di questo `dict` sono di tipo `str` (per esempio, il nome di ciascun elemento).
    * I valori di questo `dict` sono di tipo `float` (per esempo, il prezzo di ciascun elemento).

#### `Optional`

Puoi usare `Optional` per dichiarare una variabile con un certo tipo, come `str`, ma che abbia un valore "opzionale", il che vuol dire che potrebbe anche essere `None`:

```Python hl_lines="1 4"
{!../../../docs_src/python_types/tutorial009.py!}
```

Usare `Optional[str]` invece che semplicemente `str` consentirà all'editor di testo di aiutarti a trovare errori nel caso in cui il tuo codice presupponga che un valore sia sempre `str`, quando in realtà potrebbe anche essere `None`.

#### Generic types

Questi tipi che accettano tipi di parametri tra le parentesi quadre, come per esempio:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...e altri.

sono chiamati **Generic types** oppure **Generics**.

### Classi come tipi

Puoi dichiarare una classe come il tipo di una variabile.

Immaginiamo che hai una classe `Person`, che ha un nome:

```Python hl_lines="1 2 3"
{!../../../docs_src/python_types/tutorial010.py!}
```

Allora è possibile dichiarare una variabile di tipo `Person`:

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

In questo modo l'editor di testo può aiutarti ancora una volta:

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

## Modelli di Pydantic

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> è una libreria in Python per la validazione dei dati.

Puoi dichiarare la "forma" dei dati con classi con attributi.

E ogni attributo ha un tipo.

A questo punto puoi creare un'istanza di quella classe con alcuni valori e Pydantic validerà i valori, li convertirà al tipo appropriato (se è necessario), e ti darà l'oggetto con tutti i dati.

Ancora una volta ribadiamo che l'editor di testo ti aiuterà con l'oggetto ottenuto.

Ecco del codice preso dalla documentazione ufficiale di Pydantic:

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! informazioni
    Per maggiori informazioni su <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic, consulta la sua documentazione</a>.

**FastAPI** è interamente basato su Pydantic.

Approfondiremo tutto questo con la pratica nel [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

## Annotazioni di tipo in **FastAPI**

**FastAPI** beneficia di questa annotazioni di tipo per fare parecchie cose.

Con **FastAPI** dichiari i parametri con le annotazioni di tipo e in cambio ottieni:

* **Supporto dagli editor di testo**.
* **Controlli sui tipi**.

...e **FastAPI** utilizza le stesse dichiarazioni per:

* **Definire i requisiti**: da request path parameters, query parameters, headers, bodies, dependencies, ecc.
* **Convertire i dati**: dalla richiesta al tipo richiesto.
* **Validare i dati**: da ogni richiesta:
    * Generare **automaticamente errori** per il client quando i dati sono invalidi.
* **Documentare** l'API usando OpenAPI:
    * che è a sua volta usata dalle interfacce delle documentazioni automatiche e interattive.

Questo potrebbe sembrare tutto astratto. Non ti preoccupare. Vedrai tutto questo in azione nel [Tutorial - User Guide](tutorial/index.md){.internal-link target=_blank}.

La cosa importante è che usando le annotazioni di tipo standard di Python, in un posto unico (invece di aggiungere più classi, decoratori, ecc), **FastAPI** farà gran parte del lavoro per te.

!!! Informazioni
    Se hai già completato il tutorial e sei tornato per approfondire sulle annotazioni di tipo, una buona risorsa è <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">il "cheat sheet" di `mypy`</a>.