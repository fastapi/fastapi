# 본문 - 필드

`Query`, `Path`와 `Body`를 사용해 *경로 작동 함수* 매개변수 내에서 추가적인 검증이나 메타데이터를 선언한 것처럼 Pydantic의 `Field`를 사용하여 모델 내에서 검증과 메타데이터를 선언할 수 있습니다.

## `Field` 임포트

먼저 이를 임포트해야 합니다:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[4] *}

/// warning | 경고

`Field`는 다른 것들처럼 (`Query`, `Path`, `Body` 등) `fastapi`에서가 아닌 `pydantic`에서 바로 임포트 되는 점에 주의하세요.

///

## 모델 어트리뷰트 선언

그 다음 모델 어트리뷰트와 함께 `Field`를 사용할 수 있습니다:

{* ../../docs_src/body_fields/tutorial001_an_py310.py hl[11:14] *}

`Field`는 `Query`, `Path`와 `Body`와 같은 방식으로 동작하며, 모두 같은 매개변수들 등을 가집니다.

/// note | 기술적 세부사항

실제로 `Query`, `Path`등, 여러분이 앞으로 볼 다른 것들은 공통 클래스인 `Param` 클래스의 서브클래스 객체를 만드는데, 그 자체로 Pydantic의 `FieldInfo` 클래스의 서브클래스입니다.

그리고 Pydantic의 `Field` 또한 `FieldInfo`의 인스턴스를 반환합니다.

`Body` 또한 `FieldInfo`의 서브클래스 객체를 직접적으로 반환합니다. 그리고 `Body` 클래스의 서브클래스인 것들도 여러분이 나중에 보게될 것입니다.

 `Query`, `Path`와 그 외 것들을 `fastapi`에서 임포트할 때, 이는 실제로 특별한 클래스를 반환하는 함수인 것을 기억해 주세요.

///

/// tip | 팁

주목할 점은 타입, 기본 값 및 `Field`로 이루어진 각 모델 어트리뷰트가  `Path`, `Query`와 `Body`대신 `Field`를 사용하는 *경로 작동 함수*의 매개변수와 같은 구조를 가진다는 점 입니다.

///

## 별도 정보 추가

`Field`, `Query`, `Body`, 그 외 안에 별도 정보를 선언할 수 있습니다. 이는 생성된 JSON 스키마에 포함됩니다.

여러분이 예제를 선언할 때 나중에 이 공식 문서에서 별도 정보를 추가하는 방법을 배울 것입니다.

/// warning | 경고

별도 키가 전달된 `Field` 또한 여러분의 어플리케이션의 OpenAPI 스키마에 나타날 것입니다.
이런 키가 OpenAPI 명세서, [the OpenAPI validator](https://validator.swagger.io/)같은 몇몇 OpenAPI 도구들에 포함되지 못할 수 있으며, 여러분이 생성한 스키마와 호환되지 않을 수 있습니다.

///

## 요약

모델 어트리뷰트를 위한 추가 검증과 메타데이터 선언하기 위해 Pydantic의 `Field` 를 사용할 수 있습니다.

또한 추가적인 JSON 스키마 메타데이터를 전달하기 위한 별도의 키워드 인자를 사용할 수 있습니다.
