# 쿠키 매개변수 { #cookie-parameters }

쿠키 매개변수를 `Query`와 `Path` 매개변수들과 같은 방식으로 정의할 수 있습니다.

## `Cookie` 임포트 { #import-cookie }

먼저 `Cookie`를 임포트합니다:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` 매개변수 선언 { #declare-cookie-parameters }

그런 다음, `Path`와 `Query`처럼 동일한 구조를 사용하는 쿠키 매개변수를 선언합니다.

첫 번째 값은 기본값이며, 추가 검증이나 어노테이션 매개변수 모두 전달할 수 있습니다:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | 기술 세부사항

`Cookie`는 `Path` 및 `Query`의 "자매"클래스입니다. 이 역시 동일한 공통 `Param` 클래스를 상속합니다.

하지만 `fastapi`에서 `Query`, `Path`, `Cookie` 그리고 다른 것들을 임포트할 때, 실제로는 특별한 클래스를 반환하는 함수임을 기억하세요.

///

/// info | 정보

쿠키를 선언하기 위해서는 `Cookie`를 사용해야 합니다. 그렇지 않으면 해당 매개변수를 쿼리 매개변수로 해석하기 때문입니다.

///

/// info | 정보

**브라우저는 쿠키를** 내부적으로 특별한 방식으로 처리하기 때문에, **JavaScript**가 쉽게 쿠키를 다루도록 허용하지 않는다는 점을 염두에 두세요.

`/docs`의 **API docs UI**로 이동하면 *경로 처리*에 대한 쿠키 **문서**를 확인할 수 있습니다.

하지만 **데이터를 채우고** "Execute"를 클릭하더라도, docs UI는 **JavaScript**로 동작하기 때문에 쿠키가 전송되지 않고, 아무 값도 입력하지 않은 것처럼 **오류** 메시지를 보게 될 것입니다.

///

## 요약 { #recap }

`Query`와 `Path`에서 사용하는 것과 동일한 공통 패턴으로, `Cookie`를 사용해 쿠키를 선언합니다.
