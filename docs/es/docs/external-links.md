# Links Adicionales y Artículos

**FastAPI** tiene una gran comunidad que esta en constante crecimiento.

Existen muchas publicaciones, artículos, herramientas y proyectos, relacionados con **FastAPI**.

Aquí tenemos una lista, incompleta, de algunos de ellos.

!!! tip
    Si tienes un artículo, proyecto, herramienta, o cualquier otra cosa relacionada con **FastAPI**, que no este listado aquí, no dudes en añadirla creando un <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request</a>.

## Artículos

### Ingles

{% if external_links %}
{% for article in external_links.articles.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Japones

{% if external_links %}
{% for article in external_links.articles.japanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Vietnamita

{% if external_links %}
{% for article in external_links.articles.vietnamese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Ruso

{% if external_links %}
{% for article in external_links.articles.russian %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Aleman

{% if external_links %}
{% for article in external_links.articles.german %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Podcasts

{% if external_links %}
{% for article in external_links.podcasts.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Charlas

{% if external_links %}
{% for article in external_links.talks.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> por <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Proyectos

Ultimos proyectos en GitHub con el tema `fastapi`:

<div class="github-topic-projects">
</div>
