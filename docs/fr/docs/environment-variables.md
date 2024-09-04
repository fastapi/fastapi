# Variables d'environnement

/// tip

Si vous savez déjà ce que sont les "variables d'environnement" et comment les utiliser, vous pouvez passer cette partie.

///

Une variable d'environnement (aussi appelée "**env var**") est une variable qui existe **en dehors** du code Python, au niveau du **système d'exploitation**, et qui peut être lue par votre code Python (ainsi que par d'autres programmes).

Les variables d'environnement sont utiles pour gérer les **paramètres** de l'application, dans le cadre de **l'installation** de Python, etc.

## Créer et utiliser les variables d'environnements

Il est possible de créer et d'utiliser les variables d'environnement dans un **shell (terminal)**, sans avoir à utiliser Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Vous pouvez créer une variable d'environnement MY_NAME avec
$ export MY_NAME="Wade Wilson"

// Puis vous pouvez l'utiliser dans d'autre programmes, comme
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Créez une variable d'environnement MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Utilisez-la dans d'autres programmes, comme
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Lire les variables d'environnement en Python

Vous avez aussi la possibilité de créer une variable d'environnement **en dehors** de Python, dans le terminal (ou avec n'importe quelle autre méthode), puis la **lire en Python**. 

Par exemple, vous pouvez avoir un fichier `main.py` avec:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

Le second argument de <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> est la valeur par défaut à retourner.

Si elle n'est pas fournie, ce sera `None` par defaut. Ici, on passe `"World"` comme valeur par défaut à utiliser.

///

Vous pouvez ensuite appeler ce programme Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Ici la variable d'environnement n'est pas encore fixée
$ python main.py

// Comme nous n'avons pas fixé la variable d'environnement, nous obtenons la valeur par défaut

Hello World from Python

// Mais si nous créons d'abord une variable d'environnement
$ export MY_NAME="Wade Wilson"

// Puis que l'on rappelle le programme
$ python main.py

// Maintenant il peut lire la variable d'environnement

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Ici la variable d'environnement n'est pas encore fixée
$ python main.py

// Comme nous n'avons pas fixé la variable d'environnement, nous obtenons la valeur par défaut

Hello World from Python

// Mais si nous créons d'abord une variable d'environnement
$ $Env:MY_NAME = "Wade Wilson"

// Puis que l'on rappelle le programme
$ python main.py

// Maintenant il peut lire la variable d'environnement

Hello Wade Wilson from Python
```

</div>

////

Comme les variables d'environnement peuvent être fixées à l'extérieur du code, mais peuvent être lues par le code, et n'ont pas à être stockées (commitées sur `git`) avec les autres fichiers, il est commun de les utiliser pour les configurations ou les **paramètres**.

Vous pouvez aussi créer une variable d'environnement pour **l'invocation d'un programme spécifique**. Elle ne sera utilisable que pour ce programme, et seulement pour sa durée d'exécution.

Pour ce faire, créez-la en amont du programme lui-même, sur la même ligne:

<div class="termy">

```console
// Créez une variable d'environnement MY_NAME sur la même ligne que l'appel du programme
$ MY_NAME="Wade Wilson" python main.py

// Maintenant il peut lire cette variable d'environnement

Hello Wade Wilson from Python

// La variable d'environnement n'existe plus ensuite
$ python main.py

Hello World from Python
```

</div>

/// tip

Pour en savoir plus, consultez <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Types et Validation

Ces variables d'environnement ne peuvent que traiter des **chaînes de texte**, car elles sont externes à Python et doivent être compatibles avec d'autres programmes et le reste du système (voire même avec différents systèmes d'exploitations, comme Linux, Windows, macOS).

Cela signifie que **chaque valeur** lue en Python d'une variable d'environnement **sera un `str`**, et toute conversion vers un type différent ou toute validation doit être faite dans le code.

Le [Guide de l'utilisateur avancé - Paramètres et Variables d'environnement](./advanced/settings.md){.internal-link target=_blank} vous permettra d'en savoir plus sur les variables d'environnement pour gérer les paramètres de l'application.


## La variable d'environnement `PATH`

Il existe une variable d'environnement **spéciale** appelée **`PATH`** utilisée par les systèmes d'exploitation (Linux, macOS, Windows) pour trouver les programmes à exécuter.

La valeur de la variable `PATH` est une longue chaîne de caractères, composée de répertoires séparés par un `:` sur Linux et macOS, et par un point-virgule `;` sur Windows.

Par exemple, la variable d'environnement `PATH` peut se présenter de la manière suivante:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Cela signifie que le système doit rechercher des programmes dans les répertoires:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Cela signifie que le système doit rechercher des programmes dans les répertoires:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Lorsque vous tapez une **commande** dans le terminal, le système d'exploitation **recherche** le programme dans **chaque répertoire** répertorié dans la variable d'environnement `PATH`.

Par exemple, si vous tapez `python` dans le terminal, le système d'exploitation recherche un programme nommé `python` dans le **premier répertoire** de cette liste.

S'il le trouve, alors il **l'utilisera**. Autrement, il continue de chercher dans les **autres répertoires**.

### Installer Python and modifier the `PATH`

Lorsque vous installez Python, il peut vous être demandé de modifier la variable d'environnement `PATH`.

//// tab | Linux, macOS

Disons que vous installez Python, et qu'il finisse dans le répertoire `/opt/custompython/bin`.

Si vous acceptez de mettre à jour la variable d'environnement `PATH`, l'installateur inclura alors `/opt/custompython/bin` à la variable d'environnement `PATH`.

Ce qui pourrait donner:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

En tapant `python` dans le terminal, le système trouvera le programme Python dans `/opt/custompython/bin` (le dernier répertoire) et utilisera celui-ci.

////

//// tab | Windows

Disons que vous installez Python, et il finis dans le répertoire `C:\opt\custompython\bin`.

Si vous acceptez de mettre à jour la variable d'environnement `PATH`, l'installateur inclura alors `C:\opt\custompython\bin` à la variable d'environnement `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

En tapant `python` dans le terminal, le système trouvera le programme Python dans `/opt/custompython/bin` (le dernier répertoire) et utilisera celui-ci.

////


Donc, si vous tapez:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Le système **trouvera** le programme `python` dans `/opt/custompython/bin` et le lancera.

Ce serait à peu près équivalent à taper:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Le système **trouvera** le programme `python` dans `C:\opt\custompython\bin` et le lancera.

Ce serait à peut près équivalent à taper:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Cette information vous sera utile, quand vous apprendrez les [Environnements virtuels](virtual-environments.md){.internal-link target=_blank}.

## Conclusion

Maintenant, vous devriez avoir une compréhension basique des variables d'environnement, et leurs utilisation en Python.

Vous pouvez aussi en apprendre plus sur elles sur <a href="https://fr.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia pour les variables d'environnements</a>.

Il sera difficile de comprendre rapidement leurs utilités et leurs applications dans de nombreux cas.  Cependant, elles se manifesteront dans divers scénarios lorsque vous développerez, il est donc bénéfique de les connaître.

Par exemple, vous aurez besoin de cette information dans la section suivante, sur les [Environnements Virtuels](virtual-environments.md).
