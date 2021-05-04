# デバッグ

Visual Studio CodeやPyCharmなどを使用して、エディター上でデバッガーと連携できます。

## `uvicorn` の実行

FastAPIアプリケーション上で、`uvicorn` を直接インポートして実行します:

```Python hl_lines="1  15"
{!../../../docs_src/debugging/tutorial001.py!}
```

### `__name__ == "__main__"` について

`__name__ == "__main__"` の主な目的は、ファイルが次のコマンドで呼び出されたときに実行されるコードを用意することです:

<div class="termy">

```console
$ python myapp.py
```

</div>

ただし、次のように、別のファイルからインポートされるときには呼び出されません:

```Python
from myapp import app
```

#### より詳しい説明

ファイルの名前が `myapp.py` だとします。

以下の様に実行する場合:

<div class="termy">

```console
$ python myapp.py
```

</div>

Pythonによって自動的に作成されたファイル内の内部変数 `__name__` は、値として文字列 `"__main__"` を持ちます。

なので、以下:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

は実行されます。

---

そのモジュール (ファイル) をインポートした場合は、こうはなりません。

したがって、次のようなもう一つのファイル `importer.py` がある場合:

```Python
from myapp import app

# Some more code
```

`myapp.py` 内の自動変数には、値が `"__main __"` の変数 `__name__` はありません。

したがって、以下の行:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

は実行されません。

!!! info "情報"
    より詳しい情報は、<a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">公式Pythonドキュメント</a>を参照してください。

## デバッガーでコードを実行

コードから直接Uvicornサーバーを実行しているため、デバッガーから直接Pythonプログラム (FastAPIアプリケーション) を呼び出せます。

---

例えば、Visual Studio Codeでは、次のことが可能です:

* 「デバッグ」パネルに移動。
* 「構成の追加...」
* 「Python」を選択。
* オプション「`Python: Current File (Integrated Terminal)`」を指定してデバッガーを実行。

すると、**FastAPI** コードでサーバーが起動され、ブレークポイントで停止したりするでしょう。

以下の様な画面になります:

<img src="/img/tutorial/debugging/image01.png">

---

Pycharmを使用する場合、次のことが可能です:

* 「実行」メニューをオープン。
* オプション「デバッグ...」を選択。
* 次にコンテキストメニューが表示される。
* デバッグするファイル (ここでは `main.py`) を選択。

すると、**FastAPI** コードでサーバーが起動され、ブレークポイントで停止したりするでしょう。

以下の様な画面になります:

<img src="/img/tutorial/debugging/image02.png">
