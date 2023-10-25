# Links externos e Artigos

**FastAPI** tem uma grande comunidade em crescimento constante.

Existem muitas postagens, artigos, ferramentas e projetos relacionados ao **FastAPI**.

Aqui tem uma lista, incompleta, de algumas delas.

!!! tip "Dica"
    Se você tem um artigo, projeto, ferramenta ou qualquer coisa relacionada ao **FastAPI** que ainda não está listada aqui, crie um <a href="https://github.com/tiangolo/fastapi/edit/master/docs/external-links.md" class="external-link" target="_blank">_Pull Request_ adicionando ele</a>.

{% for section_name, section_content in external_links.items() %}

## {{ section_name }}

{% for lang_name, lang_content in section_content.items() %}

### {{ lang_name }}

{% for item in lang_content %}

* <a href="{{ item.link }}" class="external-link" target="_blank">{{ item.title }}</a> by <a href="{{ item.author_link }}" class="external-link" target="_blank">{{ item.author }}</a>.

{% endfor %}
{% endfor %}
{% endfor %}

## Projetos

Últimos projetos no GitHub com o tópico `fastapi`:

<div class="github-topic-projects">
</div>
