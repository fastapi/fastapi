# 프론트엔드 { #frontend }

정적 프론트엔드 앱을 `app.frontend()` (또는 `router.frontend()`)로 제공할 수 있습니다.

이는 React + Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid 등 정적 파일을 생성하는 프론트엔드 도구에 유용합니다.

이러한 도구들은 보통 다음과 같은 명령어로 프론트엔드를 빌드하는 단계가 있습니다:

```bash
npm run build
```

이 단계는 프론트엔드 파일이 들어 있는 `./dist/` 같은 디렉터리를 생성합니다.

`app.frontend()`를 사용하면 이러한 프론트엔드 프레임워크가 요구하는 규칙에 따라 해당 디렉터리를 제공할 수 있습니다.

**FastAPI**는 *path operations*를 먼저 확인합니다. 일치하는 일반 경로가 없을 때에만 프론트엔드 파일을 확인하므로, API에는 영향을 주지 않습니다.

## 프론트엔드 제공하기 { #serve-a-frontend }

프론트엔드를 빌드한 후 (예: `npm run build`), 생성된 파일을 `dist` 같은 디렉터리에 넣습니다.

프로젝트 구조는 다음과 같을 수 있습니다:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

그런 다음 `app.frontend()`로 제공합니다:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

이렇게 하면 `/assets/app.js` 요청 시 `dist/assets/app.js`가 제공됩니다.

만약 **FastAPI** *path operation*도 함께 정의되어 있다면, *path operation*이 우선합니다.

## 클라이언트 사이드 라우팅 { #client-side-routing }

**단일 페이지 앱**(SPA)을 포함한 많은 프론트엔드 앱은 클라이언트 사이드 라우팅을 사용합니다. `/dashboard/settings` 같은 경로는 실제 파일이 아닐 수 있지만, 프레임워크가 이를 처리합니다.

따라서 (앱을 통해 이동하는 대신) 해당 URL에 직접 접근하는 경우, 백엔드는 `index.html`을 통해 프론트엔드 앱을 제공해야 하며, 이를 통해 프론트엔드 프레임워크가 클라이언트 사이드 라우팅을 처리할 수 있게 됩니다.

이를 위해 `fallback="index.html"`을 사용합니다:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI**는 브라우저 내비게이션처럼 보이는 요청에 대해서만 이 fallback을 사용합니다. JavaScript, CSS, 이미지처럼 누락된 파일들은 여전히 `404`를 반환합니다.

/// tip

기본적으로 `fallback`은 `fallback="auto"` 값을 가집니다. 대부분의 경우 `fallback`을 명시할 필요가 없습니다. 자세한 내용은 아래를 참고하세요.

///

이는 React + TanStack Router, Vue, Angular, SvelteKit, Solid처럼 클라이언트 사이드 라우팅을 사용하는 많은 프론트엔드 앱에서 원하는 동작입니다.

## 커스텀 404 페이지 { #custom-404-page }

누락된 프론트엔드 경로에 대해 정적 `404.html` 페이지를 제공할 수도 있습니다:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

해당 응답은 `404` 상태 코드를 유지합니다.

이 경우 **FastAPI**는 누락된 프론트엔드 경로에 대해 `index.html`을 제공하지 않습니다. 대신 `404.html` 파일을 반환합니다.

/// tip

기본적으로 `fallback`은 `fallback="auto"` 값을 가집니다. 이로 인해 `404.html` 파일이 있으면 자동으로 fallback으로 사용됩니다.

따라서 보통은 `fallback` 인자를 생략할 수 있습니다.

///

이는 Astro처럼 페이지마다 정적 HTML 파일을 생성하는 프론트엔드 도구에 유용합니다.

## 자동 Fallback { #fallback-auto }

기본적으로 `app.frontend()`는 `fallback="auto"`를 사용합니다.

프론트엔드 디렉터리에 `404.html` 파일이 있으면, 누락된 프론트엔드 경로는 해당 파일을 `404` 상태 코드와 함께 제공합니다.

그렇지 않고 `index.html` 파일이 있으면, 누락된 브라우저 내비게이션 경로는 `index.html`을 제공하며, 이는 클라이언트 사이드 라우팅을 사용하는 많은 프론트엔드 앱이 기대하는 동작입니다.

따라서 대부분의 경우 `fallback` 인자를 명시하지 않고 `app.frontend("/", directory="dist")`만 사용할 수 있습니다.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Fallback 비활성화 { #disable-fallback }

누락된 프론트엔드 경로에 대해 fallback 파일을 제공하고 싶지 않다면 `fallback=None`을 사용합니다:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

그러면 누락된 프론트엔드 경로는 일반적인 `404`를 반환합니다.

## 디렉터리 확인 { #check-directory }

기본적으로 `app.frontend()`는 앱이 생성될 때 디렉터리가 존재하는지 확인합니다.

이는 설정 오류를 일찍 발견하는 데 도움이 됩니다. 예를 들어, 프론트엔드 빌드 출력 디렉터리가 없다면 **FastAPI**는 시작 시점에 오류를 발생시킵니다.

만약 프론트엔드 파일이 나중에 생성되는 경우 (예: 앱 객체가 생성된 후 별도의 빌드 단계에서), `check_dir=False`로 설정합니다:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

`check_dir=False`를 사용하면 **FastAPI**는 앱이 생성될 때 디렉터리를 확인하지 않습니다. 요청이 처리되는 시점에도 구성된 디렉터리가 여전히 없다면, **FastAPI**는 그때 오류를 발생시킵니다.

## `APIRouter`와 함께 사용하기 { #use-it-with-apirouter }

프론트엔드 파일을 `APIRouter`에 추가하고 prefix와 함께 포함시킬 수도 있습니다:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

이 예시에서 프론트엔드 경로는 `/app` 아래에서 제공됩니다.

다른 라우터에 있는 것을 포함해, 앱에 정의된 일반적인 *path operations*는 여전히 우선합니다.

## 정적 빌드 출력 전용 { #static-build-output-only }

`app.frontend()`는 프론트엔드 빌드로 이미 생성된 파일을 제공합니다.

서버 사이드 렌더링은 실행하지 않습니다. 정적 파일을 생성하는 프론트엔드 프레임워크를 위한 것이며, 각 요청마다 서버에서 동적 렌더링이 필요한 프레임워크를 위한 것은 아닙니다.
