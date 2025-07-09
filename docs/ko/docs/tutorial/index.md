# 자습서 - 사용자 안내서

이 자습서는 단계별로 **FastAPI**의 대부분의 기능에 대해 설명합니다.

각 섹션은 이전 섹션에 기반하는 순차적인 구조로 작성되었지만, 각 주제로 구분되어 있기 때문에 필요에 따라 특정 섹션으로 바로 이동하여 필요한 내용을 바로 확인할 수 있습니다.

또한 향후에도 참조 자료로 쓰일 수 있도록 작성되었습니다.

그러므로 필요할 때에 다시 돌아와서 원하는 것을 정확히 찾을 수 있습니다.

## 코드 실행하기

모든 코드 블록은 복사하여 바로 사용할 수 있습니다(실제로 테스트된 파이썬 파일입니다).

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

코드를 작성하거나 복사, 편집할 때, 로컬 환경에서 실행하는 것을 **강력히 권장**합니다.

로컬 편집기에서 사용한다면, 모든 타입 검사와 자동완성 등 작성해야 하는 코드가 얼마나 적은지 보면서 FastAPI의 이점을 비로소 경험할 수 있습니다.


---

## FastAPI 설치

첫 번째 단계는 FastAPI를 설치하는 것입니다.

자습시에는 모든 선택적인 의존성 및 기능을 함께 설치하는 것을 추천합니다:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...이는 코드를 실행하는 서버로 사용할 수 있는 `uvicorn` 또한 포함하고 있습니다.

/// note | 참고

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

///

## 고급 사용자 안내서

이 **자습서 - 사용자 안내서** 다음에 읽을 수 있는 **고급 사용자 안내서**도 있습니다.

**고급 사용자 안내서**는 현재 문서를 기반으로 하고, 동일한 개념을 사용하며, 추가적인 기능들에 대해 설명합니다.

하지만 (지금 읽고 있는) **자습서 - 사용자 안내서**를 먼저 읽는 것을 권장합니다.

**자습서 - 사용자 안내서**만으로도 완전한 애플리케이션을 구축할 수 있도록 작성되었으며, 필요에 따라 **고급 사용자 안내서**의 추가적인 아이디어를 적용하여 다양한 방식으로 확장할 수 있습니다.
