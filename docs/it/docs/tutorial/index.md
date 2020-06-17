# Tutorial - Guida Utente - Introduzione

Questo tutorial ti spiega come usare **FastAPI** e le sue funzionalità, passo dopo passo.

Ogni sezione sviluppa gli argomenti trattati nella sezione precedente, ma la guida è strutturata in modo tale che ciascuna sezione possa essere consultata singolarmente.

In questo modo potrai usare il tutorial anche come referenza.

Così potrai tornare indietro e rivedere solo i concetti che ti servono.

## Esegui il codice

Tutti i blocchi di codice che vedrai nella guida possono essere copiati e usati direttamente (fanno parte della suite di test del framework).

Per provare gli esempi, copia il codice in un file chiamato `main.py`, e avvia `uvicorn` con il seguente comando:

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

È **ALTAMENTE consigliato** scrivere o copiare il codice, modificarlo ed eseguirlo localmente.

Quando proverai gli esempi direttamente all'interno dell'editor di testo ti accorgerai subito dei vantaggi di FastAPI, quanto poco codice serva scrivere, i controlli sulle annotazioni di tipo, l'autocompletamento, ecc.

---

## Installa FastAPI

Il primo passo è quello di installare FastAPI.

Per questo tutorial è consigliato installarlo insieme alle dipendenze e funzionalità opzionali con il seguente comando:

<div class="termy">

```console
$ pip install fastapi[all]

---> 100%
```

</div>

...il che include `uvicorn`, che puoi usare come server per eseguire il tuo codice.

!!! nota
    Puoi anche installare le dipendenze singolarmente, una per una.

    Il che è consigliato quando vorrai rilasciare la tua applicazione in produzione:

    ```
    pip install fastapi
    ```

    Per installare `uvicorn`, il server che esegue il codice, usa:

    ```
    pip install uvicorn
    ```

    Puoi seguire lo stesso procedimento per ciascuna dipendenza opzionale che vorrai usare.

## Guida Utente Avanzata

È disponibile anche una **Guida Utente Avanzata** che potrai consultare dopo il **Tutorial - Guida Utente**.

La **Guida Utente Avanzata**, che usa gli stessi concetti di questo Tutorial e ne è il suo proseguimento, ti mostra alcune funzionalità aggiuntive.

Ti consigliamo però di completare prima il **Tutorial - Guida Utente** (che stai leggendo in questo momento).

Il **Tutorial - Guida Utente** ti mostra come sviluppare un'applicazione completa, che potrai migliorare a seconda delle tue esigenze usando alcuni dei concetti più avanzati della **Guida Avanzata Utente**.
