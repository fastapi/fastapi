# 경로 매개변수와 숫자 검증 { #path-parameters-and-numeric-validations }

`Query`를 사용하여 쿼리 매개변수에 더 많은 검증과 메타데이터를 선언하는 방법과 동일하게 `Path`를 사용하여 경로 매개변수에 검증과 메타데이터를 같은 타입으로 선언할 수 있습니다.

## `Path` 임포트 { #import-path }

먼저 `fastapi`에서 `Path`를 임포트하고, `Annotated`도 임포트합니다:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | 정보

FastAPI는 0.95.0 버전에서 `Annotated` 지원을 추가했고(그리고 이를 권장하기 시작했습니다).

더 오래된 버전이 있다면 `Annotated`를 사용하려고 할 때 오류가 발생합니다.

`Annotated`를 사용하기 전에 최소 0.95.1까지 [FastAPI 버전 업그레이드](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}를 꼭 하세요.

///

## 메타데이터 선언 { #declare-metadata }

`Query`에 동일한 매개변수를 선언할 수 있습니다.

예를 들어, 경로 매개변수 `item_id`에 `title` 메타데이터 값을 선언하려면 다음과 같이 입력할 수 있습니다:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | 참고

경로 매개변수는 경로의 일부여야 하므로 언제나 필수입니다. `None`으로 선언하거나 기본값을 지정하더라도 아무 영향이 없으며, 항상 필수입니다.

///

## 필요한 대로 매개변수 정렬하기 { #order-the-parameters-as-you-need }

/// tip | 팁

`Annotated`를 사용한다면 이것은 아마 그렇게 중요하지 않거나 필요하지 않을 수 있습니다.

///

`str` 형인 쿼리 매개변수 `q`를 필수로 선언하고 싶다고 해봅시다.

해당 매개변수에 대해 아무런 선언을 할 필요가 없으므로 `Query`를 정말로 써야 할 필요는 없습니다.

하지만 `item_id` 경로 매개변수는 여전히 `Path`를 사용해야 합니다. 그리고 어떤 이유로 `Annotated`를 사용하고 싶지 않다고 해봅시다.

파이썬은 "기본값"이 있는 값을 "기본값"이 없는 값 앞에 두면 불평합니다.

하지만 순서를 재정렬해서 기본값이 없는 값(쿼리 매개변수 `q`)을 앞에 둘 수 있습니다.

**FastAPI**에서는 중요하지 않습니다. 이름, 타입 그리고 기본값 선언(`Query`, `Path` 등)로 매개변수를 감지하며 순서는 신경 쓰지 않습니다.

따라서 함수를 다음과 같이 선언할 수 있습니다:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py39.py hl[7] *}

하지만 `Annotated`를 사용하면 이 문제가 없다는 점을 기억하세요. `Query()`나 `Path()`에 함수 매개변수 기본값을 사용하지 않기 때문에, 순서는 중요하지 않습니다.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py *}

## 필요한 대로 매개변수 정렬하기, 트릭 { #order-the-parameters-as-you-need-tricks }

/// tip | 팁

`Annotated`를 사용한다면 이것은 아마 그렇게 중요하지 않거나 필요하지 않을 수 있습니다.

///

유용할 수 있는 **작은 트릭**이 하나 있지만, 자주 필요하진 않을 겁니다.

만약 다음을 원한다면:

* `Query`나 어떤 기본값 없이 쿼리 매개변수 `q`를 선언하기
* `Path`를 사용해서 경로 매개변수 `item_id`를 선언하기
* 이들을 다른 순서로 두기
* `Annotated`를 사용하지 않기

...이를 위해 파이썬에는 작은 특별한 문법이 있습니다.

함수의 첫 번째 매개변수로 `*`를 전달하세요.

파이썬은 `*`으로 아무것도 하지 않지만, 뒤따르는 모든 매개변수는 키워드 인자(키-값 쌍)로 호출되어야 함을 알게 됩니다. 이는 <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>로도 알려져 있습니다. 기본값이 없더라도 마찬가지입니다.

{* ../../docs_src/path_params_numeric_validations/tutorial003_py39.py hl[7] *}

### `Annotated`를 쓰면 더 좋습니다 { #better-with-annotated }

`Annotated`를 사용하면 함수 매개변수 기본값을 사용하지 않기 때문에 이 문제가 발생하지 않으며, 아마 `*`도 사용할 필요가 없다는 점을 기억하세요.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py hl[10] *}

## 숫자 검증: 크거나 같음 { #number-validations-greater-than-or-equal }

`Query`와 `Path`(그리고 나중에 볼 다른 것들)를 사용하여 숫자 제약을 선언할 수 있습니다.

여기서 `ge=1`인 경우, `item_id`는 `1`보다 "`g`reater than or `e`qual"(크거나 같은) 정수형 숫자여야 합니다.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py hl[10] *}

## 숫자 검증: 크거나 및 작거나 같음 { #number-validations-greater-than-and-less-than-or-equal }

동일하게 적용됩니다:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py hl[10] *}

## 숫자 검증: 부동소수, 크거나 및 작거나 { #number-validations-floats-greater-than-and-less-than }

숫자 검증은 `float` 값에도 동작합니다.

여기에서 <abbr title="greater than"><code>gt</code></abbr>를, <abbr title="greater than or equal"><code>ge</code></abbr>뿐만 아니라 선언할 수 있다는 점이 중요해집니다. 예를 들어 값이 `1`보다 작더라도, 반드시 `0`보다 커야 한다고 요구할 수 있습니다.

즉, `0.5`는 유효한 값입니다. 그러나 `0.0` 또는 `0`은 그렇지 않습니다.

<abbr title="less than"><code>lt</code></abbr> 역시 마찬가지입니다.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py hl[13] *}

## 요약 { #recap }

`Query`, `Path`(아직 보지 못한 다른 것들도)를 사용하면 [쿼리 매개변수와 문자열 검증](query-params-str-validations.md){.internal-link target=_blank}에서와 마찬가지로 메타데이터와 문자열 검증을 선언할 수 있습니다.

그리고 숫자 검증 또한 선언할 수 있습니다:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// info | 정보

`Query`, `Path`, 그리고 나중에 보게 될 다른 클래스들은 공통 `Param` 클래스의 서브클래스입니다.

이들 모두는 여러분이 본 추가 검증과 메타데이터에 대한 동일한 매개변수를 공유합니다.

///

/// note | 기술 세부사항

`fastapi`에서 `Query`, `Path` 등을 임포트할 때, 이것들은 실제로 함수입니다.

호출되면 동일한 이름의 클래스의 인스턴스를 반환합니다.

즉, 함수인 `Query`를 임포트한 겁니다. 그리고 호출하면 `Query`라는 이름을 가진 클래스의 인스턴스를 반환합니다.

이 함수들이 있는 이유는(클래스를 직접 사용하는 대신) 편집기에서 타입에 대한 오류를 표시하지 않도록 하기 위해서입니다.

이렇게 하면 오류를 무시하기 위한 사용자 설정을 추가하지 않고도 일반 편집기와 코딩 도구를 사용할 수 있습니다.

///
