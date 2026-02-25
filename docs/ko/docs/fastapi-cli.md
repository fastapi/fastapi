# FastAPI CLI { #fastapi-cli }

**FastAPI CLI**는 FastAPI 애플리케이션을 서빙하고, FastAPI 프로젝트를 관리하는 등 다양한 작업에 사용할 수 있는 커맨드 라인 프로그램입니다.

FastAPI를 설치할 때(예: `pip install "fastapi[standard]"`), `fastapi-cli`라는 패키지가 포함되며, 이 패키지는 터미널에서 `fastapi` 명령어를 제공합니다.

개발용으로 FastAPI 애플리케이션을 실행하려면 `fastapi dev` 명령어를 사용할 수 있습니다:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

`fastapi`라고 불리는 커맨드 라인 프로그램은 **FastAPI CLI**입니다.

FastAPI CLI는 Python 프로그램의 경로(예: `main.py`)를 받아 `FastAPI` 인스턴스(일반적으로 `app`으로 이름을 붙임)를 자동으로 감지하고, 올바른 임포트 과정을 결정한 다음 서빙합니다.

프로덕션에서는 대신 `fastapi run`을 사용합니다. 🚀

내부적으로 **FastAPI CLI**는 고성능의, 프로덕션에 적합한 ASGI 서버인 <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>을 사용합니다. 😎

## `fastapi dev` { #fastapi-dev }

`fastapi dev`를 실행하면 개발 모드가 시작됩니다.

기본적으로 **auto-reload**가 활성화되어 코드에 변경이 생기면 서버를 자동으로 다시 로드합니다. 이는 리소스를 많이 사용하며, 비활성화했을 때보다 안정성이 떨어질 수 있습니다. 개발 환경에서만 사용해야 합니다. 또한 컴퓨터가 자신과만 통신하기 위한(`localhost`) IP인 `127.0.0.1`에서 연결을 대기합니다.

## `fastapi run` { #fastapi-run }

`fastapi run`을 실행하면 기본적으로 프로덕션 모드로 FastAPI가 시작됩니다.

기본적으로 **auto-reload**는 비활성화되어 있습니다. 또한 사용 가능한 모든 IP 주소를 의미하는 `0.0.0.0`에서 연결을 대기하므로, 해당 컴퓨터와 통신할 수 있는 누구에게나 공개적으로 접근 가능해집니다. 보통 프로덕션에서는 이렇게 실행하며, 예를 들어 컨테이너에서 이런 방식으로 실행합니다.

대부분의 경우 위에 "termination proxy"를 두고 HTTPS를 처리하게(그리고 처리해야) 됩니다. 이는 애플리케이션을 배포하는 방식에 따라 달라지며, 제공자가 이 작업을 대신 처리해줄 수도 있고 직접 설정해야 할 수도 있습니다.

/// tip | 팁

자세한 내용은 [배포 문서](deployment/index.md){.internal-link target=_blank}에서 확인할 수 있습니다.

///
