# OpenTelemetry { #opentelemetry }

APIを実行しているとき、受信するトラフィックの量、遅いリクエスト、エラーが発生するタイミングを把握したくなることがあります。

**テレメトリー**は、こうした疑問に答えるためのアプリケーションの動作に関するデータです。一般的には、次の種類があります:

- **メトリクス**: レスポンス時間や処理中のリクエスト数など、時間の経過に沿って集計できる測定値です。
- **トレース**: 個々のリクエストと、それを処理するために実行された操作の記録です。時間を計測する各操作を**スパン**と呼びます。
- **ログ**: アプリケーションの起動や操作の失敗など、イベントのタイムスタンプ付きの記録です。

[**OpenTelemetry**](https://opentelemetry.io/)は、テレメトリーを収集して監視サービスに送信するための標準とツールのセットです。監視サービスのダッシュボードで、そのデータを確認できます。

**FastAPIはデフォルトでOpenTelemetryをサポートしており**、HTTPリクエストのトレース、メトリクス、ログを提供します。WebSocket接続でもトレースとログを提供します。このデータを確認するには、受信する監視サービスを設定してください。

## FastAPIのインストール { #install-fastapi }

テレメトリーを送信するためのパッケージを含む`standard`オプションを指定してFastAPIをインストールします:

<div class="termy">

```console
$ uv add "fastapi[standard]"
---> 100%
```

</div>

## アプリの作成 { #create-the-app }

`main.py`ファイルを作成します:

{* ../../docs_src/opentelemetry/tutorial001_py310.py *}

すべてデフォルトで動作するため、テレメトリーを有効にするための独自のコードを書く必要はありません。

## FastAPI Cloud { #fastapi-cloud }

`fastapi[standard]`を使用して[FastAPI Cloud](https://fastapicloud.com)にデプロイすると、メトリクスは自動的に機能します。追加の設定は不要です。

Proプランでは、[メトリクスダッシュボード](https://fastapicloud.com/docs/monitoring-and-performance/metrics/)でリクエスト数、エラー率、レスポンス時間を確認できます。

<img src="/img/tutorial/opentelemetry/image01.png" alt="サンプルデータを表示したFastAPI Cloud Proのメトリクスダッシュボード">

## その他の監視サービス { #other-monitoring-services }

別の監視サービスにテレメトリーを送信するには、テレメトリー送信用のOpenTelemetryプロトコルである**OTLP**を受け付けるエンドポイントを設定します。サービスのHTTP/protobufベースエンドポイントを使用してください。

例のURLを自分のエンドポイントに置き換えて、次の環境変数を設定します:

```bash
export OTEL_SERVICE_NAME=my-api
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.example.com
```

`OTEL_SERVICE_NAME`は、監視サービス内でアプリを識別するための名前です。エンドポイントはデータを受信するためのベースURLです。そのURL配下の`/v1/traces`にトレース、`/v1/metrics`にメトリクス、`/v1/logs`にログが送信されます。

サービスで認証が必要な場合は、`OTEL_EXPORTER_OTLP_HEADERS`にサービスが指定するヘッダー（例: `api-key=YOUR_API_KEY`）を設定してください。

## アプリの実行 { #run-the-app }

同じターミナルでアプリを起動します:

<div class="termy">

```console
$ uv run fastapi run
```

</div>

別のターミナルでリクエストを送信します:

```console
$ curl http://127.0.0.1:8000/items/1
{"item_id":1}
```

監視サービスを開き、`my-api`を探します。次のエクスポート後に、`GET /items/{item_id}`スパンを含むトレースと、リクエスト数、レスポンス時間、処理中のリクエスト数のメトリクスを確認できます。

## テレメトリーのカスタマイズ { #customize-telemetry }

### プロバイダーとエクスポーターの設定 { #configure-providers-and-exporters }

**プロバイダー**は、トレース、メトリクス、ログを記録するオブジェクトを提供します。その設定によって、データの処理方法とエクスポート方法を制御します。

テレメトリーライブラリは、OpenTelemetryのグローバルプロバイダーを設定できます。アプリの起動前にライブラリを設定すると、FastAPIはそれらのプロバイダーを自動的に使用します。

環境変数にOTLPエンドポイントが設定されている場合、FastAPIは有効な各プロバイダーに、その送信先のエクスポーターを追加します。既存のエクスポーターは、それぞれの送信先にデータを送信し続けます。

各送信先は一度だけ設定してください。別のライブラリがすでに環境変数で指定された送信先への送信を処理している場合は、そのライブラリの環境変数に基づくエクスポートを無効にするか、FastAPIの自動設定を無効にします:

```python
app = FastAPI(telemetry={"auto_configure": False})
```

`telemetry`辞書にプロバイダーを直接渡すこともできます。例えば、次のプロバイダーはOpenTelemetryのコンソールエクスポーターを使用して、リクエストのスパンをターミナルに出力します:

{* ../../docs_src/opentelemetry/tutorial002_py310.py hl[2:8] *}

**エクスポーター**は、スパンを送信先に送ります。`BatchSpanProcessor`はスパンをまとめ、バックグラウンドで送信します。監視ライブラリの送信先を使用するには、コンソールエクスポーターをそのライブラリが提供するエクスポーターに置き換えてください。その他の設定オプションについては、[OpenTelemetryのPython計装ガイド](https://opentelemetry.io/docs/languages/python/instrumentation/)を参照してください。

メトリクスやログのプロバイダーを指定するには、同じ辞書内で`meter_provider`または`logger_provider`を使用します。プロバイダーを作成したアプリケーションまたはライブラリが、そのシャットダウンを管理します。FastAPIは、自身が追加したエクスポートコンポーネントを管理します。

/// warning | 注意

OpenTelemetryはデフォルトでグローバルプロバイダーを使用します。[マウントされたサブアプリケーション](sub-applications.md)ごとに独立したテレメトリー設定は保証されません。

///

### リクエスト操作のトレース { #trace-request-operations }

デフォルトでは、リクエストのトレースには、依存関係の解決、path operation関数の実行、レスポンスのシリアライズ、FastAPIの`BackgroundTasks`内の各タスクの実行に対応するスパンが含まれます。これらのスパンは同じプロバイダーとエクスポーターを使用します。

バックグラウンドタスクのスパンも、リクエストのトレースの一部として扱われます。これらはHTTPレスポンスのスパンが終了した後に実行されるため、測定されるレスポンス時間は増加しません。

HTTPリクエストのスパンのみを記録するには、`operation_spans`を`False`に設定します:

{* ../../docs_src/opentelemetry/tutorial003_py310.py hl[3] *}


### WebSocket接続のトレース { #trace-websocket-connections }

各WebSocket接続には、`WS /ws/{room}`のようなスパンがあり、ハンドラーと依存関係のクリーンアップを対象とします。同じプロバイダーと設定を使用し、依存関係の解決とエンドポイントの実行には`operation_spans`の設定も適用されます。

HTTPリクエストのメトリクスは、HTTPリクエストのみを対象とします。コード`1000`または`1001`による正常なWebSocket切断では、エラーログは生成されません。

### エラーの確認 { #inspect-errors }

FastAPIは、未処理の例外をOpenTelemetryのログとして記録し、リクエストまたは接続のトレースに関連付けます。トレースがサンプリングされていない場合でも、エラーログは記録されます。

例外ログには、例外の型、メッセージ、スタックトレースが含まれます。メッセージやスタックトレースには機密情報が含まれる可能性があります。プロバイダーのログプロセッサーを使用してフィルタリングやマスキングを行うか、`logs`を`False`に設定してこれらのログを無効にしてください。

FastAPIは、リクエストのバリデーション失敗も、ルートとエラー数を含む警告ログとして記録します。これらのログに無効な入力値は含まれません。

## 記録対象の選択 { #choose-what-to-record }

`telemetry`辞書では、次の設定も指定できます:

| 設定 | 目的 | デフォルト |
| --- | --- | --- |
| `tracing` | HTTPリクエストとWebSocket接続のスパンを記録します | `True` |
| `metrics` | HTTPリクエストのメトリクスを記録します | `True` |
| `logs` | バリデーション失敗と未処理の例外を記録します | `True` |
| `operation_spans` | リクエスト操作のスパンを追加します | `True` |
| `exclude` | ASGIスコープを受け取る関数が`True`を返した場合、そのリクエストを除外します | `None` |
| `auto_configure` | 環境変数に設定されたエンドポイントのエクスポーターを追加します | `True` |

例えば、ヘルスチェックを除外してメトリクスを収集するには、次のようにします:

```python
from fastapi import FastAPI

app = FastAPI(
    telemetry={
        "tracing": False,
        "exclude": lambda scope: scope["path"] == "/health",
    }
)
```

lifespan関数内などで、アプリケーション自身がプロバイダーの設定を行う場合は、`auto_configure`を`False`に設定してください。
