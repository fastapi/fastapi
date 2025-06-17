# 요청 본문

클라이언트(브라우저라고 해봅시다)로부터 여러분의 API로 데이터를 보내야 할 때, **요청 본문**으로 보냅니다.

**요청** 본문은 클라이언트에서 API로 보내지는 데이터입니다. **응답** 본문은 API가 클라이언트로 보내는 데이터입니다.

여러분의 API는 대부분의 경우 **응답** 본문을 보내야 합니다. 하지만 클라이언트는 **요청** 본문을 매 번 보낼 필요가 없습니다.

**요청** 본문을 선언하기 위해서 모든 강력함과 이점을 갖춘 <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> 모델을 사용합니다.

/// info | 정보

데이터를 보내기 위해, (좀 더 보편적인) `POST`, `PUT`, `DELETE` 혹은 `PATCH` 중에 하나를 사용하는 것이 좋습니다.

`GET` 요청에 본문을 담아 보내는 것은 명세서에 정의되지 않은 행동입니다. 그럼에도 불구하고, 이 방식은 아주 복잡한/극한의 사용 상황에서만 FastAPI에 의해 지원됩니다.

`GET` 요청에 본문을 담는 것은 권장되지 않기에, Swagger UI같은 대화형 문서에서는 `GET` 사용시 담기는 본문에 대한 문서를 표시하지 않으며, 중간에 있는 프록시는 이를 지원하지 않을 수도 있습니다.

///

## Pydantic의 `BaseModel` 임포트

먼저 `pydantic`에서 `BaseModel`를 임포트해야 합니다:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## 여러분의 데이터 모델 만들기

`BaseModel`를 상속받은 클래스로 여러분의 데이터 모델을 선언합니다.

모든 어트리뷰트에 대해 표준 파이썬 타입을 사용합니다:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

쿼리 매개변수를 선언할 때와 같이, 모델 어트리뷰트가 기본 값을 가지고 있어도 이는 필수가 아닙니다. 그외에는 필수입니다. 그저 `None`을 사용하여 선택적으로 만들 수 있습니다.

예를 들면, 위의 이 모델은 JSON "`object`" (혹은 파이썬 `dict`)을 다음과 같이 선언합니다:

```JSON
{
    "name": "Foo",
    "description": "선택적인 설명란",
    "price": 45.2,
    "tax": 3.5
}
```

...`description`과 `tax`는 (기본 값이 `None`으로 되어 있어) 선택적이기 때문에, 이 JSON "`object`"는 다음과 같은 상황에서도 유효합니다:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 매개변수로서 선언하기

여러분의 *경로 작동*에 추가하기 위해, 경로 매개변수 그리고 쿼리 매개변수에서 선언했던 것과 같은 방식으로 선언하면 됩니다.

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...그리고 만들어낸 모델인 `Item`으로 타입을 선언합니다.

## 결과

위에서의 단순한 파이썬 타입 선언으로, **FastAPI**는 다음과 같이 동작합니다:

* 요청의 본문을 JSON으로 읽어 들입니다.
* (필요하다면) 대응되는 타입으로 변환합니다.
* 데이터를 검증합니다.
    * 만약 데이터가 유효하지 않다면, 정확히 어떤 것이 그리고 어디에서 데이터가 잘 못 되었는지 지시하는 친절하고 명료한 에러를 반환할 것입니다.
* 매개변수 `item`에 포함된 수신 데이터를 제공합니다.
    * 함수 내에서 매개변수를 `Item` 타입으로 선언했기 때문에, 모든 어트리뷰트와 그에 대한 타입에 대한 편집기 지원(완성 등)을 또한 받을 수 있습니다.
* 여러분의 모델을 위한 <a href="https://json-schema.org" class="external-link" target="_blank">JSON 스키마</a> 정의를 생성합니다. 여러분의 프로젝트에 적합하다면 여러분이 사용하고 싶은 곳 어디에서나 사용할 수 있습니다.
* 이러한 스키마는, 생성된 OpenAPI 스키마 일부가 될 것이며, 자동 문서화 <abbr title="사용자 인터페이스">UI</abbr>에 사용됩니다.

## 자동 문서화

모델의 JSON 스키마는 생성된 OpenAPI 스키마에 포함되며 대화형 API 문서에 표시됩니다:

<img src="/img/tutorial/body/image01.png">

이를 필요로 하는 각각의 *경로 작동*내부의 API 문서에도 사용됩니다:

<img src="/img/tutorial/body/image02.png">

## 편집기 지원

편집기에서, 함수 내에서 타입 힌트와 완성을 어디서나 (만약 Pydantic model 대신에 `dict`을 받을 경우 나타나지 않을 수 있습니다) 받을 수 있습니다:

<img src="/img/tutorial/body/image03.png">

잘못된 타입 연산에 대한 에러 확인도 받을 수 있습니다:

<img src="/img/tutorial/body/image04.png">

단순한 우연이 아닙니다. 프레임워크 전체가 이러한 디자인을 중심으로 설계되었습니다.

그 어떤 실행 전에, 모든 편집기에서 작동할 수 있도록 보장하기 위해 설계 단계에서 혹독하게 테스트되었습니다.

이를 지원하기 위해 Pydantic 자체에서 몇몇 변경점이 있었습니다.

이전 스크린샷은 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>를 찍은 것입니다.

하지만 똑같은 편집기 지원을 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>에서 받을 수 있거나, 대부분의 다른 편집기에서도 받을 수 있습니다:

<img src="/img/tutorial/body/image05.png">

/// tip | 팁

만약 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>를 편집기로 사용한다면, <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>을 사용할 수 있습니다.

다음 사항을 포함해 Pydantic 모델에 대한 편집기 지원을 향상시킵니다:

* 자동 완성
* 타입 확인
* 리팩토링
* 검색
* 점검

///

## 모델 사용하기

함수 안에서 모델 객체의 모든 어트리뷰트에 직접 접근 가능합니다:

{* ../../docs_src/body/tutorial002_py310.py hl[19] *}

## 요청 본문 + 경로 매개변수

경로 매개변수와 요청 본문을 동시에 선언할 수 있습니다.

**FastAPI**는 경로 매개변수와 일치하는 함수 매개변수가 **경로에서 가져와야 한다**는 것을 인지하며, Pydantic 모델로 선언된 그 함수 매개변수는 **요청 본문에서 가져와야 한다**는 것을 인지할 것입니다.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## 요청 본문 + 경로 + 쿼리 매개변수

**본문**, **경로** 그리고 **쿼리** 매개변수 모두 동시에 선언할 수도 있습니다.

**FastAPI**는 각각을 인지하고 데이터를 옳바른 위치에 가져올 것입니다.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

함수 매개변수는 다음을 따라서 인지하게 됩니다:

* 만약 매개변수가 **경로**에도 선언되어 있다면, 이는 경로 매개변수로 사용될 것입니다.
* 만약 매개변수가 (`int`, `float`, `str`, `bool` 등과 같은) **유일한 타입**으로 되어있으면, **쿼리** 매개변수로 해석될 것입니다.
* 만약 매개변수가 **Pydantic 모델** 타입으로 선언되어 있으면, 요청 **본문**으로 해석될 것입니다.

/// note | 참고

FastAPI는 `q`의 값이 필요없음을 알게 될 것입니다. 기본 값이 `= None`이기 때문입니다.

`Union[str, None]`에 있는 `Union`은 FastAPI에 의해 사용된 것이 아니지만, 편집기로 하여금 더 나은 지원과 에러 탐지를 지원할 것입니다.

///

## Pydantic없이

만약 Pydantic 모델을 사용하고 싶지 않다면, **Body** 매개변수를 사용할 수도 있습니다. [Body - 다중 매개변수: 본문에 있는 유일한 값](body-multiple-params.md#_2){.internal-link target=_blank} 문서를 확인하세요.
