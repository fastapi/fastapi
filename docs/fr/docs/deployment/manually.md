# Déployer manuellement

Vous pouvez également déployer **FastAPI** manuellement.

Il vous suffit d'installer un serveur compatible ASGI comme :

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, un serveur ASGI rapide comme l'éclair, basé sur uvloop et httptools.

    <div class="termy">

    ```console
    $ pip install uvicorn[standard]

    ---> 100%
    ```

    </div>

    !!! tip "Astuce"
        En ajoutant le `standard`, Uvicorn va installer et utiliser quelques dépendances supplémentaires recommandées.
        
        Cela inclut `uvloop`, le remplaçant performant de `asyncio`, qui fournit le gros gain de performance en matière de concurrence.

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, un serveur ASGI également compatible avec HTTP/2.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...ou tout autre serveur ASGI.

Et d'exécuter votre application comme vous l'avez fait dans les tutoriels, mais sans l'option `--reload`, par exemple :

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```

    </div>

Vous pourriez vouloir mettre en place des outils pour vous assurer qu'il est redémarré automatiquement s'il s'arrête.

Vous pourriez également vouloir installer <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a> et <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">l'utiliser comme gestionnaire pour Uvicorn</a>, ou utiliser Hypercorn avec plusieurs workers.

Assurez-vous d'ajuster le nombre de workers, etc.

Mais si vous faites tout cela, vous pouvez simplement utiliser l'image Docker qui le fait automatiquement.
