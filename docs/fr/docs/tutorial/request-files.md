# Envoyer des fichiers { #request-files }

Vous pouvez définir des fichiers à téléverser par le client en utilisant `File`.

/// info

Pour recevoir des fichiers téléversés, installez d'abord <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Assurez-vous de créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, de l'activer, puis d'installer le paquet, par exemple :

```console
$ pip install python-multipart
```

C'est parce que les fichiers téléversés sont envoyés en « données de formulaire ».

///

## Importer `File` { #import-file }

Importez `File` et `UploadFile` depuis `fastapi` :

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## Définir des paramètres `File` { #define-file-parameters }

Créez des paramètres de fichier de la même manière que pour `Body` ou `Form` :

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info

`File` est une classe qui hérite directement de `Form`.

Mais souvenez-vous que lorsque vous importez `Query`, `Path`, `File` et d'autres depuis `fastapi`, ce sont en réalité des fonctions qui renvoient des classes spéciales.

///

/// tip | Astuce

Pour déclarer des fichiers dans le corps de la requête, vous devez utiliser `File`, sinon les paramètres seraient interprétés comme des paramètres de requête ou des paramètres de corps (JSON).

///

Les fichiers seront téléversés en « données de formulaire ».

Si vous déclarez le type de votre paramètre de *fonction de chemin d'accès* comme `bytes`, **FastAPI** lira le fichier pour vous et vous recevrez le contenu sous forme de `bytes`.

Gardez à l'esprit que cela signifie que tout le contenu sera stocké en mémoire. Cela fonctionnera bien pour de petits fichiers.

Mais dans plusieurs cas, vous pourriez bénéficier de l'utilisation d'`UploadFile`.

## Paramètres de fichier avec `UploadFile` { #file-parameters-with-uploadfile }

Définissez un paramètre de fichier de type `UploadFile` :

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

Utiliser `UploadFile` présente plusieurs avantages par rapport à `bytes` :

- Vous n'avez pas besoin d'utiliser `File()` comme valeur par défaut du paramètre.
- Il utilise un fichier « spooled » :
    - Un fichier stocké en mémoire jusqu'à une taille maximale, puis, au-delà de cette limite, stocké sur le disque.
- Cela fonctionne donc bien pour des fichiers volumineux comme des images, des vidéos, de gros binaires, etc., sans consommer toute la mémoire.
- Vous pouvez obtenir des métadonnées à partir du fichier téléversé.
- Il offre une interface `async` de type <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a>.
- Il expose un véritable objet Python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> que vous pouvez passer directement à d'autres bibliothèques qui attendent un objet « file-like ».

### `UploadFile` { #uploadfile }

`UploadFile` a les attributs suivants :

- `filename` : une `str` contenant le nom de fichier original téléversé (par ex. `myimage.jpg`).
- `content_type` : une `str` avec le type de contenu (type MIME / type média) (par ex. `image/jpeg`).
- `file` : un <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (un objet <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">de type fichier</a>). C'est l'objet fichier Python réel que vous pouvez passer directement à d'autres fonctions ou bibliothèques qui attendent un objet « file-like ».

`UploadFile` a les méthodes `async` suivantes. Elles appellent toutes les méthodes correspondantes du fichier sous-jacent (en utilisant le `SpooledTemporaryFile` interne).

- `write(data)` : écrit `data` (`str` ou `bytes`) dans le fichier.
- `read(size)` : lit `size` (`int`) octets/caractères du fichier.
- `seek(offset)` : se déplace à la position d'octet `offset` (`int`) dans le fichier.
    - Par ex., `await myfile.seek(0)` irait au début du fichier.
    - C'est particulièrement utile si vous exécutez `await myfile.read()` une fois puis devez relire le contenu.
- `close()` : ferme le fichier.

Comme toutes ces méthodes sont `async`, vous devez les « await ».

Par exemple, à l'intérieur d'une *fonction de chemin d'accès* `async`, vous pouvez obtenir le contenu avec :

```Python
contents = await myfile.read()
```

Si vous êtes dans une *fonction de chemin d'accès* `def` normale, vous pouvez accéder directement à `UploadFile.file`, par exemple :

```Python
contents = myfile.file.read()
```

/// note | Détails techniques `async`

Lorsque vous utilisez les méthodes `async`, **FastAPI** exécute les méthodes de fichier dans un pool de threads et les attend.

///

/// note | Détails techniques Starlette

L'`UploadFile` de **FastAPI** hérite directement de l'`UploadFile` de **Starlette**, mais ajoute certaines parties nécessaires pour le rendre compatible avec **Pydantic** et les autres parties de FastAPI.

///

## Qu'est-ce que les « données de formulaire » { #what-is-form-data }

La façon dont les formulaires HTML (`<form></form>`) envoient les données au serveur utilise normalement un encodage « spécial » pour ces données, différent de JSON.

**FastAPI** s'assure de lire ces données au bon endroit plutôt que depuis JSON.

/// note | Détails techniques

Les données des formulaires sont normalement encodées avec le « type de média » `application/x-www-form-urlencoded` lorsqu'elles n'incluent pas de fichiers.

Mais lorsque le formulaire inclut des fichiers, il est encodé en `multipart/form-data`. Si vous utilisez `File`, **FastAPI** saura qu'il doit récupérer les fichiers depuis la partie appropriée du corps.

Si vous souhaitez en savoir plus sur ces encodages et les champs de formulaire, consultez la <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Réseau des développeurs Mozilla">MDN</abbr> Web Docs pour <code>POST</code></a>.

///

/// warning | Alertes

Vous pouvez déclarer plusieurs paramètres `File` et `Form` dans un *chemin d'accès*, mais vous ne pouvez pas également déclarer des champs `Body` que vous vous attendez à recevoir en JSON, car la requête aura le corps encodé en `multipart/form-data` au lieu de `application/json`.

Ce n'est pas une limitation de **FastAPI**, cela fait partie du protocole HTTP.

///

## Téléversement de fichier facultatif { #optional-file-upload }

Vous pouvez rendre un fichier facultatif en utilisant des annotations de type standard et en définissant une valeur par défaut à `None` :

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## `UploadFile` avec des métadonnées supplémentaires { #uploadfile-with-additional-metadata }

Vous pouvez aussi utiliser `File()` avec `UploadFile`, par exemple pour définir des métadonnées supplémentaires :

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## Téléverser plusieurs fichiers { #multiple-file-uploads }

Il est possible de téléverser plusieurs fichiers en même temps.

Ils seraient associés au même « champ de formulaire » envoyé en « données de formulaire ».

Pour cela, déclarez une `list` de `bytes` ou d'`UploadFile` :

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

Vous recevrez, comme déclaré, une `list` de `bytes` ou d'`UploadFile`.

/// note | Détails techniques

Vous pourriez aussi utiliser `from starlette.responses import HTMLResponse`.

**FastAPI** fournit les mêmes `starlette.responses` sous `fastapi.responses` simplement pour votre convenance en tant que développeur. Mais la plupart des réponses disponibles proviennent directement de Starlette.

///

### Téléversements multiples avec métadonnées supplémentaires { #multiple-file-uploads-with-additional-metadata }

Et de la même manière que précédemment, vous pouvez utiliser `File()` pour définir des paramètres supplémentaires, même pour `UploadFile` :

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## Récapitulatif { #recap }

Utilisez `File`, `bytes` et `UploadFile` pour déclarer des fichiers à téléverser dans la requête, envoyés en « données de formulaire ».
