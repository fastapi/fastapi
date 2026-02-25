# Dataclasses の使用 { #using-dataclasses }

FastAPI は **Pydantic** の上に構築されており、これまでにリクエストやレスポンスを宣言するために Pydantic モデルを使う方法を紹介してきました。

しかし FastAPI は、同様の方法で <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> もサポートします:

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

これは **Pydantic** によって引き続きサポートされています。Pydantic には <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">`dataclasses` の内部サポート</a> があるためです。

そのため、上記のように明示的に Pydantic を使っていないコードでも、FastAPI は標準の dataclass を Pydantic 独自の dataclass に変換するために Pydantic を使用しています。

そして当然ながら、次の点も同様にサポートされます:

- データ検証
- データのシリアライズ
- データのドキュメント化 など

これは Pydantic モデルの場合と同じように動作します。内部的にも同様に Pydantic を使って実現されています。

/// info | 情報

dataclasses は、Pydantic モデルができることをすべては行えない点に留意してください。

そのため、Pydantic モデルを使う必要がある場合もあります。

しかし既存の dataclass が多数あるなら、FastAPI で Web API を構築する際にそれらを活用するちょっとしたテクニックになります。🤓

///

## `response_model` での dataclasses { #dataclasses-in-response-model }

`response_model` パラメータでも `dataclasses` を使用できます:

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

dataclass は自動的に Pydantic の dataclass に変換されます。

このため、そのスキーマは API ドキュメントの UI に表示されます:

<img src="/img/tutorial/dataclasses/image01.png">

## ネストしたデータ構造での dataclasses { #dataclasses-in-nested-data-structures }

`dataclasses` を他の型注釈と組み合わせて、ネストしたデータ構造を作成できます。

場合によっては、自動生成された API ドキュメントでエラーが発生するなどの理由で、Pydantic 版の `dataclasses` を使う必要があるかもしれません。

その場合は、標準の `dataclasses` を `pydantic.dataclasses` に置き換えるだけで済みます。これはドロップイン置換です:

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. 依然として標準の `dataclasses` から `field` をインポートします。

2. `pydantic.dataclasses` は `dataclasses` のドロップイン置換です。

3. `Author` dataclass は `Item` dataclass のリストを含みます。

4. `Author` dataclass を `response_model` パラメータとして使用しています。

5. リクエストボディとしての dataclass と併せて、他の標準の型注釈を使用できます。

    この例では、`Item` dataclass のリストです。

6. ここでは、dataclass のリストである `items` を含む辞書を返しています。

    FastAPI はデータを JSON に <dfn title="送信可能な形式にデータを変換すること">シリアライズ</dfn> できます。

7. ここでは `response_model` に `Author` dataclass のリストという型注釈を使用しています。

    このように、`dataclasses` は標準の型注釈と組み合わせられます。

8. この *path operation 関数* は、`async def` ではなく通常の `def` を使用しています。

    いつもどおり、FastAPI では必要に応じて `def` と `async def` を組み合わせられます。

    どちらをいつ使うかの復習が必要な場合は、[`async` と `await`](../async.md#in-a-hurry){.internal-link target=_blank} に関するドキュメントの _"In a hurry?"_ セクションを参照してください。

9. この *path operation 関数* は（可能ではありますが）dataclass 自体は返さず、内部データを持つ辞書のリストを返しています。

    FastAPI は dataclass を含む `response_model` パラメータを使ってレスポンスを変換します。

`dataclasses` は他の型注釈と多様な組み合わせが可能で、複雑なデータ構造を構成できます。

上記のコード内コメントのヒントを参照して、より具体的な詳細を確認してください。

## さらに学ぶ { #learn-more }

`dataclasses` を他の Pydantic モデルと組み合わせたり、継承したり、自分のモデルに含めたりもできます。

詳しくは、<a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">dataclasses に関する Pydantic ドキュメント</a> を参照してください。

## バージョン { #version }

これは FastAPI バージョン `0.67.0` 以降で利用可能です。🔖
