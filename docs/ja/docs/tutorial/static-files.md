# 静的ファイル

`StaticFiles` を使用して、ディレクトリから静的ファイルを自動的に提供できます。

## `StaticFiles` の使用

* `StaticFiles` をインポート。
* `StaticFiles()` インスタンスを生成し、特定のパスに「マウント」。

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "技術詳細"
    `from starlette.staticfiles import StaticFiles` も使用できます。

    **FastAPI**は、開発者の利便性のために、`starlette.staticfiles` と同じ `fastapi.staticfiles` を提供します。しかし、実際にはStarletteから直接渡されています。

### 「マウント」とは

「マウント」とは、特定のパスに完全な「独立した」アプリケーションを追加することを意味します。これにより、すべてのサブパスの処理がなされます。

これは、マウントされたアプリケーションが完全に独立しているため、`APIRouter` とは異なります。メインアプリケーションのOpenAPIとドキュメントには、マウントされたアプリケーションの内容などは含まれません。

これについて詳しくは、**高度なユーザーガイド** をご覧ください。

## 詳細

最初の `"/static"` は、この「サブアプリケーション」が「マウント」されるサブパスを指します。したがって、`"/static"` から始まるパスはすべてサブアプリケーションによって処理されます。

`directory="static"` は、静的ファイルを含むディレクトリの名前を指します。

`name="static"` は、**FastAPI** が内部で使用できる名前を付けます。

これらのパラメータはすべて「`静的`」とは異なる場合があり、独自のアプリケーションのニーズと詳細に合わせて調整します。

## より詳しい情報

詳細とオプションについては、<a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Starletteの静的ファイルに関するドキュメント</a>を確認してください。
