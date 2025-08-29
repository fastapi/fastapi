# メタデータとドキュメントのURL

**FastAPI** アプリケーションのいくつかのメタデータの設定をカスタマイズできます。

## タイトル、説明文、バージョン

以下を設定できます:

* **タイトル**: OpenAPIおよび自動APIドキュメントUIでAPIのタイトル/名前として使用される。
* **説明文**: OpenAPIおよび自動APIドキュメントUIでのAPIの説明文。
* **バージョン**: APIのバージョン。例: `v2` または `2.5.0`。
     *たとえば、以前のバージョンのアプリケーションがあり、OpenAPIも使用している場合に便利です。

これらを設定するには、パラメータ `title`、`description`、`version` を使用します:

{* ../../docs_src/metadata/tutorial001.py hl[4:6] *}

この設定では、自動APIドキュメントは以下の様になります:

<img src="/img/tutorial/metadata/image01.png">

## タグのためのメタデータ

さらに、パラメータ `openapi_tags` を使うと、path operations をグループ分けするための複数のタグに関するメタデータを追加できます。

それぞれのタグ毎にひとつの辞書を含むリストをとります。

それぞれの辞書は以下をもつことができます:

* `name` (**必須**): *path operations* および `APIRouter` の `tags` パラメーターで使用するのと同じタグ名である `str`。
* `description`: タグの簡単な説明文である `str`。 Markdownで記述でき、ドキュメントUIに表示されます。
* `externalDocs`: 外部ドキュメントを説明するための `dict`:
    * `description`: 外部ドキュメントの簡単な説明文である `str`。
    * `url` (**必須**): 外部ドキュメントのURLである `str`。

### タグのためのメタデータの作成

`users` と `items` のタグを使った例でメタデータの追加を試してみましょう。

タグのためのメタデータを作成し、それを `openapi_tags` パラメータに渡します。

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

説明文 (description) の中で Markdown を使用できることに注意してください。たとえば、「login」は太字 (**login**) で表示され、「fancy」は斜体 (_fancy_) で表示されます。

/// tip | 豆知識

使用するすべてのタグにメタデータを追加する必要はありません。

///

### 自作タグの使用

`tags` パラメーターを使用して、それぞれの *path operations* (および `APIRouter`) を異なるタグに割り当てます:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info | 情報

タグのより詳しい説明を知りたい場合は [Path Operation Configuration](path-operation-configuration.md#tags){.internal-link target=_blank} を参照して下さい。

///

### ドキュメントの確認

ここで、ドキュメントを確認すると、追加したメタデータがすべて表示されます:

<img src="/img/tutorial/metadata/image02.png">

### タグの順番

タグのメタデータ辞書の順序は、ドキュメントUIに表示される順序の定義にもなります。

たとえば、`users` はアルファベット順では `items` の後に続きます。しかし、リストの最初に `users` のメタデータ辞書を追加したため、ドキュメントUIでは `users` が先に表示されます。

## OpenAPI URL

デフォルトでは、OpenAPIスキーマは `/openapi.json` で提供されます。

ただし、パラメータ `openapi_url` を使用して設定を変更できます。

たとえば、`/api/v1/openapi.json` で提供されるように設定するには:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

OpenAPIスキーマを完全に無効にする場合は、`openapi_url=None` を設定できます。これにより、それを使用するドキュメントUIも無効になります。

## ドキュメントのURL

以下の2つのドキュメントUIを構築できます:

* **Swagger UI**: `/docs` で提供されます。
     * URL はパラメータ `docs_url` で設定できます。
     * `docs_url=None` を設定することで無効にできます。
* ReDoc: `/redoc` で提供されます。
     * URL はパラメータ `redoc_url` で設定できます。
     * `redoc_url=None` を設定することで無効にできます。

たとえば、`/documentation` でSwagger UIが提供されるように設定し、ReDocを無効にするには:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
