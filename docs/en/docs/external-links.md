# External Links

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

You could easily use a search engine or video platform to find many resources related to FastAPI.

/// info

Before, this page used to list links to external articles.

But now that FastAPI is the most starred backend framework across languages and one of the most widely used Python frameworks, listing every article written about it no longer makes sense.

///

## GitHub Repositories

Most starred [GitHub repositories with the topic `fastapi`](https://github.com/topics/fastapi):

{% for repo in topic_repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
