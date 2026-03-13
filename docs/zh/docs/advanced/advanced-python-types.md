# 高级 Python 类型 { #advanced-python-types }

这里有一些在使用 Python 类型时可能有用的额外想法。

## 使用 `Union` 或 `Optional` { #using-union-or-optional }

如果你的代码因为某些原因不能使用 `|`，例如它不是在类型注解里，而是在 `response_model=` 之类的参数中，那么你可以使用 `typing` 中的 `Union` 来代替竖线（`|`）。

例如，你可以声明某个值可以是 `str` 或 `None`：

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` 也提供了一个声明“可能为 `None`”的快捷方式：`Optional`。

从我非常主观的角度给个小建议：

- 🚨 避免使用 `Optional[SomeType]`
- 改用 ✨`Union[SomeType, None]`✨。

两者是等价的，底层其实也是一样的。但我更推荐使用 `Union` 而不是 `Optional`，因为单词“optional”（可选）看起来会暗示该值是可选的，而它真正的含义是“它可以是 `None`”，即使它并不是可选的，仍然是必填的。

我认为 `Union[SomeType, None]` 更能明确表达其含义。

这只是关于词语和命名的问题，但这些词语会影响你和你的队友如何看待代码。

举个例子，看这段函数：

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

参数 `name` 被定义为 `Optional[str]`，但它并不是“可选”的，你不能不传这个参数就调用函数：

```Python
say_hi()  # 哎呀，这会报错！😱
```

参数 `name` 仍然是必填的（不是“可选”），因为它没有默认值。不过，`name` 接受 `None` 作为取值：

```Python
say_hi(name=None)  # 这样可以，None 是有效的 🎉
```

好消息是，在大多数情况下，你可以直接使用 `|` 来定义类型联合：

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

因此，通常你不必为像 `Optional` 和 `Union` 这样的名字而操心。😎
