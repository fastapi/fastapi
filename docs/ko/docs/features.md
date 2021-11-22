# 기능

## FastAPI 기능

**FastAPI** 에는 다음과 같은 기능이 있습니다:

### 개방형 표준 준수

- API 작성을 위한 [**OpenAPI**](https://github.com/OAI/OpenAPI-Specification) 에는, 경로 작업 선언, 매개 변수, 본문 요청, 보안 등이 포함됩니다.
- [**JSON Schema**](https://json-schema.org/) 를 사용한 데이터 모델의 문서를 자동 생성합니다(OpenAPI는 JSON 스키마를 기반으로 함).
- 면밀히 조사의 결과, 상층에 개설하는 것이 아니라, 이 기준에 의거해 설계되었습니다.
- 이것은 또한 많은 언어에서 자동 **클라이언트 코드 생성**을 허용합니다.

### 자동 문서 생성

대화형 API 문서와 탐색적인 웹 사용자 인터페이스를 제공합니다. 프레임워크가 OpenAPI를 기반으로 하기 때문에, 몇 가지 옵션이 있으며, 기본적으로 두 가지가 포함되어 있습니다.

- [**Swagger UI**](https://github.com/swagger-api/swagger-ui), 에서 대화형 탐색을 통해, 브라우저에서 직접 API를 호출하고 테스트할 수 있습니다.

[![Swagger UI interaction](https://camo.githubusercontent.com/b8ead36860df4f2befd2203bfa1da701c57c09ceb16e4ac6b9881d698e9950ce/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f696e6465782f696e6465782d30332d737761676765722d30322e706e67)](https://camo.githubusercontent.com/b8ead36860df4f2befd2203bfa1da701c57c09ceb16e4ac6b9881d698e9950ce/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f696e6465782f696e6465782d30332d737761676765722d30322e706e67)

- [**ReDoc**](https://github.com/Rebilly/ReDoc)을 사용한 대체 API 문서 생성.

[![ReDoc](https://camo.githubusercontent.com/dbecb8020ca255e9565bef9b49cb8056a756cef7ad5d7e5fea010babb216e5e8/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f696e6465782f696e6465782d30362d7265646f632d30322e706e67)](https://camo.githubusercontent.com/dbecb8020ca255e9565bef9b49cb8056a756cef7ad5d7e5fea010babb216e5e8/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f696e6465782f696e6465782d30362d7265646f632d30322e706e67)

### 현대 파이썬

FastAPI의 모든 기능은 표준 **파이썬 3.6 버전** 선언을 기반으로 합니다 (Pydantic 덕분에). 학습할 새로운 구문은 없습니다. 그냥 현대적인 표준 파이썬입니다.

(FastAPI를 사용하지 않더라도) 파이썬 유형을 사용하는 방법에 대한 간단한 복습이 필요한 경우, 짧은 튜토리얼을 확인하십시오: [Python Types](https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/python-types.md){.internal-link target=_blank}.

표준 파이썬은 다음과 같은 형식으로 작성합니다:

```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

이것은 다음과 같이 사용됩니다:

```
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! 정보 `**second_user_data` 는 다음을 의미합니다:

```
Pass the keys and values of the `second_user_data` dict directly as key-value arguments, equivalent to: `User(id=4, name="Mary", joined="2018-11-30")`
```

### 편집기 지원

모든 프레임워크는 사용하기 쉽고 직관적으로 설계되었으며, 모든 결정은 개발을 시작하기 전에 여러 편집기에서 테스트되어 최상의 개발 경험을 보장합니다.

지난 파이썬 개발자 설문조사에서 [가장 많이 사용된 기능이 "자동 완성"](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features)이라는 것이 밝혀졌습니다.

**FastAPI** 프레임워크는 이 요구사항을 충족하는 것을 기본으로 합니다. 자동 완성은 어디에서나 작동합니다.

다시 문서로 돌아올 필요가 거의 없습니다.

편집기가 어떻게 도움이 되는지는 다음과 같습니다:

- [Visual Studio Code](https://code.visualstudio.com/)의 경우:

[![editor support](https://camo.githubusercontent.com/99884510d53d86b6b309c53e5e446c9f4154b2a4f7e3c11b4e98e0f0bf74017b/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f7673636f64652d636f6d706c6574696f6e2e706e67)](https://camo.githubusercontent.com/99884510d53d86b6b309c53e5e446c9f4154b2a4f7e3c11b4e98e0f0bf74017b/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f7673636f64652d636f6d706c6574696f6e2e706e67)

- [PyCharm](https://www.jetbrains.com/pycharm/)의 경우:

[![editor support](https://camo.githubusercontent.com/7c87f92e5c55b3c05b24b6952fd3fd50fca44714e84533b352eb8559011f7ab4/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f7079636861726d2d636f6d706c6574696f6e2e706e67)](https://camo.githubusercontent.com/7c87f92e5c55b3c05b24b6952fd3fd50fca44714e84533b352eb8559011f7ab4/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f7079636861726d2d636f6d706c6574696f6e2e706e67)

이전에는 불가능하다고 생각될 수 있는 코드를 완성할 수 있습니다. 예를 들어, JSON 본문 (중첩될 수 있음)의 `price` 키입니다.

더 이상 잘못된 키 이름을 입력하거나, 문서 사이를 왔다 갔다 하거나, `username` 또는 `user_name`을 사용했는지 여부를 찾기 위해 위아래로 스크롤할 필요가 없습니다.

### 간결

모든 항목에 적합한 **기본값**이 있으며, 어디서나 선택적 구성이 가능합니다. 필요한 작업을 수행하고 필요한 API를 정의하기 위해 모든 매개 변수를 미세 조정할 수 있습니다.

그러나 기본적으로, 모든 기능이 **"잘 작동합니다"**.

### 검증

- 대부분 (또는 모두?)에 대한 파이썬 **데이터 유형** 유효성검사는, 다음을 포함합니다:
  - JSON 객체 (`dict`).
  - 항목 유형을 정의하는 JSON 배열 (`list`).
  - 최소 길이와 최대 길이가 있는 문자열 (`str`) 필드.
  - 최소값과 최대값이 있는 숫자 (`int`, `float`), 등.
- 보다 이국적인 유형에 대한 검증, 예를 들면:
  - URL.
  - 이메일.
  - UUID.
  - ...기타.

모든 검증은 잘 확립되고 강력한 **Pydantic**에 의해 처리됩니다.

### 보안 및 인증

보안 및 인증이 통합되어 있습니다. 데이터베이스 또는 데이터 모델에 대해서도 타협하지 않습니다.

다음 OpenAPI에 정의된 모든 보안 체계를 포함합니다:

- HTTP Basic.
- **OAuth2** (**JWT tokens** 포함). JWT를 사용하여 OAuth2 자습서([OAuth2 with JWT](https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md))를 확인하십시오{.internal-link target=_blank}.
- API 키:
  - 헤더.
  - 쿼리 매개변수.
  - 쿠키 등.

또한 Starlette의 모든 보안 기능을 포함합니다 (**세션 쿠키** 포함).

모두 재사용 가능한 도구 및 구성요소로 구축되어 시스템, 데이터 저장소, 관계형 및 NoSQL 데이터베이스 등과  쉽게 통합됩니다.

### 종속성 주입(Dependency Injection)

FastAPI는 매우 사용하기 쉽고, 매우 강력한 **종속성 주입** 시스템을 갖추고 있습니다.

- 종속성은 종속성을 가질 수 있으며, 계층 또는 **종속성의 "그래프"**를 만들 수 있습니다.
- 모든 프레임워크가 **자동으로 처리** 합니다.
- 모든 종속성에는 필요한 데이터를 요청할 수 있으며, **경로 작동** 제약 조건과 자동 문서화를 확장할 수 있습니다.
- 종속성으로 정의된 *경로 작동* 매개변수도 **자동 검증** 이 가능합니다.
- 복잡한 사용자 인증 시스템, **데이터베이스 연결** 등을 지원합니다.
- 데이터베이스, 프론트엔드 등에 대한 **타협은 없습니다**. 하지만 이 모든 것들과 쉽게 통합됩니다.

### 무제한 "플러그인"

아니면 다른 방법으로, 그들이 필요없을 때, 필요한 코드를 가져와서 사용합니다.

통합은 매우 쉽게 사용할 수 있도록 설계되었으며 (종속성을 사용하여)  *경로 작동* 에서 사용되는 것과 동일한 구조와 구문을 사용하여 두 줄의 코드로 응용 프로그램의 "플러그인"을 만들 수 있습니다.

### 테스트

- 100% 테스트 범위.
- 100% 유형 주석 처리된 코드 베이스.
- 프로덕션 응용 프로그램에 사용.

## Starlette 기능

**FastAPI** 는 [**Starlette**](https://www.starlette.io/)와 완벽하게 호환됩니다. 그러므로, 어떤 추가적인 Starlette 코드도 작동될 것입니다 .

`FastAPI` 는 실제로는 `Starlette`의 서브 클래스입니다. 따라서, Starlette을 이미 알고 있거나 사용하는 경우, 대부분의 기능이 동일한 방식으로 작동합니다.

**FastAPI** 를 사용하면 다음과 같은 **Starlette**의 모든 기능을 이용할 수 있습니다 (FastAPI는 단지 Starlette를 강화한 것이기 때문입니다):

- 놀라운 성능. 이것은 [ **NodeJS** 와 **Go**에 필적하는 가장 빠른 파이썬 프레임워크 중 하나입니다](https://github.com/encode/starlette#performance).
- **WebSocket** 지원.
- 프로세스 내 백그라운드 작업.
- 시작 및 종료 이벤트.
- `requests` 기반으로 구축된 테스트 클라이언트.
- **CORS**, GZip, 정적 파일, 스트리밍 응답.
- **세션 및 쿠키** 지원.
- 100% 테스트 범위.
- 100% 유형 주석 처리된 코드베이스.

## Pydantic 기능

**FastAPI** 는 [**Pydantic**](https://pydantic-docs.helpmanual.io/)와 완벽하게 호환됩니다. 그러므로, 어떤 추가적인 Pydantic 코드도 작동될 것입니다.

데이터 베이스용 ORMs, ODMs과 같은 Pydantic 기반의 외부 라이브러리가 있습니다.

이는 모든 것이 자동으로 검증되기 때문에, 대부분의 경우 요청에서 얻은 객체를 **데이터베이스에 직접** 전달할 수 있다는 것을 의미합니다.

똑같은 것이 그 반대에도 적용되며, 대부분의 경우 데이터베이스에서 가져온 객체를 **클라이언트에 직접** 전달할 수 있습니다.

**FastAPI** 를 사용하면 **Pydantic**의 모든 기능을 사용할 수 있습니다 (FastAPI가 Pydantic을 기반으로 모든 데이터 처리를 수행하기 때문입니다):

- **No brainfuck**:
  - 스키마 정의를 위한 마이크로언어를 새롭게 배울 필요가 없습니다.
  - 파이썬 유형을 알고 있다면, 이미 Pydantic을 사용하는 방법을 알고 있습니다.
- 사용자의 **IDE/linter/brain**와 잘 작동합니다:
  - Pydantic 데이터 구조는 사용자가 정의하는 클래스의 단순한 인스턴스이기 때문에 자동완성, 린팅, mypy 및 사용자의 직관력은 모두 검증된 데이터에서 제대로 작동해야 합니다.
- **고속**:
  - [benchmarks](https://pydantic-docs.helpmanual.io/#benchmarks-tag) 에서 Pydantic은 다른 모든 테스트된 라이브러리보다 빠릅니다.
- **복잡한 구조** 검증:
  - 계층적인 Pydantic 모델, 파이썬의 `typing`의 `List` 와 `Dict` 등의 이용.
  - 유효성 검사기를 사용하면 복잡한 데이터 스키마를 명확하고 쉽게 정의, 확인 및  JSON 스키마로 문서화 할 수 있습니다.
  - 깊게 **중첩된 JSON** 객체를 만들고 이를 모두 확인하고 주석을 달 수 있습니다.
- **확장 가능**:
  - Pydantic에서는 사용자 정의 데이터 유형을 정의할 수 있습니다. 또는 유효성 검사 데코레이터로 장식된 모델의 메서드를 사용하여 유효성 검사를 확장할 수 있습니다.
- 100% 테스트 범위.