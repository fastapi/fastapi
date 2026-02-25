# External Links

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

You could easily use a search engine or video platform to find many resources related to FastAPI.

/// info

Before, this page used to list links to external articles.

But now that FastAPI is the backend framework with the most GitHub stars across languages, and the most starred and used framework in Python, it no longer makes sense to attempt to list all articles written about it.

///

## GitHub Repositories

Most starred <a href="https://github.com/topics/fastapi" class="external-link" target="_blank">GitHub repositories with the topic `fastapi`</a>:

{% for repo in topic_repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
