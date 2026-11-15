# AIを使った開発 { #develop-with-ai }

FastAPIには、公式の**エージェントスキル**がPythonパッケージに同梱されています。プロジェクトにインストールされたバージョンに対応するガイダンスを提供します。

## スキルのインストール { #install-the-skill }

[FastAPIをインストール](tutorial/index.md#install-fastapi)した後、プロジェクトディレクトリから[Library Skills](https://library-skills.io/use/)を実行します:

```bash
uvx library-skills
```

FastAPIスキルを選択し、Codexやほとんどのエージェントでは`.agents/skills`を、Claude Codeでは`.claude/skills`を選択します。両方を選択することもできます。

これで、エージェントはFastAPIのコードを扱う際にスキルを自動的に使用できます。

### 対話なしでのインストール { #install-without-prompts }

エージェントやスクリプト向けには、対話型プロンプトなしでFastAPIスキルを選択します:

```bash
uvx library-skills install --skill fastapi --yes
```

Claude Code向けには、`--claude`を追加して`.claude/skills`にもインストールします:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## アプリの設定 { #configure-your-app }

FastAPIのツールがアプリを見つけられるように、`pyproject.toml`で[アプリのエントリーポイント](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml)を設定します:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

アプリのモジュール名と変数名を使用してください。ここでは、`main:app`は`main.py`内の`app`オブジェクトを指します。

## アプリの実行 { #run-your-app }

ローカル開発には[FastAPI CLI](fastapi-cli.md)を使用します:

```bash
uv run fastapi dev
```

本番環境では、`uv run fastapi run`を使用します。

## SDKの生成 { #generate-an-sdk }

フロントエンドやAPIクライアントの開発については、[SDKの生成](advanced/generate-clients.md)を参照してください。

## アプリのデプロイ { #deploy-your-app }

FastAPIチームが提供する公式のマネージドデプロイプラットフォーム、[FastAPI Cloud](deployment/fastapicloud.md)にデプロイするには、次を実行します:

```bash
uv run fastapi deploy
```

別のクラウドプロバイダーや独自のサーバーに[手動でデプロイ](deployment/manually.md)することもできます。

## エージェントプラグイン { #agent-plugins }

[CodexおよびClaude Code向けのFastAPI Cloudプラグイン](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/)には、プロジェクトの作成方法と、依存パッケージに同梱されたライブラリスキルの使用方法が含まれています。FastAPI Cloudを使用しない場合でも役立ちます。

また、FastAPI Cloudへのデプロイ、ログ、環境変数についても説明しています。
