# Full Stack FastAPI テンプレート { #full-stack-fastapi-template }

テンプレートは通常、特定のセットアップが含まれていますが、柔軟でカスタマイズできるように設計されています。これにより、プロジェクトの要件に合わせて変更・適応でき、優れた出発点になります。🏁

このテンプレートを使って開始できます。初期セットアップ、セキュリティ、データベース、いくつかのAPIエンドポイントがすでに用意されています。

GitHubリポジトリ: <a href="https://github.com/tiangolo/full-stack-fastapi-template" class="external-link" target="_blank">Full Stack FastAPI Template</a>

## Full Stack FastAPI テンプレート - 技術スタックと機能 { #full-stack-fastapi-template-technology-stack-and-features }

- ⚡ PythonバックエンドAPI向けの [**FastAPI**](https://fastapi.tiangolo.com/ja)。
  - 🧰 PythonのSQLデータベース操作（ORM）向けの [SQLModel](https://sqlmodel.tiangolo.com)。
  - 🔍 FastAPIで使用される、データバリデーションと設定管理向けの [Pydantic](https://docs.pydantic.dev)。
  - 💾 SQLデータベースとしての [PostgreSQL](https://www.postgresql.org)。
- 🚀 フロントエンド向けの [React](https://react.dev)。
  - 💃 TypeScript、hooks、Vite、その他のモダンなフロントエンドスタックの各要素を使用。
  - 🎨 フロントエンドコンポーネント向けの [Tailwind CSS](https://tailwindcss.com) と [shadcn/ui](https://ui.shadcn.com)。
  - 🤖 自動生成されたフロントエンドクライアント。
  - 🧪 End-to-Endテスト向けの [Playwright](https://playwright.dev)。
  - 🦇 ダークモードのサポート。
- 🐋 開発および本番向けの [Docker Compose](https://www.docker.com)。
- 🔒 デフォルトでの安全なパスワードハッシュ化。
- 🔑 JWT（JSON Web Token）認証。
- 📫 メールベースのパスワードリカバリ。
- ✅ [Pytest](https://pytest.org) によるテスト。
- 📞 リバースプロキシ / ロードバランサとしての [Traefik](https://traefik.io)。
- 🚢 Docker Composeを使用したデプロイ手順（自動HTTPS証明書を処理するフロントエンドTraefikプロキシのセットアップ方法を含む）。
- 🏭 GitHub Actionsに基づくCI（continuous integration）とCD（continuous deployment）。
