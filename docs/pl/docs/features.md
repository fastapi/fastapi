# Cechy

## Cechy FastAPI

**FastAPI** zapewnia Ci:

### Oparcie o standardy open

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> do tworzenia API, w tym deklaracji <abbr title="znanie również jako: paths, endpoints, routes">ścieżek</abbr> <abbr title="znane również jako metody HTTP, takie jak POST, GET, PUT, DELETE">operacji</abbr>, parametrów, ciał zapytań, bezpieczeństwa, itp.
* Automatyczna dokumentacja modelu danych za pomocą <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (ponieważ samo OpenAPI bazuje na JSON Schema).
* Zaprojektowane wokół tych standardów, po drobiazgowej analizie, zamiast skupiania się na górnej warstwie.
* Możliwość automatycznego **generowania kodu klienta** w wielu językach.

### Automatyczna dokumentacja

Interaktywna dokumentacja API i przegląd interfejsów użytkownika. Z racji tego, że framework bazuje na OpenAPI, istnieje wiele opcji, z czego 2 są domyślnie dołączone.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, z interaktywnym interfejsem - odpytuj i testuj swoje API bezpośrednio z przeglądarki.

![Swagger UI interakcja](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternatywna dokumentacja API z <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Nowoczesny Python

Wszystko opiera się na standardowych deklaracjach typu **Python 3.6** (dzięki Pydantic). Brak nowej składni do uczenia. Po prostu standardowy, współczesny Python.

Jeśli potrzebujesz szybkiego przypomnienia jak używać deklaracji typów w Pythonie (nawet jeśli nie używasz FastAPI), sprawdź krótki samouczek: [Python Types](python-types.md){.internal-link target=_blank}.

Po prostu piszesz standardowe deklaracje typów Pythona:

```Python
from datetime import date

from pydantic import BaseModel

# Zadeklaruj parametr jako str
# i uzyskaj wsparcie edytora wewnątrz funkcji
def main(user_id: str):
    return user_id


# Model Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Które mogą zostać później użyte w następujący sposób:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` oznacza:

    Przekaż klucze i wartości słownika `second_user_data` bezpośrednio jako argumenty klucz-wartość, co jest równoznaczne z: `User(id=4, name="Mary", joined="2018-11-30")`

### Wsparcie edytora

Cały framework został zaprojektowany tak, aby był łatwy i intuicyjny w użyciu. Wszystkie decyzje zostały przetestowane na wielu edytorach jeszcze przed rozpoczęciem developmentu, aby zapewnić najlepsze wrażenia programistyczne.

Ostatnia ankieta "Python developer survey" jasno wskazuje, że <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">najczęściej używaną funkcjonalnością jest autouzupełnianie w edytorze</a>.

Cała struktura frameworku **FastAPI** jest na tym oparta. Autouzupełnianie działa wszędzie.

Rzadko będziesz musiał wracać do dokumentacji.

Oto, jak twój edytor może Ci pomóc:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![wsparcie edytora](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![wsparcie edytora](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Otrzymasz nawet uzupełnienie w miejscach, w których normalnie uzupełnienia nie ma. Na przykład klucz "price" w treści JSON (który mógł być zagnieżdżony), który pochodzi z zapytania.

Koniec z wpisywaniem błędnych nazw kluczy, przechodzeniem tam i z powrotem w dokumentacji lub przewijaniem w górę i w dół, aby sprawdzić, czy w końcu użyłeś nazwy `username` czy `user_name`.

### Zwięzłość

Wszystko posiada sensowne **domyślne wartości**. Wszędzie znajdziesz opcjonalne konfiguracje. Wszystkie parametry możesz dostroić, aby zrobić to co potrzebujesz do zdefiniowania API.

Ale domyślnie wszystko **"po prostu działa"**.

### Walidacja

* Walidacja większości (lub wszystkich?) **typów danych** Pythona, w tym:
    * Obiektów JSON (`dict`).
    * Tablic JSON (`list`) definiujących typ elementów.
    * Pól tekstowych (`str`) określających minimalną i maksymalną długość.
    * Liczb (`int`, `float`) z wartościami minimalnymi, maksymalnymi, itp.

* Walidacja bardziej egzotycznych typów danych, takich jak:
    * URL.
    * Email.
    * UUID.
    * ...i inne.

Cała walidacja jest obsługiwana przez ugruntowaną i solidną bibliotekę **Pydantic**.

### Bezpieczeństwo i uwierzytelnianie

Bezpieczeństwo i uwierzytelnianie jest zintegrowane. Bez żadnych kompromisów z bazami czy modelami danych.

Wszystkie schematy bezpieczeństwa zdefiniowane w OpenAPI, w tym:

* Podstawowy protokół HTTP.
* **OAuth2** (również z **tokenami JWT**). Sprawdź samouczek [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* Klucze API w:
    * Nagłówkach.
    * Parametrach zapytań.
    * Ciasteczkach, itp.

Plus wszystkie funkcje bezpieczeństwa Starlette (włączając w to **session cookies**).

Wszystko zbudowane jako narzędzia i komponenty wielokrotnego użytku, które można łatwo zintegrować z systemami, magazynami oraz bazami danych - relacyjnymi i NoSQL, itp.

### Wstrzykiwanie zależności

FastAPI zawiera niezwykle łatwy w użyciu, ale niezwykle potężny system <abbr title='"Dependency Injection" również znane jako "components", "resources", "services", "providers"'><strong>wstrzykiwania zależności</strong></abbr>.

* Nawet zależności mogą mieć zależności, tworząc hierarchię lub **"graf" zależności**.
* Wszystko **obsługiwane automatycznie** przez framework.
* Wszystkie zależności mogą wymagać danych w żądaniach oraz rozszerzać ograniczenia i automatyczną dokumentację **operacji na ścieżce**.
* **Automatyczna walidacja** parametrów *operacji na ścieżce* zdefiniowanych w zależnościach.
* Obsługa złożonych systemów uwierzytelniania użytkowników, **połączeń z bazami danych**, itp.
* Bazy danych, front end, itp. **bez kompromisów**, ale wciąż łatwe do integracji

### Nieograniczone "wtyczki"

Lub ujmując to inaczej - brak potrzeby wtyczek. Importuj i używaj kod, który potrzebujesz.

Każda integracja została zaprojektowana tak, aby była tak prosta w użyciu (z zależnościami), że możesz utworzyć "wtyczkę" dla swojej aplikacji w 2 liniach kodu, używając tej samej struktury i składni, które są używane w *operacjach na ścieżce*.

### Testy

* 100% <abbr title="Ilość kodu, który jest automatycznie testowany">pokrycia kodu testami</abbr>.
* 100% <abbr title="Deklaracje typów Python - dzięki nim twój edytor i zewnętrzne narzędzia mogą zapewnić Ci lepszą obsługę">adnotacji typów</abbr>.
* Używany w aplikacjach produkcyjnych.

## Funkcje Starlette

**FastAPI** jest w pełni kompatybilny (oraz bazuje na) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Tak więc każdy dodatkowy kod Starlette, który posiadasz, również będzie działał.

`FastAPI` jest w rzeczywitości podklasą `Starlette`, więc jeśli już znasz lub używasz Starlette, większość funkcji będzie działać w ten sam sposób.

Dzięki **FastAPI** otrzymujesz wszystkie funkcje **Starlette** (ponieważ FastAPI to po prostu Starlette na sterydach):

* Bardzo imponująca wydajność. Jest to <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">jeden z najszybszych dostępnych frameworków Pythona, na równi z **NodeJS** i **Go**</a>.
* Wsparcie dla **WebSocket**.
* <abbr title='Zadania wykonywane w tle, bez zatrzymywania żądań, w tym samym procesie. Po angielsku: In-process background tasks'>Zadania w tle</abbr>.
* Zdarzenia startup i shutdown.
* Klient testowy zbudowany na podstawie `requests`.
* **CORS**, GZip, pliki statyczne, streamy.
* Obsługa **sesji i ciasteczek**
* 100% pokrycie testami
* 100% adnotacji typów

## Funkcje Pydantic

**FastAPI** jest w pełni kompatybilny (oraz bazuje na) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Tak więc każdy dodatkowy kod Pydantic, który posiadasz, również będzie działał.

Wliczając w to zewnętrzne biblioteki, również oparte o Pydantic, takie jak <abbr title="Mapowanie obiektowo-relacyjne. Po angielsku: Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr> dla baz danych.

Oznacza to, że w wielu przypadkach możesz przekazać ten sam obiekt, który otrzymasz z żądania **bezpośrednio do bazy danych**, ponieważ wszystko jest walidowane automatycznie.

Działa to również w drugą stronę, w wielu przypadkach możesz po prostu przekazać obiekt otrzymany z bazy danych **bezpośrednio do klienta**.

Dzięki **FastAPI** otrzymujesz wszystkie funkcje **Pydantic** (ponieważ FastAPI bazuje na Pydantic do obsługi wszystkich danych):

* **Bez prania mózgu**:
    * Brak nowego <abbr title="Po angielsku: schema definition micro-language">mikrojęzyka definicji schematu</abbr> do nauki.
    * Jeśli znasz adnotacje typów Pythona to wiesz jak używać Pydantic.
* Dobrze współpracuje z Twoim **<abbr title='Skrót od "Integrated Development Environment", podobne do edytora kodu'>IDE</abbr>/<abbr title="Program, który sprawdza Twój kod pod kątem błędów">linter</abbr>/mózgiem**:
    * Ponieważ struktury danych Pydantic to po prostu instancje klas, które definiujesz; autouzupełnianie, linting, mypy i twoja intuicja powinny działać poprawnie z Twoimi zweryfikowanymi danymi.
* **Szybkość**:
    * w <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">benchmarkach</a> Pydantic jest szybszy niż wszystkie inne testowane biblioteki.
* Walidacja **złożonych struktur**:
    * Wykorzystanie hierarchicznych modeli Pydantic, Pythonowego modułu `typing` zawierającego `List`, `Dict`, itp.
    * Walidatory umożliwiają jasne i łatwe definiowanie, sprawdzanie złożonych struktur danych oraz dokumentowanie ich jako JSON Schema.
    * Możesz mieć głęboko **zagnieżdżone obiekty JSON** i wszystkie je weryfikować i adnotować.
* **Rozszerzalność**:
    * Pydantic umożliwia zdefiniowanie niestandardowych typów danych lub rozszerzenie walidacji o metody na modelu, na których użyty jest dekorator walidatora.
* 100% pokrycie testami
