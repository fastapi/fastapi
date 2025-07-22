# 하위 응용프로그램 - 마운트

만약 각각의 독립적인 OpenAPI와 문서 UI를 갖는 두 개의 독립적인 FastAPI 응용프로그램이 필요하다면, 메인 어플리케이션에 하나 (또는 그 이상의) 하위-응용프로그램(들)을 “마운트"해서 사용할 수 있습니다.

## **FastAPI** 응용프로그램 마운트

“마운트"이란 완전히 “독립적인" 응용프로그램을 특정 경로에 추가하여 해당 하위 응용프로그램에서 선언된 *경로 동작*을 통해 해당 경로 아래에 있는 모든 작업들을 처리할 수 있도록 하는 것을 의미합니다.

### 최상단 응용프로그램

먼저, 메인, 최상단의 **FastAPI** 응용프로그램과 이것의 *경로 동작*을 생성합니다:

{* ../../docs_src/sub_applications/tutorial001.py hl[3, 6:8] *}

### 하위 응용프로그램

다음으로, 하위 응용프로그램과 이것의 *경로 동작*을 생성합니다:

이 하위 응용프로그램은 또 다른 표준 FastAPI 응용프로그램입니다. 다만 이것은 “마운트”될 것입니다:

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 14:16] *}

### 하위 응용프로그램 마운트

최상단 응용프로그램, `app`에 하위 응용프로그램, `subapi`를 마운트합니다.

이 예시에서, 하위 응용프로그램션은 `/subapi` 경로에 마운트 될 것입니다:

{* ../../docs_src/sub_applications/tutorial001.py hl[11, 19] *}

### 자동으로 생성된 API 문서 확인

이제, `uvicorn`으로 메인 응용프로그램을 실행하십시오. 당신의 파일이 `main.py`라면, 이렇게 실행합니다:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그리고 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 문서를 여십시오.

메인 응용프로그램의 *경로 동작*만을 포함하는, 메인 응용프로그램에 대한 자동 API 문서를 확인할 수 있습니다:

<img src="https://fastapi.tiangolo.com//img/tutorial/sub-applications/image01.png">

다음으로, <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>에서 하위 응용프로그램의 문서를 여십시오.

하위 경로 접두사 `/subapi` 아래에 선언된 *경로 동작* 을 포함하는, 하위 응용프로그램에 대한 자동 API 문서를 확인할 수 있습니다:

<img src="https://fastapi.tiangolo.com//img/tutorial/sub-applications/image02.png">

두 사용자 인터페이스 중 어느 하나를 사용해야하는 경우, 브라우저는 특정 응용프로그램 또는 하위 응용프로그램과 각각 통신할 수 있기 때문에 올바르게 동작할 것입니다.

### 기술적 세부사항: `root_path`

위에 설명된 것과 같이 하위 응용프로그램을 마운트하는 경우, FastAPI는 `root_path`라고 하는 ASGI 명세의 매커니즘을 사용하여 하위 응용프로그램에 대한 마운트 경로 통신을 처리합니다.

이를 통해, 하위 응용프로그램은 문서 UI를 위해 경로 접두사를 사용해야 한다는 사실을 인지합니다.

하위 응용프로그램에도 역시 다른 하위 응용프로그램을 마운트하는 것이 가능하며 FastAPI가 모든 `root_path` 들을 자동적으로 처리하기 때문에 모든 것은 올바르게 동작할 것입니다.

`root_path`와 이것을 사용하는 방법에 대해서는 [프록시의 뒷단](./behind-a-proxy.md){.internal-link target=_blank} 섹션에서 배울 수 있습니다.
