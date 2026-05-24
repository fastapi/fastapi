# JSON avec des octets en Base64 { #json-with-bytes-as-base64 }

Si votre application doit recevoir et envoyer des données JSON, mais que vous devez y inclure des données binaires, vous pouvez les encoder en base64.

## Base64 vs fichiers { #base64-vs-files }

Envisagez d'abord d'utiliser [Fichiers de requête](../tutorial/request-files.md) pour téléverser des données binaires et [Réponse personnalisée - FileResponse](./custom-response.md#fileresponse--fileresponse-) pour envoyer des données binaires, plutôt que de les encoder dans du JSON.

JSON ne peut contenir que des chaînes encodées en UTF-8, il ne peut donc pas contenir d'octets bruts.

Base64 peut encoder des données binaires en chaînes, mais pour cela il doit utiliser plus de caractères que les données binaires originales ; c'est donc en général moins efficace que des fichiers classiques.

N'utilisez base64 que si vous devez absolument inclure des données binaires dans du JSON et que vous ne pouvez pas utiliser des fichiers pour cela.

## Pydantic `bytes` { #pydantic-bytes }

Vous pouvez déclarer un modèle Pydantic avec des champs `bytes`, puis utiliser `val_json_bytes` dans la configuration du modèle pour lui indiquer d'utiliser base64 pour valider les données JSON en entrée ; dans le cadre de cette validation, il décodera la chaîne base64 en octets.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

Si vous allez sur les `/docs`, vous verrez que le champ `data` attend des octets encodés en base64 :

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

Vous pourriez envoyer une requête comme :

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | Astuce

`aGVsbG8=` est l'encodage base64 de `hello`.

///

Pydantic décodera ensuite la chaîne base64 et vous fournira les octets originaux dans le champ `data` du modèle.

Vous recevrez une réponse comme :

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Pydantic `bytes` pour les données de sortie { #pydantic-bytes-for-output-data }

Vous pouvez également utiliser des champs `bytes` avec `ser_json_bytes` dans la configuration du modèle pour les données de sortie ; Pydantic sérialisera alors les octets en base64 lors de la génération de la réponse JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Pydantic `bytes` pour les données d'entrée et de sortie { #pydantic-bytes-for-input-and-output-data }

Et bien sûr, vous pouvez utiliser le même modèle configuré pour utiliser base64 afin de gérer à la fois l'entrée (valider) avec `val_json_bytes` et la sortie (sérialiser) avec `ser_json_bytes` lors de la réception et de l'envoi de données JSON.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
