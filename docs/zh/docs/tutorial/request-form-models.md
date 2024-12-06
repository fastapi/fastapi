# 表单模型

您可以使用 **Pydantic 模型**在 FastAPI 中声明**表单字段**。

/// info

要使用表单，需预先安装 <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> 。

确保您创建、激活一个[虚拟环境](../virtual-environments.md){.internal-link target=_blank}后再安装。

```console
$ pip install python-multipart
```

///

/// note

自 FastAPI 版本 `0.113.0` 起支持此功能。🤓

///

## 表单的 Pydantic 模型

您只需声明一个 **Pydantic 模型**，其中包含您希望接收的**表单字段**，然后将参数声明为 `Form` :

{* ../../docs_src/request_form_models/tutorial001_an_py39.py hl[9:11,15] *}

**FastAPI** 将从请求中的**表单数据**中**提取**出**每个字段**的数据，并提供您定义的 Pydantic 模型。

## 检查文档

您可以在文档 UI 中验证它，地址为 `/docs` ：

<div class="screenshot">
<img src="/img/tutorial/request-form-models/image01.png">
</div>

## 禁止额外的表单字段

在某些特殊使用情况下（可能并不常见），您可能希望将表单字段**限制**为仅在 Pydantic 模型中声明过的字段，并**禁止**任何**额外**的字段。

/// note

自 FastAPI 版本 `0.114.0` 起支持此功能。🤓

///

您可以使用 Pydantic 的模型配置来禁止（ `forbid` ）任何额外（ `extra` ）字段：

{* ../../docs_src/request_form_models/tutorial002_an_py39.py hl[12] *}

如果客户端尝试发送一些额外的数据，他们将收到**错误**响应。

例如，如果客户端尝试发送这样的表单字段：

* `username`: `Rick`
* `password`: `Portal Gun`
* `extra`: `Mr. Poopybutthole`

他们将收到一条错误响应，表明字段 `extra` 是不被允许的：

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["body", "extra"],
            "msg": "Extra inputs are not permitted",
            "input": "Mr. Poopybutthole"
        }
    ]
}
```

## 总结

您可以使用 Pydantic 模型在 FastAPI 中声明表单字段。😎
