# Enlaces Externos y Artículos

**FastAPI** tiene una gran comunidad en constante crecimiento.

Hay muchas publicaciones, artículos, herramientas y proyectos relacionados con **FastAPI**.

Aquí hay una lista incompleta de algunos de ellos.

!!! tip "Consejo"
    Si tienes un artículo, proyecto, herramienta o cualquier cosa relacionada con **FastAPI** que aún no aparece aquí, crea un <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request agregándolo</a>.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Projects

Últimos proyectos de GitHub con el tema `fastapi`:

<div class="github-topic-projects">
</div>
