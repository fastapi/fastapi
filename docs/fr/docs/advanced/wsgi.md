# Inclure WSGI - Flask, Django, autres { #including-wsgi-flask-django-others }

Vous pouvez monter des applications WSGI comme vous l'avez vu avec [Sous-applications - Montages](sub-applications.md){.internal-link target=_blank}, [Derrière un proxy](behind-a-proxy.md){.internal-link target=_blank}.

Pour cela, vous pouvez utiliser `WSGIMiddleware` et l'utiliser pour envelopper votre application WSGI, par exemple Flask, Django, etc.

## Utiliser `WSGIMiddleware` { #using-wsgimiddleware }

/// info

Cela nécessite l'installation de `a2wsgi`, par exemple avec `pip install a2wsgi`.

///

Vous devez importer `WSGIMiddleware` depuis `a2wsgi`.

Ensuite, enveloppez l'application WSGI (par ex. Flask) avec le middleware.

Puis, montez-la sous un chemin.

{* ../../docs_src/wsgi/tutorial001_py310.py hl[1,3,23] *}

/// note | Remarque

Auparavant, il était recommandé d'utiliser `WSGIMiddleware` depuis `fastapi.middleware.wsgi`, mais il est désormais déprécié.

Il est conseillé d'utiliser le package `a2wsgi` à la place. L'utilisation reste la même.

Assurez-vous simplement que le package `a2wsgi` est installé et importez `WSGIMiddleware` correctement depuis `a2wsgi`.

///

## Vérifiez { #check-it }

Désormais, chaque requête sous le chemin `/v1/` sera gérée par l'application Flask.

Et le reste sera géré par **FastAPI**.

Si vous l'exécutez et allez à <a href="http://localhost:8000/v1/" class="external-link" target="_blank">http://localhost:8000/v1/</a>, vous verrez la réponse de Flask :

```txt
Hello, World from Flask!
```

Et si vous allez à <a href="http://localhost:8000/v2" class="external-link" target="_blank">http://localhost:8000/v2</a>, vous verrez la réponse de FastAPI :

```JSON
{
    "message": "Hello World"
}
```
