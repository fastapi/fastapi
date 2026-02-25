# path operation デコレータの依存関係 { #dependencies-in-path-operation-decorators }

場合によっては、*path operation 関数*の中で依存関係の戻り値を実際には必要としないことがあります。

または、依存関係が値を返さない場合もあります。

しかし、それでも実行・解決される必要があります。

そのような場合、`Depends` で *path operation 関数* のパラメータを宣言する代わりに、*path operation デコレータ*に `dependencies` の `list` を追加できます。

## *path operation デコレータ*に`dependencies`を追加 { #add-dependencies-to-the-path-operation-decorator }

*path operation デコレータ*はオプション引数`dependencies`を受け取ります。

それは`Depends()`の`list`であるべきです:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

これらの依存関係は、通常の依存関係と同様に実行・解決されます。しかし、それらの値（何かを返す場合）は*path operation 関数*には渡されません。

/// tip | 豆知識

一部のエディタは、未使用の関数パラメータをチェックしてエラーとして表示します。

これらの`dependencies`を*path operation デコレータ*で使用することで、エディタ/ツールのエラーを回避しつつ、確実に実行されるようにできます。

また、コード内の未使用のパラメータを見た新しい開発者が、それを不要だと思って混乱するのを避ける助けにもなるかもしれません。

///

/// info | 情報

この例では、架空のカスタムヘッダー `X-Key` と `X-Token` を使用しています。

しかし実際のケースでセキュリティを実装する際は、統合された[Security utilities（次の章）](../security/index.md){.internal-link target=_blank}を使うことで、より多くの利点を得られます。

///

## 依存関係のエラーと戻り値 { #dependencies-errors-and-return-values }

通常使用している依存関係の*関数*と同じものを使用できます。

### 依存関係の要件 { #dependency-requirements }

これらはリクエストの要件（ヘッダーのようなもの）やその他のサブ依存関係を宣言できます:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### 例外の発生 { #raise-exceptions }

これらの依存関係は、通常の依存関係と同じように例外を`raise`できます:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### 戻り値 { #return-values }

そして、値を返すことも返さないこともできますが、値は使われません。

つまり、すでにどこかで使っている通常の依存関係（値を返すもの）を再利用でき、値は使われなくても依存関係は実行されます:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## *path operation*のグループに対する依存関係 { #dependencies-for-a-group-of-path-operations }

後で、より大きなアプリケーションを（おそらく複数ファイルで）構造化する方法（[Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}）について読むときに、*path operation*のグループに対して単一の`dependencies`パラメータを宣言する方法を学びます。

## グローバル依存関係 { #global-dependencies }

次に、`FastAPI`アプリケーション全体に依存関係を追加して、各*path operation*に適用する方法を見ていきます。
