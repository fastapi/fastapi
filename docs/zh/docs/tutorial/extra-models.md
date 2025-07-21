# 更多模型

书接上文，多个关联模型这种情况很常见。

特别是用户模型，因为：

* **输入模型**应该含密码
* **输出模型**不应含密码
* **数据库模型**需要加密的密码

/// danger | 危险

千万不要存储用户的明文密码。始终存储可以进行验证的**安全哈希值**。

如果不了解这方面的知识，请参阅[安全性中的章节](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}，了解什么是**密码哈希**。

///

## 多个模型

下面的代码展示了不同模型处理密码字段的方式，及使用位置的大致思路：

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### `**user_in.dict()` 简介

#### Pydantic 的 `.dict()`

`user_in` 是类 `UserIn` 的 Pydantic 模型。

Pydantic 模型支持 `.dict()` 方法，能返回包含模型数据的**字典**。

因此，如果使用如下方式创建 Pydantic 对象 `user_in`：

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

就能以如下方式调用：

```Python
user_dict = user_in.dict()
```

现在，变量 `user_dict`中的就是包含数据的**字典**（变量 `user_dict` 是字典，不是 Pydantic 模型对象）。

以如下方式调用：

```Python
print(user_dict)
```

输出的就是 Python **字典**：

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 解包 `dict`

把**字典** `user_dict` 以 `**user_dict` 形式传递给函数（或类），Python 会执行**解包**操作。它会把 `user_dict` 的键和值作为关键字参数直接传递。

因此，接着上面的 `user_dict` 继续编写如下代码：

```Python
UserInDB(**user_dict)
```

就会生成如下结果：

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

或更精准，直接把可能会用到的内容与 `user_dict` 一起使用：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 用其它模型中的内容生成 Pydantic 模型

上例中 ，从 `user_in.dict()` 中得到了 `user_dict`，下面的代码：

```Python
user_dict = user_in.dict()
UserInDB(**user_dict)
```

等效于：

```Python
UserInDB(**user_in.dict())
```

……因为 `user_in.dict()` 是字典，在传递给 `UserInDB` 时，把 `**` 加在  `user_in.dict()` 前，可以让 Python 进行**解包**。

这样，就可以用其它 Pydantic 模型中的数据生成 Pydantic 模型。

#### 解包 `dict` 和更多关键字

接下来，继续添加关键字参数 `hashed_password=hashed_password`，例如：

```Python
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

……输出结果如下：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | 警告

辅助的附加函数只是为了演示可能的数据流，但它们显然不能提供任何真正的安全机制。

///

## 减少重复

**FastAPI** 的核心思想就是减少代码重复。

代码重复会导致 bug、安全问题、代码失步等问题（更新了某个位置的代码，但没有同步更新其它位置的代码）。

上面的这些模型共享了大量数据，拥有重复的属性名和类型。

FastAPI 可以做得更好。

声明 `UserBase` 模型作为其它模型的基类。然后，用该类衍生出继承其属性（类型声明、验证等）的子类。

所有数据转换、校验、文档等功能仍将正常运行。

这样，就可以仅声明模型之间的差异部分（具有明文的 `password`、具有 `hashed_password` 以及不包括密码）。

通过这种方式，可以只声明模型之间的区别（分别包含明文密码、哈希密码，以及无密码的模型）。

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 或者 `anyOf`

响应可以声明为两种类型的 `Union` 类型，即该响应可以是两种类型中的任意类型。

在 OpenAPI 中可以使用 `anyOf` 定义。

为此，请使用 Python 标准类型提示 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>：

/// note | 笔记

定义 <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> 类型时，要把详细的类型写在前面，然后是不太详细的类型。下例中，更详细的 `PlaneItem` 位于 `Union[PlaneItem，CarItem]` 中的 `CarItem` 之前。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

## 模型列表

使用同样的方式也可以声明由对象列表构成的响应。

为此，请使用标准的 Python `typing.List`：

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}

## 任意 `dict` 构成的响应

任意的 `dict` 都能用于声明响应，只要声明键和值的类型，无需使用 Pydantic 模型。

事先不知道可用的字段 / 属性名时（Pydantic 模型必须知道字段是什么），这种方式特别有用。

此时，可以使用 `typing.Dict`：

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}

## 小结

针对不同场景，可以随意使用不同的 Pydantic 模型继承定义的基类。

实体必须具有不同的**状态**时，不必为不同状态的实体单独定义数据模型。例如，用户**实体**就有包含 `password`、包含 `password_hash` 以及不含密码等多种状态。
