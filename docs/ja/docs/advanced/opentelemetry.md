# OpenTelemetry { #opentelemetry }

API が実行されているとき、どのくらいのトラフィックを受けているのか、どのリクエストが遅いのか、いつエラーが発生したのかを知りたい場合があります。

**テレメトリ**は、これらの疑問に答えるために役立つ、アプリケーションの動作に関するデータです。一般的な種類には次のものがあります。

- **メトリクス**: レスポンス時間や処理中のリクエスト数など、時間の経過に沿って集計できる測定値です。
- **トレース**: 個々のリクエストと、それを処理するために実行された操作の記録です。時間計測された各操作は **span** と呼ばれます。
- **ログ**: アプリケーションの起動や操作の失敗など、イベントのタイムスタンプ付き記録です。

[**OpenTelemetry**](https://opentelemetry.io/) は、テレメトリを収集して監視サービスへ送信するための標準とツールのセットです。監視サービスでは、ダッシュボードでそれらを確認できます。

**FastAPI はデフォルトで OpenTelemetry をサポートしています**。HTTP リクエストのトレース、メトリクス、ログに対応しています。WebSocket 接続でもトレースとログが提供されます。そのデータを確認するには、監視サービスが受信できるように設定してください。

## FastAPI のインストール { #install-fastapi }

テレメトリ送信用のパッケージを含む `standard` extras とともに FastAPI をインストールします。

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## アプリの作成 { #create-the-app }

`main.py` ファイルを作成します。

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

すべてがデフォルトで動作することに注目してください。テレメトリを動作させるためにカスタムコードを書く必要はありません。

## FastAPI Cloud { #fastapi-cloud }

`fastapi[standard]` を使って [FastAPI Cloud](https://fastapicloud.com) にデプロイすると、メトリクスは自動的に動作します。それ以外の設定は不要です。

Pro プランでは、[メトリクスダッシュボード](https://fastapicloud.com/docs/monitoring-and-performance/metrics/) でリクエスト数、エラー率、レスポンス時間を確認できます。

<img src="/img/tutorial/opentelemetry/image01.png" alt="サンプルデータを表示した FastAPI Cloud Pro のメトリクスダッシュボード">

## 他の監視サービス { #other-monitoring-services }

テレメトリを別の監視サービスへ送信するには、テレメトリ送信用の OpenTelemetry プロトコルである **OTLP** を受け付けるエンドポイントを設定します。サービスの HTTP/protobuf ベースエンドポイントを使用してください。

例の URL を自分のエンドポイントに置き換えて、以下の環境変数を設定します。

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME` は監視サービス内でアプリを識別します。エンドポイントはデータ受信用のベース URL です。その URL の下で、トレースは `/v1/traces` に、メトリクスは `/v1/metrics` に、ログは `/v1/logs` に送信されます。

サービスが認証を要求する場合は、指定されたヘッダーを `OTEL_EXPORTER_OTLP_HEADERS` に設定します。たとえば `api-key=YOUR_API_KEY` のようにします。

## アプリの実行 { #run-the-app }

同じターミナルでアプリを起動します。

<div class="termy">

```console
$ uv run fastapi run
```

</div>

別のターミナルでリクエストを送信します。

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

監視サービスを開いて `my-api` を探します。次回のエクスポート後に、`GET /items/{item_id}` span を含むトレースと、リクエスト数、レスポンス時間、アクティブなリクエストのメトリクスを確認できます。

## テレメトリのカスタマイズ { #customize-telemetry }

### プロバイダーとエクスポーターの設定 { #configure-providers-and-exporters }

**プロバイダー**は、トレース、メトリクス、ログを記録するオブジェクトを提供します。その設定により、データがどのように処理され、エクスポートされるかが制御されます。

テレメトリライブラリは、OpenTelemetry のグローバルプロバイダーを設定できます。アプリの起動前にライブラリを設定すると、FastAPI はそれらのプロバイダーを自動的に使用します。

環境で OTLP エンドポイントが設定されている場合、FastAPI は有効な各プロバイダーに対して、その宛先用のエクスポーターを追加します。既存のエクスポーターは引き続き各宛先へデータを送信します。

各宛先は一度だけ設定してください。別のライブラリがすでに環境の宛先を処理している場合は、その環境エクスポートを無効にするか、FastAPI の自動設定をオフにします。

```python
app = FastAPI(telemetry={"auto_configure": False})
```

`telemetry` 辞書にプロバイダーを直接渡すこともできます。たとえば、このプロバイダーは OpenTelemetry のコンソールエクスポーターを使って、リクエスト span をターミナルに出力します。

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**エクスポーター**は span を宛先へ送信します。`BatchSpanProcessor` は span をまとめてバックグラウンドで送信します。その宛先を使用するには、コンソールエクスポーターを監視ライブラリが提供するものに置き換えてください。その他の設定オプションについては、[OpenTelemetry の Python instrumentation ガイド](https://opentelemetry.io/docs/languages/python/instrumentation/)を参照してください。

同じ辞書で `meter_provider` または `logger_provider` を使用して、メトリクスまたはログのプロバイダーを提供できます。プロバイダーを作成したアプリケーションまたはライブラリが、その shutdown を管理します。FastAPI は追加したエクスポートコンポーネントを管理します。

/// warning | 注意

OpenTelemetry はデフォルトでグローバルプロバイダーを使用します。[マウントされたサブアプリケーション](sub-applications.md)ごとの独立したテレメトリ設定は保証されません。

///

### リクエスト操作のトレース { #trace-request-operations }

デフォルトでは、リクエストトレースには、依存関係の解決、path operation 関数の実行、レスポンスのシリアライズ、FastAPI の `BackgroundTasks` 内の各タスク実行の span が含まれます。これらの span は同じプロバイダーとエクスポーターを使用します。

バックグラウンドタスクの span は、リクエストのトレースの一部として残ります。これらは HTTP レスポンス span の終了後に実行されるため、測定されるレスポンス時間は増加しません。

HTTP リクエスト span のみを記録するには、`operation_spans` を `False` に設定します。

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket 接続のトレース { #trace-websocket-connections }

各 WebSocket 接続には、`WS /ws/{room}` のような span があり、ハンドラーと依存関係のクリーンアップを対象にします。依存関係の解決とエンドポイント実行に関する `operation_spans` を含め、同じプロバイダーと設定を使用します。

HTTP リクエストメトリクスは HTTP リクエストのみを対象にします。コード `1000` または `1001` による通常の WebSocket 切断では、エラーログは生成されません。

### エラーの確認 { #inspect-errors }

FastAPI は未処理の例外を OpenTelemetry ログとして記録し、リクエストまたは接続のトレースに関連付けます。エラーログは、トレースがサンプリングされていない場合でも記録されます。

例外ログには、例外の型、メッセージ、スタックトレースが含まれます。メッセージやスタックトレースには機密情報が含まれる可能性があります。プロバイダーのログプロセッサを使用してフィルターまたはマスクするか、`logs` を `False` に設定してこれらのログを無効にしてください。

FastAPI はリクエストのバリデーション失敗も、ルートとエラー数を含む warning ログとして記録します。これらのログには不正な入力は含まれません。

## 記録する内容の選択 { #choose-what-to-record }

`telemetry` 辞書は、次の設定も受け付けます。

| 設定 | 目的 | デフォルト |
| --- | --- | --- |
| `tracing` | HTTP リクエストと WebSocket 接続の span を記録します | `True` |
| `metrics` | HTTP リクエストメトリクスを記録します | `True` |
| `logs` | バリデーション失敗と未処理の例外を記録します | `True` |
| `operation_spans` | リクエスト操作の span を追加します | `True` |
| `exclude` | ASGI scope を受け取る関数が `True` を返した場合にリクエストをスキップします | `None` |
| `auto_configure` | 環境変数で設定されたエンドポイント用のエクスポーターを追加します | `True` |

たとえば、ヘルスチェックを除外しつつメトリクスを収集するには、次のようにします。

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

アプリケーションが lifespan 関数内などでプロバイダーの設定を自分で処理する場合は、`auto_configure` を `False` に設定します。
