# 开发 - 贡献

首先，你可能想了解 [帮助 FastAPI 及获取帮助](help-fastapi.md){.internal-link target=_blank}的基本方式。

## 开发

如果你已经克隆了源码仓库，并且需要深入研究代码，下面是设置开发环境的指南。

### 通过 `venv` 管理虚拟环境

你可以使用 Python 的 `venv` 模块在一个目录中创建虚拟环境：

<div class="termy">

```console
$ python -m venv env
```

</div>

这将使用 Python 程序创建一个 `./env/` 目录，然后你将能够为这个隔离的环境安装软件包。

### 激活虚拟环境

使用以下方法激活新环境：

//// tab | Linux, macOS

<div class="termy">

```console
$ source ./env/bin/activate
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ .\env\Scripts\Activate.ps1
```

</div>

////

//// tab | Windows Bash

Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

<div class="termy">

```console
$ source ./env/Scripts/activate
```

</div>

////

要检查操作是否成功，运行：

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
$ which pip

some/directory/fastapi/env/bin/pip
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
$ Get-Command pip

some/directory/fastapi/env/bin/pip
```

</div>

////

如果显示 `pip` 程序文件位于 `env/bin/pip` 则说明激活成功。 🎉

确保虚拟环境中的 pip 版本是最新的，以避免后续步骤出现错误：

<div class="termy">

```console
$ python -m pip install --upgrade pip

---> 100%
```

</div>

/// tip

每一次你在该环境下使用 `pip` 安装了新软件包时，请再次激活该环境。

这样可以确保你在使用由该软件包安装的终端程序时使用的是当前虚拟环境中的程序，而不是其他的可能是全局安装的程序。

///

### pip

如上所述激活环境后：

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

这将在虚拟环境中安装所有依赖和本地版本的 FastAPI。

#### 使用本地 FastAPI

如果你创建一个导入并使用 FastAPI 的 Python 文件，然后使用虚拟环境中的 Python 运行它，它将使用你本地的 FastAPI 源码。

并且如果你更改该本地 FastAPI 的源码，由于它是通过 `-e` 安装的，当你再次运行那个 Python 文件，它将使用你刚刚编辑过的最新版本的 FastAPI。

这样，你不必再去重新"安装"你的本地版本即可测试所有更改。

/// note | "技术细节"

仅当你使用此项目中的 `requirements.txt` 安装而不是直接使用 `pip install fastapi` 安装时，才会发生这种情况。

这是因为在 `requirements.txt` 中，本地的 FastAPI 是使用“可编辑” （`-e`）选项安装的

///

### 格式化

你可以运行下面的脚本来格式化和清理所有代码：

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

它还会自动对所有导入代码进行排序整理。

为了使整理正确进行，你需要在当前环境中安装本地的 FastAPI，即在运行上述段落中的命令时添加 `-e`。

## 文档

首先，请确保按上述步骤设置好环境，这将安装所有需要的依赖。

### 实时文档

在本地开发时，可以使用该脚本构建站点并检查所做的任何更改，并实时重载：

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

文档服务将运行在 `http://127.0.0.1:8008`。

这样，你可以编辑文档 / 源文件并实时查看更改。

/// tip

或者你也可以手动执行和该脚本一样的操作

进入语言目录，如果是英文文档，目录则是 `docs/en/`:

```console
$ cd docs/en/
```

在该目录执行 `mkdocs` 命令

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer CLI （可选）

本指引向你展示了如何直接用 `python` 运行 `./scripts/docs.py` 中的脚本。

但你也可以使用 <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>，而且在安装了补全功能后，你将可以在终端中对命令进行自动补全。

如果你已经安装 Typer CLI ，则可以使用以下命令安装自动补全功能：

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### 文档架构

文档使用 <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a> 生成。

在 `./scripts/docs.py` 中还有额外工具 / 脚本来处理翻译。

/// tip

你不需要去了解 `./scripts/docs.py` 中的代码，只需在命令行中使用它即可。

///

所有文档均在 `./docs/en/` 目录中以 Markdown 文件格式保存。

许多的教程中都有一些代码块，大多数情况下，这些代码是可以直接运行的，因为这些代码不是写在 Markdown 文件里的，而是写在 `./docs_src/` 目录中的 Python 文件里。

在生成站点的时候，这些 Python 文件会被打包进文档中。

### 测试文档

大多数的测试实际上都是针对文档中的示例源文件运行的。

这有助于确保：

* 文档始终是最新的。
* 文档示例可以直接运行。
* 绝大多数特性既在文档中得以阐述，又通过测试覆盖进行保障。


### 应用和文档同时运行

如果你使用以下方式运行示例程序：

<div class="termy">

```console
$ uvicorn tutorial001:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

由于 Uvicorn 默认使用 `8000` 端口 ，因此运行在 `8008` 端口上的文档不会与之冲突。

### 翻译

**非常感谢**你能够参与文档的翻译！这项工作需要社区的帮助才能完成。 🌎 🚀

以下是参与帮助翻译的步骤。

#### 建议和指南

* 在当前 <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">已有的 pull requests</a> 中查找你使用的语言，添加要求修改或同意合并的评审意见。

/// tip

你可以为已有的 pull requests <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">添加包含修改建议的评论</a>。

详情可查看关于 <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">添加 pull request 评审意见</a> 以同意合并或要求修改的文档。

///

* 检查在 <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussion</a> 是否有关于你所用语言的协作翻译。 如果有，你可以订阅它，当有一条新的 PR 请求需要评审时，系统会自动将其添加到讨论中，你也会收到对应的推送。

* 每翻译一个页面新增一个 pull request。这将使其他人更容易对其进行评审。

对于我（译注：作者使用西班牙语和英语）不懂的语言，我将在等待其他人评审翻译之后将其合并。

* 你还可以查看是否有你所用语言的翻译，并对其进行评审，这将帮助我了解翻译是否正确以及能否将其合并。
    * 可以在 <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussions</a> 中查看。
    * 也可以在现有 PR 中通过你使用的语言标签来筛选对应的 PR，举个例子，对于西班牙语，标签是 <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3A%22awaiting+review%22" class="external-link" target="_blank">`lang-es`</a>。

* 请使用相同的 Python 示例，且只需翻译文档中的文本，不用修改其它东西。

* 请使用相同的图片、文件名以及链接地址，不用修改其它东西。

* 你可以从 <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">ISO 639-1 代码列表</a> 表中查找你想要翻译语言的两位字母代码。

#### 已有的语言

假设你想将某个页面翻译成已经翻译了一些页面的语言，例如西班牙语。

对于西班牙语来说，它的两位字母代码是 `es`。所以西班牙语翻译的目录位于 `docs/es/`。

/// tip

默认语言是英语，位于 `docs/en/`目录。

///

现在为西班牙语文档运行实时服务器：

<div class="termy">

```console
// Use the command "live" and pass the language code as a CLI argument
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

/// tip

或者你也可以手动执行和该脚本一样的操作

进入语言目录，对于西班牙语的翻译，目录是 `docs/es/`:

```console
$ cd docs/es/
```

在该目录执行 `mkdocs` 命令

```console
$ mkdocs serve --dev-addr 8008
```

///

现在你可以访问 <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> 实时查看你所做的更改。

如果你查看 FastAPI 的线上文档网站，会看到每种语言都有所有的文档页面，但是某些页面并未被翻译并且会有一处关于缺少翻译的提示。（但是当你像上面这样在本地运行文档时，你只会看到已经翻译的页面。）

现在假设你要为 [Features](features.md){.internal-link target=_blank} 章节添加翻译。

* 复制下面的文件：

```
docs/en/docs/features.md
```

* 粘贴到你想要翻译语言目录的相同位置，比如：

```
docs/es/docs/features.md
```

/// tip

注意路径和文件名的唯一变化是语言代码，从 `en` 更改为 `es`。

///

回到浏览器你就可以看到刚刚更新的章节了。🎉

现在，你可以翻译这些内容并在保存文件后进行预览。

#### 新语言

假设你想要为尚未有任何页面被翻译的语言添加翻译。

假设你想要添加克里奥尔语翻译，而且文档中还没有该语言的翻译。

点击上面提到的“ISO 639-1 代码列表”链接，可以查到“克里奥尔语”的代码为 `ht`。

下一步是运行脚本以生成新的翻译目录：

<div class="termy">

```console
// Use the command new-lang, pass the language code as a CLI argument
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

现在，你可以在编辑器中查看新创建的目录 `docs/ht/`。

这条命令会生成一个从 `en` 版本继承了所有属性的配置文件 `docs/ht/mkdocs.yml`:

```yaml
INHERIT: ../en/mkdocs.yml
```

/// tip

你也可以自己手动创建包含这些内容的文件。

///

这条命令还会生成一个文档主页 `docs/ht/index.md`，你可以从这个文件开始翻译。

然后，你可以根据上面的"已有语言"的指引继续进行翻译。

翻译完成后，你就可以用 `docs/ht/mkdocs.yml` 和 `docs/ht/index.md` 发起 PR 了。🎉

#### 预览结果

你可以执行 `./scripts/docs.py live` 命令来预览结果（或者 `mkdocs serve`）。

但是当你完成翻译后，你可以像在线上展示一样测试所有内容，包括所有其他语言。

为此，首先构建所有文档：

<div class="termy">

```console
// Use the command "build-all", this will take a bit
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

这样会对每一种语言构建一个独立的文档站点，并最终把这些站点全部打包输出到 `./site/` 目录。



然后你可以使用命令 `serve` 来运行生成的站点：

<div class="termy">

```console
// Use the command "serve" after running "build-all"
$ python ./scripts/docs.py serve

Warning: this is a very simple server. For development, use mkdocs serve instead.
This is here only to preview a site with translations already built.
Make sure you run the build-all command first.
Serving at: http://127.0.0.1:8008
```

</div>

## 测试

你可以在本地运行下面的脚本来测试所有代码并生成 HTML 格式的覆盖率报告：

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

该命令生成了一个 `./htmlcov/` 目录，如果你在浏览器中打开 `./htmlcov/index.html` 文件，你可以交互式地浏览被测试所覆盖的代码区块，并注意是否缺少了任何区块。
