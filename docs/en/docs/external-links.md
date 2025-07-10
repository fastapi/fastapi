# External Links and Articles

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

Here's an incomplete list of some of them.

/// tip

If you have an article, project, tool, or anything related to **FastAPI** that is not yet listed here, create a <a href="https://github.com/fastapi/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request adding it</a>.

///

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## GitHub Repositories

Most starred GitHub repositories with the topic `fastapi`:

{% for repo in topic_repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
