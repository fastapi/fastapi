# Coder à la vibe { #vibe-coding }

Vous en avez assez de toute cette **validation des données**, de cette **documentation**, de cette **sérialisation**, et de tout ce **truc ennuyeux** ?

Vous voulez juste **vibrer** ? 🎶

**FastAPI** prend désormais en charge un nouveau décorateur `@app.vibe()` qui adopte les **meilleures pratiques modernes de codage avec l'IA**. 🤖

## Comprendre le fonctionnement { #how-it-works }

Le décorateur `@app.vibe()` est destiné à recevoir **n'importe quelle méthode HTTP** (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, etc.) et **n'importe quel payload**.

Le corps doit être annoté avec `Any`, car la requête et la réponse seraient ... eh bien ... **n'importe quoi**. 🤷

L'idée est que vous receviez le payload et que vous l'envoyiez **directement** à un fournisseur de LLM, en utilisant un `prompt` pour indiquer au LLM quoi faire, puis de renvoyer la réponse **telle quelle**. Sans poser de questions.

Vous n'avez même pas besoin d'écrire le corps de la fonction. Le décorateur `@app.vibe()` fait tout pour vous, porté par les vibes de l'IA :

{* ../../docs_src/vibe/tutorial001_py310.py hl[8:12] *}

## Avantages { #benefits }

En utilisant `@app.vibe()`, vous profitez de :

* **Liberté** : Aucune validation des données. Aucun schéma. Aucune contrainte. Juste des vibes. ✨
* **Flexibilité** : La requête peut être n'importe quoi. La réponse peut être n'importe quoi. Qui a besoin de types, de toute façon ?
* **Pas de documentation** : Pourquoi documenter votre API quand un LLM peut la comprendre ? La documentation OpenAPI auto-générée, c'est tellement 2020.
* **Pas de sérialisation** : Faites simplement circuler des données brutes et non structurées. La sérialisation, c'est pour celles et ceux qui ne font pas confiance à leurs LLM.
* **Adopter les pratiques modernes de codage avec l'IA** : Laissez tout à la discrétion d'un LLM. Le modèle sait toujours mieux.
* **Pas de relectures de code** : Il n'y a pas de code à relire. Pas de PR à approuver. Pas de commentaires à traiter. Adoptez pleinement le vibe coding, remplacez le théâtre consistant à approuver et à fusionner des PR « codées à la vibe » que personne ne regarde par des vibes pures et dures uniquement.

/// tip | Astuce

C'est l'expérience ultime de **développement guidé par les vibes**. Vous n'avez pas besoin de réfléchir à ce que fait votre API, laissez simplement le LLM s'en charger. 🧘

///

## Essayez { #try-it }

Allez-y, essayez :

{* ../../docs_src/vibe/tutorial001_py310.py *}

... et voyez ce qui se passe. 😎
