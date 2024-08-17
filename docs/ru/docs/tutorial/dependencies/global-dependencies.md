# Глобальные зависимости

Для некоторых типов приложений может потребоваться добавить зависимости ко всему приложению.

Подобно тому, как вы можете [добавлять зависимости через параметр `dependencies` в *декораторах операций пути*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, вы можете добавлять зависимости сразу ко всему `FastAPI` приложению.

В этом случае они будут применяться ко всем *операциям пути* в приложении:

//// tab | Python 3.9+

```Python hl_lines="16"
{!> ../../../docs_src/dependencies/tutorial012_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="16"
{!> ../../../docs_src/dependencies/tutorial012_an.py!}
```

////

//// tab | Python 3.8 non-Annotated

/// tip | "Подсказка"

Рекомендуется использовать 'Annotated' версию, если это возможно.

///

```Python hl_lines="15"
{!> ../../../docs_src/dependencies/tutorial012.py!}
```

////

Все способы [добавления зависимостей в *декораторах операций пути*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} по-прежнему применимы, но в данном случае зависимости применяются ко всем *операциям пути* приложения.

## Зависимости для групп *операций пути*

Позднее, читая о том, как структурировать более крупные [приложения, содержащие много файлов](../../tutorial/bigger-applications.md){.internal-link target=_blank}, вы узнаете, как объявить один параметр dependencies для целой группы *операций пути*.
