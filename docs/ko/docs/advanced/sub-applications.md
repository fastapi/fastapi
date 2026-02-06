# 하위 응용프로그램 - 마운트 { #sub-applications-mounts }

각각의 독립적인 OpenAPI와 문서 UI를 갖는 두 개의 독립적인 FastAPI 애플리케이션이 필요하다면, 메인 앱을 두고 하나(또는 그 이상)의 하위 응용프로그램을 "마운트"할 수 있습니다.

## **FastAPI** 애플리케이션 마운트 { #mounting-a-fastapi-application }

"마운트"란 완전히 "독립적인" 애플리케이션을 특정 경로에 추가하고, 그 하위 응용프로그램에 선언된 _경로 처리_로 해당 경로 아래의 모든 것을 처리하도록 하는 것을 의미합니다.

### 최상위 애플리케이션 { #top-level-application }

먼저, 메인 최상위 **FastAPI** 애플리케이션과 그 *경로 처리*를 생성합니다:

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[3, 6:8] *}

### 하위 응용프로그램 { #sub-application }

그 다음, 하위 응용프로그램과 그 *경로 처리*를 생성합니다.

이 하위 응용프로그램은 또 다른 표준 FastAPI 애플리케이션이지만, "마운트"될 애플리케이션입니다:

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[11, 14:16] *}

### 하위 응용프로그램 마운트 { #mount-the-sub-application }

최상위 애플리케이션 `app`에서 하위 응용프로그램 `subapi`를 마운트합니다.

이 경우 `/subapi` 경로에 마운트됩니다:

{* ../../docs_src/sub_applications/tutorial001_py39.py hl[11, 19] *}

### 자동 API 문서 확인 { #check-the-automatic-api-docs }

이제 파일과 함께 `fastapi` 명령을 실행하세요:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

그리고 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 문서를 여세요.

메인 앱의 자동 API 문서를 보게 될 것이며, 메인 앱 자체의 _경로 처리_만 포함됩니다:

<img src="/img/tutorial/sub-applications/image01.png">

그 다음, <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>에서 하위 응용프로그램의 문서를 여세요.

하위 응용프로그램의 자동 API 문서를 보게 될 것이며, 하위 경로 접두사 `/subapi` 아래에 올바르게 포함된 하위 응용프로그램 자체의 _경로 처리_만 포함됩니다:

<img src="/img/tutorial/sub-applications/image02.png">

두 사용자 인터페이스 중 어느 것과 상호작용을 시도하더라도 올바르게 동작할 것입니다. 브라우저가 각 특정 앱 또는 하위 앱과 통신할 수 있기 때문입니다.

### 기술적 세부사항: `root_path` { #technical-details-root-path }

위에서 설명한 대로 하위 응용프로그램을 마운트하면, FastAPI는 ASGI 명세의 메커니즘인 `root_path`를 사용해 하위 응용프로그램에 대한 마운트 경로를 전달하는 작업을 처리합니다.

이렇게 하면 하위 응용프로그램은 문서 UI를 위해 해당 경로 접두사를 사용해야 한다는 것을 알게 됩니다.

또한 하위 응용프로그램도 자체적으로 하위 앱을 마운트할 수 있으며, FastAPI가 이 모든 `root_path`를 자동으로 처리하기 때문에 모든 것이 올바르게 동작합니다.

`root_path`와 이를 명시적으로 사용하는 방법에 대해서는 [프록시 뒤](behind-a-proxy.md){.internal-link target=_blank} 섹션에서 더 알아볼 수 있습니다.
