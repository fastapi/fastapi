# OpenTelemetry { #opentelemetry }

Lorsque votre API est en cours d'exécution, vous pouvez vouloir savoir quel trafic elle reçoit, quelles requêtes sont lentes et quand des erreurs se produisent.

La **télémétrie** désigne les données sur le comportement de votre application qui vous aident à répondre à ces questions. Les types courants comprennent :

- **Métriques** : des mesures que vous pouvez agréger au fil du temps, comme les temps de réponse et le nombre de requêtes en cours de traitement.
- **Traces** : des enregistrements de requêtes individuelles et des opérations effectuées pour les traiter. Chaque opération chronométrée est appelée un **span**.
- **Logs** : des enregistrements horodatés d'événements, comme le démarrage d'une application ou l'échec d'une opération.

[**OpenTelemetry**](https://opentelemetry.io/) est un ensemble de standards et d'outils permettant de collecter la télémétrie et de l'envoyer à un service de supervision, où vous pouvez l'explorer dans des tableaux de bord.

**FastAPI prend en charge OpenTelemetry par défaut** pour les traces, les métriques et les logs des requêtes HTTP. Les connexions WebSocket fournissent également des traces et des logs. Pour consulter ces données, configurez un service de supervision pour les recevoir.

## Installer FastAPI { #install-fastapi }

Installez FastAPI avec les dépendances optionnelles `standard`, qui incluent les paquets permettant d'envoyer la télémétrie :

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## Créer l'application { #create-the-app }

Créez un fichier `main.py` :

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

Remarquez que tout fonctionne par défaut : vous n'avez pas besoin d'écrire de code personnalisé pour que la télémétrie fonctionne.

## FastAPI Cloud { #fastapi-cloud }

Lorsque vous déployez sur [FastAPI Cloud](https://fastapicloud.com) avec `fastapi[standard]`, les métriques fonctionnent automatiquement. Vous n'avez rien d'autre à configurer.

Avec les offres Pro, vous pouvez consulter le nombre de requêtes, les taux d'erreur et les temps de réponse dans le [tableau de bord des métriques](https://fastapicloud.com/docs/monitoring-and-performance/metrics/).

<img src="/img/tutorial/opentelemetry/image01.png" alt="Tableau de bord des métriques FastAPI Cloud Pro avec des exemples de données">

## Autres services de supervision { #other-monitoring-services }

Pour envoyer la télémétrie à un autre service de supervision, configurez un endpoint qui accepte **OTLP**, le protocole OpenTelemetry pour l'envoi de télémétrie. Utilisez l'endpoint de base HTTP/protobuf du service.

Définissez ces variables d'environnement en remplaçant l'URL d'exemple par votre endpoint :

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` identifie votre application dans le service de supervision. L'endpoint est l'URL de base pour recevoir les données. Les traces sont envoyées à `/v1/traces`, les métriques à `/v1/metrics` et les logs à `/v1/logs` sous cette URL.

Si votre service nécessite une authentification, définissez `OTEL_EXPORTER_OTLP_HEADERS` avec les en-têtes qu'il spécifie, par exemple `api-key=YOUR_API_KEY`.

## Exécuter l'application { #run-the-app }

Démarrez l'application dans le même terminal :

<div class="termy">

```console
$ uv run fastapi run
```

</div>

Dans un autre terminal, envoyez une requête :

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

Ouvrez votre service de supervision et recherchez `my-api`. Après le prochain export, vous pouvez voir une trace avec un span `GET /items/{item_id}`, ainsi que des métriques sur le nombre de requêtes, la durée des réponses et les requêtes actives.

## Personnaliser la télémétrie { #customize-telemetry }

### Configurer les fournisseurs et les exportateurs { #configure-providers-and-exporters }

Un **fournisseur** fournit les objets qui enregistrent les traces, les métriques ou les logs. Sa configuration contrôle la façon dont ces données sont traitées et exportées.

Les bibliothèques de télémétrie peuvent configurer les fournisseurs globaux d'OpenTelemetry. Configurez la bibliothèque avant le démarrage de l'application, et FastAPI utilise automatiquement ces fournisseurs.

Lorsqu'un endpoint OTLP est défini dans l'environnement, FastAPI ajoute un exportateur pour cette destination à chaque fournisseur activé. Les exportateurs existants continuent d'envoyer des données vers leurs destinations.

Configurez chaque destination une seule fois. Si une autre bibliothèque gère déjà la destination définie dans l'environnement, désactivez son export vers cette destination ou désactivez la configuration automatique de FastAPI :

```python
app = FastAPI(telemetry={"auto_configure": False})
```

Vous pouvez aussi passer un fournisseur directement dans le dictionnaire `telemetry`. Par exemple, ce fournisseur utilise l'exportateur console d'OpenTelemetry pour afficher les spans des requêtes dans votre terminal :

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

L'**exportateur** envoie les spans vers leur destination. `BatchSpanProcessor` regroupe les spans et les envoie en arrière-plan. Remplacez l'exportateur console par un exportateur fourni par votre bibliothèque de supervision pour utiliser sa destination. Consultez le [guide d'instrumentation Python d'OpenTelemetry](https://opentelemetry.io/docs/languages/python/instrumentation/) pour plus d'options de configuration.

Utilisez `meter_provider` ou `logger_provider` dans le même dictionnaire pour fournir un fournisseur de métriques ou de logs. L'application ou la bibliothèque qui crée un fournisseur gère son arrêt. FastAPI gère les composants d'export qu'il ajoute.

/// warning | Alertes

OpenTelemetry utilise des fournisseurs globaux par défaut. Une configuration indépendante de la télémétrie pour les [sous-applications montées](sub-applications.md) n'est pas garantie.

///

### Tracer les opérations des requêtes { #trace-request-operations }

Par défaut, les traces des requêtes incluent des spans pour la résolution des dépendances, l'exécution de votre fonction de chemin d'accès, la sérialisation de la réponse et l'exécution de chaque tâche dans `BackgroundTasks` de FastAPI. Ces spans utilisent le même fournisseur et les mêmes exportateurs.

Les spans des tâches en arrière-plan font toujours partie de la trace de la requête. Ils s'exécutent après la fin du span de la réponse HTTP et n'augmentent donc pas le temps de réponse mesuré.

Pour enregistrer uniquement le span de la requête HTTP, définissez `operation_spans` sur `False` :

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### Tracer les connexions WebSocket { #trace-websocket-connections }

Chaque connexion WebSocket possède un span tel que `WS /ws/{room}`, qui couvre le gestionnaire et le nettoyage des dépendances. Il utilise les mêmes fournisseurs et paramètres, notamment `operation_spans` pour la résolution des dépendances et l'exécution de l'endpoint.

Les métriques des requêtes HTTP couvrent uniquement les requêtes HTTP. Les déconnexions WebSocket normales avec les codes `1000` ou `1001` ne produisent pas de logs d'erreur.

### Examiner les erreurs { #inspect-errors }

FastAPI enregistre les exceptions non gérées sous forme de logs OpenTelemetry, liés à la trace de la requête ou de la connexion. Les logs d'erreur sont enregistrés même lorsque la trace n'est pas échantillonnée.

Les logs d'exception incluent le type, le message et la trace de pile de l'exception. Les messages et les traces de pile peuvent contenir des informations sensibles. Utilisez les processeurs de logs de votre fournisseur pour les filtrer ou masquer ces informations, ou définissez `logs` sur `False` pour désactiver ces logs.

FastAPI enregistre également les échecs de validation des requêtes sous forme de logs d'avertissement avec la route et le nombre d'erreurs. Ces logs n'incluent pas les données d'entrée invalides.

## Choisir les données à enregistrer { #choose-what-to-record }

Le dictionnaire `telemetry` accepte également ces paramètres :

| Paramètre | Fonction | Valeur par défaut |
| --- | --- | --- |
| `tracing` | Enregistrer les spans des requêtes HTTP et des connexions WebSocket | `True` |
| `metrics` | Enregistrer les métriques des requêtes HTTP | `True` |
| `logs` | Enregistrer les échecs de validation et les exceptions non gérées | `True` |
| `operation_spans` | Ajouter des spans pour les opérations des requêtes | `True` |
| `exclude` | Ignorer les requêtes lorsqu'une fonction recevant le scope ASGI renvoie `True` | `None` |
| `auto_configure` | Ajouter des exportateurs pour les endpoints définis dans les variables d'environnement | `True` |

Par exemple, pour collecter des métriques tout en excluant les vérifications de l'état de santé :

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

Définissez `auto_configure` sur `False` lorsque votre application gère elle-même la configuration des fournisseurs, par exemple dans sa fonction lifespan.
