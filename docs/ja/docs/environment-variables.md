# 環境変数

/// tip

もし、「環境変数」とは何か、それをどう使うかを既に知っている場合は、このセクションをスキップして構いません。

///

環境変数（**env var**とも呼ばれる）はPythonコードの**外側**、つまり**OS**に存在する変数で、Pythonから読み取ることができます。（他のプログラムでも同様に読み取れます。）

環境変数は、アプリケーションの**設定**の管理や、Pythonの**インストール**などに役立ちます。

## 環境変数の作成と使用

環境変数は**シェル（ターミナル）**内で**作成**して使用でき、それらにPythonは不要です。

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

## Pythonで環境変数を読み取る

環境変数をPythonの**外側**、ターミナル（や他の方法）で作成し、**Python内で読み取る**こともできます。

例えば、以下のような`main.py`ファイルを用意します:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

<a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> の第2引数は、デフォルトで返される値を指定します。

この引数を省略するとデフォルト値として`None`が返されますが、ここではデフォルト値として`"World"`を指定しています。

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

環境変数はコードの外側で設定し、内側から読み取ることができるので、他のファイルと一緒に（`git`に）保存する必要がありません。そのため、環境変数をコンフィグレーションや**設定**に使用することが一般的です。

また、**特定のプログラムの呼び出し**のための環境変数を、そのプログラムのみ、その実行中に限定して利用できるよう作成できます。

そのためには、プログラム起動コマンドと同じコマンドライン上の、起動コマンド直前で環境変数を作成してください。

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

/// tip

詳しくは <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a> を参照してください。

///

## 型とバリデーション

環境変数は**テキスト文字列**のみを扱うことができます。これは、環境変数がPython外部に存在し、他のプログラムやシステム全体（Linux、Windows、macOS間の互換性を含む）と連携する必要があるためです。

つまり、Pythonが環境変数から読み取る**あらゆる値**は **`str`型となり**、他の型への変換やバリデーションはコード内で行う必要があります。

環境変数を使用して**アプリケーション設定**を管理する方法については、[高度なユーザーガイド - Settings and Environment Variables](./advanced/settings.md){.internal-link target=_blank}で詳しく学べます。

## `PATH`環境変数

**`PATH`**という**特別な**環境変数があります。この環境変数は、OS（Linux、macOS、Windows）が実行するプログラムを発見するために使用されます。

`PATH`変数は、複数のディレクトリのパスから成る長い文字列です。このパスはLinuxやMacOSの場合は`:`で、Windowsの場合は`;`で区切られています。

例えば、`PATH`環境変数は次のような文字列かもしれません:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

これは、OSはプログラムを見つけるために以下のディレクトリを探す、ということを意味します:

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

これは、OSはプログラムを見つけるために以下のディレクトリを探す、ということを意味します:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

ターミナル上で**コマンド**を入力すると、 OSはそのプログラムを見つけるために、`PATH`環境変数のリストに記載された**それぞれのディレクトリを探し**ます。

例えば、ターミナル上で`python`を入力すると、OSは`python`によって呼ばれるプログラムを見つけるために、そのリストの**先頭のディレクトリ**を最初に探します。

OSは、もしそのプログラムをそこで発見すれば**実行し**ますが、そうでなければリストの**他のディレクトリ**を探していきます。

### PythonのインストールとPATH環境変数の更新

Pythonのインストール時に`PATH`環境変数を更新したいか聞かれるかもしれません。

/// tab | Linux, macOS

Pythonをインストールして、そのプログラムが`/opt/custompython/bin`というディレクトリに配置されたとします。

もし、`PATH`環境変数を更新するように答えると、`PATH`環境変数に`/opt/custompython/bin`が追加されます。

`PATH`環境変数は以下のように更新されるでしょう：

``` plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

このようにして、ターミナルで`python`と入力したときに、OSは`/opt/custompython/bin`（リストの末尾のディレクトリ）にあるPythonプログラムを見つけ、使用します。

///

/// tab | Windows

Pythonをインストールして、そのプログラムが`C:\opt\custompython\bin`というディレクトリに配置されたとします。

もし、`PATH`環境変数を更新するように答えると、`PATH`環境変数に`C:\opt\custompython\bin`が追加されます。

`PATH`環境変数は以下のように更新されるでしょう：

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

このようにして、ターミナルで`python`と入力したときに、OSは`C:\opt\custompython\bin\python`（リストの末尾のディレクトリ）にあるPythonプログラムを見つけ、使用します。

///

つまり、ターミナルで以下のコマンドを入力すると：

<div class="termy">

``` console
$ python
```

</div>

/// tab | Linux, macOS

OSは`/opt/custompython/bin`にある`python`プログラムを**見つけ**て実行します。

これは、次のコマンドを入力した場合とほとんど同等です：

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

///

/// tab | Windows

OSは`C:\opt\custompython\bin\python`にある`python`プログラムを**見つけ**て実行します。

これは、次のコマンドを入力した場合とほとんど同等です：

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

///

この情報は、[Virtual Environments](virtual-environments.md) について学ぶ際にも役立ちます。

## まとめ

これで、**環境変数**とは何か、Pythonでどのように使用するかについて、基本的な理解が得られたはずです。

環境変数についての詳細は、<a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia: Environment Variable</a> を参照してください。

環境変数の用途や適用方法が最初は直感的ではないかもしれませんが、開発中のさまざまなシナリオで繰り返し登場します。そのため、基本を知っておくことが重要です。

たとえば、この情報は次のセクションで扱う[Virtual Environments](virtual-environments.md)にも関連します。
