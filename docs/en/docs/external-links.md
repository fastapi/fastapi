# External Links and Articles

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

Here's an incomplete list of some of them.

!!! tip
    If you have an article, project, tool, or anything related to **FastAPI** that is not yet listed here, create a <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external-links.yml" class="external-link" target="_blank">Pull Request adding it</a>.

## Articles

### English

{% for article in external_links.articles.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

### Japanese

{% for article in external_links.articles.japanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

### Vietnamese

{% for article in external_links.articles.vietnamese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

### Russian

{% for article in external_links.articles.russian %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

### German

{% for article in external_links.articles.german %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

## Podcasts

{% for article in external_links.podcasts.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

## Talks

{% for article in external_links.talks.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}

## Projects

Latest GitHub projects with the topic `fastapi`:

<div class="github-topic-projects">
</div>
