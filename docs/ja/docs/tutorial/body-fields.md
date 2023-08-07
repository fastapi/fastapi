# ボディ - フィールド

 *パス操作関数*で`Query`、`Path` や`Body`を使って追加のバリデーションとメタデータを宣言した時と同じ方法で、Pydanticの `Field`を使って、Pydanticモデル内部に、バリデーションとメタデータを宣言することができます。

## Import `Field`

はじめに、インポートを行います:

=== "Python 3.10+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        可能であれば `Annotated` バージョンを使ってください。

    ```Python hl_lines="2"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        可能であれば `Annotated` バージョンを使ってください。

    ```Python hl_lines="4"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

!!! warning "注意"
     `Field` は `pydantic`から直接インポートされており、`Query`, `Path`, `Body`, etc などの他のものとは違い、`fastapi` からのインポートではありません。

## Declare model attributes

`Field`をモデル属性と共に使うことができるようになりました:

=== "Python 3.10+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="12-15"
    {!> ../../../docs_src/body_fields/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        可能であれば `Annotated` バージョンを使ってください。

    ```Python hl_lines="9-12"
    {!> ../../../docs_src/body_fields/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        可能であれば `Annotated` バージョンを使ってください。

    ```Python hl_lines="11-14"
    {!> ../../../docs_src/body_fields/tutorial001.py!}
    ```

`Field`は`Query`、`Path`、および`Body`と同じように機能し、すべてのパラメーターなどが同じです。

!!! note "備考"
    実は、`Query`、`Path`など、次に見る他の要素は、共通の`Param`クラスのサブクラスのオブジェクトを生成します。この`Param`クラス自体は、Pydanticの`FieldInfo`クラスのサブクラスです。

    そしてPydanticの`Field`は`FieldInfo`インスタンスも返します。

    `Body`はまた、`FieldInfo`のサブクラスのオブジェクトを直接返します。また、のちに見ることになる他のクラスも`Body`クラスのサブクラスです。

    `Query`や`Path`、`fastapi`から何かをインポートする際は、それらが実際は特別なクラスを返す関数であることを覚えていてください。

!!! tip "豆知識"
    各モデルの属性には、タイプ、デフォルト値、および`Field`が含まれており、*パス操作関数* のパラメータと同じ構造になっている事に注意してください。ただし、`Query`、`Body`の代わりに`Field`が使われます。



## 補足情報の追加
`Field`, `Query`, `Body`やその他の追加の情報を宣言すると、それらは生成されたJSONスキーマに含まれることになります。

サンプルの宣言を学習する際に、より詳しくドキュメント内での補足情報の追加について学ぶことができるでしょう。

!!! warning "注意"
    `Field` に渡された追加のキーは、アプリケーションのOpenAPIスキーマに表示されるでしょう。

    これらのキーが必ずしもOpenAPIの仕様の一部であるとは限らないので、[the OpenAPI validator](https://validator.swagger.io/)などの一部のOpenAPIツールでは、生成されたスキーマで動作しない場合があります。

## 要約

Pydanticの`Field`で、追加のバリデーションやメタデータをモデルの属性に付与することができます。

補足のキーワード引数を使うことで、追加のJSONスキーマをメタデータに渡すことができます。
