# Sicherheit { #security }

Es gibt viele Wege, Sicherheit, Authentifizierung und Autorisierung zu handhaben.

Und normalerweise ist es ein komplexes und „schwieriges“ Thema.

In vielen Frameworks und Systemen erfordert allein die Handhabung von Sicherheit und Authentifizierung viel Aufwand und Code (in vielen Fällen kann er 50 % oder mehr des gesamten geschriebenen Codes ausmachen).

**FastAPI** bietet mehrere Tools, die Ihnen helfen, schnell und auf standardisierte Weise mit **Sicherheit** umzugehen, ohne alle Sicherheits-Spezifikationen studieren und erlernen zu müssen.

Aber schauen wir uns zunächst ein paar kleine Konzepte an.

## In Eile? { #in-a-hurry }

Wenn Ihnen diese Begriffe egal sind und Sie einfach *jetzt* Sicherheit mit Authentifizierung basierend auf Benutzername und Passwort hinzufügen müssen, fahren Sie mit den nächsten Kapiteln fort.

## OAuth2 { #oauth2 }

OAuth2 ist eine Spezifikation, die verschiedene Möglichkeiten zur Handhabung von Authentifizierung und Autorisierung definiert.

Es handelt sich um eine recht umfangreiche Spezifikation, und sie deckt mehrere komplexe Anwendungsfälle ab.

Sie umfasst Möglichkeiten zur Authentifizierung mithilfe eines „Dritten“ („third party“).

Das ist es, was alle diese „Login mit Facebook, Google, X (Twitter), GitHub“-Systeme unter der Haube verwenden.

### OAuth 1 { #oauth-1 }

Es gab ein OAuth 1, das sich stark von OAuth2 unterscheidet und komplexer ist, da es direkte Spezifikationen enthält, wie die Kommunikation verschlüsselt wird.

Heutzutage ist es nicht sehr populär und wird kaum verwendet.

OAuth2 spezifiziert nicht, wie die Kommunikation verschlüsselt werden soll, sondern erwartet, dass Ihre Anwendung mit HTTPS bereitgestellt wird.

/// tip | Tipp

Im Abschnitt über **Deployment** erfahren Sie, wie Sie HTTPS mithilfe von Traefik und Let's Encrypt kostenlos einrichten.

///

## OpenID Connect { #openid-connect }

OpenID Connect ist eine weitere Spezifikation, die auf **OAuth2** basiert.

Sie erweitert lediglich OAuth2, indem sie einige Dinge spezifiziert, die in OAuth2 relativ mehrdeutig sind, um zu versuchen, es interoperabler zu machen.

Beispielsweise verwendet der Google Login OpenID Connect (welches seinerseits OAuth2 verwendet).

Aber der Facebook Login unterstützt OpenID Connect nicht. Es hat seine eigene Variante von OAuth2.

### OpenID (nicht „OpenID Connect“) { #openid-not-openid-connect }

Es gab auch eine „OpenID“-Spezifikation. Sie versuchte das Gleiche zu lösen wie **OpenID Connect**, basierte aber nicht auf OAuth2.

Es handelte sich also um ein komplett zusätzliches System.

Heutzutage ist es nicht sehr populär und wird kaum verwendet.

## OpenAPI { #openapi }

OpenAPI (früher bekannt als Swagger) ist die offene Spezifikation zum Erstellen von APIs (jetzt Teil der Linux Foundation).

**FastAPI** basiert auf **OpenAPI**.

Das ist es, was erlaubt, mehrere automatische interaktive Dokumentations-Oberflächen, Codegenerierung, usw. zu haben.

OpenAPI bietet die Möglichkeit, mehrere Sicherheits„systeme“ zu definieren.

Durch deren Verwendung können Sie alle diese Standards-basierten Tools nutzen, einschließlich dieser interaktiven Dokumentationssysteme.

OpenAPI definiert die folgenden Sicherheitsschemas:

* `apiKey`: ein anwendungsspezifischer Schlüssel, der stammen kann von:
    * Einem Query-Parameter.
    * Einem Header.
    * Einem Cookie.
* `http`: Standard-HTTP-Authentifizierungssysteme, einschließlich:
    * `bearer`: ein Header `Authorization` mit dem Wert `Bearer ` plus einem Token. Dies wird von OAuth2 geerbt.
    * HTTP Basic Authentication.
    * HTTP Digest, usw.
* `oauth2`: Alle OAuth2-Methoden zum Umgang mit Sicherheit (genannt „Flows“).
    * Mehrere dieser Flows eignen sich zum Aufbau eines OAuth 2.0-Authentifizierungsanbieters (wie Google, Facebook, X (Twitter), GitHub usw.):
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * Es gibt jedoch einen bestimmten „Flow“, der perfekt für die direkte Abwicklung der Authentifizierung in derselben Anwendung verwendet werden kann:
        * `password`: Einige der nächsten Kapitel werden Beispiele dafür behandeln.
* `openIdConnect`: bietet eine Möglichkeit, zu definieren, wie OAuth2-Authentifizierungsdaten automatisch ermittelt werden können.
    * Diese automatische Erkennung ist es, die in der OpenID Connect Spezifikation definiert ist.


/// tip | Tipp

Auch die Integration anderer Authentifizierungs-/Autorisierungsanbieter wie Google, Facebook, X (Twitter), GitHub, usw. ist möglich und relativ einfach.

Das komplexeste Problem besteht darin, einen Authentifizierungs-/Autorisierungsanbieter wie solche aufzubauen, aber **FastAPI** reicht Ihnen die Tools, das einfach zu erledigen, während Ihnen die schwere Arbeit abgenommen wird.

///

## **FastAPI** Tools { #fastapi-utilities }

FastAPI stellt für jedes dieser Sicherheitsschemas im Modul `fastapi.security` verschiedene Tools bereit, die die Verwendung dieser Sicherheitsmechanismen vereinfachen.

In den nächsten Kapiteln erfahren Sie, wie Sie mit diesen von **FastAPI** bereitgestellten Tools Sicherheit zu Ihrer API hinzufügen.

Und Sie werden auch sehen, wie dies automatisch in das interaktive Dokumentationssystem integriert wird.
