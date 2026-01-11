# Класи як залежності { #classes-as-dependencies }

Перш ніж занурюватися глибше в систему **Dependency Injection**, покращімо попередній приклад.

## `dict` з попереднього прикладу { #a-dict-from-the-previous-example }

У попередньому прикладі ми повертали `dict` з нашої залежності («dependable»):

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Але потім ми отримуємо `dict` у параметрі `commons` *функції операції шляху*.

І ми знаємо, що редактори не можуть надати багато підтримки (як-от автодоповнення) для `dict`, бо вони не знають його ключів і типів значень.

Можна зробити краще...

## Що робить щось залежністю { #what-makes-a-dependency }

Досі ви бачили залежності, оголошені як функції.

Але це не єдиний спосіб оголошувати залежності (хоча, ймовірно, найпоширеніший).

Ключовий фактор — залежність має бути «callable».

«**callable**» у Python — це будь-що, що Python може «викликати» як функцію.

Тобто, якщо у вас є об’єкт `something` (який може _не_ бути функцією) і ви можете «викликати» його (виконати) так:

```Python
something()
```

або

```Python
something(some_argument, some_keyword_argument="foo")
```

то це «callable».

## Класи як залежності { #classes-as-dependencies_1 }

Ви могли помітити, що для створення екземпляра класу Python використовується той самий синтаксис.

Наприклад:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

У цьому випадку `fluffy` — екземпляр класу `Cat`.

А щоб створити `fluffy`, ви «викликаєте» `Cat`.

Отже, клас Python також є **callable**.

Тоді у **FastAPI** ви можете використати клас Python як залежність.

Насправді FastAPI перевіряє, що це «callable» (функція, клас або щось інше) і які параметри визначені.

Якщо ви передасте «callable» як залежність у **FastAPI**, він проаналізує параметри цього «callable» і обробить їх так само, як параметри *функції операції шляху*. Включно з підзалежностями.

Це також стосується callables взагалі без параметрів. Так само, як і для *функцій операції шляху* без параметрів.

Тож ми можемо змінити залежність «dependable» `common_parameters` з прикладу вище на клас `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Зверніть увагу на метод `__init__`, який використовується для створення екземпляра класу:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

...він має ті самі параметри, що й наш попередній `common_parameters`:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Саме ці параметри **FastAPI** використає, щоб «розв’язати» залежність.

В обох випадках буде:

* Необов’язковий query-параметр `q`, який є `str`.
* Query-параметр `skip`, який є `int`, зі значенням за замовчуванням `0`.
* Query-параметр `limit`, який є `int`, зі значенням за замовчуванням `100`.

В обох випадках дані буде перетворено, валідовано, задокументовано в схемі OpenAPI тощо.

## Використайте це { #use-it }

Тепер ви можете оголосити вашу залежність, використовуючи цей клас.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** викликає клас `CommonQueryParams`. Це створює «екземпляр» цього класу, і екземпляр буде передано як параметр `commons` у вашу функцію.

## Анотація типу vs `Depends` { #type-annotation-vs-depends }

Зверніть увагу, що в коді вище ми пишемо `CommonQueryParams` двічі:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

Останній `CommonQueryParams` у:

```Python
... Depends(CommonQueryParams)
```

...це те, що **FastAPI** фактично використає, щоб зрозуміти, що є залежністю.

Саме з нього FastAPI витягне оголошені параметри і саме його FastAPI реально викличе.

---

У цьому випадку перший `CommonQueryParams` у:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons: CommonQueryParams ...
```

////

...не має жодного спеціального значення для **FastAPI**. FastAPI не використовуватиме його для перетворення даних, валідації тощо (оскільки для цього він використовує `Depends(CommonQueryParams)`).

Ви фактично могли б написати просто:

//// tab | Python 3.9+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons = Depends(CommonQueryParams)
```

////

...як тут:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Але оголошувати тип заохочується, адже так ваш редактор знатиме, що буде передано як параметр `commons`, і зможе допомогти вам з автодоповненням коду, перевірками типів тощо:

<img src="/img/tutorial/dependencies/image02.png">

## Скорочення { #shortcut }

Але ви бачите, що тут є повторення коду — ми пишемо `CommonQueryParams` двічі:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** надає скорочення для таких випадків, коли залежність *саме* є класом, який **FastAPI** «викликає», щоб створити екземпляр цього класу.

Для цих конкретних випадків ви можете зробити таке:

Замість того, щоб писати:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

...ви пишете:

//// tab | Python 3.9+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.9+ без Annotated

/// tip | Порада

За можливості надавайте перевагу варіанту з `Annotated`.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Ви оголошуєте залежність як тип параметра і використовуєте `Depends()` без жодного параметра, замість того щоб писати повний клас *ще раз* всередині `Depends(CommonQueryParams)`.

Тоді цей самий приклад виглядатиме так:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

...і **FastAPI** знатиме, що робити.

/// tip | Порада

Якщо це здається вам більш заплутаним, ніж корисним, просто ігноруйте це — вам це *не* потрібно.

Це лише скорочення. Адже **FastAPI** прагне допомогти вам мінімізувати повторення коду.

///
