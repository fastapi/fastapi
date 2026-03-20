# 바이트를 Base64로 포함하는 JSON { #json-with-bytes-as-base64 }

애플리케이션에서 JSON 데이터를 주고받아야 하지만 그 안에 바이너리 데이터를 포함해야 한다면, base64로 인코딩해서 포함할 수 있습니다.

## Base64와 파일 { #base64-vs-files }

바이너리 데이터 업로드에는 [요청 파일](../tutorial/request-files.md)을, 바이너리 데이터 전송에는 [커스텀 응답 - FileResponse](./custom-response.md#fileresponse--fileresponse-)를 사용할 수 있는지 먼저 고려하세요. JSON으로 인코딩하는 대신 말입니다.

JSON은 UTF-8로 인코딩된 문자열만 포함할 수 있으므로, 원시 바이트를 그대로 담을 수 없습니다.

Base64는 바이너리 데이터를 문자열로 인코딩할 수 있지만, 이를 위해 원래의 바이너리 데이터보다 더 많은 문자 수를 사용해야 하므로 일반적인 파일 전송보다 비효율적일 수 있습니다.

반드시 JSON 안에 바이너리 데이터를 포함해야 하고, 파일을 사용할 수 없을 때만 base64를 사용하세요.

## Pydantic `bytes` { #pydantic-bytes }

`bytes` 필드를 가진 Pydantic 모델을 선언하고, 모델 설정에서 `val_json_bytes`를 사용하도록 지정하면 입력 JSON 데이터를 base64로 “검증”하도록 할 수 있습니다. 이 검증 과정의 일부로 base64 문자열을 바이트로 디코딩합니다.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

`/docs`를 확인하면 `data` 필드가 base64로 인코딩된 bytes를 기대한다고 표시됩니다:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

아래와 같은 요청을 보낼 수 있습니다:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | 팁

`aGVsbG8=`는 `hello`의 base64 인코딩입니다.

///

그러면 Pydantic이 base64 문자열을 디코딩하여 모델의 `data` 필드에 원래 바이트를 제공합니다.

다음과 같은 응답을 받게 됩니다:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## 출력 데이터용 Pydantic `bytes` { #pydantic-bytes-for-output-data }

출력 데이터에도 모델 설정에서 `ser_json_bytes`와 함께 `bytes` 필드를 사용할 수 있습니다. 그러면 Pydantic이 JSON 응답을 생성할 때 바이트를 base64로 “직렬화”합니다.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## 입력과 출력 데이터용 Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

물론, 동일한 모델을 사용해 JSON 데이터를 받을 때는 `val_json_bytes`로 입력을 “검증”하고, JSON 데이터를 보낼 때는 `ser_json_bytes`로 출력을 “직렬화”하도록 base64를 모두 처리하게 구성할 수 있습니다.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
