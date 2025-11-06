# Events testen: Lifespan und Startup – Shutdown { #testing-events-lifespan-and-startup-shutdown }

Wenn Sie `lifespan` in Ihren Tests ausführen müssen, können Sie den `TestClient` mit einer `with`-Anweisung verwenden:

{* ../../docs_src/app_testing/tutorial004.py hl[9:15,18,27:28,30:32,41:43] *}


Sie können mehr Details unter [„Lifespan in Tests ausführen in der offiziellen Starlette-Dokumentation.“](https://www.starlette.dev/lifespan/#running-lifespan-in-tests) nachlesen.

Für die deprecateten Events <abbr title="Hochfahren">`startup`</abbr> und <abbr title="Herunterfahren">`shutdown`</abbr> können Sie den `TestClient` wie folgt verwenden:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
