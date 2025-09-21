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

* <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> 🍓
    * Mit <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Dokumentation für FastAPI</a>
* <a href="https://ariadnegraphql.org/" class="external-link" target="_blank">Ariadne</a>
    * Mit <a href="https://ariadnegraphql.org/docs/fastapi-integration" class="external-link" target="_blank">Dokumentation für FastAPI</a>
* <a href="https://tartiflette.io/" class="external-link" target="_blank">Tartiflette</a>
    * Mit <a href="https://tartiflette.github.io/tartiflette-asgi/" class="external-link" target="_blank">Tartiflette ASGI</a> für ASGI-Integration
* <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>
    * Mit <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a>

## GraphQL mit Strawberry { #graphql-with-strawberry }

Wenn Sie mit **GraphQL** arbeiten möchten oder müssen, ist <a href="https://strawberry.rocks/" class="external-link" target="_blank">**Strawberry**</a> die **empfohlene** Bibliothek, da deren Design **FastAPIs** Design am nächsten kommt und alles auf **Typannotationen** basiert.

Abhängig von Ihrem Anwendungsfall könnten Sie eine andere Bibliothek vorziehen, aber wenn Sie mich fragen würden, würde ich Ihnen wahrscheinlich empfehlen, **Strawberry** auszuprobieren.

Hier ist eine kleine Vorschau, wie Sie Strawberry mit FastAPI integrieren können:

{* ../../docs_src/graphql/tutorial001.py hl[3,22,25] *}

Weitere Informationen zu Strawberry finden Sie in der <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry-Dokumentation</a>.

Und auch in der Dokumentation zu <a href="https://strawberry.rocks/docs/integrations/fastapi" class="external-link" target="_blank">Strawberry mit FastAPI</a>.

## Ältere `GraphQLApp` von Starlette { #older-graphqlapp-from-starlette }

Frühere Versionen von Starlette enthielten eine `GraphQLApp`-Klasse zur Integration mit <a href="https://graphene-python.org/" class="external-link" target="_blank">Graphene</a>.

Das wurde von Starlette <abbr title="veraltet, obsolet: Es soll nicht mehr verwendet werden">deprecatet</abbr>, aber wenn Sie Code haben, der das verwendet, können Sie einfach zu <a href="https://github.com/ciscorn/starlette-graphene3" class="external-link" target="_blank">starlette-graphene3</a> **migrieren**, das denselben Anwendungsfall abdeckt und eine **fast identische Schnittstelle** hat.

/// tip | Tipp

Wenn Sie GraphQL benötigen, würde ich Ihnen trotzdem empfehlen, sich <a href="https://strawberry.rocks/" class="external-link" target="_blank">Strawberry</a> anzuschauen, da es auf Typannotationen basiert, statt auf benutzerdefinierten Klassen und Typen.

///

## Mehr darüber lernen { #learn-more }

Weitere Informationen zu **GraphQL** finden Sie in der <a href="https://graphql.org/" class="external-link" target="_blank">offiziellen GraphQL-Dokumentation</a>.

Sie können auch mehr über jede der oben beschriebenen Bibliotheken in den jeweiligen Links lesen.
