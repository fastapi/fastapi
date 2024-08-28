# Events testen: Hochfahren – Herunterfahren

Wenn Sie in Ihren Tests Ihre Event-Handler (`startup` und `shutdown`) ausführen wollen, können Sie den `TestClient` mit einer `with`-Anweisung verwenden:

```Python hl_lines="9-12  20-24"
{!../../../docs_src/app_testing/tutorial003.py!}
```
