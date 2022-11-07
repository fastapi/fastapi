# 수동으로 서버를 실행하는법 - Uvicorn

우선 원격 서버 시스템에서 **FastAPI** 응용 프로그램을 실행하기 위해 필요한 것은 Uvicorn과 같은 ASGI 서버 프로그램입니다.

여기 3가지 방법이 있습니다.:

* <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>: a high performance ASGI server.
* <a href="https://pgjones.gitlab.io/hypercorn/" class="external-link" target="_blank">Hypercorn</a>: an ASGI server compatible with HTTP/2 and Trio among other features.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: the ASGI server built for Django Channels.

## 서버 머신과 서버 프로그램

이름에 대해 염두에 두어야 할 작은 세부 사항이 있습니다. 💡

"**서버**"라는 단어는 일반적으로 원격/클라우드 컴퓨터(물리적 또는 가상 머신)와 그 컴퓨터에서 실행 중인 프로그램(예: Uvicorn)을 모두 나타내는 데 사용됩니다.

일반적으로 "서버"를 읽을 때 이 두 가지 뜻 중 하나를 언급한다는 것을 염두에 두십시오.

원격 머신을 언급할 때 일반적으로 **서버**라고 부르지만 **머신**, **VM**(가상 머신), **노드**라고도 합니다. 이들은 모두 일종의 프로그램을 실행하는 원격 시스템을 나타내며 일반적으로 리눅스를 사용합니다.

## 서버 프로그램을 설치하는 법

아래와 같이 ASGI 호환 서버를 설치할 수 있습니다.:

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>, uvloop와 http 툴을 기반으로 구축된 초고속 ASGI 서버입니다.

    <div class="termy">

    ```console
    $ pip install "uvicorn[standard]"

    ---> 100%
    ```

    </div>

    !!! tip
        Uvicorn은 'standard' 구문을 추가함으로써 몇 가지 권장되는 추가 종속성을 설치하고 사용할 것입니다.

        그것은 'asyncio'를 큰 코드 변환없이 대체하는 고성능의 `uvloop`를 포함하며, 큰 동시성 성능 향상을 제공합니다.

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>, HTTP/2와 호환되는 ASGI 서버.

    <div class="termy">

    ```console
    $ pip install hypercorn

    ---> 100%
    ```

    </div>

    ...또는 다른 ASGI 서버.

## 서버 프로그램 실행.

그리고 '--reload' 옵션을 사용하지 않고, 다음과 같이 튜토리얼과 동일한 방식으로 응용 프로그램을 실행할 수 있습니다.

=== "Uvicorn"

    <div class="termy">

    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80

    <span style="color: green;">INFO</span>:     Uvicorn이 다음 주소에서 실행 중 http://0.0.0.0:80 (종료하려면 CTRL+C를 누르세요)
    ```

    </div>

=== "Hypercorn"

    <div class="termy">

    ```console
    $ hypercorn main:app --bind 0.0.0.0:80

    http를 통해 0.0.0.0:8080에서 실행 중 (종료하려면 CTRL+C를 누르세요)
    ```

    </div>

!!! warning "경고"
    `--reload` 옵션을 사용 중이라면 제거하는 것을 잊지 마십시오.

    `--reload` 옵션은 훨씬 더 많은 리소스를 소비하고 더 불안정합니다.

    **개발** 동안 많은 도움이 되지만 **프로덕션**에서는 **사용해서는 안 됩니다**.

## Hypercorn 및 Trio

Starlette 과 **FastAPI** 는 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>에 기반을 두고 있으며, 이를 통해 파이썬의 스탠다드 라이브러리인 <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a>, <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a> 와 호환됩니다.

그럼에도 불구하고, Uvicorn 은 현재 asyncio 와만 호환되며, 일반적으로 'asyncio'를 큰 코드 변환없이 대체하는 고성능의 <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a>를 사용합니다.

하지만 **Trio**를 직접 사용하고 싶다면, **Hypercorn** 도 지원하므로 사용하실 수 있습니다. ✨

### Hypercorn 및 Trio 설치하기

먼저 Trio를 지원하는 Hypercorn을 설치해야 합니다:

<div class="termy">

```console
$ pip install "hypercorn[trio]"
---> 100%
```

</div>

### Trio 실행

그런 다음 `--worker-class` 와 `trio` 값을 함께 명령줄 옵션으로 전달할 수 있습니다:

<div class="termy">

```console
$ hypercorn main:app --worker-class trio
```

</div>

그러면 Trio를 백엔드로 사용하는 앱에서 Hypercorn이 시작됩니다.


이제 앱에서 내부적으로 Trio를 사용할 수 있습니다. 또는 더 나은 방법으로 AnyIO를 사용하여 코드를 Trio 및 asyncio와 호환되도록 유지할 수 있습니다. 🎉

## 디플로이먼트 개념

이 예제는 서버 프로그램(예: Uvicorn)을 실행하고, **단일 프로세스**를 시작하여 사전 정의된 포트(예: `80`)에서 모든 IP(`0.0.0.0`)를 수신 대기합니다.

이것은 기본 아이디어입니다. 그러나, 다음과 같은 추가사항을 처리하고 싶을 수 있을 것입니다:

* 보안 - HTTPS
* 시작 시 실행
* 재시작
* 복제 (실행 중인 프로세스 수)
* 메모리
* 시작하기 전의 이전 단계


다음 장에서 이러한 개념 각각에 대해 더 자세히 설명하고 개념에 대해 생각하는 방법과 이러한 개념을 처리하기 위한 전략과 함께 몇 가지 구체적인 예를 설명하겠습니다. 🚀
