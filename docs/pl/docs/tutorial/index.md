# Samouczek - Instrukcja - Wprowadzenie

Ten samouczek pokaże Ci, krok po kroku, jak używać większości funkcji **FastAPI**.

Każda część korzysta z poprzednich, ale jest jednocześnie osobnym tematem. Możesz przejść bezpośrednio do każdego rozdziału, jeśli szukasz rozwiązania konkretnego problemu.

Samouczek jest tak zbudowany, żeby służył jako punkt odniesienia w przyszłości.

Możesz wracać i sprawdzać dokładnie to czego potrzebujesz.

## Wykonywanie kodu

Wszystkie fragmenty kodu mogą być skopiowane bezpośrednio i użyte (są poprawnymi i przetestowanymi plikami)

Żeby wykonać każdy przykład skopiuj kod to pliku `main.py` i uruchom `uvicorn` za pomocą:

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

**BARDZO zalecamy** pisanie bądź kopiowanie kodu, edycję, a następnie wykonywanie go lokalnie.

Użycie w Twoim edytorze jest tym, co pokazuje prawdziwe korzyści z FastAPI, pozwala zobaczyć jak mało kodu musisz napisać, wszystkie funkcje, takie jak kontrola typów, <abbr title="auto-complete, autocompletion, IntelliSense">automatyczne uzupełnianie</abbr>, itd.

---

## Instalacja FastAPI

Jako pierwszy krok zainstaluj FastAPI.

Na potrzeby samouczka lepiej zainstaluj ze wszystkimi opcjonalnymi zależnościami i funkcjami:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...wliczając w to `uvicorn`, który będzie służył jako serwer wykonujacy Twój kod.

!!! note
    You can also install it part by part.

    This is what you would probably do once you want to deploy your application to production:

    ```
    pip install fastapi
    ```

    Also install `uvicorn` to work as the server:

    ```
    pip install "uvicorn[standard]"
    ```

    And the same for each of the optional dependencies that you want to use.

## Instrukcja dla zaawansowanych

Jest też **Instrukcja dla zaawansowanych**, którą możesz przeczytać po lekturze tego **Samouczka - Instrukcji**.

**Instrukcja dla zaawansowanych**, opiera się na tym samouczku, używa tych samych pojęć, żeby pokazać Ci kilka dodatkowych funkcji.

Najpierw przeczytaj **Samouczek - Instrukcja** (czytasz to teraz).

Samouczek jest zaprojektowany tak, że możesz stworzyć kompletną aplikację używając tylko **Samouczka - Instrukcji**, a następnie rozszerzać ją na różne sposoby, w zależności od potrzeb, używając kilku dodatkowych pomysłów z **Instrukcji dla zaawansowanych**

