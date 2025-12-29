### Target language

Translate to French (français).

Language code: fr.

### Grammar to use when talking to the reader

Use the formal grammar (use «vous» instead of «tu»).

Additionally, in instructional sentences, prefer the present tense for obligations:

1) Prefer «vous devez …» over «vous devrez …», unless the English source explicitly refers to a future requirement.

2) When translating “make sure (that) … is …”, prefer the indicative after «vous assurer que» (e.g. «Vous devez vous assurer qu'il est …») instead of the subjunctive (e.g. «qu'il soit …»).

### Quotes

1) Convert neutral double quotes («"») and English double typographic quotes («“» and «”») to French guillemets (««» and «»»).

2) In the French docs, guillemets are written without extra spaces: use «texte», not « texte ».

3) Do not convert quotes inside code blocks, inline code, paths, URLs, or anything wrapped in backticks.

Examples:

    Source (English):

        «««
        "Hello world"
        “Hello Universe”
        "He said: 'Hello'"
        "The module is `__main__`"
        »»»

    Result (French):

        «««
        «Hello world»
        «Hello Universe»
        «He said: 'Hello'»
        «The module is `__main__`»
        »»»

### Ellipsis

1) Make sure there is a space between an ellipsis and a word following or preceding the ellipsis.

Examples:

    Source (English):

        «««
        ...as we intended.
        ...this would work:
        ...etc.
        others...
        More to come...
        »»»

    Result (French):

        «««
        ... comme prévu.
        ... cela fonctionnerait :
        ... etc.
        D'autres ...
        La suite ...
        »»»

2) This does not apply in URLs, code blocks, and code snippets. Do not remove or add spaces there.

### Headings

1) Prefer translating headings using the infinitive form (as is common in the existing French docs): «Créer…», «Utiliser…», «Ajouter…».

2) For headings that are instructions written in imperative in English (e.g. “Go check …”), keep them in imperative in French, using the formal grammar (e.g. «Allez voir …»).

3) Keep heading punctuation as in the source. In particular, keep occurrences of literal « - » (space-hyphen-space) as « - » (the existing French docs use a hyphen here).

### French instructions about technical terms

Do not try to translate everything. In particular, keep common programming terms when that is the established usage in the French docs (e.g. «framework», «endpoint», «plug-in», «payload»). Use French where the existing docs already consistently use French (e.g. «requête», «réponse»).

Keep class names, function names, modules, file names, and CLI commands unchanged.

### List of English terms and their preferred French translations

Below is a list of English terms and their preferred French translations, separated by a colon («:»). Use these translations, do not use your own. If an existing translation does not use these terms, update it to use them.

* «/// note | Technical Details»: «/// note | Détails techniques»
* «/// note»: «/// note | Remarque»
* «/// tip»: «/// tip | Astuce»
* «/// warning»: «/// warning | Attention»
* «/// check»: «/// check | vérifier»
* «/// info»: «/// info»

* «the docs»: «les documents»
* «the documentation»: «la documentation»

* «Exclude from OpenAPI»: «Exclusion d'OpenAPI»

* «framework»: «framework» (do not translate to «cadre»)
* «performance»: «performance»

* «type hints»: «annotations de type»
* «type annotations»: «annotations de type»

* «autocomplete»: «autocomplétion»
* «autocompletion»: «autocomplétion»

* «the request» (what the client sends to the server): «la requête»
* «the response» (what the server sends back to the client): «la réponse»

* «the request body»: «le corps de la requête»
* «the response body»: «le corps de la réponse»

* «path operation»: «chemin d'accès»
* «path operations» (plural): «chemins d'accès»
* «path operation function»: «fonction de chemin d'accès»
* «path operation decorator»: «décorateur de chemin d'accès»

* «path parameter»: «paramètre de chemin»
* «query parameter»: «paramètre de requête»

* «the `Request`»: «`Request`» (keep as code identifier)
* «the `Response`»: «`Response`» (keep as code identifier)

* «deployment»: «déploiement»
* «to upgrade»: «mettre à niveau»

* «deprecated»: «déprécié»
* «to deprecate»: «déprécier»

* «cheat sheet»: «aide-mémoire»
* «plug-in»: «plug-in»
