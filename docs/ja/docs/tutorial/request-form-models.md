# フォームモデル { #form-models }

FastAPI では、フォームフィールドを宣言するために Pydantic モデルを使用できます。

/// info | 情報

フォームを使うには、まず <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> をインストールします。

まず [仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成して有効化し、そのうえでインストールしてください。例えば:

```console
$ pip install python-multipart
```

///

/// note | 備考

これは FastAPI バージョン `0.113.0` 以降でサポートされています。🤓

///

## フォーム用の Pydantic モデル { #pydantic-models-for-forms }

受け取りたいフィールドを **フォームフィールド** として持つ **Pydantic モデル** を宣言し、パラメータを `Form` として宣言するだけです:

{* ../../docs_src/request_form_models/tutorial001_an_py310.py hl[9:11,15] *}

**FastAPI** はリクエストの **フォームデータ** から **各フィールド** のデータを **抽出** し、定義した Pydantic モデルとして渡します。

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

- `username`: `Rick`
- `password`: `Portal Gun`
- `extra`: `Mr. Poopybutthole`

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

## まとめ { #summary }

FastAPI でフォームフィールドを宣言するために Pydantic モデルを使用できます。😎
