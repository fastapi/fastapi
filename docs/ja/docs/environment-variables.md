# 環境変数 { #environment-variables }

/// tip | 豆知識

もし、「環境変数」とは何か、それをどう使うかを既に知っている場合は、このセクションをスキップして構いません。

///

環境変数（「**env var**」とも呼ばれます）とは、Pythonコードの**外側**、つまり**オペレーティングシステム**に存在する変数で、Pythonコード（または他のプログラム）から読み取れます。

環境変数は、アプリケーションの**設定**の扱い、Pythonの**インストール**の一部などで役立ちます。

## 環境変数の作成と使用 { #create-and-use-env-vars }

環境変数は、Pythonを必要とせず、**シェル（ターミナル）**で**作成**して使用できます。

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Pythonで環境変数を読み取る { #read-env-vars-in-python }

環境変数はPythonの**外側**（ターミナル、またはその他の方法）で作成し、その後に**Pythonで読み取る**こともできます。

例えば、以下のような`main.py`ファイルを用意します:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | 豆知識

<a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> の第2引数は、デフォルトで返される値です。

指定しない場合、デフォルトは`None`ですが、ここでは使用するデフォルト値として`"World"`を指定しています。

///

次に、このPythonプログラムを呼び出します。

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

環境変数はコードの外側で設定でき、コードから読み取れ、他のファイルと一緒に（`git`に）保存（コミット）する必要がないため、設定や**settings**に使うのが一般的です。

また、**特定のプログラムの呼び出し**のためだけに、そのプログラムでのみ、実行中の間だけ利用できる環境変数を作成することもできます。

そのためには、同じ行で、プログラム自体の直前に作成してください。

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | 豆知識

詳しくは <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: 設定</a> を参照してください。

///

## 型とバリデーション { #types-and-validation }

これらの環境変数が扱えるのは**テキスト文字列**のみです。環境変数はPythonの外部にあり、他のプログラムやシステム全体（Linux、Windows、macOSなど異なるオペレーティングシステム間も）との互換性が必要になるためです。

つまり、環境変数からPythonで読み取る**あらゆる値**は **`str`になり**、他の型への変換やバリデーションはコード内で行う必要があります。

環境変数を使って**アプリケーション設定**を扱う方法については、[高度なユーザーガイド - Settings and Environment Variables](./advanced/settings.md){.internal-link target=_blank} で詳しく学べます。

## `PATH`環境変数 { #path-environment-variable }

**`PATH`**という**特別な**環境変数があります。これはオペレーティングシステム（Linux、macOS、Windows）が実行するプログラムを見つけるために使用されます。

変数`PATH`の値は長い文字列で、LinuxとmacOSではコロン`:`、Windowsではセミコロン`;`で区切られたディレクトリで構成されます。

例えば、`PATH`環境変数は次のような文字列かもしれません:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

これは、システムが次のディレクトリでプログラムを探すことを意味します:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

これは、システムが次のディレクトリでプログラムを探すことを意味します:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

ターミナル上で**コマンド**を入力すると、オペレーティングシステムは`PATH`環境変数に記載された**それぞれのディレクトリ**の中からプログラムを**探し**ます。

例えば、ターミナルで`python`と入力すると、オペレーティングシステムはそのリストの**最初のディレクトリ**で`python`というプログラムを探します。

見つかればそれを**使用**します。見つからなければ、**他のディレクトリ**を探し続けます。

### Pythonのインストールと`PATH`の更新 { #installing-python-and-updating-the-path }

Pythonのインストール時に、`PATH`環境変数を更新するかどうかを尋ねられるかもしれません。

//// tab | Linux, macOS

Pythonをインストールして、その結果`/opt/custompython/bin`というディレクトリに配置されたとします。

`PATH`環境変数を更新することに同意すると、インストーラーは`PATH`環境変数に`/opt/custompython/bin`を追加します。

例えば次のようになります:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

このようにして、ターミナルで`python`と入力すると、システムは`/opt/custompython/bin`（最後のディレクトリ）にあるPythonプログラムを見つけ、それを使用します。

////

//// tab | Windows

Pythonをインストールして、その結果`C:\opt\custompython\bin`というディレクトリに配置されたとします。

`PATH`環境変数を更新することに同意すると、インストーラーは`PATH`環境変数に`C:\opt\custompython\bin`を追加します。

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

このようにして、ターミナルで`python`と入力すると、システムは`C:\opt\custompython\bin`（最後のディレクトリ）にあるPythonプログラムを見つけ、それを使用します。

////

つまり、ターミナルで次のように入力すると:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

システムは`/opt/custompython/bin`にある`python`プログラムを**見つけ**て実行します。

これは、次のように入力するのとおおむね同等です:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

システムは`C:\opt\custompython\bin\python`にある`python`プログラムを**見つけ**て実行します。

これは、次のように入力するのとおおむね同等です:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

この情報は、[Virtual Environments](virtual-environments.md){.internal-link target=_blank} について学ぶ際にも役立ちます。

## まとめ { #conclusion }

これで、**環境変数**とは何か、Pythonでどのように使用するかについて、基本的な理解が得られたはずです。

環境変数についての詳細は、<a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia の環境変数</a> も参照してください。

多くの場合、環境変数がどのように役立ち、すぐに適用できるのかはあまり明確ではありません。しかし、開発中のさまざまなシナリオで何度も登場するため、知っておくとよいでしょう。

例えば、次のセクションの[Virtual Environments](virtual-environments.md)でこの情報が必要になります。
