# Benchmarks

Unabhängige TechEmpower-Benchmarks zeigen, **FastAPI**-Anwendungen, die unter Uvicorn ausgeführt werden, gehören zu <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">den schnellsten existierenden Python-Frameworks</a>, nur Starlette und Uvicorn selbst (intern von FastAPI verwendet) sind schneller.

Beim Ansehen von Benchmarks und Vergleichen sollten Sie jedoch Folgende Punkte beachten.

## Benchmarks und Geschwindigkeit

Wenn Sie sich die Benchmarks ansehen, werden häufig mehrere Tools mit unterschiedlichen Eigenschaften als gleichwertig verglichen.

Konkret geht es darum, Uvicorn, Starlette und FastAPI miteinander zu vergleichen (neben vielen anderen Tools).

Je einfacher das Problem, welches durch das Tool gelöst wird, desto besser ist die Performanz. Und die meisten Benchmarks testen nicht die zusätzlichen Funktionen, welche das Tool bietet.

Die Hierarchie ist wie folgt:

* **Uvicorn**: ein ASGI-Server
    * **Starlette**: (verwendet Uvicorn) ein Web-Mikroframework
        * **FastAPI**: (verwendet Starlette) ein API-Mikroframework mit mehreren zusätzlichen Funktionen zum Erstellen von APIs, mit Datenvalidierung, usw.

* **Uvicorn**:
    * Bietet die beste Leistung, da außer dem Server selbst nicht viel zusätzlicher Code vorhanden ist.
    * Sie würden eine Anwendung nicht direkt in Uvicorn schreiben. Das würde bedeuten, dass Ihr Code zumindest mehr oder weniger den gesamten von Starlette (oder **FastAPI**) bereitgestellten Code enthalten müsste. Und wenn Sie das täten, hätte Ihre endgültige Anwendung den gleichen Overhead wie die Verwendung eines Frameworks nebst Minimierung Ihres Anwendungscodes und der Fehler.
    * Wenn Sie Uvicorn vergleichen, vergleichen Sie es mit Anwendungsservern wie Daphne, Hypercorn, uWSGI, usw.
* **Starlette**:
    * Wird nach Uvicorn die nächstbeste Performanz erbringen. Tatsächlich nutzt Starlette intern Uvicorn. Daher kann es wahrscheinlich nur „langsamer“ als Uvicorn sein, weil mehr Code ausgeführt wird.
    * Aber es bietet Ihnen die Tools zum Erstellen einfacher Webanwendungen, mit Routing basierend auf Pfaden, usw.
    * Wenn Sie Starlette vergleichen, vergleichen Sie es mit Webframeworks (oder Mikroframeworks) wie Sanic, Flask, Django, usw.
* **FastAPI**:
    * So wie Starlette Uvicorn verwendet und nicht schneller als dieses sein kann, verwendet **FastAPI** Starlette, sodass es nicht schneller als dieses sein kann.
    * FastAPI bietet zusätzlich zu Starlette weitere Funktionen. Funktionen, die Sie beim Erstellen von APIs fast immer benötigen, wie Datenvalidierung und Serialisierung. Und wenn Sie es verwenden, erhalten Sie kostenlos automatische Dokumentation (die automatische Dokumentation verursacht nicht einmal zusätzlichen Aufwand für laufende Anwendungen, sie wird beim Start generiert).
    * Wenn Sie FastAPI nicht, und direkt Starlette (oder ein anderes Tool wie Sanic, Flask, Responder, usw.) verwenden würden, müssten Sie die gesamte Datenvalidierung und Serialisierung selbst implementieren. Ihre finale Anwendung hätte also immer noch den gleichen Overhead, als ob sie mit FastAPI erstellt worden wäre. Und in vielen Fällen ist diese Datenvalidierung und Serialisierung der größte Teil des in Anwendungen geschriebenen Codes.
    * Durch die Verwendung von FastAPI sparen Sie also Entwicklungszeit, Fehler und Codezeilen und würden wahrscheinlich die gleiche Leistung (oder eine bessere) erzielen, die Sie hätten, wenn Sie es nicht verwenden würden (da Sie alles in Ihrem Code implementieren müssten).
    * Wenn Sie FastAPI vergleichen, vergleichen Sie es mit einem Webanwendung-Framework (oder einer Reihe von Tools), welche Datenvalidierung, Serialisierung und Dokumentation bereitstellen, wie Flask-apispec, NestJS, Molten, usw. – Frameworks mit integrierter automatischer Datenvalidierung, Serialisierung und Dokumentation.
