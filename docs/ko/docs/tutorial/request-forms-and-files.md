# 폼 및 파일 요청 { #request-forms-and-files }

`File` 과 `Form` 을 사용하여 파일과 폼 필드를 동시에 정의할 수 있습니다.

/// info | 정보

업로드된 파일 및/또는 폼 데이터를 받으려면 먼저 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>를 설치해야 합니다.

[가상 환경](../virtual-environments.md){.internal-link target=_blank}을 생성하고, 활성화한 다음 설치해야 합니다. 예:

```console
$ pip install python-multipart
```

///

## `File` 및 `Form` 임포트 { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## `File` 및 `Form` 매개변수 정의 { #define-file-and-form-parameters }

`Body` 및 `Query`와 동일한 방식으로 파일과 폼의 매개변수를 생성합니다:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

파일과 폼 필드는 폼 데이터로 업로드되며, 파일과 폼 필드를 받게 됩니다.

또한 일부 파일은 `bytes`로, 일부 파일은 `UploadFile`로 선언할 수 있습니다.

/// warning | 경고

다수의 `File`과 `Form` 매개변수를 한 *경로 처리*에 선언하는 것이 가능하지만, 요청의 본문이 `application/json`가 아닌 `multipart/form-data`로 인코딩되기 때문에 JSON으로 받기를 기대하는 `Body` 필드를 함께 선언할 수는 없습니다.

이는 **FastAPI**의 한계가 아니라, HTTP 프로토콜의 일부입니다.

///

## 요약 { #recap }

하나의 요청으로 데이터와 파일들을 받아야 할 경우 `File`과 `Form`을 함께 사용하기 바랍니다.
