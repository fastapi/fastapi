# Démarrer { #first-steps }

Le fichier **FastAPI** le plus simple possible pourrait ressembler à ceci :

{* ../../docs_src/first_steps/tutorial001_py310.py *}

Copiez cela dans un fichier `main.py`.

Démarrez le serveur en direct :

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Dans la sortie, il y a une ligne semblable à :

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Cette ligne montre l’URL où votre application est servie, sur votre machine locale.

### Vérifier { #check-it }

Ouvrez votre navigateur à l’adresse <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Vous verrez la réponse JSON suivante :

```JSON
{"message": "Hello World"}
```

### Documentation interactive de l’API { #interactive-api-docs }

Allez maintenant sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation interactive de l’API générée automatiquement (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation alternative de l’API { #alternative-api-docs }

Et maintenant, allez sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation automatique alternative (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** génère un « schéma » contenant toute votre API en utilisant le standard **OpenAPI** pour définir des API.

#### « Schéma » { #schema }

Un « schéma » est une définition ou une description de quelque chose. Pas le code qui l’implémente, mais uniquement une description abstraite.

#### « Schéma » d’API { #api-schema }

Ici, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> est une spécification qui dicte comment définir le schéma de votre API.

Cette définition de schéma inclut les chemins de votre API, les paramètres possibles qu’ils prennent, etc.

#### « Schéma » de données { #data-schema }

Le terme « schéma » peut également faire référence à la forme d’une donnée, comme un contenu JSON.

Dans ce cas, cela désignerait les attributs JSON, ainsi que leurs types, etc.

#### OpenAPI et JSON Schema { #openapi-and-json-schema }

OpenAPI définit un schéma d’API pour votre API. Et ce schéma inclut des définitions (ou « schémas ») des données envoyées et reçues par votre API en utilisant **JSON Schema**, le standard pour les schémas de données JSON.

#### Voir le `openapi.json` { #check-the-openapi-json }

Si vous êtes curieux de voir à quoi ressemble le schéma OpenAPI brut, FastAPI génère automatiquement un JSON (schéma) avec les descriptions de toute votre API.

Vous pouvez le voir directement à l’adresse : <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Il affichera un JSON commençant par quelque chose comme :

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### À quoi sert OpenAPI { #what-is-openapi-for }

Le schéma OpenAPI est ce qui alimente les deux systèmes de documentation interactive inclus.

Et il existe des dizaines d’alternatives, toutes basées sur OpenAPI. Vous pourriez facilement ajouter n’importe laquelle de ces alternatives à votre application construite avec **FastAPI**.

Vous pourriez également l’utiliser pour générer du code automatiquement, pour les clients qui communiquent avec votre API. Par exemple, des applications frontend, mobiles ou IoT.

### Déployer votre application (optionnel) { #deploy-your-app-optional }

Vous pouvez, si vous le souhaitez, déployer votre application FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>, allez rejoindre la liste d’attente si ce n’est pas déjà fait. 🚀

Si vous avez déjà un compte **FastAPI Cloud** (nous vous avons invité depuis la liste d’attente 😉), vous pouvez déployer votre application avec une seule commande.

Avant de déployer, vous devez vous assurer que vous êtes connecté :

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Puis déployez votre application :

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

C’est tout ! Vous pouvez maintenant accéder à votre application à cette URL. ✨

## Récapitulatif, étape par étape { #recap-step-by-step }

### Étape 1 : importer `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` est une classe Python qui fournit toutes les fonctionnalités nécessaires à votre API.

/// note | Détails techniques

`FastAPI` est une classe qui hérite directement de `Starlette`.

Vous pouvez donc aussi utiliser toutes les fonctionnalités de <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> avec `FastAPI`.

///

### Étape 2 : créer une « instance » `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Ici, la variable `app` sera une « instance » de la classe `FastAPI`.

Ce sera le point principal d’interaction pour créer toute votre API.

### Étape 3 : créer un « chemin d’accès » { #step-3-create-a-path-operation }

#### Chemin { #path }

« Chemin » fait ici référence à la dernière partie de l’URL à partir du premier `/`.

Donc, dans une URL telle que :

```
https://example.com/items/foo
```

... le chemin serait :

```
/items/foo
```

/// info

Un « chemin » est aussi couramment appelé « endpoint » ou « route ».

///

Lors de la création d’une API, le « chemin » est la manière principale de séparer les « préoccupations » et les « ressources ».

#### Opération { #operation }

« Opération » fait ici référence à l’une des « méthodes » HTTP.

L’une de :

* `POST`
* `GET`
* `PUT`
* `DELETE`

... et les plus exotiques :

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Dans le protocole HTTP, vous pouvez communiquer avec chaque chemin en utilisant une (ou plusieurs) de ces « méthodes ».

---

En construisant des APIs, vous utilisez normalement ces méthodes HTTP spécifiques pour effectuer une action précise.

En général, vous utilisez :

* `POST` : pour créer des données.
* `GET` : pour lire des données.
* `PUT` : pour mettre à jour des données.
* `DELETE` : pour supprimer des données.

Donc, dans OpenAPI, chacune des méthodes HTTP est appelée une « opération ».

Nous allons donc aussi les appeler « opérations ».

#### Définir un « décorateur de chemin d’accès » { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

Le `@app.get("/")` indique à **FastAPI** que la fonction juste en dessous est chargée de gérer les requêtes qui vont vers :

* le chemin `/`
* en utilisant une <dfn title="une méthode HTTP GET"><code>get</code> opération</dfn>

/// info | `@decorator` Info

Cette syntaxe `@something` en Python est appelée un « décorateur ».

Vous la mettez au-dessus d’une fonction. Comme un joli chapeau décoratif (j’imagine que c’est de là que vient le terme 🤷🏻‍♂).

Un « décorateur » prend la fonction en dessous et fait quelque chose avec.

Dans notre cas, ce décorateur indique à **FastAPI** que la fonction en dessous correspond au **chemin** `/` avec une **opération** `get`.

C’est le « décorateur de chemin d’accès ».

///

Vous pouvez aussi utiliser les autres opérations :

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Ainsi que les plus exotiques :

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Astuce

Vous êtes libre d’utiliser chaque opération (méthode HTTP) comme vous le souhaitez.

**FastAPI** n’impose aucune signification spécifique.

Les informations ici sont présentées comme des lignes directrices, pas comme une obligation.

Par exemple, lorsque vous utilisez GraphQL, vous effectuez normalement toutes les actions en utilisant uniquement des opérations `POST`.

///

### Étape 4 : définir la **fonction de chemin d’accès** { #step-4-define-the-path-operation-function }

Voici notre « fonction de chemin d’accès » :

* **chemin** : `/`.
* **opération** : `get`.
* **fonction** : la fonction sous le « décorateur » (sous `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

C’est une fonction Python.

Elle sera appelée par **FastAPI** chaque fois qu’il recevra une requête vers l’URL « / » en utilisant une opération `GET`.

Dans ce cas, c’est une fonction `async`.

---

Vous pouvez aussi la définir comme une fonction normale au lieu de `async def` :

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | Remarque

Si vous ne connaissez pas la différence, consultez [Asynchrone : « Pressé ? »](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Étape 5 : retourner le contenu { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

Vous pouvez retourner un `dict`, une `list`, des valeurs uniques comme `str`, `int`, etc.

Vous pouvez également retourner des modèles Pydantic (vous en verrez plus à ce sujet plus tard).

Il existe de nombreux autres objets et modèles qui seront automatiquement convertis en JSON (y compris des ORM, etc.). Essayez d’utiliser vos favoris, il est fort probable qu’ils soient déjà pris en charge.

### Étape 6 : le déployer { #step-6-deploy-it }

Déployez votre application sur **<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** avec une seule commande : `fastapi deploy`. 🎉

#### À propos de FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** est construit par le même auteur et l’équipe derrière **FastAPI**.

Il simplifie le processus de **construction**, de **déploiement** et d’**accès** à une API avec un minimum d’effort.

Il apporte la même **expérience développeur** de création d’applications avec FastAPI au **déploiement** dans le cloud. 🎉

FastAPI Cloud est le sponsor principal et le financeur des projets open source *FastAPI and friends*. ✨

#### Déployer sur d’autres fournisseurs cloud { #deploy-to-other-cloud-providers }

FastAPI est open source et basé sur des standards. Vous pouvez déployer des applications FastAPI chez n’importe quel fournisseur cloud de votre choix.

Suivez les guides de votre fournisseur cloud pour y déployer des applications FastAPI. 🤓

## Récapitulatif { #recap }

* Importez `FastAPI`.
* Créez une instance `app`.
* Écrivez un **décorateur de chemin d’accès** avec des décorateurs comme `@app.get("/")`.
* Définissez une **fonction de chemin d’accès** ; par exemple, `def root(): ...`.
* Exécutez le serveur de développement avec la commande `fastapi dev`.
* Déployez éventuellement votre application avec `fastapi deploy`.
