# 서버 워커 - 구니콘과 유비콘

전단계에서의 배포 개념들을 다시 확인해보겠습니다:

* 보안 - HTTPS
* 서버 시작과 동시에 실행하기
* 재시작
* **복제본 (실행 중인 프로세스의 숫자)**
* 메모리
* 시작하기 전의 여러 단계들

지금까지 문서의 모든 튜토리얼을 참고하여 **단일 프로세스**로 Uvicorn과 같은 **서버 프로그램**을 실행했을 것입니다.

애플리케이션을 배포할 때 **다중 코어**를 활용하고 더 많은 요청을 처리할 수 있도록 **프로세스 복제본**이 필요합니다.

전 과정이었던 [배포 개념들](concepts.md){.internal-link target=_blank}에서 본 것처럼 여러가지 방법이 존재합니다.

지금부터 <a href="https://gunicorn.org/" class="external-link" target="_blank">**구니콘**</a>을 **유비콘 워커 프로세스**와 함께 사용하는 방법을 알려드리겠습니다.

/// info | 정보

만약 도커와 쿠버네티스 같은 컨테이너를 사용하고 있다면 다음 챕터 [FastAPI와 컨테이너 - 도커](docker.md){.internal-link target=_blank}에서 더 많은 정보를 얻을 수 있습니다.

특히, 쿠버네티스에서 실행할 때는 구니콘을 사용하지 않고 대신 컨테이너당 하나의 유비콘 프로세스를 실행하는 것이 좋습니다. 이 장의 뒷부분에서 설명하겠습니다.

///

## 구니콘과 유비콘 워커

**Gunicorn**은 **WSGI 표준**을 주로 사용하는 애플리케이션 서버입니다. 이것은 구니콘이 플라스크와 쟝고와 같은 애플리케이션을 제공할 수 있다는 것을 의미합니다. 구니콘 자체는 최신 **<a href="https://asgi.readthedocs.io/en/latest/" class="external-link" target="_blank">ASGI 표준</a>**을 사용하기 때문에 FastAPI와 호환되지 않습니다.

하지만 구니콘은 **프로세스 관리자**역할을 하고 사용자에게 특정 **워커 프로세스 클래스**를 알려줍니다. 그런 다음 구니콘은 해당 클래스를 사용하여 하나 이상의 **워커 프로세스**를 시작합니다.

그리고 **유비콘**은 **구니콘과 호환되는 워커 클래스**가 있습니다.

이 조합을 사용하여 구니콘은 **프로세스 관리자** 역할을 하며 **포트**와 **IP**를 관찰하고, **유비콘 클래스**를 실행하는 워커 프로세스로 통신 정보를 **전송**합니다.

그리고 나서 구니콘과 호환되는 **유비콘 워커** 클래스는 구니콘이 보낸 데이터를 FastAPI에서 사용하기 위한 ASGI 표준으로 변환하는 일을 담당합니다.

## 구니콘과 유비콘 설치하기

<div class="termy">

```console
$ pip install "uvicorn[standard]" gunicorn

---> 100%
```

</div>

이 명령어는 유비콘 `standard` 추가 패키지(좋은 성능을 위한)와 구니콘을 설치할 것입니다.

## 구니콘을 유비콘 워커와 함께 실행하기

설치 후 구니콘 실행하기:

<div class="termy">

```console
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

[19499] [INFO] Starting gunicorn 20.1.0
[19499] [INFO] Listening at: http://0.0.0.0:80 (19499)
[19499] [INFO] Using worker: uvicorn.workers.UvicornWorker
[19511] [INFO] Booting worker with pid: 19511
[19513] [INFO] Booting worker with pid: 19513
[19514] [INFO] Booting worker with pid: 19514
[19515] [INFO] Booting worker with pid: 19515
[19511] [INFO] Started server process [19511]
[19511] [INFO] Waiting for application startup.
[19511] [INFO] Application startup complete.
[19513] [INFO] Started server process [19513]
[19513] [INFO] Waiting for application startup.
[19513] [INFO] Application startup complete.
[19514] [INFO] Started server process [19514]
[19514] [INFO] Waiting for application startup.
[19514] [INFO] Application startup complete.
[19515] [INFO] Started server process [19515]
[19515] [INFO] Waiting for application startup.
[19515] [INFO] Application startup complete.
```

</div>

각 옵션이 무엇을 의미하는지 살펴봅시다:

* 이것은 유비콘과 똑같은 문법입니다. `main`은 파이썬 모듈 네임 "`main`"을 의미하므로 `main.py`파일을 뜻합니다. 그리고 `app`은 **FastAPI** 어플리케이션이 들어 있는 변수의 이름입니다.
    * `main:app`이 파이썬의 `import` 문법과 흡사한 면이 있다는 걸 알 수 있습니다:

        ```Python
        from main import app
        ```

    * 곧, `main:app`안에 있는 콜론의 의미는 파이썬에서 `from main import app`에서의 `import`와 같습니다.
* `--workers`: 사용할 워커 프로세스의 개수이며 숫자만큼의 유비콘 워커를 실행합니다. 이 예제에서는 4개의 워커를 실행합니다.
* `--worker-class`: 워커 프로세스에서 사용하기 위한 구니콘과 호환되는 워커클래스.
    * 이런식으로 구니콘이 import하여 사용할 수 있는 클래스를 전달해줍니다:

        ```Python
        import uvicorn.workers.UvicornWorker
        ```

* `--bind`: 구니콘이 관찰할 IP와 포트를 의미합니다. 콜론 (`:`)을 사용하여 IP와 포트를 구분합니다.
    * 만약에 `--bind 0.0.0.0:80` (구니콘 옵션) 대신 유비콘을 직접 실행하고 싶다면 `--host 0.0.0.0`과 `--port 80`을 사용해야 합니다.

출력에서 각 프로세스에 대한 **PID** (process ID)를 확인할 수 있습니다. (단순한 숫자입니다)

출력 내용:

* 구니콘 **프로세스 매니저**는 PID `19499`로 실행됩니다. (직접 실행할 경우 숫자가 다를 수 있습니다)
* 다음으로 `Listening at: http://0.0.0.0:80`을 시작합니다.
* 그런 다음 사용해야할 `uvicorn.workers.UvicornWorker`의 워커클래스를 탐지합니다.
* 그리고 PID `19511`, `19513`, `19514`, 그리고 `19515`를 가진 **4개의 워커**를 실행합니다.


또한 구니콘은 워커의 수를 유지하기 위해 **죽은 프로세스**를 관리하고 **재시작**하는 작업을 책임집니다. 이것은 이번 장 상단 목록의 **재시작** 개념을 부분적으로 도와주는 것입니다.

그럼에도 불구하고 필요할 경우 외부에서 **구니콘을 재시작**하고, 혹은 **서버를 시작할 때 실행**할 수 있도록 하고 싶어할 것입니다.

## 유비콘과 워커

유비콘은 몇 개의 **워커 프로세스**와 함께 실행할 수 있는 선택지가 있습니다.

그럼에도 불구하고, 유비콘은 워커 프로세스를 다루는 데에 있어서 구니콘보다 더 제한적입니다. 따라서 이 수준(파이썬 수준)의 프로세스 관리자를 사용하려면 구니콘을 프로세스 관리자로 사용하는 것이 좋습니다.

보통 이렇게 실행할 수 있습니다:

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

새로운 옵션인 `--workers`은 유비콘에게 4개의 워커 프로세스를 사용한다고 알려줍니다.

각 프로세스의 **PID**를 확인할 수 있습니다. `27365`는 상위 프로세스(**프로세스 매니저**), 그리고 각각의 워커프로세스는 `27368`, `27369`, `27370`, 그리고 `27367`입니다.

## 배포 개념들

여기에서는 **유비콘 워커 프로세스**를 관리하는 **구니콘**(또는 유비콘)을 사용하여 애플리케이션을 **병렬화**하고, CPU **멀티 코어**의 장점을 활용하고, **더 많은 요청**을 처리할 수 있는 방법을 살펴보았습니다.

워커를 사용하는 것은 배포 개념 목록에서 주로 **복제본** 부분과 **재시작**에 약간 도움이 되지만 다른 배포 개념들도 다루어야 합니다:

* **보안 - HTTPS**
* **서버 시작과 동시에 실행하기**
* ***재시작***
* 복제본 (실행 중인 프로세스의 숫자)
* **메모리**
* **시작하기 전의 여러 단계들**


## 컨테이너와 도커

다음 장인 [FastAPI와 컨테이너 - 도커](docker.md){.internal-link target=_blank}에서 다른 **배포 개념들**을 다루는 전략들을 알려드리겠습니다.

또한 간단한 케이스에서 사용할 수 있는, **구니콘과 유비콘 워커**가 포함돼 있는 **공식 도커 이미지**와 함께 몇 가지 기본 구성을 보여드리겠습니다.

그리고 단일 유비콘 프로세스(구니콘 없이)를 실행할 수 있도록 **사용자 자신의 이미지를 처음부터 구축**하는 방법도 보여드리겠습니다. 이는 간단한 과정이며, **쿠버네티스**와 같은 분산 컨테이너 관리 시스템을 사용할 때 수행할 작업입니다.

## 요약

당신은 **구니콘**(또는 유비콘)을 유비콘 워커와 함께 프로세스 관리자로 사용하여 **멀티-코어 CPU**를 활용하는 **멀티 프로세스를 병렬로 실행**할 수 있습니다.

다른 배포 개념을 직접 다루면서 **자신만의 배포 시스템**을 구성하는 경우 이러한 도구와 개념들을 활용할 수 있습니다.

다음 장에서 컨테이너(예: 도커 및 쿠버네티스)와 함께하는 **FastAPI**에 대해 배워보세요. 이러한 툴에는 다른 **배포 개념**들을 간단히 해결할 수 있는 방법이 있습니다. ✨
