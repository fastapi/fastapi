# 기능

## FastAPI의 기능

**FastAPI**는 다음과 같은 기능을 제공합니다:

### 개방형 표준을 기반으로

* <abbr title="엔드포인트, 라우트로도 알려져 있습니다">경로</abbr><abbr title="POST, GET, PUT, DELETE와 같은 HTTP 메소드로 알려져 있습니다">작동</abbr>, 매개변수, 본문 요청, 보안 그 외의 선언을 포함한 API 생성을 위한 <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a>
* <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (OpenAPI 자체가 JSON Schema를 기반으로 하고 있습니다)를 사용한 자동 데이터 모델 문서화.
* 단순히 떠올려서 덧붙인 기능이 아닙니다. 세심한 검토를 거친 후, 이러한 표준을 기반으로 설계되었습니다.
* 이는 또한 다양한 언어로 자동적인 **클라이언트 코드 생성**을 사용할 수 있게 지원합니다.

### 문서 자동화

대화형 API 문서와 웹 탐색 유저 인터페이스를 제공합니다. 프레임워크가 OpenAPI를 기반으로 하기에, 2가지 옵션이 기본적으로 들어간 여러 옵션이 존재합니다.

* 대화형 탐색 <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>를 이용해, 브라우저에서 바로 여러분의 API를 호출하거나 테스트할 수 있습니다.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>을 이용해 API 문서화를 대체할 수 있습니다.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### 그저 현대 파이썬

(Pydantic 덕분에) FastAPI는 표준 **파이썬 3.6 타입** 선언에 기반하고 있습니다. 새로 배울 문법이 없습니다. 그저 표준적인 현대 파이썬입니다.

만약 여러분이 파이썬 타입을 어떻게 사용하는지에 대한 2분 정도의 복습이 필요하다면 (비록 여러분이 FastAPI를 사용하지 않는다 하더라도), 다음의 짧은 자습서를 확인하세요: [파이썬 타입](python-types.md){.internal-link target=\_blank}.

여러분은 타입을 이용한 표준 파이썬을 다음과 같이 적을 수 있습니다:

```Python
from datetime import date

from pydantic import BaseModel

# 변수를 str로 선언
# 그 후 함수 안에서 편집기 지원을 받으세요
def main(user_id: str):
    return user_id


# Pydantic 모델
class User(BaseModel):
    id: int
    name: str
    joined: date
```

위의 코드는 다음과 같이 사용될 수 있습니다:

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

`**second_user_data`가 뜻하는 것:

`second_user_data` 딕셔너리의 키와 값을 키-값 인자로서 바로 넘겨줍니다. 다음과 동일합니다: `User(id=4, name="Mary", joined="2018-11-30")`

///

### 편집기 지원

모든 프레임워크는 사용하기 쉽고 직관적으로 설계되었으며, 좋은 개발 경험을 보장하기 위해 개발을 시작하기도 전에 모든 결정들은 여러 편집기에서 테스트됩니다.

최근 파이썬 개발자 설문조사에서 <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">"자동 완성"이 가장 많이 사용되는 기능</a>이라는 것이 밝혀졌습니다.

**FastAPI** 프레임워크의 모든 부분은 이를 충족하기 위해 설계되었습니다. 자동완성은 어느 곳에서나 작동합니다.

여러분은 문서로 다시 돌아올 일이 거의 없을 겁니다.

다음은 편집기가 어떻게 여러분을 도와주는지 보여줍니다:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>에서:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>에서:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

여러분이 이전에 불가능하다고 고려했던 코드도 완성할 수 있을 겁니다. 예를 들어, 요청에서 전달되는 (중첩될 수도 있는)JSON 본문 내부에 있는 `price` 키입니다.

잘못된 키 이름을 적을 일도, 문서를 왔다 갔다할 일도 없으며, 혹은 마지막으로 `username` 또는 `user_name`을 사용했는지 찾기 위해 위 아래로 스크롤할 일도 없습니다.

### 토막 정보

어느 곳에서나 선택적 구성이 가능한 모든 것에 합리적인 기본값이 설정되어 있습니다. 모든 매개변수는 여러분이 필요하거나, 원하는 API를 정의하기 위해 미세하게 조정할 수 있습니다.

하지만 기본적으로 모든 것이 "그냥 작동합니다".

### 검증

* 다음을 포함한, 대부분의 (혹은 모든?) 파이썬 **데이터 타입** 검증할 수 있습니다:
    * JSON 객체 (`dict`).
    * 아이템 타입을 정의하는 JSON 배열 (`list`).
    * 최소 길이와 최대 길이를 정의하는 문자열 (`str`) 필드.
    * 최솟값과 최댓값을 가지는 숫자 (`int`, `float`), 그 외.

* 다음과 같이 더욱 이색적인 타입에 대해 검증할 수 있습니다:
    * URL.
    * 이메일.
    * UUID.
    * ...다른 것들.

모든 검증은 견고하면서 잘 확립된 **Pydantic**에 의해 처리됩니다.

### 보안과 인증

보안과 인증이 통합되어 있습니다. 데이터베이스나 데이터 모델과의 타협없이 사용할 수 있습니다.

다음을 포함하는, 모든 보안 스키마가 OpenAPI에 정의되어 있습니다.

* HTTP Basic.
* **OAuth2** (**JWT tokens** 또한 포함). [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=\_blank}에 있는 자습서를 확인해 보세요.
* 다음에 들어 있는 API 키:
    * 헤더.
    * 매개변수.
    * 쿠키 및 그 외.

추가적으로 (**세션 쿠키**를 포함한) 모든 보안 기능은 Starlette에 있습니다.

모두 재사용할 수 있는 도구와 컴포넌트로 만들어져 있어 여러분의 시스템, 데이터 저장소, 관계형 및 NoSQL 데이터베이스 등과 쉽게 통합할 수 있습니다.

### 의존성 주입

FastAPI는 사용하기 매우 간편하지만, 엄청난 <abbr title='"컴포넌트", "자원", "서비스", "제공자"로도 알려진'><strong>의존성 주입</strong></abbr>시스템을 포함하고 있습니다.

* 의존성은 의존성을 가질수도 있어, 이를 통해 의존성의 계층이나 **의존성의 "그래프"**를 형성합니다.
* 모든 것이 프레임워크에 의해 **자동적으로 처리됩니다**.
* 모든 의존성은 요청에서 데이터를 요구하여 자동 문서화와 **경로 작동 제약을 강화할 수 있습니다**.
* 의존성에서 정의된 _경로 작동_ 매개변수에 대해서도 **자동 검증**이 이루어 집니다.
* 복잡한 사용자의 인증 시스템, **데이터베이스 연결**, 등등을 지원합니다.
* 데이터베이스, 프론트엔드 등과 관련되어 **타협하지 않아도 됩니다**. 하지만 그 모든 것과 쉽게 통합이 가능합니다.

### 제한 없는 "플러그인"

또는 다른 방법으로, 그것들을 사용할 필요 없이 필요한 코드만 임포트할 수 있습니다.

어느 통합도 (의존성과 함께) 사용하기 쉽게 설계되어 있어, *경로 작동*에 사용된 것과 동일한 구조와 문법을 사용하여 2줄의 코드로 여러분의 어플리케이션에 사용할 "플러그인"을 만들 수 있습니다.

### 테스트 결과

* 100% <abbr title="자동적으로 테스트된 코드의 양">테스트 범위</abbr>.
* 100% <abbr title="파이썬의 타입 어노테이션, 이를 통해 여러분의 편집기와 외부 도구는 여러분에게 더 나은 지원을 할 수 있습니다">타입이 명시된</abbr> 코드 베이스.
* 상용 어플리케이션에서의 사용.

## Starlette 기능

**FastAPI**는 <a href="https://www.starlette.dev/" class="external-link" target="_blank"><strong>Starlette</strong></a>를 기반으로 구축되었으며, 이와 완전히 호환됩니다. 따라서, 여러분이 보유하고 있는 어떤 추가적인 Starlette 코드도 작동할 것입니다.

`FastAPI`는 실제로 `Starlette`의 하위 클래스입니다. 그래서, 여러분이 이미 Starlette을 알고 있거나 사용하고 있으면, 대부분의 기능이 같은 방식으로 작동할 것입니다.

**FastAPI**를 사용하면 여러분은 **Starlette**의 기능 대부분을 얻게 될 것입니다(FastAPI가 단순히 Starlette를 강화했기 때문입니다):

* 아주 인상적인 성능. 이는 <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">**NodeJS**와 **Go**와 동등하게 사용 가능한 가장 빠른 파이썬 프레임워크 중 하나입니다</a>.
* **WebSocket** 지원.
* 프로세스 내의 백그라운드 작업.
* 시작과 종료 이벤트.
* HTTPX 기반 테스트 클라이언트.
* **CORS**, GZip, 정적 파일, 스트리밍 응답.
* **세션과 쿠키** 지원.
* 100% 테스트 범위.
* 100% 타입이 명시된 코드 베이스.

## Pydantic 기능

**FastAPI**는 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank"><strong>Pydantic</strong></a>을 기반으로 하며 Pydantic과 완벽하게 호환됩니다. 그래서 어느 추가적인 Pydantic 코드를 여러분이 가지고 있든 작동할 것입니다.

Pydantic을 기반으로 하는, 데이터베이스를 위한 <abbr title="Object-Relational Mapper">ORM</abbr>, <abbr title="Object-Document Mapper">ODM</abbr>을 포함한 외부 라이브러리를 포함합니다.

이는 모든 것이 자동으로 검증되기 때문에, 많은 경우에서 요청을 통해 얻은 동일한 객체를, **직접 데이터베이스로** 넘겨줄 수 있습니다.

반대로도 마찬가지이며, 많은 경우에서 여러분은 **직접 클라이언트로** 그저 객체를 넘겨줄 수 있습니다.

**FastAPI**를 사용하면 (모든 데이터 처리를 위해 FastAPI가 Pydantic을 기반으로 하기 있기에) **Pydantic**의 모든 기능을 얻게 됩니다:

* **어렵지 않은 언어**:
    * 새로운 스키마 정의 마이크로 언어를 배우지 않아도 됩니다.
    * 여러분이 파이썬 타입을 안다면, 여러분은 Pydantic을 어떻게 사용하는지 아는 겁니다.
* 여러분의 **<abbr title="통합 개발 환경, 코드 편집기와 비슷합니다">IDE</abbr>/<abbr title="코드 에러를 확인하는 프로그램">린터</abbr>/뇌**와 잘 어울립니다:
    * Pydantic 데이터 구조는 단순 여러분이 정의한 클래스의 인스턴스이기 때문에, 자동 완성, 린팅, mypy 그리고 여러분의 직관까지 여러분의 검증된 데이터와 올바르게 작동합니다.
* **복잡한 구조**를 검증합니다:
    * 계층적인 Pydantic 모델, 파이썬 `typing`의 `List`와 `Dict`, 그 외를 사용합니다.
    * 그리고 검증자는 복잡한 데이터 스키마를 명확하고 쉽게 정의 및 확인하며 JSON 스키마로 문서화합니다.
    * 여러분은 깊게 **중첩된 JSON** 객체를 가질 수 있으며, 이 객체 모두 검증하고 설명을 붙일 수 있습니다.
* **확장 가능성**:
    * Pydantic은 사용자 정의 데이터 타입을 정의할 수 있게 하거나, 검증자 데코레이터가 붙은 모델의 메소드를 사용하여 검증을 확장할 수 있습니다.
* 100% 테스트 범위.
