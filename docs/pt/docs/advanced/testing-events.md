# Testando eventos: lifespan e inicialização - encerramento { #testing-events-lifespan-and-startup-shutdown }

Quando você precisa que o `lifespan` seja executado em seus testes, você pode utilizar o `TestClient` com a instrução `with`:

{* ../../docs_src/app_testing/tutorial004.py hl[9:15,18,27:28,30:32,41:43] *}

Você pode ler mais detalhes sobre o ["Executando lifespan em testes no site oficial da documentação do Starlette."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

Para os eventos `startup` e `shutdown` descontinuados, você pode usar o `TestClient` da seguinte forma:

{* ../../docs_src/app_testing/tutorial003.py hl[9:12,20:24] *}
