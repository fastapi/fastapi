# Externe Links und Artikel

**FastAPI** hat eine großartige Community, die ständig wächst.

Es gibt viele Beiträge, Artikel, Tools und Projekte zum Thema **FastAPI**.

Hier ist eine unvollständige Liste einiger davon.

!!! tip "Tipp"
    Wenn Sie einen Artikel, ein Projekt, ein Tool oder irgendetwas im Zusammenhang mit **FastAPI** haben, was hier noch nicht aufgeführt ist, erstellen Sie einen <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request und fügen Sie es hinzu</a>.

!!! note "Hinweis Deutsche Übersetzung"
    Die folgenden Überschriften und Links werden aus einer <a href="https://github.com/tiangolo/fastapi/blob/master/docs/en/data/external_links.yml" class="external-link" target="_blank">anderen Datei</a> gelesen und sind daher nicht ins Deutsche übersetzt.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Projekte

Die neuesten GitHub-Projekte zum Thema `fastapi`:

<div class="github-topic-projects">
</div>
