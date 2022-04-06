# Tutorial - Handleiding - Introductie

Deze handleiding licht stap voor stap het gebruik toe van **FastAPI**, met aandacht voor de verschillende features.

Elk hoofdstuk bouwt verder op de voorgaande, maar de handleiding is onderverdeeld in aparte onderwerpen, zodat u rechtstreeks naar het specifieke onderwerp kan gaan voor uw noden.

Verder is de handleiding bedoeld als een naslagwerk.

U kunt dus later terugkomen om exact te vinden wat u zoekt.

## De code uitvoeren

Alle codeblokken kunnen gekopieerd en meteen gebruikt worden (het zijn namelijk geteste Python bestanden).

Om een van de voorbeelden uit te voeren, kopieert u de code in een bestand genaamd `main.py` en voert u `uvicorn` als volgt uit:

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

Het is **TEN ZEERSTE aangeraden** dat u de code lokaal schrijft of kopieert, bewerkt en uitvoert.

Juist in het gebruiken van uw editor schuilt de kracht achter FastAPI, zo ziet u namelijk hoe weinig code u slechts hoeft te schrijven, hoe de typechecks en autocompletion werken, enzovoorts.

---

## FastAPI installeren

De eerste stap is het installeren van FastAPI.

Voor deze tutorial is het aangeraden om FastAPI te installeren met alle optionele dependencies:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...hieronder valt ook `uvicorn`, dat u kunt gebruiken als een server om uw code uit te voeren.

!!! note
    U kunt ook alles stuk voor stuk apart installeren.

    Dit is waarschijnlijk wat u zou doen eens u de applicatie in een productieomgeving zou uitrollen:

    ```
    pip install fastapi
    ```

    Installeer ook `uvicorn` dat als webserver zal fungeren:

    ```
    pip install "uvicorn[standard]"
    ```

    Herhaal dit laatste commando op een analoge manier voor elke optionele dependency die u wenst te gebruiken.

## Geavanceerde handleiding

Er is ook een **Geavanceerde handleiding** die u later kan lezen, na deze **Tutorial - Handleiding**.

De **Geavanceerde handleiding** steunt op de concepten die in deze handleiding worden geïntroduceerd en leert u kennismaken met extra functionaliteit, maar het is aangeraden om eerst de **Tutorial - Handleiding** te lezen (hier bent u nu).

De volledige handleiding is dusdanig opgesteld dat u een volledige applicatie kan bouwen met enkel de **Tutorial - Handleiding**, waarna u die op verschillende manieren kan uitbreiden door, afhankelijk van uw noden, enkele aanvullende ideeën uit de **Geavanceerde handleiding** te gebruiken.