# JSON互換エンコーダ

データ型（Pydanticモデルのような）をJSONと互換性のあるもの（`dict`や`list`など）に変更する必要がある場合があります。

例えば、データベースに保存する必要がある場合です。

そのために、**FastAPI** は`jsonable_encoder()`関数を提供しています。

## `jsonable_encoder`の使用

JSON互換のデータのみを受信するデータベース`fake_db`があるとしましょう。

例えば、`datetime`オブジェクトはJSONと互換性がないので、このデーターベースには受け取られません。

そのため、`datetime`オブジェクトは<a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO形式</a>のデータを含む`str`に変換されなければなりません。

同様に、このデータベースはPydanticモデル（属性を持つオブジェクト）を受け取らず、`dict`だけを受け取ります。

そのために`jsonable_encoder`を使用することができます。

Pydanticモデルのようなオブジェクトを受け取り、JSON互換版を返します:

{* ../../docs_src/encoder/tutorial001.py hl[5,22] *}

この例では、Pydanticモデルを`dict`に、`datetime`を`str`に変換します。

呼び出した結果は、Pythonの標準の<a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>でエンコードできるものです。

これはJSON形式のデータを含む大きな`str`を（文字列として）返しません。JSONと互換性のある値とサブの値を持つPython標準のデータ構造（例：`dict`）を返します。

/// note | 備考

`jsonable_encoder`は実際には **FastAPI** が内部的にデータを変換するために使用します。しかしこれは他の多くのシナリオで有用です。

///
