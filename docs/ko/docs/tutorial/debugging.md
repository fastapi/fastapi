# 디버깅

예를 들면 Visual Studio Code 또는 PyCharm을 사용하여 편집기에서 디버거를 연결할 수 있습니다.

## `uvicorn` 호출

FastAPI 애플리케이션에서 `uvicorn`을 직접 임포트하여 실행합니다

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### `__name__ == "__main__"` 에 대하여

`__name__ == "__main__"`의 주요 목적은 다음과 같이 파일이 호출될 때 실행되는 일부 코드를 갖는 것입니다.

<div class="termy">

```console
$ python myapp.py
```

</div>

그러나 다음과 같이 다른 파일을 가져올 때는 호출되지 않습니다.

```Python
from myapp import app
```

#### 추가 세부사항

파일 이름이 `myapp.py`라고 가정해 보겠습니다.

다음과 같이 실행하면

<div class="termy">

```console
$ python myapp.py
```

</div>

Python에 의해 자동으로 생성된 파일의 내부 변수 `__name__`은 문자열 `"__main__"`을 값으로 갖게 됩니다.

따라서 섹션

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

이 실행됩니다.

---

해당 모듈(파일)을 가져오면 이런 일이 발생하지 않습니다

그래서 다음과 같은 다른 파일 `importer.py`가 있는 경우:

```Python
from myapp import app

# Some more code
```

이 경우 `myapp.py` 내부의 자동 변수에는 값이 `"__main__"`인 변수 `__name__`이 없습니다.

따라서 다음 행

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

은 실행되지 않습니다.

/// info | 정보

자세한 내용은 <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">공식 Python 문서</a>를 확인하세요

///

## 디버거로 코드 실행

코드에서 직접 Uvicorn 서버를 실행하고 있기 때문에 디버거에서 직접 Python 프로그램(FastAPI 애플리케이션)을 호출할 수 있습니다.

---

예를 들어 Visual Studio Code에서 다음을 수행할 수 있습니다.

* "Debug" 패널로 이동합니다.
* "Add configuration...".
* "Python"을 선택합니다.
* "`Python: Current File (Integrated Terminal)`" 옵션으로 디버거를 실행합니다.

그런 다음 **FastAPI** 코드로 서버를 시작하고 중단점 등에서 중지합니다.

다음과 같이 표시됩니다.

<img src="/img/tutorial/debugging/image01.png">

---

Pycharm을 사용하는 경우 다음을 수행할 수 있습니다

* "Run" 메뉴를 엽니다
* "Debug..." 옵션을 선택합니다.
* 그러면 상황에 맞는 메뉴가 나타납니다.
* 디버그할 파일을 선택합니다(이 경우 `main.py`).

그런 다음 **FastAPI** 코드로 서버를 시작하고 중단점 등에서 중지합니다.

다음과 같이 표시됩니다.

<img src="/img/tutorial/debugging/image02.png">
