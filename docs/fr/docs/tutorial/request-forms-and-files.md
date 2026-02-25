# Utiliser des formulaires et des fichiers de requête { #request-forms-and-files }

Vous pouvez définir des fichiers et des champs de formulaire en même temps à l'aide de `File` et `Form`.

/// info

Pour recevoir des fichiers téléversés et/ou des données de formulaire, installez d'abord <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Vous devez créer un [environnement virtuel](../virtual-environments.md){.internal-link target=_blank}, l'activer, puis installer ce paquet, par exemple :

```console
$ pip install python-multipart
```

///

## Importer `File` et `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## Définir des paramètres `File` et `Form` { #define-file-and-form-parameters }

Créez des paramètres de fichier et de formulaire de la même manière que pour `Body` ou `Query` :

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

Les fichiers et les champs de formulaire seront téléversés en tant que données de formulaire et vous les recevrez.

Et vous pouvez déclarer certains fichiers comme `bytes` et d'autres comme `UploadFile`.

/// warning | Alertes

Vous pouvez déclarer plusieurs paramètres `File` et `Form` dans un *chemin d'accès*, mais vous ne pouvez pas aussi déclarer des champs `Body` que vous vous attendez à recevoir en JSON, car la requête aura le corps encodé en `multipart/form-data` au lieu de `application/json`.

Ce n'est pas une limitation de **FastAPI**, cela fait partie du protocole HTTP.

///

## Récapitulatif { #recap }

Utilisez `File` et `Form` ensemble lorsque vous devez recevoir des données et des fichiers dans la même requête.
