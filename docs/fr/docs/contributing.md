# Développement - Contribuer

Tout d'abord, vous voudrez peut-être voir les moyens de base pour [aider FastAPI et obtenir de l'aide](help-fastapi.md){.internal-link target=_blank}.

## Développement

Si vous avez déjà cloné le dépôt et que vous savez que vous devez vous plonger dans le code, voici quelques directives pour mettre en place votre environnement.

### Environnement virtuel avec `venv`

Vous pouvez créer un environnement virtuel dans un répertoire en utilisant le module `venv` de Python :

<div class="termy">

```console
$ python -m venv env
```

</div>

Cela va créer un répertoire `./env/` avec les binaires Python et vous pourrez alors installer des paquets pour cet environnement isolé.

### Activer l'environnement

Activez le nouvel environnement avec :

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ source ./env/bin/activate
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ .\env\Scripts\Activate.ps1
    ```

    </div>

=== "Windows Bash"

    Ou si vous utilisez Bash pour Windows (par exemple <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

Pour vérifier que cela a fonctionné, utilisez :

=== "Linux, macOS, Windows Bash"

    <div class="termy">

    ```console
    $ which pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ Get-Command pip

    some/directory/fastapi/env/bin/pip
    ```

    </div>

Si celui-ci montre le binaire `pip` à `env/bin/pip`, alors ça a fonctionné. 🎉



!!! tip
    Chaque fois que vous installez un nouveau paquet avec `pip` sous cet environnement, activez à nouveau l'environnement.

    Cela permet de s'assurer que si vous utilisez un programme terminal installé par ce paquet (comme `flit`), vous utilisez celui de votre environnement local et pas un autre qui pourrait être installé globalement.

### Flit

**FastAPI** utilise <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> pour build, packager et publier le projet.

Après avoir activé l'environnement comme décrit ci-dessus, installez `flit` :

<div class="termy">

```console
$ pip install flit

---> 100%
```

</div>

Réactivez maintenant l'environnement pour vous assurer que vous utilisez le "flit" que vous venez d'installer (et non un environnement global).

Et maintenant, utilisez `flit` pour installer les dépendances de développement :

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ flit install --deps develop --symlink

    ---> 100%
    ```

    </div>

=== "Windows"

    Si vous êtes sous Windows, utilisez `--pth-file` au lieu de `--symlink` :

    <div class="termy">

    ```console
    $ flit install --deps develop --pth-file

    ---> 100%
    ```

    </div>

Il installera toutes les dépendances et votre FastAPI local dans votre environnement local.

#### Utiliser votre FastAPI local

Si vous créez un fichier Python qui importe et utilise FastAPI, et que vous l'exécutez avec le Python de votre environnement local, il utilisera votre code source FastAPI local.

Et si vous mettez à jour le code source local de FastAPI, tel qu'il est installé avec `--symlink` (ou `--pth-file` sous Windows), lorsque vous exécutez à nouveau ce fichier Python, il utilisera la nouvelle version de FastAPI que vous venez d'éditer.

De cette façon, vous n'avez pas à "installer" votre version locale pour pouvoir tester chaque changement.

### Formatage

Il existe un script que vous pouvez exécuter qui formatera et nettoiera tout votre code :

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Il effectuera également un tri automatique de touts vos imports.

Pour qu'il puisse les trier correctement, vous devez avoir FastAPI installé localement dans votre environnement, avec la commande dans la section ci-dessus en utilisant `--symlink` (ou `--pth-file` sous Windows).

### Formatage des imports

Il existe un autre script qui permet de formater touts les imports et de s'assurer que vous n'avez pas d'imports inutilisés :

<div class="termy">

```console
$ bash scripts/format-imports.sh
```

</div>

Comme il exécute une commande après l'autre et modifie et inverse de nombreux fichiers, il prend un peu plus de temps à s'exécuter, il pourrait donc être plus facile d'utiliser fréquemment `scripts/format.sh` et `scripts/format-imports.sh` seulement avant de commit.

## Documentation

Tout d'abord, assurez-vous que vous configurez votre environnement comme décrit ci-dessus, qui installera toutes les exigences.

La documentation utilise <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

Et il y a des outils/scripts supplémentaires en place pour gérer les traductions dans `./scripts/docs.py`.

!!! tip
    Vous n'avez pas besoin de voir le code dans `./scripts/docs.py`, vous l'utilisez simplement dans la ligne de commande.

Toute la documentation est au format Markdown dans le répertoire `./docs/fr/`.

De nombreux tutoriels comportent des blocs de code.

Dans la plupart des cas, ces blocs de code sont de véritables applications complètes qui peuvent être exécutées telles quelles.

En fait, ces blocs de code ne sont pas écrits à l'intérieur du Markdown, ce sont des fichiers Python dans le répertoire `./docs_src/`.

Et ces fichiers Python sont inclus/injectés dans la documentation lors de la génération du site.

### Documentation pour les tests

La plupart des tests sont en fait effectués par rapport aux exemples de fichiers sources dans la documentation.

Cela permet de s'assurer que :

* La documentation est à jour.
* Les exemples de documentation peuvent être exécutés tels quels.
* La plupart des fonctionnalités sont couvertes par la documentation, assurées par la couverture des tests.

Au cours du développement local, un script build le site et vérifie les changements éventuels, puis il est rechargé en direct :

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Il servira la documentation sur `http://127.0.0.1:8008`.

De cette façon, vous pouvez modifier la documentation/les fichiers sources et voir les changements en direct.

#### Typer CLI (facultatif)

Les instructions ici vous montrent comment utiliser le script à `./scripts/docs.py` avec le programme `python` directement.

Mais vous pouvez également utiliser <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, et vous obtiendrez l'auto-complétion dans votre terminal pour les commandes après l'achèvement de l'installation.

Si vous installez Typer CLI, vous pouvez installer la complétion avec :

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Apps et documentation en même temps

Si vous exécutez les exemples avec, par exemple :

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Comme Uvicorn utilisera par défaut le port `8000`, la documentation sur le port `8008` n'entrera pas en conflit.

### Traductions

L'aide aux traductions est TRÈS appréciée ! Et cela ne peut se faire sans l'aide de la communauté. 🌎 🚀

Voici les étapes à suivre pour aider à la traduction.

#### Conseils et lignes directrices

* Vérifiez les <a href="https://github.com/tiangolo/fastapi/pulls" class="external-link" target="_blank">pull requests existantes</a> pour votre langue et ajouter des reviews demandant des changements ou les approuvant.

!!! tip
    Vous pouvez <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">ajouter des commentaires avec des suggestions de changement</a> aux pull requests existantes.

    Consultez les documents concernant <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">l'ajout d'un review de pull request</a> pour l'approuver ou demander des modifications.

* Vérifiez dans <a href="https://github.com/tiangolo/fastapi/issues" class="external-link" target="_blank">issues</a> pour voir s'il y a une personne qui coordonne les traductions pour votre langue.

* Ajoutez une seule pull request par page traduite. Il sera ainsi beaucoup plus facile pour les autres de l'examiner.

Pour les langues que je ne parle pas, je vais attendre plusieurs autres reviews de la traduction avant de merge.

* Vous pouvez également vérifier s'il existe des traductions pour votre langue et y ajouter une review, ce qui m'aidera à savoir si la traduction est correcte et je pourrai la fusionner.

* Utilisez les mêmes exemples en Python et ne traduisez que le texte des documents. Vous n'avez pas besoin de changer quoi que ce soit pour que cela fonctionne.

* Utilisez les mêmes images, noms de fichiers et liens. Vous n'avez pas besoin de changer quoi que ce soit pour que cela fonctionne.

* Pour vérifier le code à 2 lettres de la langue que vous souhaitez traduire, vous pouvez utiliser le tableau <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">Liste des codes ISO 639-1</a>.

#### Langue existante

Disons que vous voulez traduire une page pour une langue qui a déjà des traductions pour certaines pages, comme l'espagnol.

Dans le cas de l'espagnol, le code à deux lettres est `es`. Ainsi, le répertoire des traductions espagnoles se trouve à l'adresse `docs/es/`.

!!! tip
    La langue principale ("officielle") est l'anglais, qui se trouve à l'adresse "docs/en/".

Maintenant, lancez le serveur en live pour les documents en espagnol :

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Vous pouvez maintenant aller sur <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> et voir vos changements en direct.

Si vous regardez le site web FastAPI docs, vous verrez que chaque langue a toutes les pages. Mais certaines pages ne sont pas traduites et sont accompagnées d'une notification concernant la traduction manquante.

Mais si vous le gérez localement de cette manière, vous ne verrez que les pages déjà traduites.

Disons maintenant que vous voulez ajouter une traduction pour la section [Features](features.md){.internal-link target=_blank}.

* Copiez le fichier à :

```
docs/en/docs/features.md
```

* Collez-le exactement au même endroit mais pour la langue que vous voulez traduire, par exemple :

```
docs/es/docs/features.md
```

!!! tip
    Notez que le seul changement dans le chemin et le nom du fichier est le code de langue, qui passe de `en` à `es`.

* Ouvrez maintenant le fichier de configuration de MkDocs pour l'anglais à

```
docs/en/docs/mkdocs.yml
```

* Trouvez l'endroit où cette `docs/features.md` se trouve dans le fichier de configuration. Quelque part comme :

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

* Ouvrez le fichier de configuration MkDocs pour la langue que vous éditez, par exemple :

```
docs/es/docs/mkdocs.yml
```

* Ajoutez-le à l'endroit exact où il se trouvait pour l'anglais, par exemple :

```YAML hl_lines="8"
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

Assurez-vous que s'il y a d'autres entrées, la nouvelle entrée avec votre traduction est exactement dans le même ordre que dans la version anglaise.

Si vous allez sur votre navigateur, vous verrez que maintenant les documents montrent votre nouvelle section. 🎉

Vous pouvez maintenant tout traduire et voir à quoi cela ressemble au fur et à mesure que vous enregistrez le fichier.

#### Nouvelle langue

Disons que vous voulez ajouter des traductions pour une langue qui n'est pas encore traduite, pas même quelques pages.

Disons que vous voulez ajouter des traductions pour le Créole, et que ce n'est pas encore dans les documents.

En vérifiant le lien ci-dessus, le code pour "Créole" est `ht`.

L'étape suivante consiste à exécuter le script pour générer un nouveau répertoire de traduction :

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
Updating ht
Updating en
```

</div>

Vous pouvez maintenant vérifier dans votre éditeur de code le répertoire nouvellement créé `docs/ht/`.

!!! tip
    Créez une première demande d'extraction à l'aide de cette fonction, afin de configurer la nouvelle langue avant d'ajouter des traductions.

    Ainsi, d'autres personnes peuvent vous aider à rédiger d'autres pages pendant que vous travaillez sur la première. 🚀

Commencez par traduire la page principale, `docs/ht/index.md`.

Vous pouvez ensuite continuer avec les instructions précédentes, pour une "langue existante".

##### Nouvelle langue non prise en charge

Si, lors de l'exécution du script du serveur en direct, vous obtenez une erreur indiquant que la langue n'est pas prise en charge, quelque chose comme :

```
 raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: partials/language/xx.html
```

Cela signifie que le thème ne supporte pas cette langue (dans ce cas, avec un faux code de 2 lettres de `xx`).

Mais ne vous inquiétez pas, vous pouvez définir la langue du thème en anglais et ensuite traduire le contenu des documents.

Si vous avez besoin de faire cela, modifiez le fichier `mkdocs.yml` pour votre nouvelle langue, il aura quelque chose comme :

```YAML hl_lines="5"
site_name: FastAPI
# More stuff
theme:
  # More stuff
  language: xx
```

Changez cette langue de `xx` (de votre code de langue) à `fr`.

Vous pouvez ensuite relancer le serveur live.

#### Prévisualisez le résultat

Lorsque vous utilisez le script à `./scripts/docs.py` avec la commande `live`, il n'affiche que les fichiers et les traductions disponibles pour la langue courante.

Mais une fois que vous avez terminé, vous pouvez tester le tout comme il le ferait en ligne.

Pour ce faire, il faut d'abord construire tous les documents :

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Updating es
Updating en
Building docs for: en
Building docs for: es
Successfully built docs for: es
Copying en index.md to README.md
```

</div>

Cela génère tous les documents à `./docs_build/` pour chaque langue. Cela inclut l'ajout de tout fichier dont la traduction est manquante, avec une note disant que "ce fichier n'a pas encore de traduction". Mais vous n'avez rien à faire avec ce répertoire.

Ensuite, il construit tous ces sites MkDocs indépendants pour chaque langue, les combine, et génère le résultat final à `./site/`.

Ensuite, vous pouvez servir cela avec le commandement `serve`:

<div class="termy">

```console
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

## Tests

Il existe un script que vous pouvez exécuter localement pour tester tout le code et générer des rapports de couverture en HTML :

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Cette commande génère un répertoire `./htmlcov/`, si vous ouvrez le fichier `./htmlcov/index.html` dans votre navigateur, vous pouvez explorer interactivement les régions de code qui sont couvertes par les tests, et remarquer s'il y a une région manquante.
