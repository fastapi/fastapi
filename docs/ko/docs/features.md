# 특징

## FastAPI 특징

**FastAPI**는 다음과 같은 기능들을 제공합니다.

### 개방형 표준(Open standards) 기반

- <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>는 <abbr title="endpoints, routes 등">path</abbr> <abbr title="POST, GET, PUT, DELETE 와 같은 HTTP 메소드들">operations</abbr>, 파라미터, body requests, 보안 등을 포함한 다양한 API 생성에 대한 표준입니다.
- Automatic data model documentation with <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (OpenAPI 자체도 JSON Schema 기반이므로).
- 이러한 표준들은 철저한 연구를 바탕으로 설계되었습니다.
- 그리고 다양한 언어에서 **클라이언트 코드를 자동으로 생성**하는 것도 가능하게 합니다.

### 문서 자동화

프레임워크가 OpenAPI에 기반하고 있기 때문에, 여러 선택지가 있습니다. 기본적으로 Interactive API 문서와 웹 유저 인터페이스 정리가 기본적으로 제공됩니다.

- 대화형 API 문서로는 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>를 사용합니다. 브라우저에서 API를 직접 호출하고 테스트할 수 있습니다.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- 다른 API 문서로는 <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>이 제공됩니다.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Just Modern Python

이 모든 게 (Pydantic 덕분에) **Python 3.6의 타입** 표준 정의을 기반으로 합니다. 새로 배울 구문도 없습니다. 그저 Modern Python 표준입니다.

Python 타입에 대해서 잘 모른다면 (FastAPI을 안 쓰더라도), 여기 짧은 튜토리얼을 확인해보세요: [Python Types](python-types.md){.internal-link target=\_blank}.

Python 타입을 사용해서 아래처럼 작성할 수 있습니다:

```Python
from datetime import date

from pydantic import BaseModel

# 변수를 str형으로 받겠다고 선언하면
# 이제 에디터는 함수 내부의 변수도 타입을 알 수 있습니다
def main(user_id: str):
    return user_id


# Pydantic 모델
class User(BaseModel):
    id: int
    name: str
    joined: date
```

이제 이렇게 사용할 수 있습니다:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info "정보"
    `**second_user_data` 는 의미하는 것은 이렇습니다.

    `second_user_data` 딕셔너리(dict) 내의 모든 키(key)와 값(value)들을 key-value 형태의 파라미터로 전부 넘긴다는 뜻입니다. 즉, `User(id=4, name="Mary", joined="2018-11-30")` 와 같은 코드가 됩니다.

### 에디터 지원

모든 프레임워크는 사용하기 쉽고 직관적으로 사용할 수 있도록 설계되었습니다. 그리고 모든 내용은 개발을 시작하기 전에 여러 에디터에서 테스트된 최고의 개발 경험을 보장받을 수 있도록 결정되었습니다.

최근 파이썬 개발자 설문에서, <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">가장 많이 사용하는 기능은 "자동완성"</a>이었습니다.

**FastAPI** 프레임워크 전체에서 이걸 만족합니다. 어디서든 자동완성 할 수 있습니다.

문서를 보러 오는 일이 거의 없을겁니다.

에디터별로 어떻게 지원하는 지는 아래를 참고하세요.

- <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

- <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

전에는 안될거라고 생각했던 코드도 자동 완성을 할 수 있습니다. 예를 들면, JSON body 안의 (중첩되어 있을 수도 있는) `price`라는 키는 Request로 넘어온 객체 내에 있지만 자동 완성을 지원합니다.

이젠 이름을 잘못 적지 마세요. `username`인지 `user_name`인지 몰라서, 문서를 왔다 갔다 할 일도 스크롤을 위아래로 훑을 필요도 없습니다.

### 요약

모든 것이 합리적인 **기본값**을 갖고 있고, 어디든 원하면 설정할 수도 있습니다. 모든 파라미터는 하고 싶은 것에 따라, 원하는 API 정의에 따라 입맛에 맞게 바꿀 수 있습니다.

기본적으로, 전부 **"그냥 되거든요"**.

### 검증

- 아래를 포함한, 거의 대부분의 파이썬 **데이터 타입**에 대한 검증을 지원합니다.
  - JSON objects (`dict`).
  - JSON array (`list`) defining item types.
  - String (`str`) fields, defining min and max lengths.
  - Numbers (`int`, `float`) with min and max values, etc.

- 아래와 같은, 외부적인 타입들의 검증도 지원합니다.
  - URL
  - Email
  - UUID
  - 그 외

모든 검증은 견고하게 잘 설계된 **Pydantic**으로 처리합니다.

### 보안과 인증

데이터베이스나 데이터 모델과 관계 없이, 보안과 인증을 통합합니다.

OpenAPI에 정의된 보안 스키마들은 다음과 같습니다:

- HTTP Basic.
- **OAuth2** (**JWT tokens** 포함). [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=\_blank} 문서를 확인하세요.
- API keys in:
  - 헤더(Headers)
  - 쿼리 매개변수(Query parameters)
  - 쿠키(Cookies) 등

그리고 모든 보안 기능들은 Starlette 기반입니다. (**세션 쿠키** 포함).

빌드된 모든 재사용 가능한 툴과 컴포넌트들은 시스템이나 데이터 저장소, 관계형 데이터베이스, NoSQL 데이터베이스 등과도 연동하기 쉽습니다.

### 의존성 주입(Dependency Injection)

FastAPI는 매우 사용하기 쉽고 매우 강력한 <abbr title='"컴포넌트", "리소스", "서비스", "providers" 등으로 알려진'><strong>의존성 주입(Dependency Injection)</strong></abbr> 시스템을 갖고 있습니다.

- 의존성이 다른 의존성을 갖고 있다면, 의존성 계층 구조나 **의존성 "그래프"** 를 만듭니다.
- 프레임워크에서 전부 **자동으로 처리**됩니다.
- All the dependencies can require data from requests and **augment the path operation** constraints and automatic documentation.
- **자동 검증**은 _path operation_ 파라미터에도 의존성을 정의할 수 있습니다.
- 복잡한 유저 인증 시스템, **데이터베이스 연결** 등 지원
- 데이터베이스, 프론트엔드 등을 **신경 쓸 필요가 없습니다.** 하지만 통합은 무척 쉽습니다.

### 무한한 "플러그인"

다르게 말하면, 플러그인이라고 할 게 필요가 없습니다. 필요한 코드를 불러와서 사용하세요.

모든 의존성을 고려하면서 통합하기 쉽도록 고안되었습니다. *path operations*에 작성한 것과 동일한 구조와 구문으로 짠 2줄짜리 코드로도 "플러그인"을 만들 수 있습니다.

### 테스트

- 100% <abbr title="자동으로 테스트 된 코드의 규모">test coverage</abbr>.
- 100% <abbr title="Python type annotations, with this your editor and external tools can give you better support">type annotated</abbr> code base.
- 실제로 배포해서 사용해봤음.

## Starlette features

**FastAPI**는 <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>를 완전히 호환하고, 그 기반이기도 합니다. 그래서 가지고 있던 Starlette 코드를 추가해도 잘 동작할 것입니다.

`FastAPI` 는 실제로 `Starlette`의 서브 클래스입니다. 그래서 이미 Starlette를 알고 있거나 써봤다면, 대부분의 기능은 같은 방식으로 동작할 것입니다.

**FastAPI**에서는 **Starlette**의 모든 기능을 그대로 사용하실 수 있습니다. (FastAPI는 Starlette의 상위 호환이기 때문입니다.)

- 매우 엄청난 성능. <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS**, **Go**만큼 가장 빠른 파이썬 프레임워크 중 하나</a>.
- **WebSocket** 지원.
- 백그라운드에서 처리하는 작업들.
- 시작과 종료 이벤트들.
- Test client built on `requests`.
- **CORS**, GZip, 정적 파일들, Streaming responses.
- **세션과 쿠키** 지원.
- 100% test coverage.
- 100% type annotated codebase.

## Pydantic features

**FastAPI**는 <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>를 완전히 호환하고, 그 기반이기도 합니다. 그래서 가지고 있던 Pydantic 코드를 추가해도 잘 동작할 것입니다.

데이터베이스 관련 <abbr title="Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr> 등의 Pydantic 기반의 외부 라이브러리들도 마찬가지로 호환됩니다.

모든 게 자동적으로 검증되기 때문에, request로 받은 객체를 그대로 **데이터베이스로 직접** 넘기는 등의 상황도 가능하다는 의미입니다.

반대의 경우도 그대로 적용할 수 있습니다. 데이터베이스에서 꺼낸 객체를 그대로 **클라이언트에 직접** 전달할 수도 있습니다.

**FastAPI**에서는 **Pydantic**의 모든 기능을 그대로 사용하실 수 있습니다. (FastAPI는 모든 데이터 처리를 Pydantic 기반으로 하고 있기 때문입니다.)

- **머리 깨지는 일은 이제 그만**:
  - 새로 배워야 할 자잘한 schema 정의가 없습니다.
  - 파이썬 타입에 대해서 안다면, Pydantic를 충분히 쓸 수 있습니다.
- **<abbr title="코드 편집기와 비슷한 통합 환경 개발 툴">IDE</abbr>, <abbr title="코드의 에러를 체크해주는 프로그램">linter</abbr>, 그리도 당신의 두뇌**를 잘 활용하세요:
  - Pydantic의 자료 구조는 여러분이 정의한 클래스의 인스턴스들뿐입니다. 자동 완성, 문법 검사, <abbr title="역. 파이썬의 정적 타입 검사 도구">mypy</abbr> 그리고 여러분의 직감은 검증된 데이터와 잘 돌아갈 겁니다.
- **빠르다**:
  - <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">벤치마킹</a>에서 Pydantic이 다른 라이브러리들보다 빠르단 것을 확인했습니다.
- **복잡한 구조** 검증:
  - 계층적인 Pydantic 모델, 파이썬의 `typing`에 있는 `List` and `Dict` 등을 사용하세요.
  - Validator는 복잡한 데이터 스키마들을 간단하고 쉽게 정의하고 검사할 수 있게, 그리고 JSON 스키마로 문서화까지 할 수 있게 해줍니다.
  - 깊이가 깊은 **Nested JSON** 객체도 사용할 수 있습니다. 전부 검증되고 주석이 달린 채로요.
- **확장성**:
  - Pydantic은 커스텀 데이터 타입들을 정의할 수 있게 만듭니다. 아니면, 모델에 validator decorator를 데코레이트(decorate)한 후, 함수를 작성해서 validation을 확장할 수도 있습니다.
- 100% test coverage.
