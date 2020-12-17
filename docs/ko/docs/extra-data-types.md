# 추가 데이터 타입들

지금까지, 일반적인 데이터 타입을 사용했습니다. 예를 들어:

* `int`
* `float`
* `str`
* `bool`

하지만 보다 복잡한 데이터 타입 또한 사용할 수 있습니다.

그리고 지금까지와 같은 기능들을 계속해서 사용할 수 있습니다.

* 훌륭한 에디터 도움.
* 수신한 요청의 데이터 변환.
* 응답 데이터의 데이터 변환.
* 데이터 검증.
* 자동 어노테이션과 문서화.

## 다른 데이터 타입들

여기에 사용할 수 있는 몇 가지 추가적인 데이터 타입들이 있습니다:

* `UUID`:
    * "범용 고유 식별자"의 표준으로, 많은 데이터베이스와 시스템에서 ID로 사용됩니다.
    * 요청과 응답에서 `str`로 표현됩니다.
* `datetime.datetime`:
    * 파이썬의 `datetime.datetime`.
    * ISO 8601 형식에 따라, 요청과 응답에서 `str`로 표현됩니다. 예시: `2008-09-15T15:53:00+05:00`
* `datetime.date`:
    * 파이썬의 `datetime.date`.
    * ISO 8601 형식에 따라, 요청과 응답에서 `str`로 표현됩니다. 예시: `2008-09-15`.
* `datetime.time`:
    * 파이썬의 `datetime.time`.
    * ISO 8601 형식에 따라, 요청과 응답에서 `str`로 표현됩니다. 예시: `14:23:55.003`.
* `datetime.timedelta`:
    * 파이썬의 `datetime.timedelta`.
    * 요청과 응답에서 전체 초의 `float`으로 표현됩니다.
    * 또한 Pydantic은 "ISO 8601 시차 인코딩"으로 표현하는 것을 허용합니다. <a href="https://pydantic-docs.helpmanual.io/#json-serialisation" class="external-link" target="_blank">더 많은 정보를 가진 문서 보기</a>.
* `frozenset`:
    * 요청과 응답에서 `set`로 동일하게 처리됩니다:
        * 요청에서, 리스트를 읽고 중복을 제거해 `set`로 변환합니다.
        * 응답에서, `set`는 `list`로 변환됩니다.
        * 생성된 스키마는 (JSON 스키마의 `uniqueItems`를 이용해서) `set`의 값이 고유함 명시합니다.
* `bytes`:
    * 표준 파이썬의 `bytes`.
    * 요청과 응답에서 `str`로 처리됩니다.
    * 생성된 스키마는 `binary` "형태"의 `str`로 명시합니다.
* `Decimal`:
    * 표준 파이썬의 `Decimal`.
    * 요청과 응답에서, `float`과 동일하게 취급됩니다.
* 모든 유효한 pydantic 데이터 타입에 대해 확인 할 수 있습니다: <a href="https://pydantic-docs.helpmanual.io/usage/types" class="external-link" target="_blank">Pydantic 데이터 타입</a>.

## 예시
다음은 위의 나온 몇몇 타입의 매개변수를 활용한 *경로 동작* 예시입니다.

```Python hl_lines="1  3  12-16"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```

함수 안의 매개변수가 그들만의 데이터 타입을 갖고 있고, 또한 다음과 같은 날짜 조작을 할 수 있습니다. 예시:

```Python hl_lines="18-19"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```
