# 高度な Python の型 { #advanced-python-types }

Python の型を扱うときに役立つ追加のアイデアをいくつか紹介します。

## `Union` または `Optional` の利用 { #using-union-or-optional }

何らかの理由で `|` が使えない場合、たとえば型アノテーションではなく `response_model=` のような場所では、縦棒（`|`）の代わりに `typing` の `Union` を使えます。

例えば、`str` または `None` になり得ることを宣言できます:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` には、`None` を取り得ることを宣言するための短縮形として `Optional` もあります。

ここからは私のとても主観的な提案です:

- 🚨 `Optional[SomeType]` の使用は避けましょう
- 代わりに ✨ **`Union[SomeType, None]` を使いましょう** ✨。

どちらも等価で内部的には同一ですが、「optional（任意）」という語が値が任意だと誤解させやすく、実際の意味は「`None` を取り得る」であり、任意ではなく依然として必須である場合でもそうです。そのため `Optional` より `Union` を勧めます。

`Union[SomeType, None]` の方が意味がより明確だと思います。

これは用語や名前付けの話に過ぎませんが、その言葉があなたやチームメイトのコードの捉え方に影響します。

例として次の関数を見てみましょう:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

パラメータ `name` は `Optional[str]` と定義されていますが、任意ではありません。このパラメータなしで関数を呼び出すことはできません:

```Python
say_hi()  # あっ、これはエラーになります！😱
```

`name` パラメータにはデフォルト値がないため、依然として必須（任意ではない）です。ただし、`name` は値として `None` を受け付けます:

```Python
say_hi(name=None)  # これは動作します。None は有効です 🎉
```

朗報として、多くの場合は単純に `|` を使って型の Union を定義できます:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

したがって、通常は `Optional` や `Union` といった名前を気にする必要はありません。😎
