# Authentification HTTP Basic { #http-basic-auth }

Pour les cas les plus simples, vous pouvez utiliser l'authentification HTTP Basic.

Avec l'authentification HTTP Basic, l'application attend un en-tête contenant un nom d'utilisateur et un mot de passe.

Si elle ne le reçoit pas, elle renvoie une erreur HTTP 401 « Unauthorized ».

Et elle renvoie un en-tête `WWW-Authenticate` avec la valeur `Basic`, et un paramètre optionnel `realm`.

Cela indique au navigateur d'afficher l'invite intégrée pour saisir un nom d'utilisateur et un mot de passe.

Ensuite, lorsque vous saisissez ce nom d'utilisateur et ce mot de passe, le navigateur les envoie automatiquement dans l'en-tête.

## Authentification HTTP Basic simple { #simple-http-basic-auth }

- Importer `HTTPBasic` et `HTTPBasicCredentials`.
- Créer un « schéma de sécurité » en utilisant `HTTPBasic`.
- Utiliser ce `security` avec une dépendance dans votre chemin d'accès.
- Cela renvoie un objet de type `HTTPBasicCredentials` :
    - Il contient le `username` et le `password` envoyés.

{* ../../docs_src/security/tutorial006_an_py310.py hl[4,8,12] *}

Lorsque vous essayez d'ouvrir l'URL pour la première fois (ou cliquez sur le bouton « Execute » dans les documents) le navigateur vous demandera votre nom d'utilisateur et votre mot de passe :

<img src="/img/tutorial/security/image12.png">

## Vérifier le nom d'utilisateur { #check-the-username }

Voici un exemple plus complet.

Utilisez une dépendance pour vérifier si le nom d'utilisateur et le mot de passe sont corrects.

Pour cela, utilisez le module standard Python <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> pour vérifier le nom d'utilisateur et le mot de passe.

`secrets.compare_digest()` doit recevoir des `bytes` ou une `str` ne contenant que des caractères ASCII (ceux de l'anglais), ce qui signifie qu'elle ne fonctionnerait pas avec des caractères comme `á`, comme dans `Sebastián`.

Pour gérer cela, nous convertissons d'abord `username` et `password` en `bytes` en les encodant en UTF-8.

Nous pouvons ensuite utiliser `secrets.compare_digest()` pour vérifier que `credentials.username` est « stanleyjobson » et que `credentials.password` est « swordfish ».

{* ../../docs_src/security/tutorial007_an_py310.py hl[1,12:24] *}

Cela serait équivalent à :

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Renvoyer une erreur
    ...
```

Mais en utilisant `secrets.compare_digest()`, cela sera sécurisé contre un type d'attaques appelé « attaques par chronométrage ».

### Attaques par chronométrage { #timing-attacks }

Mais qu'est-ce qu'une « attaque par chronométrage » ?

Imaginons que des attaquants essaient de deviner le nom d'utilisateur et le mot de passe.

Ils envoient alors une requête avec un nom d'utilisateur `johndoe` et un mot de passe `love123`.

Le code Python de votre application serait alors équivalent à quelque chose comme :

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Mais au moment où Python compare le premier `j` de `johndoe` au premier `s` de `stanleyjobson`, il retournera `False`, car il sait déjà que ces deux chaînes ne sont pas identiques, en se disant qu'« il n'est pas nécessaire de gaspiller plus de calcul pour comparer le reste des lettres ». Et votre application dira « Nom d'utilisateur ou mot de passe incorrect ».

Mais ensuite, les attaquants essaient avec le nom d'utilisateur `stanleyjobsox` et le mot de passe `love123`.

Et le code de votre application fait quelque chose comme :

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python devra comparer tout `stanleyjobso` dans `stanleyjobsox` et `stanleyjobson` avant de réaliser que les deux chaînes ne sont pas identiques. Cela prendra donc quelques microsecondes supplémentaires pour répondre « Nom d'utilisateur ou mot de passe incorrect ».

#### Le temps de réponse aide les attaquants { #the-time-to-answer-helps-the-attackers }

À ce stade, en remarquant que le serveur a mis quelques microsecondes de plus à envoyer la réponse « Nom d'utilisateur ou mot de passe incorrect », les attaquants sauront qu'ils ont trouvé quelque chose de juste : certaines des premières lettres étaient correctes.

Ils peuvent alors réessayer en sachant que c'est probablement quelque chose de plus proche de `stanleyjobsox` que de `johndoe`.

#### Une attaque « professionnelle » { #a-professional-attack }

Bien sûr, les attaquants n'essaieraient pas tout cela à la main ; ils écriraient un programme pour le faire, avec éventuellement des milliers ou des millions de tests par seconde. Ils obtiendraient une lettre correcte supplémentaire à la fois.

Ce faisant, en quelques minutes ou heures, les attaquants devineraient le nom d'utilisateur et le mot de passe corrects, avec « l'aide » de notre application, simplement en se basant sur le temps de réponse.

#### Corrigez-le avec `secrets.compare_digest()` { #fix-it-with-secrets-compare-digest }

Mais dans notre code nous utilisons justement `secrets.compare_digest()`.

En bref, il faudra le même temps pour comparer `stanleyjobsox` à `stanleyjobson` que pour comparer `johndoe` à `stanleyjobson`. Il en va de même pour le mot de passe.

Ainsi, en utilisant `secrets.compare_digest()` dans le code de votre application, votre application sera protégée contre toute cette gamme d'attaques de sécurité.

### Renvoyer l'erreur { #return-the-error }

Après avoir détecté que les identifiants sont incorrects, renvoyez une `HTTPException` avec un code d'état 401 (le même que lorsque aucun identifiant n'est fourni) et ajoutez l'en-tête `WWW-Authenticate` pour que le navigateur affiche à nouveau l'invite de connexion :

{* ../../docs_src/security/tutorial007_an_py310.py hl[26:30] *}
