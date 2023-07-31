# Глобальные Зависимости

Для некоторых типов приложений может потребоваться добавить зависимости ко всему приложению.

Подобно тому, как вы можете [добавлять `dependencies` к *декораторам путевых операций*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank}, вы можете добавить их через приложение `FastAPI`.

В этом случае они будут применяться ко всем *путевым операциям* в приложении:

=== "Python 3.9+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/dependencies/tutorial012_an.py!}
    ```

=== "Python 3.6 non-Annotated"

    !!! tip "Подсказка"
        Рекомендуется использовать 'Annotated' версию, если это возможно.

    ```Python hl_lines="15"
    {!> ../../../docs_src/dependencies/tutorial012.py!}
    ```

Все способы [добавления `dependencies` к *декораторам путевых операций*](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} по-прежнему применимы, но в данном случае зависимости применяются ко всем *путевым операциям* приложения.

## Зависимости для групп *путевых операций*

Позднее, читая о том как структурировать большие приложения([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}), состоящие из большого количества файлов, вы узнаете как объявить один параметр `dependencies` для целой группы *путевых операций*.
