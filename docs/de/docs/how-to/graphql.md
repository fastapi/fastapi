# GraphQL { #graphql }

Da **FastAPI** auf dem **ASGI**-Standard basiert, ist es sehr einfach, jede **GraphQL**-Bibliothek zu integrieren, die auch mit ASGI kompatibel ist.

Sie können normale FastAPI-*Pfadoperationen* mit GraphQL in derselben Anwendung kombinieren.

/// tip | Tipp

**GraphQL** löst einige sehr spezifische Anwendungsfälle.

Es hat **Vorteile** und **Nachteile** im Vergleich zu gängigen **Web-APIs**.

Stellen Sie sicher, dass Sie prüfen, ob die **Vorteile** für Ihren Anwendungsfall die **Nachteile** ausgleichen. 🤓

///

## GraphQL-Bibliotheken { #graphql-libraries }

Hier sind einige der **GraphQL**-Bibliotheken, die **ASGI**-Unterstützung haben. Sie könnten sie mit **FastAPI** verwenden:

* [Strawberry](https://strawberry.rocks/) 🍓
    * Mit [Dokumentation für FastAPI](https://strawberry.rocks/docs/integrations/fastapi)
* [Ariadne](https://ariadnegraphql.org/)
    * Mit [Dokumentation für FastAPI](https://ariadnegraphql.org/docs/fastapi-integration)
* [Tartiflette](https://tartiflette.io/)
    * Mit [Tartiflette ASGI](https://tartiflette.github.io/tartiflette-asgi/) für ASGI-Integration
* [Graphene](https://graphene-python.org/)
    * Mit [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3)

## GraphQL mit Strawberry { #graphql-with-strawberry }

Wenn Sie mit **GraphQL** arbeiten möchten oder müssen, ist [**Strawberry**](https://strawberry.rocks/) die **empfohlene** Bibliothek, da deren Design **FastAPIs** Design am nächsten kommt und alles auf **Typannotationen** basiert.

Abhängig von Ihrem Anwendungsfall könnten Sie eine andere Bibliothek vorziehen, aber wenn Sie mich fragen würden, würde ich Ihnen wahrscheinlich empfehlen, **Strawberry** auszuprobieren.

Hier ist eine kleine Vorschau, wie Sie Strawberry mit FastAPI integrieren können:

{* ../../docs_src/graphql_/tutorial001_py310.py hl[3,22,25] *}

Weitere Informationen zu Strawberry finden Sie in der [Strawberry-Dokumentation](https://strawberry.rocks/).

Und auch in der Dokumentation zu [Strawberry mit FastAPI](https://strawberry.rocks/docs/integrations/fastapi).

## Ältere `GraphQLApp` von Starlette { #older-graphqlapp-from-starlette }

Frühere Versionen von Starlette enthielten eine `GraphQLApp`-Klasse zur Integration mit [Graphene](https://graphene-python.org/).

Das wurde von Starlette <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr>, aber wenn Sie Code haben, der das verwendet, können Sie einfach zu [starlette-graphene3](https://github.com/ciscorn/starlette-graphene3) **migrieren**, das denselben Anwendungsfall abdeckt und eine **fast identische Schnittstelle** hat.

/// tip | Tipp

Wenn Sie GraphQL benötigen, würde ich Ihnen trotzdem empfehlen, sich [Strawberry](https://strawberry.rocks/) anzuschauen, da es auf Typannotationen basiert, statt auf benutzerdefinierten Klassen und Typen.

///

## Mehr darüber lernen { #learn-more }

Weitere Informationen zu **GraphQL** finden Sie in der [offiziellen GraphQL-Dokumentation](https://graphql.org/).

Sie können auch mehr über jede der oben beschriebenen Bibliotheken in den jeweiligen Links lesen.
