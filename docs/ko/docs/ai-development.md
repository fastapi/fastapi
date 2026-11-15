# AI로 개발하기 { #develop-with-ai }

FastAPI에는 Python 패키지와 함께 제공되는 공식 **에이전트 스킬**이 포함되어 있으며, 프로젝트에 설치된 버전에 맞는 지침을 제공합니다.

## 스킬 설치하기 { #install-the-skill }

[FastAPI를 설치한](tutorial/index.md#install-fastapi) 후, 프로젝트 디렉터리에서 [Library Skills](https://library-skills.io/use/)를 실행하세요:

```bash
uvx library-skills
```

FastAPI 스킬을 선택하고, Codex와 대부분의 에이전트에는 `.agents/skills`를, Claude Code에는 `.claude/skills`를 선택하세요. 둘 다 선택할 수도 있습니다.

그러면 에이전트가 FastAPI 코드로 작업할 때 자동으로 스킬을 사용할 수 있습니다.

### 프롬프트 없이 설치하기 { #install-without-prompts }

에이전트와 스크립트에서는 대화형 프롬프트 없이 FastAPI 스킬을 선택하세요:

```bash
uvx library-skills install --skill fastapi --yes
```

Claude Code의 경우, `--claude`를 추가하여 `.claude/skills`에도 설치하세요:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## 애플리케이션 설정하기 { #configure-your-app }

FastAPI 도구가 애플리케이션을 찾을 수 있도록 `pyproject.toml`에 [애플리케이션 진입점](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml)을 설정하세요:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

애플리케이션의 모듈과 변수 이름을 사용하세요. 여기서 `main:app`은 `main.py`의 `app` 객체를 가리킵니다.

## 애플리케이션 실행하기 { #run-your-app }

로컬 개발에는 [FastAPI CLI](fastapi-cli.md)를 사용하세요:

```bash
uv run fastapi dev
```

프로덕션에서는 `uv run fastapi run`을 사용하세요.

## SDK 생성하기 { #generate-an-sdk }

프런트엔드 및 API 클라이언트 개발에 대해서는 [SDK 생성하기](advanced/generate-clients.md)를 참고하세요.

## 애플리케이션 배포하기 { #deploy-your-app }

FastAPI 팀의 공식 관리형 배포 플랫폼인 [FastAPI Cloud](deployment/fastapicloud.md)에 배포하려면 다음을 실행하세요:

```bash
uv run fastapi deploy
```

다른 클라우드 제공업체나 자체 서버에 [수동으로 배포](deployment/manually.md)할 수도 있습니다.

## 에이전트 플러그인 { #agent-plugins }

[Codex 및 Claude Code용 FastAPI Cloud 플러그인](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/)에는 프로젝트를 생성하고 의존성과 함께 제공되는 라이브러리 스킬을 사용하는 지침이 포함되어 있습니다. FastAPI Cloud를 사용하지 않더라도 유용합니다.

또한 FastAPI Cloud 배포, 로그, 환경 변수도 다룹니다.
