# Gelişmiş Python Tipleri { #advanced-python-types }

Python tipleriyle çalışırken işinize yarayabilecek bazı ek fikirler.

## `Union` veya `Optional` Kullanımı { #using-union-or-optional }

Kodunuz herhangi bir nedenle `|` kullanamıyorsa — örneğin bir tip açıklamasında (type annotation) değil de `response_model=` gibi bir yerdeyse — dikey çizgi (`|`) yerine `typing` içindeki `Union`'ı kullanabilirsiniz.

Örneğin, bir şeyin `str` ya da `None` olabileceğini şöyle belirtebilirsiniz:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing`, bir şeyin `None` olabileceğini belirtmek için `Optional` ile bir kısayol da sunar.

Benim oldukça öznel bakış açıma göre küçük bir ipucu:

- 🚨 `Optional[SomeType]` kullanmaktan kaçının
- Bunun yerine ✨ **`Union[SomeType, None]` kullanın** ✨.

İkisi de eşdeğer ve temelde aynıdır; ancak "**optional**" kelimesi değerin isteğe bağlı olduğunu ima eder. Oysa aslında " `None` olabilir" demektir; değer isteğe bağlı olmasa ve hâlâ zorunlu olsa bile.

Bence `Union[SomeType, None]` ne demek istediğini daha açık anlatır.

Burada mesele sadece kelimeler ve isimler. Ancak bu kelimeler sizin ve ekip arkadaşlarınızın koda bakışını etkileyebilir.

Örnek olarak şu fonksiyona bakalım:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

`name` parametresi `Optional[str]` olarak tanımlıdır; ancak isteğe bağlı değildir, parametre olmadan fonksiyonu çağıramazsınız:

```Python
say_hi()  # Ah hayır, bu hata fırlatır! 😱
```

`name` parametresi varsayılan bir değeri olmadığı için hâlâ zorunludur (yani *optional* değildir). Yine de `name`, değer olarak `None` kabul eder:

```Python
say_hi(name=None)  # Bu çalışır, None geçerlidir 🎉
```

İyi haber şu ki, çoğu durumda tip birliklerini (union) tanımlamak için doğrudan `|` kullanabilirsiniz:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

Dolayısıyla, normalde `Optional` ve `Union` gibi isimler için endişelenmenize gerek yok. 😎
