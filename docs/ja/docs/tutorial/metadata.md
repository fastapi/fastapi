# メタデータとドキュメントのURL { #metadata-and-docs-urls }

**FastAPI** アプリケーションのいくつかのメタデータ設定をカスタマイズできます。

## APIのメタデータ { #metadata-for-api }

OpenAPI仕様および自動APIドキュメントUIで使用される次のフィールドを設定できます:

| パラメータ | 型 | 説明 |
|------------|------|-------------|
| `title` | `str` | APIのタイトルです。 |
| `summary` | `str` | APIの短い要約です。 <small>OpenAPI 3.1.0、FastAPI 0.99.0 以降で利用できます。</small> |
| `description` | `str` | APIの短い説明です。Markdownを使用できます。 |
| `version` | `string` | APIのバージョンです。これはOpenAPIのバージョンではなく、あなた自身のアプリケーションのバージョンです。たとえば `2.5.0` です。 |
| `terms_of_service` | `str` | APIの利用規約へのURLです。指定する場合、URLである必要があります。 |
| `contact` | `dict` | 公開されるAPIの連絡先情報です。複数のフィールドを含められます。 <details><summary><code>contact</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>連絡先の個人/組織を識別する名前です。</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>連絡先情報を指すURLです。URL形式である必要があります。</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>連絡先の個人/組織のメールアドレスです。メールアドレス形式である必要があります。</td></tr></tbody></table></details> |
| `license_info` | `dict` | 公開されるAPIのライセンス情報です。複数のフィールドを含められます。 <details><summary><code>license_info</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>必須</strong>（<code>license_info</code> が設定されている場合）。APIに使用されるライセンス名です。</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>APIの <a href="https://spdx.org/licenses/" class="external-link" target="_blank">SPDX</a> ライセンス式です。<code>identifier</code> フィールドは <code>url</code> フィールドと同時に指定できません。 <small>OpenAPI 3.1.0、FastAPI 0.99.0 以降で利用できます。</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>APIに使用されるライセンスへのURLです。URL形式である必要があります。</td></tr></tbody></table></details> |

以下のように設定できます:

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip | 豆知識

`description` フィールドにはMarkdownを書けて、出力ではレンダリングされます。

///

この設定では、自動APIドキュメントは以下のようになります:

<img src="/img/tutorial/metadata/image01.png">

## ライセンス識別子 { #license-identifier }

OpenAPI 3.1.0 および FastAPI 0.99.0 以降では、`license_info` を `url` の代わりに `identifier` で設定することもできます。

例:

{* ../../docs_src/metadata/tutorial001_1_py310.py hl[31] *}

## タグのメタデータ { #metadata-for-tags }

パラメータ `openapi_tags` を使うと、path operation をグループ分けするために使用する各タグに追加のメタデータを追加できます。

それぞれのタグごとに1つの辞書を含むリストを取ります。

それぞれの辞書は以下を含められます:

* `name` (**必須**): *path operation* および `APIRouter` の `tags` パラメータで使用するのと同じタグ名の `str`。
* `description`: タグの短い説明の `str`。Markdownを含められ、ドキュメントUIに表示されます。
* `externalDocs`: 外部ドキュメントを説明する `dict`。以下を含みます:
    * `description`: 外部ドキュメントの短い説明の `str`。
    * `url` (**必須**): 外部ドキュメントのURLの `str`。

### タグのメタデータの作成 { #create-metadata-for-tags }

`users` と `items` のタグを使った例で試してみましょう。

タグのメタデータを作成し、それを `openapi_tags` パラメータに渡します:

{* ../../docs_src/metadata/tutorial004_py310.py hl[3:16,18] *}

説明の中でMarkdownを使用できることに注意してください。たとえば「login」は太字 (**login**) で表示され、「fancy」は斜体 (_fancy_) で表示されます。

/// tip | 豆知識

使用するすべてのタグにメタデータを追加する必要はありません。

///

### タグの使用 { #use-your-tags }

*path operation*（および `APIRouter`）の `tags` パラメータを使用して、それらを異なるタグに割り当てます:

{* ../../docs_src/metadata/tutorial004_py310.py hl[21,26] *}

/// info | 情報

タグの詳細は [Path Operation Configuration](path-operation-configuration.md#tags){.internal-link target=_blank} を参照してください。

///

### ドキュメントの確認 { #check-the-docs }

ここでドキュメントを確認すると、追加したメタデータがすべて表示されます:

<img src="/img/tutorial/metadata/image02.png">

### タグの順番 { #order-of-tags }

タグのメタデータ辞書の順序は、ドキュメントUIに表示される順序の定義にもなります。

たとえば、`users` はアルファベット順では `items` の後に続きますが、リストの最初の辞書としてメタデータを追加したため、それより前に表示されます。

## OpenAPI URL { #openapi-url }

デフォルトでは、OpenAPIスキーマは `/openapi.json` で提供されます。

ただし、パラメータ `openapi_url` を使用して設定を変更できます。

たとえば、`/api/v1/openapi.json` で提供されるように設定するには:

{* ../../docs_src/metadata/tutorial002_py310.py hl[3] *}

OpenAPIスキーマを完全に無効にする場合は、`openapi_url=None` を設定できます。これにより、それを使用するドキュメントUIも無効になります。

## ドキュメントのURL { #docs-urls }

含まれている2つのドキュメントUIを設定できます:

* **Swagger UI**: `/docs` で提供されます。
    * URL はパラメータ `docs_url` で設定できます。
    * `docs_url=None` を設定することで無効にできます。
* **ReDoc**: `/redoc` で提供されます。
    * URL はパラメータ `redoc_url` で設定できます。
    * `redoc_url=None` を設定することで無効にできます。

たとえば、`/documentation` でSwagger UIが提供されるように設定し、ReDocを無効にするには:

{* ../../docs_src/metadata/tutorial003_py310.py hl[3] *}
