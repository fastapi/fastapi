# Benchmarks { #benchmarks }

Unabhängige TechEmpower-Benchmarks zeigen **FastAPI**-Anwendungen, die unter Uvicorn ausgeführt werden, als <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">eines der schnellsten verfügbaren Python-Frameworks</a>, nur unterhalb von Starlette und Uvicorn selbst (die intern von FastAPI verwendet werden).

Aber bei der Betrachtung von Benchmarks und Vergleichen sollten Sie Folgendes beachten.

## Benchmarks und Geschwindigkeit { #benchmarks-and-speed }

Wenn Sie die Benchmarks ansehen, ist es üblich, dass mehrere Tools unterschiedlichen Typs als gleichwertig verglichen werden.

Insbesondere dass Uvicorn, Starlette und FastAPI zusammen verglichen werden (neben vielen anderen Tools).

Je einfacher das Problem, das durch das Tool gelöst wird, desto besser wird die Performanz sein. Und die meisten Benchmarks testen nicht die zusätzlichen Funktionen, die das Tool bietet.

Die Hierarchie ist wie folgt:

* **Uvicorn**: ein ASGI-Server
    * **Starlette**: (verwendet Uvicorn) ein Web-Mikroframework
        * **FastAPI**: (verwendet Starlette) ein API-Mikroframework mit mehreren zusätzlichen Funktionen zum Erstellen von APIs, mit Datenvalidierung, usw.

* **Uvicorn**:
    * Wird die beste Performanz haben, da außer dem Server selbst nicht viel zusätzlicher Code vorhanden ist.
    * Sie würden eine Anwendung nicht direkt in Uvicorn schreiben. Das würde bedeuten, dass Ihr Code zumindest mehr oder weniger den gesamten von Starlette (oder **FastAPI**) bereitgestellten Code enthalten müsste. Und wenn Sie das täten, hätte Ihre endgültige Anwendung den gleichen Overhead wie bei der Verwendung eines Frameworks und der Minimierung Ihres Anwendungscodes und der Fehler.
    * Wenn Sie Uvicorn vergleichen, vergleichen Sie es mit Anwendungsservern wie Daphne, Hypercorn, uWSGI, usw.
* **Starlette**:
    * Wird nach Uvicorn die nächstbeste Performanz erbringen. Tatsächlich verwendet Starlette intern Uvicorn, um zu laufen. Daher kann es wahrscheinlich nur „langsamer“ als Uvicorn werden, weil mehr Code ausgeführt werden muss.
    * Aber es bietet Ihnen die Werkzeuge, um einfache Webanwendungen zu erstellen, mit Routing basierend auf Pfaden, usw.
    * Wenn Sie Starlette vergleichen, vergleichen Sie es mit Webframeworks (oder Mikroframeworks) wie Sanic, Flask, Django, usw.
* **FastAPI**:
    * So wie Starlette Uvicorn verwendet und nicht schneller als dieses sein kann, verwendet **FastAPI** Starlette, sodass es nicht schneller als dieses sein kann.
    * FastAPI bietet zusätzliche Funktionen auf Basis von Starlette. Funktionen, die Sie beim Erstellen von APIs fast immer benötigen, wie Datenvalidierung und Serialisierung. Und wenn Sie es verwenden, erhalten Sie kostenlose automatische Dokumentation (die automatische Dokumentation verursacht nicht einmal zusätzlichen Overhead für laufende Anwendungen, sie wird beim Starten generiert).
    * Wenn Sie FastAPI nicht verwenden und stattdessen Starlette direkt (oder ein anderes Tool wie Sanic, Flask, Responder, usw.) verwenden würden, müssten Sie die gesamte Datenvalidierung und Serialisierung selbst implementieren. Ihre finale Anwendung hätte also immer noch den gleichen Overhead, als ob sie mit FastAPI erstellt worden wäre. Und in vielen Fällen ist diese Datenvalidierung und Serialisierung der größte Teil des in Anwendungen geschriebenen Codes.
    * Durch die Verwendung von FastAPI sparen Sie also Entwicklungszeit, Fehler und Codezeilen und würden wahrscheinlich die gleiche Performanz (oder eine bessere) erzielen, die Sie hätten, wenn Sie es nicht verwenden würden (da Sie alles in Ihrem Code implementieren müssten).
    * Wenn Sie FastAPI vergleichen, vergleichen Sie es mit einem Webanwendungs-Framework (oder einer Reihe von Tools), das Datenvalidierung, Serialisierung und Dokumentation bereitstellt, wie Flask-apispec, NestJS, Molten, usw. – Frameworks mit integrierter automatischer Datenvalidierung, Serialisierung und Dokumentation.
