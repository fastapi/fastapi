# Alternativen, Inspiration und Vergleiche { #alternatives-inspiration-and-comparisons }

Was hat **FastAPI** inspiriert, wie es sich im Vergleich zu Alternativen verhält und was es von ihnen gelernt hat.

## Einführung { #intro }

**FastAPI** würde ohne die frühere Arbeit anderer nicht existieren.

Es wurden zuvor viele Tools entwickelt, die als Inspiration für seine Entwicklung dienten.

Ich habe die Schaffung eines neuen Frameworks viele Jahre lang vermieden. Zuerst habe ich versucht, alle von **FastAPI** abgedeckten Funktionen mithilfe vieler verschiedener Frameworks, Plugins und Tools zu lösen.

Aber irgendwann gab es keine andere Möglichkeit, als etwas zu schaffen, das all diese Funktionen bereitstellte, die besten Ideen früherer Tools aufnahm und diese auf die bestmögliche Weise kombinierte, wobei Sprachfunktionen verwendet wurden, die vorher noch nicht einmal verfügbar waren (Python 3.6+ Typhinweise).

## Vorherige Tools { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

Es ist das beliebteste Python-Framework und genießt großes Vertrauen. Es wird zum Aufbau von Systemen wie Instagram verwendet.

Es ist relativ eng mit relationalen Datenbanken (wie MySQL oder PostgreSQL) gekoppelt, daher ist es nicht sehr einfach, eine NoSQL-Datenbank (wie Couchbase, MongoDB, Cassandra, usw.) als Hauptspeicherengine zu verwenden.

Es wurde erstellt, um den HTML-Code im Backend zu generieren, nicht um APIs zu erstellen, die von einem modernen Frontend (wie React, Vue.js und Angular) oder von anderen Systemen (wie <abbr title="Internet of Things – Internet der Dinge">IoT</abbr>-Geräten) verwendet werden, um mit ihm zu kommunizieren.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Das Django REST Framework wurde als flexibles Toolkit zum Erstellen von Web-APIs unter Verwendung von Django entwickelt, um dessen API-Möglichkeiten zu verbessern.

Es wird von vielen Unternehmen verwendet, darunter Mozilla, Red Hat und Eventbrite.

Es war eines der ersten Beispiele für **automatische API-Dokumentation**, und dies war insbesondere eine der ersten Ideen, welche „die Suche nach“ **FastAPI** inspirierten.

/// note | Hinweis

Das Django REST Framework wurde von Tom Christie erstellt. Derselbe Schöpfer von Starlette und Uvicorn, auf denen **FastAPI** basiert.

///

/// check | Inspirierte **FastAPI**

Eine automatische API-Dokumentationsoberfläche zu haben.

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask ist ein „Mikroframework“, es enthält weder Datenbankintegration noch viele der Dinge, die standardmäßig in Django enthalten sind.

Diese Einfachheit und Flexibilität ermöglichen beispielsweise die Verwendung von NoSQL-Datenbanken als Hauptdatenspeichersystem.

Da es sehr einfach ist, ist es relativ intuitiv zu erlernen, obwohl die Dokumentation an einigen Stellen etwas technisch wird.

Es wird auch häufig für andere Anwendungen verwendet, die nicht unbedingt eine Datenbank, Benutzerverwaltung oder eine der vielen in Django enthaltenen Funktionen benötigen. Obwohl viele dieser Funktionen mit Plugins hinzugefügt werden können.

Diese Entkopplung der Teile und die Tatsache, dass es sich um ein „Mikroframework“ handelt, welches so erweitert werden kann, dass es genau das abdeckt, was benötigt wird, war ein Schlüsselmerkmal, das ich beibehalten wollte.

Angesichts der Einfachheit von Flask schien es eine gute Ergänzung zum Erstellen von APIs zu sein. Als Nächstes musste ein „Django REST Framework“ für Flask gefunden werden.

/// check | Inspirierte **FastAPI**

Ein Mikroframework zu sein. Es einfach zu machen, die benötigten Tools und Teile zu kombinieren.

Über ein einfaches und benutzerfreundliches Routingsystem zu verfügen.

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI** ist eigentlich keine Alternative zu **Requests**. Der Umfang der beiden ist sehr unterschiedlich.

Es wäre tatsächlich üblich, Requests *innerhalb* einer FastAPI-Anwendung zu verwenden.

Dennoch erhielt FastAPI von Requests einiges an Inspiration.

**Requests** ist eine Bibliothek zur *Interaktion* mit APIs (als Client), während **FastAPI** eine Bibliothek zum *Erstellen* von APIs (als Server) ist.

Die beiden stehen mehr oder weniger an entgegengesetzten Enden und ergänzen sich.

Requests hat ein sehr einfaches und intuitives Design, ist sehr einfach zu bedienen und verfügt über sinnvolle Standardeinstellungen. Aber gleichzeitig ist es sehr leistungsstark und anpassbar.

Aus diesem Grund heißt es auf der offiziellen Website:

> Requests ist eines der am häufigsten heruntergeladenen Python-Packages aller Zeiten

Die Art und Weise, wie Sie es verwenden, ist sehr einfach. Um beispielsweise einen `GET`-<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> zu machen, würden Sie schreiben:

```Python
response = requests.get("http://example.com/some/url")
```

Die entsprechende *Pfadoperation* der FastAPI-API könnte wie folgt aussehen:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

Sehen Sie sich die Ähnlichkeiten in `requests.get(...)` und `@app.get(...)` an.

/// check | Inspirierte **FastAPI**

* Über eine einfache und intuitive API zu verfügen.
* HTTP-Methodennamen (Operationen) direkt, auf einfache und intuitive Weise zu verwenden.
* Vernünftige Standardeinstellungen zu haben, aber auch mächtige Einstellungsmöglichkeiten.

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

Die Hauptfunktion, die ich vom Django REST Framework haben wollte, war die automatische API-Dokumentation.

Dann fand ich heraus, dass es einen Standard namens Swagger gab, zur Dokumentation von APIs unter Verwendung von JSON (oder YAML, einer Erweiterung von JSON).

Und es gab bereits eine Web-Oberfläche für Swagger-APIs. Die Möglichkeit, Swagger-Dokumentation für eine API zu generieren, würde die automatische Nutzung dieser Web-Oberfläche ermöglichen.

Irgendwann wurde Swagger an die Linux Foundation übergeben und in OpenAPI umbenannt.

Aus diesem Grund spricht man bei Version 2.0 häufig von „Swagger“ und ab Version 3 von „OpenAPI“.

/// check | Inspirierte **FastAPI**

Einen offenen Standard für API-Spezifikationen zu übernehmen und zu verwenden, anstelle eines benutzerdefinierten Schemas.

Und Standard-basierte Tools für die Oberfläche zu integrieren:

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

Diese beiden wurden ausgewählt, weil sie ziemlich beliebt und stabil sind, aber bei einer schnellen Suche könnten Sie Dutzende alternativer Benutzeroberflächen für OpenAPI finden (welche Sie mit **FastAPI** verwenden können).

///

### Flask REST Frameworks { #flask-rest-frameworks }

Es gibt mehrere Flask REST Frameworks, aber nachdem ich die Zeit und Arbeit investiert habe, sie zu untersuchen, habe ich festgestellt, dass viele nicht mehr unterstützt werden oder abgebrochen wurden und dass mehrere fortbestehende Probleme sie unpassend machten.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

Eine der von API-Systemen benötigten Hauptfunktionen ist die Daten-<abbr title="Auch „Marshalling“, „Konvertierung“ genannt">„Serialisierung“</abbr>, welche Daten aus dem Code (Python) entnimmt und in etwas umwandelt, was durch das Netzwerk gesendet werden kann. Beispielsweise das Konvertieren eines Objekts, welches Daten aus einer Datenbank enthält, in ein JSON-Objekt. Konvertieren von `datetime`-Objekten in Strings, usw.

Eine weitere wichtige Funktion, benötigt von APIs, ist die Datenvalidierung, welche sicherstellt, dass die Daten unter gegebenen Umständen gültig sind. Zum Beispiel, dass ein Feld ein `int` ist und kein zufälliger String. Das ist besonders nützlich für hereinkommende Daten.

Ohne ein Datenvalidierungssystem müssten Sie alle Prüfungen manuell im Code durchführen.

Für diese Funktionen wurde Marshmallow entwickelt. Es ist eine großartige Bibliothek und ich habe sie schon oft genutzt.

Aber sie wurde erstellt, bevor Typhinweise in Python existierten. Um also ein <abbr title="die Definition, wie Daten geformt sein sollen">Schema</abbr> zu definieren, müssen Sie bestimmte Werkzeuge und Klassen verwenden, die von Marshmallow bereitgestellt werden.

/// check | Inspirierte **FastAPI**

Code zu verwenden, um „Schemas“ zu definieren, welche Datentypen und Validierung automatisch bereitstellen.

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

Eine weitere wichtige Funktion, die von APIs benötigt wird, ist das <abbr title="Lesen und Konvertieren nach Python-Daten">Parsen</abbr> von Daten aus eingehenden Requests.

Webargs wurde entwickelt, um dieses für mehrere Frameworks, einschließlich Flask, bereitzustellen.

Es verwendet unter der Haube Marshmallow, um die Datenvalidierung durchzuführen. Und es wurde von denselben Entwicklern erstellt.

Es ist ein großartiges Tool und ich habe es auch oft verwendet, bevor ich **FastAPI** hatte.

/// info | Info

Webargs wurde von denselben Marshmallow-Entwicklern erstellt.

///

/// check | Inspirierte **FastAPI**

Eingehende Requestdaten automatisch zu validieren.

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow und Webargs bieten Validierung, Parsen und Serialisierung als Plugins.

Es fehlt jedoch noch die Dokumentation. Dann wurde APISpec erstellt.

Es ist ein Plugin für viele Frameworks (und es gibt auch ein Plugin für Starlette).

Die Funktionsweise besteht darin, dass Sie die Definition des Schemas im YAML-Format im Docstring jeder Funktion schreiben, die eine Route verarbeitet.

Und es generiert OpenAPI-Schemas.

So funktioniert es in Flask, Starlette, Responder, usw.

Aber dann haben wir wieder das Problem einer Mikrosyntax innerhalb eines Python-Strings (eines großen YAML).

Der Texteditor kann dabei nicht viel helfen. Und wenn wir Parameter oder Marshmallow-Schemas ändern und vergessen, auch den YAML-Docstring zu ändern, wäre das generierte Schema veraltet.

/// info | Info

APISpec wurde von denselben Marshmallow-Entwicklern erstellt.

///

/// check | Inspirierte **FastAPI**

Den offenen Standard für APIs, OpenAPI, zu unterstützen.

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

Hierbei handelt es sich um ein Flask-Plugin, welches Webargs, Marshmallow und APISpec miteinander verbindet.

Es nutzt die Informationen von Webargs und Marshmallow, um mithilfe von APISpec automatisch OpenAPI-Schemas zu generieren.

Ein großartiges Tool, sehr unterbewertet. Es sollte weitaus populärer als viele andere Flask-Plugins sein. Möglicherweise liegt es daran, dass die Dokumentation zu kompakt und abstrakt ist.

Das löste das Problem, YAML (eine andere Syntax) in Python-Docstrings schreiben zu müssen.

Diese Kombination aus Flask, Flask-apispec mit Marshmallow und Webargs war bis zur Entwicklung von **FastAPI** mein Lieblings-Backend-Stack.

Die Verwendung führte zur Entwicklung mehrerer Flask-Full-Stack-Generatoren. Dies sind die Hauptstacks, die ich (und mehrere externe Teams) bisher verwendet haben:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

Und dieselben Full-Stack-Generatoren bildeten die Basis der [**FastAPI**-Projektgeneratoren](project-generation.md){.internal-link target=_blank}.

/// info | Info

Flask-apispec wurde von denselben Marshmallow-Entwicklern erstellt.

///

/// check | Inspirierte **FastAPI**

Das OpenAPI-Schema automatisch zu generieren, aus demselben Code, welcher die Serialisierung und Validierung definiert.

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (und <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>) { #nestjs-and-angular }

Dies ist nicht einmal Python, NestJS ist ein von Angular inspiriertes JavaScript (TypeScript) NodeJS Framework.

Es erreicht etwas Ähnliches wie Flask-apispec.

Es verfügt über ein integriertes Dependency Injection System, welches von Angular 2 inspiriert ist. Erfordert ein Vorab-Registrieren der „Injectables“ (wie alle anderen Dependency Injection Systeme, welche ich kenne), sodass der Code ausschweifender wird und es mehr Codeverdoppelung gibt.

Da die Parameter mit TypeScript-Typen beschrieben werden (ähnlich den Python-Typhinweisen), ist die Editorunterstützung ziemlich gut.

Da TypeScript-Daten jedoch nach der Kompilierung nach JavaScript nicht erhalten bleiben, können die Typen nicht gleichzeitig die Validierung, Serialisierung und Dokumentation definieren. Aus diesem Grund und aufgrund einiger Designentscheidungen ist es für die Validierung, Serialisierung und automatische Schemagenerierung erforderlich, an vielen Stellen Dekoratoren hinzuzufügen. Es wird also ziemlich ausführlich.

Es kann nicht sehr gut mit verschachtelten Modellen umgehen. Wenn es sich beim JSON-Body im Request also um ein JSON-Objekt mit inneren Feldern handelt, die wiederum verschachtelte JSON-Objekte sind, kann er nicht richtig dokumentiert und validiert werden.

/// check | Inspirierte **FastAPI**

Python-Typen zu verwenden, um eine hervorragende Editorunterstützung zu erhalten.

Über ein leistungsstarkes Dependency Injection System zu verfügen. Eine Möglichkeit zu finden, Codeverdoppelung zu minimieren.

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

Es war eines der ersten extrem schnellen Python-Frameworks, welches auf `asyncio` basierte. Es wurde so gestaltet, dass es Flask sehr ähnlich ist.

/// note | Technische Details

Es verwendete <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> anstelle der standardmäßigen Python-`asyncio`-Schleife. Das hat es so schnell gemacht.

Hat eindeutig Uvicorn und Starlette inspiriert, welche derzeit in offenen Benchmarks schneller als Sanic sind.

///

/// check | Inspirierte **FastAPI**

Einen Weg zu finden, eine hervorragende Performanz zu haben.

Aus diesem Grund basiert **FastAPI** auf Starlette, da dieses das schnellste verfügbare Framework ist (getestet in Benchmarks von Dritten).

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon ist ein weiteres leistungsstarkes Python-Framework. Es ist minimalistisch konzipiert und dient als Grundlage für andere Frameworks wie Hug.

Es ist so konzipiert, dass es über Funktionen verfügt, welche zwei Parameter empfangen, einen <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">„Request“</abbr> und eine <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">„Response“</abbr>. Dann „lesen“ Sie Teile des Requests und „schreiben“ Teile der Response. Aufgrund dieses Designs ist es nicht möglich, Request-Parameter und -Bodys mit Standard-Python-Typhinweisen als Funktionsparameter zu deklarieren.

Daher müssen Datenvalidierung, Serialisierung und Dokumentation im Code und nicht automatisch erfolgen. Oder sie müssen als Framework oberhalb von Falcon implementiert werden, so wie Hug. Dieselbe Unterscheidung findet auch in anderen Frameworks statt, die vom Design von Falcon inspiriert sind und ein Requestobjekt und ein Responseobjekt als Parameter haben.

/// check | Inspirierte **FastAPI**

Wege zu finden, eine großartige Performanz zu erzielen.

Zusammen mit Hug (da Hug auf Falcon basiert), einen `response`-Parameter in Funktionen zu deklarieren.

Obwohl er in FastAPI optional ist und hauptsächlich zum Festlegen von Headern, Cookies und alternativen Statuscodes verwendet wird.

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

Ich habe Molten in den ersten Phasen der Entwicklung von **FastAPI** entdeckt. Und es hat ganz ähnliche Ideen:

* Basierend auf Python-Typhinweisen.
* Validierung und Dokumentation aus diesen Typen.
* Dependency Injection System.

Es verwendet keine Datenvalidierungs-, Serialisierungs- und Dokumentationsbibliothek eines Dritten wie Pydantic, sondern verfügt über eine eigene. Daher wären diese Datentyp-Definitionen nicht so einfach wiederverwendbar.

Es erfordert eine etwas ausführlichere Konfiguration. Und da es auf WSGI (anstelle von ASGI) basiert, ist es nicht darauf ausgelegt, die hohe Leistung von Tools wie Uvicorn, Starlette und Sanic zu nutzen.

Das Dependency Injection System erfordert eine Vorab-Registrierung der Abhängigkeiten und die Abhängigkeiten werden basierend auf den deklarierten Typen aufgelöst. Daher ist es nicht möglich, mehr als eine „Komponente“ zu deklarieren, welche einen bestimmten Typ bereitstellt.

Routen werden an einer einzigen Stelle deklariert, indem Funktionen verwendet werden, die an anderen Stellen deklariert wurden (anstatt Dekoratoren zu verwenden, welche direkt über der Funktion platziert werden können, welche den Endpunkt verarbeitet). Dies ähnelt eher der Vorgehensweise von Django als der Vorgehensweise von Flask (und Starlette). Es trennt im Code Dinge, die relativ eng miteinander gekoppelt sind.

/// check | Inspirierte **FastAPI**

Zusätzliche Validierungen für Datentypen zu definieren, mithilfe des „Default“-Werts von Modellattributen. Dies verbessert die Editorunterstützung und war zuvor in Pydantic nicht verfügbar.

Das hat tatsächlich dazu geführt, dass Teile von Pydantic aktualisiert wurden, um denselben Validierungsdeklarationsstil zu unterstützen (diese gesamte Funktionalität ist jetzt bereits in Pydantic verfügbar).

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug war eines der ersten Frameworks, welches die Deklaration von API-Parametertypen mithilfe von Python-Typhinweisen implementierte. Das war eine großartige Idee, die andere Tools dazu inspirierte, dasselbe zu tun.

Es verwendete benutzerdefinierte Typen in seinen Deklarationen anstelle von Standard-Python-Typen, es war aber dennoch ein großer Fortschritt.

Außerdem war es eines der ersten Frameworks, welches ein benutzerdefiniertes Schema generierte, welches die gesamte API in JSON deklarierte.

Es basierte nicht auf einem Standard wie OpenAPI und JSON Schema. Daher wäre es nicht einfach, es in andere Tools wie Swagger UI zu integrieren. Aber, nochmal, es war eine sehr innovative Idee.

Es verfügt über eine interessante, ungewöhnliche Funktion: Mit demselben Framework ist es möglich, APIs und auch CLIs zu erstellen.

Da es auf dem bisherigen Standard für synchrone Python-Webframeworks (WSGI) basiert, kann es nicht mit Websockets und anderen Dingen umgehen, verfügt aber dennoch über eine hohe Performanz.

/// info | Info

Hug wurde von Timothy Crosley erstellt, demselben Schöpfer von <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>, einem großartigen Tool zum automatischen Sortieren von Importen in Python-Dateien.

///

/// check | Ideen, die **FastAPI** inspiriert haben

Hug inspirierte Teile von APIStar und war eines der Tools, die ich am vielversprechendsten fand, neben APIStar.

Hug hat dazu beigetragen, **FastAPI** dazu zu inspirieren, Python-Typhinweise zum Deklarieren von Parametern zu verwenden und ein Schema zu generieren, das die API automatisch definiert.

Hug inspirierte **FastAPI** dazu, einen `response`-Parameter in Funktionen zu deklarieren, um Header und Cookies zu setzen.

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (≦ 0.5) { #apistar-0-5 }

Kurz bevor ich mich entschied, **FastAPI** zu erstellen, fand ich den **APIStar**-Server. Er hatte fast alles, was ich suchte, und ein tolles Design.

Er war eine der ersten Implementierungen eines Frameworks, die ich je gesehen hatte (vor NestJS und Molten), welches Python-Typhinweise zur Deklaration von Parametern und Requests verwendeten. Ich habe ihn mehr oder weniger zeitgleich mit Hug gefunden. Aber APIStar nutzte den OpenAPI-Standard.

Er verfügte an mehreren Stellen über automatische Datenvalidierung, Datenserialisierung und OpenAPI-Schemagenerierung, basierend auf denselben Typhinweisen.

Body-Schemadefinitionen verwendeten nicht die gleichen Python-Typhinweise wie Pydantic, er war Marshmallow etwas ähnlicher, sodass die Editorunterstützung nicht so gut war, aber dennoch war APIStar die beste verfügbare Option.

Er hatte zu dieser Zeit die besten Leistungsbenchmarks (nur übertroffen von Starlette).

Anfangs gab es keine Web-Oberfläche für die automatische API-Dokumentation, aber ich wusste, dass ich Swagger UI hinzufügen konnte.

Er verfügte über ein Dependency Injection System. Es erforderte eine Vorab-Registrierung der Komponenten, wie auch bei anderen oben besprochenen Tools. Aber dennoch, es war ein tolles Feature.

Ich konnte ihn nie in einem vollständigen Projekt verwenden, da er keine Sicherheitsintegration hatte, sodass ich nicht alle Funktionen, die ich hatte, durch die auf Flask-apispec basierenden Full-Stack-Generatoren ersetzen konnte. Ich hatte in meinem Projekte-Backlog den Eintrag, einen Pull Request zu erstellen, welcher diese Funktionalität hinzufügte.

Doch dann verlagerte sich der Schwerpunkt des Projekts.

Es handelte sich nicht länger um ein API-Webframework, da sich der Entwickler auf Starlette konzentrieren musste.

Jetzt handelt es sich bei APIStar um eine Reihe von Tools zur Validierung von OpenAPI-Spezifikationen, nicht um ein Webframework.

/// info | Info

APIStar wurde von Tom Christie erstellt. Derselbe, welcher Folgendes erstellt hat:

* Django REST Framework
* Starlette (auf welchem **FastAPI** basiert)
* Uvicorn (verwendet von Starlette und **FastAPI**)

///

/// check | Inspirierte **FastAPI**

Zu existieren.

Die Idee, mehrere Dinge (Datenvalidierung, Serialisierung und Dokumentation) mit denselben Python-Typen zu deklarieren, welche gleichzeitig eine hervorragende Editorunterstützung bieten, hielt ich für eine brillante Idee.

Und nach einer langen Suche nach einem ähnlichen Framework und dem Testen vieler verschiedener Alternativen, war APIStar die beste verfügbare Option.

Dann hörte APIStar auf, als Server zu existieren, und Starlette wurde geschaffen, welches eine neue, bessere Grundlage für ein solches System bildete. Das war die finale Inspiration für die Entwicklung von **FastAPI**.

Ich betrachte **FastAPI** als einen „spirituellen Nachfolger“ von APIStar, welcher die Funktionen, das Typsystem und andere Teile verbessert und erweitert, basierend auf den Erkenntnissen aus all diesen früheren Tools.

///

## Verwendet von **FastAPI** { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic ist eine Bibliothek zum Definieren von Datenvalidierung, Serialisierung und Dokumentation (unter Verwendung von JSON Schema) basierend auf Python-Typhinweisen.

Das macht es äußerst intuitiv.

Es ist vergleichbar mit Marshmallow. Obwohl es in Benchmarks schneller als Marshmallow ist. Und da es auf den gleichen Python-Typhinweisen basiert, ist die Editorunterstützung großartig.

/// check | **FastAPI** verwendet es, um

Die gesamte Datenvalidierung, Datenserialisierung und automatische Modelldokumentation (basierend auf JSON Schema) zu erledigen.

**FastAPI** nimmt dann, abgesehen von all den anderen Dingen, die es tut, dieses JSON-Schema und fügt es in OpenAPI ein.

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette ist ein leichtgewichtiges <abbr title="Der neue Standard für die Erstellung asynchroner Python-Webanwendungen">ASGI</abbr>-Framework/Toolkit, welches sich ideal für die Erstellung hochperformanter asynchroner Dienste eignet.

Es ist sehr einfach und intuitiv. Es ist so konzipiert, dass es leicht erweiterbar ist und über modulare Komponenten verfügt.

Es bietet:

* Eine sehr beeindruckende Leistung.
* WebSocket-Unterstützung.
* Hintergrundtasks im selben Prozess.
* Startup- und Shutdown-Events.
* Testclient basierend auf HTTPX.
* CORS, GZip, statische Dateien, Responses streamen.
* Session- und Cookie-Unterstützung.
* 100 % Testabdeckung.
* 100 % Typannotierte Codebasis.
* Wenige starke Abhängigkeiten.

Starlette ist derzeit das schnellste getestete Python-Framework. Nur übertroffen von Uvicorn, welches kein Framework, sondern ein Server ist.

Starlette bietet alle grundlegenden Funktionen eines Web-Microframeworks.

Es bietet jedoch keine automatische Datenvalidierung, Serialisierung oder Dokumentation.

Das ist eines der wichtigsten Dinge, welche **FastAPI** hinzufügt, alles basierend auf Python-Typhinweisen (mit Pydantic). Das, plus, das Dependency Injection System, Sicherheitswerkzeuge, OpenAPI-Schemagenerierung, usw.

/// note | Technische Details

ASGI ist ein neuer „Standard“, welcher von Mitgliedern des Django-Kernteams entwickelt wird. Es handelt sich immer noch nicht um einen „Python-Standard“ (ein PEP), obwohl sie gerade dabei sind, das zu tun.

Dennoch wird es bereits von mehreren Tools als „Standard“ verwendet. Das verbessert die Interoperabilität erheblich, da Sie Uvicorn mit jeden anderen ASGI-Server (wie Daphne oder Hypercorn) tauschen oder ASGI-kompatible Tools wie `python-socketio` hinzufügen können.

///

/// check | **FastAPI** verwendet es, um

Alle Kern-Webaspekte zu handhaben. Und fügt Funktionen obenauf.

Die Klasse `FastAPI` selbst erbt direkt von der Klasse `Starlette`.

Alles, was Sie also mit Starlette machen können, können Sie direkt mit **FastAPI** machen, da es sich im Grunde um Starlette auf Steroiden handelt.

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn ist ein blitzschneller ASGI-Server, der auf uvloop und httptools basiert.

Es handelt sich nicht um ein Webframework, sondern um einen Server. Beispielsweise werden keine Tools für das Routing von Pfaden bereitgestellt. Das ist etwas, was ein Framework wie Starlette (oder **FastAPI**) zusätzlich bieten würde.

Es ist der empfohlene Server für Starlette und **FastAPI**.

/// check | **FastAPI** empfiehlt es als

Hauptwebserver zum Ausführen von **FastAPI**-Anwendungen.

Sie können auch die Kommandozeilenoption `--workers` verwenden, um einen asynchronen Multiprozess-Server zu erhalten.

Weitere Details finden Sie im Abschnitt [Deployment](deployment/index.md){.internal-link target=_blank}.

///

## Benchmarks und Geschwindigkeit { #benchmarks-and-speed }

Um den Unterschied zwischen Uvicorn, Starlette und FastAPI zu verstehen, zu vergleichen und zu sehen, lesen Sie den Abschnitt über [Benchmarks](benchmarks.md){.internal-link target=_blank}.
