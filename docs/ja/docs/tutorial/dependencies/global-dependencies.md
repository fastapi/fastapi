# グローバルな依存関係 { #global-dependencies }

アプリケーションの種類によっては、アプリ全体に依存関係を追加したい場合があります。

[`dependencies` を path operation のデコレータに追加](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}できるのと同様に、`FastAPI` アプリケーション自体にも追加できます。

その場合、アプリケーション内のすべての path operation に適用されます:

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}

また、[`dependencies` を path operation のデコレータに追加](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}する節で説明した考え方はすべて引き続き当てはまりますが、この場合はアプリ内のすべての path operation に対して適用されます。

## path operation のグループに対する依存関係 { #dependencies-for-groups-of-path-operations }

後で、複数ファイルを含む大規模アプリケーションの構成方法（[大規模アプリケーション - 複数ファイル](../../tutorial/bigger-applications.md){.internal-link target=_blank}）を読むと、path operation のグループに対して 1 つの `dependencies` パラメータを宣言する方法を学びます。
