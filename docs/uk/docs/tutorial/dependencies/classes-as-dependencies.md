# Класи як залежності { #classes-as-dependencies }

Перш ніж заглибитися у систему **впровадження залежностей**, оновімо попередній приклад.

## `dict` з попереднього прикладу { #a-dict-from-the-previous-example }

У попередньому прикладі ми повертали `dict` із нашого «залежного»:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[9] *}

Але тоді ми отримуємо `dict` у параметрі `commons` функції операції шляху.

І ми знаємо, що редактори не можуть надати багато підтримки (наприклад, автодоповнення) для `dict`, адже вони не знають їхніх ключів і типів значень.

Можна зробити краще…

## Що робить об’єкт залежністю { #what-makes-a-dependency }

Дотепер ви бачили залежності, оголошені як функції.

Але це не єдиний спосіб оголошувати залежності (хоча, ймовірно, найпоширеніший).

Ключовий момент у тому, що залежність має бути «викликаємим».

«Викликаємий» у Python - це будь-що, що Python може «викликати», як функцію.

Отже, якщо у вас є об’єкт `something` (який може й не бути функцією) і ви можете «викликати» його (виконати) так:

```Python
something()
```

або

```Python
something(some_argument, some_keyword_argument="foo")
```

тоді це «викликаємий».

## Класи як залежності { #classes-as-dependencies_1 }

Ви могли помітити, що для створення екземпляра класу Python ви використовуєте той самий синтаксис.

Наприклад:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

У цьому випадку `fluffy` - екземпляр класу `Cat`.

А для створення `fluffy` ви «викликаєте» `Cat`.

Отже, клас Python також є **викликаємим**.

Тож у **FastAPI** ви можете використовувати клас Python як залежність.

Насправді **FastAPI** перевіряє, що це «викликаємий» об’єкт (функція, клас чи щось інше) і які параметри в нього оголошені.

Якщо ви передаєте «викликаємий» як залежність у **FastAPI**, він проаналізує параметри цього об’єкта і обробить їх так само, як параметри для функції операції шляху. Включно з підзалежностями.

Це також стосується викликаємих без жодних параметрів. Так само, як і для функцій операцій шляху без параметрів.

Тоді ми можемо змінити залежність `common_parameters` вище на клас `CommonQueryParams`:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[11:15] *}

Зверніть увагу на метод `__init__`, який використовують для створення екземпляра класу:

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[12] *}

…він має ті самі параметри, що й наш попередній `common_parameters`:

{* ../../docs_src/dependencies/tutorial001_an_py310.py hl[8] *}

Саме ці параметри **FastAPI** використає, щоб «розв’язати» залежність.

В обох випадках буде:

- Необов’язковий параметр запиту `q`, який є `str`.
- Параметр запиту `skip`, який є `int`, зі значенням за замовчуванням `0`.
- Параметр запиту `limit`, який є `int`, зі значенням за замовчуванням `100`.

В обох випадках дані будуть перетворені, перевірені й задокументовані в схемі OpenAPI тощо.

## Використання { #use-it }

Тепер ви можете оголосити залежність, використовуючи цей клас.

{* ../../docs_src/dependencies/tutorial002_an_py310.py hl[19] *}

**FastAPI** викликає клас `CommonQueryParams`. Це створює «екземпляр» цього класу, і цей екземпляр буде передано як параметр `commons` у вашу функцію.

## Анотація типів проти `Depends` { #type-annotation-vs-depends }

Зверніть увагу, що вище ми двічі пишемо `CommonQueryParams`:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

Останній `CommonQueryParams` у:

```Python
... Depends(CommonQueryParams)
```

 - це те, що **FastAPI** фактично використає, щоб дізнатися, яка залежність.

Саме з нього **FastAPI** витягне оголошені параметри і саме його **FastAPI** буде викликати.

---

У цьому випадку перший `CommonQueryParams` у:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, ...
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons: CommonQueryParams ...
```

////

…не має жодного особливого значення для **FastAPI**. FastAPI не використовуватиме його для перетворення даних, перевірки тощо (адже для цього використовується `Depends(CommonQueryParams)`).

Насправді ви могли б написати просто:

//// tab | Python 3.10+

```Python
commons: Annotated[Any, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons = Depends(CommonQueryParams)
```

////

…як у:

{* ../../docs_src/dependencies/tutorial003_an_py310.py hl[19] *}

Але оголошувати тип рекомендується - так ваш редактор знатиме, що буде передано в параметр `commons`, і зможе допомагати з автодоповненням, перевірками типів тощо:

<img src="/img/tutorial/dependencies/image02.png">

## Скорочення { #shortcut }

Але ви бачите, що тут маємо деяке дублювання коду - `CommonQueryParams` пишемо двічі:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

**FastAPI** надає скорочення для таких випадків, коли залежність - це саме клас, який **FastAPI** «викличе», щоб створити екземпляр цього класу.

Для таких випадків ви можете зробити так:

Замість того щоб писати:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

////

…напишіть:

//// tab | Python 3.10+

```Python
commons: Annotated[CommonQueryParams, Depends()]
```

////

//// tab | Python 3.10+ без Annotated

/// tip | Порада

Надавайте перевагу варіанту з `Annotated`, якщо це можливо.

///

```Python
commons: CommonQueryParams = Depends()
```

////

Ви оголошуєте залежність як тип параметра і використовуєте `Depends()` без параметрів, замість того щоб вдруге писати повний клас усередині `Depends(CommonQueryParams)`.

Той самий приклад виглядатиме так:

{* ../../docs_src/dependencies/tutorial004_an_py310.py hl[19] *}

…і **FastAPI** знатиме, що робити.

/// tip | Порада

Якщо це здається заплутанішим, ніж корисним, просто не використовуйте це - воно не є обов’язковим.

Це лише скорочення. Адже **FastAPI** дбає про мінімізацію дублювання коду.

///
