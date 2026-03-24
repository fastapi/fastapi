# Nebenläufigkeit und async / await { #concurrency-and-async-await }

Details zur `async def`-Syntax für *Pfadoperation-Funktionen* und Hintergrundinformationen zu asynchronem Code, Nebenläufigkeit und Parallelität.

## In Eile? { #in-a-hurry }

<abbr title="too long; didn't read - Zu lang; nicht gelesen"><strong>TL;DR:</strong></abbr>

Wenn Sie Bibliotheken von Dritten verwenden, die mit `await` aufgerufen werden müssen, wie zum Beispiel:

```Python
results = await some_library()
```

Dann deklarieren Sie Ihre *Pfadoperation-Funktionen* mit `async def`, wie in:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Hinweis

Sie können `await` nur innerhalb von Funktionen verwenden, die mit `async def` erstellt wurden.

///

---

Wenn Sie eine Bibliothek eines Dritten verwenden, die mit etwas kommuniziert (einer Datenbank, einer API, dem Dateisystem, usw.) und welche die Verwendung von `await` nicht unterstützt (dies ist derzeit bei den meisten Datenbankbibliotheken der Fall), dann deklarieren Sie Ihre *Pfadoperation-Funktionen* ganz normal nur mit `def`, wie in:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Wenn Ihre Anwendung (irgendwie) nicht mit etwas anderem kommunizieren und auf dessen Antwort warten muss, verwenden Sie `async def`, auch wenn Sie `await` im Inneren nicht verwenden müssen.

---

Wenn Sie sich unsicher sind, verwenden Sie einfach `def`.

---

**Hinweis**: Sie können `def` und `async def` in Ihren *Pfadoperation-Funktionen* beliebig mischen, so wie Sie es benötigen, und jede einzelne Funktion in der für Sie besten Variante erstellen. FastAPI wird damit das Richtige tun.

Wie dem auch sei, in jedem der oben genannten Fälle wird FastAPI immer noch asynchron arbeiten und extrem schnell sein.

Wenn Sie jedoch den oben genannten Schritten folgen, können einige Performanz-Optimierungen vorgenommen werden.

## Technische Details { #technical-details }

Moderne Versionen von Python unterstützen **„asynchronen Code“** unter Verwendung sogenannter **„Coroutinen“** mithilfe der Syntax **`async` und `await`**.

Nehmen wir obigen Satz in den folgenden Abschnitten Schritt für Schritt unter die Lupe:

* **Asynchroner Code**
* **`async` und `await`**
* **Coroutinen**

## Asynchroner Code { #asynchronous-code }

Asynchroner Code bedeutet lediglich, dass die Sprache 💬 eine Möglichkeit hat, dem Computer / Programm 🤖 mitzuteilen, dass es 🤖 an einem bestimmten Punkt im Code darauf warten muss, dass *etwas anderes* irgendwo anders fertig wird. Nehmen wir an, *etwas anderes* ist hier „Langsam-Datei“ 📝.

Während der Zeit, die „Langsam-Datei“ 📝 benötigt, kann das System also andere Aufgaben erledigen.

Dann kommt der Computer / das Programm 🤖 bei jeder Gelegenheit zurück, weil es entweder wieder wartet oder wann immer es 🤖 die ganze Arbeit erledigt hat, die zu diesem Zeitpunkt zu tun war. Und es 🤖 wird nachschauen, ob eine der Aufgaben, auf die es gewartet hat, fertig ist.

Dann nimmt es 🤖 die erste erledigte Aufgabe (sagen wir, unsere „Langsam-Datei“ 📝) und bearbeitet sie weiter.

Das „Warten auf etwas anderes“ bezieht sich normalerweise auf <abbr title="Input and Output - Eingabe und Ausgabe">I/O</abbr>-Operationen, die relativ „langsam“ sind (im Vergleich zur Geschwindigkeit des Prozessors und des Arbeitsspeichers), wie etwa das Warten darauf, dass:

* die Daten des Clients über das Netzwerk empfangen wurden
* die von Ihrem Programm gesendeten Daten vom Client über das Netzwerk empfangen wurden
* der Inhalt einer Datei vom System von der Festplatte gelesen und an Ihr Programm übergeben wurde
* der Inhalt, den Ihr Programm dem System übergeben hat, auf die Festplatte geschrieben wurde
* eine Remote-API-Operation beendet wurde
* Eine Datenbankoperation abgeschlossen wurde
* eine Datenbankabfrage die Ergebnisse zurückgegeben hat
* usw.

Da die Ausführungszeit hier hauptsächlich durch das Warten auf <abbr title="Input and Output - Eingabe und Ausgabe">I/O</abbr>-Operationen verbraucht wird, nennt man dies auch „I/O-lastige“ („I/O bound“) Operationen.

„Asynchron“, sagt man, weil der Computer / das Programm nicht mit einer langsamen Aufgabe „synchronisiert“ werden muss und nicht auf den genauen Moment warten muss, in dem die Aufgabe beendet ist, ohne dabei etwas zu tun, um schließlich das Ergebnis der Aufgabe zu übernehmen und die Arbeit fortsetzen zu können.

Da es sich stattdessen um ein „asynchrones“ System handelt, kann die Aufgabe nach Abschluss ein wenig (einige Mikrosekunden) in der Schlange warten, bis der Computer / das Programm seine anderen Dinge erledigt hat und zurückkommt, um die Ergebnisse entgegenzunehmen und mit ihnen weiterzuarbeiten.

Für „synchron“ (im Gegensatz zu „asynchron“) wird auch oft der Begriff „sequentiell“ verwendet, da der Computer / das Programm alle Schritte in einer Sequenz („der Reihe nach“) ausführt, bevor es zu einer anderen Aufgabe wechselt, auch wenn diese Schritte mit Warten verbunden sind.

### Nebenläufigkeit und Hamburger { #concurrency-and-burgers }

Diese oben beschriebene Idee von **asynchronem** Code wird manchmal auch **„Nebenläufigkeit“** genannt. Sie unterscheidet sich von **„Parallelität“**.

**Nebenläufigkeit** und **Parallelität** beziehen sich beide auf „verschiedene Dinge, die mehr oder weniger gleichzeitig passieren“.

Aber die Details zwischen *Nebenläufigkeit* und *Parallelität* sind ziemlich unterschiedlich.

Um den Unterschied zu erkennen, stellen Sie sich die folgende Geschichte über Hamburger vor:

### Nebenläufige Hamburger { #concurrent-burgers }

Sie gehen mit Ihrem Schwarm Fastfood holen, stehen in der Schlange, während der Kassierer die Bestellungen der Leute vor Ihnen entgegennimmt. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Dann sind Sie an der Reihe und Sie bestellen zwei sehr schmackhafte Burger für Ihren Schwarm und Sie. 🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

Der Kassierer sagt etwas zum Koch in der Küche, damit dieser weiß, dass er Ihre Burger zubereiten muss (obwohl er gerade die für die vorherigen Kunden zubereitet).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Sie bezahlen. 💸

Der Kassierer gibt Ihnen die Nummer Ihrer Bestellung.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Während Sie warten, suchen Sie sich mit Ihrem Schwarm einen Tisch aus, Sie sitzen da und reden lange mit Ihrem Schwarm (da Ihre Burger sehr aufwändig sind und die Zubereitung einige Zeit dauert).

Während Sie mit Ihrem Schwarm am Tisch sitzen und auf die Burger warten, können Sie die Zeit damit verbringen, zu bewundern, wie großartig, süß und klug Ihr Schwarm ist ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Während Sie warten und mit Ihrem Schwarm sprechen, überprüfen Sie von Zeit zu Zeit die auf dem Zähler angezeigte Nummer, um zu sehen, ob Sie bereits an der Reihe sind.

Dann, irgendwann, sind Sie endlich an der Reihe. Sie gehen zur Theke, holen sich die Burger und kommen zurück an den Tisch.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Sie und Ihr Schwarm essen die Burger und haben eine schöne Zeit. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info | Info

Die wunderschönen Illustrationen stammen von [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

Stellen Sie sich vor, Sie wären der Computer / das Programm 🤖 in dieser Geschichte.

Während Sie an der Schlange stehen, sind Sie einfach untätig 😴, warten darauf, dass Sie an die Reihe kommen, und tun nichts sehr „Produktives“. Aber die Schlange ist schnell abgearbeitet, weil der Kassierer nur die Bestellungen entgegennimmt (und nicht zubereitet), also ist das vertretbar.

Wenn Sie dann an der Reihe sind, erledigen Sie tatsächliche „produktive“ Arbeit, Sie gehen das Menü durch, entscheiden sich, was Sie möchten, bekunden Ihre und die Wahl Ihres Schwarms, bezahlen, prüfen, ob Sie die richtige Menge Geld oder die richtige Karte geben, prüfen, ob die Rechnung korrekt ist, prüfen, dass die Bestellung die richtigen Artikel enthält, usw.

Aber dann, auch wenn Sie Ihre Burger noch nicht haben, ist Ihre Interaktion mit dem Kassierer erst mal „auf Pause“ ⏸, weil Sie warten müssen 🕙, bis Ihre Burger fertig sind.

Aber wenn Sie sich von der Theke entfernt haben und mit der Nummer für die Bestellung an einem Tisch sitzen, können Sie Ihre Aufmerksamkeit auf Ihren Schwarm lenken und an dieser Aufgabe „arbeiten“ ⏯ 🤓. Sie machen wieder etwas sehr „Produktives“ und flirten mit Ihrem Schwarm 😍.

Dann sagt der Kassierer 💁 „Ich bin mit dem Burger fertig“, indem er Ihre Nummer auf dem Display über der Theke anzeigt, aber Sie springen nicht sofort wie verrückt auf, wenn das Display auf Ihre Nummer springt. Sie wissen, dass niemand Ihnen Ihre Burger wegnimmt, denn Sie haben die Nummer Ihrer Bestellung, und andere Leute haben andere Nummern.

Also warten Sie darauf, dass Ihr Schwarm ihre Geschichte zu Ende erzählt (die aktuelle Arbeit ⏯ / bearbeitete Aufgabe beendet 🤓), lächeln sanft und sagen, dass Sie die Burger holen ⏸.

Dann gehen Sie zur Theke 🔀, zur ursprünglichen Aufgabe, die nun erledigt ist ⏯, nehmen die Burger auf, sagen Danke, und bringen sie zum Tisch. Damit ist dieser Schritt / diese Aufgabe der Interaktion mit der Theke abgeschlossen ⏹. Das wiederum schafft eine neue Aufgabe, „Burger essen“ 🔀 ⏯, aber die vorherige Aufgabe „Burger holen“ ist erledigt ⏹.

### Parallele Hamburger { #parallel-burgers }

Stellen wir uns jetzt vor, dass es sich hierbei nicht um „nebenläufige Hamburger“, sondern um „parallele Hamburger“ handelt.

Sie gehen los mit Ihrem Schwarm, um paralleles Fast Food zu bekommen.

Sie stehen in der Schlange, während mehrere (sagen wir acht) Kassierer, die gleichzeitig Köche sind, die Bestellungen der Leute vor Ihnen entgegennehmen.

Alle vor Ihnen warten darauf, dass ihre Burger fertig sind, bevor sie die Theke verlassen, denn jeder der 8 Kassierer geht los und bereitet den Burger sofort zu, bevor er die nächste Bestellung entgegennimmt.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Dann sind Sie endlich an der Reihe und bestellen zwei sehr leckere Burger für Ihren Schwarm und Sie.

Sie zahlen 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

Der Kassierer geht in die Küche.

Sie warten, vor der Theke stehend 🕙, damit niemand außer Ihnen Ihre Burger entgegennimmt, da es keine Nummern für die Reihenfolge gibt.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Da Sie und Ihr Schwarm damit beschäftigt sind, niemanden vor sich zu lassen, der Ihre Burger nimmt, wenn sie ankommen, können Sie Ihrem Schwarm keine Aufmerksamkeit schenken. 😞

Das ist „synchrone“ Arbeit, Sie sind mit dem Kassierer/Koch „synchronisiert“ 👨‍🍳. Sie müssen warten 🕙 und genau in dem Moment da sein, in dem der Kassierer/Koch 👨‍🍳 die Burger zubereitet hat und Ihnen gibt, sonst könnte jemand anderes sie nehmen.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Dann kommt Ihr Kassierer/Koch 👨‍🍳 endlich mit Ihren Burgern zurück, nachdem Sie lange vor der Theke gewartet 🕙 haben.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Sie nehmen Ihre Burger und gehen mit Ihrem Schwarm an den Tisch.

Sie essen sie und sind fertig. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Es wurde nicht viel geredet oder geflirtet, da die meiste Zeit mit Warten 🕙 vor der Theke verbracht wurde. 😞

/// info | Info

Die wunderschönen Illustrationen stammen von [Ketrina Thompson](https://www.instagram.com/ketrinadrawsalot). 🎨

///

---

In diesem Szenario der parallelen Hamburger sind Sie ein Computersystem / Programm 🤖 mit zwei Prozessoren (Sie und Ihr Schwarm), die beide warten 🕙 und ihre Aufmerksamkeit darauf verwenden, „lange Zeit vor der Theke zu warten“ 🕙.

Der Fast-Food-Laden verfügt über 8 Prozessoren (Kassierer/Köche). Während der nebenläufige Burger-Laden nur zwei hatte (einen Kassierer und einen Koch).

Dennoch ist das schlussendliche Benutzererlebnis nicht das Beste. 😞

---

Dies wäre die parallele äquivalente Geschichte für Hamburger. 🍔

Für ein „realeres“ Beispiel hierfür, stellen Sie sich eine Bank vor.

Bis vor kurzem hatten die meisten Banken mehrere Kassierer 👨‍💼👨‍💼👨‍💼👨‍💼 und eine große Warteschlange 🕙🕙🕙🕙🕙🕙🕙🕙.

Alle Kassierer erledigen die ganze Arbeit mit einem Kunden nach dem anderen 👨‍💼⏯.

Und man muss lange in der Schlange warten 🕙 sonst kommt man nicht an die Reihe.

Sie würden Ihren Schwarm 😍 wahrscheinlich nicht mitnehmen wollen, um Besorgungen bei der Bank zu erledigen 🏦.

### Hamburger Schlussfolgerung { #burger-conclusion }

In diesem Szenario „Fastfood-Burger mit Ihrem Schwarm“ ist es viel sinnvoller, ein nebenläufiges System zu haben ⏸🔀⏯, da viel gewartet wird 🕙.

Das ist auch bei den meisten Webanwendungen der Fall.

Viele, viele Benutzer, aber Ihr Server wartet 🕙 darauf, dass deren nicht so gute Internetverbindungen die <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr> übermitteln.

Und dann wieder warten 🕙, bis die <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Responses</abbr> zurückkommen.

Dieses „Warten“ 🕙 wird in Mikrosekunden gemessen, aber zusammenfassend lässt sich sagen, dass am Ende eine Menge gewartet wird.

Deshalb ist es sehr sinnvoll, asynchronen ⏸🔀⏯ Code für Web-APIs zu verwenden.

Diese Art der Asynchronität hat NodeJS populär gemacht (auch wenn NodeJS nicht parallel ist) und darin liegt die Stärke von Go als Programmiersprache.

Und das ist das gleiche Leistungsniveau, das Sie mit **FastAPI** erhalten.

Und da Sie Parallelität und Asynchronität gleichzeitig haben können, erzielen Sie eine höhere Performanz als die meisten getesteten NodeJS-Frameworks und sind mit Go auf Augenhöhe, einer kompilierten Sprache, die näher an C liegt [(alles dank Starlette)](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1).

### Ist Nebenläufigkeit besser als Parallelität? { #is-concurrency-better-than-parallelism }

Nein! Das ist nicht die Moral der Geschichte.

Nebenläufigkeit unterscheidet sich von Parallelität. Und sie ist besser bei **bestimmten** Szenarien, die viel Warten erfordern. Aus diesem Grund ist sie im Allgemeinen viel besser als Parallelität für die Entwicklung von Webanwendungen. Aber das stimmt nicht für alle Anwendungen.

Um die Dinge auszugleichen, stellen Sie sich die folgende Kurzgeschichte vor:

> Sie müssen ein großes, schmutziges Haus aufräumen.

*Yup, das ist die ganze Geschichte*.

---

Es gibt kein Warten 🕙, nur viel Arbeit an mehreren Stellen im Haus.

Sie könnten wie im Hamburger-Beispiel hin- und herspringen, zuerst das Wohnzimmer, dann die Küche, aber da Sie auf nichts warten 🕙, sondern nur putzen und putzen, hätte das Hin- und Herspringen keine Auswirkungen.

Es würde mit oder ohne Hin- und Herspringen (Nebenläufigkeit) die gleiche Zeit in Anspruch nehmen, um fertig zu werden, und Sie hätten die gleiche Menge an Arbeit erledigt.

Aber wenn Sie in diesem Fall die acht Ex-Kassierer/Köche/jetzt Reinigungskräfte mitbringen würden und jeder von ihnen (plus Sie) würde einen Bereich des Hauses reinigen, könnten Sie die ganze Arbeit **parallel** erledigen, und würden mit dieser zusätzlichen Hilfe viel schneller fertig werden.

In diesem Szenario wäre jede einzelne Reinigungskraft (einschließlich Ihnen) ein Prozessor, der seinen Teil der Arbeit erledigt.

Und da die meiste Ausführungszeit durch tatsächliche Arbeit (anstatt durch Warten) in Anspruch genommen wird und die Arbeit in einem Computer von einer <abbr title="Central Processing Unit - Zentrale Recheneinheit">CPU</abbr> erledigt wird, werden diese Probleme als „CPU-lastig“ („CPU bound“) bezeichnet.

---

Typische Beispiele für CPU-lastige Vorgänge sind Dinge, die komplexe mathematische Berechnungen erfordern.

Zum Beispiel:

* **Audio-** oder **Bildbearbeitung**.
* **Computer Vision**: Ein Bild besteht aus Millionen von Pixeln, jedes Pixel hat 3 Werte / Farben, die Verarbeitung erfordert normalerweise, Berechnungen mit diesen Pixeln durchzuführen, alles zur gleichen Zeit.
* **Maschinelles Lernen**: Normalerweise sind viele „Matrix“- und „Vektor“-Multiplikationen erforderlich. Stellen Sie sich eine riesige Tabelle mit Zahlen vor, in der Sie alle Zahlen gleichzeitig multiplizieren.
* **Deep Learning**: Dies ist ein Teilgebiet des maschinellen Lernens, daher gilt das Gleiche. Es ist nur so, dass es nicht eine einzige Tabelle mit Zahlen zum Multiplizieren gibt, sondern eine riesige Menge davon, und in vielen Fällen verwendet man einen speziellen Prozessor, um diese Modelle zu erstellen und / oder zu verwenden.

### Nebenläufigkeit + Parallelität: Web + maschinelles Lernen { #concurrency-parallelism-web-machine-learning }

Mit **FastAPI** können Sie die Vorteile der Nebenläufigkeit nutzen, die in der Webentwicklung weit verbreitet ist (derselbe Hauptvorteil von NodeJS).

Sie können aber auch die Vorteile von Parallelität und Multiprocessing (mehrere Prozesse werden parallel ausgeführt) für **CPU-lastige** Workloads wie in Systemen für maschinelles Lernen nutzen.

Dies und die einfache Tatsache, dass Python die Hauptsprache für **Data Science**, maschinelles Lernen und insbesondere Deep Learning ist, machen FastAPI zu einem sehr passenden Werkzeug für Web-APIs und Anwendungen für Data Science / maschinelles Lernen (neben vielen anderen).

Wie Sie diese Parallelität in der Produktion erreichen, erfahren Sie im Abschnitt über [Deployment](deployment/index.md).

## `async` und `await` { #async-and-await }

Moderne Versionen von Python verfügen über eine sehr intuitive Möglichkeit, asynchronen Code zu schreiben. Dadurch sieht es wie normaler „sequentieller“ Code aus und übernimmt im richtigen Moment das „Warten“ für Sie.

Wenn es einen Vorgang gibt, der erfordert, dass gewartet wird, bevor die Ergebnisse zurückgegeben werden, und der diese neue Python-Funktionalität unterstützt, können Sie ihn wie folgt schreiben:

```Python
burgers = await get_burgers(2)
```

Der Schlüssel hier ist das `await`. Es teilt Python mit, dass es warten ⏸ muss, bis `get_burgers(2)` seine Aufgabe erledigt hat 🕙, bevor die Ergebnisse in `burgers` gespeichert werden. Damit weiß Python, dass es in der Zwischenzeit etwas anderes tun kann 🔀 ⏯ (z. B. einen weiteren Request empfangen).

Damit `await` funktioniert, muss es sich in einer Funktion befinden, die diese Asynchronität unterstützt. Dazu deklarieren Sie sie einfach mit `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Mache hier etwas Asynchrones, um die Burger zu erstellen
    return burgers
```

... statt mit `def`:

```Python hl_lines="2"
# Dies ist nicht asynchron
def get_sequential_burgers(number: int):
    # Mache hier etwas Sequentielles, um die Burger zu erstellen
    return burgers
```

Mit `async def` weiß Python, dass es innerhalb dieser Funktion auf `await`-Ausdrücke achten muss und dass es die Ausführung dieser Funktion „anhalten“ ⏸ und etwas anderes tun kann 🔀, bevor es zurückkommt.

Wenn Sie eine `async def`-Funktion aufrufen möchten, müssen Sie sie „erwarten“ („await“). Das folgende wird also nicht funktionieren:

```Python
# Das funktioniert nicht, weil get_burgers definiert wurde mit: async def
burgers = get_burgers(2)
```

---

Wenn Sie also eine Bibliothek verwenden, die Ihnen sagt, dass Sie sie mit `await` aufrufen können, müssen Sie die *Pfadoperation-Funktionen*, die diese Bibliothek verwenden, mittels `async def` erstellen, wie in:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Weitere technische Details { #more-technical-details }

Ihnen ist wahrscheinlich aufgefallen, dass `await` nur innerhalb von Funktionen verwendet werden kann, die mit `async def` definiert sind.

Gleichzeitig müssen aber mit `async def` definierte Funktionen „erwartet“ („awaited“) werden. Daher können Funktionen mit `async def` nur innerhalb von Funktionen aufgerufen werden, die auch mit `async def` definiert sind.

Daraus resultiert das Ei-und-Huhn-Problem: Wie ruft man die erste `async` Funktion auf?

Wenn Sie mit **FastAPI** arbeiten, müssen Sie sich darüber keine Sorgen machen, da diese „erste“ Funktion Ihre *Pfadoperation-Funktion* sein wird und FastAPI weiß, was zu tun ist.

Wenn Sie jedoch `async` / `await` ohne FastAPI verwenden möchten, können Sie dies auch tun.

### Schreiben Sie Ihren eigenen asynchronen Code { #write-your-own-async-code }

Starlette (und **FastAPI**) basieren auf [AnyIO](https://anyio.readthedocs.io/en/stable/), was bedeutet, dass es sowohl kompatibel mit der Python-Standardbibliothek [asyncio](https://docs.python.org/3/library/asyncio-task.html) als auch mit [Trio](https://trio.readthedocs.io/en/stable/) ist.

Insbesondere können Sie [AnyIO](https://anyio.readthedocs.io/en/stable/) direkt verwenden für Ihre fortgeschrittenen nebenläufigen Anwendungsfälle, die fortgeschrittenere Muster in Ihrem eigenen Code erfordern.

Und auch wenn Sie FastAPI nicht verwenden würden, könnten Sie Ihre eigenen asynchronen Anwendungen mit [AnyIO](https://anyio.readthedocs.io/en/stable/) schreiben, um hochkompatibel zu sein und dessen Vorteile zu nutzen (z. B. *strukturierte Nebenläufigkeit*).

Ich habe eine weitere Bibliothek auf Basis von AnyIO erstellt, als dünne Schicht obendrauf, um die Typannotationen etwas zu verbessern und bessere **Autovervollständigung**, **Inline-Fehler** usw. zu erhalten. Sie hat auch eine freundliche Einführung und ein Tutorial, um Ihnen zu helfen, **Ihren eigenen asynchronen Code zu verstehen** und zu schreiben: [Asyncer](https://asyncer.tiangolo.com/). Sie ist insbesondere nützlich, wenn Sie **asynchronen Code mit regulärem** (blockierendem/synchronem) Code kombinieren müssen.

### Andere Formen von asynchronem Code { #other-forms-of-asynchronous-code }

Diese Art der Verwendung von `async` und `await` ist in der Sprache relativ neu.

Aber sie erleichtert die Arbeit mit asynchronem Code erheblich.

Die gleiche Syntax (oder fast identisch) wurde kürzlich auch in moderne Versionen von JavaScript (im Browser und in NodeJS) aufgenommen.

Davor war der Umgang mit asynchronem Code jedoch deutlich komplexer und schwieriger.

In früheren Versionen von Python hätten Sie Threads oder [Gevent](https://www.gevent.org/) verwenden können. Der Code ist jedoch viel komplexer zu verstehen, zu debuggen und nachzuvollziehen.

In früheren Versionen von NodeJS / Browser JavaScript hätten Sie „Callbacks“ verwendet. Was zur „Callback-Hölle“ führt.

## Coroutinen { #coroutines }

**Coroutine** ist nur ein schicker Begriff für dasjenige, was von einer `async def`-Funktion zurückgegeben wird. Python weiß, dass es so etwas wie eine Funktion ist, die es starten kann und die irgendwann endet, aber auch dass sie pausiert ⏸ werden kann, wann immer darin ein `await` steht.

Aber all diese Funktionalität der Verwendung von asynchronem Code mit `async` und `await` wird oft als Verwendung von „Coroutinen“ zusammengefasst. Es ist vergleichbar mit dem Hauptmerkmal von Go, den „Goroutinen“.

## Fazit { #conclusion }

Sehen wir uns den gleichen Satz von oben noch mal an:

> Moderne Versionen von Python unterstützen **„asynchronen Code“** unter Verwendung sogenannter **„Coroutinen“** mithilfe der Syntax **`async` und `await`**.

Das sollte jetzt mehr Sinn ergeben. ✨

All das ist es, was FastAPI (via Starlette) befeuert und es eine so beeindruckende Performanz haben lässt.

## Sehr technische Details { #very-technical-details }

/// warning | Achtung

Das folgende können Sie wahrscheinlich überspringen.

Dies sind sehr technische Details darüber, wie **FastAPI** unter der Haube funktioniert.

Wenn Sie über gute technische Kenntnisse verfügen (Coroutinen, Threads, Blocking, usw.) und neugierig sind, wie FastAPI mit `async def`s im Vergleich zu normalen `def`s umgeht, fahren Sie fort.

///

### Pfadoperation-Funktionen { #path-operation-functions }

Wenn Sie eine *Pfadoperation-Funktion* mit normalem `def` anstelle von `async def` deklarieren, wird sie in einem externen Threadpool ausgeführt, der dann `await`et wird, anstatt direkt aufgerufen zu werden (da dies den Server blockieren würde).

Wenn Sie von einem anderen asynchronen Framework kommen, das nicht auf die oben beschriebene Weise funktioniert, und Sie es gewohnt sind, triviale, nur-berechnende *Pfadoperation-Funktionen* mit einfachem `def` zu definieren, um einen geringfügigen Geschwindigkeitsgewinn (etwa 100 Nanosekunden) zu erzielen, beachten Sie bitte, dass der Effekt in **FastAPI** genau gegenteilig wäre. In solchen Fällen ist es besser, `async def` zu verwenden, es sei denn, Ihre *Pfadoperation-Funktionen* verwenden Code, der blockierende <abbr title="Input/Output - Eingabe/Ausgabe: Lesen oder Schreiben von/auf Festplatte, Netzwerkkommunikation.">I/O</abbr>-Operationen durchführt.

Dennoch besteht in beiden Fällen eine gute Chance, dass **FastAPI** [immer noch schneller](index.md#performance) als Ihr bisheriges Framework (oder zumindest damit vergleichbar) ist.

### Abhängigkeiten { #dependencies }

Das Gleiche gilt für [Abhängigkeiten](tutorial/dependencies/index.md). Wenn eine Abhängigkeit eine normale `def`-Funktion anstelle einer `async def` ist, wird sie im externen Threadpool ausgeführt.

### Unterabhängigkeiten { #sub-dependencies }

Sie können mehrere Abhängigkeiten und [Unterabhängigkeiten](tutorial/dependencies/sub-dependencies.md) haben, die einander bedingen (als Parameter der Funktionsdefinitionen), einige davon könnten erstellt werden mit `async def` und einige mit normalem `def`. Es würde immer noch funktionieren, und diejenigen, die mit normalem `def` erstellt wurden, würden in einem externen Thread (vom Threadpool stammend) aufgerufen werden, anstatt `await`et zu werden.

### Andere Hilfsfunktionen { #other-utility-functions }

Jede andere Hilfsfunktion, die Sie direkt aufrufen, kann mit normalem `def` oder `async def` erstellt werden, und FastAPI beeinflusst nicht die Art und Weise, wie Sie sie aufrufen.

Dies steht im Gegensatz zu den Funktionen, die FastAPI für Sie aufruft: *Pfadoperation-Funktionen* und Abhängigkeiten.

Wenn Ihre Hilfsfunktion eine normale Funktion mit `def` ist, wird sie direkt aufgerufen (so wie Sie es in Ihrem Code schreiben), nicht in einem Threadpool. Wenn die Funktion mit `async def` erstellt wurde, sollten Sie sie `await`en, wenn Sie sie in Ihrem Code aufrufen.

---

Nochmal, es handelt sich hier um sehr technische Details, die Ihnen helfen, falls Sie danach gesucht haben.

Andernfalls liegen Sie richtig, wenn Sie sich an die Richtlinien aus dem obigen Abschnitt halten: <a href="#in-a-hurry">In Eile?</a>.
