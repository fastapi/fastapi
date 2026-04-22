### Target language

Translate to French (français).

Language code: fr.

### Grammar to use when talking to the reader

Use the formal grammar (use `vous` instead of `tu`).

Additionally, in instructional sentences, prefer the present tense for obligations:

- Prefer `vous devez …` over `vous devrez …`, unless the English source explicitly refers to a future requirement.

- When translating “make sure (that) … is …”, prefer the indicative after `vous assurer que` (e.g. `Vous devez vous assurer qu'il est …`) instead of the subjunctive (e.g. `qu'il soit …`).

### Quotes

- Convert neutral double quotes (`"`) to French guillemets (`«` and `»`).

- Do not convert quotes inside code blocks, inline code, paths, URLs, or anything wrapped in backticks.

Examples:

Source (English):

```
"Hello world"
“Hello Universe”
"He said: 'Hello'"
"The module is `__main__`"
```

Result (French):

```
"Hello world"
“Hello Universe”
"He said: 'Hello'"
"The module is `__main__`"
```

### Ellipsis

- Make sure there is a space between an ellipsis and a word following or preceding the ellipsis.

Examples:

Source (English):

```
...as we intended.
...this would work:
...etc.
others...
More to come...
```

Result (French):

```
... comme prévu.
... cela fonctionnerait :
... etc.
D'autres ...
La suite ...
```

- This does not apply in URLs, code blocks, and code snippets. Do not remove or add spaces there.

### Headings

- Prefer translating headings using the infinitive form (as is common in the existing French docs): `Créer…`, `Utiliser…`, `Ajouter…`.

- For headings that are instructions written in imperative in English (e.g. `Go check …`), keep them in imperative in French, using the formal grammar (e.g. `Allez voir …`).

### French instructions about technical terms

Do not try to translate everything. In particular, keep common programming terms (e.g. `framework`, `endpoint`, `plug-in`, `payload`).

Keep class names, function names, modules, file names, and CLI commands unchanged.

### List of English terms and their preferred French translations

Below is a list of English terms and their preferred French translations, separated by a colon (:). Use these translations, do not use your own. If an existing translation does not use these terms, update it to use them.

- /// note | Technical Details»: /// note | Détails techniques
- /// note: /// note | Remarque
- /// tip: /// tip | Astuce
- /// warning: /// warning | Alertes
- /// check: /// check | Vérifications
- /// info: /// info

- the docs: les documents
- the documentation: la documentation

- Exclude from OpenAPI: Exclusion d'OpenAPI

- framework: framework (do not translate to cadre)
- performance: performance

- type hints: annotations de type
- type annotations: annotations de type

- autocomplete: autocomplétion
- autocompletion: autocomplétion

- the request (what the client sends to the server): la requête
- the response (what the server sends back to the client): la réponse

- the request body: le corps de la requête
- the response body: le corps de la réponse

- path operation: chemin d'accès
- path operations (plural): chemins d'accès
- path operation function: fonction de chemin d'accès
- path operation decorator: décorateur de chemin d'accès

- path parameter: paramètre de chemin
- query parameter: paramètre de requête

- the `Request`: `Request` (keep as code identifier)
- the `Response`: `Response` (keep as code identifier)

- deployment: déploiement
- to upgrade: mettre à niveau

- deprecated: déprécié
- to deprecate: déprécier

- cheat sheet: aide-mémoire
- plug-in: plug-in
