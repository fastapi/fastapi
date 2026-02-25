# 更多模型 { #extra-models }

书接上文，多个关联模型这种情况很常见。

特别是用户模型，因为：

* **输入模型**应该含密码
* **输出模型**不应含密码
* **数据库模型**可能需要包含哈希后的密码

/// danger | 危险

不要存储用户的明文密码。始终只存储之后可用于校验的“安全哈希”。

如果你还不了解，可以在[安全性章节](security/simple-oauth2.md#password-hashing){.internal-link target=_blank}中学习什么是“密码哈希”。

///

## 多个模型 { #multiple-models }

下面的代码展示了不同模型处理密码字段的方式，及使用位置的大致思路：

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### 关于 `**user_in.model_dump()` { #about-user-in-model-dump }

#### Pydantic 的 `.model_dump()` { #pydantics-model-dump }

`user_in` 是类 `UserIn` 的 Pydantic 模型。

Pydantic 模型有 `.model_dump()` 方法，会返回包含模型数据的 `dict`。

因此，如果使用如下方式创建 Pydantic 对象 `user_in`：

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

就能以如下方式调用：

```Python
user_dict = user_in.model_dump()
```

现在，变量 `user_dict` 中的是包含数据的 `dict`（它是 `dict`，不是 Pydantic 模型对象）。

以如下方式调用：

```Python
print(user_dict)
```

输出的就是 Python `dict`：

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### 解包 `dict` { #unpacking-a-dict }

把 `dict`（如 `user_dict`）以 `**user_dict` 形式传递给函数（或类），Python 会执行“解包”。它会把 `user_dict` 的键和值作为关键字参数直接传递。

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

或更精准，直接使用 `user_dict`（无论它将来包含什么字段）：

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### 用另一个模型的内容生成 Pydantic 模型 { #a-pydantic-model-from-the-contents-of-another }

上例中 ，从 `user_in.model_dump()` 中得到了 `user_dict`，下面的代码：

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

等效于：

```Python
UserInDB(**user_in.model_dump())
```

……因为 `user_in.model_dump()` 是 `dict`，在传递给 `UserInDB` 时，把 `**` 加在 `user_in.model_dump()` 前，可以让 Python 进行解包。

这样，就可以用其它 Pydantic 模型中的数据生成 Pydantic 模型。

#### 解包 `dict` 并添加额外关键字参数 { #unpacking-a-dict-and-extra-keywords }

接下来，继续添加关键字参数 `hashed_password=hashed_password`，例如：

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
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

配套的辅助函数 `fake_password_hasher` 和 `fake_save_user` 仅用于演示可能的数据流，当然并不提供真实的安全性。

///

## 减少重复 { #reduce-duplication }

减少代码重复是 **FastAPI** 的核心思想之一。

代码重复会导致 bug、安全问题、代码失步等问题（更新了某个位置的代码，但没有同步更新其它位置的代码）。

上面的这些模型共享了大量数据，拥有重复的属性名和类型。

我们可以做得更好。

声明 `UserBase` 模型作为其它模型的基类。然后，用该类衍生出继承其属性（类型声明、校验等）的子类。

所有数据转换、校验、文档等功能仍将正常运行。

这样，就可以仅声明模型之间的差异部分（具有明文的 `password`、具有 `hashed_password` 以及不包括密码）：

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` 或 `anyOf` { #union-or-anyof }

响应可以声明为两个或多个类型的 `Union`，即该响应可以是这些类型中的任意一种。

在 OpenAPI 中会用 `anyOf` 表示。

为此，请使用 Python 标准类型提示 <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">`typing.Union`</a>：

/// note | 注意

定义 <a href="https://docs.pydantic.dev/latest/concepts/types/#unions" class="external-link" target="_blank">`Union`</a> 类型时，要把更具体的类型写在前面，然后是不太具体的类型。下例中，更具体的 `PlaneItem` 位于 `Union[PlaneItem, CarItem]` 中的 `CarItem` 之前。

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 中的 `Union` { #union-in-python-3-10 }

在这个示例中，我们把 `Union[PlaneItem, CarItem]` 作为参数 `response_model` 的值传入。

因为这是作为“参数的值”而不是放在“类型注解”中，所以即使在 Python 3.10 也必须使用 `Union`。

如果是在类型注解中，我们就可以使用竖线：

```Python
some_variable: PlaneItem | CarItem
```

但如果把它写成赋值 `response_model=PlaneItem | CarItem`，就会报错，因为 Python 会尝试在 `PlaneItem` 和 `CarItem` 之间执行一个“无效的运算”，而不是把它当作类型注解来解析。

## 模型列表 { #list-of-models }

同样地，你可以声明由对象列表构成的响应。

为此，请使用标准的 Python `list`：

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## 任意 `dict` 的响应 { #response-with-arbitrary-dict }

你也可以使用普通的任意 `dict` 来声明响应，只需声明键和值的类型，无需使用 Pydantic 模型。

如果你事先不知道有效的字段/属性名（Pydantic 模型需要预先知道字段）时，这很有用。

此时，可以使用 `dict`：

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## 小结 { #recap }

针对不同场景，可以随意使用不同的 Pydantic 模型并通过继承复用。

当一个实体需要具备不同的“状态”时，无需只为该实体定义一个数据模型。例如，用户“实体”就可能有包含 `password`、包含 `password_hash` 以及不含密码等多种状态。
