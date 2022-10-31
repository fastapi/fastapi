# Déployer FastAPI sur Deta

Dans cette section, vous apprendrez à déployer facilement une application **FastAPI** sur <a href="https://www.deta.
sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> en utilisant le plan tarifaire gratuit. 🎁

Cela vous prendra environ **10 minutes**.

!!! info
    <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> sponsorise **FastAPI**. 🎉

## Une application **FastAPI** de base

* Créez un répertoire pour votre application, par exemple `./fastapideta/` et déplacez-vous dedans.

### Le code FastAPI

* Créer un fichier `main.py` avec :

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Dépendances

Maintenant, dans le même répertoire, créez un fichier `requirements.txt` avec :

```text
fastapi
```

!!! tip "Astuce"
    Il n'est pas nécessaire d'installer Uvicorn pour déployer sur Deta, bien qu'il soit probablement souhaitable de l'installer localement pour tester votre application.

### Structure du répertoire

Vous aurez maintenant un répertoire `./fastapideta/` avec deux fichiers :

```
.
└── main.py
└── requirements.txt
```

## Créer un compte gratuit sur Deta

Créez maintenant un <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">compte gratuit
sur Deta</a>, vous avez juste besoin d'une adresse email et d'un mot de passe.

Vous n'avez même pas besoin d'une carte de crédit.

## Installer le CLI (Interface en Ligne de Commande)

Une fois que vous avez votre compte, installez le  <abbr title="Command Line Interface application">CLI</abbr> de Deta :

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/cli.sh | sh
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/cli.ps1 -useb | iex
    ```

    </div>

Après l'avoir installé, ouvrez un nouveau terminal afin que la nouvelle installation soit détectée.

Dans un nouveau terminal, confirmez qu'il a été correctement installé avec :

<div class="termy">

```console
$ deta --help

Deta command line interface for managing deta micros.
Complete documentation available at https://docs.deta.sh

Usage:
  deta [flags]
  deta [command]

Available Commands:
  auth        Change auth settings for a deta micro

...
```

</div>

!!! tip "Astuce"
    Si vous rencontrez des problèmes pour installer le CLI, consultez la <a href="https://docs.deta. sh/docs/micros/getting_started?ref=fastapi" class="external-link" target="_blank">documentation officielle de Deta (en anglais)</a>.

## Connexion avec le CLI

Maintenant, connectez-vous à Deta depuis le CLI avec :

<div class="termy">

```console
$ deta login

Please, log in from the web page. Waiting..
Logged in successfully.
```

</div>

Cela ouvrira un navigateur web et permettra une authentification automatique.

## Déployer avec Deta

Ensuite, déployez votre application avec le CLI de Deta :

<div class="termy">

```console
$ deta new

Successfully created a new micro

// Notice the "endpoint" 🔍

{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}

Adding dependencies...


---> 100%


Successfully installed fastapi-0.61.1 pydantic-1.7.2 starlette-0.13.6
```

</div>

Vous verrez un message JSON similaire à :

```JSON hl_lines="4"
{
        "name": "fastapideta",
        "runtime": "python3.7",
        "endpoint": "https://qltnci.deta.dev",
        "visor": "enabled",
        "http_auth": "enabled"
}
```

!!! tip "Astuce"
    Votre déploiement aura une URL `"endpoint"` différente.

## Vérifiez

Maintenant, dans votre navigateur ouvrez votre URL `endpoint`. Dans l'exemple ci-dessus, c'était
`https://qltnci.deta.dev`, mais la vôtre sera différente.

Vous verrez la réponse JSON de votre application FastAPI :

```JSON
{
    "Hello": "World"
}
```

Et maintenant naviguez vers `/docs` dans votre API, dans l'exemple ci-dessus ce serait `https://qltnci.deta.dev/docs`.

Vous verrez votre documentation comme suit :

<img src="/img/deployment/deta/image01.png">

## Activer l'accès public

Par défaut, Deta va gérer l'authentification en utilisant des cookies pour votre compte.

Mais une fois que vous êtes prêt, vous pouvez le rendre public avec :

<div class="termy">

```console
$ deta auth disable

Successfully disabled http auth
```

</div>

Maintenant, vous pouvez partager cette URL avec n'importe qui et ils seront en mesure d'accéder à votre API. 🚀

## HTTPS

Félicitations ! Vous avez déployé votre application FastAPI sur Deta ! 🎉 🍰

Remarquez également que Deta gère correctement HTTPS pour vous, vous n'avez donc pas à vous en occuper et pouvez être sûr que vos clients auront une connexion cryptée sécurisée. ✅ 🔒

## Vérifiez le Visor

À partir de l'interface graphique de votre documentation (dans une URL telle que `https://qltnci.deta.dev/docs`)
envoyez une requête à votre *opération de chemin* `/items/{item_id}`.

Par exemple avec l'ID `5`.

Allez maintenant sur <a href="https://web.deta.sh/" class="external-link" target="_blank">https://web.deta.sh</a>.

Vous verrez qu'il y a une section à gauche appelée <abbr title="ça vient de Micro(server)">"Micros"</abbr> avec chacune de vos applications.

Vous verrez un onglet avec "Details", et aussi un onglet "Visor", allez à l'onglet "Visor".

Vous pouvez y consulter les requêtes récentes envoyées à votre application.

Vous pouvez également les modifier et les relancer.

<img src="/img/deployment/deta/image02.png">

## En savoir plus

À un moment donné, vous voudrez probablement stocker certaines données pour votre application d'une manière qui
persiste dans le temps. Pour cela, vous pouvez utiliser <a href="https://docs.deta.sh/docs/base/py_tutorial?ref=fastapi" class="external-link" target="_blank">Deta Base</a>, il dispose également d'un généreux **plan gratuit**.

Vous pouvez également en lire plus dans la <a href="https://docs.deta.sh?ref=fastapi" class="external-link" target="_blank">documentation Deta</a>.
