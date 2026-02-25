# Héberger en propre les ressources statiques de l’UI des docs personnalisées { #custom-docs-ui-static-assets-self-hosting }

Les documents de l’API utilisent **Swagger UI** et **ReDoc**, et chacune nécessite des fichiers JavaScript et CSS.

Par défaut, ces fichiers sont servis depuis un <abbr title="Content Delivery Network - Réseau de diffusion de contenu: Un service, normalement composé de plusieurs serveurs, qui fournit des fichiers statiques, comme JavaScript et CSS. Il est couramment utilisé pour servir ces fichiers depuis le serveur le plus proche du client, améliorant la performance.">CDN</abbr>.

Mais il est possible de le personnaliser : vous pouvez définir un CDN spécifique, ou servir vous‑même les fichiers.

## Configurer un CDN personnalisé pour JavaScript et CSS { #custom-cdn-for-javascript-and-css }

Supposons que vous souhaitiez utiliser un autre <abbr title="Content Delivery Network - Réseau de diffusion de contenu">CDN</abbr>, par exemple vous voulez utiliser `https://unpkg.com/`.

Cela peut être utile si, par exemple, vous vivez dans un pays qui restreint certaines URL.

### Désactiver les docs automatiques { #disable-the-automatic-docs }

La première étape consiste à désactiver les docs automatiques, car par défaut elles utilisent le CDN par défaut.

Pour les désactiver, définissez leurs URL sur `None` lors de la création de votre application `FastAPI` :

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### Inclure les docs personnalisées { #include-the-custom-docs }

Vous pouvez maintenant créer les chemins d'accès pour les docs personnalisées.

Vous pouvez réutiliser les fonctions internes de FastAPI pour créer les pages HTML de la documentation et leur passer les arguments nécessaires :

- `openapi_url` : l’URL où la page HTML des docs peut récupérer le schéma OpenAPI de votre API. Vous pouvez utiliser ici l’attribut `app.openapi_url`.
- `title` : le titre de votre API.
- `oauth2_redirect_url` : vous pouvez utiliser `app.swagger_ui_oauth2_redirect_url` ici pour utiliser la valeur par défaut.
- `swagger_js_url` : l’URL où la page HTML de Swagger UI peut récupérer le fichier **JavaScript**. C’est l’URL du CDN personnalisé.
- `swagger_css_url` : l’URL où la page HTML de Swagger UI peut récupérer le fichier **CSS**. C’est l’URL du CDN personnalisé.

Et de même pour ReDoc ...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | Astuce

Le chemin d'accès pour `swagger_ui_redirect` est un assistant lorsque vous utilisez OAuth2.

Si vous intégrez votre API à un fournisseur OAuth2, vous pourrez vous authentifier et revenir aux docs de l’API avec les identifiants acquis. Et interagir avec elle en utilisant la véritable authentification OAuth2.

Swagger UI s’en chargera en arrière‑plan pour vous, mais il a besoin de cet assistant « redirect ».

///

### Créer un chemin d'accès pour tester { #create-a-path-operation-to-test-it }

Maintenant, pour pouvoir vérifier que tout fonctionne, créez un chemin d'accès :

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### Tester { #test-it }

Vous devriez maintenant pouvoir aller à vos docs sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, puis recharger la page : elle chargera ces ressources depuis le nouveau CDN.

## Héberger en propre JavaScript et CSS pour les docs { #self-hosting-javascript-and-css-for-docs }

Héberger vous‑même le JavaScript et le CSS peut être utile si, par exemple, votre application doit continuer de fonctionner même hors ligne, sans accès Internet ouvert, ou sur un réseau local.

Vous verrez ici comment servir ces fichiers vous‑même, dans la même application FastAPI, et configurer les docs pour les utiliser.

### Structure des fichiers du projet { #project-file-structure }

Supposons que la structure de vos fichiers de projet ressemble à ceci :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

Créez maintenant un répertoire pour stocker ces fichiers statiques.

Votre nouvelle structure de fichiers pourrait ressembler à ceci :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### Télécharger les fichiers { #download-the-files }

Téléchargez les fichiers statiques nécessaires aux docs et placez‑les dans ce répertoire `static/`.

Vous pouvez probablement cliquer avec le bouton droit sur chaque lien et choisir une option similaire à « Enregistrer le lien sous ... ».

**Swagger UI** utilise les fichiers :

- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

Et **ReDoc** utilise le fichier :

- <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

Après cela, votre structure de fichiers pourrait ressembler à :

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### Servir les fichiers statiques { #serve-the-static-files }

- Importer `StaticFiles`.
- « Monter » une instance `StaticFiles()` sur un chemin spécifique.

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### Tester les fichiers statiques { #test-the-static-files }

Démarrez votre application et rendez‑vous sur <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>.

Vous devriez voir un très long fichier JavaScript pour **ReDoc**.

Il pourrait commencer par quelque chose comme :

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

Cela confirme que vous parvenez à servir des fichiers statiques depuis votre application et que vous avez placé les fichiers statiques des docs au bon endroit.

Nous pouvons maintenant configurer l’application pour utiliser ces fichiers statiques pour les docs.

### Désactiver les docs automatiques pour les fichiers statiques { #disable-the-automatic-docs-for-static-files }

Comme lors de l’utilisation d’un CDN personnalisé, la première étape consiste à désactiver les docs automatiques, car elles utilisent un CDN par défaut.

Pour les désactiver, définissez leurs URL sur `None` lors de la création de votre application `FastAPI` :

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### Inclure les docs personnalisées pour les fichiers statiques { #include-the-custom-docs-for-static-files }

Et comme avec un CDN personnalisé, vous pouvez maintenant créer les chemins d'accès pour les docs personnalisées.

Là encore, vous pouvez réutiliser les fonctions internes de FastAPI pour créer les pages HTML de la documentation et leur passer les arguments nécessaires :

- `openapi_url` : l’URL où la page HTML des docs peut récupérer le schéma OpenAPI de votre API. Vous pouvez utiliser ici l’attribut `app.openapi_url`.
- `title` : le titre de votre API.
- `oauth2_redirect_url` : vous pouvez utiliser `app.swagger_ui_oauth2_redirect_url` ici pour utiliser la valeur par défaut.
- `swagger_js_url` : l’URL où la page HTML de Swagger UI peut récupérer le fichier **JavaScript**. **C’est celui que votre propre application sert désormais**.
- `swagger_css_url` : l’URL où la page HTML de Swagger UI peut récupérer le fichier **CSS**. **C’est celui que votre propre application sert désormais**.

Et de même pour ReDoc ...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | Astuce

Le chemin d'accès pour `swagger_ui_redirect` est un assistant lorsque vous utilisez OAuth2.

Si vous intégrez votre API à un fournisseur OAuth2, vous pourrez vous authentifier et revenir aux docs de l’API avec les identifiants acquis. Et interagir avec elle en utilisant la véritable authentification OAuth2.

Swagger UI s’en chargera en arrière‑plan pour vous, mais il a besoin de cet assistant « redirect ».

///

### Créer un chemin d'accès pour tester les fichiers statiques { #create-a-path-operation-to-test-static-files }

Maintenant, pour pouvoir vérifier que tout fonctionne, créez un chemin d'accès :

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### Tester l’UI avec des fichiers statiques { #test-static-files-ui }

Vous devriez maintenant pouvoir couper votre Wi‑Fi, aller à vos docs sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> et recharger la page.

Et même sans Internet, vous pourrez voir la documentation de votre API et interagir avec elle.
