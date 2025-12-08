# Alte 403-Authentifizierungsfehler-Statuscodes verwenden { #use-old-403-authentication-error-status-codes }

Vor FastAPI-Version `0.122.0` verwendeten die integrierten Sicherheits-Utilities den HTTP-Statuscode `403 Forbidden`, wenn sie dem Client nach einer fehlgeschlagenen Authentifizierung einen Fehler zurückgaben.

Ab FastAPI-Version `0.122.0` verwenden sie den passenderen HTTP-Statuscode `401 Unauthorized` und geben in der Response einen sinnvollen `WWW-Authenticate`-Header zurück, gemäß den HTTP-Spezifikationen, <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Aber falls Ihre Clients aus irgendeinem Grund vom alten Verhalten abhängen, können Sie darauf zurückgreifen, indem Sie in Ihren Sicherheitsklassen die Methode `make_not_authenticated_error` überschreiben.

Sie können beispielsweise eine Unterklasse von `HTTPBearer` erstellen, die einen Fehler `403 Forbidden` zurückgibt, statt des Default-`401 Unauthorized`-Fehlers:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py39.py hl[9:13] *}

/// tip | Tipp

Beachten Sie, dass die Funktion die Exception-Instanz zurückgibt; sie wirft sie nicht. Das Werfen erfolgt im restlichen internen Code.

///
