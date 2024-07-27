# グローバルな依存関係 <!-- # Global Dependencies -->

<!-- For some types of applications you might want to add dependencies to the whole application. -->
アプリケーションによっては、アプリケーション全体に依存関係を追加したい場合があります。

<!-- Similar to the way you can [add `dependencies` to the *path operation decorators*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, you can add them to the `FastAPI` application. -->
[*path operations*デコレータの`依存関係`](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}と同じ方法で、`FastAPI`アプリケーション全体に依存関係を追加することができます。

<!-- In that case, they will be applied to all the *path operations* in the application: -->
この方法は、アプリケーション内のすべての*path operations*に適用されます:

=== "Python 3.9+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an.py!}
    ```

=== "Python 3.8 non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="15"
    {!> ../../../docs_src/dependencies/tutorial012.py!}
    ```

<!-- And all the ideas in the section about [adding `dependencies` to the *path operation decorators*](dependencies-in-path-operation-decorators.md ){.internal-link target=_blank} still apply, but in this case, to all of the *path operations* in the app. -->
[*path operations* デコレータの依存関係](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}に記載されていることが、アプリケーション内のすべての*path operations*に適用されます。

<!-- ## Dependencies for groups of *path operations* -->
## *path operations*のグループに対する依存関係

<!-- Later, when reading about how to structure bigger applications ([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}), possibly with multiple files, you will learn how to declare a single `dependencies` parameter for a group of *path operations*. -->

後で、より大きなアプリケーションの構造([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}))について読む時に、おそらく複数のファイルを使用して、*path operations*のグループに対して単一の`dependencies`パラメータを宣言する方法を学ぶでしょう。
