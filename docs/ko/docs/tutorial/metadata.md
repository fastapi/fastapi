# 메타데이터 및 문서화 URL

**FastAPI** 응용 프로그램에서 다양한 메타데이터 구성을 사용자 맞춤 설정할 수 있습니다.

## API에 대한 메타데이터

OpenAPI 명세 및 자동화된 API 문서 UI에 사용되는 다음 필드를 설정할 수 있습니다:

| 매개변수 | 타입 | 설명 |
|----------|------|-------|
| `title` | `str` | API의 제목입니다. |
| `summary` | `str` | API에 대한 짧은 요약입니다. <small>OpenAPI 3.1.0, FastAPI 0.99.0부터 사용 가능</small> |
| `description` | `str` | API에 대한 짧은 설명입니다. 마크다운을 사용할 수 있습니다. |
| `version` | `string` | API의 버전입니다. OpenAPI의 버전이 아닌, 여러분의 애플리케이션의 버전을 나타냅니다. 예: `2.5.0` |
| `terms_of_service` | `str` | API 이용 약관의 URL입니다. 제공하는 경우 URL 형식이어야 합니다. |
| `contact` | `dict` | 노출된 API에 대한 연락처 정보입니다. 여러 필드를 포함할 수 있습니다. <details><summary><code>contact</code> 필드</summary><table><thead><tr><th>매개변수</th><th>타입</th><th>설명</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>연락처 인물/조직의 식별명입니다.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>연락처 정보가 담긴 URL입니다. URL 형식이어야 합니다.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>연락처 인물/조직의 이메일 주소입니다. 이메일 주소 형식이어야 합니다.</td></tr></tbody></table></details> |
| `license_info` | `dict` | 노출된 API의 라이선스 정보입니다. 여러 필드를 포함할 수 있습니다. <details><summary><code>license_info</code> 필드</summary><table><thead><tr><th>매개변수</th><th>타입</th><th>설명</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>필수</strong> (<code>license_info</code>가 설정된 경우). API에 사용된 라이선스 이름입니다.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>API에 대한 <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> 라이선스 표현입니다. <code>identifier</code> 필드는 <code>url</code> 필드와 상호 배타적입니다. <small>OpenAPI 3.1.0, FastAPI 0.99.0부터 사용 가능</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>API에 사용된 라이선스의 URL입니다. URL 형식이어야 합니다.</td></tr></tbody></table></details> |

다음과 같이 설정할 수 있습니다:

{* ../../docs_src/metadata/tutorial001.py hl[3:16,19:32] *}

/// tip

`description` 필드에 마크다운을 사용할 수 있으며, 출력에서 렌더링됩니다.

///

이 구성을 사용하면 문서 자동화(로 생성된) API 문서는 다음과 같이 보입니다:

<img src="/img/tutorial/metadata/image01.png">

## 라이선스 식별자

OpenAPI 3.1.0 및 FastAPI 0.99.0부터 `license_info`에 `identifier`를 URL 대신 설정할 수 있습니다.

예:

{* ../../docs_src/metadata/tutorial001_1.py hl[31] *}

## 태그에 대한 메타데이터

`openapi_tags` 매개변수를 사용하여 경로 작동을 그룹화하는 데 사용되는 태그에 추가 메타데이터를 추가할 수 있습니다.

리스트는 각 태그에 대해 하나의 딕셔너리를 포함해야 합니다.

각 딕셔너리에는 다음이 포함될 수 있습니다:

* `name` (**필수**): `tags` 매개변수에서 *경로 작동*과 `APIRouter`에 사용된 태그 이름과 동일한 `str`입니다.
* `description`: 태그에 대한 간단한 설명을 담은 `str`입니다. 마크다운을 사용할 수 있으며 문서 UI에 표시됩니다.
* `externalDocs`: 외부 문서를 설명하는 `dict`이며:
    * `description`: 외부 문서에 대한 간단한 설명을 담은 `str`입니다.
    * `url` (**필수**): 외부 문서의 URL을 담은 `str`입니다.

### 태그에 대한 메타데이터 생성

`users` 및 `items`에 대한 태그 예시와 함께 메타데이터를 생성하고 이를 `openapi_tags` 매개변수로 전달해 보겠습니다:

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

설명 안에 마크다운을 사용할 수 있습니다. 예를 들어 "login"은 굵게(**login**) 표시되고, "fancy"는 기울임꼴(_fancy_)로 표시됩니다.

/// tip

사용 중인 모든 태그에 메타데이터를 추가할 필요는 없습니다.

///

### 태그 사용

`tags` 매개변수를 *경로 작동* 및 `APIRouter`와 함께 사용하여 태그에 할당할 수 있습니다:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info

태그에 대한 자세한 내용은 [경로 작동 구성](path-operation-configuration.md#tags){.internal-link target=_blank}에서 읽어보세요.

///

### 문서 확인

이제 문서를 확인하면 모든 추가 메타데이터가 표시됩니다:

<img src="/img/tutorial/metadata/image02.png">

### 태그 순서

각 태그 메타데이터 딕셔너리의 순서는 문서 UI에 표시되는 순서를 정의합니다.

예를 들어, 알파벳 순서상 `users`는 `items` 뒤에 오지만, 우리는 `users` 메타데이터를 리스트의 첫 번째 딕셔너리로 추가했기 때문에 먼저 표시됩니다.

## OpenAPI URL

OpenAPI 구조는 기본적으로  `/openapi.json`에서 제공됩니다.

`openapi_url` 매개변수를 통해 이를 설정할 수 있습니다.

예를 들어, 이를 `/api/v1/openapi.json`에 제공하도록 설정하려면:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

OpenAPI 구조를 완전히 비활성화하려면 `openapi_url=None`으로 설정할 수 있으며, 이를 사용하여 문서화 사용자 인터페이스도 비활성화됩니다.

## 문서화 URL

포함된 두 가지 문서화 사용자 인터페이스를 설정할 수 있습니다:

* **Swagger UI**: `/docs`에서 제공됩니다.
    * `docs_url` 매개변수로 URL을 설정할 수 있습니다.
    * `docs_url=None`으로 설정하여 비활성화할 수 있습니다.
* **ReDoc**: `/redoc`에서 제공됩니다.
    * `redoc_url` 매개변수로 URL을 설정할 수 있습니다.
    * `redoc_url=None`으로 설정하여 비활성화할 수 있습니다.

예를 들어, Swagger UI를 `/documentation`에서 제공하고 ReDoc을 비활성화하려면:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
