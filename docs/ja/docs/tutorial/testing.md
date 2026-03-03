# テスト { #testing }

<a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a> のおかげで、**FastAPI** アプリケーションのテストは簡単で楽しいものになっています。

<a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> がベースで、さらにその設計は Requests をベースにしているため、とても馴染みがあり直感的です。

これを使用すると、**FastAPI** と共に <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> を直接利用できます。

## `TestClient` を使用 { #using-testclient }

/// info | 情報

`TestClient` を使用するには、まず <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a> をインストールします。

[仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成し、それを有効化してから、例えば以下のようにインストールしてください:

```console
$ pip install httpx
```

///

`TestClient` をインポートします。

`TestClient` を作成し、**FastAPI** に渡します。

`test_` から始まる名前の関数を作成します (これは `pytest` の標準的なコンベンションです)。

`httpx` と同じ様に `TestClient` オブジェクトを使用します。

チェックしたい Python の標準的な式と共に、シンプルに `assert` 文を記述します (これも `pytest` の標準です)。

{* ../../docs_src/app_testing/tutorial001_py310.py hl[2,12,15:18] *}

/// tip | 豆知識

テスト関数は `async def` ではなく、通常の `def` であることに注意してください。

また、クライアントへの呼び出しも通常の呼び出しであり、`await` を使用しません。

これにより、煩雑にならずに、`pytest` を直接使用できます。

///

/// note | 技術詳細

`from starlette.testclient import TestClient` も使用できます。

**FastAPI** は開発者の利便性のために `fastapi.testclient` と同じ `starlette.testclient` を提供します。しかし、実際にはStarletteから直接渡されています。

///

/// tip | 豆知識

FastAPIアプリケーションへのリクエストの送信とは別に、テストで `async` 関数 (非同期データベース関数など) を呼び出したい場合は、高度なチュートリアルの[Async Tests](../advanced/async-tests.md){.internal-link target=_blank} を参照してください。

///

## テストの分離 { #separating-tests }

実際のアプリケーションでは、おそらくテストを別のファイルに保存します。

また、**FastAPI** アプリケーションは、複数のファイル/モジュールなどで構成されている場合もあります。

### **FastAPI** アプリファイル { #fastapi-app-file }

[Bigger Applications](bigger-applications.md){.internal-link target=_blank} で説明されている、次のようなファイル構成があるとします:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

ファイル `main.py` に **FastAPI** アプリがあります:


{* ../../docs_src/app_testing/app_a_py310/main.py *}

### テストファイル { #testing-file }

次に、テストを含む `test_main.py` ファイルを用意できます。これは同じ Python パッケージ (`__init__.py` ファイルがある同じディレクトリ) に置けます:

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

このファイルは同じパッケージ内にあるため、相対インポートを使って `main` モジュール (`main.py`) からオブジェクト `app` をインポートできます:

{* ../../docs_src/app_testing/app_a_py310/test_main.py hl[3] *}


...そして、これまでと同じようにテストコードを書けます。

## テスト: 例の拡張 { #testing-extended-example }

次に、この例を拡張し、詳細を追加して、さまざまなパーツをテストする方法を確認しましょう。

### 拡張版 **FastAPI** アプリファイル { #extended-fastapi-app-file }

先ほどと同じファイル構成で続けます:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

ここで、**FastAPI** アプリがある `main.py` ファイルには、他の path operation があります。

エラーを返す可能性のある `GET` オペレーションがあります。

いくつかのエラーを返す可能性のある `POST` オペレーションもあります。

両方の *path operation* には `X-Token` ヘッダーが必要です。

{* ../../docs_src/app_testing/app_b_an_py310/main.py *}

### 拡張版テストファイル { #extended-testing-file }

次に、拡張版のテストで `test_main.py` を更新できます:

{* ../../docs_src/app_testing/app_b_an_py310/test_main.py *}


リクエストに情報を渡せるクライアントが必要で、その方法がわからない場合はいつでも、`httpx` での実現方法、あるいは HTTPX の設計が Requests の設計をベースにしているため `requests` での実現方法を検索 (Google) できます。

テストでも同じことを行います。

例えば:

* *パス* または *クエリ* パラメータを渡すには、それをURL自体に追加します。
* JSONボディを渡すには、Pythonオブジェクト (例: `dict`) を `json` パラメータに渡します。
* JSONの代わりに *フォームデータ* を送信する必要がある場合は、代わりに `data` パラメータを使用してください。
* *ヘッダー* を渡すには、`headers` パラメータに `dict` を渡します。
* *cookies* の場合、 `cookies` パラメータに `dict` です。

(`httpx` または `TestClient` を使用して) バックエンドにデータを渡す方法の詳細は、<a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPXのドキュメント</a>を確認してください。

/// info | 情報

`TestClient` は、Pydanticモデルではなく、JSONに変換できるデータを受け取ることに注意してください。

テストにPydanticモデルがあり、テスト中にそのデータをアプリケーションに送信したい場合は、[JSON互換エンコーダ](encoder.md){.internal-link target=_blank} で説明されている `jsonable_encoder` が利用できます。

///

## 実行 { #run-it }

その後、`pytest` をインストールするだけです。

[仮想環境](../virtual-environments.md){.internal-link target=_blank} を作成し、それを有効化してから、例えば以下のようにインストールしてください:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

ファイルとテストを自動的に検出し、実行して、結果のレポートを返します。

以下でテストを実行します:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
