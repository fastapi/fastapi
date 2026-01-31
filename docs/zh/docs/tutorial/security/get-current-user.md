# 获取当前用户 { #get-current-user }

在上一章中，安全系统（基于依赖注入系统）向*路径操作函数*传递了一个 `str` 类型的 `token`：

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

但这仍然不是很有用。

让它给我们提供当前用户吧。

## 创建用户模型 { #create-a-user-model }

首先，创建一个 Pydantic 用户模型。

就像我们使用 Pydantic 声明请求体一样，我们也可以在任何其他地方使用它：

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## 创建 `get_current_user` 依赖项 { #create-a-get-current-user-dependency }

让我们创建一个依赖项 `get_current_user`。

还记得依赖项可以有子依赖项吗？

`get_current_user` 将拥有一个依赖项，使用我们之前创建的同一个 `oauth2_scheme`。

和之前我们在*路径操作*中直接做的一样，我们新的依赖项 `get_current_user` 将从子依赖项 `oauth2_scheme` 接收一个 `str` 类型的 `token`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## 获取用户 { #get-the-user }

`get_current_user` 将使用我们创建的（伪）工具函数，该函数接收一个 `str` 类型的 token，并返回我们的 Pydantic `User` 模型：

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## 注入当前用户 { #inject-the-current-user }

所以现在，我们可以在*路径操作*中使用同样的 `Depends`，配合 `get_current_user`：

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

注意，我们将 `current_user` 的类型声明为 Pydantic 模型 `User`。

这将帮助我们在函数内部获得代码补全和类型检查。

/// tip | 提示

你可能还记得，请求体也是用 Pydantic 模型声明的。

这里因为你使用了 `Depends`，所以 **FastAPI** 不会搞混。

///

/// check

这个依赖系统的设计方式允许我们拥有不同的依赖项（不同的“可依赖对象”），它们都返回一个 `User` 模型。

我们并不局限于只能有一个依赖项返回那种类型的数据。

///

## 其他模型 { #other-models }

你现在可以直接在*路径操作函数*中获取当前用户，并使用 `Depends` 在 **Dependency Injection** 层面处理安全机制。

并且你可以为安全需求使用任何模型或数据（本例中是一个 Pydantic 模型 `User`）。

但你并不局限于使用某个特定的数据模型、类或类型。

你想在模型中有 `id` 和 `email`，而不包含 `username` 吗？当然可以。你可以使用同样的工具。

你只想用一个 `str`？或者只用一个 `dict`？或者直接用一个数据库类模型实例？工作方式都一样。

实际上，你的应用里登录的不是用户，而是机器人、bot 或其他系统，它们只有一个访问令牌？同样，一切照常工作。

只要使用你的应用所需的任何类型的模型、任何类型的类、任何类型的数据库即可。**FastAPI** 会通过依赖注入系统为你搞定。

## 代码大小 { #code-size }

这个示例看起来可能有些冗长。请记住，我们在同一个文件里混合了安全、数据模型、工具函数以及*路径操作*。

但关键点在这里。

安全和依赖注入的内容只需要写一次。

并且你可以让它变得任意复杂。仍然只需要在一个位置写一次，且具有所有的灵活性。

但你可以有成千上万个端点（*路径操作*）使用同一个安全系统。

并且它们全部（或其中你想要的任何部分）都可以利用复用这些依赖项或你创建的任何其他依赖项。

而这成千上万个*路径操作*都可以小到只有 3 行：

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## 小结 { #recap }

你现在可以直接在你的*路径操作函数*中获取当前用户。

我们已经完成一半了。

我们只需要再添加一个*路径操作*，让用户/客户端真正发送 `username` 和 `password`。

接下来就是这个。
