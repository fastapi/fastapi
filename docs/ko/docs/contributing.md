# 개발 - 기여하기

먼저, 여러분은 [FastAPI를 돕고 도움을 받는](help-fastapi.md){.internal-link target=_blank} 기본 방법을 확인하고 싶을 수도 있습니다.

## 개발

<a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">fastapi 저장소</a>를 이미 복제했고 코드를 자세히 살펴보고 싶다면, 환경 설정을 위한 몇 가지 지침을 따르세요.

### 가상 환경

안내에 따라 `fastapi`의 내부 코드에 대한 [가상 환경](virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화하세요.

### pip를 사용하여 요구 사항 설치

환경을 활성화한 후 필수 패키지를 설치합니다:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

이는 로컬 환경에 모든 종속성과 로컬 FastAPI를 설치합니다.

### 로컬 FastAPI 사용하기

FastAPI를 임포트하여 사용하는 파이썬 파일을 생성하고 로컬 환경에서 파이썬으로 실행하면, 복제된 로컬 FastAPI 소스 코드가 사용됩니다.

그리고 해당 파이썬 파일을 다시 실행할 때 해당 로컬 FastAPI 소스 코드를 업데이트하면, 방금 편집한 FastAPI의 새로운 버전을 사용합니다.

이렇게 하면 모든 변경 사항을 테스트하기 위해 로컬 버전을 "설치"할 필요가 없어집니다.

/// note | 기술 세부사항

`pip install fastapi`를 직접 실행하는 대신 포함된 `requirements.txt`를 사용하여 설치할 때만 이런 일이 일어납니다.

FastAPI의 로컬 버전이 `requirements.txt` 파일 내에서 `-e` 옵션을 사용하여 "편집 가능" 모드로 설치되도록 표시되어 있기 때문입니다.

///

### 코드 포맷하기

모든 코드를 포맷하고 정리하는 스크립트가 있습니다.

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

또한 모든 임포트 구문을 자동으로 정렬합니다.

## 테스트

모든 코드를 테스트하고 HTML로 커버리지 보고서를 생성하기 위해 로컬에서 실행할 수 있는 스크립트가 있습니다:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

이 명령은 `./htmlcov/` 디렉터리를 생성합니다. 브라우저에서 `./htmlcov/index.html` 파일을 열면, 테스트에서 다루는 코드 영역을 대화형으로 탐색하고 누락된 영역이 있는지 확인할 수 있습니다.

## 문서

먼저, 위에 설명된 대로 환경을 설정하여 모든 요구 사항을 설치하는지 확인하세요.

### 실시간 문서

로컬 개발 중에, 사이트를 빌드하고 실시간 리로드로 변경 사항을 확인하는 스크립트가 있습니다.

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

이는 `http://127.0.0.1:8008`에서 문서를 제공합니다.

이렇게 하면 문서/소스 파일을 편집하고 변경 사항을 실시간으로 확인할 수 있습니다.

/// tip | 팁

대안으로, 스크립트가 수동으로 실행하는 것과 동일한 단계를 수행할 수 있습니다.

언어 디렉터리로 이동하세요, 영어로 된 주요 문서는 `docs/en/`에 있습니다:

```console
$ cd docs/en/
```

그런 다음 해당 디렉터리에서 `mkdocs`를 실행하세요:

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer CLI(선택 사항)

여기 지침은 `./scripts/docs.py`에 있는 스크립트를 `python` 프로그램으로 직접 사용하는 방법을 보여줍니다.

하지만 <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>를 사용할 수도 있으며, 설치 완료 후 터미널에서 명령에 대해 자동 완성(autocompletion)을 설치 할 수 있습니다.

Typer CLI를 설치하는 경우, 다음을 사용하여 자동 완성을 설치할 수 있습니다:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### 문서 구조

문서화에 <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>를 사용합니다.

그리고 `./scripts/docs.py`에는 번역을 처리하기 위한 추가 도구/스크립트가 있습니다.

/// tip | 팁

`./scripts/docs.py`의 코드를 볼 필요는 없으며 명령줄에서 사용만 하면 됩니다.

///

모든 문서는 `./docs/en/` 디렉터리에 마크다운 형식으로 되어 있습니다.

수많은 튜토리얼에 코드 블록들이 있습니다.

대부분의 경우, 이러한 코드 블록들은 있는 그대로 실행할 수 있는 실제 완전한 응용 프로그램입니다.

사실, 이러한 코드 블록들은 마크다운 내부에 작성되는게 아니라 `./docs_src/` 디렉터리에 있는 파이썬 파일들입니다.

그리고 해당 파이썬 파일들은 사이트를 생성할 때 문서에 포함/주입됩니다.

### 테스트를 위한 문서

대부분의 테스트는 문서에 있는 예제 소스 파일을 실제로 실행합니다.

이는 다음 사항을 확실히 하는데 도움이 됩니다:

* 문서가 최신 상태입니다.
* 문서 예제는 있는 그대로 실행할 수 있습니다.
* 대부분의 기능은 문서에 포함되어 있으며, 테스트 커버리지로 보장됩니다.

#### 앱과 문서를 동시에

예를 들어, 다음과 같이 예제를 실행하면:

<div class="termy">

```console
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

유비콘(Uvicorn)은 기본적으로 `8000` 포트를 사용하므로 `8008` 포트에 대한 문서는 충돌하지 않습니다.

### 번역

번역에 도움을 주시면 매우 매우 감사하겠습니다! 그리고 이는 커뮤니티의 도움 없이는 이루어질 수 없습니다. 🌎 🚀

여기, 번역을 돕는 단계가 있습니다.

#### 팁과 가이드라인

* 사용하는 언어에 대한 <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">이미 있는 끌어오기 요청</a>을 확인하세요. 사용하는 언어의 레이블이 있는 끌어오기 요청을 필터링할 수 있습니다. 예를 들어, 스페인어의 경우 레이블은 <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>입니다.

* 끌어오기 요청을 검토하고 변경 사항을 요청하거나 승인하세요. 사용하지 않는 언어의 경우, 병합하기 전에 다른 여러 사람이 번역을 검토할 때까지 기다립니다.

/// tip | 팁

이미 있는 끌어오기 요청에 <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">변경사항 제안과 함께 댓글을 추가</a> 할 수 있습니다.

승인하거나 변경사항을 요청하려면 <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">끌어오기 요청 검토 추가</a>에 관한 문서를 확인하세요.

///

* 사용하는 언어에 대한 번역을 조정하기 위한 <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub 토론</a>이 있는지 확인하세요. 토론은 구독할 수 있으며, 검토할 새 끌어오기 요청이 있으면 자동 댓글이 추가됩니다.

* 페이지를 번역하는 경우, 번역한 페이지당 하나의 끌어오기 요청을 추가하세요. 그러면 다른 사람들이 검토하기가 훨씬 쉬워집니다.

* 번역하려는 언어의 2자리 코드를 확인하려면, <a href="https://ko.wikipedia.org/wiki/ISO_639-1_%EC%BD%94%EB%93%9C_%EB%AA%A9%EB%A1%9D" class="external-link" target="_blank">ISO 639-1 코드 목록</a> 표를 사용할 수 있습니다.

#### 이미 있는 언어

스페인어처럼, 일부 페이지에 대한 번역이 이미 있는 언어의 페이지를 번역한다고 가정해 보겠습니다.

스페인어의 경우, 2자리 코드는 `es` 입니다. 따라서 스페인어 번역 디렉터리는 `docs/es/`에 있습니다.

/// tip | 팁

주("공식") 언어는 영어이며 `docs/en/`에 있습니다.

///

이제 스페인어 문서에 대한 실시간 서버를 실행합니다:

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

/// tip | 팁

대안으로, 스크립트가 수동으로 실행하는 것과 동일한 단계를 수행할 수 있습니다.

언어 디렉터리로 이동하세요, 스페인어 번역은 `docs/es/`에 있습니다.

```console
$ cd docs/es/
```

그런 다음 해당 디렉터리에서 `mkdocs`를 실행하세요:

```console
$ mkdocs serve --dev-addr 8008
```

///

이제 <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a>으로 이동해서 변경사항을 실시간으로 볼 수 있습니다.

각 언어들이 모든 페이지를 갖고 있는 것을 볼 수 있습니다. 그러나 일부 페이지는 번역되지 않았으며 상단에 누락된 번역에 대한 정보 상자가 있습니다.

이제 [기능](features.md){.internal-link target=_blank} 섹션에 대한 번역을 추가한다고 가정해 보겠습니다.

* 다음 위치에 파일을 복사하세요:

```
docs/en/docs/features.md
```

* 번역하려는 언어를 정확히 같은 위치에 붙여넣으세요. 예:

```
docs/es/docs/features.md
```

/// tip | 팁

경로와 파일 이름의 유일한 변경 사항은 `en`에서 `es`로의 언어 코드입니다.

///

브라우저로 이동하면 이제 문서에 새 섹션이 표시되는 것을 볼 수 있습니다(상단의 정보 상자가 사라짐). 🎉

이제 모든 내용을 번역하고 파일을 저장할 때 어떻게 보이는지 확인할 수 있습니다.

#### 이 페이지들은 번역하지 마세요

🚨 번역하지 않음:

* `reference/` 하위 파일들
* `release-notes.md`
* `fastapi-people.md`
* `external-links.md`
* `newsletter.md`
* `management-tasks.md`
* `management.md`
* `contributing.md`

이러한 파일 중 일부는 매우 자주 업데이트되므로 번역이 항상 뒤처져 있거나 영어 소스 파일 등의 주요 내용이 포함되어 있습니다.

#### 새 언어

아직 번역되지 않은 언어, 심지어 일부 페이지도 없는 번역을 추가하고 싶다고 가정해 보겠습니다.

크리올어 번역을 추가하려고 하는데 아직 문서에 없다고 가정해 보겠습니다.

위에서 링크를 확인해보면, "Creole"의 코드는 `ht`입니다.

다음 단계는 스크립트를 실행하여 새 번역 디렉터리를 생성하는 것입니다:

<div class="termy">

```console
// new-lang 명령으로 언어 코드를 CLI 인수로 전달하세요
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

이제 코드 편집기에서 새로 생성된 `docs/ht/` 디렉터리를 확인할 수 있습니다.

해당 명령은 `en` 버전의 모든 것을 상속하는 간단한 구성으로 `docs/ht/mkdocs.yml` 파일을 생성했습니다:

```yaml
INHERIT: ../en/mkdocs.yml
```

/// tip | 팁

이 내용으로 간단하게 직접 파일을 만들어도 됩니다.

///

해당 명령은 메인 페이지에 대한 더미 파일 `docs/ht/index.md`도 생성했습니다. 해당 파일을 번역하는 것부터 시작할 수 있습니다.

"이미 있는 언어"의 진행 방식과 마찬가지로 이전 지침을 이용해 이어 나갈 수 있습니다.

`docs/ht/mkdocs.yml`과 `docs/ht/index.md` 두 파일로 첫 번째 끌어오기 요청을 만들 수 있습니다. 🎉

#### 결과 미리보기

위에서 이미 언급했듯이, `live` 명령과 함께 `./scripts/docs.py`를 사용(또는 `mkdocs serve`)하여 결과를 미리 볼 수 있습니다.

작업을 완료하면 다른 모든 언어를 포함하여 온라인에서 보이는 것처럼 모든 것을 테스트할 수도 있습니다.

그렇게 하려면 먼저 모든 문서를 빌드하세요:

<div class="termy">

```console
// "build-all" 명령을 사용하세요, 시간이 조금 걸립니다
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

이는 각 언어에 대한 모든 독립적인 MkDocs 사이트를 빌드하고 결합한 후 `./site/`에 최종 출력을 생성합니다.

그런 다음 `serve` 명령을 사용하여 서버를 띄울 수 있습니다:

<div class="termy">

```console
// "build-all" 실행 후에 "serve" 명령을 사용하세요
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

#### 번역 관련 팁 및 가이드라인

* 마크다운 문서(`.md`)만 번역하세요. `./docs_src`의 코드 예제를 번역하지 마세요.

* 마크다운 문서 내의 코드 블록의 주석(`# a comment`)은 번역하세요, 하지만 나머지는 변경하지 않고 그대로 둡니다.

* "``"(인라인 코드)로 묶인 내용은 변경하지 마세요.

* `///`로 시작하는 줄에서는 `|` 뒤의 텍스트 부분만 번역합니다. 나머지는 변경하지 않고 그대로 둡니다.

* `/// warning`과 같은 정보 상자를 `/// warning | 경고`의 예시처럼 번역해도 됩니다. 하지만 `///` 바로 뒤의 단어를 변경하지 마세요. 이것으로 정보 상자의 색상이 결정됩니다.

* 이미지, 코드 파일, 마크다운 문서에 대한 링크의 경로를 변경하지 마세요.

* 그러나 마크다운 문서가 번역되면 해당 제목 링크의 `#hash-parts`가 변경될 수 있습니다. 가능하다면 이 링크를 업데이트하세요.
    * 정규식 `#[^# ]`을 사용하여 번역된 문서에서 해당 링크를 검색합니다.
    * 이미 번역된 모든 문서에서 `your-translated-document.md`를 검색하세요. 예를 들어 VS Code에는 "편집" -> "파일에서 찾기" 옵션이 있습니다.
    * 문서를 번역할 때, 번역되지 않은 문서의 제목으로 연결되는 `#hash-parts`를 "미리 번역"하지 마세요.
