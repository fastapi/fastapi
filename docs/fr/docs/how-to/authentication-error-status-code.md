# Utiliser les anciens codes d'erreur d'authentification 403 { #use-old-403-authentication-error-status-codes }

Avant FastAPI version `0.122.0`, lorsque les utilitaires de sécurité intégrés renvoyaient une erreur au client après un échec d'authentification, ils utilisaient le code d'état HTTP `403 Forbidden`.

À partir de FastAPI version `0.122.0`, ils utilisent le code d'état HTTP plus approprié `401 Unauthorized`, et renvoient un en-tête `WWW-Authenticate` pertinent dans la réponse, conformément aux spécifications HTTP, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Mais si, pour une raison quelconque, vos clients dépendent de l'ancien comportement, vous pouvez y revenir en surchargeant la méthode `make_not_authenticated_error` dans vos classes de sécurité.

Par exemple, vous pouvez créer une sous-classe de `HTTPBearer` qui renvoie une erreur `403 Forbidden` au lieu de l'erreur par défaut `401 Unauthorized` :

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | Astuce

Remarquez que la fonction renvoie l'instance de l'exception, elle ne la lève pas. La levée est effectuée dans le reste du code interne.

///
