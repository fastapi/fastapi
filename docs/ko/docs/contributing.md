# 개발 - 기여

먼저 [help FastAPI and get help](https://github.com/tiangolo/fastapi/blob/master/docs/en/docs/help-fastapi.md)에서 기본 방법을 보고 도움을 얻는 것이 좋을지도 모릅니다.

## 개발

이미 저장소를 복제했고, 코드를 조사하게 알고싶은 경우에 환경 구축을 위한 몇 가지 가이드라인이 있습니다.

### `venv`를 이용한 가상환경

파이썬의 `venv` 모듈을 사용하여 디렉토리에 가상 환경을 만들 수 있습니다:

```
$ python -m venv env
```

그러면 파이썬 바이너리를 포함한  `./env/` 디렉토리가 생성되고 그 고립된 환경에 패키지를 설치할 수 있습니다.

### 가상 환경 활성화

새로운 환경을 활성화하려면:

=== "Linux, macOS"

````
<div class="termy">

```console
$ source ./env/bin/activate
```

</div>
````

=== "Windows PowerShell"

````
<div class="termy">

```console
$ .\env\Scripts\Activate.ps1
```

</div>
````

=== "Windows Bash"

````
Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

<div class="termy">

```console
$ source ./env/Scripts/activate
```

</div>
````

작동하는 걸 확인하기 위해 다음을 실행하십시오:

=== "Linux, macOS, Windows Bash"

````
<div class="termy">

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

</div>
````

=== "Windows PowerShell"

````
<div class="termy">

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```

</div>
````

`env/bin/pip` 에 `pip` 바이너리가 나타난다면 제대로 작동하고 있는 것입니다. 🎉

!!! tip "팁" 이 환경 아래에 `pip` 에서 새 패키지를 설치할 때마다, 가상 환경을 다시 활성화 합니다.

```
This makes sure that if you use a terminal program installed by that package (like `flit`), you use the one from your local environment and not any other that could be installed globally.
```

### Flit

**FastAPI** 는 [Flit](https://flit.readthedocs.io/en/latest/index.html) 을 사용하여 프로젝트를 빌드, 패키지, 공개합니다.

위와 같이 환경을 활성화 한 후, `flit` 을 설치합니다:

```
$ pip install flit

---> 100%
```

이제 환경을 다시 활성화하여 설치한  `flit` 이 전역이 아닌 환경에서 사용되고 있는지 확인하십시오.

그리고  `flit` 을 사용하여 개발 의존성을 설치합니다 :

=== "Linux, macOS"

````
<div class="termy">

```console
$ flit install --deps develop --symlink

---> 100%
```

</div>
````

=== "Windows"

````
If you are on Windows, use `--pth-file` instead of `--symlink`:

<div class="termy">

```console
$ flit install --deps develop --pth-file

---> 100%
```

</div>
````

이제 모든 의존성과 FastAPI를 당신의 로컬환경에 설치합니다.

#### 로컬 환경에서의 FastAPI 사용

FastAPI를 가져오고 사용하는 파이썬 파일을 만들어, 로컬 환경에 설치된 파이썬으로 실행하면, 로컬 FastAPI 소스코드가 사용됩니다.

그리고 `--symlink` (Windows의 경우 `--pth-file` )에 설치되어있는 로컬 FastAPI 소스코드를 업데이트한 경우, 파이썬 파일을 다시 실행하면, 새로운 버전의 FastAPI를 사용합니다.

이런 방법으로 로컬버전을 "install" 하지 않고 모든 변경 사항을 테스트 할 수 있습니다.

### Format

모든 코드를 포맷하고 지워주는 스크립트가 있습니다 :

```
$ bash scripts/format.sh
```

또한 모든 가져오기를 자동으로 정렬합니다.

올바르게 정렬하려면, 위 섹션의 명령인 `--symlink` (Windows의 경우 `--pth-file` )을 사용하여 FastAPI를 로컬환경에 설치해야 합니다.

## 문서

먼저 위와 같이 환경을 설정한다면 필요한 모든 패키지가 설치됩니다.

문서화 하는데 [MkDocs](https://www.mkdocs.org/) 를 사용하고 있습니다.

그리고 번역을 처리하기 위한 추가 도구 / 스크립트인  `./scripts/docs.py` 가 있습니다.

!!! tip "팁"`./scripts/docs.py` 의 코드를 볼 필요는 없고, 그냥 명령행에서 사용하면 됩니다.

모든 문서는 마크다운 형식으로 `./docs/en/` 디렉토리에 있습니다.

많은 자습서는 코드 블록이 있습니다.

대부분의 경우, 이러한 코드 블록들은 있는 그대로 실행할 수 있는 완전한 응용프로그램입니다.

사실, 이러한 코드 블록들은 마크다운 내부에 작성되지 않고, `./docs_src/` 디렉토리에 있는 파이썬 파일입니다.

그리고 해당 파이썬 파일은 사이트를 생성할 때 문서에 포함/삽입됩니다.

### 테스트용 문서

대부분의 테스트는 실제 문서의 예제 소스 파일에 대해 실행됩니다.

그러면 다음을 확인할 수 있습니다 :

- 문서가 최신 상태인가?
- 문서의 예제를 그대로 실행할 수 있는가?
- 대부분의 기능이 문서에 포함되어 있으며, 테스트 범위에서 보장되는가?

로컬 개발 중에, 사이트를 구축하여 변경 사항의 유무를 확인하는 스크립트가 실시간-반영 됩니다:

```
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

문서는  `http://127.0.0.1:8008` 에서 제공됩니다.

이 방법으로, 문서/소스 파일 을 편집하고 변경사항을 실시간으로 볼 수 있습니다.

#### Typer CLI (선택 사항)

 `./scripts/docs.py` 에서는 `파이썬` 프로그램에서 직접 사용하는 방법을 설명합니다.

하지만 [Typer CLI](https://typer.tiangolo.com/typer-cli/) 를 사용하여 설치한다면, 설치가 완료된 후 터미널에서 자동 완성 기능을 할 수 있습니다.

다음을 이용하여 Typer CLI를 설치를 완료할 수 있습니다:

```
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

### 앱과 문서를 동시에

다음과 같이 예시을 실행하면 :

```
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Uvicorn은 기본 값으로 `8000`포트를 사용하기 때문에,  `8008`포트인 문서와 충돌하지 않습니다.

### 번역

번역에 대한 도움은 매우 환영합니다! 그리고 이것은 커뮤니티의 도움 없이 이룰 수 없습니다. 🌎 🚀

번역을 지원하기 위한 절차는 다음과 같습니다.

#### 팁 및 지침

- 당신의 언어를 [existing pull requests](https://github.com/tiangolo/fastapi/pulls) 에서 확인하고, 변경을 요청하거나 승인하는 리뷰를 추가합니다.

!!! tip "팁" 이미 존재하는 풀 리퀘스트에  [add comments with change suggestions](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request) 할 수 있습니다.

```
Check the docs about <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">adding a pull request review</a> to approve it or request changes.
```

- [issues](https://github.com/tiangolo/fastapi/issues) 에서 당신의 언어에 대한 번역이 있는지 확인하십시오.
- 번역하는 페이지 당 한 개의 풀 리퀘스트를 추가하십시오. 이것은 다른 사용자가 검토하기 쉬워집니다.

제가 할 수 없는 언어의 경우, 병합하기 전에 다른 여러 사용자가 번역을 검토할 때까지 기다리겠습니다.

- 자신의 언어가 번역되고 있는지 확인하고, 그것에 리뷰를 추가할 수 있습니다. 리뷰는 번역이 잘 이루어졌는지 확인 할 수 있고, 그것을 병합할 수 있습니다.
- 같은 파이썬 예시를 사용하고 문서내에 있는 텍스트만을 번역합니다. 이 작업 중에 아무것도 변경할 필요가 없습니다.
- 같은 이미지, 파일, 링크를 사용하십시오. 이 작업중에 아무것도 변경할 필요가 없습니다.
- 번역을 원하는 언어의 두 문자로 된 코드를 확인하려면 표 [List of ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) 를 이용할 수 있습니다.

#### 기존 언어

스페인어처럼 이미 일부 페이지가 번역되어 있는 언어의 번역을 추가하고 싶다고 가정합니다.

스페인어의 경우, 두 문자로 된 코드가 `es` 입니다. 따라서 스페인어의 디렉토리는 `docs/es/` 에 있습니다.

!!! tip "팁" 기본 ("공식") 언어는 영어이고, `docs/en/` 에 있습니다.

이제 스페인어로 작성된 문서를 라이브 서버에서 실행합니다 :

```
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

이제 [http://127.0.0.1:8008](http://127.0.0.1:8008/) 을 열어 수정한 내용을 확인할 수 있습니다.

FastAPI 문서 웹 사이트를 보면 모든 언어에 모든 페이지가 있음을 알 수 있습니다. 그러나 일부 페이지는 번역되지 않고, 누락된 번역에 대한 알림이 있습니다.

하지만 이런 방법으로 로컬에서 실행하면 번역된 페이지만 표시됩니다.

Now let's say that you want to add a translation for the section [Features](https://github.com/kty4119/fastapi/blob/master/docs/en/docs/features.md){.internal-link target=_blank}.

- 다음 파일을 복사합니다 :

```
docs/en/docs/features.md
```

- 번역하고 싶은 언어를 위해서 이것을 정확히 같은 위치에 붙여 넣습니다. 예를들면:

```
docs/es/docs/features.md
```

!!! tip "팁" 경로와 파일의 유일한 변경 사항은  `en` 에서 `es` 로 바꾸는 언어코드입니다.

- 이제 영어로된 MkDocs config file 을 엽니다 :

```
docs/en/docs/mkdocs.yml
```

- config file에서 `docs/features.md` 의 위치를 찾습니다. :

```
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

- 편집하고자 하는 언어의 MkDocs 구성 파일을 엽니다, 예를 들면:

```
docs/es/docs/mkdocs.yml
```

- 그것을 영어와 똑같은 위치에 추가합니다, 예를 들면:

```
site_name: FastAPI
# More stuff
nav:
- FastAPI: index.md
- Languages:
  - en: /
  - es: /es/
- features.md
```

다른 항목이 있는 경우에는 번역을 포함한 새로운 항목이 영어 버전과 동일한 순서로되어 있는지 확인하십시오.

브라우저에 접속하면 문서에 새로운 섹션이 표시되어 있는 것을 확인할 수 있습니다. 🎉

이제 모든 것을 번역할 수 있고, 파일의 저장 상태를 확인할 수 있습니다.

#### 새로운 언어

아직 번역되지 않은 언어의 번역으로 추가하고 싶다고 가정합니다.

크리올어 번역을 추가하고 싶지만, 아직 문서에 없습니다.

위의 링크를 확인하면 "크리올"의 문자코드는 `ht` 입니다.

다음 단계는 스크립트를 실행하여 새로운 번역 디렉토리를 생성하는 것입니다 :

```
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
Updating ht
Updating en
```

이제 코드편집기에서 새로 생성된  `docs/ht/` 디렉토리를 확인할 수 있습니다.

!!! tip "팁" Create a first pull request with just this, to set up the configuration for the new language, before adding translations.

```
이렇게 하면 첫 번째 페이지에서 작업하는 동안 누군가 다른 페이지 작업을 도울 수 있습니다. 🚀
```

먼저 메인 페이지의 `docs/ht/index.md` 를 번역합니다.

그 후 "기존의 언어"에 대한 이전의 지시를 계속할 수 있습니다.

##### 지원되지 않는 새로운 언어

라이브 서버 스크립트를 실행할 때 지원되지 않는 언어에 대한 오류가 발생한 경우에는 다음과 같이 표시됩니다 :

```
 raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: partials/language/xx.html
```

이것은 테마가 해당 언어를 지원하지 않는다는 것을 의미합니다 (이 경우,  `xx` 의 두 문자로 된 가짜 코드).

그러나 걱정하지 마십시오, 테마 언어를 영어로 설정하여 문서의 내용을 번역할 수 있습니다.

그 필요가 있는 경우, 새로운 언어의 `mkdocs.yml` 를 다음과 같이 편집하십시오:

```
site_name: FastAPI
# More stuff
theme:
  # More stuff
  language: xx
```

언어를 `xx` (당신의 언어 코드) 에서 `en` 으로 변경합니다.

그 후 라이브 서버를 다시 시작합니다.

#### 결과 미리보기

 `./scripts/docs.py` 스크립트를 `live` 명령으로 실행하면 현재의 언어에서 이용가능한 파일과 번역만 표시됩니다.

그러나 일단 실행되면 온라인에서 보이는 것과 같이 모두 테스트 할 수 있습니다.

이를 위해, 먼저 모든 문서를 빌드합니다 :

```
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Updating es
Updating en
Building docs for: en
Building docs for: es
Successfully built docs for: es
Copying en index.md to README.md
```

이제 언어마다  `./docs_build/` 에 있는 모든 문서가 생성됩니다. 여기에는 번역이 누락된 파일을 추가하는 것과 "이 파일에는 번역이 아직 없습니다" 라는 메모가 포함되어 있습니다. 그러나 그 디렉토리에서 아무것도 할 필요가 없습니다.

그런 다음 각 언어에 대한 모든 독립 MkDocs 사이트를 빌드하여 그것들을 결합하고  `./site/` 에서 생성한다.

그러면 `serve` 명령으로 그것을 처리할 수 있습니다:

```
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

## 테스트

로컬에서 모든 코드를 테스트하고 HTML에서 coverage 보고서를 생성하기 위한 스크립트가 있습니다:

```
$ bash scripts/test-cov-html.sh
```

이 명령은 `./htmlcov/` 디렉토리를 생성합니다. 브라우저에서 `./htmlcov/index.html` 파일을 열면, 테스트에 포함된 코드의 영역을 대화식으로 탐색할 수 있고 누락된 영역이 있는지 확인할 수 있습니다.

