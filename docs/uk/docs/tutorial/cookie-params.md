# Параметри Cookie

Ви можете визначити параметри Cookie таким же чином, як визначаються параметри `Query` і `Path`.

## Імпорт `Cookie`

Спочатку імпортуйте `Cookie`:

=== "Python 3.10+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="1"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="3"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

## Визначення параметрів `Cookie`

Потім визначте параметри cookie, використовуючи таку ж конструкцію як для `Path` і `Query`.

Перше значення це значення за замовчуванням, ви можете також передати всі додаткові параметри валідації чи анотації:

=== "Python 3.10+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/cookie_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="7"
    {!> ../../../docs_src/cookie_params/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! tip
        Бажано використовувати `Annotated` версію, якщо це можливо.

    ```Python hl_lines="9"
    {!> ../../../docs_src/cookie_params/tutorial001.py!}
    ```

!!! note "Технічні Деталі"
    `Cookie` це "сестра" класів `Path` і `Query`. Вони наслідуються від одного батьківського класу `Param`.
    Але пам'ятайте, що коли ви імпортуєте `Query`, `Path`, `Cookie` та інше з `fastapi`, це фактично функції, що повертають спеціальні класи.

!!! info
    Для визначення cookies ви маєте використовувати `Cookie`, тому що в іншому випадку параметри будуть інтерпритовані, як параметри запиту.

## Підсумки

Визначайте cookies за допомогою `Cookie`, використовуючи той же спільний шаблон, що і `Query` та `Path`.
