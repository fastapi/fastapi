# Dependencies

**FastAPI** имеет очень мощную и интуитивную систему **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>**.

Она проектировалась таким образом, чтобы быть простой в использовании и облегчить любому разработчику интеграцию других компонентов с **FastAPI**.

## Что такое "Dependency Injection" (иньекция зависимости)

**"Dependency Injection"** в програмировании это означает, что у вашего кода (в данном случае, ваша *функция обработки пути*) есть способы объявить вещи которые запрашиваются для работы и использования: "dependencies".

И потом эта система (в нашем случае **FastAPI**) организует всё что требуется чтобы обеспечить ваш код этой зависимостью (сделать "иньекцию" в зависимости).

Это очень полезно когда вам нужно:

* Обеспечить общую логику (одна и таже логика кода снова и снова).
* Общее соединение с базой данных.
* Обеспечение безопастности, аутентефикации, запроса роли и т.п. 
* И много другое.

Всё из этого минимизирует повторение кода.

## Первые шаги

Давайте рассмотрим очень простой пример. Он настолько простой, что на данный момент почти бесполезный.

Но таким способом мы можем сфокусироваться на том, как же всё таки работает система **Dependency Injection**.

### Создание зависимости или "зависимого" 
Давайте для начала сфокусируемся на зависимостях.

Это просто функция которая может принимать все теже параметры, что и *функции обработки пути*:

=== "Python 3.10+"

    ```Python hl_lines="8-9"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="8-11"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="9-12"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="6-7"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! Совет
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="8-11"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

И всё.

**2 строчки**.

И теперь она той же формы и структуры что и все ваши *функции обработки пути*. 

Вы можете думать об *функции обработки пути* как о функции без "декоратора" (без `@app.get("/some-path")`).

И она может возвращать всё что требуется.

В этом случае, эта зависимость ожидает:

* Не обязательный query параметр `q` с типом `str`.
* Не обязательный query параметр `skip` с типом `int`, и значением по умолчанию `0`.
* Не обязательный query параметр `limit` с типом `int`, и значением по умолчанию `100`.

И в конце она возвращает `dict` содержащий эти значения.

!!! Информация

    **FastAPI** добавил поддержку для `Annotated` (и начал её рекомендовать) в версии 0.95.0.

     Если у вас более старая версия, будут ошибки при попытке использовать `Annotated`.

    Убедитесь что вы [Обновили FastAPI версию](../../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} до, как минимум 0.95.1, перед тем как использовать `Annotated`.

### Import `Depends`

=== "Python 3.10+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="1"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! Совет
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="3"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

### Объявите dependency (зависимость) в "dependant" (зависимом)

С тем же смыслом, вы используете с  `Body`, `Query`, и т.д. с вашей *функцией обработки пути* параметров, используейте `Depends` с новым параметром:

=== "Python 3.10+"

    ```Python hl_lines="13  18"
    {!> ../../../docs_src/dependencies/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="15  20"
    {!> ../../../docs_src/dependencies/tutorial001_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="16  21"
    {!> ../../../docs_src/dependencies/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! Совет
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="11  16"
    {!> ../../../docs_src/dependencies/tutorial001_py310.py!}
    ```

=== "Python 3.8+ non-Annotated"

    !!! Совет
        Настоятельно рекомендуем использовать `Annotated` версию насколько это возможно.

    ```Python hl_lines="15  20"
    {!> ../../../docs_src/dependencies/tutorial001.py!}
    ```

Так же вы используете `Depends` в параметрах вашей функции, как вы использовали `Body`, `Query`, и т.д., но `Depends` работает немного иначе.

Вы передаёте в `Depends` одиночный параметр.

Этот параметр будет чем то похож на функцию.


**Вы не вызываете его** на месте (не добавляете скобочки в конце: 👎 *your_best_func()*👎), просто передаёте как параметр в `Depends()`.

И потом функция берёт параметры так же, как *функция обработки пути*.

!!! Совет
	 В следующей главе вы увидите, какие другие вещи, помимо функций, можно использовать в качестве зависимостей.

Whenever a new request arrives, **FastAPI** will take care of:

* Calling your dependency ("dependable") function with the correct parameters.
* Get the result from your function.
* Assign that result to the parameter in your *функции обработки пути*.

```mermaid
graph TB

common_parameters(["common_parameters"])
read_items["/items/"]
read_users["/users/"]

common_parameters --> read_items
common_parameters --> read_users
```

This way you write shared code once and **FastAPI** takes care of calling it for your *path operations*.

!!! check
    Notice that you don't have to create a special class and pass it somewhere to **FastAPI** to "register" it or anything similar.

    You just pass it to `Depends` and **FastAPI** knows how to do the rest.

## Share `Annotated` dependencies

In the examples above, you see that there's a tiny bit of **code duplication**.

When you need to use the `common_parameters()` dependency, you have to write the whole parameter with the type annotation and `Depends()`:

```Python
commons: Annotated[dict, Depends(common_parameters)]
```

But because we are using `Annotated`, we can store that `Annotated` value in a variable and use it in multiple places:

=== "Python 3.10+"

    ```Python hl_lines="12  16  21"
    {!> ../../../docs_src/dependencies/tutorial001_02_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="14  18  23"
    {!> ../../../docs_src/dependencies/tutorial001_02_an_py39.py!}
    ```

=== "Python 3.8+"

    ```Python hl_lines="15  19  24"
    {!> ../../../docs_src/dependencies/tutorial001_02_an.py!}
    ```

!!! tip
    This is just standard Python, it's called a "type alias", it's actually not specific to **FastAPI**.

    But because **FastAPI** is based on the Python standards, including `Annotated`, you can use this trick in your code. 😎

The dependencies will keep working as expected, and the **best part** is that the **type information will be preserved**, which means that your editor will be able to keep providing you with **autocompletion**, **inline errors**, etc. The same for other tools like `mypy`.

This will be especially useful when you use it in a **large code base** where you use **the same dependencies** over and over again in **many *path operations***.

## To `async` or not to `async`

As dependencies will also be called by **FastAPI** (the same as your *функции обработки путиs*), the same rules apply while defining your functions.

You can use `async def` or normal `def`.

And you can declare dependencies with `async def` inside of normal `def` *функции обработки путиs*, or `def` dependencies inside of `async def` *функции обработки путиs*, etc.

It doesn't matter. **FastAPI** will know what to do.

!!! note
    If you don't know, check the [Async: *"In a hurry?"*](../../async.md){.internal-link target=_blank} section about `async` and `await` in the docs.

## Integrated with OpenAPI

All the request declarations, validations and requirements of your dependencies (and sub-dependencies) will be integrated in the same OpenAPI schema.

So, the interactive docs will have all the information from these dependencies too:

<img src="/img/tutorial/dependencies/image01.png">

## Simple usage

If you look at it, *функции обработки путиs* are declared to be used whenever a *path* and *operation* matches, and then **FastAPI** takes care of calling the function with the correct parameters, extracting the data from the request.

Actually, all (or most) of the web frameworks work in this same way.

You never call those functions directly. They are called by your framework (in this case, **FastAPI**).

With the Dependency Injection system, you can also tell **FastAPI** that your *функции обработки пути* also "depends" on something else that should be executed before your *функции обработки пути*, and **FastAPI** will take care of executing it and "injecting" the results.

Other common terms for this same idea of "dependency injection" are:

* resources
* providers
* services
* injectables
* components

## **FastAPI** plug-ins

Integrations and "plug-ins" can be built using the **Dependency Injection** system. But in fact, there is actually **no need to create "plug-ins"**, as by using dependencies it's possible to declare an infinite number of integrations and interactions that become available to your *функции обработки пути*.

And dependencies can be created in a very simple and intuitive way that allows you to just import the Python packages you need, and integrate them with your API functions in a couple of lines of code, *literally*.

You will see examples of this in the next chapters, about relational and NoSQL databases, security, etc.

## **FastAPI** compatibility

The simplicity of the dependency injection system makes **FastAPI** compatible with:

* all the relational databases
* NoSQL databases
* external packages
* external APIs
* authentication and authorization systems
* API usage monitoring systems
* response data injection systems
* etc.

## Simple and Powerful

Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.

You can define dependencies that in turn can define dependencies themselves.

In the end, a hierarchical tree of dependencies is built, and the **Dependency Injection** system takes care of solving all these dependencies for you (and their sub-dependencies) and providing (injecting) the results at each step.

For example, let's say you have 4 API endpoints (*path operations*):

* `/items/public/`
* `/items/private/`
* `/users/{user_id}/activate`
* `/items/pro/`

then you could add different permission requirements for each of them just with dependencies and sub-dependencies:

```mermaid
graph TB

current_user(["current_user"])
active_user(["active_user"])
admin_user(["admin_user"])
paying_user(["paying_user"])

public["/items/public/"]
private["/items/private/"]
activate_user["/users/{user_id}/activate"]
pro_items["/items/pro/"]

current_user --> active_user
active_user --> admin_user
active_user --> paying_user

current_user --> public
active_user --> private
admin_user --> activate_user
paying_user --> pro_items
```

## Integrated with **OpenAPI**

All these dependencies, while declaring their requirements, also add parameters, validations, etc. to your *path operations*.

**FastAPI** will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems.
