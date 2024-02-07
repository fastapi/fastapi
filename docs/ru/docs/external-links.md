# Внешние ссылки и статьи

**FastAPI** имеет отличное и постоянно растущее сообщество.

Существует множество сообщений, статей, инструментов и проектов, связанных с **FastAPI**.

Вот неполный список некоторых из них.

!!! tip
    Если у вас есть статья, проект, инструмент или что-либо, связанное с **FastAPI**, что еще не перечислено здесь, создайте <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request</a>.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Проекты

Последние GitHub-проекты с пометкой `fastapi`:

<div class="github-topic-projects">
</div>
