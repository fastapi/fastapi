# LLM 테스트 파일 { #llm-test-file }

이 문서는 문서를 번역하는 <abbr title="Large Language Model - 대규모 언어 모델">LLM</abbr>이 `scripts/translate.py`의 `general_prompt`와 `docs/{language code}/llm-prompt.md`의 언어별 프롬프트를 이해하는지 테스트합니다. 언어별 프롬프트는 `general_prompt`에 추가됩니다.

여기에 추가된 테스트는 언어별 프롬프트를 설계하는 모든 사람이 보게 됩니다.

사용 방법은 다음과 같습니다:

* 언어별 프롬프트 `docs/{language code}/llm-prompt.md`를 준비합니다.
* 이 문서를 원하는 대상 언어로 새로 번역합니다(예: `translate.py`의 `translate-page` 명령). 그러면 `docs/{language code}/docs/_llm-test.md` 아래에 번역이 생성됩니다.
* 번역에서 문제가 없는지 확인합니다.
* 필요하다면 언어별 프롬프트, 일반 프롬프트, 또는 영어 문서를 개선합니다.
* 그런 다음 번역에서 남아 있는 문제를 수동으로 수정해 좋은 번역이 되게 합니다.
* 좋은 번역을 둔 상태에서 다시 번역합니다. 이상적인 결과는 LLM이 더 이상 번역에 변경을 만들지 않는 것입니다. 이는 일반 프롬프트와 언어별 프롬프트가 가능한 한 최선이라는 뜻입니다(때때로 몇 가지 seemingly random 변경을 할 수 있는데, 그 이유는 [LLM은 결정론적 알고리즘이 아니기 때문](https://doublespeak.chat/#/handbook#deterministic-output)입니다).

테스트:

## 코드 스니펫 { #code-snippets }

//// tab | 테스트

다음은 코드 스니펫입니다: `foo`. 그리고 이것은 또 다른 코드 스니펫입니다: `bar`. 그리고 또 하나: `baz quux`.

////

//// tab | 정보

코드 스니펫의 내용은 그대로 두어야 합니다.

`scripts/translate.py`의 일반 프롬프트에서 `### Content of code snippets` 섹션을 참고하세요.

////

## 따옴표 { #quotes }

//// tab | 테스트

어제 제 친구가 이렇게 썼습니다: "If you spell incorrectly correctly, you have spelled it incorrectly". 이에 저는 이렇게 답했습니다: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'".

/// note | 참고

LLM은 아마 이것을 잘못 번역할 것입니다. 흥미로운 점은 재번역할 때 고정된 번역을 유지하는지 여부뿐입니다.

///

////

//// tab | 정보

프롬프트 설계자는 중립 따옴표를 타이포그래피 따옴표로 변환할지 선택할 수 있습니다. 그대로 두어도 괜찮습니다.

예를 들어 `docs/de/llm-prompt.md`의 `### Quotes` 섹션을 참고하세요.

////

## 코드 스니펫의 따옴표 { #quotes-in-code-snippets }

//// tab | 테스트

`pip install "foo[bar]"`

코드 스니펫에서 문자열 리터럴의 예: `"this"`, `'that'`.

코드 스니펫에서 문자열 리터럴의 어려운 예: `f"I like {'oranges' if orange else "apples"}"`

하드코어: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | 정보

... 하지만 코드 스니펫 안의 따옴표는 그대로 유지되어야 합니다.

////

## 코드 블록 { #code-blocks }

//// tab | 테스트

Bash 코드 예시...

```bash
# 우주에 인사말 출력
echo "Hello universe"
```

...그리고 콘솔 코드 예시...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...그리고 또 다른 콘솔 코드 예시...

```console
// "Code" 디렉터리 생성
$ mkdir code
// 해당 디렉터리로 이동
$ cd code
```

...그리고 Python 코드 예시...

```Python
wont_work()  # 이건 동작하지 않습니다 😱
works(foo="bar")  # 이건 동작합니다 🎉
```

...이상입니다.

////

//// tab | 정보

코드 블록의 코드는(주석을 제외하고) 수정하면 안 됩니다.

`scripts/translate.py`의 일반 프롬프트에서 `### Content of code blocks` 섹션을 참고하세요.

////

## 탭과 색상 박스 { #tabs-and-colored-boxes }

//// tab | 테스트

/// info | 정보
일부 텍스트
///

/// note | 참고
일부 텍스트
///

/// note | 기술 세부사항
일부 텍스트
///

/// check | 확인
일부 텍스트
///

/// tip | 팁
일부 텍스트
///

/// warning | 경고
일부 텍스트
///

/// danger | 위험
일부 텍스트
///

////

//// tab | 정보

탭과 `Info`/`Note`/`Warning`/등의 블록은 제목 번역을 수직 막대(`|`) 뒤에 추가해야 합니다.

`scripts/translate.py`의 일반 프롬프트에서 `### Special blocks`와 `### Tab blocks` 섹션을 참고하세요.

////

## 웹 및 내부 링크 { #web-and-internal-links }

//// tab | 테스트

링크 텍스트는 번역되어야 하고, 링크 주소는 변경되지 않아야 합니다:

* [위의 제목으로 가는 링크](#code-snippets)
* [내부 링크](index.md#installation)
* [외부 링크](https://sqlmodel.tiangolo.com/)
* [스타일로 가는 링크](https://fastapi.tiangolo.com/css/styles.css)
* [스크립트로 가는 링크](https://fastapi.tiangolo.com/js/logic.js)
* [이미지로 가는 링크](https://fastapi.tiangolo.com/img/foo.jpg)

링크 텍스트는 번역되어야 하고, 링크 주소는 번역 페이지를 가리켜야 합니다:

* [FastAPI 링크](https://fastapi.tiangolo.com/ko/)

////

//// tab | 정보

링크는 번역되어야 하지만, 주소는 변경되지 않아야 합니다. 예외는 FastAPI 문서 페이지로 향하는 절대 링크이며, 이 경우 번역 페이지로 연결되어야 합니다.

`scripts/translate.py`의 일반 프롬프트에서 `### Links` 섹션을 참고하세요.

////

## HTML "abbr" 요소 { #html-abbr-elements }

//// tab | 테스트

여기 HTML "abbr" 요소로 감싼 몇 가지가 있습니다(일부는 임의로 만든 것입니다):

### abbr가 전체 문구를 제공 { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done - 일을 끝내는 방법론">GTD</abbr>
* <abbr title="less than - 보다 작음"><code>lt</code></abbr>
* <abbr title="XML Web Token - XML 웹 토큰">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface - 병렬 서버 게이트웨이 인터페이스">PSGI</abbr>

### abbr가 전체 문구와 설명을 제공 { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network - 모질라 개발자 네트워크: Firefox를 만드는 사람들이 작성한 개발자용 문서">MDN</abbr>
* <abbr title="Input/Output - 입력/출력: 디스크 읽기 또는 쓰기, 네트워크 통신.">I/O</abbr>.

////

//// tab | 정보

"abbr" 요소의 "title" 속성은 몇 가지 구체적인 지침에 따라 번역됩니다.

번역에서는(영어 단어를 설명하기 위해) 자체 "abbr" 요소를 추가할 수 있으며, LLM은 이를 제거하면 안 됩니다.

`scripts/translate.py`의 일반 프롬프트에서 `### HTML abbr elements` 섹션을 참고하세요.

////

## HTML "dfn" 요소 { #html-dfn-elements }

* <dfn title="어떤 방식으로든 서로 연결되고 함께 작동하도록 구성된 머신들의 집합입니다.">클러스터</dfn>
* <dfn title="입력과 출력 계층 사이에 수많은 은닉 계층을 둔 인공 신경망을 사용하는 머신 러닝 방법으로, 이를 통해 포괄적인 내부 구조를 형성합니다">딥 러닝</dfn>

## 제목 { #headings }

//// tab | 테스트

### 웹앱 개발하기 - 튜토리얼 { #develop-a-webapp-a-tutorial }

안녕하세요.

### 타입 힌트와 -애너테이션 { #type-hints-and-annotations }

다시 안녕하세요.

### super- 및 subclasses { #super-and-subclasses }

다시 안녕하세요.

////

//// tab | 정보

제목에 대한 유일한 강한 규칙은, LLM이 중괄호 안의 해시 부분을 변경하지 않아 링크가 깨지지 않게 하는 것입니다.

`scripts/translate.py`의 일반 프롬프트에서 `### Headings` 섹션을 참고하세요.

언어별 지침은 예를 들어 `docs/de/llm-prompt.md`의 `### Headings` 섹션을 참고하세요.

////

## 문서에서 사용되는 용어 { #terms-used-in-the-docs }

//// tab | 테스트

* 여러분
* 여러분의

* 예:
* 등

* `foo`로서의 `int`
* `bar`로서의 `str`
* `baz`로서의 `list`

* 튜토리얼 - 사용자 가이드
* 고급 사용자 가이드
* SQLModel 문서
* API 문서
* 자동 문서

* Data Science
* Deep Learning
* Machine Learning
* Dependency Injection
* HTTP Basic authentication
* HTTP Digest
* ISO format
* JSON Schema 표준
* JSON schema
* schema definition
* Password Flow
* Mobile

* deprecated
* designed
* invalid
* on the fly
* standard
* default
* case-sensitive
* case-insensitive

* 애플리케이션을 서빙하다
* 페이지를 서빙하다

* 앱
* 애플리케이션

* 요청
* 응답
* 오류 응답

* 경로 처리
* 경로 처리 데코레이터
* 경로 처리 함수

* body
* 요청 body
* 응답 body
* JSON body
* form body
* file body
* 함수 body

* parameter
* body parameter
* path parameter
* query parameter
* cookie parameter
* header parameter
* form parameter
* function parameter

* event
* startup event
* 서버 startup
* shutdown event
* lifespan event

* handler
* event handler
* exception handler
* 처리하다

* model
* Pydantic model
* data model
* database model
* form model
* model object

* class
* base class
* parent class
* subclass
* child class
* sibling class
* class method

* header
* headers
* authorization header
* `Authorization` header
* forwarded header

* dependency injection system
* dependency
* dependable
* dependant

* I/O bound
* CPU bound
* concurrency
* parallelism
* multiprocessing

* env var
* environment variable
* `PATH`
* `PATH` variable

* authentication
* authentication provider
* authorization
* authorization form
* authorization provider
* 사용자가 인증한다
* 시스템이 사용자를 인증한다

* CLI
* command line interface

* server
* client

* cloud provider
* cloud service

* development
* development stages

* dict
* dictionary
* enumeration
* enum
* enum member

* encoder
* decoder
* encode하다
* decode하다

* exception
* raise하다

* expression
* statement

* frontend
* backend

* GitHub discussion
* GitHub issue

* performance
* performance optimization

* return type
* return value

* security
* security scheme

* task
* background task
* task function

* template
* template engine

* type annotation
* type hint

* server worker
* Uvicorn worker
* Gunicorn Worker
* worker process
* worker class
* workload

* deployment
* deploy하다

* SDK
* software development kit

* `APIRouter`
* `requirements.txt`
* Bearer Token
* breaking change
* bug
* button
* callable
* code
* commit
* context manager
* coroutine
* database session
* disk
* domain
* engine
* fake X
* HTTP GET method
* item
* library
* lifespan
* lock
* middleware
* mobile application
* module
* mounting
* network
* origin
* override
* payload
* processor
* property
* proxy
* pull request
* query
* RAM
* remote machine
* status code
* string
* tag
* web framework
* wildcard
* return하다
* validate하다

////

//// tab | 정보

이것은 문서에서 보이는 (대부분) 기술 용어의 불완전하고 비규범적인 목록입니다. 프롬프트 설계자가 어떤 용어에 대해 LLM에 추가적인 도움이 필요한지 파악하는 데 유용할 수 있습니다. 예를 들어, 좋은 번역을 계속 덜 좋은 번역으로 되돌릴 때, 또는 언어에서 용어의 활용/변화를 처리하는 데 문제가 있을 때 도움이 됩니다.

예를 들어 `docs/de/llm-prompt.md`의 `### List of English terms and their preferred German translations` 섹션을 참고하세요.

////
