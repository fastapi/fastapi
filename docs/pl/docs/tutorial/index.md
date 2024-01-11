# Samouczek

Ten samouczek pokaże Ci, krok po kroku, jak używać większości funkcji **FastAPI**.

Każda część korzysta z poprzednich, ale jest jednocześnie osobnym tematem. Możesz przejść bezpośrednio do każdego rozdziału, jeśli szukasz rozwiązania konkretnego problemu.

Samouczek jest tak zbudowany, żeby służył jako punkt odniesienia w przyszłości.

Możesz wracać i sprawdzać dokładnie to czego potrzebujesz.

## Wykonywanie kodu

Wszystkie fragmenty kodu mogą być skopiowane bezpośrednio i użyte (są poprawnymi i przetestowanymi plikami).

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

Na potrzeby samouczka możesz zainstalować również wszystkie opcjonalne biblioteki:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...wliczając w to `uvicorn`, który będzie służył jako serwer wykonujacy Twój kod.

!!! note
    Możesz również wykonać instalację "krok po kroku".

    Prawdopodobnie zechcesz to zrobić, kiedy będziesz wdrażać swoją aplikację w środowisku produkcyjnym:

    ```
    pip install fastapi
    ```

    Zainstaluj też `uvicorn`, który będzie służył jako serwer:

    ```
    pip install "uvicorn[standard]"
    ```

    Tak samo możesz zainstalować wszystkie dodatkowe biblioteki, których chcesz użyć.

## Zaawansowany poradnik

Jest też **Zaawansowany poradnik**, który możesz przeczytać po lekturze tego **Samouczka**.

**Zaawansowany poradnik** opiera się na tym samouczku, używa tych samych pojęć, żeby pokazać Ci kilka dodatkowych funkcji.

Najpierw jednak  powinieneś przeczytać **Samouczek** (czytasz go teraz).

Ten rozdział jest zaprojektowany tak, że możesz stworzyć kompletną aplikację używając tylko informacji tutaj zawartych, a następnie rozszerzać ją na różne sposoby, w zależności od potrzeb, używając kilku dodatkowych pomysłów z **Zaawansowanego poradnika**.
