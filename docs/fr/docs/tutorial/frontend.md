# Frontend { #frontend }

Vous pouvez servir des applications frontend statiques avec `app.frontend()` (ou `router.frontend()`).

C'est utile pour les outils frontend qui génèrent des fichiers statiques, comme React avec Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid, et d'autres.

Avec ces outils, vous avez normalement une étape qui build le frontend, avec une commande comme :

```bash
npm run build
```

Cela générerait un répertoire comme `./dist/` avec vos fichiers frontend.

Vous pouvez utiliser `app.frontend()` pour servir ce répertoire en suivant les conventions nécessaires à ces frameworks frontend.

**FastAPI** vérifie d'abord les *chemins d'accès*. Les fichiers frontend ne sont vérifiés que si aucune route normale ne correspond, donc votre API ne sera pas affectée.

## Servir un frontend { #serve-a-frontend }

Après avoir build votre frontend, par exemple avec `npm run build`, placez les fichiers générés dans un répertoire, par exemple `dist`.

La structure de votre projet pourrait ressembler à ceci :

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

Servez-le ensuite avec `app.frontend()` :

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

Avec cela, une requête vers `/assets/app.js` peut servir `dist/assets/app.js`.

Si vous avez également un *chemin d'accès* **FastAPI**, le *chemin d'accès* est prioritaire.

## Routage côté client { #client-side-routing }

De nombreuses applications frontend, y compris les **applications monopages** (SPAs), utilisent le routage côté client. Un chemin comme `/dashboard/settings` peut ne pas être un vrai fichier, mais le framework se chargerait de le gérer.

Ainsi, si vous accédez directement à cette URL (au lieu de naviguer via l'application), le backend doit servir l'application frontend depuis `index.html`, afin que le framework frontend puisse ensuite gérer le routage côté client.

Pour cela, utilisez `fallback="index.html"` :

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** utilise ce fallback uniquement pour les requêtes `GET` et `HEAD` qui ressemblent à une navigation de navigateur. Les fichiers manquants comme JavaScript, CSS et les images renvoient toujours `404`.

Les requêtes avec d'autres méthodes, comme `POST` ou `PUT`, vers des chemins qui ne correspondent qu'au fallback frontend renvoient également `404`. Les *chemins d'accès* **FastAPI** réguliers ont toujours une priorité plus élevée que les routes frontend.

/// tip | Astuce

Par défaut, `fallback` a une valeur de `fallback="auto"`. Dans la plupart des cas, vous n'avez pas besoin de spécifier `fallback`. Lisez ci-dessous pour plus de détails.

///

C'est ce que vous souhaitez avec de nombreuses applications frontend qui utilisent le routage côté client, par exemple React avec TanStack Router, Vue, Angular, SvelteKit ou Solid.

## Page 404 personnalisée { #custom-404-page }

Vous pouvez également servir une page statique `404.html` pour les chemins frontend manquants :

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Cette réponse conserve un code de statut `404`.

Dans ce cas, **FastAPI** ne servira pas `index.html` pour les chemins frontend manquants. Il renverra le fichier `404.html` à la place.

/// tip | Astuce

Par défaut, `fallback` a une valeur de `fallback="auto"`. Avec cela, si un fichier `404.html` est trouvé, il sera utilisé automatiquement comme fallback.

Vous pouvez donc normalement omettre l'argument `fallback`.

///

C'est utile avec les outils frontend qui génèrent des fichiers HTML statiques pour chaque page, comme Astro.

## Fallback automatique { #fallback-auto }

Par défaut, `app.frontend()` utilise `fallback="auto"`.

S'il y a un fichier `404.html` dans le répertoire frontend, les chemins frontend manquants servent ce fichier avec le code de statut `404`.

Sinon, s'il y a un fichier `index.html`, les chemins de navigation de navigateur manquants servent `index.html`, ce qui est attendu par de nombreuses applications frontend avec routage côté client.

Ainsi, dans la plupart des cas, vous pouvez utiliser `app.frontend("/", directory="dist")` sans spécifier l'argument `fallback`.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Désactiver le fallback { #disable-fallback }

Si vous ne souhaitez pas servir de fichier fallback pour les chemins frontend manquants, utilisez `fallback=None` :

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Les chemins frontend manquants renvoient alors le `404` normal.

## Vérifier le répertoire { #check-directory }

Par défaut, `app.frontend()` vérifie que le répertoire existe lorsque l'application est créée.

Cela permet de détecter tôt les erreurs de configuration. Par exemple, si le répertoire de sortie du build frontend est manquant, **FastAPI** lèvera une erreur au démarrage.

Si vos fichiers frontend sont créés plus tard, par exemple par une étape de build séparée après la création de l'objet app, définissez `check_dir=False` :

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

Avec `check_dir=False`, **FastAPI** ne vérifiera pas le répertoire lorsque l'application est créée. Si le répertoire configuré est toujours manquant lorsqu'une requête est traitée, **FastAPI** lèvera alors une erreur.

## L'utiliser avec `APIRouter` { #use-it-with-apirouter }

Vous pouvez également ajouter des fichiers frontend à un `APIRouter` et l'inclure avec un préfixe :

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

Dans cet exemple, les chemins frontend sont servis sous `/app`.

Tous les *chemins d'accès* réguliers dans l'application seront toujours prioritaires, y compris dans d'autres routers.

## Sortie de build statique uniquement { #static-build-output-only }

`app.frontend()` sert des fichiers déjà générés par votre build frontend.

Il n'exécute pas de rendu côté serveur. Il est destiné aux frameworks frontend qui génèrent des fichiers statiques, pas aux frameworks qui nécessitent un rendu dynamique sur le serveur pour chaque requête.
