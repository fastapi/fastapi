# フォームモデル { #form-models }

FastAPI では、**フォームフィールド**を宣言するために **Pydantic モデル**を使用できます。

/// note | 備考

フォームを使うには、まず [`python-multipart`](https://github.com/Kludex/python-multipart) をインストールします。

プロジェクトに追加します:

```console
$ uv add python-multipart
```

///

/// note | 備考

これは FastAPI バージョン `0.113.0` 以降でサポートされています。🤓

///

## フォーム用の Pydantic モデル { #pydantic-models-for-forms }

受け取りたいフィールドを **フォームフィールド** として持つ **Pydantic モデル** を宣言し、パラメータを `Form` として宣言するだけです:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** はリクエストの **フォームデータ** から **各フィールド** のデータを **抽出** し、定義した Pydantic モデルとして渡します。

[HTML チェックボックス](request-forms.md#boolean-form-fields)には、デフォルト値を `False` とした真偽値フィールドを宣言します。

## ドキュメントで確認 { #check-the-docs }

`/docs` のドキュメント UI で確認できます:

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 追加のフォームフィールドを禁止 { #forbid-extra-form-fields }

一部の特殊なユースケース（おそらくあまり一般的ではありません）では、フォームフィールドを Pydantic モデルで宣言したもののみに**制限**し、**追加**のフィールドを**禁止**したい場合があります。

/// note | 備考

これは FastAPI バージョン `0.114.0` 以降でサポートされています。🤓

///

Pydantic のモデル設定で、`extra` フィールドを `forbid` にできます:

{* ../../docs_src/request_form_models/tutorial002_an_py310.py hl[12] *}

クライアントが余分なデータを送信しようとすると、**エラー**のレスポンスを受け取ります。

例えば、クライアントが次のフォームフィールドを送ろうとした場合:

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

フィールド `extra` は許可されていない旨のエラーレスポンスが返されます:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## フォームモデルの組み合わせ { #combine-form-models }

複数のフォームモデルと個別の `Form` パラメータを組み合わせることができます。

{* ../../docs_src/request_form_models/tutorial003_an_py310.py hl[9:14,19:21] *}

クライアントは `name`、`tags`、`token` をフォームフィールドとして送信します。各モデルはフォームフィールドを個別に検証します。

各モデルの `extra` 設定は、他のパラメータや依存関係で宣言されたフィールドやファイルを含む、すべてのフォームフィールドに適用されます。`extra="forbid"` では、そのモデルにないフィールドはすべて拒否されます。`extra="allow"` では、それらのフィールドはモデルの追加データとして含まれます。

複数の宣言で同じフォームフィールド名を使用すると、それぞれがそのフィールドの値を検証します。OpenAPI スキーマで一貫した記述ができるように、共有フィールドには互換性のある型と制約を使用してください。

## オプションのフォームモデル { #optional-form-models }

フォームモデルに `| None` とデフォルト値 `None` を指定して宣言すると、フィールドのグループをオプションにできます。

{* ../../docs_src/request_form_models/tutorial005_an_py310.py hl[17] *}

`name` も `age` も送信されない場合、`profile` は `None` になります。どちらかが送信された場合、FastAPI はモデルを検証し、両方のフィールドを必須とします。空の値を送信した場合も、フィールドが指定されたものとして扱われます。

デフォルト値なしで `| None` を使用した場合、パラメータは必須のままです。

追加のフィールドはモデルの `extra` 設定に従います。無視された追加フィールドによって、モデルが指定されたことにはなりません。

チェックされていないチェックボックスのみを含むオプションのモデルは省略されます。明示的に指定するには、`enabled=false` などの値を送信してください。

## フォームモデルのオプションの Union { #optional-unions-of-form-models }

モデルのオプションの Union も使用できます。

{* ../../docs_src/request_form_models/tutorial006_an_py310.py hl[9:16,21] *}

フォームフィールドが送信されない場合、`contact` は `None` になります。`kind=person` と `name`、または `kind=company` と `company_name` を送信してください。判別子によって検証するモデルが選択されます。

## フォームモデルの Union の組み合わせ { #combine-unions-of-form-models }

Union を他のフォームモデル、個別の `Form` パラメータ、`File` パラメータと組み合わせることができます。各 Union は個別に検証されます。

{* ../../docs_src/request_form_models/tutorial007_an_py310.py hl[31:35] *}

すべてのフィールドを同じフォームで送信してください。例えば、`contact_type=person`、`name=Rick`、`notification_type=email`、`email=rick@example.com`、`token=secret` を送信します。

`notification` を `None` のままにするには、通知用のフィールドを省略してください。

## フォームモデルとファイル { #form-models-and-files }

フォームモデルを[ファイルパラメータ](request-files.md)と組み合わせることもできます。

{* ../../docs_src/request_form_models/tutorial004_an_py310.py hl[14] *}

ここでは、クライアントは `multipart/form-data` を使用して `name` フィールドと `avatar` ファイルを送信します。

## まとめ { #summary }

FastAPI でフォームフィールドを宣言するために Pydantic モデルを使用できます。😎
