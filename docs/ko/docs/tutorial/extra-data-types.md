# 추가 데이터 자료형

지금까지 일반적인 데이터 자료형을 사용했습니다. 예를 들면 다음과 같습니다:

* `int`
* `float`
* `str`
* `bool`

하지만 더 복잡한 데이터 자료형 또한 사용할 수 있습니다.

그리고 지금까지와 같은 기능들을 여전히 사용할 수 있습니다.

* 훌륭한 편집기 지원.
* 들어오는 요청의 데이터 변환.
* 응답 데이터의 데이터 변환.
* 데이터 검증.
* 자동 어노테이션과 문서화.

## 다른 데이터 자료형

아래의 추가적인 데이터 자료형을 사용할 수 있습니다:

* `UUID`:
    * 표준 "범용 고유 식별자"로, 많은 데이터베이스와 시스템에서 ID로 사용됩니다.
    * 요청과 응답에서 `str`로 표현됩니다.
* `datetime.datetime`:
    * 파이썬의 `datetime.datetime`.
    * 요청과 응답에서 `2008-09-15T15:53:00+05:00`와 같은 ISO 8601 형식의 `str`로 표현됩니다.
* `datetime.date`:
    * 파이썬의 `datetime.date`.
    * 요청과 응답에서 `2008-09-15`와 같은 ISO 8601 형식의 `str`로 표현됩니다.
* `datetime.time`:
    * 파이썬의 `datetime.time`.
    * 요청과 응답에서 `14:23:55.003`와 같은 ISO 8601 형식의 `str`로 표현됩니다.
* `datetime.timedelta`:
    * 파이썬의 `datetime.timedelta`.
    * 요청과 응답에서 전체 초(seconds)의 `float`로 표현됩니다.
    * Pydantic은 "ISO 8601 시차 인코딩"으로 표현하는 것 또한 허용합니다. <a href="https://docs.pydantic.dev/latest/concepts/serialization/#json_encoders" class="external-link" target="_blank">더 많은 정보는 이 문서에서 확인하십시오.</a>.
* `frozenset`:
    * 요청과 응답에서 `set`와 동일하게 취급됩니다:
        * 요청 시, 리스트를 읽어 중복을 제거하고 `set`로 변환합니다.
        * 응답 시, `set`는 `list`로 변환됩니다.
        * 생성된 스키마는 (JSON 스키마의 `uniqueItems`를 이용해) `set`의 값이 고유함을 명시합니다.
* `bytes`:
    * 표준 파이썬의 `bytes`.
    * 요청과 응답에서 `str`로 취급됩니다.
    * 생성된 스키마는 이것이 `binary` "형식"의 `str`임을 명시합니다.
* `Decimal`:
    * 표준 파이썬의 `Decimal`.
    * 요청과 응답에서 `float`와 동일하게 다뤄집니다.
* 여기에서 모든 유효한 pydantic 데이터 자료형을 확인할 수 있습니다: <a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Pydantic 데이터 자료형</a>.

## 예시

위의 몇몇 자료형을 매개변수로 사용하는 *경로 작동* 예시입니다.

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

함수 안의 매개변수가 그들만의 데이터 자료형을 가지고 있으며, 예를 들어, 다음과 같이 날짜를 조작할 수 있음을 참고하십시오:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
