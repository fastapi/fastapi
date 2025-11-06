# Pfad-Parameter und Validierung von Zahlen { #path-parameters-and-numeric-validations }

So wie Sie mit `Query` für Query-Parameter zusätzliche Validierungen und Metadaten deklarieren können, können Sie mit `Path` die gleichen Validierungen und Metadaten für Pfad-Parameter deklarieren.

## `Path` importieren { #import-path }

Importieren Sie zuerst `Path` von `fastapi`, und importieren Sie `Annotated`:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | Info

FastAPI hat in Version 0.95.0 Unterstützung für `Annotated` hinzugefügt und es zur Verwendung empfohlen.

Wenn Sie eine ältere Version haben, würden Fehler angezeigt werden, wenn Sie versuchen, `Annotated` zu verwenden.

Stellen Sie sicher, dass Sie [FastAPI aktualisieren](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}, auf mindestens Version 0.95.1, bevor Sie `Annotated` verwenden.

///

## Metadaten deklarieren { #declare-metadata }

Sie können dieselben Parameter wie für `Query` deklarieren.

Um zum Beispiel einen `title`-Metadaten-Wert für den Pfad-Parameter `item_id` zu deklarieren, können Sie schreiben:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Hinweis

Ein Pfad-Parameter ist immer erforderlich, da er Teil des Pfads sein muss. Selbst wenn Sie ihn mit `None` deklarieren oder einen Defaultwert setzen, würde das nichts ändern, er wäre dennoch immer erforderlich.

///

## Die Parameter sortieren, wie Sie möchten { #order-the-parameters-as-you-need }

/// tip | Tipp

Das ist wahrscheinlich nicht so wichtig oder notwendig, wenn Sie `Annotated` verwenden.

///

Angenommen, Sie möchten den Query-Parameter `q` als erforderlichen `str` deklarieren.

Und Sie müssen sonst nichts anderes für diesen Parameter deklarieren, Sie brauchen also `Query` nicht wirklich.

Aber Sie müssen dennoch `Path` für den `item_id`-Pfad-Parameter verwenden. Und aus irgendeinem Grund möchten Sie `Annotated` nicht verwenden.

Python wird sich beschweren, wenn Sie einen Wert mit einem „Default“ vor einem Wert ohne „Default“ setzen.

Aber Sie können die Reihenfolge ändern und den Wert ohne Default (den Query-Parameter `q`) zuerst setzen.

Für **FastAPI** spielt es keine Rolle. Es erkennt die Parameter anhand ihrer Namen, Typen und Default-Deklarationen (`Query`, `Path`, usw.), es kümmert sich nicht um die Reihenfolge.

Sie können Ihre Funktion also so deklarieren:

{* ../../docs_src/path_params_numeric_validations/tutorial002.py hl[7] *}

Aber bedenken Sie, dass Sie dieses Problem nicht haben, wenn Sie `Annotated` verwenden, da es nicht darauf ankommt, dass Sie keine Funktionsparameter-Defaultwerte für `Query()` oder `Path()` verwenden.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py *}

## Die Parameter sortieren, wie Sie möchten: Tricks { #order-the-parameters-as-you-need-tricks }

/// tip | Tipp

Das ist wahrscheinlich nicht so wichtig oder notwendig, wenn Sie `Annotated` verwenden.

///

Hier ist ein **kleiner Trick**, der nützlich sein kann, obwohl Sie ihn nicht oft benötigen werden.

Wenn Sie:

* den `q`-Query-Parameter sowohl ohne `Query` als auch ohne Defaultwert deklarieren
* den Pfad-Parameter `item_id` mit `Path` deklarieren
* sie in einer anderen Reihenfolge haben
* nicht `Annotated` verwenden

... möchten, dann hat Python eine kleine Spezial-Syntax dafür.

Übergeben Sie `*`, als den ersten Parameter der Funktion.

Python wird nichts mit diesem `*` machen, aber es wird wissen, dass alle folgenden Parameter als Schlüsselwortargumente (Schlüssel-Wert-Paare) verwendet werden sollen, auch bekannt als <abbr title="Von: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Selbst wenn diese keinen Defaultwert haben.

{* ../../docs_src/path_params_numeric_validations/tutorial003.py hl[7] *}

### Besser mit `Annotated` { #better-with-annotated }

Bedenken Sie, dass Sie, wenn Sie `Annotated` verwenden, da Sie keine Funktionsparameter-Defaultwerte verwenden, dieses Problem nicht haben werden und wahrscheinlich nicht `*` verwenden müssen.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py hl[10] *}

## Validierung von Zahlen: Größer oder gleich { #number-validations-greater-than-or-equal }

Mit `Query` und `Path` (und anderen, die Sie später sehen werden) können Sie Zahlenbeschränkungen deklarieren.

Hier, mit `ge=1`, muss `item_id` eine ganze Zahl sein, die „`g`reater than or `e`qual to“ (größer oder gleich) `1` ist.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py hl[10] *}

## Validierung von Zahlen: Größer und kleiner oder gleich { #number-validations-greater-than-and-less-than-or-equal }

Das Gleiche gilt für:

* `gt`: `g`reater `t`han (größer als)
* `le`: `l`ess than or `e`qual (kleiner oder gleich)

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py hl[10] *}

## Validierung von Zahlen: Floats, größer und kleiner { #number-validations-floats-greater-than-and-less-than }

Zahlenvalidierung funktioniert auch für <abbr title="Fließkommazahlen">`float`</abbr>-Werte.

Hier wird es wichtig, in der Lage zu sein, <abbr title="greater than – größer als"><code>gt</code></abbr> und nicht nur <abbr title="greater than or equal – größer oder gleich"><code>ge</code></abbr> zu deklarieren. Da Sie mit dieser Option erzwingen können, dass ein Wert größer als `0` sein muss, selbst wenn er kleiner als `1` ist.

Also wäre `0.5` ein gültiger Wert. Aber `0.0` oder `0` nicht.

Und das Gleiche gilt für <abbr title="less than – kleiner als"><code>lt</code></abbr>.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py hl[13] *}

## Zusammenfassung { #recap }

Mit `Query`, `Path` (und anderen, die Sie noch nicht gesehen haben) können Sie Metadaten und Stringvalidierungen auf die gleichen Weisen deklarieren wie in [Query-Parameter und Stringvalidierungen](query-params-str-validations.md){.internal-link target=_blank} beschrieben.

Und Sie können auch Zahlenvalidierungen deklarieren:

* `gt`: `g`reater `t`han (größer als)
* `ge`: `g`reater than or `e`qual (größer oder gleich)
* `lt`: `l`ess `t`han (kleiner als)
* `le`: `l`ess than or `e`qual (kleiner oder gleich)

/// info | Info

`Query`, `Path`, und andere Klassen, die Sie später sehen werden, sind Unterklassen einer gemeinsamen `Param`-Klasse.

Alle von ihnen teilen die gleichen Parameter für zusätzliche Validierung und Metadaten, die Sie gesehen haben.

///

/// note | Technische Details

Wenn Sie `Query`, `Path` und andere von `fastapi` importieren, sind sie tatsächlich Funktionen.

Die, wenn sie aufgerufen werden, Instanzen von Klassen mit demselben Namen zurückgeben.

Sie importieren also `Query`, was eine Funktion ist. Und wenn Sie sie aufrufen, gibt sie eine Instanz einer Klasse zurück, die auch `Query` genannt wird.

Diese Funktionen existieren (statt die Klassen direkt zu verwenden), damit Ihr Editor keine Fehlermeldungen über ihre Typen ausgibt.

Auf diese Weise können Sie Ihren normalen Editor und Ihre Programmier-Tools verwenden, ohne besondere Einstellungen vornehmen zu müssen, um diese Fehlermeldungen stummzuschalten.

///
