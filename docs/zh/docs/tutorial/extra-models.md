# 更多模型 { #extra-models }

书接上文，多个关联模型这种情况很常见。

特别是用户模型，因为：

* **输入模型**需要能够包含密码。
* **输出模型**不应包含密码。
* **数据库模型**很可能需要包含哈希后的密码。

/// danger | 危险

千万不要存储用户的明文密码。始终存储可以进行验证的“安全哈希值”。

如果不了解，你会在[安全性章节](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}中学习什么是“密码哈希”。

///

## 多个模型 { #multiple-models }

下面的代码展示了不同模型处理密码字段的方式，及使用位置的大致思路：

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### 关于 `**user_in.model_dump()` { #about-user-in-model-dump }

#### Pydantic 的 `.model_dump()` { #pydantics-model-dump }

`user_in` 是类 `UserIn` 的 Pydantic 模型。

Pydantic 模型有一个 `.model_dump()` 方法，它会返回一个包含模型数据的 `dict`。

因此，如果我们像下面这样创建一个 Pydantic 对象 `user_in`：

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

然后调用：

```Python
user_dict = user_in.model_dump()
```

现在，我们在变量 `user_dict` 中得到了一个包含数据的 `dict`（它是 `dict`，而不是 Pydantic 模型对象）。

如果我们调用：

```Python
print(user_dict)
```

会得到一个 Python `dict`：

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 解包 `dict` { #unpacking-a-dict }

如果我们拿到一个像 `user_dict` 这样的 `dict`，并用 `**user_dict` 把它传给一个函数（或类），Python 会“解包”它。它会把 `user_dict` 的键和值直接作为键值参数传递。

因此，接着上面的 `user_dict` 继续编写如下代码：

```Python
UserInDB(**user_dict)
```

结果等价于：

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

或者更准确地说，直接使用 `user_dict`，并且无论它将来可能包含什么内容：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 从另一个模型的内容创建 Pydantic 模型 { #a-pydantic-model-from-the-contents-of-another }

如上例所示，我们从 `user_in.model_dump()` 得到了 `user_dict`，这段代码：

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

等价于：

```Python
UserInDB(**user_in.model_dump())
```

...因为 `user_in.model_dump()` 是一个 `dict`，而我们在把它传给 `UserInDB` 时加上了 `**` 前缀，让 Python 对它进行“解包”。

因此，我们就能用另一个 Pydantic 模型中的数据得到一个 Pydantic 模型。

#### 解包 `dict` 并添加额外关键字参数 { #unpacking-a-dict-and-extra-keywords }

然后再添加额外的关键字参数 `hashed_password=hashed_password`，就像：

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...最终就类似于：

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

辅助的附加函数 `fake_password_hasher` 和 `fake_save_user` 只是为了演示一种可能的数据流，但它们当然不会提供任何真正的安全性。

///

## 减少重复 { #reduce-duplication }

减少代码重复是 **FastAPI** 的核心思想之一。

因为代码重复会增加 bug、安全问题、代码失步问题（在一个地方更新了但其它地方没有更新）等的概率。

而这些模型共享了很多数据，并重复了属性名和类型。

我们可以做得更好。

我们可以声明一个 `UserBase` 模型，作为其它模型的基类。然后基于它创建子类，这些子类会继承它的属性（类型声明、校验等）。

所有数据转换、校验、文档等仍将照常工作。

这样，我们就只需要声明模型之间的差异部分（包含明文 `password`、包含 `hashed_password`、以及不包含密码）：

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 或 `anyOf` { #union-or-anyof }

你可以把响应声明为两个或更多类型的 `Union`，这意味着响应可以是其中任意一种类型。

在 OpenAPI 中会用 `anyOf` 来定义。

为此，请使用 Python 标准类型提示 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>：

/// note | 注意

定义 <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> 时，先包含最具体的类型，再包含不那么具体的类型。在下面的例子中，更具体的 `PlaneItem` 在 `Union[PlaneItem, CarItem]` 里位于 `CarItem` 之前。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 中的 `Union` { #union-in-python-3-10 }

在这个例子中，我们把 `Union[PlaneItem, CarItem]` 作为参数 `response_model` 的值传入。

因为我们是把它作为**参数的值**传入，而不是放在**类型注解**里，所以即使在 Python 3.10 中也必须使用 `Union`。

如果它在类型注解中，我们就可以使用竖线，例如：

```Python
some_variable: PlaneItem | CarItem
```

但如果把它放在赋值中 `response_model=PlaneItem | CarItem`，会报错，因为 Python 会尝试在 `PlaneItem` 和 `CarItem` 之间执行一个**无效操作**，而不是将其解释为类型注解。

## 模型列表 { #list-of-models }

同样地，你也可以声明由对象列表构成的响应。

为此，请使用标准的 Python `typing.List`（或在 Python 3.9 及以上直接用 `list`）：

{* ../../docs_src/extra_models/tutorial004_py39.py hl[18] *}

## 使用任意 `dict` 的响应 { #response-with-arbitrary-dict }

你也可以使用普通的任意 `dict` 来声明响应，只声明键和值的类型，而不使用 Pydantic 模型。

当你事先不知道合法的字段/属性名（而 Pydantic 模型需要这些）时，这会很有用。

此时，可以使用 `typing.Dict`（或在 Python 3.9 及以上直接用 `dict`）：

{* ../../docs_src/extra_models/tutorial005_py39.py hl[6] *}

## 小结 { #recap }

针对每种场景都可以随意使用多个 Pydantic 模型并自由继承。

如果一个实体必须能够拥有不同的“状态”，你不需要为每个实体只设置单一的数据模型。例如，用户这个“实体”可以有包含 `password`、`password_hash` 以及不包含密码等状态。
