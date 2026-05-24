# エディタ対応 { #editor-support }

公式の[FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode)は、*path operation* の検出・ナビゲーションに加え、FastAPI Cloud へのデプロイやライブログストリーミングなど、FastAPI の開発ワークフローを強化します。

拡張機能の詳細は、[GitHub リポジトリ](https://github.com/fastapi/fastapi-vscode)の README を参照してください。

## セットアップとインストール { #setup-and-installation }

**FastAPI Extension** は [VS Code](https://code.visualstudio.com/) と [Cursor](https://www.cursor.com/) の両方で利用できます。各エディタの拡張機能パネルから「FastAPI」を検索し、**FastAPI Labs** が公開している拡張機能を選択して直接インストールできます。 [vscode.dev](https://vscode.dev) や [github.dev](https://github.dev) などのブラウザベースのエディタでも動作します。

### アプリケーション検出 { #application-discovery }

既定では、ワークスペース内で `FastAPI()` を生成しているファイルを走査し、FastAPI アプリケーションを自動検出します。プロジェクト構成の都合で自動検出が機能しない場合は、`pyproject.toml` の `[tool.fastapi]`、または VS Code 設定の `fastapi.entryPoint` にモジュール記法（例: `myapp.main:app`）でエントリポイントを指定できます。

## 機能 { #features }

- **Path Operation エクスプローラー** - アプリケーション内のすべての <dfn title="ルート、エンドポイント">*path operations*</dfn> をサイドバーのツリービューで表示します。クリックして任意のルートまたはルーター定義へジャンプできます。
- **ルート検索** - <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>（macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>）で、パス・メソッド・名前で検索できます。
- **CodeLens ナビゲーション** - テストクライアント呼び出し（例: `client.get('/items')`）の上に表示されるクリック可能なリンクから、対応する *path operation* にジャンプし、テストと実装の行き来をすばやく行えます。
- **FastAPI Cloud へデプロイ** - [FastAPI Cloud](https://fastapicloud.com/) にワンクリックでアプリをデプロイできます。
- **アプリケーションログのストリーミング** - FastAPI Cloud にデプロイしたアプリから、レベルフィルタやテキスト検索付きでリアルタイムにログをストリーミングできます。

拡張機能の機能に慣れるには、コマンドパレット（<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>、macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>）を開き、"Welcome: Open walkthrough..." を選択してから、"Get started with FastAPI" のウォークスルーを選んでください。
