# Virtuelle Umgebungen { #virtual-environments }

Wenn Sie mit Python-Projekten arbeiten, sollten Sie eine **virtuelle Umgebung** verwenden, um die für jedes Projekt installierten Packages zu isolieren.

Für FastAPI-Projekte empfehle ich die Verwendung von [uv](https://docs.astral.sh/uv/), um das Projekt, seine Abhängigkeiten und seine virtuelle Umgebung zu verwalten.

## Ein Projekt erstellen { #create-a-project }

Installieren Sie `uv` mithilfe der [offiziellen Installationsanleitung](https://docs.astral.sh/uv/getting-started/installation/) und erstellen Sie dann ein Projekt:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` erstellt automatisch eine virtuelle Umgebung für das Projekt. Sie müssen selbst keine erstellen oder aktivieren.

Führen Sie Befehle innerhalb der Projektumgebung mit `uv run` aus, zum Beispiel:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## Mehr erfahren { #learn-more }

Lesen Sie den [Leitfaden zu virtuellen Umgebungen](https://tiangolo.com/guides/virtual-environments/), um zu erfahren, wie virtuelle Umgebungen unter der Haube funktionieren, einschließlich Aktivierung und dem alternativen `python -m venv`- und `pip`-Workflow.
