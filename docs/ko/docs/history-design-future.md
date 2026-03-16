# 역사, 디자인 그리고 미래 { #history-design-and-future }

얼마 전, <a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">한 **FastAPI** 사용자가 이렇게 물었습니다</a>:

> 이 프로젝트의 역사는 무엇인가요? 몇 주 만에 아무 데서도 갑자기 나타나 엄청나게 좋아진 것처럼 보이네요 [...]

여기서 그 역사에 대해 간단히 설명하겠습니다.

## 대안 { #alternatives }

저는 여러 해 동안 복잡한 요구사항(머신러닝, 분산 시스템, 비동기 작업, NoSQL 데이터베이스 등)을 가진 API를 만들면서 여러 개발 팀을 이끌어 왔습니다.

그 과정에서 많은 대안을 조사하고, 테스트하고, 사용해야 했습니다.

**FastAPI**의 역사는 상당 부분 그 이전에 있던 도구들의 역사입니다.

[대안](alternatives.md){.internal-link target=_blank} 섹션에서 언급된 것처럼:

<blockquote markdown="1">

**FastAPI**는 다른 사람들이 이전에 해온 작업이 없었다면 존재하지 않았을 것입니다.

그 전에 만들어진 많은 도구들이 이것의 탄생에 영감을 주었습니다.

저는 여러 해 동안 새로운 프레임워크를 만드는 것을 피하고 있었습니다. 처음에는 **FastAPI**가 다루는 모든 기능을 여러 다른 프레임워크, 플러그인, 도구들을 사용해 해결하려고 했습니다.

하지만 어느 시점에는, 이전 도구들의 최고의 아이디어를 가져와 가능한 한 최선의 방식으로 조합하고, 이전에는 존재하지 않았던 언어 기능(Python 3.6+ type hints)을 사용해 이 모든 기능을 제공하는 무언가를 만드는 것 외에는 다른 선택지가 없었습니다.

</blockquote>

## 조사 { #investigation }

이전의 모든 대안을 사용해 보면서, 각 도구로부터 배울 기회를 얻었고, 아이디어를 가져와 제가 일해온 개발 팀들과 저 자신에게 가장 적합하다고 찾은 방식으로 조합할 수 있었습니다.

예를 들어, 이상적으로는 표준 Python 타입 힌트에 기반해야 한다는 점이 분명했습니다.

또한, 가장 좋은 접근법은 이미 존재하는 표준을 사용하는 것이었습니다.

그래서 **FastAPI**의 코딩을 시작하기도 전에, OpenAPI, JSON Schema, OAuth2 등과 같은 명세를 몇 달 동안 공부했습니다. 이들의 관계, 겹치는 부분, 차이점을 이해하기 위해서였습니다.

## 디자인 { #design }

그 다음에는 (FastAPI를 사용하는 개발자로서) 사용자로서 갖고 싶었던 개발자 "API"를 디자인하는 데 시간을 썼습니다.

가장 인기 있는 Python 편집기들: PyCharm, VS Code, Jedi 기반 편집기에서 여러 아이디어를 테스트했습니다.

약 80%의 사용자를 포함하는 최근 <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python Developer Survey</a>에 따르면 그렇습니다.

즉, **FastAPI**는 Python 개발자의 80%가 사용하는 편집기들로 특별히 테스트되었습니다. 그리고 대부분의 다른 편집기도 유사하게 동작하는 경향이 있으므로, 그 모든 이점은 사실상 모든 편집기에서 동작해야 합니다.

그렇게 해서 코드 중복을 가능한 한 많이 줄이고, 어디서나 자동 완성, 타입 및 에러 검사 등을 제공하는 최선의 방법을 찾을 수 있었습니다.

모든 개발자에게 최고의 개발 경험을 제공하는 방식으로 말입니다.

## 필요조건 { #requirements }

여러 대안을 테스트한 후, 장점 때문에 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a>을 사용하기로 결정했습니다.

그 후, JSON Schema를 완전히 준수하도록 하고, 제약 조건 선언을 정의하는 다양한 방식을 지원하며, 여러 편집기에서의 테스트를 바탕으로 편집기 지원(타입 검사, 자동 완성)을 개선하기 위해 기여했습니다.

개발 과정에서, 또 다른 핵심 필요조건인 <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a>에도 기여했습니다.

## 개발 { #development }

**FastAPI** 자체를 만들기 시작했을 때쯤에는, 대부분의 조각들이 이미 갖춰져 있었고, 디자인은 정의되어 있었으며, 필요조건과 도구는 준비되어 있었고, 표준과 명세에 대한 지식도 명확하고 최신 상태였습니다.

## 미래 { #future }

이 시점에는, **FastAPI**가 그 아이디어와 함께 많은 사람들에게 유용하다는 것이 이미 분명합니다.

많은 사용 사례에 더 잘 맞기 때문에 이전 대안들보다 선택되고 있습니다.

많은 개발자와 팀이 이미 자신의 프로젝트를 위해 **FastAPI**에 의존하고 있습니다(저와 제 팀도 포함해서요).

하지만 여전히, 앞으로 나올 개선 사항과 기능들이 많이 있습니다.

**FastAPI**의 미래는 밝습니다.

그리고 [여러분의 도움](help-fastapi.md){.internal-link target=_blank}은 큰 힘이 됩니다.
