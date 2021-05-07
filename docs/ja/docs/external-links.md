# 外部リンク・記事

**FastAPI**には、絶えず成長している素晴らしいコミュニティがあります。

**FastAPI**に関連する投稿、記事、ツール、およびプロジェクトは多数あります。

それらの不完全なリストを以下に示します。

!!! tip "豆知識"
    ここにまだ載っていない**FastAPI**に関連する記事、プロジェクト、ツールなどがある場合は、 <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">プルリクエストして下さい</a>。

## 記事

### 英語

{% if external_links %}
{% for article in external_links.articles.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### 日本語

{% if external_links %}
{% for article in external_links.articles.japanese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### ベトナム語

{% if external_links %}
{% for article in external_links.articles.vietnamese %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### ロシア語

{% if external_links %}
{% for article in external_links.articles.russian %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

### ドイツ語

{% if external_links %}
{% for article in external_links.articles.german %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## ポッドキャスト

{% if external_links %}
{% for article in external_links.podcasts.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## トーク

{% if external_links %}
{% for article in external_links.talks.english %}

* <a href="{{ article.link }}" class="external-link" target="_blank">{{ article.title }}</a> by <a href="{{ article.author_link }}" class="external-link" target="_blank">{{ article.author }}</a>.
{% endfor %}
{% endif %}

## プロジェクト

`fastapi`トピックの最新のGitHubプロジェクト:

<div class="github-topic-projects">
</div>
