# バックグラウンドタスク { #background-tasks }

レスポンスを返した *後に* 実行されるバックグラウンドタスクを定義できます。

これは、リクエスト後に処理を開始する必要があるが、クライアントがレスポンスを受け取る前に処理を終える必要のない操作に役立ちます。

これには、たとえば次のものが含まれます。

* 作業実行後のメール通知:
    * メールサーバーへの接続とメールの送信は「遅い」(数秒) 傾向があるため、すぐにレスポンスを返し、バックグラウンドでメール通知ができます。
* データ処理:
    * たとえば、時間のかかる処理を必要とするファイル受信時には、「Accepted」(HTTP 202) のレスポンスを返し、バックグラウンドで処理できます。

## `BackgroundTasks` の使用 { #using-backgroundtasks }

まず初めに、`BackgroundTasks` をインポートし、`BackgroundTasks` の型宣言と共に、*path operation function* のパラメーターを定義します:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** は、`BackgroundTasks` 型のオブジェクトを作成し、そのパラメーターに渡します。

## タスク関数の作成 { #create-a-task-function }

バックグラウンドタスクとして実行される関数を作成します。

これは、パラメーターを受け取ることができる単なる標準的な関数です。

これは `async def` または通常の `def` 関数であり、**FastAPI** はこれを正しく処理します。

ここで、タスク関数はファイル書き込みを実行します (メール送信のシミュレーション)。

また、書き込み操作では `async` と `await` を使用しないため、通常の `def` で関数を定義します。

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## バックグラウンドタスクの追加 { #add-the-background-task }

*path operation function* 内で、`.add_task()` メソッドを使用してタスク関数を *background tasks* オブジェクトに渡します。

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` は以下の引数を受け取ります:

* バックグラウンドで実行されるタスク関数 (`write_notification`)。
* タスク関数に順番に渡す必要のある引数の列 (`email`)。
* タスク関数に渡す必要のあるキーワード引数 (`message="some notification"`)。

## 依存性注入 { #dependency-injection }

`BackgroundTasks` の使用は依存性注入システムでも機能し、様々な階層 (*path operation function*、依存性 (dependable)、サブ依存性など) で `BackgroundTasks` 型のパラメーターを宣言できます。

**FastAPI** は、それぞれの場合の処理​​方法と同じオブジェクトの再利用方法を知っているため、すべてのバックグラウンドタスクがマージされ、バックグラウンドで後で実行されます:


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


この例では、レスポンスが送信された *後* にメッセージが `log.txt` ファイルに書き込まれます。

リクエストにクエリがあった場合、バックグラウンドタスクでログに書き込まれます。

そして、*path operation function* で生成された別のバックグラウンドタスクは、`email` パスパラメータを使用してメッセージを書き込みます。

## 技術的な詳細 { #technical-details }

`BackgroundTasks` クラスは、<a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>から直接取得されます。

これは、FastAPI に直接インポート/インクルードされるため、`fastapi` からインポートできる上に、`starlette.background`から別の `BackgroundTask` (末尾に `s` がない) を誤ってインポートすることを回避できます。

`BackgroundTasks`のみを使用することで (`BackgroundTask` ではなく)、`Request` オブジェクトを直接使用する場合と同様に、それを *path operation function* パラメーターとして使用し、**FastAPI** に残りの処理を任せることができます。

それでも、FastAPI で `BackgroundTask` を単独で使用することは可能ですが、コード内でオブジェクトを作成し、それを含むStarlette `Response` を返す必要があります。

詳細については、<a href="https://www.starlette.dev/background/" class="external-link" target="_blank">Starlette のバックグラウンドタスクに関する公式ドキュメント</a>を参照して下さい。

## 注意 { #caveat }

大量のバックグラウンド計算が必要であり、必ずしも同じプロセスで実行する必要がない場合 (たとえば、メモリや変数などを共有する必要がない場合)、<a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a> のようなより大きな他のツールを使用するとメリットがあるかもしれません。

これらは、より複雑な構成、RabbitMQ や Redis などのメッセージ/ジョブキューマネージャーを必要とする傾向がありますが、複数のプロセス、特に複数のサーバーでバックグラウンドタスクを実行できます。

ただし、同じ **FastAPI** アプリから変数とオブジェクトにアクセスする必要がある場合、または小さなバックグラウンドタスク (電子メール通知の送信など) を実行する必要がある場合は、単に `BackgroundTasks` を使用できます。

## まとめ { #recap }

*path operation functions* と依存性のパラメータで `BackgroundTasks`をインポートして使用し、バックグラウンドタスクを追加して下さい。
