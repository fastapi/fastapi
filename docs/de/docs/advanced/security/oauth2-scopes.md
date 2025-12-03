# OAuth2-Scopes { #oauth2-scopes }

Sie können OAuth2-<abbr title="Geltungsbereiche">Scopes</abbr> direkt in **FastAPI** verwenden, sie sind nahtlos integriert.

Das ermöglicht es Ihnen, ein feingranuliertes Berechtigungssystem nach dem OAuth2-Standard in Ihre OpenAPI-Anwendung (und deren API-Dokumentation) zu integrieren.

OAuth2 mit Scopes ist der Mechanismus, der von vielen großen Authentifizierungsanbietern wie Facebook, Google, GitHub, Microsoft, X (Twitter) usw. verwendet wird. Sie verwenden ihn, um Benutzern und Anwendungen spezifische Berechtigungen zu erteilen.

Jedes Mal, wenn Sie sich mit Facebook, Google, GitHub, Microsoft oder X (Twitter) anmelden („log in with“), verwendet die entsprechende Anwendung OAuth2 mit Scopes.

In diesem Abschnitt erfahren Sie, wie Sie Authentifizierung und Autorisierung mit demselben OAuth2, mit Scopes in Ihrer **FastAPI**-Anwendung verwalten.

/// warning | Achtung

Dies ist ein mehr oder weniger fortgeschrittener Abschnitt. Wenn Sie gerade erst anfangen, können Sie ihn überspringen.

Sie benötigen nicht unbedingt OAuth2-Scopes, und Sie können die Authentifizierung und Autorisierung handhaben wie Sie möchten.

Aber OAuth2 mit Scopes kann bequem in Ihre API (mit OpenAPI) und deren API-Dokumentation integriert werden.

Dennoch, verwenden Sie solche Scopes oder andere Sicherheits-/Autorisierungsanforderungen in Ihrem Code so wie Sie es möchten.

In vielen Fällen kann OAuth2 mit Scopes ein Overkill sein.

Aber wenn Sie wissen, dass Sie es brauchen oder neugierig sind, lesen Sie weiter.

///

## OAuth2-Scopes und OpenAPI { #oauth2-scopes-and-openapi }

Die OAuth2-Spezifikation definiert „Scopes“ als eine Liste von durch Leerzeichen getrennten Strings.

Der Inhalt jedes dieser Strings kann ein beliebiges Format haben, sollte jedoch keine Leerzeichen enthalten.

Diese Scopes stellen „Berechtigungen“ dar.

In OpenAPI (z. B. der API-Dokumentation) können Sie „Sicherheitsschemas“ definieren.

Wenn eines dieser Sicherheitsschemas OAuth2 verwendet, können Sie auch Scopes deklarieren und verwenden.

Jeder „Scope“ ist nur ein String (ohne Leerzeichen).

Er wird normalerweise verwendet, um bestimmte Sicherheitsberechtigungen zu deklarieren, zum Beispiel:

* `users:read` oder `users:write` sind gängige Beispiele.
* `instagram_basic` wird von Facebook / Instagram verwendet.
* `https://www.googleapis.com/auth/drive` wird von Google verwendet.

/// info | Info

In OAuth2 ist ein „Scope“ nur ein String, der eine bestimmte erforderliche Berechtigung deklariert.

Es spielt keine Rolle, ob er andere Zeichen wie `:` enthält oder ob es eine URL ist.

Diese Details sind implementierungsspezifisch.

Für OAuth2 sind es einfach nur Strings.

///

## Gesamtübersicht { #global-view }

Sehen wir uns zunächst kurz die Teile an, die sich gegenüber den Beispielen im Haupt-**Tutorial – Benutzerhandbuch** für [OAuth2 mit Password (und Hashing), Bearer mit JWT-Tokens](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank} ändern. Diesmal verwenden wir OAuth2-Scopes:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

Sehen wir uns diese Änderungen nun Schritt für Schritt an.

## OAuth2-Sicherheitsschema { #oauth2-security-scheme }

Die erste Änderung ist, dass wir jetzt das OAuth2-Sicherheitsschema mit zwei verfügbaren Scopes deklarieren: `me` und `items`.

Der `scopes`-Parameter erhält ein <abbr title="Dictionary – Zuordnungstabelle: In anderen Sprachen auch Hash, Map, Objekt, Assoziatives Array genannt">`dict`</abbr> mit jedem Scope als Schlüssel und dessen Beschreibung als Wert:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

Da wir diese Scopes jetzt deklarieren, werden sie in der API-Dokumentation angezeigt, wenn Sie sich einloggen/autorisieren.

Und Sie können auswählen, auf welche Scopes Sie Zugriff haben möchten: `me` und `items`.

Das ist derselbe Mechanismus, der verwendet wird, wenn Sie beim Anmelden mit Facebook, Google, GitHub, usw. Berechtigungen erteilen:

<img src="/img/tutorial/security/image11.png">

## JWT-Token mit Scopes { #jwt-token-with-scopes }

Ändern Sie nun die Token-*Pfadoperation*, um die angeforderten Scopes zurückzugeben.

Wir verwenden immer noch dasselbe `OAuth2PasswordRequestForm`. Es enthält eine Eigenschaft `scopes` mit einer `list`e von `str`s für jeden Scope, den es im <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Request</abbr> erhalten hat.

Und wir geben die Scopes als Teil des JWT-Tokens zurück.

/// danger | Gefahr

Der Einfachheit halber fügen wir hier die empfangenen Scopes direkt zum Token hinzu.

Aus Sicherheitsgründen sollten Sie jedoch sicherstellen, dass Sie in Ihrer Anwendung nur die Scopes hinzufügen, die der Benutzer tatsächlich haben kann, oder die Sie vordefiniert haben.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## Scopes in *Pfadoperationen* und Abhängigkeiten deklarieren { #declare-scopes-in-path-operations-and-dependencies }

Jetzt deklarieren wir, dass die *Pfadoperation* für `/users/me/items/` den Scope `items` erfordert.

Dazu importieren und verwenden wir `Security` von `fastapi`.

Sie können `Security` verwenden, um Abhängigkeiten zu deklarieren (genau wie `Depends`), aber `Security` erhält auch einen Parameter `scopes` mit einer Liste von Scopes (Strings).

In diesem Fall übergeben wir eine Abhängigkeitsfunktion `get_current_active_user` an `Security` (genauso wie wir es mit `Depends` tun würden).

Wir übergeben aber auch eine `list`e von Scopes, in diesem Fall mit nur einem Scope: `items` (es könnten mehrere sein).

Und die Abhängigkeitsfunktion `get_current_active_user` kann auch Unterabhängigkeiten deklarieren, nicht nur mit `Depends`, sondern auch mit `Security`. Ihre eigene Unterabhängigkeitsfunktion (`get_current_user`) und weitere Scope-Anforderungen deklarierend.

In diesem Fall erfordert sie den Scope `me` (sie könnte mehr als einen Scope erfordern).

/// note | Hinweis

Sie müssen nicht unbedingt an verschiedenen Stellen verschiedene Scopes hinzufügen.

Wir tun dies hier, um zu demonstrieren, wie **FastAPI** auf verschiedenen Ebenen deklarierte Scopes verarbeitet.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | Technische Details

`Security` ist tatsächlich eine Unterklasse von `Depends` und hat nur noch einen zusätzlichen Parameter, den wir später kennenlernen werden.

Durch die Verwendung von `Security` anstelle von `Depends` weiß **FastAPI** jedoch, dass es Sicherheits-Scopes deklarieren, intern verwenden und die API mit OpenAPI dokumentieren kann.

Wenn Sie jedoch `Query`, `Path`, `Depends`, `Security` und andere von `fastapi` importieren, handelt es sich tatsächlich um Funktionen, die spezielle Klassen zurückgeben.

///

## `SecurityScopes` verwenden { #use-securityscopes }

Aktualisieren Sie nun die Abhängigkeit `get_current_user`.

Das ist diejenige, die von den oben genannten Abhängigkeiten verwendet wird.

Hier verwenden wir dasselbe OAuth2-Schema, das wir zuvor erstellt haben, und deklarieren es als Abhängigkeit: `oauth2_scheme`.

Da diese Abhängigkeitsfunktion selbst keine Scope-Anforderungen hat, können wir `Depends` mit `oauth2_scheme` verwenden. Wir müssen `Security` nicht verwenden, wenn wir keine Sicherheits-Scopes angeben müssen.

Wir deklarieren auch einen speziellen Parameter vom Typ `SecurityScopes`, der aus `fastapi.security` importiert wird.

Diese `SecurityScopes`-Klasse ähnelt `Request` (`Request` wurde verwendet, um das Request-Objekt direkt zu erhalten).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## Die `scopes` verwenden { #use-the-scopes }

Der Parameter `security_scopes` wird vom Typ `SecurityScopes` sein.

Dieses verfügt über ein Attribut `scopes` mit einer Liste, die alle von ihm selbst benötigten Scopes enthält und ferner alle Abhängigkeiten, die dieses als Unterabhängigkeit verwenden. Sprich, alle „Dependanten“ ... das mag verwirrend klingen, wird aber später noch einmal erklärt.

Das `security_scopes`-Objekt (der Klasse `SecurityScopes`) stellt außerdem ein `scope_str`-Attribut mit einem einzelnen String bereit, der die durch Leerzeichen getrennten Scopes enthält (den werden wir verwenden).

Wir erstellen eine `HTTPException`, die wir später an mehreren Stellen wiederverwenden (`raise`n) können.

In diese Exception fügen wir (falls vorhanden) die erforderlichen Scopes als durch Leerzeichen getrennten String ein (unter Verwendung von `scope_str`). Wir fügen diesen String mit den Scopes in den Header `WWW-Authenticate` ein (das ist Teil der Spezifikation).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## Den `username` und das Format der Daten überprüfen { #verify-the-username-and-data-shape }

Wir verifizieren, dass wir einen `username` erhalten, und extrahieren die Scopes.

Und dann validieren wir diese Daten mit dem Pydantic-Modell (wobei wir die `ValidationError`-Exception abfangen), und wenn wir beim Lesen des JWT-Tokens oder beim Validieren der Daten mit Pydantic einen Fehler erhalten, lösen wir die zuvor erstellte `HTTPException` aus.

Dazu aktualisieren wir das Pydantic-Modell `TokenData` mit einem neuen Attribut `scopes`.

Durch die Validierung der Daten mit Pydantic können wir sicherstellen, dass wir beispielsweise präzise eine `list`e von `str`s mit den Scopes und einen `str` mit dem `username` haben.

Anstelle beispielsweise eines `dict`s oder etwas anderem, was später in der Anwendung zu Fehlern führen könnte und darum ein Sicherheitsrisiko darstellt.

Wir verifizieren auch, dass wir einen Benutzer mit diesem Benutzernamen haben, und wenn nicht, lösen wir dieselbe Exception aus, die wir zuvor erstellt haben.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## Die `scopes` verifizieren { #verify-the-scopes }

Wir überprüfen nun, ob das empfangene Token alle Scopes enthält, die von dieser Abhängigkeit und deren Verwendern (einschließlich *Pfadoperationen*) gefordert werden. Andernfalls lösen wir eine `HTTPException` aus.

Hierzu verwenden wir `security_scopes.scopes`, das eine `list`e mit allen diesen Scopes als `str` enthält.

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Abhängigkeitsbaum und Scopes { #dependency-tree-and-scopes }

Sehen wir uns diesen Abhängigkeitsbaum und die Scopes noch einmal an.

Da die Abhängigkeit `get_current_active_user` von `get_current_user` abhängt, wird der bei `get_current_active_user` deklarierte Scope `"me"` in die Liste der erforderlichen Scopes in `security_scopes.scopes` aufgenommen, das an `get_current_user` übergeben wird.

Die *Pfadoperation* selbst deklariert auch einen Scope, `"items"`, sodass dieser auch in der Liste der `security_scopes.scopes` enthalten ist, die an `get_current_user` übergeben wird.

So sieht die Hierarchie der Abhängigkeiten und Scopes aus:

* Die *Pfadoperation* `read_own_items` hat:
    * Erforderliche Scopes `["items"]` mit der Abhängigkeit:
    * `get_current_active_user`:
        * Die Abhängigkeitsfunktion `get_current_active_user` hat:
            * Erforderliche Scopes `["me"]` mit der Abhängigkeit:
            * `get_current_user`:
                * Die Abhängigkeitsfunktion `get_current_user` hat:
                    * Selbst keine erforderlichen Scopes.
                    * Eine Abhängigkeit, die `oauth2_scheme` verwendet.
                    * Einen `security_scopes`-Parameter vom Typ `SecurityScopes`:
                        * Dieser `security_scopes`-Parameter hat ein Attribut `scopes` mit einer `list`e, die alle oben deklarierten Scopes enthält, sprich:
                            * `security_scopes.scopes` enthält `["me", "items"]` für die *Pfadoperation* `read_own_items`.
                            * `security_scopes.scopes` enthält `["me"]` für die *Pfadoperation* `read_users_me`, da das in der Abhängigkeit `get_current_active_user` deklariert ist.
                            * `security_scopes.scopes` wird `[]` (nichts) für die *Pfadoperation* `read_system_status` enthalten, da diese keine `Security` mit `scopes` deklariert hat, und deren Abhängigkeit `get_current_user` ebenfalls keinerlei `scopes` deklariert.

/// tip | Tipp

Das Wichtige und „Magische“ hier ist, dass `get_current_user` für jede *Pfadoperation* eine andere Liste von `scopes` hat, die überprüft werden.

Alles hängt von den „Scopes“ ab, die in jeder *Pfadoperation* und jeder Abhängigkeit im Abhängigkeitsbaum für diese bestimmte *Pfadoperation* deklariert wurden.

///

## Weitere Details zu `SecurityScopes` { #more-details-about-securityscopes }

Sie können `SecurityScopes` an jeder Stelle und an mehreren Stellen verwenden, es muss sich nicht in der „Wurzel“-Abhängigkeit befinden.

Es wird immer die Sicherheits-Scopes enthalten, die in den aktuellen `Security`-Abhängigkeiten deklariert sind und in allen Abhängigkeiten für **diese spezifische** *Pfadoperation* und **diesen spezifischen** Abhängigkeitsbaum.

Da die `SecurityScopes` alle von den Verwendern der Abhängigkeiten deklarierten Scopes enthalten, können Sie damit überprüfen, ob ein Token in einer zentralen Abhängigkeitsfunktion über die erforderlichen Scopes verfügt, und dann unterschiedliche Scope-Anforderungen in unterschiedlichen *Pfadoperationen* deklarieren.

Diese werden für jede *Pfadoperation* unabhängig überprüft.

## Es testen { #check-it }

Wenn Sie die API-Dokumentation öffnen, können Sie sich authentisieren und angeben, welche Scopes Sie autorisieren möchten.

<img src="/img/tutorial/security/image11.png">

Wenn Sie keinen Scope auswählen, werden Sie „authentifiziert“, aber wenn Sie versuchen, auf `/users/me/` oder `/users/me/items/` zuzugreifen, wird eine Fehlermeldung angezeigt, die sagt, dass Sie nicht über genügend Berechtigungen verfügen. Sie können aber auf `/status/` zugreifen.

Und wenn Sie den Scope `me`, aber nicht den Scope `items` auswählen, können Sie auf `/users/me/` zugreifen, aber nicht auf `/users/me/items/`.

Das würde einer Drittanbieteranwendung passieren, die versucht, auf eine dieser *Pfadoperationen* mit einem Token zuzugreifen, das von einem Benutzer bereitgestellt wurde, abhängig davon, wie viele Berechtigungen der Benutzer dieser Anwendung erteilt hat.

## Über Integrationen von Drittanbietern { #about-third-party-integrations }

In diesem Beispiel verwenden wir den OAuth2-Flow „Password“.

Das ist angemessen, wenn wir uns bei unserer eigenen Anwendung anmelden, wahrscheinlich mit unserem eigenen Frontend.

Weil wir darauf vertrauen können, dass es den `username` und das `password` erhält, welche wir kontrollieren.

Wenn Sie jedoch eine OAuth2-Anwendung erstellen, mit der andere eine Verbindung herstellen würden (d.h. wenn Sie einen Authentifizierungsanbieter erstellen, der Facebook, Google, GitHub usw. entspricht), sollten Sie einen der anderen Flows verwenden.

Am häufigsten ist der „Implicit“-Flow.

Am sichersten ist der „Code“-Flow, die Implementierung ist jedoch komplexer, da mehr Schritte erforderlich sind. Da er komplexer ist, schlagen viele Anbieter letztendlich den „Implicit“-Flow vor.

/// note | Hinweis

Es ist üblich, dass jeder Authentifizierungsanbieter seine Flows anders benennt, um sie zu einem Teil seiner Marke zu machen.

Aber am Ende implementieren sie denselben OAuth2-Standard.

///

**FastAPI** enthält Werkzeuge für alle diese OAuth2-Authentifizierungs-Flows in `fastapi.security.oauth2`.

## `Security` in Dekorator-`dependencies` { #security-in-decorator-dependencies }

Auf die gleiche Weise können Sie eine `list`e von `Depends` im Parameter `dependencies` des Dekorators definieren (wie in [Abhängigkeiten in Pfadoperation-Dekoratoren](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank} erläutert), Sie könnten auch dort `Security` mit `scopes` verwenden.
