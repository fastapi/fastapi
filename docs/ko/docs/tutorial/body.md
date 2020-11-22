# 요청 본문

클라이언트(브라우저라고 합시다)에서 API로 데이터를 보내야 할 때, **요청 본문**을 보냅니다.

**요청** 본문은 클라이언트에서 API로 보내는 데이터입니다. **응답** 본문은 API에서 클라이언트로 보내는 데이터입니다.

API는 대부분 **응답** 본문을 보냅니다. 하지만 클라이언트는 항상 **요청** 본문을 보낼 필요는 없습니다.

**요청** 본문을 선언하려면, 강력한 힘과 장점을 가진 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 모델을 사용하면 됩니다.

!!! info "정보"
    데이터를 보내기 위해서 다음 중 하나를 사용하면 됩니다: `POST` (좀 더 일반적), `PUT`, `DELETE` 또는 `PATCH`.

    `GET` 요청으로 본문을 보내는 것은 사양에 정의되지 않은 동작이 있지만, 그럼에도 FastAPI는 매우 복잡/극단적 사용 사례에 대해서만 지원됩니다.

    이것은 권장되지 않기 때문에 Swagger UI 대화형 문서는 `GET`을 사용할 경우 본문에 대한 문서를 보여주지 않고, 중간에 있는 프록시가 지원하지 않을수 있습니다.

## Pydantic의 `BaseModel` 임포트

우선, `pydantic`에서 `BaseModel`를 임포트해야 합니다:

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## 데이터 모델 생성

이제 `BaseModel`을 상속하는 클래스로 데이터 모델을 선언합니다.

모든 어트리뷰트에 표준 파이썬 타입을 사용합니다:

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

쿼리 매개변수를 선언할 때와 마찬가지로, 모델 어트리뷰트에 기본값이 있으면 필수가 아닙니다. 그렇지 않으면 필수입니다. 선택적으로 만들려면 `None`을 사용합니다.

예를 들어, 위에서 이 모델은 JSON "`object`"(또는 파이썬 `dict`)를 다음과 같이 선언합니다:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...`description`과 `tax`는 (`None` 값을 기본값으로 하면서) 선택적이며, 이 JSON "`object`" 또한 유효합니다:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 매개변수로 선언

이를 *경로 동작*에 추가하려면 경로 및 쿼리 매개변수를 선언한 것과 동일한 방식으로 선언합니다:

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

...그리고 생성한 `Item` 모델로 타입을 선언합니다.

## 결과

파이선 타입 선언만으로 **FastAPI**는:

* 요청 본문을 JSON으로 읽습니다.
* (필요하다면) 해당 타입을 변환합니다.
* 데이터를 검증합니다.
    * 데이터가 유효하지 않다면, 잘못된 데이터가 어디에서 무엇인지 정확하게 표시하는 멋지고 명확한 오류를 반환합니다.
* 매개변수 `item`에 수신한 데이터를 전달합니다.
    * 함수에 `Item` 타입으로 선언함으로써, 모든 어트리뷰트와 그 타입에 대한 편집기 지원(자동완성 등) 역시 제공합니다.
* 모델의 <a href="https://json-schema.org" class="external-link" target="_blank">JSON 스키마</a> 정의를 생성하고, 프로젝트에 적합한 경우 원하는 곳 어디에서나 사용할 수도 있습니다.
* 이 스키마들은 생성한 OpenAPI 스키마의 일부가 되며 자동 <abbr title="유저 인터페이스(User Interface)">UI</abbr> 문서화에 사용됩니다.

## 자동 문서

모델의 JSON 스키마는 OpenAPI 생성 스키마의 일부가 되며 대화형 API 문서에 표시됩니다:

<img src="/img/tutorial/body/image01.png">

그리고 이를 필요로 하는 각 *경로 동작* 내의 API 문서에서도 사용됩니다:

<img src="/img/tutorial/body/image02.png">

## 편집기 지원

편집기에서 함수 내부 모든 곳(Pydantic 모델 대신 `dict`를 받은 경우에는 발생하지 않습니다)에서 타입 힌트와 자동완성을 얻을 수 있습니다:

<img src="/img/tutorial/body/image03.png">

잘못된 타입 작업에 대한 오류 검사도 받습니다:

<img src="/img/tutorial/body/image04.png">

이는 우연이 아니며, 전체 프레임워크는 이러한 설계를 중심으로 구축되었습니다.

그리고 구현하기 전에 설계 단계에서 철저히 테스트하여 모든 편집자와 함께 작동하는지 확인했습니다.

이를 지원하기 위해 Pydantic 자체에도 약간의 변경이 있었습니다.

이전 스크린샷은 <a href="https://code.visualstudio.com" class="external-link" target="_blank">비주얼 스튜디오 코드</a>에서 찍은 것입니다.

하지만 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 및 대부분의 다른 파이썬 편집기에서 동일한 편집기 지원을 얻을 수 있습니다:

<img src="/img/tutorial/body/image05.png">

!!! tip "팁"
    <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>을 편집기로 사용하고 있다면, <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm 플러그인</a>을 사용할 수 있습니다.

    다음을 통해 Pydantic 모델에 대한 편집기 지원을 개선합니다:

    * 자동완성
    * 타입 검사
    * 리팩토링
    * 검색
    * 검사(Inspection)

## 모델 사용

함수 내부에서 모델 객체의 모든 어트리뷰트에 직접 접근할 수 있습니다:

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## 요청 본문 + 경로 매개변수

경로 매개변수와 요청 본문을 동시에 선언할 수 있습니다.

**FastAPI**는 경로 매개변수와 일치하는 함수 매개변수는 **경로에서 가져와야 함**을, Pydantic 모델로 선언한 함수 매개변수는 **요청 본문에서 가져와야 함**을 인지합니다.

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## 요청 본문 + 경로 + 쿼리 매개변수

**본문**, **경로** 그리고 **쿼리** 매개변수 전부를 동시에 선언할 수도 있습니다.

**FastAPI**는 각각을 인식하고 올바른 위치에서 데이터를 가져옵니다.

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

함수 매개변수는 다음으로 인식됩니다:

* 매개변수가 **경로**에도 선언되었다면 경로 매개변수로 사용됩니다.
* 매개변수가 **단수형**(`int`, `float`, `str`, `bool` 등)이면 **쿼리** 매개변수로 해석됩니다.
* 매개변수가 **Pydantic 모델** 타입으로 선언되었다면 요청 **본문**으로 해석됩니다.

!!! note "참고"
    FastAPI는 `q`가 `= None`이므로 선택적이라는 것을 인지합니다.

    `Optional[str]`에 있는 `Optional`은 FastAPI(FastAPI는 `str` 부분만 사용합니다)가 사용하는게 아니지만, `Optional[str]`은 편집기에게 코드에서 오류를 찾아낼 수 있게 도와줍니다.

## Pydantic 없이 사용하기

Pydantic 모델을 사용하고 싶지 않다면, **본문(Body)** 매개변수를 사용할 수 있습니다. [본문 - 다중 매개변수: 본문의 단수형 값](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank} 문서를 보세요.
