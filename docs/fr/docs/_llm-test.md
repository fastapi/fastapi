# Fichier de test LLM { #llm-test-file }

Ce document teste si le <abbr title="Large Language Model - Grand modèle de langage">LLM</abbr>, qui traduit la documentation, comprend le `general_prompt` dans `scripts/translate.py` et l’invite spécifique à la langue dans `docs/{language code}/llm-prompt.md`. L’invite spécifique à la langue est ajoutée à la fin de `general_prompt`.

Les tests ajoutés ici seront visibles par tous les concepteurs d’invites spécifiques à chaque langue.

Utiliser comme suit :

* Avoir une invite spécifique à la langue - `docs/{language code}/llm-prompt.md`.
* Effectuer une nouvelle traduction de ce document dans votre langue cible souhaitée (voir par exemple la commande `translate-page` de `translate.py`). Cela créera la traduction sous `docs/{language code}/docs/_llm-test.md`.
* Vérifier si tout est correct dans la traduction.
* Si nécessaire, améliorer votre invite spécifique à la langue, l’invite générale, ou le document anglais.
* Corriger ensuite manuellement les problèmes restants dans la traduction, afin que ce soit une bonne traduction.
* Retraduire, en ayant la bonne traduction en place. Le résultat idéal serait que le LLM ne fasse plus aucun changement à la traduction. Cela signifie que l’invite générale et votre invite spécifique à la langue sont aussi bonnes que possible (il fera parfois quelques changements apparemment aléatoires, la raison étant que <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">les LLM ne sont pas des algorithmes déterministes</a>).

Les tests :

## Extraits de code { #code-snippets }

//// tab | Test

Ceci est un extrait de code : `foo`. Et ceci est un autre extrait de code : `bar`. Et encore un autre : `baz quux`.

////

//// tab | Info

Le contenu des extraits de code doit être laissé tel quel.

Voir la section `### Content of code snippets` dans l’invite générale dans `scripts/translate.py`.

////

## Guillemets { #quotes }

//// tab | Test

Hier, mon ami a écrit : « Si vous écrivez « incorrectly » correctement, vous l’avez écrit de façon incorrecte ». À quoi j’ai répondu : « Correct, mais ‘incorrectly’ est incorrectement non pas ‘« incorrectly »’ ».

/// note | Remarque

Le LLM traduira probablement ceci de manière erronée. Il est seulement intéressant de voir s’il conserve la traduction corrigée lors d’une retraduction.

///

////

//// tab | Info

Le concepteur de l’invite peut choisir s’il souhaite convertir les guillemets neutres en guillemets typographiques. Il est acceptable de les laisser tels quels.

Voir par exemple la section `### Quotes` dans `docs/de/llm-prompt.md`.

////

## Guillemets dans les extraits de code { #quotes-in-code-snippets }

//// tab | Test

`pip install "foo[bar]"`

Exemples de littéraux de chaîne dans des extraits de code : `"this"`, `'that'`.

Un exemple difficile de littéraux de chaîne dans des extraits de code : `f"I like {'oranges' if orange else "apples"}"`

Hardcore: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Info

... Cependant, les guillemets à l’intérieur des extraits de code doivent rester tels quels.

////

## Blocs de code { #code-blocks }

//// tab | Test

Un exemple de code Bash ...

```bash
# Afficher un message de bienvenue à l'univers
echo "Hello universe"
```

... et un exemple de code console ...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

... et un autre exemple de code console ...

```console
// Créer un répertoire "Code"
$ mkdir code
// Aller dans ce répertoire
$ cd code
```

... et un exemple de code Python ...

```Python
wont_work()  # Cela ne fonctionnera pas 😱
works(foo="bar")  # Cela fonctionne 🎉
```

... et c’est tout.

////

//// tab | Info

Le code dans les blocs de code ne doit pas être modifié, à l’exception des commentaires.

Voir la section `### Content of code blocks` dans l’invite générale dans `scripts/translate.py`.

////

## Onglets et encadrés colorés { #tabs-and-colored-boxes }

//// tab | Test

/// info | Info
Du texte
///

/// note | Remarque
Du texte
///

/// note | Détails techniques
Du texte
///

/// check | Vérifications
Du texte
///

/// tip | Astuce
Du texte
///

/// warning | Alertes
Du texte
///

/// danger | Danger
Du texte
///

////

//// tab | Info

Les onglets et les blocs « Info »/« Note »/« Warning »/etc. doivent avoir la traduction de leur titre ajoutée après une barre verticale (« | »).

Voir les sections `### Special blocks` et `### Tab blocks` dans l’invite générale dans `scripts/translate.py`.

////

## Liens Web et internes { #web-and-internal-links }

//// tab | Test

Le texte du lien doit être traduit, l’adresse du lien doit rester inchangée :

* [Lien vers le titre ci-dessus](#code-snippets)
* [Lien interne](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Lien externe</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Lien vers une feuille de style</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Lien vers un script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Lien vers une image</a>

Le texte du lien doit être traduit, l’adresse du lien doit pointer vers la traduction :

* <a href="https://fastapi.tiangolo.com/fr/" class="external-link" target="_blank">Lien FastAPI</a>

////

//// tab | Info

Les liens doivent être traduits, mais leur adresse doit rester inchangée. Exception faite des liens absolus vers des pages de la documentation FastAPI. Dans ce cas, il faut pointer vers la traduction.

Voir la section `### Links` dans l’invite générale dans `scripts/translate.py`.

////

## Éléments HTML « abbr » { #html-abbr-elements }

//// tab | Test

Voici quelques éléments entourés d’un élément HTML « abbr » (certains sont inventés) :

### L’abbr fournit une expression complète { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - S'organiser pour réussir">GTD</abbr>
* <abbr title="less than - inférieur à"><code>lt</code></abbr>
* <abbr title="XML Web Token - Jeton Web XML">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - Interface passerelle serveur parallèle">PSGI</abbr>

### L’abbr donne une expression complète et une explication { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - Réseau des développeurs Mozilla: documentation pour les développeurs, écrite par l’équipe Firefox">MDN</abbr>
* <abbr title="Input/Output - Entrée/Sortie: lecture ou écriture sur le disque, communications réseau.">I/O</abbr>.

////

//// tab | Info

Les attributs « title » des éléments « abbr » sont traduits en suivant des consignes spécifiques.

Les traductions peuvent ajouter leurs propres éléments « abbr » que le LLM ne doit pas supprimer. Par exemple pour expliquer des mots anglais.

Voir la section `### HTML abbr elements` dans l’invite générale dans `scripts/translate.py`.

////

## Éléments HTML « dfn » { #html-dfn-elements }

* <dfn title="Un groupe de machines configurées pour être connectées et travailler ensemble d’une certaine manière.">grappe</dfn>
* <dfn title="Une méthode d’apprentissage automatique qui utilise des réseaux de neurones artificiels avec de nombreuses couches cachées entre les couches d’entrée et de sortie, développant ainsi une structure interne complète">Apprentissage profond</dfn>

## Titres { #headings }

//// tab | Test

### Créer une application Web - un tutoriel { #develop-a-webapp-a-tutorial }

Bonjour.

### Annotations de type et indications de type { #type-hints-and-annotations }

Rebonjour.

### Superclasses et sous-classes { #super-and-subclasses }

Rebonjour.

////

//// tab | Info

La seule règle stricte pour les titres est que le LLM laisse la partie hachage entre accolades inchangée, ce qui garantit que les liens ne se rompent pas.

Voir la section `### Headings` dans l’invite générale dans `scripts/translate.py`.

Pour certaines consignes spécifiques à la langue, voir par exemple la section `### Headings` dans `docs/de/llm-prompt.md`.

////

## Termes utilisés dans les documents { #terms-used-in-the-docs }

//// tab | Test

* vous
* votre

* p. ex.
* etc.

* `foo` en tant que `int`
* `bar` en tant que `str`
* `baz` en tant que `list`

* le Tutoriel - Guide utilisateur
* le Guide utilisateur avancé
* la documentation SQLModel
* la documentation de l’API
* la documentation automatique

* Data Science
* Apprentissage profond
* Apprentissage automatique
* Injection de dépendances
* authentification HTTP Basic
* HTTP Digest
* format ISO
* la norme JSON Schema
* le schéma JSON
* la définition de schéma
* Flux Password
* Mobile

* déprécié
* conçu
* invalide
* à la volée
* standard
* par défaut
* sensible à la casse
* insensible à la casse

* servir l’application
* servir la page

* l’app
* l’application

* la requête
* la réponse
* la réponse d’erreur

* le chemin d’accès
* le décorateur de chemin d’accès
* la fonction de chemin d’accès

* le corps
* le corps de la requête
* le corps de la réponse
* le corps JSON
* le corps de formulaire
* le corps de fichier
* le corps de la fonction

* le paramètre
* le paramètre de corps
* le paramètre de chemin
* le paramètre de requête
* le paramètre de cookie
* le paramètre d’en-tête
* le paramètre de formulaire
* le paramètre de fonction

* l’événement
* l’événement de démarrage
* le démarrage du serveur
* l’événement d’arrêt
* l’événement de cycle de vie

* le gestionnaire
* le gestionnaire d’événements
* le gestionnaire d’exceptions
* gérer

* le modèle
* le modèle Pydantic
* le modèle de données
* le modèle de base de données
* le modèle de formulaire
* l’objet modèle

* la classe
* la classe de base
* la classe parente
* la sous-classe
* la classe enfant
* la classe sœur
* la méthode de classe

* l’en-tête
* les en-têtes
* l’en-tête d’autorisation
* l’en-tête `Authorization`
* l’en-tête transféré

* le système d’injection de dépendances
* la dépendance
* l’élément dépendable
* le dépendant

* lié aux E/S
* lié au processeur
* concurrence
* parallélisme
* multi-traitement

* la variable d’env
* la variable d’environnement
* le `PATH`
* la variable `PATH`

* l’authentification
* le fournisseur d’authentification
* l’autorisation
* le formulaire d’autorisation
* le fournisseur d’autorisation
* l’utilisateur s’authentifie
* le système authentifie l’utilisateur

* la CLI
* l’interface en ligne de commande

* le serveur
* le client

* le fournisseur cloud
* le service cloud

* le développement
* les étapes de développement

* le dict
* le dictionnaire
* l’énumération
* l’enum
* le membre d’enum

* l’encodeur
* le décodeur
* encoder
* décoder

* l’exception
* lever

* l’expression
* l’instruction

* le frontend
* le backend

* la discussion GitHub
* le ticket GitHub

* la performance
* l’optimisation des performances

* le type de retour
* la valeur de retour

* la sécurité
* le schéma de sécurité

* la tâche
* la tâche d’arrière-plan
* la fonction de tâche

* le template
* le moteur de templates

* l’annotation de type
* l’annotation de type

* le worker du serveur
* le worker Uvicorn
* le Worker Gunicorn
* le processus worker
* la classe de worker
* la charge de travail

* le déploiement
* déployer

* le SDK
* le kit de développement logiciel

* le `APIRouter`
* le `requirements.txt`
* le jeton Bearer
* le changement majeur incompatible
* le bogue
* le bouton
* l’appelable
* le code
* le commit
* le gestionnaire de contexte
* la coroutine
* la session de base de données
* le disque
* le domaine
* le moteur
* le faux X
* la méthode HTTP GET
* l’élément
* la bibliothèque
* le cycle de vie
* le verrou
* le middleware
* l’application mobile
* le module
* le montage
* le réseau
* l’origine
* la surcharge
* le payload
* le processeur
* la propriété
* le proxy
* la pull request
* la requête
* la RAM
* la machine distante
* le code d’état
* la chaîne
* l’étiquette
* le framework Web
* le joker
* retourner
* valider

////

//// tab | Info

Il s’agit d’une liste non exhaustive et non normative de termes (principalement) techniques présents dans les documents. Elle peut aider le concepteur de l’invite à déterminer pour quels termes le LLM a besoin d’un coup de main. Par exemple, lorsqu’il continue de remplacer une bonne traduction par une traduction sous-optimale. Ou lorsqu’il a des difficultés à conjuguer/décliner un terme dans votre langue.

Voir par exemple la section `### List of English terms and their preferred German translations` dans `docs/de/llm-prompt.md`.

////
