# Contribuire allo Sviluppo

Per prima cosa, puoi consultare i modi principali per [aiutare FastAPI e ricevere aiuto](help-fastapi.md){.internal-link target=_blank}.


## Sviluppare

Se hai già clonato la repository e sai di dover fare un'immersione profonda nel codice, ecco alcune linee guida per impostare il tuo ambiente di lavoro.

### Ambiente virtuale con `venv`

Puoi creare un <abbr title="in inglese: virtual environment">ambiente virtuale</abbr> in una cartella usando il modulo `venv` di Python:

<div class="termy">

```console
$ python -m venv env
```

</div>

Questo creerà una directory `./env/` con i binari di Python e poi potrai installare pacchetti in quell'ambiente isolato.

### Attivare l'ambiente

Attiva il nuovo ambiente con:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ source ./env/bin/activate
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ .\env\Scripts\Activate.ps1
    ```

    </div>

=== "Windows Bash"

    Oppure se usi Bash per Windows (per esempio <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

Per vedere se ha funzionato, usa:

=== "Linux, macOS, Windows Bash"

    <div class="termy">

    ```console
    $ which pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ Get-Command pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

Se viene mostrato il binario `pip` all'interno di `env/bin/pip`, allora ha funzionato. 🎉



!!! tip
    Ogni volta che installi un nuovo pacchetto con `pip` in quell'ambiente, attiva nuovamente l'ambiente.

    Questo fa sì che se si utilizza un programma terminale installato da quel pacchetto (come `flit`), si utilizzi quello del proprio ambiente locale e non qualsiasi altro che potrebbe essere stato installato a livello globale.

### Flit

**FastAPI** usa <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> per creare, impacchettare e pubblicare il progetto.

Dopo aver attivato l'ambiente come descritto sopra, installa `flit`:

<div class="termy">

```console
$ pip install flit

---> 100%
```

</div>

Ora riattiva l'ambiente per essere sicuro che stai usando il `flit` che hai appena installato (e non quello globale).

E ora usa `flit` per installare le dipendenze del progetto:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ flit install --deps develop --symlink

    ---> 100%
    ```

    </div>

=== "Windows"

    Se sei su Windows, usa `--pth-file` invece che `--symlink`:

    <div class="termy">

    ```console
    $ flit install --deps develop --pth-file

    ---> 100%
    ```

    </div>

Verranno installate tutte le dipendenze e FastAPI nell'ambiente locale.

#### Usare il FastAPI locale

Se crei un file Python che importa e utilizza FastAPI, e lo esegui con il Python dal proprio ambiente locale, esso utilizzerà il codice sorgente del FastAPI locale.

E se aggiorni il codice sorgente locale di FastAPI, dato che è installato con `--symlink` (o `--pth-file` su Windows), quando esegui di nuovo quel file Python, esso userà la versione aggiornata di FastAPI appena modificata.

In questo modo, non è necessario "installare" la versione locale per poter testare ogni modifica.

### Format

C'è uno script che puoi eseguire che formatterà e pulirà tutto il tuo codice:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Inoltre, ordinerà automaticamente tutti gli `import`.

Per poterli ordinare correttamente, è necessario che FastAPI sia installato localmente nel proprio ambiente, con il comando nella sezione precedente usando `--symlink` (o `--pth-file` su Windows).

### Formatta gli `import`

C'è un altro script che formatta tutti gli `import` e fa in modo di non avere `import` inutilizzati:

<div class="termy">

```console
$ bash scripts/format-imports.sh
```

</div>

Poiché esegue un comando dopo l'altro e modifica e ripristina molti file, l'esecuzione richiede un po' più di tempo, quindi potrebbe essere più facile usare `scripts/format.sh` frequentemente e `scripts/format-imports.sh` solo prima del commit.

## Documentazione

Per prima cosa, assicurati di aver impostato il tuo ambiente e installato tutti i requisiti come descritto sopra.

La documentazione utilizza <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

E ci sono strumenti/script extra per gestire le traduzioni in `./scripts/docs.py`.

!!! tip
    Non è necessario vedere il codice in `./scripts/docs.py`, basta usarlo nel terminale.

Tutta la documentazione è in formato Markdown nella directory `./docs/en/`.

Molti dei tutorial hanno blocchi di codice.

Nella maggior parte dei casi, questi blocchi di codice sono vere e proprie applicazioni complete che possono essere eseguite così come sono.

Infatti, quei blocchi di codice non sono scritti all'interno del Markdown, sono file Python nella directory `./docs_src/`.

E quei file Python sono inclusi/iniettati nella documentazione durante la generazione del sito.

### Documentazione per i test

La maggior parte dei test sono effettivamente eseguiti con i file sorgente di esempio nella documentazione.

Questo assicura che:

* La documentazione sia aggiornata.
* Gli esempi di documentazione possano essere eseguiti così come sono.
* La maggior parte delle funzionalità sono coperte dalla documentazione, garantito dalla copertura dei test.

Durante lo sviluppo locale, c'è uno script che costruisce il sito e controlla eventuali modifiche, live-reloading:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Mostrerà la documentazione su `http://127.0.0.1:8008`.

In questo modo, puoi modificare la documentazione/file sorgente e vedere le modifiche in tempo reale.

#### Typer CLI (optional)

Le istruzioni qui mostrano come usare lo script a `./scripts/docs.py` con il programma `python` direttamente.

Ma potete puoi anche usare <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, e otterrai l'autocompletamento nel tuo terminale per i comandi dopo l'installazione dell'autocompletamento.

Se si installa Typer CLI, è possibile installare il completamento con:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Apps and docs allo stesso tempo

Se si eseguono gli esempi con, ad es:

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

poiché Uvicorn per default userà la porta `8000`, la documentazione sulla porta `8008` non si scontrerà.

### Traduzioni

L'aiuto per le traduzioni è MOLTO apprezzato! E non può essere fatto senza l'aiuto della comunità. 🌎 🚀

Ecco i passi per aiutare con le traduzioni.

#### Suggerimenti e linee guida

* Controlla le <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">pull request esistenti</a> per la tua lingua e approvale o richiedi modifiche.

!!! tip
    È possibile <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">aggiungere commenti con suggerimenti di modifica</a> alle pull request esistenti.

    Controlla la documentazione su <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">valutare una pull request</a> per approvarla o richiedere modifiche.

* Controlla negli <a href="https://github.com/tiangolo/fastapi/issues" class="external-link" target="_blank">issues</a> per vedere se c'è una traduzione coordinata per la tua lingua.

* Aggiungi una singola pull request per ogni pagina tradotta. Questo renderà molto più facile per gli altri esaminarla.

Per le lingue che non parlo, aspetterò che molti altri esaminino la traduzione prima di approvarla definitivamente per il merging.

* Puoi anche controllare se ci sono traduzioni per la vostra lingua e aggiungere un commento, che mi aiuterà a sapere che la traduzione è corretta e posso fare il merge.

* Utilizza gli stessi esempi di Python e traduci solo il testo nei documenti. Non devi cambiare nulla perché questo funzioni.

* Utilizzare le stesse immagini, gli stessi nomi di file e gli stessi link. Non devi cambiare nulla perché funzioni.

* Per recuperare il codice di 2 lettere per la lingua che si desidera tradurre puoi utilizzare la tabella <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">Lista dei codici ISO 639-1</a>.

#### Lingua esistente

Supponiamo che vuoi tradurre una pagina per una lingua che ha già delle traduzioni per alcune pagine, come lo spagnolo.

Nel caso dello spagnolo, il codice di 2 lettere è `es`. Quindi, la directory per le traduzioni in spagnolo si trova a `docs/es/`.

!!! tip
    La lingua principale ("ufficiale") è l'inglese, che si trova a `docs/en/`.

Ora fai andare il server per visualizzare la documentazione in spagnolo:

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Ora puoi andare su <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> e vedere le tue modifiche in diretta.

Se guardi il sito web di FastAPI docs, vedrai che ogni lingua ha tutte le pagine. Ma alcune pagine non sono tradotte e hanno una notifica sulla traduzione mancante.

Ma quando lo si esegue localmente in questo modo, si vedranno solo le pagine già tradotte.

Ora supponiamo che vuoi aggiungnere una traduzione per la sezione [Features](features.md){.internal-link target=_blank}.

* Copia il file a:

```
docs/en/docs/features.md
```

* Incollalo esattamente nella stessa posizione ma per la lingua che volete tradurre, ad es:

```
docs/es/docs/features.md
```

!!! tip
    Si noti che l'unico cambiamento nel percorso e nel nome del file è il codice della lingua, da `en` a `es`.

* Ora aprite il file di configurazione MkDocs per l'inglese a:

```
docs/en/docs/mkdocs.yml
```

* Trova il luogo dove si trova quel `docs/features.md` nel file di configurazione. Da qualche parte come:

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

* Apri il file di configurazione MkDocs per la lingua che si sta modificando, ad es:

```
docs/es/docs/mkdocs.yml
```

* Aggiungilo lì nello stesso punto in cui era per l'inglese, ad esempio:

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

Assicurati che se ci sono altre voci, la nuova voce con la tua traduzione sia esattamente nello stesso ordine della versione inglese.

Se vai sul tuo browser vedrai che ora i documenti mostrano la tua nuova sezione. 🎉

Ora è possibile tradurre il tutto e vedere come appare mentre si salva il file.

#### Nuova Lingua

Supponiamo che vuoi aggiungere la traduzione per una lingua che non è ancora tradotta, nemmeno alcune pagine.

Supponiamo che si vuoi aggiungere la traduzione per il creolo, e non è ancora presente nella documentazione.

Controllando il link riportato in alto, il codice per il "creolo" è `ht`.

Il passo successivo è quello di eseguire lo script per generare una nuova directory di traduzione:

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
Updating ht
Updating en
```

</div>

Ora puoi controllare nel vostro editor di codice la directory appena creata `docs/ht/`.

!!! tip
    Crea una pull request con solo questo, per impostare la configurazione per la nuova lingua, prima di aggiungere le traduzioni.

    In questo modo altri possono aiutare con altre pagine mentre tu lavori alla prima. 🚀

Inizia traducendo la pagina principale, `docs/ht/index.md`.

Poi si può continuare con le istruzioni precedenti, per una "Lingua esistente".

##### Nuova lingua non supportata

Se durante l'esecuzione dello script del server live si ottiene un errore sulla lingua non supportata, qualcosa del genere:

```
 raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: partials/language/xx.html
```

Ciò significa che il tema non supporta quel linguaggio (in questo caso, con un falso codice di 2 lettere di `xx`).

Ma non preoccuparti, potete impostare la lingua del tema in inglese e poi tradurre il contenuto della documentazione.

Se hai bisogno di farlo, modifica il `mkdocs.yml` per la tua nuova lingua, avrà qualcosa di simile:

```YAML hl_lines="5"
site_name: FastAPI
# More stuff
theme:
  # More stuff
  language: xx
```

Cambia quella lingua da `xx` (dal tuo codice lingua) a `en`.

Poi si può avviare di nuovo il server live.

#### Anteprima del risultato

Quando usi lo script a `./scripts/docs.py` con il comando `live`, verranno mostrati solo i file e le traduzioni disponibili per la lingua corrente.

Ma una volta che hai finito, puoi testare come la documentazione apparirebbe online.

Per farlo, prima genera tutta la documentazione:

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Updating es
Updating en
Building docs for: en
Building docs for: es
Successfully built docs for: es
Copying en index.md to README.md
```

</div>

Questo genera tutta la documentazione a `./docs_build/` per ogni lingua. Questo include l'aggiunta di qualsiasi file con traduzioni mancanti, con una nota che dice che "questo file non ha ancora una traduzione". Ma non è necessario fare nulla con quella directory.

Poi costruisce tutti quei siti MkDocs indipendenti per ogni lingua, li combina e genera l'output finale a `./site/`.

Poi si può servire con il comando `serve':

<div class="termy">

```console
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

## Tests

C'è uno script che si può eseguire localmente per testare tutto il codice e generare report di copertura in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Questo comando genera una directory `./htmlcov/`, se si apre il file `./htmlcov/index.html` nel browser, è possibile esplorare in modo interattivo le regioni di codice che sono coperte dai test, e notare se manca qualche regione.
