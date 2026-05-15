# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - 명령줄 인터페이스">CLI</abbr>**는 FastAPI 애플리케이션을 서빙하고, FastAPI 프로젝트를 관리하는 등 다양한 작업에 사용할 수 있는 커맨드 라인 프로그램입니다.

FastAPI를 설치하면(예: `pip install "fastapi[standard]"`) 터미널에서 실행할 수 있는 커맨드 라인 프로그램이 함께 제공됩니다.

개발용으로 FastAPI 애플리케이션을 실행하려면 `fastapi dev` 명령어를 사용할 수 있습니다:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | 팁

프로덕션에서는 `fastapi dev` 대신 `fastapi run`을 사용합니다. 🚀

///

내부적으로 **FastAPI CLI**는 고성능의, 프로덕션에 적합한 ASGI 서버인 [Uvicorn](https://www.uvicorn.dev)을 사용합니다. 😎

`fastapi` CLI는 기본적으로 실행할 FastAPI 앱을 자동으로 감지하려고 시도합니다. `main.py` 파일 안의 `app`이라는 객체(또는 몇 가지 변형)가 있다고 가정합니다.

하지만 사용할 앱을 명시적으로 구성할 수도 있습니다.

## `pyproject.toml`에서 앱 `entrypoint` 구성하기 { #configure-the-app-entrypoint-in-pyproject-toml }

`pyproject.toml` 파일에서 앱이 어디에 있는지 다음과 같이 구성할 수 있습니다:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

이 `entrypoint`는 `fastapi` 명령어에 다음과 같이 앱을 임포트하라고 알려줍니다:

```python
from main import app
```

코드 구조가 다음과 같다면:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

`entrypoint`를 다음과 같이 설정합니다:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

이는 다음과 동일합니다:

```python
from backend.main import app
```

### 경로와 함께 `fastapi dev` { #fastapi-dev-with-path }

`fastapi dev` 명령어에 파일 경로를 전달할 수도 있으며, 그러면 사용할 FastAPI 앱 객체를 추정합니다:

```console
$ fastapi dev main.py
```

하지만 매번 `fastapi` 명령어를 호출할 때 올바른 경로를 전달하는 것을 기억해야 합니다.

또한 [VS Code 확장](editor-support.md)이나 [FastAPI Cloud](https://fastapicloud.com) 같은 다른 도구에서는 이를 찾지 못할 수도 있으므로, `pyproject.toml`의 `entrypoint`를 사용하는 것을 권장합니다.

## `fastapi dev` { #fastapi-dev }

`fastapi dev`를 실행하면 개발 모드가 시작됩니다.

기본적으로 **auto-reload**가 활성화되어 코드에 변경이 생기면 서버를 자동으로 다시 로드합니다. 이는 리소스를 많이 사용하며, 비활성화했을 때보다 안정성이 떨어질 수 있습니다. 개발 환경에서만 사용해야 합니다. 또한 컴퓨터가 자신과만 통신하기 위한(`localhost`) IP인 `127.0.0.1`에서 연결을 대기합니다.

## `fastapi run` { #fastapi-run }

`fastapi run`을 실행하면 프로덕션 모드로 FastAPI가 시작됩니다.

기본적으로 **auto-reload**는 비활성화되어 있습니다. 또한 사용 가능한 모든 IP 주소를 의미하는 `0.0.0.0`에서 연결을 대기하므로, 해당 컴퓨터와 통신할 수 있는 누구에게나 공개적으로 접근 가능해집니다. 보통 프로덕션에서는 이렇게 실행하며, 예를 들어 컨테이너에서 이런 방식으로 실행합니다.

대부분의 경우 위에 "termination proxy"를 두고 HTTPS를 처리하게(그리고 처리해야) 됩니다. 이는 애플리케이션을 배포하는 방식에 따라 달라지며, 제공자가 이 작업을 대신 처리해줄 수도 있고 직접 설정해야 할 수도 있습니다.

/// tip | 팁

자세한 내용은 [배포 문서](deployment/index.md)에서 확인할 수 있습니다.

///
