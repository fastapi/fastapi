# ボディ - フィールド

`Query`や`Path`、`Body`を使って *path operation関数* のパラメータに追加のバリデーションやメタデータを宣言するのと同じように、Pydanticの`Field`を使ってPydanticモデルの内部でバリデーションやメタデータを宣言することができます。

## `Field`のインポート

まず、以下のようにインポートします:

```Python hl_lines="4"
{!../../../docs_src/body_fields/tutorial001.py!}
```

!!! warning "注意"
    `Field`は他の全てのもの（`Query`、`Path`、`Body`など）とは違い、`fastapi`からではなく、`pydantic`から直接インポートされていることに注意してください。

## モデルの属性の宣言

以下のように`Field`をモデルの属性として使用することができます:

```Python hl_lines="11 12 13 14"
{!../../../docs_src/body_fields/tutorial001.py!}
```

`Field`は`Query`や`Path`、`Body`と同じように動作し、全く同様のパラメータなどを持ちます。

!!! note "技術詳細"
    実際には次に見る`Query`や`Path`などは、共通の`Param`クラスのサブクラスのオブジェクトを作成しますが、それ自体はPydanticの`FieldInfo`クラスのサブクラスです。

    また、Pydanticの`Field`は`FieldInfo`のインスタンスも返します。

    `Body`は`FieldInfo`のサブクラスのオブジェクトを直接返すこともできます。そして、他にも`Body`クラスのサブクラスであるものがあります。

    `fastapi`から`Query`や`Path`などをインポートする場合、これらは実際には特殊なクラスを返す関数であることに注意してください。

!!! tip "豆知識"
    型、デフォルト値、`Field`を持つ各モデルの属性が、`Path`や`Query`、`Body`の代わりに`Field`を持つ、*path operation 関数の*パラメータと同じ構造になっていることに注目してください。

## 追加情報の追加

追加情報は`Field`や`Query`、`Body`などで宣言することができます。そしてそれは生成されたJSONスキーマに含まれます。

後に例を用いて宣言を学ぶ際に、追加情報を句悪方法を学べます。

## まとめ

Pydanticの`Field`を使用して、モデルの属性に追加のバリデーションやメタデータを宣言することができます。

追加のキーワード引数を使用して、追加のJSONスキーマのメタデータを渡すこともできます。
