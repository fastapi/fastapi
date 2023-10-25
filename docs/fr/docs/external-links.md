# Articles et liens externes

**FastAPI** possède une grande communauté en constante extension.

Il existe de nombreux articles, outils et projets liés à **FastAPI**.

Voici une liste incomplète de certains d'entre eux.

!!! tip "Astuce"
    Si vous avez un article, projet, outil, ou quoi que ce soit lié à **FastAPI** qui n'est actuellement pas listé ici, créez une <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request l'ajoutant</a>.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Projets

Les projets Github avec le topic `fastapi` les plus récents :

<div class="github-topic-projects">
</div>
