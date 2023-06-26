# Cechy

## Cechy FastAPI

**FastAPI** zapewnia Ci następujące korzyści:

### Oparcie o standardy open

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> do tworzenia API, w tym deklaracji <abbr title="znane również jako: paths, endpoints, routes">ścieżek</abbr> <abbr title="znane również jako metody HTTP, takie jak POST, GET, PUT, DELETE">operacji</abbr>, parametrów, <abbr title="po angielsku: body requests">ciał zapytań</abbr>, bezpieczeństwa, itp.
* Automatyczna dokumentacja modelu danych za pomocą <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (ponieważ OpenAPI bazuje na JSON Schema).
* Zaprojektowane z myślą o zgodności z powyższymi standardami zamiast dodawania ich obsługi po fakcie.
* Możliwość automatycznego **generowania kodu klienta** w wielu językach.

### Automatyczna dokumentacja

Interaktywna dokumentacja i webowe interfejsy do eksploracji API. Z racji tego, że framework bazuje na OpenAPI, istnieje wiele opcji, z czego 2 są domyślnie dołączone.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, z interaktywnym interfejsem - odpytuj i testuj swoje API bezpośrednio z przeglądarki.

![Swagger UI interakcja](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Alternatywna dokumentacja API z <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Nowoczesny Python

Wszystko opiera się na standardowych deklaracjach typu **Python 3.6** (dzięki Pydantic). Brak nowej składni do uczenia. Po prostu standardowy, współczesny Python.

Jeśli potrzebujesz szybkiego przypomnienia jak używać deklaracji typów w Pythonie (nawet jeśli nie używasz FastAPI), sprawdź krótki samouczek: [Python Types](python-types.md){.internal-link target=_blank}.

Wystarczy, że napiszesz standardowe deklaracje typów Pythona:

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

A one będą mogły zostać później użyte w następujący sposób:

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

Cały framework został zaprojektowany tak, aby był łatwy i intuicyjny w użyciu. Wszystkie pomysły zostały przetestowane na wielu edytorach jeszcze przed rozpoczęciem procesu tworzenia, aby zapewnić najlepsze wrażenia programistyczne.

Ostatnia ankieta <abbr title="coroczna ankieta przeprowadza w środowisku programistów języka Python">Python developer survey</abbr> jasno wskazuje, że <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">najczęściej używaną funkcjonalnością jest autouzupełnianie w edytorze</a>.

Cała struktura frameworku **FastAPI** jest na tym oparta. Autouzupełnianie działa wszędzie.

Rzadko będziesz musiał wracać do dokumentacji.

Oto, jak twój edytor może Ci pomóc:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![wsparcie edytora](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![wsparcie edytora](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Otrzymasz uzupełnienie nawet w miejscach, w których normalnie uzupełnienia nie ma. Na przykład klucz "price" w treści JSON (który mógł być zagnieżdżony), który pochodzi z zapytania.

Koniec z wpisywaniem błędnych nazw kluczy, przechodzeniem tam i z powrotem w dokumentacji lub przewijaniem w górę i w dół, aby sprawdzić, czy w końcu użyłeś nazwy `username` czy `user_name`.

### Zwięzłość

Wszystko posiada sensowne **domyślne wartości**. Wszędzie znajdziesz opcjonalne konfiguracje. Wszystkie parametry możesz dostroić, aby zrobić to co potrzebujesz do zdefiniowania API.

Ale domyślnie wszystko **"po prostu działa"**.

### Walidacja

* Walidacja większości (lub wszystkich?) **typów danych** Pythona, w tym:
    * Obiektów JSON (`dict`).
    * Tablic JSON (`list`) ze zdefiniowanym typem elementów.
    * Pól tekstowych (`str`) z określeniem minimalnej i maksymalnej długości.
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

Plus wszystkie funkcje bezpieczeństwa Starlette (włączając w to **<abbr title="po angielsku: session cookies">ciasteczka sesyjne</abbr>**).

Wszystko zbudowane jako narzędzia i komponenty wielokrotnego użytku, które można łatwo zintegrować z systemami, magazynami oraz bazami danych - relacyjnymi, NoSQL, itp.

### Wstrzykiwanie Zależności

FastAPI zawiera niezwykle łatwy w użyciu, ale niezwykle potężny system <abbr title='Po angielsku: Dependency Injection. Znane również jako "components", "resources", "services", "providers"'><strong>Wstrzykiwania Zależności</strong></abbr>.

* Nawet zależności mogą mieć zależności, tworząc hierarchię lub **"graf" zależności**.
* Wszystko jest **obsługiwane automatycznie** przez framework.
* Wszystkie zależności mogą wymagać danych w żądaniach oraz rozszerzać ograniczenia i automatyczną dokumentację **<abbr title="po angielsku: path operations">operacji na ścieżce</abbr>**.
* **Automatyczna walidacja** parametrów *operacji na ścieżce* zdefiniowanych w zależnościach.
* Obsługa złożonych systemów uwierzytelniania użytkowników, **połączeń z bazami danych**, itp.
* Bazy danych, front end, itp. **bez kompromisów**, ale wciąż łatwe do integracji.

### Nieograniczone "wtyczki"

Lub ujmując to inaczej - brak potrzeby wtyczek. Importuj i używaj kod, który potrzebujesz.

Każda integracja została zaprojektowana tak, aby była tak prosta w użyciu (z zależnościami), że możesz utworzyć "wtyczkę" dla swojej aplikacji w 2 liniach kodu, używając tej samej struktury i składni, które są używane w *operacjach na ścieżce*.

### Testy

* 100% <abbr title="Ilość kodu, który jest automatycznie testowany">pokrycia kodu testami</abbr>.
* 100% <abbr title="Deklaracje typów Python - dzięki nim twój edytor i zewnętrzne narzędzia mogą zapewnić Ci lepsze wsparcie ">adnotacji typów</abbr>.
* Używany w aplikacjach produkcyjnych.

## Cechy Starlette

**FastAPI** jest w pełni kompatybilny z (oraz bazuje na) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. Tak więc każdy dodatkowy kod Starlette, który posiadasz, również będzie działał.

`FastAPI` jest w rzeczywistości podklasą `Starlette`, więc jeśli już znasz lub używasz Starlette, większość funkcji będzie działać w ten sam sposób.

Dzięki **FastAPI** otrzymujesz wszystkie funkcje **Starlette** (ponieważ FastAPI to po prostu Starlette na sterydach):

* Bardzo imponująca wydajność. Jest to <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">jeden z najszybszych dostępnych frameworków Pythona, na równi z **NodeJS** i **Go**</a>.
* Wsparcie dla **WebSocket**.
* <abbr title='Zadania wykonywane w tle, bez zatrzymywania żądań, w tym samym procesie. Po angielsku: In-process background tasks'>Zadania w tle</abbr>.
* Eventy startup i shutdown.
* Klient testowy zbudowany na bazie biblioteki `requests`.
* **CORS**, GZip, pliki statyczne, streamy.
* Obsługa **sesji i ciasteczek**.
* 100% pokrycie testami.
* 100% adnotacji typów.

## Cechy Pydantic

**FastAPI** jest w pełni kompatybilny z (oraz bazuje na) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Tak więc każdy dodatkowy kod Pydantic, który posiadasz, również będzie działał.

Wliczając w to zewnętrzne biblioteki, również oparte o Pydantic, takie jak <abbr title="Mapowanie obiektowo-relacyjne. Po angielsku: Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr> dla baz danych.

Oznacza to, że w wielu przypadkach możesz przekazać ten sam obiekt, który otrzymasz z żądania **bezpośrednio do bazy danych**, ponieważ wszystko jest walidowane automatycznie.

Działa to również w drugą stronę, w wielu przypadkach możesz po prostu przekazać obiekt otrzymany z bazy danych **bezpośrednio do klienta**.

Dzięki **FastAPI** otrzymujesz wszystkie funkcje **Pydantic** (ponieważ FastAPI bazuje na Pydantic do obsługi wszystkich danych):

* **Bez prania mózgu**:
    * Brak nowego mikrojęzyka do definiowania schematu, którego trzeba się nauczyć.
    * Jeśli znasz adnotacje typów Pythona to wiesz jak używać Pydantic.
* Dobrze współpracuje z Twoim **<abbr title='Skrót od "Integrated Development Environment", podobne do edytora kodu'>IDE</abbr>/<abbr title="Program, który sprawdza Twój kod pod kątem błędów">linterem</abbr>/mózgiem**:
    * Ponieważ struktury danych Pydantic to po prostu instancje klas, które definiujesz; autouzupełnianie, linting, mypy i twoja intuicja powinny działać poprawnie z Twoimi zwalidowanymi danymi.
* **Szybkość**:
    * w <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">benchmarkach</a> Pydantic jest szybszy niż wszystkie inne testowane biblioteki.
* Walidacja **złożonych struktur**:
    * Wykorzystanie hierarchicznych modeli Pydantic, Pythonowego modułu `typing` zawierającego `List`, `Dict`, itp.
    * Walidatory umożliwiają jasne i łatwe definiowanie, sprawdzanie złożonych struktur danych oraz dokumentowanie ich jako JSON Schema.
    * Możesz mieć głęboko **zagnieżdżone obiekty JSON** i wszystkie je poddać walidacji i adnotować.
* **Rozszerzalność**:
    * Pydantic umożliwia zdefiniowanie niestandardowych typów danych lub rozszerzenie walidacji o metody na modelu, na których użyty jest dekorator walidatora.
* 100% pokrycie testami.
