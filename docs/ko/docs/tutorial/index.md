# 자습서 - 사용자 안내서 { #tutorial-user-guide }

이 자습서는 **FastAPI**의 대부분의 기능을 단계별로 사용하는 방법을 보여줍니다.

각 섹션은 이전 섹션을 바탕으로 점진적으로 구성되지만, 주제를 분리한 구조로 되어 있어 특정 API 요구사항을 해결하기 위해 원하는 섹션으로 바로 이동할 수 있습니다.

또한 나중에 참고 자료로도 사용할 수 있도록 만들어졌으므로, 필요할 때 다시 돌아와 정확히 필요한 내용을 확인할 수 있습니다.

## 코드 실행하기 { #run-the-code }

모든 코드 블록은 복사해서 바로 사용할 수 있습니다(실제로 테스트된 Python 파일입니다).

예제 중 어떤 것이든 실행하려면, 코드를 `main.py` 파일에 복사하고 다음으로 `fastapi dev`를 시작하세요:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

코드를 작성하거나 복사한 뒤 편집하고, 로컬에서 실행하는 것을 **강력히 권장**합니다.

에디터에서 사용해 보면, 작성해야 하는 코드가 얼마나 적은지, 모든 타입 검사와 자동완성 등 FastAPI의 이점을 제대로 확인할 수 있습니다.

---

## FastAPI 설치 { #install-fastapi }

첫 단계는 FastAPI를 설치하는 것입니다.

[가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고 활성화한 다음, **FastAPI를 설치**하세요:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | 참고

`pip install "fastapi[standard]"`로 설치하면 `fastapi-cloud-cli`를 포함한 몇 가지 기본 선택적 standard 의존성이 함께 설치되며, 이를 사용해 <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>에 배포할 수 있습니다.

이러한 선택적 의존성이 필요 없다면 `pip install fastapi`로 대신 설치할 수 있습니다.

standard 의존성은 설치하되 `fastapi-cloud-cli` 없이 설치하려면 `pip install "fastapi[standard-no-fastapi-cloud-cli]"`로 설치할 수 있습니다.

///

## 고급 사용자 안내서 { #advanced-user-guide }

이 **자습서 - 사용자 안내서**를 읽은 뒤에 나중에 읽을 수 있는 **고급 사용자 안내서**도 있습니다.

**고급 사용자 안내서**는 이 문서를 바탕으로 동일한 개념을 사용하며, 몇 가지 추가 기능을 알려줍니다.

하지만 먼저 **자습서 - 사용자 안내서**(지금 읽고 있는 내용)를 읽어야 합니다.

**자습서 - 사용자 안내서**만으로 완전한 애플리케이션을 만들 수 있도록 설계되었고, 필요에 따라 **고급 사용자 안내서**의 추가 아이디어를 활용해 다양한 방식으로 확장할 수 있습니다.
