# Unteranwendungen – Mounts

Wenn Sie zwei unabhängige FastAPI-Anwendungen mit deren eigenen unabhängigen OpenAPI und deren eigenen Dokumentationsoberflächen benötigen, können Sie eine Hauptanwendung haben und dann eine (oder mehrere) Unteranwendung(en) „mounten“.

## Mounten einer **FastAPI**-Anwendung

„Mounten“ („Einhängen“) bedeutet das Hinzufügen einer völlig „unabhängigen“ Anwendung an einem bestimmten Pfad, die sich dann um die Handhabung aller unter diesem Pfad liegenden _Pfadoperationen_ kümmert, welche in dieser Unteranwendung deklariert sind.

### Hauptanwendung

Erstellen Sie zunächst die Hauptanwendung **FastAPI** und deren *Pfadoperationen*:

```Python hl_lines="3  6-8"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Unteranwendung

Erstellen Sie dann Ihre Unteranwendung und deren *Pfadoperationen*.

Diese Unteranwendung ist nur eine weitere Standard-FastAPI-Anwendung, aber diese wird „gemountet“:

```Python hl_lines="11  14-16"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Die Unteranwendung mounten

Mounten Sie in Ihrer Top-Level-Anwendung `app` die Unteranwendung `subapi`.

In diesem Fall wird sie im Pfad `/subapi` gemountet:

```Python hl_lines="11  19"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Es in der automatischen API-Dokumentation betrachten

Führen Sie nun `uvicorn` mit der Hauptanwendung aus. Wenn Ihre Datei `main.py` lautet, wäre das:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Und öffnen Sie die Dokumentation unter <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Sie sehen die automatische API-Dokumentation für die Hauptanwendung, welche nur deren eigene _Pfadoperationen_ anzeigt:

<img src="/img/tutorial/sub-applications/image01.png">

Öffnen Sie dann die Dokumentation für die Unteranwendung unter <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Sie sehen die automatische API-Dokumentation für die Unteranwendung, welche nur deren eigene _Pfadoperationen_ anzeigt, alle unter dem korrekten Unterpfad-Präfix `/subapi`:

<img src="/img/tutorial/sub-applications/image02.png">

Wenn Sie versuchen, mit einer der beiden Benutzeroberflächen zu interagieren, funktionieren diese ordnungsgemäß, da der Browser mit jeder spezifischen Anwendung oder Unteranwendung kommunizieren kann.

### Technische Details: `root_path`

Wenn Sie eine Unteranwendung wie oben beschrieben mounten, kümmert sich FastAPI darum, den Mount-Pfad für die Unteranwendung zu kommunizieren, mithilfe eines Mechanismus aus der ASGI-Spezifikation namens `root_path`.

Auf diese Weise weiß die Unteranwendung, dass sie dieses Pfadpräfix für die Benutzeroberfläche der Dokumentation verwenden soll.

Und die Unteranwendung könnte auch ihre eigenen gemounteten Unteranwendungen haben und alles würde korrekt funktionieren, da FastAPI sich um alle diese `root_path`s automatisch kümmert.

Mehr über den `root_path` und dessen explizite Verwendung erfahren Sie im Abschnitt [Hinter einem Proxy](behind-a-proxy.md){.internal-link target=_blank}.
