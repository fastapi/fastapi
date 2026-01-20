# 서버를 수동으로 실행하기 { #run-a-server-manually }

## `fastapi run` 명령 사용하기 { #use-the-fastapi-run-command }

요약하면, `fastapi run`을 사용해 FastAPI 애플리케이션을 서비스하세요:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

대부분의 경우에는 이것으로 동작합니다. 😎

예를 들어 이 명령은 컨테이너나 서버 등에서 **FastAPI** 앱을 시작할 때 사용할 수 있습니다.

## ASGI 서버 { #asgi-servers }

이제 조금 더 자세히 살펴보겠습니다.

FastAPI는 <abbr title="Asynchronous Server Gateway Interface">ASGI</abbr>라고 불리는, Python 웹 프레임워크와 서버를 만들기 위한 표준을 사용합니다. FastAPI는 ASGI 웹 프레임워크입니다.

원격 서버 머신에서 **FastAPI** 애플리케이션(또는 다른 ASGI 애플리케이션)을 실행하기 위해 필요한 핵심 요소는 **Uvicorn** 같은 ASGI 서버 프로그램입니다. `fastapi` 명령에는 기본으로 이것이 포함되어 있습니다.

다음을 포함해 여러 대안이 있습니다:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: 고성능 ASGI 서버.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: HTTP/2 및 Trio 등 여러 기능과 호환되는 ASGI 서버.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: Django Channels를 위해 만들어진 ASGI 서버.
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>: Python 애플리케이션을 위한 Rust HTTP 서버.
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>: NGINX Unit은 가볍고 다용도로 사용할 수 있는 웹 애플리케이션 런타임입니다.

## 서버 머신과 서버 프로그램 { #server-machine-and-server-program }

이름에 관해 기억해 둘 작은 디테일이 있습니다. 💡

"**server**"라는 단어는 보통 원격/클라우드 컴퓨터(물리 또는 가상 머신)와, 그 머신에서 실행 중인 프로그램(예: Uvicorn) 둘 다를 가리키는 데 사용됩니다.

일반적으로 "server"를 읽을 때, 이 두 가지 중 하나를 의미할 수 있다는 점을 기억하세요.

원격 머신을 가리킬 때는 **server**라고 부르는 것이 일반적이지만, **machine**, **VM**(virtual machine), **node**라고 부르기도 합니다. 이것들은 보통 Linux를 실행하는 원격 머신의 한 형태를 뜻하며, 그곳에서 프로그램을 실행합니다.

## 서버 프로그램 설치하기 { #install-the-server-program }

FastAPI를 설치하면 프로덕션 서버인 Uvicorn이 함께 설치되며, `fastapi run` 명령으로 시작할 수 있습니다.

하지만 ASGI 서버를 수동으로 설치할 수도 있습니다.

[가상 환경](../virtual-environments.md){.internal-link target=_blank}을 만들고 활성화한 다음, 서버 애플리케이션을 설치하세요.

예를 들어 Uvicorn을 설치하려면:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

다른 어떤 ASGI 서버 프로그램도 비슷한 과정이 적용됩니다.

/// tip | 팁

`standard`를 추가하면 Uvicorn이 권장되는 추가 의존성 몇 가지를 설치하고 사용합니다.

여기에는 `asyncio`를 고성능으로 대체할 수 있는 드롭인 대체재인 `uvloop`가 포함되며, 큰 동시성 성능 향상을 제공합니다.

`pip install "fastapi[standard]"` 같은 방식으로 FastAPI를 설치하면 `uvicorn[standard]`도 함께 설치됩니다.

///

## 서버 프로그램 실행하기 { #run-the-server-program }

ASGI 서버를 수동으로 설치했다면, 보통 FastAPI 애플리케이션을 임포트하기 위해 특별한 형식의 import string을 전달해야 합니다:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | 참고

`uvicorn main:app` 명령은 다음을 가리킵니다:

* `main`: 파일 `main.py`(Python "module").
* `app`: `main.py` 안에서 `app = FastAPI()` 라인으로 생성된 객체.

이는 다음과 동일합니다:

```Python
from main import app
```

///

각 ASGI 서버 프로그램의 대안도 비슷한 명령을 갖고 있으며, 자세한 내용은 각자의 문서를 참고하세요.

/// warning | 경고

Uvicorn과 다른 서버는 개발 중에 유용한 `--reload` 옵션을 지원합니다.

`--reload` 옵션은 훨씬 더 많은 리소스를 소비하고, 더 불안정합니다.

**개발** 중에는 큰 도움이 되지만, **프로덕션**에서는 사용하지 **말아야** 합니다.

///

## 배포 개념 { #deployment-concepts }

이 예제들은 서버 프로그램(예: Uvicorn)을 실행하여 **단일 프로세스**를 시작하고, 사전에 정한 포트(예: `80`)에서 모든 IP(`0.0.0.0`)로 들어오는 요청을 받도록 합니다.

이것이 기본 아이디어입니다. 하지만 보통은 다음과 같은 추가 사항들도 처리해야 합니다:

* 보안 - HTTPS
* 시작 시 자동 실행
* 재시작
* 복제(실행 중인 프로세스 수)
* 메모리
* 시작 전 선행 단계

다음 장들에서 이 각각의 개념을 어떻게 생각해야 하는지, 그리고 이를 다루기 위한 전략의 구체적인 예시를 더 알려드리겠습니다. 🚀
