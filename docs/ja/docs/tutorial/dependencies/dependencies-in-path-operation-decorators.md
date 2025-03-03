# path operationデコレータの依存関係

場合によっては*path operation関数*の中で依存関係の戻り値を本当に必要としないこともあります。

もしくは、依存関係が値を返さない場合もあります。

しかし、それでも実行・解決する必要があります。

このような場合、*path operation関数*のパラメータを`Depends`で宣言する代わりに、*path operation decorator*に`dependencies`の`list`を追加することができます。

##  *path operationデコレータ*への`dependencies`の追加

*path operationデコレータ*はオプショナルの引数`dependencies`を受け取ります。

それは`Depends()`の`list`であるべきです:

{* ../../docs_src/dependencies/tutorial006.py hl[17] *}

これらの依存関係は、通常の依存関係と同様に実行・解決されます。しかし、それらの値（何かを返す場合）は*path operation関数*には渡されません。

/// tip | 豆知識

エディタによっては、未使用の関数パラメータをチェックしてエラーとして表示するものもあります。

`dependencies`を`path operationデコレータ`で使用することで、エディタやツールのエラーを回避しながら確実に実行することができます。

また、コードの未使用のパラメータがあるのを見て、それが不要だと思ってしまうような新しい開発者の混乱を避けるのにも役立つかもしれません。

///

## 依存関係のエラーと戻り値

通常使用している依存関係の*関数*と同じものを使用することができます。

### 依存関係の要件

これらはリクエストの要件（ヘッダのようなもの）やその他のサブ依存関係を宣言することができます:

{* ../../docs_src/dependencies/tutorial006.py hl[6,11] *}

### 例外の発生

これらの依存関係は通常の依存関係と同じように、例外を`raise`発生させることができます:

{* ../../docs_src/dependencies/tutorial006.py hl[8,13] *}

### 戻り値

そして、値を返すことも返さないこともできますが、値は使われません。

つまり、すでにどこかで使っている通常の依存関係（値を返すもの）を再利用することができ、値は使われなくても依存関係は実行されます:

{* ../../docs_src/dependencies/tutorial006.py hl[9,14] *}

## *path operations*のグループに対する依存関係

後で、より大きなアプリケーションの構造([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank})について読む時に、おそらく複数のファイルを使用して、*path operations*のグループに対して単一の`dependencies`パラメータを宣言する方法を学ぶでしょう。
