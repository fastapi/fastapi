# 기능 { #features }

## FastAPI의 기능 { #fastapi-features }

**FastAPI**는 다음과 같은 기능을 제공합니다:

### 개방형 표준을 기반으로 { #based-on-open-standards }

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>: <abbr title="또한 다음으로도 불립니다: 엔드포인트, 라우트">path</abbr> <abbr title="HTTP 메소드(POST, GET, PUT, DELETE 등)로도 알려져 있습니다">operations</abbr>, 매개변수, 요청 본문, 보안 등의 선언을 포함하여 API를 생성합니다.
* <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a>를 사용한 자동 데이터 모델 문서화(OpenAPI 자체가 JSON Schema를 기반으로 하기 때문입니다).
* 단순히 떠올려서 덧붙인 레이어가 아니라, 세심한 검토를 거친 뒤 이러한 표준을 중심으로 설계되었습니다.
* 이는 또한 다양한 언어로 자동 **클라이언트 코드 생성**을 사용할 수 있게 해줍니다.

### 문서 자동화 { #automatic-docs }

대화형 API 문서와 탐색용 웹 사용자 인터페이스를 제공합니다. 프레임워크가 OpenAPI를 기반으로 하기에 여러 옵션이 있으며, 기본으로 2가지가 포함됩니다.

* 대화형 탐색이 가능한 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>로 브라우저에서 직접 API를 호출하고 테스트할 수 있습니다.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>을 이용한 대체 API 문서화.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 그저 현대 파이썬 { #just-modern-python }

( Pydantic 덕분에) 모든 것이 표준 **Python 타입** 선언을 기반으로 합니다. 새로 배울 문법이 없습니다. 그저 표준적인 현대 파이썬입니다.

Python 타입을 어떻게 사용하는지 2분 정도 복습이 필요하다면(FastAPI를 사용하지 않더라도), 다음의 짧은 자습서를 확인하세요: [Python 타입](python-types.md){.internal-link target=_blank}.

여러분은 타입이 있는 표준 Python을 다음과 같이 작성합니다:

```Python
from datetime import date

from pydantic import BaseModel

# 변수를 str로 선언합니다
# 그리고 함수 내부에서 편집기 지원을 받습니다
def main(user_id: str):
    return user_id


# Pydantic 모델
class User(BaseModel):
    id: int
    name: str
    joined: date
```

그 다음 다음과 같이 사용할 수 있습니다:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// info | 정보

`**second_user_data`는 다음을 의미합니다:

`second_user_data` `dict`의 키와 값을 키-값 인자로서 바로 넘겨주는 것으로, 다음과 동일합니다: `User(id=4, name="Mary", joined="2018-11-30")`

///

### 편집기 지원 { #editor-support }

프레임워크 전체는 사용하기 쉽고 직관적으로 설계되었으며, 최고의 개발 경험을 보장하기 위해 개발을 시작하기도 전에 모든 결정은 여러 편집기에서 테스트되었습니다.

Python 개발자 설문조사에서 <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">가장 많이 사용되는 기능 중 하나가 "자동 완성"이라는 점</a>이 분명합니다.

**FastAPI** 프레임워크 전체는 이를 만족하기 위해 만들어졌습니다. 자동 완성은 어디서나 작동합니다.

문서로 다시 돌아올 일은 거의 없을 것입니다.

편집기가 여러분을 어떻게 도와줄 수 있는지 살펴보세요:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>에서:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>에서:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

이전에 불가능하다고 생각했을 코드에서도 자동 완성을 받을 수 있습니다. 예를 들어, 요청에서 전달되는(중첩될 수도 있는) JSON 본문 내부의 `price` 키 같은 경우입니다.

더 이상 잘못된 키 이름을 입력하거나, 문서 사이를 왔다 갔다 하거나, `username`을 썼는지 `user_name`을 썼는지 찾으려고 위아래로 스크롤할 필요가 없습니다.

### 간결함 { #short }

선택적 구성을 어디서나 할 수 있도록 하면서도, 모든 것에 합리적인 **기본값**이 설정되어 있습니다. 모든 매개변수는 필요한 작업을 하거나 필요한 API를 정의하기 위해 미세하게 조정할 수 있습니다.

하지만 기본적으로 모든 것이 **"그냥 작동합니다"**.

### 검증 { #validation }

* 다음을 포함해 대부분(혹은 전부?)의 Python **데이터 타입**에 대한 검증:
    * JSON 객체 (`dict`).
    * 아이템 타입을 정의하는 JSON 배열 (`list`).
    * 최소/최대 길이를 정의하는 문자열(`str`) 필드.
    * 최소/최대 값을 가지는 숫자(`int`, `float`) 등.

* 다음과 같은 좀 더 이색적인 타입에 대한 검증:
    * URL.
    * Email.
    * UUID.
    * ...그 외.

모든 검증은 잘 확립되어 있고 견고한 **Pydantic**이 처리합니다.

### 보안과 인증 { #security-and-authentication }

보안과 인증이 통합되어 있습니다. 데이터베이스나 데이터 모델과 타협하지 않습니다.

다음을 포함해 OpenAPI에 정의된 모든 보안 스키마:

* HTTP Basic.
* **OAuth2**(**JWT tokens** 또한 포함). [JWT를 사용한 OAuth2](tutorial/security/oauth2-jwt.md){.internal-link target=_blank} 자습서를 확인해 보세요.
* 다음에 들어 있는 API 키:
    * 헤더.
    * 쿼리 매개변수.
    * 쿠키 등.

추가로 Starlette의 모든 보안 기능(**세션 쿠키** 포함)도 제공합니다.

모두 재사용 가능한 도구와 컴포넌트로 만들어져 있어, 여러분의 시스템, 데이터 저장소, 관계형 및 NoSQL 데이터베이스 등과 쉽게 통합할 수 있습니다.

### 의존성 주입 { #dependency-injection }

FastAPI는 사용하기 매우 쉽지만, 매우 강력한 <abbr title='또한 다음으로도 불립니다: "컴포넌트", "자원", "서비스", "제공자"'><strong>Dependency Injection</strong></abbr> 시스템을 포함하고 있습니다.

* 의존성도 의존성을 가질 수 있어, 의존성의 계층 또는 **의존성의 "그래프"**를 생성합니다.
* 모든 것이 프레임워크에 의해 **자동으로 처리됩니다**.
* 모든 의존성은 요청에서 데이터를 요구할 수 있으며, **경로 처리** 제약과 자동 문서화를 강화할 수 있습니다.
* 의존성에 정의된 *경로 처리* 매개변수에 대해서도 **자동 검증**을 합니다.
* 복잡한 사용자 인증 시스템, **데이터베이스 연결** 등을 지원합니다.
* 데이터베이스, 프론트엔드 등과 **타협하지 않습니다**. 하지만 모두와 쉽게 통합할 수 있습니다.

### 제한 없는 "플러그인" { #unlimited-plug-ins }

또 다른 방식으로는, 그것들이 필요 없습니다. 필요한 코드를 임포트해서 사용하면 됩니다.

어떤 통합이든(의존성과 함께) 사용하기 매우 간단하도록 설계되어 있어, *경로 처리*에 사용된 것과 동일한 구조와 문법을 사용해 2줄의 코드로 애플리케이션용 "플러그인"을 만들 수 있습니다.

### 테스트됨 { #tested }

* 100% <abbr title="자동으로 테스트되는 코드의 양">test coverage</abbr>.
* 100% <abbr title="Python 타입 어노테이션으로, 이를 통해 편집기와 외부 도구가 더 나은 지원을 제공할 수 있습니다">type annotated</abbr> 코드 베이스.
* 프로덕션 애플리케이션에서 사용됩니다.

## Starlette 기능 { #starlette-features }

**FastAPI**는 <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a>와 완전히 호환되며(또한 이를 기반으로 합니다). 따라서 추가로 가지고 있는 Starlette 코드도 모두 동작합니다.

`FastAPI`는 실제로 `Starlette`의 하위 클래스입니다. 그래서 Starlette을 이미 알고 있거나 사용하고 있다면, 대부분의 기능이 같은 방식으로 동작할 것입니다.

**FastAPI**를 사용하면 **Starlette**의 모든 기능을 얻게 됩니다(FastAPI는 Starlette에 강력한 기능을 더한 것입니다):

* 정말 인상적인 성능. <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS**와 **Go**에 버금가는, 사용 가능한 가장 빠른 Python 프레임워크 중 하나입니다</a>.
* **WebSocket** 지원.
* 프로세스 내 백그라운드 작업.
* 시작 및 종료 이벤트.
* HTTPX 기반 테스트 클라이언트.
* **CORS**, GZip, 정적 파일, 스트리밍 응답.
* **세션과 쿠키** 지원.
* 100% test coverage.
* 100% type annotated codebase.

## Pydantic 기능 { #pydantic-features }

**FastAPI**는 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>과 완벽하게 호환되며(또한 이를 기반으로 합니다). 따라서 추가로 가지고 있는 Pydantic 코드도 모두 동작합니다.

데이터베이스를 위한 <abbr title="Object-Relational Mapper - 객체-관계 매퍼">ORM</abbr>, <abbr title="Object-Document Mapper - 객체-문서 매퍼">ODM</abbr>과 같은, Pydantic을 기반으로 하는 외부 라이브러리도 포함합니다.

이는 모든 것이 자동으로 검증되기 때문에, 많은 경우 요청에서 얻은 동일한 객체를 **직접 데이터베이스로** 넘겨줄 수 있다는 의미이기도 합니다.

반대로도 마찬가지이며, 많은 경우 데이터베이스에서 얻은 객체를 **직접 클라이언트로** 그대로 넘겨줄 수 있습니다.

**FastAPI**를 사용하면(모든 데이터 처리를 위해 FastAPI가 Pydantic을 기반으로 하기에) **Pydantic**의 모든 기능을 얻게 됩니다:

* **No brainfuck**:
    * 새로운 스키마 정의 마이크로 언어를 배울 필요가 없습니다.
    * Python 타입을 알고 있다면 Pydantic 사용법도 알고 있는 것입니다.
* 여러분의 **<abbr title="Integrated Development Environment - 통합 개발 환경: 코드 편집기와 비슷합니다">IDE</abbr>/<abbr title="코드 오류를 확인하는 프로그램">linter</abbr>/뇌**와 잘 어울립니다:
    * pydantic 데이터 구조는 여러분이 정의한 클래스 인스턴스일 뿐이므로, 자동 완성, 린팅, mypy, 그리고 직관까지도 검증된 데이터와 함께 제대로 작동합니다.
* **복잡한 구조**를 검증합니다:
    * 계층적인 Pydantic 모델, Python `typing`의 `List`와 `Dict` 등을 사용합니다.
    * 그리고 validator는 복잡한 데이터 스키마를 명확하고 쉽게 정의하고, 검사하고, JSON Schema로 문서화할 수 있게 해줍니다.
    * 깊게 **중첩된 JSON** 객체를 가질 수 있으며, 이를 모두 검증하고 주석을 달 수 있습니다.
* **확장 가능**:
    * Pydantic은 사용자 정의 데이터 타입을 정의할 수 있게 하거나, validator decorator가 붙은 모델 메서드로 검증을 확장할 수 있습니다.
* 100% test coverage.
