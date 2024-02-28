# Xarici Linklər və Məqalələr

"**FastAPI**"ın daimi olaraq böyüyən böyük bir icması var.

"**FastAPI**"a aid bir çox postlar, məqalələr, alətlər və proyektlər var.

Burada onların tam olmayan siyahısı var.

!!! ipucu
    Əgər "**FastAPI**"a aid bir məqalə, proyekt, alət və ya başqa bir şey varsa, amma hələ də burada yoxdursa, onu əlavə etmək üçün <a href="https://github.com/tiangolo/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">Pull Request yaradın</a>.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Proyektlər

GitHub-da `fastapi` mövzusu ilə bağlı ən son proyektlər:

<div class="github-topic-projects">
</div>
