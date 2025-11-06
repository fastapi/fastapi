# Глобальные зависимости { #global-dependencies }

Для некоторых типов приложений может потребоваться добавить зависимости ко всему приложению.

Подобно тому, как вы можете [добавлять `dependencies` (зависимости) в *декораторах операций пути*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, вы можете добавлять зависимости сразу ко всему `FastAPI` приложению.

В этом случае они будут применяться ко всем *операциям пути* в приложении:

{* ../../docs_src/dependencies/tutorial012_an_py39.py hl[16] *}

Все способы [добавления `dependencies` (зависимостей) в *декораторах операций пути*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} по-прежнему применимы, но в данном случае зависимости применяются ко всем *операциям пути* приложения.

## Зависимости для групп *операций пути* { #dependencies-for-groups-of-path-operations }

Позднее, читая о том, как структурировать более крупные [приложения, содержащие много файлов](../../tutorial/bigger-applications.md){.internal-link target=_blank}, вы узнаете, как объявить один параметр `dependencies` для целой группы *операций пути*.
