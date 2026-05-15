# レスポンスを直接返す { #return-a-response-directly }

**FastAPI** の *path operation* では、通常は任意のデータを返すことができます: 例えば、`dict`、`list`、Pydanticモデル、データベースモデルなどです。

[レスポンスモデル](../tutorial/response-model.md) を宣言した場合、FastAPI は Pydantic を使ってデータをJSONにシリアライズします。

レスポンスモデルを宣言しない場合、FastAPI は [JSON互換エンコーダ](../tutorial/encoder.md) で説明されている `jsonable_encoder` を使用し、その結果を `JSONResponse` に入れます。

また、`JSONResponse` を直接作成して返すこともできます。

/// tip

通常は、`JSONResponse` を直接返すよりも、[レスポンスモデル](../tutorial/response-model.md) を使うほうがパフォーマンスが大幅に良くなります。これは、Pydantic によるシリアライズが Rust で実行されるためです。

///

## `Response` を返す { #return-a-response }

実際は、`Response` やそのサブクラスを返すことができます。

/// info

`JSONResponse` それ自体は、`Response` のサブクラスです。

///

`Response` を返した場合は、**FastAPI** は直接それを返します。

それは、Pydanticモデルのデータ変換や、コンテンツを任意の型に変換したりなどはしません。

これは多くの柔軟性を提供します。任意のデータ型を返したり、任意のデータ宣言やバリデーションをオーバーライドできます。

同時に多くの責任も伴います。返すデータが正しく、正しいフォーマットであり、シリアライズ可能であることなどを、あなたが保証しなければなりません。

## `jsonable_encoder` を `Response` の中で使う { #using-the-jsonable-encoder-in-a-response }

**FastAPI** はあなたが返す `Response` に対して何も変更を加えないので、コンテンツが準備できていることを保証しなければなりません。

例えば、Pydanticモデルを `JSONResponse` に含めるには、すべてのデータ型 (`datetime` や `UUID` など) をJSON互換の型に変換された `dict` に変換しなければなりません。

このようなケースでは、レスポンスにデータを含める前に `jsonable_encoder` を使ってデータを変換できます。

{* ../../docs_src/response_directly/tutorial001_py310.py hl[5:6,20:21] *}

/// note | 技術詳細

また、`from starlette.responses import JSONResponse` も利用できます。

**FastAPI** は開発者の利便性のために `fastapi.responses` という `starlette.responses` と同じものを提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。

///

## カスタム `Response` を返す { #returning-a-custom-response }

上記の例では必要な部分を全て示していますが、あまり便利ではありません。`item` を直接返すことができるし、**FastAPI** はそれを `dict` に変換して `JSONResponse` に含めてくれるなど。すべて、デフォルトの動作です。

では、これを使ってカスタムレスポンスをどう返すか見てみましょう。

[XML](https://en.wikipedia.org/wiki/XML)レスポンスを返したいとしましょう。

XMLを文字列にし、`Response` に含め、それを返します。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

## Response Model の仕組み { #how-a-response-model-works }

path operation で [Response Model - 戻り値の型](../tutorial/response-model.md) を宣言すると、**FastAPI** はそれを使って Pydantic によりデータをJSONにシリアライズします。

{* ../../docs_src/response_model/tutorial001_01_py310.py hl[16,21] *}

これは Rust 側で行われるため、通常の Python と `JSONResponse` クラスで行う場合より、パフォーマンスははるかに良くなります。

`response_model` や戻り値の型を使用する場合、FastAPI はデータ変換に（低速になりうる）`jsonable_encoder` も `JSONResponse` クラスも使いません。

代わりに、response model（または戻り値の型）を使って Pydantic が生成した JSON のバイト列をそのまま用い、JSON 用の正しいメディアタイプ（`application/json`）を持つ `Response` を直接返します。

## 備考 { #notes }

`Response` を直接返す場合、バリデーションや、変換 (シリアライズ) や、自動ドキュメントは行われません。

しかし、[Additional Responses in OpenAPI](additional-responses.md)に記載されたようにドキュメントを書くこともできます。

後のセクションで、カスタム `Response` を使用・宣言しながら、自動的なデータ変換やドキュメンテーションを行う方法を説明します。
