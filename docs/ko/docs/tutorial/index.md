# 자습서 - 사용자 안내서 - 도입부

이 자습서는 **FastAPI**의 대부분의 기능을 단계별로 사용하는 방법을 보여줍니다.

각 섹션은 이전 섹션을 기반해서 점진적으로 만들어 졌지만, 주제를 구분하여 구성 되었기 때문에 특정 API 요구사항을 해결하기 위해 어떤 특정 항목이던지 직접 이동할 수 있습니다.

또한 향후 참조가 될 수 있도록 만들어졌습니다.

그러므로 다시 돌아와서 정확히 필요한 것을 볼 수 있습니다.

## 코드 실행하기

모든 코드 블록은 복사하고 직접 사용할 수 있습니다(실제로 테스트한 파이썬 파일입니다).

예제를 실행하려면 코드를 `main.py` 파일에 복사하고 다음을 사용하여 `uvicorn`을 시작합니다:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

코드를 작성하거나 복사, 편집할 때, 로컬에서 실행하는 것을 **강력히 장려**합니다.

편집기에서 이렇게 사용하면, 모든 타입 검사, 자동완성 등 작성해야 하는 코드가 얼마나 적은지 보면서 FastAPI의 장점을 실제로 확인할 수 있습니다.

---

## FastAPI 설치

첫 번째 단계는 FastAPI 설치입니다.

자습시에는 모든 선택적인 의존성 및 기능을 사용하여 설치할 수 있습니다:

<div class="termy">

```console
$ pip install fastapi[all]

---> 100%
```

</div>

...코드를 실행하는 서버로 사용할 수 있는 `uvicorn` 역시 포함하고 있습니다.

!!! note "참고"
    부분적으로 설치할 수도 있습니다.

    애플리케이션을 운영 환경에 배포하려는 경우 다음과 같이 합니다:

    ```
    pip install fastapi
    ```

    추가로 서버 역할을 하는 `uvicorn`을 설치합니다:

    ```
    pip install uvicorn
    ```

    사용하려는 각 선택적인 의존성에 대해서도 동일합니다.

## 고급 사용자 안내서

이 **자습서 - 사용자 안내서** 다음에 읽을 수 있는 **고급 사용자 안내서**도 있습니다.

**고급 사용자 안내서**는 현재 문서를 기반으로 하고, 동일한 개념을 사용하며, 추가 기능들을 알려줍니다.

하지만 (지금 읽고 있는) **자습서 - 사용자 안내서**를 먼저 읽는게 좋습니다.

**자습서 - 사용자 안내서**만으로 완전한 애플리케이션을 구축한 다음, **고급 사용자 안내서**의 몇 가지 추가 아이디어를 사용하여 필요에 따라 다양한 방식으로 확장할 수 있도록 설계되었습니다.
