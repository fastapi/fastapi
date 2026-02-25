# ヘッダーパラメータのモデル { #header-parameter-models }

関連する**ヘッダーパラメータ**が一式ある場合、それらを宣言するための**Pydantic モデル**を作成できます。

これにより、モデルを**複数箇所**で**再利用**でき、さらにすべてのパラメータに対するバリデーションやメタデータを一括で宣言できます。😎

/// note | 備考

これは FastAPI バージョン `0.115.0` 以降でサポートされています。🤓

///

## Pydantic モデルによるヘッダーパラメータ { #header-parameters-with-a-pydantic-model }

必要な**ヘッダーパラメータ**を**Pydantic モデル**内で宣言し、関数引数ではそのパラメータを `Header` として宣言します:

{* ../../docs_src/header_param_models/tutorial001_an_py310.py hl[9:14,18] *}

**FastAPI** はリクエストの**ヘッダー**から**各フィールド**の値を**抽出**し、定義した Pydantic モデルとして渡します。

## ドキュメントの確認 { #check-the-docs }

`/docs` のドキュメント UI で必要なヘッダーを確認できます:

<div class="screenshot">
<img src="/img/tutorial/header-param-models/image01.png">
</div>

## 余分なヘッダーを禁止 { #forbid-extra-headers }

特殊なユースケース（あまり一般的ではありません）では、受け付けるヘッダーを**制限**したい場合があります。

Pydantic のモデル設定で `extra` フィールドを `forbid` にして禁止できます:

{* ../../docs_src/header_param_models/tutorial002_an_py310.py hl[10] *}

クライアントが**余分なヘッダー**を送信しようとすると、**エラー**レスポンスが返されます。

例えば、クライアントが値 `plumbus` の `tool` ヘッダーを送ろうとすると、ヘッダーパラメータ `tool` は許可されていない旨の**エラー**レスポンスが返されます:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["header", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus",
        }
    ]
}
```

## アンダースコア変換の無効化 { #disable-convert-underscores }

通常のヘッダーパラメータと同様に、パラメータ名にアンダースコアがある場合は**自動的にハイフンに変換**されます。

例えば、コード上でヘッダーパラメータ `save_data` を定義すると、想定される HTTP ヘッダーは `save-data` となり、ドキュメント上にもそのように表示されます。

何らかの理由でこの自動変換を無効化する必要がある場合、ヘッダーパラメータ用の Pydantic モデルでも無効化できます。

{* ../../docs_src/header_param_models/tutorial003_an_py310.py hl[19] *}

/// warning | 注意

`convert_underscores` を `False` に設定する前に、アンダースコアを含むヘッダーの使用を禁止している HTTP プロキシやサーバーがあることに留意してください。

///

## まとめ { #summary }

**Pydantic モデル**を使って **FastAPI** で **ヘッダー**を宣言できます。😎
