# 進階 Python 型別 { #advanced-python-types }

以下是一些在使用 Python 型別時可能有用的額外想法。

## 使用 `Union` 或 `Optional` { #using-union-or-optional }

如果你的程式碼因某些原因無法使用 `|`，例如不是在型別註記中，而是在像 `response_model=` 之類的參數位置，那麼你可以用 `typing` 中的 `Union` 來取代豎線（`|`）。

例如，你可以宣告某個值可以是 `str` 或 `None`：

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

在 `typing` 中也有用 `Optional` 宣告某個值可以是 `None` 的速記法。

以下是我個人（非常主觀）的建議：

* 🚨 避免使用 `Optional[SomeType]`
* 改為 ✨ 使用 `Union[SomeType, None]` ✨。

兩者等價且底層相同，但我會推薦用 `Union` 而不要用 `Optional`，因為「optional」這個詞看起來會讓人以為這個值是可選的，但實際上它的意思是「可以是 `None`」，即使它不是可選的、仍然是必填。

我認為 `Union[SomeType, None]` 更能清楚表達其含義。

這只是措辭與命名問題，但這些詞會影響你與團隊成員對程式碼的理解。

例如，看看下面這個函式：

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

參數 `name` 被標註為 `Optional[str]`，但它並不是可選的；你不能在沒有該參數的情況下呼叫這個函式：

```Python
say_hi()  # 糟了，這會拋出錯誤！😱
```

參數 `name` 仍是必填（不是可選），因為它沒有預設值。不過，`name` 可以接受 `None` 作為值：

```Python
say_hi(name=None)  # 這可行，None 是有效的 🎉
```

好消息是，多數情況下你可以直接用 `|` 來定義型別聯集：

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

因此，通常你不必為 `Optional` 與 `Union` 這些名稱操心。😎
