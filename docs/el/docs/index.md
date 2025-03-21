# FastAPI

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, υψηλή απόδοση, εύκολο στην εκμάθηση, έτοιμο για χρήση στην παραγωγή</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Tεκμηρίωση κώδικα**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**Πηγαίος κώδικας**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI, είναι ένα σύγχρονο, γρήγορο (υψηλής απόδοσης) web framework για τη δημιουργία API (Advanced Programming Interface | Προηγμένη διεπαφή προγραμματισμού) με Python που βασίζεται σε τυπικές υποδείξεις τύπου Python.

Τα βασικά χαρακτηριστικά είναι:

* **Yψηλή απόδοση**: Στο ίδιο επίπεδο με **NodeJS** και **Go** (χάρη στo Starlette και το Pydantic). [Ένα από τα πιο γρήγορα διαθέσιμα Python web framework](#_11).
* **Γρήγορη κωδικοποίηση**: Αυξάνει την ταχύτητα εγγραφής κώδικα κατά περίπου 200% έως 300%. *
* **Λιγότερα σφάλματα**: Μειώστε περίπου το 40% των σφαλμάτων που προκαλούνται από ανθρώπους (προγραμματιστές). *
* **Διαισθητικό**: Yποστήριξη για <abbr title="γνωστό και ως IntelliSense">βοηθητικά προγράμματα συμπλήρωσης κώδικα</abbr>. Λιγότερος χρόνος αποσφαλμάτωσης.
* **Εύκολο**: Σχεδιασμένο για να είναι εύκολο στη χρήση και στην εκμάθηση. Λιγότερος χρόνος ανάγνωσης εγγράφων.
* **Σύντομο**: Ελαχιστοποιήστε την αντιγραφή κώδικα. Πολλαπλές δυνατότητες από κάθε δήλωση παραμέτρου.
* **Εύρωστο**: Λάβετε κώδικα έτοιμο για παραγωγή. Με αυτόματη διαδραστική τεκμηρίωση.
* **Βασισμένο σε πρότυπα**: Με βάση (και πλήρως συμβατό με) τα ανοιχτά πρότυπα για API: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (παλαιότερα γνωστό ως Swagger) και <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a>.

<small>* εκτίμηση που βασίζεται σε δοκιμές σε μια εσωτερική ομάδα ανάπτυξης, κατά την κατασκευή εφαρμογών παραγωγής.</small>

## Χορηγοί

<!-- sponsors -->

{% if sponsors %}
{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}
{% endif %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/fastapi-people/#sponsors" class="external-link" target="_blank">Άλλοι χορηγοί</a>

## Απόψεις

"_[...] Χρησιμοποιώ το **FastAPI** πολύ συχνά [...] Στην πραγματικότητα σκοπεύω να το χρησιμοποιήσω για όλες τις υπηρεσίες της ομάδας μου **ML services at Microsoft**. Ορισμένα από αυτά ενσωματώνονται στο βασικό προϊόν **Windows** και ορισμένα προϊόντα **Γραφείου**._"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_Υιοθετήσαμε τη βιβλιοθήκη **FastAPI** για να δημιουργήσουμε έναν διακομιστή **REST** που μπορεί να ερωτηθεί για τη λήψη **προβλέψεων**. [για το Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_Το **Netflix** είναι στην ευχάριστη θέση να ανακοινώσει την κυκλοφορία ανοιχτού κώδικα του πλαισίου ενορχήστρωσης **διαχείριση κρίσεων**: **Dispatch**! [κατασκευάστηκε με το **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_Είναι απόλαυση να δημιουργείς εφαρμογές ιστού με το **FastAPI**!_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_Ειλικρινά, αυτό που έχετε φτιάξει φαίνεται εξαιρετικά συμπαγές και γυαλισμένο. Από πολλές απόψεις, είναι αυτό που ήθελα - είναι πραγματικά εμπνευσμένο να βλέπεις κάποιον να το κατασκευάζει._"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_Αν θέλετε να μάθετε ένα **σύγχρονο framework** για τη δημιουργία REST API, ρίξτε μια ματιά στο **FastAPI** [...] Είναι γρήγορο, εύκολο στη χρήση και εύκολο στην εκμάθηση [...]_"

"_Έχουμε αλλάξει στο **FastAPI** για τα **API** [...] Νομίζω ότι θα σου αρέσει [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_Αν κάποιος θέλει να δημιουργήσει ένα Python API παραγωγής, θα συνιστούσα ανεπιφύλακτα το **FastAPI**. Είναι **όμορφα σχεδιασμένο**, **απλό στη χρήση** και **πολύ επεκτάσιμο**, έχει γίνει **βασικό συστατικό** στην πρώτη στρατηγική ανάπτυξης του API και οδηγεί πολλούς αυτοματισμούς και υπηρεσίες, όπως το Virtual TAC Engineer._"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, το FastAPI των CLI

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Εάν δημιουργείτε μια εφαρμογή <abbr title="Command Line Interface">CLI</abbr> που θα χρησιμοποιείται στο τερματικό αντί για ένα web API, ρίξτε μια ματιά <a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>.

Ο **Typer** είναι το μικρό αδερφάκι του FastAPI. Και προορίζεται να είναι το **FastAPI των CLI**. ⌨️ 🚀

## Απαιτήσεις

Το FastAPI στέκεται στους ώμους γιγάντων:

* <a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a> για τα τμήματα Ιστού.
* <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> για τα μέρη δεδομένων.

## Εγκατάσταση

Δημιουργήστε και ενεργοποιήστε ένα <a href="https://fastapi.tiangolo.com/virtual-environments/" class="external-link" target="_blank">εικονικό περιβάλλον</a> και στη συνέχεια εγκαταστήστε το FastAPI:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**Σημείωση**: Βεβαιωθείτε ότι έχετε βάλει το `"fastapi[standard]"` σε εισαγωγικά για να διασφαλίσετε ότι λειτουργεί σε όλα τα τερματικά.
## Παράδειγμα

### Δημιουργήστε το

* Δημιουργήστε ένα αρχείο `main.py` με:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>Ή χρησιμοποιήστε <code>async def</code>...</summary>

Αν ο κώδικάς σας χρησιμοποιεί `async` / `await`, χρησιμοποιήστε `async def`:

```Python hl_lines="9  14"
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Σημείωση**:

Αν δεν γνωρίζετε, ελέγξτε την ενότητα _"Βιάζεστε?"_ σχετικά με <a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">`async` και `await` στις τεκμηριώσεις</a>.

</details>

### Εκτελέστε το

Εκτελέστε τον διακομιστή με:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary>Σχετικά με την εντολή <code>fastapi dev main.py</code>...</summary>

Η εντολή `fastapi dev` διαβάζει το αρχείο σας `main.py`, ανιχνεύει την εφαρμογή **FastAPI** μέσα σε αυτό και εκκινεί έναν διακομιστή χρησιμοποιώντας το <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>.

Από προεπιλογή, το `fastapi dev` θα ξεκινήσει με ενεργοποιημένη την αυτόματη επαναφόρτωση για τοπική ανάπτυξη.

Μπορείτε να διαβάσετε περισσότερα σχετικά με αυτό στις <a href="https://fastapi.tiangolo.com/fastapi-cli/" target="_blank">τεκμηριώσεις του CLI του FastAPI</a>.

</details>

### Ελέγξτε το

Ανοίξτε τον περιηγητή σας στη διεύθυνση <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>.

Θα δείτε την απόκριση JSON ως εξής:

```JSON
{"item_id": 5, "q": "somequery"}
```

Έχετε ήδη δημιουργήσει ένα API που:

* Δέχεται αιτήματα HTTP στις _διαδρομές_ `/` και `/items/{item_id}`.
* Και οι δύο _διαδρομές_ χρησιμοποιούν <em>λειτουργίες</em> `GET` (γνωστές και ως HTTP _μέθοδοι_).
* Η _διαδρομή_ `/items/{item_id}` έχει μια _παράμετρο διαδρομής_ `item_id` που πρέπει να είναι `int`.
* Η _διαδρομή_ `/items/{item_id}` διαθέτει προαιρετική _παράμετρο ερωτήματος_ `q` που είναι `str`.

### Διαδραστική τεκμηρίωση API

Τώρα μεταβείτε στη διεύθυνση <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Θα δείτε την αυτόματη διαδραστική τεκμηρίωση API (παρέχεται από το <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Εναλλακτική τεκμηρίωση API

Και τώρα, μεταβείτε στη διεύθυνση <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Θα δείτε την εναλλακτική αυτόματη τεκμηρίωση (παρέχεται από το <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Παράδειγμα αναβάθμισης

Τώρα τροποποιήστε το αρχείο `main.py` ώστε να δέχεται ένα σώμα από ένα αίτημα `PUT`.

Ορίστε το σώμα χρησιμοποιώντας τυπικούς τύπους Python, χάρη στο Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

Ο διακομιστής `fastapi dev` θα πρέπει να επανεκκινηθεί αυτόματα.

### Αναβάθμιση διαδραστικής τεκμηρίωσης API

Τώρα μεταβείτε στη διεύθυνση <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

* Η διαδραστική τεκμηρίωση API θα ενημερωθεί αυτόματα, συμπεριλαμβάνοντας το νέο σώμα:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Κάντε κλικ στο κουμπί "Try it out", το οποίο σας επιτρέπει να συμπληρώσετε τις παραμέτρους και να αλληλεπιδράσετε απευθείας με το API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Στη συνέχεια, κάντε κλικ στο κουμπί "Execute", η διεπαφή χρήστη θα επικοινωνήσει με το API σας, θα στείλει τις παραμέτρους, θα λάβει τα αποτελέσματα και θα τα εμφανίσει στην οθόνη:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Αναβάθμιση εναλλακτικής τεκμηρίωσης API

Και τώρα, μεταβείτε στη διεύθυνση <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

* Η εναλλακτική τεκμηρίωση θα αντικατοπτρίζει επίσης τη νέα παράμετρο ερωτήματος και το σώμα:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Ανακεφαλαίωση

Συνοψίζοντας, δηλώνετε **μία φορά** τους τύπους παραμέτρων, σώματος κ.λπ. ως παραμέτρους συναρτήσεων.

Και αυτό το κάνετε χρησιμοποιώντας τους τυπικούς, σύγχρονους τύπους της Python.

Δεν χρειάζεται να μάθετε νέα σύνταξη, μεθόδους ή κλάσεις μιας συγκεκριμένης βιβλιοθήκης, κ.λπ.

Απλά την τυπική **Python**.

Για παράδειγμα, για έναν `int`:

```Python
item_id: int
```

ή για ένα πιο σύνθετο μοντέλο `Item`:

```Python
item: Item
```

...και με αυτήν τη μοναδική δήλωση έχετε:

* Υποστήριξη από τον συντάκτη, συμπεριλαμβανομένων:
    * Συμπλήρωσης.
    * Ελέγχων τύπου.
* Επικύρωση δεδομένων:
    * Αυτόματα και σαφή σφάλματα όταν τα δεδομένα είναι μη έγκυρα.
    * Επικύρωση ακόμη και για βαθιά φωλιασμένα αντικείμενα JSON.
* <abbr title="γνωστό και ως: serialization, parsing, marshalling">Μετατροπή</abbr> δεδομένων εισόδου: από το δίκτυο σε δεδομένα και τύπους Python. Ανάγνωση από:
    * JSON.
    * Path parameters (Παραμέτρους διαδρομής).
    * Query parameters (Παραμέτρους ερωτήματος).
    * Cookies.
    * Headers.
    * Forms (Φόρμες).
    * Files (Αρχεία).
* <abbr title="γνωστό και ως: serialization, parsing, marshalling">Μετατροπή</abbr> δεδομένων εξόδου: μετατροπή από δεδομένα και τύπους Python σε δεδομένα δικτύου (ως JSON):
    * Μετατροπή τύπων Python (`str`, `int`, `float`, `bool`, `list`, κ.λπ.).
    * Αντικείμενα `datetime`.
    * Αντικείμενα `UUID`.
    * Μοντέλα βάσης δεδομένων.
    * ...και πολλά περισσότερα.
* Αυτόματη διαδραστική τεκμηρίωση API, συμπεριλαμβανομένων 2 εναλλακτικών διεπαφών χρήστη:
    * Swagger UI.
    * ReDoc.

---

Επιστρέφοντας στο προηγούμενο παράδειγμα κώδικα, το **FastAPI** θα:

* Επικυρώνει ότι υπάρχει ένα `item_id` στη διαδρομή για αιτήματα `GET` και `PUT`.
* Επικυρώνει ότι το `item_id` είναι τύπου `int` για αιτήματα `GET` και `PUT`.
    * Εάν δεν είναι, ο πελάτης θα βλέπει ένα χρήσιμο, σαφές σφάλμα.
* Ελέγχει αν υπάρχει μια προαιρετική παράμετρος ερωτήματος με όνομα `q` (όπως στο `http://127.0.0.1:8000/items/foo?q=somequery`) για αιτήματα `GET`.
    * Δεδομένου ότι η παράμετρος `q` έχει δηλωθεί με `= None`, είναι προαιρετική.
    * Χωρίς το `None`, θα ήταν υποχρεωτική (όπως είναι το σώμα στην περίπτωση του `PUT`).
* Για αιτήματα `PUT` στη διαδρομή `/items/{item_id}`, διαβάζει το σώμα ως JSON:
    * Ελέγχει ότι έχει ένα υποχρεωτικό χαρακτηριστικό `name` που θα πρέπει να είναι `str`.
    * Ελέγχει ότι έχει ένα υποχρεωτικό χαρακτηριστικό `price` που πρέπει να είναι `float`.
    * Ελέγχει ότι έχει ένα προαιρετικό χαρακτηριστικό `is_offer`, το οποίο θα πρέπει να είναι `bool` (αν υπάρχει).
    * Όλα αυτά ισχύουν επίσης για βαθιά φωλιασμένα αντικείμενα JSON.
* Μετατρέπει από και προς JSON αυτόματα.
* Τεκμηριώνει τα πάντα με το OpenAPI, το οποίο μπορεί να χρησιμοποιηθεί από:
    * Διαδραστικά συστήματα τεκμηρίωσης.
    * Συστήματα αυτόματης δημιουργίας κώδικα πελάτη, για πολλές γλώσσες.
* Παρέχει 2 διαδραστικές διεπαφές ιστού για τεκμηρίωση απευθείας.

---

Μόλις αγγίξαμε την επιφάνεια, αλλά ήδη καταλαβαίνετε την ιδέα για το πώς λειτουργούν όλα.

Δοκιμάστε να αλλάξετε τη γραμμή με:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...από:

```Python
        ... "item_name": item.name ...
```

...προς:

```Python
        ... "item_price": item.price ...
```

...και δείτε πώς ο συντάκτης σας θα ολοκληρώνει αυτόματα τα χαρακτηριστικά και θα γνωρίζει τους τύπους τους:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

Για ένα πιο ολοκληρωμένο παράδειγμα που περιλαμβάνει περισσότερες δυνατότητες, δείτε τον <a href="https://fastapi.tiangolo.com/tutorial/">Οδηγό χρήσης</a>.

**Προσοχή**: ο οδηγός χρήσης περιλαμβάνει:


* Δήλωση **παραμέτρων** από διαφορετικά σημεία όπως: **headers**, **cookies**, **πεδία φόρμας** και **αρχεία**.
* Πώς να ορίσετε **περιορισμούς επικύρωσης**, όπως `maximum_length` ή `regex`.
* Ένα πολύ ισχυρό και εύκολο στη χρήση σύστημα **<abbr title="συχνά αποκαλείται και components, resources, providers, services, injectables">Εισαγωγής Εξαρτήσεων</abbr>**.
* Ασφάλεια και αυθεντικοποίηση, συμπεριλαμβανομένης της υποστήριξης για **OAuth2** με **JWT tokens** και **HTTP Basic** αυθεντικοποίηση.
* Πιο προχωρημένες (αλλά εξίσου εύκολες) τεχνικές για τη δήλωση **βαθιά φωλιασμένων JSON μοντέλων** (χάρη στο Pydantic).
* Ενσωμάτωση **GraphQL** με το <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> και άλλες βιβλιοθήκες.
* Πολλές επιπλέον δυνατότητες (χάρη στο Starlette) όπως:
    * **WebSockets**
    * εξαιρετικά εύκολα τεστ βασισμένα σε HTTPX και `pytest`
    * **CORS**
    * **Cookie Sessions**
    * ...και πολλά άλλα.

## Απόδοση

Ανεξάρτητα benchmarks από το TechEmpower δείχνουν ότι οι εφαρμογές **FastAPI** που τρέχουν με Uvicorn είναι <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">από τα ταχύτερα διαθέσιμα Python frameworks</a>, μόνο κάτω από τα ίδια τα Starlette και Uvicorn (που χρησιμοποιούνται εσωτερικά από το FastAPI). (*)

Για να κατανοήσετε περισσότερα, δείτε την ενότητα <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Εξαρτήσεις

Το FastAPI εξαρτάται από τα Pydantic και Starlette.

### `standard` Εξαρτήσεις

Όταν εγκαθιστάτε το FastAPI με την εντολή `pip install "fastapi[standard]"` περιλαμβάνει την ομάδα `standard` προαιρετικών εξαρτήσεων:

Χρησιμοποιούνται από το Pydantic:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - για επικύρωση email.

Χρησιμοποιούνται από το Starlette:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - Απαραίτητο αν θέλετε να χρησιμοποιήσετε το `TestClient`.
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - Απαραίτητο αν θέλετε να χρησιμοποιήσετε την προεπιλεγμένη ρύθμιση για templates.
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - Απαραίτητο αν θέλετε να υποστηρίξετε <abbr title="μετατροπή του string που προέρχεται από αίτημα HTTP σε δεδομένα Python">"ανάλυση"</abbr> φορμών με το `request.form()`.

Χρησιμοποιούνται από FastAPI / Starlette:

* <a href="https://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - για τον server που φορτώνει και εξυπηρετεί την εφαρμογή σας. Αυτό περιλαμβάνει το `uvicorn[standard]`, το οποίο περιέχει ορισμένες εξαρτήσεις (π.χ. `uvloop`) που απαιτούνται για υψηλή απόδοση εξυπηρέτησης.
* `fastapi-cli` - για την παροχή της εντολής `fastapi`.

### Χωρίς τις `standard` Εξαρτήσεις

Αν δεν θέλετε να συμπεριλάβετε τις προαιρετικές εξαρτήσεις `standard`, μπορείτε να εγκαταστήσετε με `pip install fastapi` αντί για `pip install "fastapi[standard]"`.

### Πρόσθετες Προαιρετικές Εξαρτήσεις

Υπάρχουν ορισμένες πρόσθετες εξαρτήσεις που μπορεί να θέλετε να εγκαταστήσετε.

Πρόσθετες προαιρετικές εξαρτήσεις για Pydantic:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - για τη διαχείριση ρυθμίσεων.
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - για πρόσθετους τύπους που μπορούν να χρησιμοποιηθούν με το Pydantic.

Πρόσθετες προαιρετικές εξαρτήσεις για το FastAPI:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Απαραίτητο αν θέλετε να χρησιμοποιήσετε το `ORJSONResponse`.
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Απαραίτητο αν θέλετε να χρησιμοποιήσετε το `UJSONResponse`.

## Άδεια Χρήσης

Αυτό το έργο διανέμεται υπό τους όρους της άδειας MIT.
