# SDK 생성하기 { #generating-sdks }

**FastAPI**는 **OpenAPI** 사양을 기반으로 하므로, FastAPI의 API는 많은 도구가 이해할 수 있는 표준 형식으로 설명할 수 있습니다.

덕분에 여러 언어용 클라이언트 라이브러리(<abbr title="Software Development Kits - 소프트웨어 개발 키트">**SDKs**</abbr>), 최신 **문서**, 그리고 코드와 동기화된 **테스트** 또는 **자동화 워크플로**를 쉽게 생성할 수 있습니다.

이 가이드에서는 FastAPI 백엔드용 **TypeScript SDK**를 생성하는 방법을 배웁니다.

## 오픈 소스 SDK 생성기 { #open-source-sdk-generators }

다양하게 활용할 수 있는 옵션으로 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>가 있으며, **다양한 프로그래밍 언어**를 지원하고 OpenAPI 사양으로부터 SDK를 생성할 수 있습니다.

**TypeScript 클라이언트**의 경우 <a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a>는 TypeScript 생태계에 최적화된 경험을 제공하는 목적에 맞게 설계된 솔루션입니다.

더 많은 SDK 생성기는 <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a>에서 확인할 수 있습니다.

/// tip | 팁

FastAPI는 **OpenAPI 3.1** 사양을 자동으로 생성하므로, 사용하는 도구는 이 버전을 지원해야 합니다.

///

## FastAPI 스폰서의 SDK 생성기 { #sdk-generators-from-fastapi-sponsors }

이 섹션에서는 FastAPI를 후원하는 회사들이 제공하는 **벤처 투자 기반** 및 **기업 지원** 솔루션을 소개합니다. 이 제품들은 고품질로 생성된 SDK에 더해 **추가 기능**과 **통합**을 제공합니다.

✨ [**FastAPI 후원하기**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨를 통해, 이 회사들은 프레임워크와 그 **생태계**가 건강하고 **지속 가능**하게 유지되도록 돕습니다.

또한 이들의 후원은 FastAPI **커뮤니티**(여러분)에 대한 강한 헌신을 보여주며, **좋은 서비스**를 제공하는 것뿐 아니라, 견고하고 활발한 프레임워크인 FastAPI를 지원하는 데에도 관심이 있음을 나타냅니다. 🙇

예를 들어 다음을 사용해 볼 수 있습니다:

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

이 중 일부는 오픈 소스이거나 무료 티어를 제공하므로, 비용 부담 없이 사용해 볼 수 있습니다. 다른 상용 SDK 생성기도 있으며 온라인에서 찾을 수 있습니다. 🤓

## TypeScript SDK 만들기 { #create-a-typescript-sdk }

간단한 FastAPI 애플리케이션으로 시작해 보겠습니다:

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

*path operation*에서 요청 페이로드와 응답 페이로드에 사용하는 모델을 `Item`, `ResponseMessage` 모델로 정의하고 있다는 점에 주목하세요.

### API 문서 { #api-docs }

`/docs`로 이동하면, 요청으로 보낼 데이터와 응답으로 받을 데이터에 대한 **스키마(schemas)**가 있는 것을 볼 수 있습니다:

<img src="/img/tutorial/generate-clients/image01.png">

이 스키마는 앱에서 모델로 선언되었기 때문에 볼 수 있습니다.

그 정보는 앱의 **OpenAPI 스키마**에서 사용할 수 있고, 이후 API 문서에 표시됩니다.

OpenAPI에 포함된 모델의 동일한 정보가 **클라이언트 코드 생성**에 사용될 수 있습니다.

### Hey API { #hey-api }

모델이 포함된 FastAPI 앱이 준비되면, Hey API를 사용해 TypeScript 클라이언트를 생성할 수 있습니다. 가장 빠른 방법은 npx를 사용하는 것입니다.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

이 명령은 `./src/client`에 TypeScript SDK를 생성합니다.

<a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">`@hey-api/openapi-ts` 설치 방법</a>과 <a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">생성된 결과물</a>은 해당 웹사이트에서 확인할 수 있습니다.

### SDK 사용하기 { #using-the-sdk }

이제 클라이언트 코드를 import해서 사용할 수 있습니다. 아래처럼 사용할 수 있으며, 메서드에 대한 자동 완성이 제공되는 것을 확인할 수 있습니다:

<img src="/img/tutorial/generate-clients/image02.png">

보낼 페이로드에 대해서도 자동 완성이 제공됩니다:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | 팁

`name`과 `price`에 대한 자동 완성은 FastAPI 애플리케이션에서 `Item` 모델에 정의된 내용입니다.

///

전송하는 데이터에 대해 인라인 오류도 표시됩니다:

<img src="/img/tutorial/generate-clients/image04.png">

응답 객체도 자동 완성을 제공합니다:

<img src="/img/tutorial/generate-clients/image05.png">

## 태그가 있는 FastAPI 앱 { #fastapi-app-with-tags }

대부분의 경우 FastAPI 앱은 더 커지고, 서로 다른 *path operations* 그룹을 분리하기 위해 태그를 사용하게 될 가능성이 큽니다.

예를 들어 **items** 섹션과 **users** 섹션이 있고, 이를 태그로 분리할 수 있습니다:

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### 태그로 TypeScript 클라이언트 생성하기 { #generate-a-typescript-client-with-tags }

태그를 사용하는 FastAPI 앱에 대해 클라이언트를 생성하면, 일반적으로 생성된 클라이언트 코드도 태그를 기준으로 분리됩니다.

이렇게 하면 클라이언트 코드에서 항목들이 올바르게 정렬되고 그룹화됩니다:

<img src="/img/tutorial/generate-clients/image06.png">

이 경우 다음이 있습니다:

* `ItemsService`
* `UsersService`

### 클라이언트 메서드 이름 { #client-method-names }

현재 `createItemItemsPost` 같은 생성된 메서드 이름은 그다지 깔끔하지 않습니다:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...이는 클라이언트 생성기가 각 *path operation*에 대해 OpenAPI 내부의 **operation ID**를 사용하기 때문입니다.

OpenAPI는 모든 *path operations* 전체에서 operation ID가 각각 유일해야 한다고 요구합니다. 그래서 FastAPI는 operation ID가 유일하도록 **함수 이름**, **경로**, **HTTP method/operation**을 조합해 operation ID를 생성합니다.

하지만 다음에서 이를 개선하는 방법을 보여드리겠습니다. 🤓

## 커스텀 Operation ID와 더 나은 메서드 이름 { #custom-operation-ids-and-better-method-names }

클라이언트에서 **더 단순한 메서드 이름**을 갖도록, operation ID가 **생성되는 방식**을 **수정**할 수 있습니다.

이 경우 operation ID가 다른 방식으로도 **유일**하도록 보장해야 합니다.

예를 들어 각 *path operation*이 태그를 갖도록 한 다음, **태그**와 *path operation* **이름**(함수 이름)을 기반으로 operation ID를 생성할 수 있습니다.

### 유일 ID 생성 함수 커스터마이징 { #custom-generate-unique-id-function }

FastAPI는 각 *path operation*에 대해 **유일 ID**를 사용하며, 이는 **operation ID** 및 요청/응답에 필요한 커스텀 모델 이름에도 사용됩니다.

이 함수를 커스터마이징할 수 있습니다. 이 함수는 `APIRoute`를 받아 문자열을 반환합니다.

예를 들어 아래에서는 첫 번째 태그(대부분 태그는 하나만 있을 것입니다)와 *path operation* 이름(함수 이름)을 사용합니다.

그 다음 이 커스텀 함수를 `generate_unique_id_function` 매개변수로 **FastAPI**에 전달할 수 있습니다:

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### 커스텀 Operation ID로 TypeScript 클라이언트 생성하기 { #generate-a-typescript-client-with-custom-operation-ids }

이제 클라이언트를 다시 생성하면, 개선된 메서드 이름을 확인할 수 있습니다:

<img src="/img/tutorial/generate-clients/image07.png">

보시다시피, 이제 메서드 이름은 태그 다음에 함수 이름이 오며, URL 경로와 HTTP operation의 정보는 포함하지 않습니다.

### 클라이언트 생성기를 위한 OpenAPI 사양 전처리 { #preprocess-the-openapi-specification-for-the-client-generator }

생성된 코드에는 여전히 일부 **중복 정보**가 있습니다.

`ItemsService`(태그에서 가져옴)에 이미 **items**가 포함되어 있어 이 메서드가 items와 관련되어 있음을 알 수 있지만, 메서드 이름에도 태그 이름이 접두사로 붙어 있습니다. 😕

OpenAPI 전반에서는 operation ID가 **유일**하다는 것을 보장하기 위해 이 방식을 유지하고 싶을 수 있습니다.

하지만 생성된 클라이언트에서는, 클라이언트를 생성하기 직전에 OpenAPI operation ID를 **수정**해서 메서드 이름을 더 보기 좋고 **깔끔하게** 만들 수 있습니다.

OpenAPI JSON을 `openapi.json` 파일로 다운로드한 뒤, 아래와 같은 스크립트로 **접두사 태그를 제거**할 수 있습니다:

{* ../../docs_src/generate_clients/tutorial004_py39.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

이렇게 하면 operation ID가 `items-get_items` 같은 형태에서 `get_items`로 변경되어, 클라이언트 생성기가 더 단순한 메서드 이름을 생성할 수 있습니다.

### 전처리된 OpenAPI로 TypeScript 클라이언트 생성하기 { #generate-a-typescript-client-with-the-preprocessed-openapi }

이제 최종 결과가 `openapi.json` 파일에 있으므로, 입력 위치를 업데이트해야 합니다:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

새 클라이언트를 생성한 후에는 **깔끔한 메서드 이름**을 가지면서도, **자동 완성**, **인라인 오류** 등은 그대로 제공됩니다:

<img src="/img/tutorial/generate-clients/image08.png">

## 장점 { #benefits }

자동으로 생성된 클라이언트를 사용하면 다음에 대해 **자동 완성**을 받을 수 있습니다:

* 메서드
* 본문(body)의 요청 페이로드, 쿼리 파라미터 등
* 응답 페이로드

또한 모든 것에 대해 **인라인 오류**도 확인할 수 있습니다.

그리고 백엔드 코드를 업데이트한 뒤 프론트엔드를 **재생성(regenerate)**하면, 새 *path operations*가 메서드로 추가되고 기존 것은 제거되며, 그 밖의 변경 사항도 생성된 코드에 반영됩니다. 🤓

이는 무언가 변경되면 그 변경이 클라이언트 코드에도 자동으로 **반영**된다는 뜻입니다. 또한 클라이언트를 **빌드(build)**하면 사용된 데이터가 **불일치(mismatch)**할 경우 오류가 발생합니다.

따라서 운영 환경에서 최종 사용자에게 오류가 노출된 뒤 문제를 추적하는 대신, 개발 사이클 초기에 **많은 오류를 매우 빨리 감지**할 수 있습니다. ✨
