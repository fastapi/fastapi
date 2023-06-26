# 폼 및 파일 요청

`File` 과 `Form` 을 사용하여 파일과 폼을 함께 정의할 수 있습니다.

!!! info "정보"
    파일과 폼 데이터를 함께, 또는 각각 업로드하기 위해 먼저 <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>를 설치해야합니다.

    예 ) `pip install python-multipart`.

## `File` 및 `Form` 업로드

```Python hl_lines="1"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

## `File` 및 `Form` 매개변수 정의

`Body` 및 `Query`와 동일한 방식으로 파일과 폼의 매개변수를 생성합니다:

```Python hl_lines="8"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

파일과 폼 필드는 폼 데이터 형식으로 업로드되어 파일과 폼 필드로 전달됩니다.

어떤 파일들은 `bytes`로, 또 어떤 파일들은 `UploadFile`로 선언할 수 있습니다.

!!! warning "주의"
    다수의 `File`과 `Form` 매개변수를 한 *경로 작동*에 선언하는 것이 가능하지만, 요청의 본문이 `application/json`가 아닌 `multipart/form-data`로 인코딩 되기 때문에 JSON으로 받아야하는 `Body` 필드를 함께 선언할 수는 없습니다.

    이는 **FastAPI**의 한계가 아니라, HTTP 프로토콜에 의한 것입니다.

## 요약

하나의 요청으로 데이터와 파일들을 받아야 할 경우 `File`과 `Form`을 함께 사용하기 바랍니다.
