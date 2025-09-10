# Zusätzliche Datentypen { #extra-data-types }

Bisher haben Sie gängige Datentypen verwendet, wie zum Beispiel:

* `int`
* `float`
* `str`
* `bool`

Sie können aber auch komplexere Datentypen verwenden.

Und Sie haben immer noch dieselbe Funktionalität wie bisher gesehen:

* Großartige Editor-Unterstützung.
* Datenkonvertierung bei eingehenden <abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr>.
* Datenkonvertierung für <abbr title="Response – Antwort: Daten, die der Server zum anfragenden Client zurücksendet">Response</abbr>-Daten.
* Datenvalidierung.
* Automatische Annotation und Dokumentation.

## Andere Datentypen { #other-data-types }

Hier sind einige der zusätzlichen Datentypen, die Sie verwenden können:

* `UUID`:
    * Ein standardmäßiger „universell eindeutiger Bezeichner“ („Universally Unique Identifier“), der in vielen Datenbanken und Systemen als ID üblich ist.
    * Wird in Requests und Responses als `str` dargestellt.
* `datetime.datetime`:
    * Ein Python-`datetime.datetime`.
    * Wird in Requests und Responses als `str` im ISO 8601-Format dargestellt, etwa: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * Python-`datetime.date`.
    * Wird in Requests und Responses als `str` im ISO 8601-Format dargestellt, etwa: `2008-09-15`.
* `datetime.time`:
    * Ein Python-`datetime.time`.
    * Wird in Requests und Responses als `str` im ISO 8601-Format dargestellt, etwa: `14:23:55.003`.
* `datetime.timedelta`:
    * Ein Python-`datetime.timedelta`.
    * Wird in Requests und Responses als `float` der Gesamtsekunden dargestellt.
    * Pydantic ermöglicht auch die Darstellung als „ISO 8601 Zeitdifferenz-Kodierung“, <a href="https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers" class="external-link" target="_blank">siehe die Dokumentation für weitere Informationen</a>.
* `frozenset`:
    * Wird in Requests und Responses wie ein `set` behandelt:
        * Bei Requests wird eine Liste gelesen, Duplikate entfernt und in ein `set` umgewandelt.
        * Bei Responses wird das `set` in eine `list` umgewandelt.
        * Das generierte Schema zeigt an, dass die `set`-Werte eindeutig sind (unter Verwendung von JSON Schemas `uniqueItems`).
* `bytes`:
    * Standard-Python-`bytes`.
    * In Requests und Responses werden sie als `str` behandelt.
    * Das generierte Schema wird anzeigen, dass es sich um einen `str` mit `binary` „Format“ handelt.
* `Decimal`:
    * Standard-Python-`Decimal`.
    * In Requests und Responses wird es wie ein `float` behandelt.
* Sie können alle gültigen Pydantic-Datentypen hier überprüfen: <a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Pydantic-Datentypen</a>.

## Beispiel { #example }

Hier ist ein Beispiel für eine *Pfadoperation* mit Parametern, die einige der oben genannten Typen verwenden.

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

Beachten Sie, dass die Parameter innerhalb der Funktion ihren natürlichen Datentyp haben und Sie beispielsweise normale Datumsmanipulationen durchführen können, wie zum Beispiel:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
