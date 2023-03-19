# パスパラメータと数値の検証

`Query`でクエリパラメータに対してバリデーションやメタデータを宣言できるのと同じように、`Path`を使うことでパスパラメータに対してもバリデーションやメタデータを宣言できます。

## Pathのインポート

まずは、`fastapi`から`Path`をインポートします。

=== "Python 3.6以上"

    ```Python hl_lines="3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "Python 3.10以上"

    ```Python hl_lines="1"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

## メタデータの宣言

`Query`と同じパラメータを全て宣言できます。

例えば、パスパラメータ`item_id`にメタデータ`title`を宣言するには、次のように入力します。

=== "Python 3.6以上"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "Python 3.10以上"

    ```Python hl_lines="8"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

!!! 情報
    パスパラメータは、パスの一部であるため常に必須です。

    必須であることを示すためには`...`を使って宣言する必要があります。

    しかし、仮に`None`で宣言したり、デフォルト値を設定していたりしても、何も影響はなく必須であることに変わりはありません。

## 必要に応じてパラメータを並べ替える

例えば、クエリパラメータ`q` を`str`型の必須パラメータとして宣言したいとします。
そして、そのパラメータにはその他の宣言は必要ないため`Query`は使いません。

一方で、パスパラメータ`item_id`に対しては`Path`を使う必要があるとします。（何らかの理由で`Annotated`を使用したくない場合でも同様です。）

Pythonでは、デフォルト値がないパラメータよりもデフォルト値があるパラメータが先にあるとエラーになります。

そのため、この場合はデフォルト値がないパラメータ(クエリパラメータ`q`)を先に書きます。

**FastAPI**は、パラメータの名前、型、デフォルトの宣言（`Query`、`Path`など）によりパラメータを検出しているため、順序は気にしません。

したがって、関数を次のように宣言することができます。

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## 必要に応じてパラメータを並べ替えるトリック

先程と同じように`Query`を使わずにデフォルト値のないクエリパラメータ`q`と、`Path`を使ったパスパラメータ`item_id`を宣言したいとします。
さらに、その順序を先程と変えたい場合は、Pythonの少し特殊な構文を使います。

関数の最初のパラメータとして`*`を渡します。

Pythonはその`*`を無視しますが、以降のすべてのパラメータは、キーワード引数（キーと値のペア）として呼び出されるようになります。これは<abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>としても知られています。デフォルト値がなくてもキーワード引数として呼び出されます。

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## 数値の検証: 大なりイコール
`Query`や`Path`(と後で出てくるその他の機能)では、数値の条件を指定することもできます。

この例では、`ge=1`が指定されているため`item_id`は1以上(`g`reater than or `e`qual)である必要があります。

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## 数値の検証: 大なり、小なりイコール

同じように指定できます:

* `gt`: より大きい(`g`reater `t`han)
* `le`: 以下(`l`ess than or `e`qual)

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## 数値の検証: 浮動小数の大なり小なり

数値の検証は、浮動小数点値(`float`)に対しても機能します。

ここで重要なのは、<abbr title="大なりイコール(greater than or equal)"><code>ge</code></abbr>だけでなく<abbr title="大なり(greater than)"><code>gt</code></abbr>も宣言できることです。
同じように、例えば`1`未満の値に対して値が`0`よりも大きいことを条件に指定できます。

したがって、この場合`0.5`は0よりも大きいため有効な値となり、`0.0`や`0`は無効な値になります。

<abbr title="小なり(less than)"><code>lt</code></abbr>でも同様です.

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## まとめ

`Query`や`Path`(と後で出てくるその他の機能)を使うと、メタデータや文字列の検証を[Query Parameters and String Validations](query-params-str-validations.md){.internal-link target=_blank}と同じ方法で宣言できます。

また、数値の検証も宣言できます。

* `gt`: 大なり(`g`reater `t`han)
* `ge`: 大なりイコール(`g`reater than or `e`qual)
* `lt`: 小なり(`l`ess `t`han)
* `le`: 小なりイコール(`l`ess than or `e`qual)

!!! 情報
    `Query`や`Path`、および後で出てくるその他機能は、共通クラス`Param`のサブクラスです。

    それらはすべて、追加の検証とメタデータのために同じパラメータを共有します。

!!! note "技術的な詳細"
    `Query`や`Path`などを`fastapi`からインポートする場合、実態は関数となっています。
    それらの関数は、呼び出されることで、同じ名前のクラスのインスタンスを返します。

    つまり、関数である`Query`をインポートして、それを呼び出すと`Query`という名前のクラスのインスタンスを返します。

    これらの関数は、クラスを直接使用することによって、エディタが型に関するエラーを表示しないようにするために用意されています。
    
    これによって、これらのエラーを無視するためのカスタム設定を追加することなく、通常のエディタやコーディングツールを使用することができます。
