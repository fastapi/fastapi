# OpenAPI の Webhook { #openapi-webhooks }

アプリがある種の**イベント**を**通知**するために、データ付きで相手のアプリ（リクエスト送信）を呼び出す可能性があることを、API の**ユーザー**に伝えたい場合があります。

これは、通常のようにユーザーがあなたの API にリクエストを送るのではなく、**あなたの API（あなたのアプリ）**が**相手のシステム**（相手の API、アプリ）にリクエストを送る、ということです。

これは一般に**Webhook**と呼ばれます。

## Webhook の手順 { #webhooks-steps }

通常の流れとして、まずあなたのコード内で、送信するメッセージ、すなわちリクエストの**本文（ボディ）**を**定義**します。

加えて、アプリがそれらのリクエスト（イベント）を送信する**タイミング**も何らかの形で定義します。

そして**ユーザー**は、アプリがそのリクエストを送るべき**URL**を（たとえばどこかの Web ダッシュボードで）定義します。

Webhook の URL を登録する方法や実際にリクエストを送るコードなど、これらの**ロジック**はすべてあなた次第です。**あなた自身のコード**で好きなように実装します。

## FastAPI と OpenAPI による Webhook のドキュメント化 { #documenting-webhooks-with-fastapi-and-openapi }

**FastAPI** と OpenAPI を使うと、Webhook の名前、アプリが送信できる HTTP の操作（例: `POST`, `PUT` など）、アプリが送るリクエストの**ボディ**を定義できます。

これにより、ユーザーがあなたの **Webhook** リクエストを受け取るための**API を実装**するのが大幅に簡単になります。場合によっては、ユーザーが自分たちの API コードを自動生成できるかもしれません。

/// info | 情報

Webhook は OpenAPI 3.1.0 以上で利用可能で、FastAPI `0.99.0` 以上が対応しています。

///

## Webhook を持つアプリ { #an-app-with-webhooks }

**FastAPI** アプリケーションを作成すると、`webhooks` という属性があり、ここで *path operations* と同様に（例: `@app.webhooks.post()`）*webhook* を定義できます。

{* ../../docs_src/openapi_webhooks/tutorial001_py310.py hl[9:12,15:20] *}

定義した webhook は **OpenAPI** スキーマおよび自動生成される **ドキュメント UI** に反映されます。

/// info | 情報

`app.webhooks` オブジェクトは実際には単なる `APIRouter` で、複数ファイルでアプリを構成する際に使うものと同じ型です。

///

Webhook では（`/items/` のような）*パス*を宣言しているわけではない点に注意してください。ここで渡す文字列は webhook の**識別子**（イベント名）です。たとえば `@app.webhooks.post("new-subscription")` での webhook 名は `new-subscription` です。

これは、**ユーザー**が実際に Webhook リクエストを受け取りたい**URL パス**を、別の方法（例: Web ダッシュボード）で定義することを想定しているためです。

### ドキュメントの確認 { #check-the-docs }

アプリを起動し、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> にアクセスします。

ドキュメントには通常の *path operations* に加えて、**webhooks** も表示されます:

<img src="/img/tutorial/openapi-webhooks/image01.png">
