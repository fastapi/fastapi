# 컨테이너의 FastAPI - 도커 { #fastapi-in-containers-docker }

FastAPI 애플리케이션을 배포할 때 일반적인 접근 방법은 **리눅스 컨테이너 이미지**를 빌드하는 것입니다. 보통 <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>를 사용해 수행합니다. 그런 다음 해당 컨테이너 이미지를 몇 가지 가능한 방법 중 하나로 배포할 수 있습니다.

리눅스 컨테이너를 사용하면 **보안**, **재현 가능성**, **단순함** 등 여러 장점이 있습니다.

/// tip | 팁

시간이 없고 이미 이런 내용들을 알고 계신가요? 아래의 [`Dockerfile` 👇](#build-a-docker-image-for-fastapi)로 이동하세요.

///

<details>
<summary>Dockerfile Preview 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## 컨테이너란 { #what-is-a-container }

컨테이너(주로 리눅스 컨테이너)는 모든 의존성과 필요한 파일을 포함해 애플리케이션을 패키징하면서, 같은 시스템의 다른 컨테이너(다른 애플리케이션이나 컴포넌트)와는 분리된 상태로 유지할 수 있는 매우 **가벼운** 방법입니다.

리눅스 컨테이너는 호스트(머신, 가상 머신, 클라우드 서버 등)와 같은 리눅스 커널을 사용해 실행됩니다. 즉, 전체 운영체제를 에뮬레이션하는 완전한 가상 머신에 비해 매우 가볍습니다.

이 방식으로 컨테이너는 프로세스를 직접 실행하는 것과 비슷한 수준의 **적은 자원**을 소비합니다(가상 머신은 훨씬 더 많은 자원을 소비합니다).

또한 컨테이너는 자체적인 **격리된** 실행 프로세스(보통 하나의 프로세스), 파일 시스템, 네트워크를 가지므로 배포, 보안, 개발 등을 단순화합니다.

## 컨테이너 이미지란 { #what-is-a-container-image }

**컨테이너**는 **컨테이너 이미지**에서 실행됩니다.

컨테이너 이미지는 컨테이너에 있어야 하는 모든 파일, 환경 변수, 기본 명령/프로그램의 **정적** 버전입니다. 여기서 **정적**이라는 것은 컨테이너 **이미지**가 실행 중이거나 수행되는 것이 아니라, 패키징된 파일과 메타데이터일 뿐이라는 뜻입니다.

저장된 정적 콘텐츠인 "**컨테이너 이미지**"와 달리, "**컨테이너**"는 보통 실행 중인 인스턴스, 즉 **실행되는** 대상을 의미합니다.

**컨테이너**가 시작되어 실행 중이면(**컨테이너 이미지**로부터 시작됨) 파일, 환경 변수 등을 생성하거나 변경할 수 있습니다. 이러한 변경은 해당 컨테이너에만 존재하며, 기반이 되는 컨테이너 이미지에는 지속되지 않습니다(디스크에 저장되지 않습니다).

컨테이너 이미지는 **프로그램** 파일과 그 콘텐츠, 예를 들어 `python`과 어떤 파일 `main.py`에 비유할 수 있습니다.

그리고 **컨테이너** 자체는(**컨테이너 이미지**와 달리) 이미지의 실제 실행 인스턴스로서 **프로세스**에 비유할 수 있습니다. 실제로 컨테이너는 **실행 중인 프로세스**가 있을 때만 실행됩니다(보통 단일 프로세스입니다). 컨테이너 내부에 실행 중인 프로세스가 없으면 컨테이너는 중지됩니다.

## 컨테이너 이미지 { #container-images }

Docker는 **컨테이너 이미지**와 **컨테이너**를 생성하고 관리하는 주요 도구 중 하나입니다.

또한 <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a>에는 다양한 도구, 환경, 데이터베이스, 애플리케이션을 위한 미리 만들어진 **공식 컨테이너 이미지**가 공개되어 있습니다.

예를 들어, 공식 <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Python Image</a>가 있습니다.

그리고 데이터베이스 등 다양한 용도의 다른 이미지도 많이 있습니다. 예를 들면:

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a> 등

미리 만들어진 컨테이너 이미지를 사용하면 서로 다른 도구를 **결합**하고 사용하기가 매우 쉽습니다. 예를 들어 새로운 데이터베이스를 시험해 볼 때도 그렇습니다. 대부분의 경우 **공식 이미지**를 사용하고, 환경 변수로 설정만 하면 됩니다.

이렇게 하면 많은 경우 컨테이너와 Docker를 학습하고, 그 지식을 여러 다른 도구와 컴포넌트에 재사용할 수 있습니다.

따라서 데이터베이스, Python 애플리케이션, React 프론트엔드 애플리케이션이 있는 웹 서버 등 서로 다른 것들을 담은 **여러 컨테이너**를 실행하고 내부 네트워크를 통해 연결할 수 있습니다.

Docker나 Kubernetes 같은 모든 컨테이너 관리 시스템에는 이러한 네트워킹 기능이 통합되어 있습니다.

## 컨테이너와 프로세스 { #containers-and-processes }

**컨테이너 이미지**는 보통 **컨테이너**가 시작될 때 실행되어야 하는 기본 프로그램/명령과 해당 프로그램에 전달할 매개변수를 메타데이터에 포함합니다. 커맨드 라인에서 실행할 때와 매우 유사합니다.

**컨테이너**가 시작되면 해당 명령/프로그램을 실행합니다(다만 오버라이드하여 다른 명령/프로그램을 실행하게 할 수도 있습니다).

컨테이너는 **메인 프로세스**(명령 또는 프로그램)가 실행되는 동안 실행됩니다.

컨테이너는 보통 **단일 프로세스**를 가지지만, 메인 프로세스에서 서브프로세스를 시작할 수도 있으며, 그러면 같은 컨테이너에 **여러 프로세스**가 존재하게 됩니다.

하지만 **최소 하나의 실행 중인 프로세스** 없이 실행 중인 컨테이너를 가질 수는 없습니다. 메인 프로세스가 중지되면 컨테이너도 중지됩니다.

## FastAPI를 위한 도커 이미지 빌드하기 { #build-a-docker-image-for-fastapi }

좋습니다, 이제 무언가를 만들어 봅시다! 🚀

**공식 Python** 이미지에 기반하여 FastAPI용 **Docker 이미지**를 **처음부터** 빌드하는 방법을 보여드리겠습니다.

이는 **대부분의 경우**에 하고 싶은 방식입니다. 예를 들면:

* **Kubernetes** 또는 유사한 도구를 사용할 때
* **Raspberry Pi**에서 실행할 때
* 컨테이너 이미지를 대신 실행해주는 클라우드 서비스를 사용할 때 등

### 패키지 요구사항 { #package-requirements }

보통 애플리케이션의 **패키지 요구사항**을 어떤 파일에 적어 둡니다.

이는 주로 그 요구사항을 **설치**하는 데 사용하는 도구에 따라 달라집니다.

가장 일반적인 방법은 패키지 이름과 버전을 한 줄에 하나씩 적어 둔 `requirements.txt` 파일을 사용하는 것입니다.

버전 범위를 설정할 때는 [FastAPI 버전들에 대하여](versions.md){.internal-link target=_blank}에서 읽은 것과 같은 아이디어를 사용하면 됩니다.

예를 들어 `requirements.txt`는 다음과 같을 수 있습니다:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

그리고 보통 `pip`로 패키지 의존성을 설치합니다. 예를 들면:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | 정보

패키지 의존성을 정의하고 설치하는 다른 형식과 도구도 있습니다.

///

### **FastAPI** 코드 생성하기 { #create-the-fastapi-code }

* `app` 디렉터리를 만들고 들어갑니다.
* 빈 파일 `__init__.py`를 만듭니다.
* 다음 내용으로 `main.py` 파일을 만듭니다:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

이제 같은 프로젝트 디렉터리에 다음 내용으로 `Dockerfile` 파일을 만듭니다:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.9

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. 공식 Python 베이스 이미지에서 시작합니다.

2. 현재 작업 디렉터리를 `/code`로 설정합니다.

    여기에 `requirements.txt` 파일과 `app` 디렉터리를 둘 것입니다.

3. 요구사항 파일을 `/code` 디렉터리로 복사합니다.

    처음에는 요구사항 파일만 **단독으로** 복사하고, 나머지 코드는 복사하지 않습니다.

    이 파일은 **자주 바뀌지 않기** 때문에 Docker는 이를 감지하여 이 단계에서 **캐시**를 사용하고, 다음 단계에서도 캐시를 사용할 수 있게 해줍니다.

4. 요구사항 파일에 있는 패키지 의존성을 설치합니다.

    `--no-cache-dir` 옵션은 `pip`가 다운로드한 패키지를 로컬에 저장하지 않도록 합니다. 이는 `pip`가 같은 패키지를 설치하기 위해 다시 실행될 때만 의미가 있지만, 컨테이너 작업에서는 그렇지 않기 때문입니다.

    /// note | 참고

    `--no-cache-dir`는 `pip`에만 관련되어 있으며 Docker나 컨테이너와는 관련이 없습니다.

    ///

    `--upgrade` 옵션은 이미 설치된 패키지가 있다면 `pip`가 이를 업그레이드하도록 합니다.

    이전 단계에서 파일을 복사한 것이 **Docker 캐시**에 의해 감지될 수 있으므로, 이 단계에서도 가능하면 **Docker 캐시를 사용**합니다.

    이 단계에서 캐시를 사용하면 개발 중에 이미지를 반복해서 빌드할 때, 의존성을 **매번 다운로드하고 설치하는** 대신 많은 **시간**을 **절약**할 수 있습니다.

5. `./app` 디렉터리를 `/code` 디렉터리 안으로 복사합니다.

    이 디렉터리에는 **가장 자주 변경되는** 코드가 모두 포함되어 있으므로, Docker **캐시**는 이 단계나 **이후 단계들**에서는 쉽게 사용되지 않습니다.

    따라서 컨테이너 이미지 빌드 시간을 최적화하려면 `Dockerfile`의 **끝부분 근처**에 두는 것이 중요합니다.

6. 내부적으로 Uvicorn을 사용하는 `fastapi run`을 사용하도록 **명령**을 설정합니다.

    `CMD`는 문자열 리스트를 받으며, 각 문자열은 커맨드 라인에서 공백으로 구분해 입력하는 항목들입니다.

    이 명령은 **현재 작업 디렉터리**에서 실행되며, 이는 위에서 `WORKDIR /code`로 설정한 `/code` 디렉터리와 같습니다.

/// tip | 팁

코드의 각 숫자 버블을 클릭해 각 줄이 하는 일을 확인하세요. 👆

///

/// warning | 경고

아래에서 설명하는 것처럼 `CMD` 지시어는 **항상** **exec form**을 사용해야 합니다.

///

#### `CMD` 사용하기 - Exec Form { #use-cmd-exec-form }

Docker 지시어 <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a>는 두 가지 형식으로 작성할 수 있습니다:

✅ **Exec** form:

```Dockerfile
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```Dockerfile
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

FastAPI가 정상적으로 종료(graceful shutdown)되고 [lifespan 이벤트](../advanced/events.md){.internal-link target=_blank}가 트리거되도록 하려면, 항상 **exec** form을 사용하세요.

자세한 내용은 <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">shell and exec form에 대한 Docker 문서</a>를 참고하세요.

이는 `docker compose`를 사용할 때 꽤 눈에 띌 수 있습니다. 좀 더 기술적인 상세 내용은 Docker Compose FAQ 섹션을 참고하세요: <a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Why do my services take 10 seconds to recreate or stop?</a>.

#### 디렉터리 구조 { #directory-structure }

이제 다음과 같은 디렉터리 구조가 되어야 합니다:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### TLS 종료 프록시의 배후 { #behind-a-tls-termination-proxy }

Nginx나 Traefik 같은 TLS 종료 프록시(로드 밸런서) 뒤에서 컨테이너를 실행하고 있다면 `--proxy-headers` 옵션을 추가하세요. 이 옵션은 (FastAPI CLI를 통해) Uvicorn에게 해당 프록시가 보낸 헤더를 신뢰하도록 하여, 애플리케이션이 HTTPS 뒤에서 실행 중임을 알게 합니다.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### 도커 캐시 { #docker-cache }

이 `Dockerfile`에는 중요한 트릭이 있습니다. 먼저 **의존성 파일만** 복사하고, 나머지 코드는 복사하지 않는 것입니다. 왜 그런지 설명하겠습니다.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker와 다른 도구들은 `Dockerfile`의 위에서부터 시작해, 각 지시어가 만든 파일을 포함하며 **레이어를 하나씩 위에 쌓는 방식으로** 컨테이너 이미지를 **점진적으로** 빌드합니다.

Docker와 유사한 도구들은 이미지를 빌드할 때 **내부 캐시**도 사용합니다. 어떤 파일이 마지막으로 컨테이너 이미지를 빌드했을 때부터 바뀌지 않았다면, 파일을 다시 복사하고 새 레이어를 처음부터 만드는 대신, 이전에 만든 **같은 레이어를 재사용**합니다.

파일 복사를 피하는 것만으로 큰 개선이 생기지는 않을 수 있지만, 해당 단계에서 캐시를 사용했기 때문에 **다음 단계에서도 캐시를 사용할 수** 있습니다. 예를 들어 다음과 같이 의존성을 설치하는 지시어에서 캐시를 사용할 수 있습니다:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

패키지 요구사항 파일은 **자주 변경되지 않습니다**. 따라서 그 파일만 복사하면 Docker는 그 단계에서 **캐시를 사용할 수** 있습니다.

그리고 Docker는 그 다음 단계에서 의존성을 다운로드하고 설치할 때도 **캐시를 사용할 수** 있습니다. 바로 여기에서 **많은 시간을 절약**하게 됩니다. ✨ ...그리고 기다리며 지루해지는 것도 피할 수 있습니다. 😪😆

패키지 의존성을 다운로드하고 설치하는 데에는 **몇 분**이 걸릴 수 있지만, **캐시**를 사용하면 많아야 **몇 초**면 끝납니다.

또한 개발 중에 코드 변경 사항이 동작하는지 확인하기 위해 컨테이너 이미지를 계속 빌드하게 되므로, 이렇게 절약되는 시간은 누적되어 상당히 커집니다.

그 다음 `Dockerfile`의 끝부분 근처에서 모든 코드를 복사합니다. 이 부분은 **가장 자주 변경되는** 부분이므로, 거의 항상 이 단계 이후에는 캐시를 사용할 수 없기 때문에 끝부분에 둡니다.

```Dockerfile
COPY ./app /code/app
```

### 도커 이미지 생성하기 { #build-the-docker-image }

이제 모든 파일이 제자리에 있으니 컨테이너 이미지를 빌드해봅시다.

* 프로젝트 디렉터리로 이동합니다(`Dockerfile`이 있고 `app` 디렉터리를 포함하는 위치).
* FastAPI 이미지를 빌드합니다:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | 팁

끝에 있는 `.`에 주목하세요. 이는 `./`와 동일하며, Docker에게 컨테이너 이미지를 빌드할 때 사용할 디렉터리를 알려줍니다.

이 경우 현재 디렉터리(`.`)입니다.

///

### 도커 컨테이너 시작하기 { #start-the-docker-container }

* 여러분의 이미지에 기반하여 컨테이너를 실행합니다:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## 확인하기 { #check-it }

Docker 컨테이너의 URL에서 확인할 수 있어야 합니다. 예를 들어: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> 또는 <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a>(또는 Docker 호스트를 사용해 동등하게 확인할 수 있습니다).

아래와 같은 것을 보게 될 것입니다:

```JSON
{"item_id": 5, "q": "somequery"}
```

## 인터랙티브 API 문서 { #interactive-api-docs }

이제 <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> 또는 <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a>(또는 Docker 호스트를 사용해 동등하게 접근)로 이동할 수 있습니다.

자동으로 생성된 인터랙티브 API 문서(<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> 제공)를 볼 수 있습니다:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 대안 API 문서 { #alternative-api-docs }

또한 <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> 또는 <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a>(또는 Docker 호스트를 사용해 동등하게 접근)로 이동할 수도 있습니다.

대안 자동 문서(<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> 제공)를 볼 수 있습니다:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## 단일 파일 FastAPI로 도커 이미지 빌드하기 { #build-a-docker-image-with-a-single-file-fastapi }

FastAPI가 단일 파일(예: `./app` 디렉터리 없이 `main.py`만 있는 경우)이라면, 파일 구조는 다음과 같을 수 있습니다:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

그런 다음 `Dockerfile`에서 해당 파일을 복사하도록 경로만 맞게 변경하면 됩니다:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. `main.py` 파일을 `/code` 디렉터리로 직접 복사합니다(`./app` 디렉터리 없이).

2. 단일 파일 `main.py`에 있는 애플리케이션을 제공(serve)하기 위해 `fastapi run`을 사용합니다.

`fastapi run`에 파일을 전달하면, 이것이 패키지의 일부가 아닌 단일 파일이라는 것을 자동으로 감지하고, 어떻게 임포트해서 FastAPI 앱을 제공할지 알아냅니다. 😎

## 배포 개념 { #deployment-concepts }

컨테이너 관점에서 같은 [배포 개념](concepts.md){.internal-link target=_blank}들을 다시 이야기해 봅시다.

컨테이너는 주로 애플리케이션의 **빌드 및 배포** 과정을 단순화하는 도구이지만, 이러한 **배포 개념**을 처리하는 특정 접근 방식을 강제하지는 않으며, 가능한 전략은 여러 가지입니다.

**좋은 소식**은 각 전략마다 모든 배포 개념을 다룰 수 있는 방법이 있다는 점입니다. 🎉

컨테이너 관점에서 이 **배포 개념**들을 살펴봅시다:

* HTTPS
* 시작 시 자동 실행
* 재시작
* 복제(실행 중인 프로세스 수)
* 메모리
* 시작 전 사전 단계

## HTTPS { #https }

FastAPI 애플리케이션의 **컨테이너 이미지**(그리고 나중에 실행 중인 **컨테이너**)에만 집중한다면, HTTPS는 보통 다른 도구에 의해 **외부적으로** 처리됩니다.

예를 들어 <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>을 사용하는 다른 컨테이너가 **HTTPS**와 **인증서**의 **자동** 획득을 처리할 수 있습니다.

/// tip | 팁

Traefik은 Docker, Kubernetes 등과 통합되어 있어, 이를 사용해 컨테이너에 HTTPS를 설정하고 구성하기가 매우 쉽습니다.

///

또는 HTTPS를 클라우드 제공자가 서비스의 일부로 처리할 수도 있습니다(애플리케이션은 여전히 컨테이너에서 실행됩니다).

## 시작 시 자동 실행과 재시작 { #running-on-startup-and-restarts }

보통 컨테이너를 **시작하고 실행**하는 역할을 담당하는 다른 도구가 있습니다.

직접 **Docker**일 수도 있고, **Docker Compose**, **Kubernetes**, **클라우드 서비스** 등일 수도 있습니다.

대부분(또는 전부)의 경우, 시작 시 컨테이너를 실행하고 실패 시 재시작을 활성화하는 간단한 옵션이 있습니다. 예를 들어 Docker에서는 커맨드 라인 옵션 `--restart`입니다.

컨테이너를 사용하지 않으면 애플리케이션을 시작 시 자동 실행하고 재시작까지 구성하는 것이 번거롭고 어렵습니다. 하지만 **컨테이너로 작업할 때**는 대부분의 경우 그 기능이 기본으로 포함되어 있습니다. ✨

## 복제 - 프로세스 개수 { #replication-number-of-processes }

**Kubernetes**, Docker Swarm Mode, Nomad 등의 복잡한 시스템으로 여러 머신에 분산된 컨테이너를 관리하는 <abbr title="A group of machines that are configured to be connected and work together in some way.">cluster</abbr>를 사용한다면, 각 컨테이너에서(**워커를 사용하는 Uvicorn** 같은) **프로세스 매니저**를 쓰는 대신, **클러스터 레벨**에서 **복제를 처리**하고 싶을 가능성이 큽니다.

Kubernetes 같은 분산 컨테이너 관리 시스템은 보통 들어오는 요청에 대한 **로드 밸런싱**을 지원하면서도, **컨테이너 복제**를 처리하는 통합된 방법을 가지고 있습니다. 모두 **클러스터 레벨**에서요.

그런 경우에는 [위에서 설명한 대로](#dockerfile) 의존성을 설치하고, 여러 Uvicorn 워커를 사용하는 대신 **단일 Uvicorn 프로세스**를 실행하는 **처음부터 만든 Docker 이미지**를 사용하는 것이 좋을 것입니다.

### 로드 밸런서 { #load-balancer }

컨테이너를 사용할 때는 보통 **메인 포트에서 대기(listening)하는** 컴포넌트가 있습니다. **HTTPS**를 처리하기 위한 **TLS 종료 프록시** 역할을 하는 다른 컨테이너일 수도 있고, 유사한 도구일 수도 있습니다.

이 컴포넌트가 요청의 **부하(load)**를 받아 워커들에 (가능하면) **균형 있게** 분산한다면, 보통 **로드 밸런서**라고 부릅니다.

/// tip | 팁

HTTPS에 사용되는 동일한 **TLS 종료 프록시** 컴포넌트가 **로드 밸런서**이기도 한 경우가 많습니다.

///

또한 컨테이너로 작업할 때, 이를 시작하고 관리하는 시스템은 이미 해당 **로드 밸런서**(또는 **TLS 종료 프록시**)에서 여러분의 앱이 있는 컨테이너로 **네트워크 통신**(예: HTTP 요청)을 전달하는 내부 도구를 가지고 있습니다.

### 하나의 로드 밸런서 - 여러 워커 컨테이너 { #one-load-balancer-multiple-worker-containers }

**Kubernetes** 같은 분산 컨테이너 관리 시스템에서는 내부 네트워킹 메커니즘을 통해, 메인 **포트**에서 대기하는 단일 **로드 밸런서**가 여러분의 앱을 실행하는 **여러 컨테이너**로 통신(요청)을 전달할 수 있습니다.

앱을 실행하는 각 컨테이너는 보통 **프로세스 하나만** 가집니다(예: FastAPI 애플리케이션을 실행하는 Uvicorn 프로세스). 모두 같은 것을 실행하는 **동일한 컨테이너**이지만, 각자 고유한 프로세스, 메모리 등을 가집니다. 이렇게 하면 CPU의 **서로 다른 코어** 또는 **서로 다른 머신**에서 **병렬화**의 이점을 얻을 수 있습니다.

그리고 **로드 밸런서**가 있는 분산 컨테이너 시스템은 여러분의 앱을 실행하는 각 컨테이너에 **번갈아가며** 요청을 **분산**합니다. 따라서 각 요청은 여러분의 앱을 실행하는 여러 **복제된 컨테이너** 중 하나에서 처리될 수 있습니다.

또한 보통 이 **로드 밸런서**는 클러스터 내 *다른* 앱으로 가는 요청(예: 다른 도메인, 또는 다른 URL 경로 접두사 아래로 가는 요청)도 처리할 수 있으며, 그 통신을 클러스터에서 실행 중인 *그 다른* 애플리케이션의 올바른 컨테이너로 전달할 수 있습니다.

### 컨테이너당 하나의 프로세스 { #one-process-per-container }

이 시나리오에서는 이미 클러스터 레벨에서 복제를 처리하고 있으므로, **컨테이너당 단일 (Uvicorn) 프로세스**를 두는 것이 좋을 가능성이 큽니다.

따라서 이 경우 컨테이너에서 `--workers` 커맨드 라인 옵션 같은 방식으로 여러 워커를 두고 싶지는 **않을** 것입니다. 컨테이너당 **단일 Uvicorn 프로세스**만 두고(하지만 컨테이너는 여러 개일 수 있습니다) 싶을 것입니다.

컨테이너 내부에 (여러 워커를 위한) 또 다른 프로세스 매니저를 두는 것은, 이미 클러스터 시스템에서 처리하고 있는 **불필요한 복잡성**만 추가할 가능성이 큽니다.

### 여러 프로세스를 가진 컨테이너와 특수한 경우 { #containers-with-multiple-processes-and-special-cases }

물론 컨테이너 하나에 여러 **Uvicorn 워커 프로세스**를 두고 싶을 수 있는 **특수한 경우**도 있습니다.

그런 경우에는 `--workers` 커맨드 라인 옵션을 사용해 실행할 워커 수를 설정할 수 있습니다:

```{ .dockerfile .annotate }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. 여기서는 `--workers` 커맨드 라인 옵션으로 워커 수를 4로 설정합니다.

이런 방식이 의미가 있을 수 있는 예시는 다음과 같습니다:

#### 단순한 앱 { #a-simple-app }

애플리케이션이 **충분히 단순**해서 클러스터가 아닌 **단일 서버**에서 실행할 수 있다면, 컨테이너에 프로세스 매니저를 두고 싶을 수 있습니다.

#### Docker Compose { #docker-compose }

**Docker Compose**로 클러스터가 아닌 **단일 서버**에 배포하는 경우, 공유 네트워크와 **로드 밸런싱**을 유지하면서(Docker Compose로) 컨테이너 복제를 관리하는 쉬운 방법이 없을 수 있습니다.

그렇다면 **프로세스 매니저**가 컨테이너 내부에서 **여러 워커 프로세스**를 시작하는 **단일 컨테이너**를 원할 수 있습니다.

---

핵심은, 이것들 중 **어느 것도** 무조건 따라야 하는 **절대적인 규칙**은 아니라는 것입니다. 이 아이디어들을 사용해 **여러분의 사용 사례를 평가**하고, 여러분의 시스템에 가장 적합한 접근 방식을 결정하면서 다음 개념을 어떻게 관리할지 확인할 수 있습니다:

* 보안 - HTTPS
* 시작 시 자동 실행
* 재시작
* 복제(실행 중인 프로세스 수)
* 메모리
* 시작 전 사전 단계

## 메모리 { #memory }

**컨테이너당 단일 프로세스**를 실행하면, 각 컨테이너(복제된 경우 여러 개)마다 소비하는 메모리 양이 대체로 잘 정의되고 안정적이며 제한된 값이 됩니다.

그런 다음 컨테이너 관리 시스템(예: **Kubernetes**) 설정에서 동일하게 메모리 제한과 요구사항을 설정할 수 있습니다. 그러면 클러스터에서 사용 가능한 머신에 있는 메모리와 컨테이너가 필요로 하는 메모리 양을 고려해 **컨테이너를 복제**할 수 있습니다.

애플리케이션이 **단순**하다면 이는 아마도 **문제가 되지 않을** 것이고, 엄격한 메모리 제한을 지정할 필요가 없을 수도 있습니다. 하지만 **많은 메모리를 사용한다면**(예: **머신 러닝** 모델), 얼마나 많은 메모리를 소비하는지 확인하고, **각 머신**에서 실행되는 **컨테이너 수**를 조정해야 합니다(필요하다면 클러스터에 머신을 더 추가할 수도 있습니다).

**컨테이너당 여러 프로세스**를 실행한다면, 시작되는 프로세스 수가 사용 가능한 것보다 **더 많은 메모리를 소비하지** 않는지 확인해야 합니다.

## 시작 전 단계와 컨테이너 { #previous-steps-before-starting-and-containers }

컨테이너(예: Docker, Kubernetes)를 사용한다면, 사용할 수 있는 주요 접근 방식은 두 가지입니다.

### 여러 컨테이너 { #multiple-containers }

**여러 컨테이너**가 있고 각 컨테이너가 보통 **단일 프로세스**를 실행한다면(예: **Kubernetes** 클러스터), 복제된 워커 컨테이너를 실행하기 **전에**, 단일 컨테이너에서 단일 프로세스로 **시작 전 사전 단계**를 수행하는 **별도의 컨테이너**를 두고 싶을 가능성이 큽니다.

/// info | 정보

Kubernetes를 사용한다면, 이는 아마도 <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>일 것입니다.

///

사용 사례에서 시작 전 사전 단계를 **여러 번 병렬로 실행**해도 문제가 없다면(예: 데이터베이스 마이그레이션을 실행하는 것이 아니라, 데이터베이스가 준비되었는지 확인만 하는 경우), 메인 프로세스를 시작하기 직전에 각 컨테이너에 그 단계를 넣을 수도 있습니다.

### 단일 컨테이너 { #single-container }

**단일 컨테이너**에서 여러 **워커 프로세스**(또는 단일 프로세스)를 시작하는 단순한 셋업이라면, 앱이 있는 프로세스를 시작하기 직전에 같은 컨테이너에서 시작 전 사전 단계를 실행할 수 있습니다.

### 베이스 도커 이미지 { #base-docker-image }

과거에는 공식 FastAPI Docker 이미지가 있었습니다: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>. 하지만 이제는 deprecated되었습니다. ⛔️

아마도 이 베이스 도커 이미지(또는 유사한 다른 이미지)는 **사용하지 않는** 것이 좋습니다.

**Kubernetes**(또는 다른 도구)를 사용하고, 클러스터 레벨에서 여러 **컨테이너**로 **복제**를 이미 설정해 둔 경우라면, 위에서 설명한 대로 **처음부터 이미지를 빌드하는 것**이 더 낫습니다: [FastAPI를 위한 도커 이미지 빌드하기](#build-a-docker-image-for-fastapi).

그리고 여러 워커가 필요하다면, `--workers` 커맨드 라인 옵션을 간단히 사용하면 됩니다.

/// note Technical Details | 기술 세부사항

이 Docker 이미지는 Uvicorn이 죽은 워커를 관리하고 재시작하는 기능을 지원하지 않던 시기에 만들어졌습니다. 그래서 Gunicorn과 Uvicorn을 함께 사용해야 했고, Gunicorn이 Uvicorn 워커 프로세스를 관리하고 재시작하도록 하기 위해 상당한 복잡성이 추가되었습니다.

하지만 이제 Uvicorn(그리고 `fastapi` 명령)은 `--workers`를 지원하므로, 베이스 도커 이미지를 사용하는 대신 직접 이미지를 빌드하지 않을 이유가 없습니다(코드 양도 사실상 거의 같습니다 😅).

///

## 컨테이너 이미지 배포하기 { #deploy-the-container-image }

컨테이너(Docker) 이미지를 만든 후에는 이를 배포하는 여러 방법이 있습니다.

예를 들어:

* 단일 서버에서 **Docker Compose**로
* **Kubernetes** 클러스터로
* Docker Swarm Mode 클러스터로
* Nomad 같은 다른 도구로
* 컨테이너 이미지를 받아 배포해주는 클라우드 서비스로

## `uv`를 사용하는 도커 이미지 { #docker-image-with-uv }

프로젝트를 설치하고 관리하기 위해 <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a>를 사용한다면, <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">uv Docker guide</a>를 따를 수 있습니다.

## 요약 { #recap }

컨테이너 시스템(예: **Docker**, **Kubernetes**)을 사용하면 모든 **배포 개념**을 다루는 것이 상당히 단순해집니다:

* HTTPS
* 시작 시 자동 실행
* 재시작
* 복제(실행 중인 프로세스 수)
* 메모리
* 시작 전 사전 단계

대부분의 경우 베이스 이미지는 사용하지 않고, 공식 Python Docker 이미지에 기반해 **처음부터 컨테이너 이미지를 빌드**하는 것이 좋습니다.

`Dockerfile`에서 지시어의 **순서**와 **Docker 캐시**를 신경 쓰면 **빌드 시간을 최소화**해 생산성을 최대화할 수 있습니다(그리고 지루함도 피할 수 있습니다). 😎
