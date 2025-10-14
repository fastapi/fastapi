# Geschichte, Design und Zukunft { #history-design-and-future }

Vor einiger Zeit fragte <a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">ein **FastAPI**-Benutzer</a>:

> Was ist die Geschichte dieses Projekts? Es scheint aus dem Nichts in ein paar Wochen zu etwas Großartigem geworden zu sein [...]

Hier ist ein wenig über diese Geschichte.

## Alternativen { #alternatives }

Ich habe seit mehreren Jahren APIs mit komplexen Anforderungen (maschinelles Lernen, verteilte Systeme, asynchrone Jobs, NoSQL-Datenbanken, usw.) erstellt und leitete mehrere Entwicklerteams.

Dabei musste ich viele Alternativen untersuchen, testen und nutzen.

Die Geschichte von **FastAPI** ist zu einem großen Teil die Geschichte seiner Vorgänger.

Wie im Abschnitt [Alternativen](alternatives.md){.internal-link target=_blank} gesagt:

<blockquote markdown="1">

**FastAPI** würde ohne die frühere Arbeit anderer nicht existieren.

Es wurden zuvor viele Tools entwickelt, die als Inspiration für seine Entwicklung dienten.

Ich habe die Schaffung eines neuen Frameworks viele Jahre lang vermieden. Zuerst habe ich versucht, alle von **FastAPI** abgedeckten Funktionen mithilfe vieler verschiedener Frameworks, Plugins und Tools zu lösen.

Aber irgendwann gab es keine andere Möglichkeit, als etwas zu schaffen, das all diese Funktionen bereitstellte, die besten Ideen früherer Tools aufnahm und diese auf die bestmögliche Weise kombinierte, wobei Sprachfunktionen verwendet wurden, die vorher noch nicht einmal verfügbar waren (Python 3.6+ Typhinweise).

</blockquote>

## Untersuchung { #investigation }

Durch die Nutzung all dieser vorherigen Alternativen hatte ich die Möglichkeit, von allen zu lernen, Ideen aufzunehmen und sie auf die beste Weise zu kombinieren, die ich für mich und die Entwicklerteams, mit denen ich zusammengearbeitet habe, finden konnte.

Es war beispielsweise klar, dass es idealerweise auf Standard-Python-Typhinweisen basieren sollte.

Der beste Ansatz bestand außerdem darin, bereits bestehende Standards zu nutzen.

Bevor ich also überhaupt angefangen habe, **FastAPI** zu schreiben, habe ich mehrere Monate damit verbracht, die Spezifikationen für OpenAPI, JSON Schema, OAuth2, usw. zu studieren und deren Beziehungen, Überschneidungen und Unterschiede zu verstehen.

## Design { #design }

Dann habe ich einige Zeit damit verbracht, die Entwickler-„API“ zu entwerfen, die ich als Benutzer haben wollte (als Entwickler, welcher FastAPI verwendet).

Ich habe mehrere Ideen in den beliebtesten Python-Editoren getestet: PyCharm, VS Code, Jedi-basierte Editoren.

Laut der letzten <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python-Entwickler-Umfrage</a> deckt das etwa 80 % der Benutzer ab.

Das bedeutet, dass **FastAPI** speziell mit den Editoren getestet wurde, die von 80 % der Python-Entwickler verwendet werden. Und da die meisten anderen Editoren in der Regel ähnlich funktionieren, sollten alle diese Vorteile für praktisch alle Editoren funktionieren.

Auf diese Weise konnte ich die besten Möglichkeiten finden, die Codeverdoppelung so weit wie möglich zu reduzieren, überall Autovervollständigung, Typ- und Fehlerprüfungen, usw. zu gewährleisten.

Alles auf eine Weise, die allen Entwicklern das beste Entwicklungserlebnis bot.

## Anforderungen { #requirements }

Nachdem ich mehrere Alternativen getestet hatte, entschied ich, dass ich <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a> wegen seiner Vorteile verwenden würde.

Dann habe ich zu dessen Code beigetragen, um es vollständig mit JSON Schema kompatibel zu machen, und so verschiedene Möglichkeiten zum Definieren von einschränkenden Deklarationen (Constraints) zu unterstützen, und die Editorunterstützung (Typprüfungen, Codevervollständigung) zu verbessern, basierend auf den Tests in mehreren Editoren.

Während der Entwicklung habe ich auch zu <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a> beigetragen, der anderen Schlüsselanforderung.

## Entwicklung { #development }

Als ich mit der Erstellung von **FastAPI** selbst begann, waren die meisten Teile bereits vorhanden, das Design definiert, die Anforderungen und Tools bereit und das Wissen über die Standards und Spezifikationen klar und frisch.

## Zukunft { #future }

Zu diesem Zeitpunkt ist bereits klar, dass **FastAPI** mit seinen Ideen für viele Menschen nützlich ist.

Es wird gegenüber früheren Alternativen gewählt, da es für viele Anwendungsfälle besser geeignet ist.

Viele Entwickler und Teams verlassen sich bei ihren Projekten bereits auf **FastAPI** (einschließlich mir und meinem Team).

Dennoch stehen uns noch viele Verbesserungen und Funktionen bevor.

**FastAPI** hat eine große Zukunft vor sich.

Und [Ihre Hilfe](help-fastapi.md){.internal-link target=_blank} wird sehr geschätzt.
