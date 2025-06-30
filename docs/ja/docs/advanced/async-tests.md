# 非同期テスト

前の章では`TestClient` を使ってFastAPIアプリをテストする方法を見てきたと思いますが、これまでは `async` を使わない同期的なテストのみでした。

しかし、テストで非同期関数を使えると便利なケースがあります。
たとえば、データベースに非同期でクエリする場合を考えてみましょう。
FastAPIアプリにリクエストを送り、非同期データベースライブラリを使って正しくデータが保存されたか確認したいときがあるかと思います。

さっそくですが、これを実現する方法を見ていきましょう。

## pytest.mark.anyio

テストで非同期関数を呼び出したい場合、テスト関数自体も非同期である必要があります。
AnyIO はそのための便利なプラグインを提供しており、特定のテスト関数を非同期で実行できるようにします。

## HTTPX

FastAPIアプリケーションが`async def`ではなく通常の`def`関数を使用していても、内部的には非同期アプリケーションのままです。

`TestClient` は、標準の pytest を使用して通常の `def` テスト関数内で非同期 FastAPI アプリケーションを呼び出すために内部でマジックをしてくれますが、非同期関数内で使用する場合は、このマジックはもはや機能しません。 

`TestClient` は <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> をベースとしており、幸い、これを直接使用して API をテストできます。

## 例

簡単な例として、[Bigger Applications](../tutorial/bigger-applications.md){.internal-link target=_blank} および [Testing](../ja/tutorial/testing.md){.internal-link target=_blank} で説明されているのと似たファイル構成で考えてみましょう。

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

ファイル `main.py` には以下の内容が含まれます：

{* ../../docs_src/async_tests/main.py *}

ファイル `test_main.py` には `main.py` のテストが含まれ、現在は次のようになっています：

{* ../../docs_src/async_tests/test_main.py *}

## 実行方法

通常通り、以下のようにテストを実行できます：

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## 詳細

マーカー @pytest.mark.anyio は、このテスト関数を非同期で実行するよう pytest に指示します：

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip | 豆知識

テスト関数が、以前の TestClient 使用時の通常の `def` ではなく、`async def` で定義されていることに注意してください。

///

次に、アプリケーションとともに `AsyncClient` を作成し、`await` を使って非同期にリクエストを送信できます。

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

上記のコードは、次のようなコードと同等です：

```Python
response = client.get('/')
```

/// tip | 豆知識

新しい AsyncClient では async/await を使用していることに注意してください。リクエストは非同期で行われています。

///

/// warning | 注意

もしアプリケーションが Lifespan イベントに依存している場合、AsyncClient はこれらのイベントをトリガーしません。
イベントを確実に発火させるには、`LifespanManager` の <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>を使用してください。

///

## その他の非同期関数の呼び出し

テスト関数が非同期になったことで、FastAPIアプリへのリクエスト送信以外にも、テスト内で他の非同期関数を呼び出し（`await`）できるようになりました。これはコードの他の部分で非同期関数を呼び出すのと全く同じです。

/// tip | 豆知識

テストで非同期関数呼び出しを統合する際に `RuntimeError: Task attached to a different loop` に遭遇した場合（例：<a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MongoDB の MotorClient</a> を使用する場合）、イベントループが必要なオブジェクトは非同期関数内でのみインスタンス化する必要があることに注意してください。 例として、`@app.on_event("startup")` コールバック内でのインスタンス化が推奨されます。

///
