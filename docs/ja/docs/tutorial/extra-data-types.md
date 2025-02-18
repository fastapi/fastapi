# 追加データ型

今までは、以下のような一般的なデータ型を使用してきました:

* `int`
* `float`
* `str`
* `bool`

しかし、より複雑なデータ型を使用することもできます。

そして、今まで見てきたのと同じ機能を持つことになります:

* 素晴らしいエディタのサポート
* 受信したリクエストからのデータ変換
* レスポンスデータのデータ変換
* データの検証
* 自動注釈と文書化

## 他のデータ型

ここでは、使用できる追加のデータ型のいくつかを紹介します:

* `UUID`:
    * 多くのデータベースやシステムで共通のIDとして使用される、標準的な「ユニバーサルにユニークな識別子」です。
    * リクエストとレスポンスでは`str`として表現されます。
* `datetime.datetime`:
    * Pythonの`datetime.datetime`です。
    * リクエストとレスポンスはISO 8601形式の`str`で表現されます: `2008-09-15T15:53:00+05:00`
* `datetime.date`:
    * Pythonの`datetime.date`です。
    * リクエストとレスポンスはISO 8601形式の`str`で表現されます: `2008-09-15`
* `datetime.time`:
    * Pythonの`datetime.time`.
    * リクエストとレスポンスはISO 8601形式の`str`で表現されます: `14:23:55.003`
* `datetime.timedelta`:
    * Pythonの`datetime.timedelta`です。
    * リクエストとレスポンスでは合計秒数の`float`で表現されます。
    * Pydanticでは「ISO 8601 time diff encoding」として表現することも可能です。<a href="https://docs.pydantic.dev/latest/concepts/serialization/" class="external-link" target="_blank">詳細はドキュメントを参照してください</a>。
* `frozenset`:
    * リクエストとレスポンスでは`set`と同じように扱われます:
        * リクエストでは、リストが読み込まれ、重複を排除して`set`に変換されます。
        * レスポンスでは`set`が`list`に変換されます。
        * 生成されたスキーマは`set`の値が一意であることを指定します（JSON Schemaの`uniqueItems`を使用します）。
* `bytes`:
    * Pythonの標準的な`bytes`です。
    * リクエストとレスポンスでは`str`として扱われます。
    * 生成されたスキーマは`str`で`binary`の「フォーマット」持つことを指定します。
* `Decimal`:
    * Pythonの標準的な`Decimal`です。
    * リクエストやレスポンスでは`float`と同じように扱います。

* Pydanticの全ての有効な型はこちらで確認できます: <a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydantic data types</a>。
## 例

ここでは、上記の型のいくつかを使用したパラメータを持つ*path operation*の例を示します。

{* ../../docs_src/extra_data_types/tutorial001.py hl[1,2,12:16] *}

関数内のパラメータは自然なデータ型を持っていることに注意してください。そして、以下のように通常の日付操作を行うことができます:

{* ../../docs_src/extra_data_types/tutorial001.py hl[18,19] *}
