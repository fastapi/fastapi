# <abbr title="En anglais: Debugging">Débogage</abbr>

Vous pouvez connecter le <abbr title="En anglais: debugger">débogueur</abbr> dans votre éditeur, par exemple avec Visual Studio Code ou PyCharm.

## Faites appel à `uvicorn`

Dans votre application FastAPI, importez et exécutez directement `uvicorn` :

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### À propos de `__name__ == "__main__"`

Le but principal de `__name__ == "__main__"` est d'avoir du code qui est exécuté lorsque votre fichier est appelé avec :

<div class="termy">

```console
$ python myapp.py
```

</div>

mais qui n'est pas appelé lorsqu'un autre fichier l'importe, comme dans :

```Python
from myapp import app
```

#### Pour davantage de détails

Imaginons que votre fichier s'appelle `myapp.py`.

Si vous l'exécutez avec :

<div class="termy">

```console
$ python myapp.py
```

</div>

alors la variable interne `__name__` de votre fichier, créée automatiquement par Python, aura pour valeur la chaîne de caractères `"__main__"`.

Ainsi, la section :

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

va s'exécuter.

---

Cela ne se produira pas si vous importez ce module (fichier).

Par exemple, si vous avez un autre fichier `importer.py` qui contient :

```Python
from myapp import app

# Code supplémentaire
```

dans ce cas, la variable automatique `__name__` à l'intérieur de `myapp.py` n'aura pas la valeur `"__main__"`.

Ainsi, la ligne :

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

ne sera pas exécutée.

/// info

Pour plus d'informations, consultez <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">la documentation officielle de Python</a>.

///

## Exécutez votre code avec votre <abbr title="En anglais: debugger">débogueur</abbr>

Parce que vous exécutez le serveur Uvicorn directement depuis votre code, vous pouvez appeler votre programme Python (votre application FastAPI) directement depuis le <abbr title="En anglais: debugger">débogueur</abbr>.

---

Par exemple, dans Visual Studio Code, vous pouvez :

- Cliquer sur l'onglet "Debug" de la barre d'activités de Visual Studio Code.
- "Add configuration...".
- Sélectionnez "Python".
- Lancez le <abbr title="En anglais: debugger">débogueur</abbr> avec l'option "`Python: Current File (Integrated Terminal)`".

Il démarrera alors le serveur avec votre code **FastAPI**, s'arrêtera à vos points d'arrêt, etc.

Voici à quoi cela pourrait ressembler :

<img src="/img/tutorial/debugging/image01.png">

---

Si vous utilisez Pycharm, vous pouvez :

- Ouvrir le menu "Run".
- Sélectionnez l'option "Debug...".
- Un menu contextuel s'affiche alors.
- Sélectionnez le fichier à déboguer (dans ce cas, `main.py`).

Il démarrera alors le serveur avec votre code **FastAPI**, s'arrêtera à vos points d'arrêt, etc.

Voici à quoi cela pourrait ressembler :

<img src="/img/tutorial/debugging/image02.png">
