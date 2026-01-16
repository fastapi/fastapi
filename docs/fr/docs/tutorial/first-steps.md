# Premiers pas { #first-steps }

Le fichier **FastAPI** le plus simple possible pourrait ressembler à ceci :

{* ../../docs_src/first_steps/tutorial001_py39.py *}

Copiez cela dans un fichier `main.py`.

Lancez le serveur de développement :

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

Dans la sortie, il y a une ligne qui ressemble à :

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Cette ligne affiche l’URL à laquelle votre app est servie, sur votre machine locale.

### Vérifiez { #check-it }

Ouvrez votre navigateur à l’adresse <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Vous verrez la réponse JSON :

```JSON
{"message": "Hello World"}
```

### Documentation interactive de l’API { #interactive-api-docs }

Rendez-vous maintenant sur <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Vous verrez la documentation interactive de l’API générée automatiquement (fournie par <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>) :

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Documentation alternative de l’API { #alternative-api-docs }

Et maintenant, rendez-vous sur <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Vous verrez la documentation alternative générée automatiquement (fournie par <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>) :

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI** génère un « schéma » contenant toute votre API en utilisant le standard **OpenAPI** pour définir les API.

#### « Schéma » { #schema }

Un « schéma » est une définition ou une description de quelque chose. Pas le code qui l’implémente, mais simplement une description abstraite.

#### « Schéma » d’API { #api-schema }

Dans ce cas, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> est une spécification qui dicte comment définir un schéma de votre API.

Cette définition de schéma inclut les chemins de votre API, les paramètres possibles qu’ils acceptent, etc.

#### « Schéma » de données { #data-schema }

Le terme « schéma » peut aussi faire référence à la structure de certaines données, comme un contenu JSON.

Dans ce cas, cela signifierait les attributs JSON, et les types de données qu’ils ont, etc.

#### OpenAPI et JSON Schema { #openapi-and-json-schema }

OpenAPI définit un schéma d’API pour votre API. Et ce schéma inclut des définitions (ou des « schémas ») des données envoyées et reçues par votre API en utilisant **JSON Schema**, le standard des schémas de données JSON.

#### Vérifiez le `openapi.json` { #check-the-openapi-json }

Si vous êtes curieux de voir à quoi ressemble le schéma OpenAPI brut, FastAPI génère automatiquement un (schéma) JSON avec les descriptions de toute votre API.

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

Vous pourriez aussi l’utiliser pour générer du code automatiquement, pour les clients qui communiquent avec votre API. Par exemple, des applications frontend, mobiles ou IoT.

### Déployer votre app (optionnel) { #deploy-your-app-optional }

Vous pouvez, de manière optionnelle, déployer votre app FastAPI sur <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> ; allez vous inscrire sur la liste d’attente si ce n’est pas déjà fait. 🚀

Si vous avez déjà un compte **FastAPI Cloud** (nous vous avons invité depuis la liste d’attente 😉), vous pouvez déployer votre application avec une seule commande.

Avant de déployer, vous devez vous assurer que vous êtes connecté :

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

Ensuite, déployez votre app :

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

C’est tout ! Vous pouvez maintenant accéder à votre app à cette URL. ✨

## Récapitulatif, étape par étape { #recap-step-by-step }

### Étape 1 : importer `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[1] *}

`FastAPI` est une classe Python qui fournit toutes les fonctionnalités pour votre API.

/// note | Détails techniques

`FastAPI` est une classe qui hérite directement de `Starlette`.

Vous pouvez aussi utiliser toutes les fonctionnalités de <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> avec `FastAPI`.

///

### Étape 2 : créer une « instance » `FastAPI` { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[3] *}

Ici, la variable `app` sera une « instance » de la classe `FastAPI`.

Ce sera le point principal d’interaction pour créer toute votre API.

### Étape 3 : créer un *chemin d'accès* { #step-3-create-a-path-operation }

#### Chemin { #path }

« Path » fait référence ici à la dernière partie de l’URL à partir du premier `/`.

Donc, dans une URL comme :

```
https://example.com/items/foo
```

... le « path » serait :

```
/items/foo
```

/// info

Un « path » est aussi communément appelé un « endpoint » ou une « route ».

///

Lors de la construction d’une API, le « path » est la principale façon de séparer les « préoccupations » et les « ressources ».

#### Opération { #operation }

« Opération » fait référence ici à l’une des « méthodes » HTTP.

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

Lors de la construction d’API, vous utilisez normalement ces méthodes HTTP spécifiques pour effectuer une action précise.

Normalement vous utilisez :

* `POST` : pour créer des données.
* `GET` : pour lire des données.
* `PUT` : pour mettre à jour des données.
* `DELETE` : pour supprimer des données.

Donc, dans OpenAPI, chacune des méthodes HTTP est appelée une « opération ».

Nous allons aussi les appeler des « **opérations** ».

#### Définir un *décorateur de chemin d'accès* { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[6] *}

Le `@app.get("/")` indique à **FastAPI** que la fonction juste en dessous est chargée de gérer les requêtes qui vont vers :

* le chemin `/`
* en utilisant une <abbr title="an HTTP GET method">opération <code>get</code></abbr>

/// info | `@decorator` Info

Cette syntaxe `@something` en Python est appelée un « décorateur ».

Vous le mettez au-dessus d’une fonction. Comme un joli chapeau décoratif (j’imagine que c’est de là que le terme vient).

Un « décorateur » prend la fonction en dessous et fait quelque chose avec elle.

Dans notre cas, ce décorateur indique à **FastAPI** que la fonction en dessous correspond au **chemin** `/` avec une **opération** `get`.

C’est le « **décorateur de chemin d'accès** ».

///

Vous pouvez aussi utiliser les autres opérations :

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Et les plus exotiques :

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | Astuce

Vous êtes libre d’utiliser chaque opération (méthode HTTP) comme vous le souhaitez.

**FastAPI** n’impose aucun sens spécifique.

Les informations présentées ici servent de guide, pas d’exigence.

Par exemple, quand vous utilisez GraphQL, vous effectuez normalement toutes les actions en utilisant uniquement des opérations `POST`.

///

### Étape 4 : définir la **fonction de chemin d'accès** { #step-4-define-the-path-operation-function }

Voici notre « **fonction de chemin d'accès** » :

* **chemin** : est `/`.
* **opération** : est `get`.
* **fonction** : est la fonction sous le « décorateur » (sous `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001_py39.py hl[7] *}

C’est une fonction Python.

Elle sera appelée par **FastAPI** chaque fois qu’il recevra une requête vers l’URL « `/` » en utilisant une opération `GET`.

Dans ce cas, c’est une fonction `async`.

---

Vous pourriez aussi la définir comme une fonction normale au lieu de `async def` :

{* ../../docs_src/first_steps/tutorial003_py39.py hl[7] *}

/// note | Remarque

Si vous ne connaissez pas la différence, consultez [Async : *« Pressé ? »*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Étape 5 : retourner le contenu { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py39.py hl[8] *}

Vous pouvez retourner un `dict`, `list`, des valeurs seules comme `str`, `int`, etc.

Vous pouvez aussi retourner des modèles Pydantic (vous en verrez plus à ce sujet plus tard).

Il y a de nombreux autres objets et modèles qui seront automatiquement convertis en JSON (y compris les ORM, etc). Essayez d’utiliser vos favoris, il est très probable qu’ils soient déjà pris en charge.

### Étape 6 : le déployer { #step-6-deploy-it }

Déployez votre app sur **<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** avec une seule commande : `fastapi deploy`. 🎉

#### À propos de FastAPI Cloud { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** est construit par le même auteur et la même équipe derrière **FastAPI**.

Il simplifie le processus de **construction**, de **déploiement** et d’**accès** à une API avec un effort minimal.

Il apporte la même **developer experience** de construction d’apps avec FastAPI au **déploiement** dans le cloud. 🎉

FastAPI Cloud est le sponsor principal et le fournisseur de financement pour les projets open source *FastAPI and friends*. ✨

#### Déployer sur d’autres fournisseurs cloud { #deploy-to-other-cloud-providers }

FastAPI est open source et basé sur des standards. Vous pouvez déployer des apps FastAPI sur n’importe quel fournisseur cloud de votre choix.

Suivez les guides de votre fournisseur cloud pour y déployer des apps FastAPI. 🤓

## Récapitulatif { #recap }

* Importez `FastAPI`.
* Créez une instance `app`.
* Écrivez un **décorateur de chemin d'accès** en utilisant des décorateurs comme `@app.get("/")`.
* Définissez une **fonction de chemin d'accès** ; par exemple, `def root(): ...`.
* Lancez le serveur de développement avec la commande `fastapi dev`.
* Déployez votre app de manière optionnelle avec `fastapi deploy`.
