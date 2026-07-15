# 프론트엔드 { #frontend }

`app.frontend()`(또는 `router.frontend()`)로 정적 프론트엔드 애플리케이션을 제공할 수 있습니다.

이는 Vite를 사용하는 React, TanStack Router, Astro, Vue, Svelte, Angular, Solid 등과 같이 정적 파일을 생성하는 프론트엔드 도구에 유용합니다.

이러한 도구에서는 보통 다음과 같은 명령어로 프론트엔드를 빌드하는 단계가 있습니다:

```bash
npm run build
```

그러면 프론트엔드 파일이 들어 있는 `./dist/` 같은 디렉터리가 생성됩니다.

`app.frontend()`를 사용하면 이러한 프론트엔드 프레임워크에 필요한 규칙에 따라 해당 디렉터리를 제공할 수 있습니다.

**FastAPI**는 먼저 *경로 처리*를 확인합니다. 프론트엔드 파일은 일반 라우트와 매칭되지 않는 경우에만 확인되므로, API에는 영향을 주지 않습니다.

## 프론트엔드 제공하기 { #serve-a-frontend }

예를 들어 `npm run build`로 프론트엔드를 빌드한 후, 생성된 파일을 `dist` 같은 디렉터리에 넣습니다.

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

이렇게 하면 `/assets/app.js`에 대한 요청이 `dist/assets/app.js`를 제공할 수 있습니다.

**FastAPI** *경로 처리*도 있다면, *경로 처리*가 우선합니다.

## 클라이언트 사이드 라우팅 { #client-side-routing }

**single-page apps**(SPAs)를 포함한 많은 프론트엔드 애플리케이션은 클라이언트 사이드 라우팅을 사용합니다. `/dashboard/settings` 같은 경로는 실제 파일이 아닐 수 있지만, 프레임워크가 이를 처리합니다.

따라서 해당 URL에 직접 접근하는 경우(애플리케이션 안에서 탐색하는 대신), 백엔드는 `index.html`에서 프론트엔드 애플리케이션을 제공해야 합니다. 그러면 프론트엔드 프레임워크가 클라이언트 사이드 라우팅을 처리할 수 있습니다.

이를 위해 `fallback="index.html"`을 사용합니다:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI**는 브라우저 탐색처럼 보이는 `GET` 및 `HEAD` 요청에만 이 fallback을 사용합니다. JavaScript, CSS, 이미지처럼 누락된 파일은 여전히 `404`를 반환합니다.

`POST`나 `PUT` 같은 다른 메서드의 요청이 프론트엔드 fallback에만 매칭되는 경로로 들어와도 `404`를 반환합니다. 일반 **FastAPI** *경로 처리*는 여전히 프론트엔드 라우트보다 높은 우선순위를 가집니다.

/// tip | 팁

기본적으로 `fallback`은 `fallback="auto"` 값을 가집니다. 대부분의 경우 `fallback`을 지정할 필요가 없습니다. 자세한 내용은 아래를 읽어보세요.

///

이는 클라이언트 사이드 라우팅을 사용하는 많은 프론트엔드 애플리케이션에서 원하는 동작입니다. 예를 들어 TanStack Router를 사용하는 React, Vue, Angular, SvelteKit, Solid 등이 있습니다.

## 사용자 정의 404 페이지 { #custom-404-page }

누락된 프론트엔드 경로에 대해 정적 `404.html` 페이지를 제공할 수도 있습니다:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

이 응답은 `404` 상태 코드를 유지합니다.

이 경우 **FastAPI**는 누락된 프론트엔드 경로에 대해 `index.html`을 제공하지 않습니다. 대신 `404.html` 파일을 반환합니다.

/// tip | 팁

기본적으로 `fallback`은 `fallback="auto"` 값을 가집니다. 이를 사용하면 `404.html` 파일이 발견될 경우 자동으로 fallback으로 사용됩니다.

따라서 일반적으로 `fallback` 인자를 생략할 수 있습니다.

///

이는 Astro처럼 각 페이지에 대한 정적 HTML 파일을 생성하는 프론트엔드 도구에 유용합니다.

## Fallback 자동 설정 { #fallback-auto }

기본적으로 `app.frontend()`는 `fallback="auto"`를 사용합니다.

프론트엔드 디렉터리에 `404.html` 파일이 있으면, 누락된 프론트엔드 경로는 상태 코드 `404`와 함께 해당 파일을 제공합니다.

그렇지 않고 `index.html` 파일이 있으면, 누락된 브라우저 탐색 경로는 `index.html`을 제공합니다. 이는 클라이언트 사이드 라우팅을 사용하는 많은 프론트엔드 애플리케이션이 기대하는 동작입니다.

따라서 대부분의 경우 `fallback` 인자를 지정하지 않고 `app.frontend("/", directory="dist")`를 사용할 수 있습니다.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Fallback 비활성화 { #disable-fallback }

누락된 프론트엔드 경로에 대해 fallback 파일을 제공하고 싶지 않다면 `fallback=None`을 사용합니다:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

그러면 누락된 프론트엔드 경로는 일반 `404`를 반환합니다.

## 디렉터리 확인하기 { #check-directory }

기본적으로 `app.frontend()`는 애플리케이션이 생성될 때 디렉터리가 존재하는지 확인합니다.

이는 설정 오류를 일찍 발견하는 데 도움이 됩니다. 예를 들어 프론트엔드 빌드 출력 디렉터리가 없다면 **FastAPI**는 시작 시 오류를 발생시킵니다.

프론트엔드 파일이 나중에 생성된다면, 예를 들어 애플리케이션 객체가 생성된 후 별도의 빌드 단계에서 생성된다면, `check_dir=False`를 설정합니다:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

`check_dir=False`를 사용하면 **FastAPI**는 애플리케이션이 생성될 때 디렉터리를 확인하지 않습니다. 요청이 처리될 때 설정된 디렉터리가 여전히 없다면, 그때 **FastAPI**가 오류를 발생시킵니다.

## `APIRouter`와 함께 사용하기 { #use-it-with-apirouter }

프론트엔드 파일을 `APIRouter`에 추가하고 prefix와 함께 포함할 수도 있습니다:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

이 예제에서는 프론트엔드 경로가 `/app` 아래에서 제공됩니다.

다른 라우터에 있는 것을 포함하여, 애플리케이션의 모든 일반 *경로 처리*가 여전히 우선합니다.

## 의존성과 미들웨어 { #dependencies-and-middleware }

프론트엔드 응답은 일반 **FastAPI** 애플리케이션 안에서 실행되므로 HTTP 미들웨어가 적용됩니다.

애플리케이션, `APIRouter`, `include_router()`의 의존성도 프론트엔드 응답에 적용됩니다. 이는 쿠키 인증 등으로 프론트엔드를 보호하는 데 유용할 수 있습니다.

## 정적 빌드 출력만 사용하기 { #static-build-output-only }

`app.frontend()`는 프론트엔드 빌드에서 이미 생성된 파일을 제공합니다.

서버 사이드 렌더링은 실행하지 않습니다. 각 요청마다 서버에서 동적 렌더링이 필요한 프레임워크가 아니라, 정적 파일을 생성하는 프론트엔드 프레임워크를 위한 것입니다.
