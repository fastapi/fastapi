# Configurer Swagger UI { #configure-swagger-ui }

Vous pouvez configurer des <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">paramètres supplémentaires de Swagger UI</a>.

Pour les configurer, passez l'argument `swagger_ui_parameters` lors de la création de l'objet d'application `FastAPI()` ou à la fonction `get_swagger_ui_html()`.

`swagger_ui_parameters` reçoit un dictionnaire avec les configurations passées directement à Swagger UI.

FastAPI convertit les configurations en **JSON** pour les rendre compatibles avec JavaScript, car c'est ce dont Swagger UI a besoin.

## Désactiver la coloration syntaxique { #disable-syntax-highlighting }

Par exemple, vous pourriez désactiver la coloration syntaxique dans Swagger UI.

Sans modifier les paramètres, la coloration syntaxique est activée par défaut :

<img src="/img/tutorial/extending-openapi/image02.png">

Mais vous pouvez la désactiver en définissant `syntaxHighlight` à `False` :

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

... et ensuite Swagger UI n'affichera plus la coloration syntaxique :

<img src="/img/tutorial/extending-openapi/image03.png">

## Modifier le thème { #change-the-theme }

De la même manière, vous pouvez définir le thème de la coloration syntaxique avec la clé « syntaxHighlight.theme » (remarquez le point au milieu) :

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

Cette configuration modifierait le thème de couleurs de la coloration syntaxique :

<img src="/img/tutorial/extending-openapi/image04.png">

## Modifier les paramètres Swagger UI par défaut { #change-default-swagger-ui-parameters }

FastAPI inclut des paramètres de configuration par défaut adaptés à la plupart des cas d'utilisation.

Il inclut ces configurations par défaut :

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

Vous pouvez remplacer n'importe lequel d'entre eux en définissant une valeur différente dans l'argument `swagger_ui_parameters`.

Par exemple, pour désactiver `deepLinking`, vous pourriez passer ces paramètres à `swagger_ui_parameters` :

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## Autres paramètres de Swagger UI { #other-swagger-ui-parameters }

Pour voir toutes les autres configurations possibles que vous pouvez utiliser, lisez la <a href="https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/" class="external-link" target="_blank">documentation officielle des paramètres de Swagger UI</a>.

## Paramètres JavaScript uniquement { #javascript-only-settings }

Swagger UI permet également d'autres configurations qui sont des objets réservés à JavaScript (par exemple, des fonctions JavaScript).

FastAPI inclut aussi ces paramètres `presets` réservés à JavaScript :

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

Ce sont des objets **JavaScript**, pas des chaînes, vous ne pouvez donc pas les passer directement depuis du code Python.

Si vous devez utiliser des configurations réservées à JavaScript comme celles-ci, vous pouvez utiliser l'une des méthodes ci-dessus. Surchargez entièrement le *chemin d'accès* Swagger UI et écrivez manuellement tout JavaScript nécessaire.
