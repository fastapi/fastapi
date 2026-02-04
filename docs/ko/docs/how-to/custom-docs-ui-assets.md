# 커스텀 Docs UI 정적 에셋(자체 호스팅) { #custom-docs-ui-static-assets-self-hosting }

API 문서는 **Swagger UI**와 **ReDoc**을 사용하며, 각각 JavaScript와 CSS 파일이 필요합니다.

기본적으로 이러한 파일은 <abbr title="Content Delivery Network - 콘텐츠 전송 네트워크: 일반적으로 여러 서버로 구성되어 JavaScript와 CSS 같은 정적 파일을 제공하는 서비스입니다. 보통 클라이언트에 더 가까운 서버에서 파일을 제공해 성능을 향상시키는 데 사용됩니다.">CDN</abbr>에서 제공됩니다.

하지만 이를 커스터마이징할 수 있으며, 특정 CDN을 지정하거나 파일을 직접 제공할 수도 있습니다.

## JavaScript와 CSS용 커스텀 CDN { #custom-cdn-for-javascript-and-css }

예를 들어 다른 <abbr title="Content Delivery Network">CDN</abbr>을 사용하고 싶다고 해봅시다. 예를 들면 `https://unpkg.com/`을 사용하려는 경우입니다.

이는 예를 들어 특정 국가에서 일부 URL을 제한하는 경우에 유용할 수 있습니다.

### 자동 문서 비활성화하기 { #disable-the-automatic-docs }

첫 번째 단계는 자동 문서를 비활성화하는 것입니다. 기본적으로 자동 문서는 기본 CDN을 사용하기 때문입니다.

비활성화하려면 `FastAPI` 앱을 생성할 때 해당 URL을 `None`으로 설정하세요:

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[8] *}

### 커스텀 문서 포함하기 { #include-the-custom-docs }

이제 커스텀 문서를 위한 *경로 처리*를 만들 수 있습니다.

FastAPI 내부 함수를 재사용해 문서용 HTML 페이지를 생성하고, 필요한 인자를 전달할 수 있습니다:

* `openapi_url`: 문서 HTML 페이지가 API의 OpenAPI 스키마를 가져올 수 있는 URL입니다. 여기서는 `app.openapi_url` 속성을 사용할 수 있습니다.
* `title`: API의 제목입니다.
* `oauth2_redirect_url`: 기본값을 사용하려면 여기서 `app.swagger_ui_oauth2_redirect_url`을 사용할 수 있습니다.
* `swagger_js_url`: Swagger UI 문서의 HTML이 **JavaScript** 파일을 가져올 수 있는 URL입니다. 커스텀 CDN URL입니다.
* `swagger_css_url`: Swagger UI 문서의 HTML이 **CSS** 파일을 가져올 수 있는 URL입니다. 커스텀 CDN URL입니다.

ReDoc도 마찬가지입니다...

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[2:6,11:19,22:24,27:33] *}

/// tip | 팁

`swagger_ui_redirect`에 대한 *경로 처리*는 OAuth2를 사용할 때 도움이 되는 헬퍼입니다.

API를 OAuth2 provider와 통합하면 인증을 수행한 뒤 획득한 자격 증명으로 API 문서로 다시 돌아올 수 있습니다. 그리고 실제 OAuth2 인증을 사용해 API와 상호작용할 수 있습니다.

Swagger UI가 이 과정을 백그라운드에서 처리해 주지만, 이를 위해 이 "redirect" 헬퍼가 필요합니다.

///

### 테스트용 *경로 처리* 만들기 { #create-a-path-operation-to-test-it }

이제 모든 것이 제대로 동작하는지 테스트할 수 있도록 *경로 처리*를 하나 만드세요:

{* ../../docs_src/custom_docs_ui/tutorial001_py39.py hl[36:38] *}

### 테스트하기 { #test-it }

이제 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 문서에 접속한 뒤 페이지를 새로고침하면, 새 CDN에서 에셋을 불러오는 것을 확인할 수 있습니다.

## 문서용 JavaScript와 CSS 자체 호스팅하기 { #self-hosting-javascript-and-css-for-docs }

JavaScript와 CSS를 자체 호스팅하는 것은 예를 들어, 오프라인 상태이거나 외부 인터넷에 접근할 수 없는 환경, 또는 로컬 네트워크에서도 앱이 계속 동작해야 할 때 유용할 수 있습니다.

여기서는 동일한 FastAPI 앱에서 해당 파일을 직접 제공하고, 문서가 이를 사용하도록 설정하는 방법을 살펴봅니다.

### 프로젝트 파일 구조 { #project-file-structure }

프로젝트 파일 구조가 다음과 같다고 해봅시다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

이제 해당 정적 파일을 저장할 디렉터리를 만드세요.

새 파일 구조는 다음과 같을 수 있습니다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### 파일 다운로드하기 { #download-the-files }

문서에 필요한 정적 파일을 다운로드해서 `static/` 디렉터리에 넣으세요.

각 링크를 우클릭한 뒤 "링크를 다른 이름으로 저장..."과 비슷한 옵션을 선택하면 될 것입니다.

**Swagger UI**는 다음 파일을 사용합니다:

* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
* <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

**ReDoc**은 다음 파일을 사용합니다:

* <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

이후 파일 구조는 다음과 같을 수 있습니다:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 정적 파일 제공하기 { #serve-the-static-files }

* `StaticFiles`를 import합니다.
* 특정 경로에 `StaticFiles()` 인스턴스를 "마운트(mount)"합니다.

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[7,11] *}

### 정적 파일 테스트하기 { #test-the-static-files }

애플리케이션을 시작하고 <a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a>로 이동하세요.

**ReDoc**용 매우 긴 JavaScript 파일이 보일 것입니다.

예를 들어 다음과 같이 시작할 수 있습니다:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

이는 앱에서 정적 파일을 제공할 수 있고, 문서용 정적 파일을 올바른 위치에 배치했다는 것을 확인해 줍니다.

이제 문서가 이 정적 파일을 사용하도록 앱을 설정할 수 있습니다.

### 정적 파일을 위한 자동 문서 비활성화하기 { #disable-the-automatic-docs-for-static-files }

커스텀 CDN을 사용할 때와 마찬가지로, 첫 단계는 자동 문서를 비활성화하는 것입니다. 자동 문서는 기본적으로 CDN을 사용합니다.

비활성화하려면 `FastAPI` 앱을 생성할 때 해당 URL을 `None`으로 설정하세요:

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[9] *}

### 정적 파일을 위한 커스텀 문서 포함하기 { #include-the-custom-docs-for-static-files }

그리고 커스텀 CDN을 사용할 때와 동일한 방식으로, 이제 커스텀 문서를 위한 *경로 처리*를 만들 수 있습니다.

다시 한 번, FastAPI 내부 함수를 재사용해 문서용 HTML 페이지를 생성하고, 필요한 인자를 전달할 수 있습니다:

* `openapi_url`: 문서 HTML 페이지가 API의 OpenAPI 스키마를 가져올 수 있는 URL입니다. 여기서는 `app.openapi_url` 속성을 사용할 수 있습니다.
* `title`: API의 제목입니다.
* `oauth2_redirect_url`: 기본값을 사용하려면 여기서 `app.swagger_ui_oauth2_redirect_url`을 사용할 수 있습니다.
* `swagger_js_url`: Swagger UI 문서의 HTML이 **JavaScript** 파일을 가져올 수 있는 URL입니다. **이제는 여러분의 앱이 직접 제공하는 파일입니다**.
* `swagger_css_url`: Swagger UI 문서의 HTML이 **CSS** 파일을 가져올 수 있는 URL입니다. **이제는 여러분의 앱이 직접 제공하는 파일입니다**.

ReDoc도 마찬가지입니다...

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[2:6,14:22,25:27,30:36] *}

/// tip | 팁

`swagger_ui_redirect`에 대한 *경로 처리*는 OAuth2를 사용할 때 도움이 되는 헬퍼입니다.

API를 OAuth2 provider와 통합하면 인증을 수행한 뒤 획득한 자격 증명으로 API 문서로 다시 돌아올 수 있습니다. 그리고 실제 OAuth2 인증을 사용해 API와 상호작용할 수 있습니다.

Swagger UI가 이 과정을 백그라운드에서 처리해 주지만, 이를 위해 이 "redirect" 헬퍼가 필요합니다.

///

### 정적 파일 테스트용 *경로 처리* 만들기 { #create-a-path-operation-to-test-static-files }

이제 모든 것이 제대로 동작하는지 테스트할 수 있도록 *경로 처리*를 하나 만드세요:

{* ../../docs_src/custom_docs_ui/tutorial002_py39.py hl[39:41] *}

### 정적 파일 UI 테스트하기 { #test-static-files-ui }

이제 WiFi 연결을 끊고 <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>에서 문서에 접속한 뒤 페이지를 새로고침해 보세요.

인터넷이 없어도 API 문서를 보고, API와 상호작용할 수 있을 것입니다.
