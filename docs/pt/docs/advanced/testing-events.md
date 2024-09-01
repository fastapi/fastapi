# Testando Eventos: inicialização - encerramento

Quando você precisa que os seus manipuladores de eventos (`startup` e `shutdown`) sejam executados em seus testes, você pode utilizar o `TestClient` usando a instrução `with`:

```Python hl_lines="9-12  20-24"
{!../../../docs_src/app_testing/tutorial003.py!}
```
