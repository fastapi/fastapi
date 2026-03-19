# Configurer OpenAPI de manière conditionnelle { #conditional-openapi }

Si nécessaire, vous pouvez utiliser des paramètres et des variables d'environnement pour configurer OpenAPI de manière conditionnelle selon l'environnement, et même le désactiver complètement.

## À propos de la sécurité, des API et de la documentation { #about-security-apis-and-docs }

Masquer vos interfaces utilisateur de la documentation en production ne devrait pas être la manière de protéger votre API.

Cela n'ajoute aucune sécurité supplémentaire à votre API, les *chemins d'accès* resteront disponibles là où ils se trouvent.

S'il y a une faille de sécurité dans votre code, elle existera toujours.

Masquer la documentation rend simplement plus difficile la compréhension de la manière d'interagir avec votre API et pourrait aussi rendre son débogage en production plus difficile. Cela pourrait être considéré simplement comme une forme de <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Sécurité par l'obscurité</a>.

Si vous voulez sécuriser votre API, il y a plusieurs meilleures approches possibles, par exemple :

* Vous devez vous assurer d'avoir des modèles Pydantic bien définis pour le corps de la requête et la réponse.
* Configurez toutes les autorisations et tous les rôles nécessaires à l'aide de dépendances.
* Ne stockez jamais de mots de passe en clair, seulement des hachages de mots de passe.
* Implémentez et utilisez des outils cryptographiques reconnus, comme pwdlib et des jetons JWT, ... etc.
* Ajoutez des contrôles d'autorisation plus granulaires avec des scopes OAuth2 lorsque nécessaire.
* ... etc.

Néanmoins, vous pourriez avoir un cas d'utilisation très spécifique où vous devez vraiment désactiver la documentation de l'API pour un certain environnement (par exemple pour la production) ou selon des configurations provenant de variables d'environnement.

## Configurer OpenAPI de manière conditionnelle avec des paramètres et des variables d'environnement { #conditional-openapi-from-settings-and-env-vars }

Vous pouvez facilement utiliser les mêmes paramètres Pydantic pour configurer votre OpenAPI généré et les interfaces utilisateur de la documentation.

Par exemple :

{* ../../docs_src/conditional_openapi/tutorial001_py310.py hl[6,11] *}

Ici nous déclarons le paramètre `openapi_url` avec la même valeur par défaut `"/openapi.json"`.

Nous l'utilisons ensuite lors de la création de l'application `FastAPI`.

Vous pouvez alors désactiver OpenAPI (y compris les interfaces utilisateur de la documentation) en définissant la variable d'environnement `OPENAPI_URL` sur la chaîne vide, comme ceci :

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Ensuite, si vous allez aux URL `/openapi.json`, `/docs` ou `/redoc`, vous obtiendrez simplement une erreur `404 Not Found` comme :

```JSON
{
    "detail": "Not Found"
}
```
