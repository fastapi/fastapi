# Variables d'environnement { #environment-variables }

/// tip | Astuce

Si vous savez déjà ce que sont les « variables d'environnement » et comment les utiliser, vous pouvez passer cette section.

///

Une variable d'environnement (également appelée « env var ») est une variable qui vit en dehors du code Python, dans le système d'exploitation, et qui peut être lue par votre code Python (ou par d'autres programmes également).

Les variables d'environnement peuvent être utiles pour gérer des **paramètres** d'application, dans le cadre de l'**installation** de Python, etc.

## Créer et utiliser des variables d'environnement { #create-and-use-env-vars }

Vous pouvez créer et utiliser des variables d'environnement dans le **shell (terminal)**, sans avoir besoin de Python :

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Vous pouvez créer une variable d'environnement MY_NAME avec
$ export MY_NAME="Wade Wilson"

// Vous pouvez ensuite l'utiliser avec d'autres programmes, par exemple
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Créer une variable d'environnement MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// L'utiliser avec d'autres programmes, par exemple
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Lire des variables d'environnement en Python { #read-env-vars-in-python }

Vous pouvez également créer des variables d'environnement **en dehors** de Python, dans le terminal (ou par tout autre moyen), puis les **lire en Python**.

Par exemple, vous pouvez avoir un fichier `main.py` contenant :

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Astuce

Le deuxième argument de <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> est la valeur par défaut à retourner.

S'il n'est pas fourni, c'est `None` par défaut ; ici, nous fournissons `"World"` comme valeur par défaut à utiliser.

///

Vous pouvez ensuite exécuter ce programme Python :

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Ici, nous ne définissons pas encore la variable d'environnement
$ python main.py

// Comme nous ne l'avons pas définie, nous obtenons la valeur par défaut

Hello World from Python

// Mais si nous créons d'abord une variable d'environnement
$ export MY_NAME="Wade Wilson"

// Puis que nous relançons le programme
$ python main.py

// Il peut maintenant lire la variable d'environnement

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Ici, nous ne définissons pas encore la variable d'environnement
$ python main.py

// Comme nous ne l'avons pas définie, nous obtenons la valeur par défaut

Hello World from Python

// Mais si nous créons d'abord une variable d'environnement
$ $Env:MY_NAME = "Wade Wilson"

// Puis que nous relançons le programme
$ python main.py

// Il peut maintenant lire la variable d'environnement

Hello Wade Wilson from Python
```

</div>

////

Comme les variables d'environnement peuvent être définies en dehors du code, mais lues par le code, et qu'elles n'ont pas besoin d'être stockées (validées dans `git`) avec le reste des fichiers, il est courant de les utiliser pour les configurations ou les **paramètres**.

Vous pouvez également créer une variable d'environnement uniquement pour l'**invocation d'un programme spécifique**, qui ne sera disponible que pour ce programme et uniquement pendant sa durée d'exécution.

Pour cela, créez-la juste avant le programme, sur la même ligne :

<div class="termy">

```console
// Créer en ligne une variable d'environnement MY_NAME pour cet appel de programme
$ MY_NAME="Wade Wilson" python main.py

// Il peut maintenant lire la variable d'environnement

Hello Wade Wilson from Python

// La variable d'environnement n'existe plus ensuite
$ python main.py

Hello World from Python
```

</div>

/// tip | Astuce

Vous pouvez en lire davantage sur <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App : Config</a>.

///

## Gérer les types et la validation { #types-and-validation }

Ces variables d'environnement ne peuvent gérer que des **chaînes de texte**, car elles sont externes à Python et doivent être compatibles avec les autres programmes et le reste du système (et même avec différents systèmes d'exploitation, comme Linux, Windows, macOS).

Cela signifie que **toute valeur** lue en Python à partir d'une variable d'environnement **sera une `str`**, et que toute conversion vers un autre type ou toute validation doit être effectuée dans le code.

Vous en apprendrez davantage sur l'utilisation des variables d'environnement pour gérer les **paramètres d'application** dans le [Guide utilisateur avancé - Paramètres et variables d'environnement](./advanced/settings.md){.internal-link target=_blank}.

## Variable d'environnement `PATH` { #path-environment-variable }

Il existe une **variable d'environnement spéciale** appelée **`PATH`** qui est utilisée par les systèmes d'exploitation (Linux, macOS, Windows) pour trouver les programmes à exécuter.

La valeur de la variable `PATH` est une longue chaîne composée de répertoires séparés par deux-points `:` sous Linux et macOS, et par point-virgule `;` sous Windows.

Par exemple, la variable d'environnement `PATH` peut ressembler à ceci :

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Cela signifie que le système doit rechercher les programmes dans les répertoires :

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

Cela signifie que le système doit rechercher les programmes dans les répertoires :

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Lorsque vous tapez une **commande** dans le terminal, le système d'exploitation **cherche** le programme dans **chacun de ces répertoires** listés dans la variable d'environnement `PATH`.

Par exemple, lorsque vous tapez `python` dans le terminal, le système d'exploitation cherche un programme nommé `python` dans le **premier répertoire** de cette liste.

S'il le trouve, alors il **l'utilise**. Sinon, il continue à chercher dans les **autres répertoires**.

### Installer Python et mettre à jour `PATH` { #installing-python-and-updating-the-path }

Lorsque vous installez Python, il est possible que l'on vous demande si vous souhaitez mettre à jour la variable d'environnement `PATH`.

//// tab | Linux, macOS

Supposons que vous installiez Python et qu'il se retrouve dans un répertoire `/opt/custompython/bin`.

Si vous acceptez de mettre à jour la variable d'environnement `PATH`, l'installateur ajoutera `/opt/custompython/bin` à la variable d'environnement `PATH`.

Cela pourrait ressembler à ceci :

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Ainsi, lorsque vous tapez `python` dans le terminal, le système trouvera le programme Python dans `/opt/custompython/bin` (le dernier répertoire) et utilisera celui-là.

////

//// tab | Windows

Supposons que vous installiez Python et qu'il se retrouve dans un répertoire `C:\opt\custompython\bin`.

Si vous acceptez de mettre à jour la variable d'environnement `PATH`, l'installateur ajoutera `C:\opt\custompython\bin` à la variable d'environnement `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Ainsi, lorsque vous tapez `python` dans le terminal, le système trouvera le programme Python dans `C:\opt\custompython\bin` (le dernier répertoire) et utilisera celui-là.

////

Ainsi, si vous tapez :

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Le système va **trouver** le programme `python` dans `/opt/custompython/bin` et l'exécuter.

Cela reviendrait à peu près à taper :

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Le système va **trouver** le programme `python` dans `C:\opt\custompython\bin\python` et l'exécuter.

Cela reviendrait à peu près à taper :

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Ces informations vous seront utiles lors de l'apprentissage des [Environnements virtuels](virtual-environments.md){.internal-link target=_blank}.

## Conclusion { #conclusion }

Avec cela, vous devriez avoir une compréhension de base de ce que sont les **variables d'environnement** et de la façon de les utiliser en Python.

Vous pouvez également en lire davantage sur la <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">page Wikipédia dédiée aux variables d'environnement</a>.

Dans de nombreux cas, il n'est pas évident de voir immédiatement en quoi les variables d'environnement seraient utiles et applicables. Mais elles réapparaissent dans de nombreux scénarios lorsque vous développez, il est donc bon de les connaître.

Par exemple, vous aurez besoin de ces informations dans la section suivante, sur les [Environnements virtuels](virtual-environments.md).
