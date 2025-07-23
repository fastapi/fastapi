# 쿠키 매개변수

쿠키 매개변수를 `Query`와 `Path` 매개변수들과 같은 방식으로 정의할 수 있습니다.

## `Cookie` 임포트

먼저 `Cookie`를 임포트합니다:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` 매개변수 선언

그런 다음, `Path`와 `Query`처럼 동일한 구조를 사용하는 쿠키 매개변수를 선언합니다.

첫 번째 값은 기본값이며, 추가 검증이나 어노테이션 매개변수 모두 전달할 수 있습니다:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 기술 세부사항

`Cookie`는 `Path` 및 `Query`의 "자매"클래스입니다. 이 역시 동일한 공통 `Param` 클래스를 상속합니다.

`Query`, `Path`, `Cookie` 그리고 다른 것들은 `fastapi`에서 임포트 할 때, 실제로는 특별한 클래스를 반환하는 함수임을 기억하세요.

///

/// info | 정보

쿠키를 선언하기 위해서는 `Cookie`를 사용해야 합니다. 그렇지 않으면 해당 매개변수를 쿼리 매개변수로 해석하기 때문입니다.

///

## 요약

`Cookie`는 `Query`, `Path`와 동일한 패턴을 사용하여 선언합니다.
