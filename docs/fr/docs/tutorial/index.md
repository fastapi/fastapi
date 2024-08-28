# Tutoriel - Guide utilisateur - Introduction

Ce tutoriel vous montre comment utiliser **FastAPI** avec la plupart de ses fonctionnalités, étape par étape.

Chaque section s'appuie progressivement sur les précédentes, mais elle est structurée de manière à séparer les sujets, afin que vous puissiez aller directement à l'un d'entre eux pour résoudre vos besoins spécifiques en matière d'API.

Il est également conçu pour fonctionner comme une référence future.

Vous pouvez donc revenir et voir exactement ce dont vous avez besoin.

## Exécuter le code

Tous les blocs de code peuvent être copiés et utilisés directement (il s'agit en fait de fichiers Python testés).

Pour exécuter l'un de ces exemples, copiez le code dans un fichier `main.py`, et commencez `uvicorn` avec :

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

Il est **FORTEMENT encouragé** que vous écriviez ou copiez le code, l'éditiez et l'exécutiez localement.

L'utiliser dans votre éditeur est ce qui vous montre vraiment les avantages de FastAPI, en voyant le peu de code que vous avez à écrire, toutes les vérifications de type, l'autocomplétion, etc.

---

## Installer FastAPI

La première étape consiste à installer FastAPI.

Pour le tutoriel, vous voudrez peut-être l'installer avec toutes les dépendances et fonctionnalités optionnelles :

<div class="termy">

```console
$ pip install fastapi[all]

---> 100%
```

</div>

... qui comprend également `uvicorn`, que vous pouvez utiliser comme serveur pour exécuter votre code.

/// note

Vous pouvez également l'installer pièce par pièce.

C'est ce que vous feriez probablement une fois que vous voudrez déployer votre application en production :

```
pip install fastapi
```

Installez également `uvicorn` pour qu'il fonctionne comme serveur :

```
pip install uvicorn
```

Et la même chose pour chacune des dépendances facultatives que vous voulez utiliser.

///

## Guide utilisateur avancé

Il existe également un **Guide d'utilisation avancé** que vous pouvez lire plus tard après ce **Tutoriel - Guide d'utilisation**.

Le **Guide d'utilisation avancé**, qui s'appuie sur cette base, utilise les mêmes concepts et vous apprend quelques fonctionnalités supplémentaires.

Mais vous devez d'abord lire le **Tutoriel - Guide d'utilisation** (ce que vous êtes en train de lire en ce moment).

Il est conçu pour que vous puissiez construire une application complète avec seulement le **Tutoriel - Guide d'utilisation**, puis l'étendre de différentes manières, en fonction de vos besoins, en utilisant certaines des idées supplémentaires du **Guide d'utilisation avancé**.
