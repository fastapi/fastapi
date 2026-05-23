# Prise en charge des éditeurs { #editor-support }

L’extension officielle [Extension FastAPI](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) améliore votre flux de développement FastAPI grâce à la découverte des chemins d'accès, à la navigation, ainsi qu’au déploiement sur FastAPI Cloud et à la diffusion en direct des journaux.

Pour plus de détails sur l’extension, reportez-vous au README sur le [référentiel GitHub](https://github.com/fastapi/fastapi-vscode).

## Configurer et installer { #setup-and-installation }

L’**Extension FastAPI** est disponible pour [VS Code](https://code.visualstudio.com/) et [Cursor](https://www.cursor.com/). Vous pouvez l’installer directement depuis le panneau Extensions de chaque éditeur en recherchant « FastAPI » et en sélectionnant l’extension publiée par **FastAPI Labs**. L’extension fonctionne également dans les éditeurs basés sur le navigateur tels que [vscode.dev](https://vscode.dev) et [github.dev](https://github.dev).

### Découvrir l’application { #application-discovery }

Par défaut, l’extension détecte automatiquement les applications FastAPI dans votre espace de travail en recherchant les fichiers qui instancient `FastAPI()`. Si la détection automatique ne convient pas à la structure de votre projet, vous pouvez spécifier un point d’entrée via `[tool.fastapi]` dans `pyproject.toml` ou le paramètre VS Code `fastapi.entryPoint`, en utilisant la notation de module (par ex. `myapp.main:app`).

## Fonctionnalités { #features }

- **Explorateur des chemins d'accès** — Une vue arborescente latérale de tous les <dfn title="routes, endpoints">*chemins d'accès*</dfn> de votre application. Cliquez pour accéder à n’importe quelle définition de route ou de routeur.
- **Recherche de routes** — Recherchez par chemin, méthode ou nom avec <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (sur macOS : <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>).
- **Navigation CodeLens** — Liens cliquables au-dessus des appels du client de test (par ex. `client.get('/items')`) menant au *chemin d'accès* correspondant, pour naviguer rapidement entre les tests et l’implémentation.
- **Déployer sur FastAPI Cloud** — Déploiement en un clic de votre application sur [FastAPI Cloud](https://fastapicloud.com/).
- **Diffuser les journaux de l’application** — Diffusion en temps réel des journaux de votre application déployée sur FastAPI Cloud, avec filtrage par niveau et recherche textuelle.

Si vous souhaitez vous familiariser avec les fonctionnalités de l’extension, vous pouvez consulter le guide pas à pas de l’extension en ouvrant la palette de commandes (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> ou sur macOS : <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) et en sélectionnant « Welcome: Open walkthrough ... » puis en choisissant le guide « Get started with FastAPI ».
