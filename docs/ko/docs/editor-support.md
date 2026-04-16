# 에디터 지원 { #editor-support }

공식 [FastAPI 확장](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)은 FastAPI 개발 워크플로우를 강화해 줍니다. *경로 처리* 탐색 및 이동, FastAPI Cloud 배포, 실시간 로그 스트리밍을 제공합니다.

확장에 대한 자세한 내용은 [GitHub 저장소](https://github.com/fastapi/fastapi-vscode)의 README를 참고하세요.

## 설치 및 설정 { #setup-and-installation }

**FastAPI 확장**은 [VS Code](https://code.visualstudio.com/)와 [Cursor](https://www.cursor.com/)에서 사용할 수 있습니다. 각 에디터의 확장(Extensions) 패널에서 "FastAPI"로 검색한 뒤 **FastAPI Labs**가 배포한 확장을 선택해 바로 설치할 수 있습니다. 또한 [vscode.dev](https://vscode.dev), [github.dev](https://github.dev) 같은 브라우저 기반 에디터에서도 동작합니다.

### 애플리케이션 자동 감지 { #application-discovery }

기본적으로 이 확장은 작업 공간에서 `FastAPI()`를 생성하는 파일을 스캔하여 FastAPI 애플리케이션을 자동으로 감지합니다. 프로젝트 구조상 자동 감지가 어려운 경우, `pyproject.toml`의 `[tool.fastapi]` 항목이나 VS Code 설정 `fastapi.entryPoint`에 모듈 표기(예: `myapp.main:app`)로 엔트리포인트를 지정할 수 있습니다.

## 기능 { #features }

- **경로 처리 탐색기** - 애플리케이션의 모든 <dfn title="경로, 엔드포인트">*경로 처리*</dfn>를 사이드바 트리 뷰로 확인합니다. 클릭하면 해당 경로 또는 라우터 정의로 바로 이동합니다.
- **경로 검색** - <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>)로 경로, 메서드, 이름으로 검색합니다.
- **CodeLens 탐색** - 테스트 클라이언트 호출(예: `client.get('/items')`) 위의 클릭 가능한 링크를 통해 해당 *경로 처리*로 즉시 이동하여 테스트와 구현 간을 빠르게 오갈 수 있습니다.
- **FastAPI Cloud에 배포** - [FastAPI Cloud](https://fastapicloud.com/)로 원클릭 배포를 지원합니다.
- **애플리케이션 로그 스트리밍** - FastAPI Cloud에 배포된 애플리케이션의 로그를 실시간으로 스트리밍하며, 레벨 필터링과 텍스트 검색을 제공합니다.

확장의 기능을 먼저 익혀보고 싶다면, 명령 팔레트(<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>, macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>)를 열고 "Welcome: Open walkthrough..."를 선택한 뒤 "Get started with FastAPI" walkthrough를 선택해 보세요.
