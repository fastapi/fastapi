# 非同期テスト { #async-tests }

これまでに、提供されている `TestClient` を使って **FastAPI** アプリケーションをテストする方法を見てきました。ここまでは、`async` 関数を使わない同期テストのみでした。

テストで非同期関数を使えると、たとえばデータベースへ非同期にクエリする場合などに便利です。非同期データベースライブラリを使いながら、FastAPI アプリにリクエストを送り、その後バックエンドが正しいデータをデータベースに書き込めたかを検証したい、といったケースを想像してください。

その方法を見ていきます。

## pytest.mark.anyio { #pytest-mark-anyio }

テスト内で非同期関数を呼び出したい場合、テスト関数自体も非同期である必要があります。AnyIO はこれを実現するための便利なプラグインを提供しており、特定のテスト関数を非同期で呼び出すことを指定できます。

## HTTPX { #httpx }

**FastAPI** アプリケーションが通常の `def` 関数を使っていても、その内側は依然として `async` アプリケーションです。

`TestClient` は、標準の pytest を使って通常の `def` のテスト関数から非同期の FastAPI アプリを呼び出すための「おまじない」を内部で行います。しかし、その「おまじない」はテスト関数自体が非同期の場合には機能しません。テストを非同期で実行すると、テスト関数内で `TestClient` は使えなくなります。

`TestClient` は <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> を基に作られており、幸いなことに API のテストには HTTPX を直接利用できます。

## 例 { #example }

簡単な例として、[大きなアプリケーション](../tutorial/bigger-applications.md){.internal-link target=_blank} と [テスト](../tutorial/testing.md){.internal-link target=_blank} で説明したものに似たファイル構成を考えます:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

`main.py` は次のようになります:

{* ../../docs_src/async_tests/app_a_py310/main.py *}

`test_main.py` は `main.py` のテストを持ち、次のようになります:

{* ../../docs_src/async_tests/app_a_py310/test_main.py *}

## 実行 { #run-it }

テストはいつも通り次で実行できます:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 詳細 { #in-detail }

マーカー `@pytest.mark.anyio` は、このテスト関数を非同期で呼び出すべきであることを pytest に伝えます:

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip | 豆知識

`TestClient` を使っていたときと異なり、テスト関数は `def` ではなく `async def` になっている点に注意してください。

///

次に、アプリを渡して `AsyncClient` を作成し、`await` を使って非同期リクエストを送信できます。

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

これは次と同等です:

```Python
response = client.get('/')
```

...これまでは `TestClient` でリクエストを送っていました。

/// tip | 豆知識

新しい `AsyncClient` では async/await を使っている点に注意してください。リクエストは非同期です。

///

/// warning | 注意

アプリケーションが lifespan イベントに依存している場合、`AsyncClient` はそれらのイベントをトリガーしません。確実にトリガーするには、<a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a> の `LifespanManager` を使用してください。

///

## その他の非同期関数呼び出し { #other-asynchronous-function-calls }

テスト関数が非同期になったので、FastAPI アプリへのリクエスト送信以外の `async` 関数も、コードの他の場所と同様に呼び出して（`await` して）使えます。

/// tip | 豆知識

テストに非同期関数呼び出しを統合した際に（例: <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB の MotorClient</a> 使用時）、`RuntimeError: Task attached to a different loop` に遭遇した場合は、イベントループを必要とするオブジェクトは非同期関数内でのみインスタンス化するようにしてください。例えば `@app.on_event("startup")` コールバック内で行います。

///
