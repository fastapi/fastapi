# 가상 환경 { #virtual-environments }

Python 프로젝트를 작업할 때는 각 프로젝트마다 설치하는 패키지를 분리하기 위해 **가상 환경**을 사용해야 합니다.

FastAPI 프로젝트에서는 [uv](https://docs.astral.sh/uv/)를 사용해 프로젝트, 의존성, 가상 환경을 관리하는 것을 권장합니다.

## 프로젝트 생성 { #create-a-project }

[공식 설치 가이드](https://docs.astral.sh/uv/getting-started/installation/)를 사용해 `uv`를 설치한 다음, 프로젝트를 생성하세요:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv`는 프로젝트를 위한 가상 환경을 자동으로 생성합니다. 직접 만들거나 활성화할 필요가 없습니다.

프로젝트 환경 안에서 명령어를 실행하려면 `uv run`을 사용하세요. 예를 들면:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## 더 알아보기 { #learn-more }

가상 환경이 내부에서 어떻게 작동하는지, 활성화와 대안인 `python -m venv` 및 `pip` 워크플로를 포함해 알아보려면 [가상 환경 가이드](https://tiangolo.com/guides/virtual-environments/)를 읽어보세요.
