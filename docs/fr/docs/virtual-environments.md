# Environnements virtuels { #virtual-environments }

Lorsque vous travaillez sur des projets Python, vous devez utiliser un **environnement virtuel** pour isoler les packages installés pour chaque projet.

Pour les projets FastAPI, je recommande d’utiliser [uv](https://docs.astral.sh/uv/) pour gérer le projet, ses dépendances et son environnement virtuel.

## Créer un projet { #create-a-project }

Installez `uv` en utilisant le [guide d’installation officiel](https://docs.astral.sh/uv/getting-started/installation/), puis créez un projet :

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` crée automatiquement un environnement virtuel pour le projet. Vous n’avez pas besoin d’en créer ou d’en activer un vous-même.

Exécutez les commandes dans l’environnement du projet avec `uv run`, par exemple :

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## En savoir plus { #learn-more }

Lisez le [guide sur les environnements virtuels](https://tiangolo.com/guides/virtual-environments/) pour apprendre comment les environnements virtuels fonctionnent en dessous, y compris l’activation et le workflow alternatif avec `python -m venv` et `pip`.
