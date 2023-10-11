# 요청 본문

웹 브라우저와 같은 클라이언트로부터 당신의 API로 데이터를 보내야 할때, **요청 본문**를 통해서 보낼 수 있습니다.

**요청** 본문는 클라이언트에서 당신의 API로 보내진 데이터 입니다. **응답** 본문는 당신의 API가 클라이언트에게 보낸 데이터 입니다.


당신의 API는 반드시 항상 **응답** 본문를 보내야 합니다. 그러나 클라이언트는 항상 **요청** 본문를 보낼 필요는 없습니다.

**요청** 본문를 선언 할 때, 성능과 이점을 모두 가진 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> 모델들을 사용합니다.

!!! 정보
    데이터를 보낼때, 이 중 한가지를 사용해야합니다: `POST` (더 일반적입니다), `PUT`, `DELETE` 또는 `PATCH`.

    `GET`요청과 본문를 함께 보내는 것은 정식으로 정의되지 않은 동작이지만, FastAPI에서는 매우 복잡하거나 극단적인 사용 사례에 한하여 지원합니다.
    
    권장하지 않은 동작이므로 Swagger UI가 포함된 대화형 문서에서는 `GET`을 사용할 때 문서에 본문를 보여주지 않고, 또한 중간의 프록시에서 지원하지 않을 수 있습니다.

## Pydantic의 `BaseModel`가져오기

먼저, `Pydantic`으로부터 `BaseModel`을 가져옵니다. :

=== "Python 3.10+"

~~~python
```Python hl_lines="2"
{!> ../../../docs_src/body/tutorial001_py310.py!}
```
~~~

=== "Python 3.6+"

~~~python
```Python hl_lines="4"
{!> ../../../docs_src/body/tutorial001.py!}
```
~~~

## 데이터 모델 만들기

그리고 `BaseModel`을 상속하는 클래스에서 데이터 모델을 선언합니다.

모든 속성에 대한 표준 파이썬 유형을 사용합니다.

=== "Python 3.10+"

    ```Python hl_lines="5-9"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="7-11"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

쿼리 매개변수를 선언할 때와 마찬가지로, 모델 속성에 기본 값이 있으면 필수가 아닙니다. (기본 값에 특정한 값을 추가하지 않으면서 선택적으로 만들기 위해서는 `none`을 이용하면 됩니다.) 반대로, 모델 속성을 필수로 만드려면 기본값을 선언할 수 없습니다. 

예를 들어, 위의 모델은 다음과 같이 JSON "`object`"(또는 파이썬 `dict`)를 선언합니다.

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

..`description`과 `tax`는 선택 사항이며(기본값은`None`), 이 JSON "'object'" 또한 유효합니다.

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## 매개변수로 선언하기

*경로 작업*에 추가하기 위해서, 경로와 쿼리 매개변수를 정의한 것과 동일한 방식으로 선언 합니다.

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial001.py!}
    ```

...그리고 해당 유형을 당신이 만든 모델로 선언합니다, `Item`

## 결과

해당 파이썬 유형 선언만으로 FastAPI는 다음을 수행합니다.:

* 요청의 본문를 JSON으로 읽습니다.
* 대응되는 유형을 변환합니다.(필요한 경우)
* 데이터를 검증합니다.
    * 만약 데이터가 유효하지 않은 경우, 확실하고 명료한 오류를 반환하여 잘못된 데이터의 위치와 내용을 정확하게 나타냅니다.
* 매개변수에 수신된 데이터를 제공합니다. `item`
    * 함수에서 타입`Item`을 선언한 것처럼, 모든 속성과 그에 대한 유형에 대한 편집 기능(완성 기능 등)을 이용할 수 있습니다.
* 당신의 프로젝트에 적합하다면 모델에 대한 <a href="https://json-schema.org" class="external-link" target="_blank">JSON 스키마</a> 정의를 생성해서 원하는 다른 곳 어디에서나 사용할 수 있습니다.
* 이러한 스키마들은 생성된 OpenAPI 스키마의 일부가 되며 자동 문서 UI에서 사용됩니다.

## 자동 문서

당신이 만든 모델의 JSON스키마는 OpenAPI에서 생성한 스키마의 일부가 되며, 대화형 API문서에서 확인할 수 있습니다.

<img src="/img/tutorial/body/image01.png">

또한 필요한 각각의 *경로 작업* 내부의 API문서에서도 사용됩니다.

<img src="/img/tutorial/body/image02.png">

## 편집기 지원

편집기에서 코딩할 때, 함수 안에서 힌트들과 완성 기능을 이용할 수 있습니다. (Pydantic 모델이 아닌 `dict`를 받았다면 이런 일은 일어나지 않았을 것입니다.)

<img src="/img/tutorial/body/image03.png">

또한 잘못된 유형 작업에 대한 오류 검사 또한 실행합니다.

<img src="/img/tutorial/body/image04.png">

전체 프레임워크가 이 디자인 중심으로 설계된 것은 우연이 아닙니다.

그리고 모든 편집기에서 작동할 수 있도록 구현하기 전에, 디자인 단계에서 철저한 테스트를 거쳤습니다.

이를 지원하기 위해서 Pydantic 자체에도 몇가지 변경 사항이 있었습니다.

이전 스크린샷은 <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>에서 촬영하였습니다.

하지만 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>과 같은 다른 파이썬 편집기를 사용할 수도 있습니다.

<img src="/img/tutorial/body/image05.png">

!!! 팁
    만약 <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> 을 편집기로 쓴다면, <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a> 을 사용할 수 있습니다..

    다음을 통해 Pydantic 모델에 대한 편집기 지원을 개선시킵니다.
    
    * 자동 완성
    * 유형 확인
    * 리팩토링
    * 검색
    * 검사

## 모델 사용하기

함수 내에서 모델 객체의 모든 속성에 직접 접근할 수 있습니다.

=== "Python 3.10+"

    ```Python hl_lines="19"
    {!> ../../../docs_src/body/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="21"
    {!> ../../../docs_src/body/tutorial002.py!}
    ```

## 요청 본문+경로 매개변수

경로 매개변수와 요청 본문을 동시에 선언할 수 있습니다.

**FastAPI**는 경로 매개변수와 일치하는 함수 매개변수를 **경로에서 가져와야**하며 Pydantic 모델로 선언된 함수 매개변수를 **요청 본문에서 가져와야**함을 스스로 인지합니다.

=== "Python 3.10+"

    ```Python hl_lines="15-16"
    {!> ../../../docs_src/body/tutorial003_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="17-18"
    {!> ../../../docs_src/body/tutorial003.py!}
    ```

## 요청 본문+경로+쿼리 매개변수

또한 **본문, 경로**와 **쿼리**매개변수를 모두 동시에 선언할 수 있습니다.

**FastAPI**는 각각을 인식하고 올바른 위치에서 데이터를 가져옵니다.

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/body/tutorial004_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body/tutorial004.py!}
    ```

함수 매개변수는 다음과 같이 인식됩니다.

* 매개변수가 **경로**에서 선언된 경우, 경로 매개변수로 사용됩니다.
* 매개변수가 **단일 유형**(예: `int`, `float`, `str`, `bool` 등)인 경우, 쿼리 매개변수로 해석됩니다.
* 매개변수가 **Pydantic 모델** 유형으로 선언되면, 요청 **본문**으로 해석됩니다.

!!! 메모
    FastAPI는 기본값이 `None`이기 때문에 `q`의 값이 필수로 필요하지 않음을 알게 됩니다.

    `Union[str, None]`의 `Union`은 FastAPI에서 사용되지 않지만 편집기가 더 나은 기능을 제공하고 오류를 감지할 수 있게 합니다.

## Pydantic 없이

Pydantic 모델을 사용하고 싶지 않다면, **본문** 매개변수를 사용할 수 있습니다. [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.문서를 참고하세요.
