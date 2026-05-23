# 서버 워커 - 워커와 함께 사용하는 Uvicorn { #server-workers-uvicorn-with-workers }

이전의 배포 개념들을 다시 확인해보겠습니다:

* 보안 - HTTPS
* 서버 시작 시 실행
* 재시작
* **복제(실행 중인 프로세스 수)**
* 메모리
* 시작하기 전의 이전 단계

지금까지 문서의 모든 튜토리얼을 참고하면서, `fastapi` 명령어처럼 Uvicorn을 실행하는 **서버 프로그램**을 사용해 **단일 프로세스**로 실행해 왔을 가능성이 큽니다.

애플리케이션을 배포할 때는 **다중 코어**를 활용하고 더 많은 요청을 처리할 수 있도록 **프로세스 복제**를 하고 싶을 가능성이 큽니다.

이전 장의 [배포 개념들](concepts.md)에서 본 것처럼, 사용할 수 있는 전략이 여러 가지 있습니다.

여기서는 `fastapi` 명령어를 사용하거나 `uvicorn` 명령어를 직접 사용해서, **워커 프로세스**와 함께 **Uvicorn**을 사용하는 방법을 보여드리겠습니다.

/// info | 정보

Docker나 Kubernetes 같은 컨테이너를 사용하고 있다면, 다음 장인 [컨테이너에서의 FastAPI - 도커](docker.md)에서 더 자세히 설명하겠습니다.

특히 **Kubernetes**에서 실행할 때는 워커를 사용하기보다는, 대신 **컨테이너당 단일 Uvicorn 프로세스 하나**를 실행하고 싶을 가능성이 크지만, 해당 내용은 그 장의 뒤에서 설명하겠습니다.

///

## 여러 워커 { #multiple-workers }

`--workers` 명령어 옵션으로 여러 워커를 시작할 수 있습니다:

//// tab | `fastapi`

`fastapi` 명령어를 사용한다면:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

`uvicorn` 명령어를 직접 사용하는 편이 좋다면:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

여기서 새로운 옵션은 `--workers`뿐이며, Uvicorn에게 워커 프로세스 4개를 시작하라고 알려줍니다.

또한 각 프로세스의 **PID**도 확인할 수 있는데, 상위 프로세스(이것이 **프로세스 관리자**)의 PID는 `27365`이고, 각 워커 프로세스의 PID는 `27368`, `27369`, `27370`, `27367`입니다.

## 배포 개념들 { #deployment-concepts }

여기서는 여러 **워커**를 사용해 애플리케이션 실행을 **병렬화**하고, CPU의 **다중 코어**를 활용하며, **더 많은 요청**을 제공할 수 있는 방법을 살펴봤습니다.

위의 배포 개념 목록에서 워커를 사용하는 것은 주로 **복제** 부분에 도움이 되고, **재시작**에도 약간 도움이 되지만, 나머지 항목들도 여전히 신경 써야 합니다:

* **보안 - HTTPS**
* **서버 시작 시 실행**
* ***재시작***
* 복제(실행 중인 프로세스 수)
* **메모리**
* **시작하기 전의 이전 단계**

## 컨테이너와 도커 { #containers-and-docker }

다음 장인 [컨테이너에서의 FastAPI - 도커](docker.md)에서는 다른 **배포 개념들**을 처리하기 위해 사용할 수 있는 몇 가지 전략을 설명하겠습니다.

단일 Uvicorn 프로세스를 실행하기 위해, **처음부터 여러분만의 이미지를 직접 빌드**하는 방법을 보여드리겠습니다. 이는 간단한 과정이며, **Kubernetes** 같은 분산 컨테이너 관리 시스템을 사용할 때 아마도 이렇게 하고 싶을 것입니다.

## 요약 { #recap }

`fastapi` 또는 `uvicorn` 명령어에서 `--workers` CLI 옵션을 사용해 여러 워커 프로세스를 실행하면, **멀티 코어 CPU**를 활용해 **여러 프로세스를 병렬로 실행**할 수 있습니다.

다른 배포 개념들을 직접 처리하면서 **자체 배포 시스템**을 구축하는 경우, 이러한 도구와 아이디어를 활용할 수 있습니다.

다음 장에서 컨테이너(예: Docker 및 Kubernetes)와 함께 사용하는 **FastAPI**에 대해 알아보세요. 해당 도구들이 다른 **배포 개념들**도 간단히 해결하는 방법이 있다는 것을 확인할 수 있습니다. ✨
