# Caratteristiche

## Caratteristiche di FastAPI

**FastAPI** ti offre quanto segue:

### Basato su standard aperti

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> per la creazione di API, inclusa la dichiarazione di <abbr title="conosciuto anche come: endpoints, rotte">path</abbr> <abbr title="conosciuto anche come metodi HTTP, come POST, GET, PUT, DELETE">operation</abbr>, parametri, body requests, sicurezza, ecc.
* Documentazione automatica del modello di dati tramite lo <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>Schema JSON</strong></a> (così come avviene per la stessa OpenAPI che è basata sullo schema JSON).
* Progettato attorno a questi standard, dopo uno studio meticoloso. Invece di un approccio dall'alto.
* Ciò consente anche di utilizzare la **generazione del codice client** automatica in molte lingue.

### Documenti automatici

Documentazione delle API interattiva ed esplorazione delle interfacce utente web. Poiché il framework è basato su OpenAPI, ci sono più opzioni, 2 incluse per default.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, con esplorazione interattiva, permette di invocare e testare la tua API direttamente dal browser.

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Documentazione delle API alternativa con <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Semplicemente Python 

È tutto basato su dichiarazioni standard di **tipo Python 3.6** (grazie a Pydantic). Nessuna nuova sintassi da imparare. Solo Python standard.

Se hai bisogno di un aggiornamento in 2 minuti su come usare i tipi Python (anche se non usi FastAPI), controlla il breve tutorial: [Python Types](python-types.md){.internal-link target=_blank}.

Scrivi codice Python standard mediante i tipi:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Che può essere usato in questo modo:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! Info
    `**second_user_data` significa:

    Passa le chiavi e i valori del `second_user_data` dict direttamente come argomenti chiave-valore, equivalenti a: `User(id=4, name="Mary", join="2018-11-30")`

### Supporto dell'editor

Tutto il framework è stato progettato per essere facile e intuitivo da usare, tutte le decisioni sono state testate su più editor anche prima di iniziare lo sviluppo, per garantire la migliore esperienza di sviluppo.

Nell'ultimo sondaggio fatto a sviluppatori Python è stato chiaro <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target= "_blank">che la funzione più utilizzata è il "completamento automatico"</a>.

L'intero framework **FastAPI** è basato per soddisfare tale requisito. Il completamento automatico funziona ovunque.

Raramente dovrai tornare ai documenti.

Ecco come il tuo editor potrebbe aiutarti:

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Codice di Visual Studio</a>:

![supporto editor](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![supporto editor](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Otterrai il completamento nel codice che prima avresti considerato impossibile. Ad esempio, la chiave `price` all'interno di un corpo JSON (che potrebbe essere stato annidato) che proviene da una richiesta.

Non dovrai più digitare i nomi delle chiavi sbagliati, andare avanti e indietro tra i documenti o scorrere su e giù per scoprire se alla fine hai usato `username` o `user_name`.

### Breve

Ci sono **default** ragionevolmente per tutto, con configurazioni opzionali ovunque. Tutti i parametri possono essere messi a punto per fare ciò di cui hai bisogno e per definire l'API di cui hai bisogno.

Ma per default, tutto **"funziona e basta"**.

### Convalida

* Convalida la maggior parte (o tutti?) Python **tipi di dati**, inclusi:
    * JSON objects (`dict`).
    * JSON array (`list`) definendone i tipi di elementi.
    * Campi Stringa (`str`), definendone la lunghezza minima e massima.
    * Numeri (`int`, `float`) con valori minimo e massimo, ecc.

* Convalida per tipi più "esotici", come:
    * URL.
    * E-mail.
    * UUID.
    * ...e molti altri.

Tutta la convalida è gestita dallo stabile e robusto **Pydantic**.

### Sicurezza e autenticazione

Sicurezza e autenticazione integrate. Senza alcun compromesso su database o modelli di dati.

Tutti gli schemi di sicurezza definiti in OpenAPI, inclusi:

* HTTP di base.
* **OAuth2** (anche con **token JWT**). Controlla il tutorial su [OAuth2 con JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys in:
    * Headers.
    * Parametri di query.
    * Cookies, ecc.

Inoltre tutte le funzionalità di sicurezza di Starlette (inclusi i **cookie di sessione**).

Tutti costruiti come strumenti e componenti riutilizzabili che sono facili da integrare con i tuoi sistemi, archivi dati, database relazionali e NoSQL, ecc.

### Dependency Injection

FastAPI include un sistema di <abbr title='also known as "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></abbr> estremamente facile da usare, ma estremamente potente.

* Anche le dipendenze possono avere dipendenze, creando una gerarchia o un **"grafico" di dipendenze**.
* Tutto **gestito automaticamente** dal framework.
* Tutte le dipendenze possono richiedere dati da richieste **aumentando così i vincoli sul path operation** e la documentazione automatica.
* **Convalida automatica** anche per i parametri di *path operation* definiti nelle dipendenze.
* Supporto per complessi sistemi di autenticazione utente, **connessioni al database**, ecc.
* **Nessun compromesso** con database, frontend, ecc. Ma facile integrazione con tutti loro.

### "Plug-in" illimitati

Che servano o meno, importa e usa il codice di cui hai bisogno.

Qualsiasi integrazione è progettata per essere così semplice da usare (con dipendenze) che puoi creare un "plug-in" per la tua applicazione in 2 righe di codice usando la stessa struttura e sintassi usata per le tue *path operation*.

### Testato

* 100% <abbr title="La quantità di codice che viene automaticamente testata">copertura del test</abbr>.
* 100% <abbr title="Annotazioni di tipo Python, con questo il tuo editor e gli strumenti esterni possono fornirti un supporto migliore">annotazioni di tipo</abbr>.
* Utilizzato nelle applicazioni in produzione.

## Funzionalità Starlette

**FastAPI** è completamente compatibile con (e basato su) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong ></a>. Quindi, qualsiasi codice Starlette aggiuntivo che hai, funzionerà lo stesso.

`FastAPI` è in realtà una sottoclasse di `Starlette`. Quindi, se conosci già o usi Starlette, la maggior parte delle funzionalità funzionerà allo stesso modo.

Con **FastAPI** ottieni tutte le funzionalità di **Starlette** (poiché FastAPI è solo uno Starlette con steroidi):

* Prestazioni davvero impressionanti. È <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">uno dei framework Python più veloci disponibili, alla pari di **NodeJS** e **Vai**</a>.
* Supporto di **WebSocket**.
* In-process background task.
* Eventi di startup e shutdown.
* Test client basato su `requests`.
* **CORS**, GZip, Static Files, Streaming responses.
* **Supporto per sessioni e cookie**.
* Copertura del test al 100%.
* Base di codice annotata al 100%.

## Pydantic features

**FastAPI** è completamente compatibile con (e basato su) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Quindi, qualsiasi codice Pydantic aggiuntivo che hai, funzionerà lo stesso.

Comprese librerie esterne basate su Pydantic, come <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s per database.

Ciò significa anche che in molti casi puoi passare lo stesso oggetto che ottieni da una richiesta **direttamente al database**, poiché tutto viene convalidato automaticamente.

Lo stesso vale al contrario, in molti casi puoi semplicemente passare l'oggetto che ottieni dal database **direttamente al client**.

Con **FastAPI** ottieni tutte le funzionalità di **Pydantic** (poiché FastAPI si basa su Pydantic per tutta la gestione dei dati):

* **Nessun mal di testa**:
    * Nessun nuovo micro-linguaggio per la definizione dello schema da imparare.
    * Se conosci i tipi di Python sai come usare Pydantic.
* Funziona bene con il tuo **<abbr title="Integrated Development Environment, similar to a code editor">IDE</abbr>/<abbr title="A program that checks for code errors">linter</abbr>/brain**:
    * Perché le strutture dati pydantic sono solo istanze di classi che definisci; completamento automatico, linting, mypy e la tua intuizione dovrebbero andare correttamente con i tuoi dati convalidati.
* **Veloce**:
    * in termindi di <a href="https://pydantic-docs.helpmanual.io/#benchmarks-tag" class="external-link" target="_blank">benchmark</a>, Pydantic è più veloce di tutte le altre librerie testate .
* Convalida **strutture complesse**:
    * Uso di modelli gerarchici Pydantic, `Lista` e `Dict` di Python, ecc.
    * E i validatori consentono di definire, controllare e documentare in modo chiaro e semplice schemi di dati complessi come quello JSON.
    * Puoi avere oggetti JSON profondamente **nidificati** e averli tutti convalidati e annotati.
* **Estendibile**:
    * Pydantic consente di definire tipi di dati personalizzati oppure è possibile estendere la convalida con metodi su cui viene applicato un decoratore di validazione.
* Copertura del test al 100%.
