# 외부 링크와 기사

**FastAPI**는 빠르게 성장하는 커뮤니티를 가지고 있습니다.

그곳에는 **FastAPI**와 관련된 많은 게시물, 기사, 도구, 프로젝트가 있습니다.

다음은 그 중 미완성인 것들에 대해서 입니다.

/// 팁

아직 이 곳에 존재하지 않는 **FastAPI**관련 기사, 프로젝트, 툴 등이 있을 경우, <a href="https://github.com/fastapi/fastapi/edit/master/docs/en/data/external_links.yml" class="external-link" target="_blank">추가하여 풀 리퀘스트를 올려주세요.</a>.

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

## 프로젝트

`fastapi`를 주제로 한 최신 GitHub 프로젝트:

<div class="github-topic-projects">
</div>
