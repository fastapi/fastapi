# Pierwsze kroki

Najprostszy plik FastAPI może wyglądać tak:

```Python
{!../../../docs_src/first_steps/tutorial001.py!}
```

Skopiuj to do pliku `main.py`.

Uruchom serwer:

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

!!! note
    Polecenie `uvicorn main:app` odnosi się do:

    * `main`: plik `main.py` ("moduł" Python).
    * `app`: obiekt utworzony w pliku `main.py` w lini `app = FastAPI()`.
    * `--reload`: sprawia, że serwer uruchamia się ponownie po zmianie kodu. Używany tylko w trakcie tworzenia oprogramowania.

Na wyjściu znajduje się linia z czymś w rodzaju:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Ta linia pokazuje adres URL, pod którym Twoja aplikacja jest obsługiwana, na Twoim lokalnym komputerze.

### Sprawdź to

Otwórz w swojej przeglądarce <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Zobaczysz odpowiedź w formacie JSON:

```JSON
{"message": "Hello World"}
```

### Interaktywna dokumentacja API

Przejdź teraz do <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Zobaczysz automatyczną i interaktywną dokumentację API (dostarczoną przez <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternatywna dokumentacja API

Teraz przejdź do <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Zobaczysz alternatywną automatycznie wygenerowaną dokumentację API (dostarczoną przez <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** generuje "schemat" z całym Twoim API przy użyciu standardu **OpenAPI** służącego do definiowania API.

#### Schema

"Schema" jest definicją lub opisem czegoś. Nie jest to kod, który go implementuje, ale po prostu abstrakcyjny opis.

#### API "Schema"

W typ przypadku, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> to specyfikacja, która dyktuje sposób definiowania schematu interfejsu API.

Definicja schematu zawiera ścieżki API, możliwe parametry, które są przyjmowane przez endpointy, itp.

#### "Schemat" danych

Termin "schemat" może również odnosić się do wyglądu niektórych danych, takich jak zawartość JSON.

W takim przypadku będzie to oznaczać atrybuty JSON, ich typy danych itp.

#### OpenAPI i JSON Schema

OpenAPI definiuje API Schema dla Twojego API, który zawiera definicje (lub "schematy") danych wysyłanych i odbieranych przez Twój interfejs API przy użyciu **JSON Schema**, standardu dla schematów danych w formacie JSON.

#### Sprawdź `openapi.json`

Jeśli jesteś ciekawy, jak wygląda surowy schemat OpenAPI, FastAPI automatycznie generuje JSON Schema z opisami wszystkich Twoich API.

Możesz to zobaczyć bezpośrednio pod adresem: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Zobaczysz JSON zaczynający się od czegoś takiego:

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

#### Do czego służy OpenAPI

Schemat OpenAPI jest tym, co zasila dwa dołączone interaktywne systemy dokumentacji.

Istnieją dziesiątki alternatyw, wszystkie oparte na OpenAPI. Możesz łatwo dodać dowolną z nich do swojej aplikacji zbudowanej za pomocą **FastAPI**.

Możesz go również użyć do automatycznego generowania kodu dla klientów, którzy komunikują się z Twoim API. Na przykład aplikacje frontendowe, mobilne lub IoT.

## Przypomnijmy, krok po kroku

### Krok 1: zaimportuj `FastAPI`

```Python hl_lines="1"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`FastAPI` jest klasą, która zapewnia wszystkie funkcjonalności Twojego API.

!!! note "Szczegóły techniczne"
    `FastAPI` jest klasą, która dziedziczy bezpośrednio z `Starlette`.

    Oznacza to, że możesz korzystać ze wszystkich funkcjonalności <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> również w `FastAPI`.


### Krok 2: utwórz instancję `FastAPI`

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Zmienna `app` będzie tutaj "instancją" klasy `FastAPI`.

Będzie to główny punkt interakcji przy tworzeniu całego interfejsu API.

Ta zmienna `app` jest tą samą zmienną, do której odnosi się `uvicorn` w poleceniu:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Jeśli stworzysz swoją aplikację, np.:

```Python hl_lines="3"
{!../../../docs_src/first_steps/tutorial002.py!}
```

I umieścisz to w pliku `main.py`, to będziesz mógł tak wywołać `uvicorn`:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Krok 3: wykonaj *operację na ścieżce*

#### Ścieżka

"Ścieżka" tutaj odnosi się do ostatniej części adresu URL, zaczynając od pierwszego `/`.

Więc, w adresie URL takim jak:

```
https://example.com/items/foo
```

...ścieżką będzie:

```
/items/foo
```

!!! info
    "Ścieżka" jest zazwyczaj nazywana "path", "endpoint" lub "route'.

Podczas budowania API, "ścieżka" jest głównym sposobem na oddzielenie "odpowiedzialności" i „zasobów”.

#### Operacje

"Operacje" tutaj odnoszą się do jednej z "metod" HTTP.

Jedna z:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...i te bardziej egzotyczne:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

W protokole HTTP można komunikować się z każdą ścieżką za pomocą jednej (lub więcej) "metod".

---

Podczas tworzenia API zwykle używasz tych metod HTTP do wykonania określonej akcji.

Zazwyczaj używasz:

* `POST`: do tworzenia danych.
* `GET`: do odczytywania danych.
* `PUT`: do aktualizacji danych.
* `DELETE`: do usuwania danych.

Tak więc w OpenAPI każda z metod HTTP nazywana jest "operacją".

Będziemy je również nazywali "**operacjami**".

#### Zdefiniuj *dekorator operacji na ścieżce*

```Python hl_lines="6"
{!../../../docs_src/first_steps/tutorial001.py!}
```

`@app.get("/")` mówi **FastAPI** że funkcja poniżej odpowiada za obsługę żądań, które trafiają do:

* ścieżki `/`
* używając <abbr title="metoda HTTP GET">operacji <code>get</code></abbr>

!!! info "`@decorator` Info"
    Składnia `@something` jest w Pythonie nazywana "dekoratorem".

    Umieszczasz to na szczycie funkcji. Jak ładną ozdobną czapkę (chyba stąd wzięła się nazwa).

    "Dekorator" przyjmuje funkcję znajdującą się poniżej jego i coś z nią robi.

    W naszym przypadku dekorator mówi **FastAPI**, że poniższa funkcja odpowiada **ścieżce** `/` z **operacją** `get`.

    Jest to "**dekorator operacji na ścieżce**".

Możesz również użyć innej operacji:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Oraz tych bardziej egzotycznych:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

!!! tip
    Możesz dowolnie używać każdej operacji (metody HTTP).

    **FastAPI** nie narzuca żadnego konkretnego znaczenia.

    Informacje tutaj są przedstawione jako wskazówka, a nie wymóg.

    Na przykład, używając GraphQL, normalnie wykonujesz wszystkie akcje używając tylko operacji `POST`.

### Krok 4: zdefiniuj **funkcję obsługującą ścieżkę**

To jest nasza "**funkcja obsługująca ścieżkę**":

* **ścieżka**: to `/`.
* **operacja**: to `get`.
* **funkcja**: to funkcja poniżej "dekoratora" (poniżej `@app.get("/")`).

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Jest to funkcja Python.

Zostanie ona wywołana przez **FastAPI** za każdym razem, gdy otrzyma żądanie do adresu URL "`/`" przy użyciu operacji `GET`.

W tym przypadku jest to funkcja "asynchroniczna".

---

Możesz również zdefiniować to jako normalną funkcję zamiast `async def`:

```Python hl_lines="7"
{!../../../docs_src/first_steps/tutorial003.py!}
```

!!! note
    Jeśli nie znasz różnicy, sprawdź [Async: *"In a hurry?"*](/async/#in-a-hurry){.internal-link target=_blank}.

### Krok 5: zwróć zawartość

```Python hl_lines="8"
{!../../../docs_src/first_steps/tutorial001.py!}
```

Możesz zwrócić `dict`, `list`, pojedynczą wartość jako `str`, `int`, itp.

Możesz również zwrócić modele Pydantic (więcej o tym później).

Istnieje wiele innych obiektów i modeli, które zostaną automatycznie skonwertowane do formatu JSON (w tym ORM itp.). Spróbuj użyć swoich ulubionych, jest bardzo prawdopodobne, że są już obsługiwane.

## Podsumowanie

* Zaimportuj `FastAPI`.
* Stwórz instancję `app`.
* Dodaj **dekorator operacji na ścieżce** (taki jak `@app.get("/")`).
* Napisz **funkcję obsługującą ścieżkę** (taką jak `def root(): ...` powyżej).
* Uruchom serwer deweloperski (`uvicorn main:app --reload`).
