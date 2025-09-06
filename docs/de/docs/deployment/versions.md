# Über FastAPI-Versionen { #about-fastapi-versions }

**FastAPI** wird bereits in vielen Anwendungen und Systemen produktiv eingesetzt. Und die Testabdeckung wird bei 100 % gehalten. Aber seine Entwicklung geht immer noch schnell voran.

Es werden regelmäßig neue Funktionen hinzugefügt, Fehler werden regelmäßig behoben und der Code wird weiterhin kontinuierlich verbessert.

Aus diesem Grund sind die aktuellen Versionen immer noch `0.x.x`, was darauf hindeutet, dass jede Version möglicherweise nicht abwärtskompatible Änderungen haben könnte. Dies folgt den Konventionen der <a href="https://semver.org/" class="external-link" target="_blank">semantischen Versionierung</a>.

Sie können jetzt Produktionsanwendungen mit **FastAPI** erstellen (und das tun Sie wahrscheinlich schon seit einiger Zeit), Sie müssen nur sicherstellen, dass Sie eine Version verwenden, die korrekt mit dem Rest Ihres Codes funktioniert.

## Ihre `fastapi`-Version pinnen { #pin-your-fastapi-version }

Als Erstes sollten Sie die Version von **FastAPI**, die Sie verwenden, an die höchste Version „pinnen“, von der Sie wissen, dass sie für Ihre Anwendung korrekt funktioniert.

Angenommen, Sie verwenden in Ihrer App die Version `0.112.0`.

Wenn Sie eine `requirements.txt`-Datei verwenden, können Sie die Version wie folgt angeben:

```txt
fastapi[standard]==0.112.0
```

Das würde bedeuten, dass Sie genau die Version `0.112.0` verwenden.

Oder Sie können sie auch anpinnen mit:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

Das würde bedeuten, dass Sie eine Version `0.112.0` oder höher verwenden würden, aber kleiner als `0.113.0`, beispielsweise würde eine Version `0.112.2` immer noch akzeptiert.

Wenn Sie zum Verwalten Ihrer Installationen andere Tools wie `uv`, Poetry, Pipenv oder andere verwenden, sie verfügen alle über eine Möglichkeit, bestimmte Versionen für Ihre Packages zu definieren.

## Verfügbare Versionen { #available-versions }

Die verfügbaren Versionen können Sie in den [Versionshinweisen](../release-notes.md){.internal-link target=_blank} einsehen (z. B. um zu überprüfen, welches die neueste Version ist).

## Über Versionen { #about-versions }

Gemäß den Konventionen zur semantischen Versionierung könnte jede Version unter `1.0.0` potenziell nicht abwärtskompatible Änderungen hinzufügen.

FastAPI folgt auch der Konvention, dass jede „PATCH“-Versionsänderung für Bugfixes und abwärtskompatible Änderungen gedacht ist.

/// tip | Tipp

Der „PATCH“ ist die letzte Zahl, zum Beispiel ist in `0.2.3` die PATCH-Version `3`.

///

Sie sollten also in der Lage sein, eine Version wie folgt anzupinnen:

```txt
fastapi>=0.45.0,<0.46.0
```

Nicht abwärtskompatible Änderungen und neue Funktionen werden in „MINOR“-Versionen hinzugefügt.

/// tip | Tipp

„MINOR“ ist die Zahl in der Mitte, zum Beispiel ist in `0.2.3` die MINOR-Version `2`.

///

## Upgrade der FastAPI-Versionen { #upgrading-the-fastapi-versions }

Sie sollten Tests für Ihre App hinzufügen.

Mit **FastAPI** ist das sehr einfach (dank Starlette), schauen Sie sich die Dokumentation an: [Testen](../tutorial/testing.md){.internal-link target=_blank}

Nachdem Sie Tests erstellt haben, können Sie die **FastAPI**-Version auf eine neuere Version aktualisieren und sicherstellen, dass Ihr gesamter Code ordnungsgemäß funktioniert, indem Sie Ihre Tests ausführen.

Wenn alles funktioniert oder nachdem Sie die erforderlichen Änderungen vorgenommen haben und alle Ihre Tests bestehen, können Sie Ihr `fastapi` an die neue aktuelle Version pinnen.

## Über Starlette { #about-starlette }

Sie sollten die Version von `starlette` nicht pinnen.

Verschiedene Versionen von **FastAPI** verwenden eine bestimmte neuere Version von Starlette.

Sie können **FastAPI** also einfach die korrekte Starlette-Version verwenden lassen.

## Über Pydantic { #about-pydantic }

Pydantic integriert die Tests für **FastAPI** in seine eigenen Tests, sodass neue Versionen von Pydantic (über `1.0.0`) immer mit FastAPI kompatibel sind.

Sie können Pydantic an jede für Sie geeignete Version über `1.0.0` anpinnen.

Zum Beispiel:

```txt
pydantic>=2.7.0,<3.0.0
```
