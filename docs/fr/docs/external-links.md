# Articles et liens externes

**FastAPI** possède une grande communauté en constante extension.

Il existe de nombreux articles, outils et projets liés à **FastAPI**.

Voici une liste incomplète de certains d'entre eux.

!!! tip "Astuce"
    Si vous avez un article, projet, outil, ou quoi que ce soit lié à **FastAPI** qui n'est actuellement pas listé ici, créez une <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request l'ajoutant</a>.

## Articles

### Anglais

{% if external_links %}
{% for article in external_links.articles.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Japonais

{% if external_links %}
{% for article in external_links.articles.japanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Vietnamien

{% if external_links %}
{% for article in external_links.articles.vietnamese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Russe

{% if external_links %}
{% for article in external_links.articles.russian %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### Allemand

{% if external_links %}
{% for article in external_links.articles.german %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Podcasts

{% if external_links %}
{% for article in external_links.podcasts.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Conférences

{% if external_links %}
{% for article in external_links.talks.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> par <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## Projets

Les projets Github avec le topic `fastapi` les plus récents :

<div class="github-topic-projects">
</div>
