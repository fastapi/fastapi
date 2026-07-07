---
include_yaml:
  topic_repos: data/topic_repos.yml
---

# 외부 링크

**FastAPI**는 끊임없이 성장하는 훌륭한 커뮤니티를 가지고 있습니다.

**FastAPI**와 관련된 수많은 게시물, 기사, 도구 및 프로젝트들이 있습니다.

검색 엔진이나 동영상 플랫폼을 사용하여 FastAPI와 관련된 많은 리소스들을 쉽게 찾으실 수 있을 것입니다.

/// note | 참고

이전에는 이 페이지에 외부 기사들에 대한 링크들을 나열했었습니다.

하지만 이제 FastAPI가 모든 언어를 통틀어 GitHub에서 가장 많은 별을 받은 백엔드 프레임워크이자, 파이썬에서 가장 많은 별을 받고 널리 쓰이는 프레임워크가 되면서, FastAPI에 대해 쓰인 모든 기사들을 나열하는 것은 더 이상 의미가 없어졌습니다.

///

## GitHub 레포지토리

가장 많은 별을 받은 [`fastapi` 토픽의 GitHub 레포지토리들](https://github.com/topics/fastapi):

{% for repo in topic_repos %}

<a href={{repo.html_url}} target="_blank">★ {{repo.stars}} - {{repo.name}}</a> by <a href={{repo.owner_html_url}} target="_blank">@{{repo.owner_login}}</a>.

{% endfor %}
