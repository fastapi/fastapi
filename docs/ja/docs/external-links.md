# 外部リンク・記事

**FastAPI**には、絶えず成長している素晴らしいコミュニティがあります。

**FastAPI**に関連する投稿、記事、ツール、およびプロジェクトは多数あります。

それらの不完全なリストを以下に示します。

!!! tip "豆知識"
    ここにまだ載っていない**FastAPI**に関連する記事、プロジェクト、ツールなどがある場合は、 <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">プルリクエストして下さい</a>。

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## プロジェクト

`fastapi`トピックの最新のGitHubプロジェクト:

<div class="github-topic-projects">
</div>
