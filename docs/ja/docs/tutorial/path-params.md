# パスパラメータ { #path-parameters }

Pythonのformat文字列と同様のシンタックスで「パスパラメータ」や「パス変数」を宣言できます:

{* ../../docs_src/path_params/tutorial001_py310.py hl[6:7] *}

パスパラメータ `item_id` の値は、引数 `item_id` として関数に渡されます。

したがって、この例を実行して <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> にアクセスすると、次のレスポンスが表示されます。

```JSON
{"item_id":"foo"}
```

## 型付きパスパラメータ { #path-parameters-with-types }

標準のPythonの型アノテーションを使用して、関数内のパスパラメータの型を宣言できます:

{* ../../docs_src/path_params/tutorial002_py310.py hl[7] *}

ここでは、 `item_id` は `int` として宣言されています。

/// check | 確認

これにより、関数内でのエディターサポート (エラーチェックや補完など) が提供されます。

///

## データ<dfn title="別名: シリアライズ、パース、マーシャリング">変換</dfn> { #data-conversion }

この例を実行し、ブラウザで <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a> を開くと、次のレスポンスが表示されます:

```JSON
{"item_id":3}
```

/// check | 確認

関数が受け取った（および返した）値は、文字列の `"3"` ではなく、Pythonの `int` としての `3` であることに注意してください。

したがって、その型宣言を使うと、**FastAPI**は自動リクエスト <dfn title="HTTPリクエストから受け取った文字列をPythonのデータに変換する">"解析"</dfn> を行います。

///

## データバリデーション { #data-validation }

しかしブラウザで <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a> を開くと、次のHTTPエラーが表示されます:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

これは、パスパラメータ `item_id` が `int` ではない値 `"foo"` だからです。

<a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a> で見られるように、`int` のかわりに `float` が与えられた場合にも同様なエラーが表示されます。

/// check | 確認

したがって、同じPythonの型宣言を使用することで、**FastAPI**はデータのバリデーションを行います。

表示されたエラーには、バリデーションが通らなかった箇所が明確に示されていることに注意してください。

これは、APIとやり取りするコードを開発・デバッグする際に非常に役立ちます。

///

## ドキュメント { #documentation }

そしてブラウザで <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> を開くと、以下の様な自動的に生成された対話的なAPIドキュメントが表示されます。

<img src="/img/tutorial/path-params/image01.png">

/// check | 確認

繰り返しになりますが、同じPython型宣言を使用するだけで、**FastAPI**は対話的なドキュメントを自動的に生成します（Swagger UIを統合）。

パスパラメータが整数として宣言されていることに注意してください。

///

## 標準ベースのメリット、ドキュメンテーションの代替物 { #standards-based-benefits-alternative-documentation }

また、生成されたスキーマが <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a> 標準に従っているので、互換性のあるツールが多数あります。

このため、**FastAPI**自体が代替のAPIドキュメントを提供します（ReDocを使用）。これは、 <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> にアクセスすると確認できます。

<img src="/img/tutorial/path-params/image02.png">

同様に、互換性のあるツールが多数あります。多くの言語用のコード生成ツールを含みます。

## Pydantic { #pydantic }

すべてのデータバリデーションは <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> によって内部で実行されるため、Pydanticの全てのメリットが得られます。そして、安心して利用することができます。

`str`、 `float` 、 `bool` および他の多くの複雑なデータ型を型宣言に使用できます。

これらのいくつかについては、チュートリアルの次の章で説明します。

## 順序の問題 { #order-matters }

*path operations* を作成する際、固定パスをもつ状況があり得ます。

`/users/me` から、現在のユーザに関するデータを取得するとします。

さらに、ユーザIDによって特定のユーザに関する情報を取得するパス  `/users/{user_id}` ももつことができます。

*path operations* は順に評価されるので、 `/users/me` が `/users/{user_id}` よりも先に宣言されているか確認する必要があります:

{* ../../docs_src/path_params/tutorial003_py310.py hl[6,11] *}

それ以外の場合、 `/users/{user_id}` は `/users/me` としてもマッチします。値が `"me"` であるパラメータ `user_id` を受け取ると「考え」ます。

同様に、path operation を再定義することはできません:

{* ../../docs_src/path_params/tutorial003b_py310.py hl[6,11] *}

パスは最初にマッチしたものが常に使われるため、最初のものが常に使用されます。

## 定義済みの値 { #predefined-values }

*パスパラメータ*を受け取る *path operation* をもち、有効な*パスパラメータ*の値を事前に定義したい場合は、標準のPython <abbr title="Enumeration - 列挙型">`Enum`</abbr> を利用できます。

### `Enum` クラスの作成 { #create-an-enum-class }

`Enum` をインポートし、 `str` と `Enum` を継承したサブクラスを作成します。

`str` を継承することで、APIドキュメントは値が `string` 型でなければいけないことを知り、正確にレンダリングできるようになります。

そして、固定値のクラス属性を作ります。すると、その値が使用可能な値となります:

{* ../../docs_src/path_params/tutorial005_py310.py hl[1,6:9] *}

/// tip | 豆知識

"AlexNet"、"ResNet"そして"LeNet"は機械学習<dfn title="厳密には、Deep Learning のモデルアーキテクチャ">モデル</dfn>の名前です。

///

### *パスパラメータ*の宣言 { #declare-a-path-parameter }

次に、作成したenumクラスである`ModelName`を使用した型アノテーションをもつ*パスパラメータ*を作成します:

{* ../../docs_src/path_params/tutorial005_py310.py hl[16] *}

### ドキュメントの確認 { #check-the-docs }

*パスパラメータ*の利用可能な値が事前に定義されているので、対話的なドキュメントで適切に表示できます:

<img src="/img/tutorial/path-params/image03.png">

### Python*列挙型*の利用 { #working-with-python-enumerations }

*パスパラメータ*の値は*列挙型メンバ*となります。

#### *列挙型メンバ*の比較 { #compare-enumeration-members }

これは、作成した列挙型 `ModelName` の*列挙型メンバ*と比較できます:

{* ../../docs_src/path_params/tutorial005_py310.py hl[17] *}

#### *列挙値*の取得 { #get-the-enumeration-value }

`model_name.value` 、もしくは一般に、 `your_enum_member.value` を使用して実際の値 (この場合は `str`) を取得できます。

{* ../../docs_src/path_params/tutorial005_py310.py hl[20] *}

/// tip | 豆知識

`ModelName.lenet.value` でも `"lenet"` 値にアクセスできます。

///

#### *列挙型メンバ*の返却 { #return-enumeration-members }

*path operation* から*列挙型メンバ*を返すことができます。JSONボディ（例: `dict`）でネストすることもできます。

それらはクライアントに返される前に適切な値 (この場合は文字列) に変換されます。

{* ../../docs_src/path_params/tutorial005_py310.py hl[18,21,23] *}

クライアントは以下の様なJSONレスポンスを得ます:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## パスを含んだパスパラメータ { #path-parameters-containing-paths }

パス `/files/{file_path}` となる *path operation* を持っているとしましょう。

ただし、 `home/johndoe/myfile.txt` のような*パス*を含んだ `file_path` が必要です。

したがって、そのファイルのURLは `/files/home/johndoe/myfile.txt` の様になります。

### OpenAPIサポート { #openapi-support }

OpenAPIはテストや定義が困難なシナリオにつながる可能性があるため、内部に*パス*を含む*パスパラメータ*の宣言をサポートしていません。

それにも関わらず、Starletteの内部ツールのひとつを使用することで、**FastAPI**はそれが実現できます。

そして、パラメータがパスを含むべきであることを示すドキュメントを追加しなくても、ドキュメントは動作します。

### パスコンバーター { #path-convertor }

Starletteのオプションを直接使用することで、以下のURLの様な*パス*を含んだ、*パスパラメータ*の宣言ができます:

```
/files/{file_path:path}
```

この場合、パラメータ名は `file_path` です。そして、最後の部分 `:path` はパラメータがいかなる*パス*にもマッチすることを示します。

したがって、以下の様に使用できます:

{* ../../docs_src/path_params/tutorial004_py310.py hl[6] *}

/// tip | 豆知識

最初のスラッシュ (`/`)が付いている `/home/johndoe/myfile.txt` をパラメータが含んでいる必要があるかもしれません。

この場合、URLは `files` と `home` の間にダブルスラッシュ (`//`) のある、 `/files//home/johndoe/myfile.txt` になります。

///

## まとめ { #recap }

簡潔で、本質的で、標準的なPythonの型宣言を使用することで、**FastAPI**は以下を行います:

* エディターサポート: エラーチェック、自動補完、など
* データ「<dfn title="HTTPリクエストから受け取った文字列をPythonのデータに変換する">解析</dfn>」
* データバリデーション
* APIアノテーションと自動ドキュメント生成

そしてこれはたった一度宣言するだけです。

これは恐らく、(パフォーマンスを除いて) 他のフレームワークと比較したときの、**FastAPI**の主な目に見える利点です。
