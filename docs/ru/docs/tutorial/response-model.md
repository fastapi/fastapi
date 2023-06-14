# Схема ответа - Возвращаемый тип
<!-- # Response Model - Return Type -->

Вы можете объявить тип **возвращаемого значения**, указав аннотацию для *функции операции пути (path operation)*.
<!-- You can declare the type used for the response by annotating the *path operation function* **return type**. -->

FastAPI позволяет пользоватсья **аннотациями типов** точно так же, как вы бы использовали их для **аргументов** функции. В аннотациях можно указывать схемы Pydantic, списки, словари, скалярные типы (такие как int, bool и т.д.).
<!-- You can use **type annotations** the same way you would for input data in function **parameters**, you can use Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc. -->

=== "Python 3.10+"

    ```Python hl_lines="16  21"
    {!> ../../../docs_src/response_model/tutorial001_01_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="18  23"
    {!> ../../../docs_src/response_model/tutorial001_01.py!}
    ```

FastAPI будет использовать этот возвращаемый тип для:
<!-- FastAPI will use this return type to: -->

* **Валидации** ответа.
    * Если данные невалидны (например, отсутствует одно из полей), это означает, что код *вашего* приложения работает некорректно и функция возвращает не то, что вы ожидаете. В таком случае приложение вернет server error вместо того, чтобы отправить неправильные данные. Таким образом, вы и ваши пользователи могут быть уверены, что получат корректные данные в том виде, в котором их ожидают.
* Добавьте **JSON Schema** для выходного значения внутри *операций пути (path operation)* OpenAPI.
    * Она будет использована для **автоматически генерируемой документации**.
    * А также - для автоматической кодогенерации пользователями.

<!-- * **Validate** the returned data.
    * If the data is invalid (e.g. you are missing a field), it means that *your* app code is broken, not returning what it should, and it will return a server error instead of returning incorrect data. This way you and your clients can be certain that they will receive the data and the data shape expected.
* Add a **JSON Schema** for the response, in the OpenAPI *path operation*.
    * This will be used by the **automatic docs**.
    * It will also be used by automatic client code generation tools. -->


Но самое важное:

* Ответ будет **ограничен и отфильтрован** - т.е. в нем останутся только те данные, которые определены в возвращаемом типе.
    * Это особенно важно для **безопасности**, далее мы рассмотрим эту тему подробнее.
<!-- But most importantly:

* It will **limit and filter** the output data to what is defined in the return type.
    * This is particularly important for **security**, we'll see more of that below. -->

## Параметр `response_model`
<!-- ## `response_model` Parameter -->

Бывают случаи, когда вам необходимо (или просто хочется) возвращать данные, которые не полностью соответствуют объявленному типу.
<!-- There are some cases where you need or want to return some data that is not exactly what the type declares. -->

Допустим, вы хотите, чтобы ваша функция **возвращала словарь (dict)** или объект базы данных, но при этом **объявите выходной тип как схему Pydantic**. Тогда именно указання схема будет использована для автоматической документации, валидации и т.п. для объекта, который вы вернули (например, словарь или объект базы данных).
<!-- For example, you could want to **return a dictionary** or a database object, but **declare it as a Pydantic model**. This way the Pydantic model would do all the data documentation, validation, etc. for the object that you returned (e.g. a dictionary or database object). -->

Но если указать аннотацию возвращаемого типа, статическая проверка типов будет выдавать ошибку (абсолютно корректную в данном случае). Она будет говорить о том, что ваша функция должна возвращать данные одного типа (например, dict), а в аннотации вы объявили другой тип (например, схема Pydantic).

<!-- If you added the return type annotation, tools and editors would complain with a (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model). -->

В таком случае можно использовать параметр `response_model` внутри *декоратора операции пути (path operation)* вместо аннотации типа для функции.
<!-- In those cases, you can use the *path operation decorator* parameter `response_model` instead of the return type. -->

Параметр `response_model` может быть указан для любой *операции пути (path operation)*:
<!-- You can use the `response_model` parameter in any of the *path operations*: -->

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* и др.
<!-- * etc. -->

=== "Python 3.10+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="17  22  24-27"
    {!> ../../../docs_src/response_model/tutorial001.py!}
    ```

!!! note
    Помните, что параметр `response_model` является параметром именно декоратора http-методов (`get`, `post`, и т.п.). Не следует его указывать для *функций операций пути (path operation)*, как вы бы поступили с другими параметрами или с телом запроса.
    <!-- Notice that `response_model` is a parameter of the "decorator" method (`get`, `post`, etc). Not of your *path operation function*, like all the parameters and body. -->

`response_model` принимает те же типы, которые можно указать для какого-либо поля в схеме Pydantic. Таким образом, это может быть как одиночная схема Pydantic, так и `список (list)` объектов Pydantic. Например, `List[Item]`.
<!-- `response_model` receives the same type you would declare for a Pydantic model field, so, it can be a Pydantic model, but it can also be, e.g. a `list` of Pydantic models, like `List[Item]`. -->

FastAPI будет использовать значение `response_model` для того, чтобы автоматически генерировать документацию, производить валидацию и т.п. А также для **конвертации и фильтрации выходных данных** в объявленный тип.
<!-- FastAPI will use this `response_model` to do all the data documentation, validation, etc. and also to **convert and filter the output data** to its type declaration. -->

!!! tip
    Если вы используете анализаторы типов со строгой проверкой (например, mypy), можно указать `Any` в качестве типа возвращаемого значения функции.
    <!-- If you have strict type checks in your editor, mypy, etc, you can declare the function return type as `Any`. -->
    Таким образом вы информируете ваш редактор кода, что намеренно возвращаете данные неопределенного типа. Но возможности FastAPI, такие как автоматическая генерация документации, валидация, фильтрация и т.д. все так же будут работать, просто используя параметр `response_model`.
    <!-- That way you tell the editor that you are intentionally returning anything. But FastAPI will still do the data documentation, validation, filtering, etc. with the `response_model`. -->

### Приоритет `response_model`

Если указать аннотацию типа для ответа функции, а также параметр `response_model` - последний будет иметь больший приоритет и FastAPI будет использовать именно его.
<!-- If you declare both a return type and a `response_model`, the `response_model` will take priority and be used by FastAPI. -->

Таким образом вы можете объявить корректные аннотации типов к вашим функциям, даже если они возвращают тип, отличающийся от указанного в `response_model`. Они будут считаны во время статической проверки типов вашими помощниками, например, mypy. При этом вы все так же используете возможности FastAPI для автоматической документации, валидации и т.д. благодаря `response_model`.
<!-- This way you can add correct type annotations to your functions even when you are returning a type different than the response model, to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the `response_model`. -->

Вы можете указать значение `response_model=None`, чтобы отключить создание схемы ответа для данной *операции пути (path operation)*. Это может понадобиться, если вы добавляете аннотации типов для данных, не являющимися валидными полями Pydantic. Мы увидим пример кода для такого случая в одном из разделов ниже.
<!-- You can also use `response_model=None` to disable creating a response model for that *path operation*, you might need to do it if you are adding type annotations for things that are not valid Pydantic fields, you will see an example of that in one of the sections below. -->

## Получить и вернуть один и тот же тип данных
<!-- ## Return the same input data -->

Здесь мы объявили схему `UserIn`, которая хранит пользователський пароль в открытом виде:
<!-- Here we are declaring a `UserIn` model, it will contain a plaintext password: -->

=== "Python 3.10+"

    ```Python hl_lines="7  9"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9  11"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

!!! info
    Чтобы использовать `EmailStr`, прежде необходимо установить <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email_validator`</a>.
    Используйте `pip install email-validator`
    или `pip install pydantic[email]`.
    <!-- To use `EmailStr`, first install <a href="https://github.com/JoshData/python-email-validator" class="external-link" target="_blank">`email_validator`</a>. -->
    <!-- E.g. `pip install email-validator`
    or `pip install pydantic[email]`. -->

Далее мы используем нашу схему в аннотациих типа как для аргумента функции, так и для выходного значения:
<!-- And we are using this model to declare our input and the same model to declare our output: -->

=== "Python 3.10+"

    ```Python hl_lines="16"
    {!> ../../../docs_src/response_model/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/response_model/tutorial002.py!}
    ```

Теперь всякий раз, когда клиент создает пользователя с паролем, API будет возвращать его пароль в ответе.
<!-- Now, whenever a browser is creating a user with a password, the API will return the same password in the response. -->

В данном случае это не такая уж большая проблема, поскольку ответ получит тот же самый пользователь, который и создал пароль.
<!-- In this case, it might not be a problem, because it's the same user sending the password. -->

Но что если мы захотим использовать эту схему для какой-либо другой *операции пути (path operation)*? Мы можем, сами того не желая, отправить пароль любому другому пользователю.
<!-- But if we use the same model for another *path operation*, we could be sending our user's passwords to every client. -->

!!! danger
    Никогда не храните пароли пользователей в открытом виде, а также никогда не возвращайте их в ответе, как в примере выше. В противном случае - убедитесь, что вы хорошо продумали и учли все возможные риски такого подхода и вам известно, что вы делаете.
    <!-- Never store the plain password of a user or send it in a response like this, unless you know all the caveats and you know what you are doing. -->

## Создадим схему для ответа
<!-- ## Add an output model -->

Вместо этого мы можем создать входную схему, хранящую пароль в открытом виде и выходную схему без пароля:
<!-- We can instead create an input model with the plaintext password and an output model without it: -->

=== "Python 3.10+"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9  11  16"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

В таком случае, даже несмотря на то, что наша *функция операции пути (path operation)* возвращает тот же самый объект с паролем, полученный на вход:
<!-- Here, even though our *path operation function* is returning the same input user that contains the password: -->

=== "Python 3.10+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

...мы указали в `response_model` схему `UserOut`, в которой отсутствует поле, содержащее пароль - и он будет исключен из ответа:
<!-- ...we declared the `response_model` to be our model `UserOut`, that doesn't include the password: -->

=== "Python 3.10+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial003.py!}
    ```

Таким образом **FastAPI** позаботится о фильтрации ответа и исключит из него всё, что не указано в выходной схеме (при помощи Pydantic).
<!-- So, **FastAPI** will take care of filtering out all the data that is not declared in the output model (using Pydantic). -->

### `response_model` или Аннотации типов
<!-- ### `response_model` or Return Type -->

В нашем примере схемы входных данных и выходных данных различаются. И если мы укажем аннотацию типа выходного значения функции как `UserOut` - проверка типов выдаст ошибку из-за того, что мы возвращаем некорректный тип. Поскольку это 2 разных класса.
<!-- In this case, because the two models are different, if we annotated the function return type as `UserOut`, the editor and tools would complain that we are returning an invalid type, as those are different classes. -->

Поэтому в нашем примере мы можем объявить тип ответа только в параметре `response_model`.
<!-- That's why in this example we have to declare it in the `response_model` parameter. -->

...но продолжайте читать дальше, чтобы узнать как можно это обойти.
<!-- ...but continue reading below to see how to overcome that. -->

## Возвращаемый тип и Фильтрация данных
<!-- ## Return Type and Data Filtering -->

Продолжим рассматривать предыдущий пример. Мы хотели **аннотировать входные данные одним типом**, а выходное значение - **другим типом**.
<!-- Let's continue from the previous example. We wanted to **annotate the function with one type** but return something that includes **more data**. -->

Мы хотим, чтобы FastAPI продолжал **фильтровать** данные, используя `response_model`.
<!-- We want FastAPI to keep **filtering** the data using the response model. -->

В прошлом примере, т.к. входной и выходной типы являлись разными классами, мы были вынуждены использовать параметр `response_model`. И как следствие, мы лишались помощи статических анализаторов для проверки ответа функции.
<!-- In the previous example, because the classes were different, we had to use the `response_model` parameter. But that also means that we don't get the support from the editor and tools checking the function return type. -->

Но в подавляющем большинстве случаев мы будем хотеть, чтобы схема ответа лишь **фильтровала/удаляла** некоторые данные из ответа, как в нашем примере.
<!-- But in most of the cases where we need to do something like this, we want the model just to **filter/remove** some of the data as in this example. -->

И в таких случаях мы можем использовать классы и наследование, чтобы пользоваться преимуществами **аннотаций типов** и получать более полную статическую проверку типов. Но при этом все так же получать **фильтрацию ответа** от FastAPI.
<!-- And in those cases, we can use classes and inheritance to take advantage of function **type annotations** to get better support in the editor and tools, and still get the FastAPI **data filtering**. -->

=== "Python 3.10+"

    ```Python hl_lines="7-10  13-14  18"
    {!> ../../../docs_src/response_model/tutorial003_01_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9-13  15-16  20"
    {!> ../../../docs_src/response_model/tutorial003_01.py!}
    ```

Таким образом, мы получаем поддержку редактора кода и mypy в части типов и мы все еще пользуемся фильтрацией данных.
<!-- With this, we get tooling support, from editors and mypy as this code is correct in terms of types, but we also get the data filtering from FastAPI. -->

Как это возможно? Давайте раздеремся. 🤓
<!-- How does this work? Let's check that out. 🤓 -->

### Аннотации типов и инструменты для их проверки
<!-- ### Type Annotations and Tooling -->

Для начала давайте рассмотрим как их видит наш редактор кода, mypy и другие помощники разработчика.
<!-- First let's see how editors, mypy and other tools would see this. -->

У схемы `BaseUser` есть некоторые поля. Затем `UserIn` наследуется от `BaseUser` и добавляет новое поле `password`. Таким образом схема будет включать в себя все поля из первой схемы (родителя), а так же свои собственные.
<!-- `BaseUser` has the base fields. Then `UserIn` inherits from `BaseUser` and adds the `password` field, so, it will include all the fields from both models. -->

Мы аннотируем возвращаемый тип функции как `BaseUser`, но фактически мы будем возвращать объект типа `UserIn`.
<!-- We annotate the function return type as `BaseUser`, but we are actually returning a `UserIn` instance. -->

Редакторы, mypy и другие инструменты не будут иметь возражений против такого подхода, поскольку `UserIn` является подклассом `BaseUser`. Это означает, что такой тип будет *корректным*, т.к. ответ может быть чем-угодно, если это будет `BaseUser`.
<!-- The editor, mypy, and other tools won't complain about this because, in typing terms, `UserIn` is a subclass of `BaseUser`, which means it's a *valid* type when what is expected is anything that is a `BaseUser`. -->

### Фильтрация Данных FastAPI
<!-- ### FastAPI Data Filtering -->

FastAPI знает тип ответа функции, так что вы можете быть уверены что на выходе будут **только** те поля, которые вы указали.
<!-- Now, for FastAPI, it will see the return type and make sure that what you return includes **only** the fields that are declared in the type. -->

FastAPI соввместно с Pydantic выполнит некоторую магию "под капотом", чтобы убедиться, что те же самые правила наследования классов не используются для фильтрации возвращаемых данных, в противном случае вы могли бы в конечном итоге вернуть гораздо больше данных, чем ожидали.
<!-- FastAPI does several things internally with Pydantic to make sure that those same rules of class inheritance are not used for the returned data filtering, otherwise you could end up returning much more data than what you expected. -->

Таким образом, вы можете получить все самое лучшее из обоих миров: аннотации типов с **поддержкой инструментов для разработки** и **фильтрацию данных**.
<!-- This way, you can get the best of both worlds: type annotations with **tooling support** and **data filtering**. -->

## Автоматическая документация
<!-- ## See it in the docs -->

Если посмотреть на сгенерированную документацию, вы можете убедиться, что в ней присутствуют обе JSON Schema - как для входной схемы, так и для выходной:
<!-- When you see the automatic docs, you can check that the input model and output model will both have their own JSON Schema: -->

<img src="/img/tutorial/response-model/image01.png">

И также обе схемы будут использованы в интерактивной документации API:
<!-- And both models will be used for the interactive API documentation: -->

<img src="/img/tutorial/response-model/image02.png">

## Другие аннотации типов
<!-- ## Other Return Type Annotations -->

Бывают случаи, когда вы возвращаете что-то, что не является валидным типом для Pydantic и вы указываете аннотацию ответа функции только для того, чтобы работала поддержка различных инструментов (редактор кода, mypy и др.).
<!-- There might be cases where you return something that is not a valid Pydantic field and you annotate it in the function, only to get the support provided by tooling (the editor, mypy, etc). -->

### Возвращаем Response
<!-- ### Return a Response Directly -->

Самый частый сценарий использования - это [возвращать Response напрямую, как описано в расширенной документации](../advanced/response-directly.md){.internal-link target=_blank}.

```Python hl_lines="8  10-11"
{!> ../../../docs_src/response_model/tutorial003_02.py!}
```

<!-- The most common case would be [returning a Response directly as explained later in the advanced docs](../advanced/response-directly.md){.internal-link target=_blank}.

```Python hl_lines="8  10-11"
{!> ../../../docs_src/response_model/tutorial003_02.py!}
``` -->

Это поддерживается FastAPI по-умолчанию, т.к. аннотация проставлена в классе (или подклассе) `Response`.
<!-- This simple case is handled automatically by FastAPI because the return type annotation is the class (or a subclass) of `Response`. -->

И ваши помощники разработки также будут счастливы, т.к. оба класса `RedirectResponse` и `JSONResponse` являются подклассами `Response`. Таким образом мы получаем корректную аннотацию типа.
<!-- And tools will also be happy because both `RedirectResponse` and `JSONResponse` are subclasses of `Response`, so the type annotation is correct. -->

### Подкласс Response в аннотации типа
<!-- ### Annotate a Response Subclass -->

Вы также можете указать подкласс `Response` в аннотации типа:
<!-- You can also use a subclass of `Response` in the type annotation: -->

```Python hl_lines="8-9"
{!> ../../../docs_src/response_model/tutorial003_03.py!}
```

Это сработает, потому что `RedirectResponse` является подклассом `Response` и FastAPI автоматически обработает этот простейший случай.
<!-- This will also work because `RedirectResponse` is a subclass of `Response`, and FastAPI will automatically handle this simple case. -->

### Некорректные аннотации типов
<!-- ### Invalid Return Type Annotations -->

Но когда вы возвращаете какой-либо другой произвольный объект, который не является допустимым типом Pydantic (например, объект базы данных), и вы аннотируете его подобным образом для функции, FastAPI попытается создать из этого типа схему Pydantic и потерпит неудачу.
<!-- But when you return some other arbitrary object that is not a valid Pydantic type (e.g. a database object) and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that type annotation, and will fail. -->

То же самое произошло бы, если бы у вас было что-то вроде <abbr title='Union между различными типами буквально означает "любой из перечисленных типов".'>Union</abbr> между различными типами и один или несколько из них не являлись бы допустимыми типами для Pydantic. Например, такой варинт приведет к ошибке 💥:
<!-- The same would happen if you had something like a <abbr title='A union between multiple types means "any of these types".'>union</abbr> between different types where one or more of them are not valid Pydantic types, for example this would fail 💥: -->

=== "Python 3.10+"

    ```Python hl_lines="8"
    {!> ../../../docs_src/response_model/tutorial003_04_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="10"
    {!> ../../../docs_src/response_model/tutorial003_04.py!}
    ```

...такой код вызовет ошибку, потому что в аннотации указан не поддерживаемый тип для Pydantic. А также этот тип не является классом или подклассом `Response`.
<!-- ...this fails because the type annotation is not a Pydantic type and is not just a single `Response` class or subclass, it's a union (any of the two) between a `Response` and a `dict`. -->

### Возможно ли отключить генерацию схемы ответа?
<!-- ### Disable Response Model -->

Продолжим рассматривать предыдущий пример. Допустим, что вы хотите отказаться от автоматической валидации ответа, документации, фильтрации и т.д. 
<!-- Continuing from the example above, you might not want to have the default data validation, documentation, filtering, etc. that is performed by FastAPI. -->

Но в то же время, хотите сохранить аннотацию возвращаемого типа для функции, чтобы обеспечить работу помощников и анализаторов типов (например, mypy).
<!-- But you might want to still keep the return type annotation in the function to get the support from tools like editors and type checkers (e.g. mypy). -->

В таком случае, вы можете отключить генерацию схемы ответа, указав `response_model=None`:
<!-- In this case, you can disable the response model generation by setting `response_model=None`: -->

=== "Python 3.10+"

    ```Python hl_lines="7"
    {!> ../../../docs_src/response_model/tutorial003_05_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="9"
    {!> ../../../docs_src/response_model/tutorial003_05.py!}
    ```

Тогда FastAPI не станет генерировать схему ответа и вы сможете сохранить такую аннотацию типа, которая вам требуется, никак не влияя на работу FastAPI. 🤓
<!-- This will make FastAPI skip the response model generation and that way you can have any return type annotations you need without it affecting your FastAPI application. 🤓 -->

## Параметры схемы ответа
<!-- ## Response Model encoding parameters -->

Схема ответа может иметь значения по-умолчанию, например:
<!-- Your response model could have default values, like: -->

=== "Python 3.10+"

    ```Python hl_lines="9  11-12"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="11  13-14"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

* `description: Union[str, None] = None` (или `str | None = None` в Python 3.10), где `None` является значением по-умолчанию.
* `tax: float = 10.5`, где `10.5` является значением по-умолчанию.
* `tags: List[str] = []`, где пустой список `[]` является значением по-умолчанию.
<!-- * `description: Union[str, None] = None` (or `str | None = None` in Python 3.10) has a default of `None`.
* `tax: float = 10.5` has a default of `10.5`.
* `tags: List[str] = []` as a default of an empty list: `[]`. -->

но вы, возможно, хотели бы исключить их из ответа, если данные поля не были заданы явно.
<!-- but you might want to omit them from the result if they were not actually stored. -->

Например, у вас есть схема с множеством необязательных полей в NoSQL базе данных, но вы не хотите отправлять в качестве ответа очень длинный JSON с множеством значений по-умолчанию.
<!-- For example, if you have models with many optional attributes in a NoSQL database, but you don't want to send very long JSON responses full of default values. -->

### Используйте параметр `response_model_exclude_unset`
<!-- ### Use the `response_model_exclude_unset` parameter -->

Установите для *декоратора операции пути (path operation)* параметр `response_model_exclude_unset=True`:
<!-- You can set the *path operation decorator* parameter `response_model_exclude_unset=True`: -->

=== "Python 3.10+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/response_model/tutorial004_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/response_model/tutorial004.py!}
    ```

и тогда значения по-умолчанию не будут включены в ответ. В нем будут только те поля, значения которых фактически были установлены.
<!-- and those default values won't be included in the response, only the values actually set. -->

Итак, если вы отправите запрос на данную *операцию пути (path operation)* для элемента, с ID = `Foo` - ответ (с исключенными значениями по-умолчанию) будет таким:
<!-- So, if you send a request to that *path operation* for the item with ID `foo`, the response (not including default values) will be: -->

```JSON
{
    "name": "Foo",
    "price": 50.2
}
```

!!! info
    "Под капотом" FastAPI использует метод `.dict()` у объектов схем Pydantic <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">с параметром `exclude_unset`</a>, чтобы достичь такого эффекта.
    <!-- FastAPI uses Pydantic model's `.dict()` with <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">its `exclude_unset` parameter</a> to achieve this. -->

!!! info
    Вы также можете использовать:
    <!-- You can also use: -->

    * `response_model_exclude_defaults=True`
    * `response_model_exclude_none=True`

    как описано в <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">документации Pydantic</a> для параметров `exclude_defaults` и `exclude_none`.
    <!-- as described in <a href="https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict" class="external-link" target="_blank">the Pydantic docs</a> for `exclude_defaults` and `exclude_none`. -->

#### Если значение поля отличается от значения по-умолчанию
<!-- #### Data with values for fields with defaults -->

Если для некоторых полей схемы, имеющих значения по-умолчанию, значения были явно установлены - как для элемента с ID = `Bar`, ответ будет таким:
<!-- But if your data has values for the model's fields with default values, like the item with ID `bar`: -->

```Python hl_lines="3  5"
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
```

они не будут исключены из ответа.
<!-- they will be included in the response. -->

#### Если значение поля совпадает с его значением по-умолчанию
<!-- #### Data with the same values as the defaults -->

Если данные содержат те же значения, которые являются для этих полей по-умолчанию, но были установлены явно - как для элемента с ID = `baz`, ответ будет таким:
<!-- If the data has the same values as the default ones, like the item with ID `baz`: -->

```Python hl_lines="3  5-6"
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
```

FastAPI достаточно умен (на самом деле, это заслуга Pydantic), чтобы понять, что, хотя `description`, `tax`, и `tags` хранят такие же данные, что и должны быть по умолчанию - для них эти значения были установлены явно (а не получены из значений по-умолчанию).
<!-- FastAPI is smart enough (actually, Pydantic is smart enough) to realize that, even though `description`, `tax`, and `tags` have the same values as the defaults, they were set explicitly (instead of taken from the defaults). -->

И поэтому, они также будут включены в JSON ответа.
<!-- So, they will be included in the JSON response. -->

!!! tip
    Значением по-умолчанию может быть что угодно, не только `None`.
    <!-- Notice that the default values can be anything, not only `None`. -->

    Так же может быть и список (`[]`), значение 10.5 с типом `float`, и т.п.
    <!-- They can be a list (`[]`), a `float` of `10.5`, etc. -->

### `response_model_include` и `response_model_exclude`
<!-- ### `response_model_include` and `response_model_exclude` -->

Вы также можете использова параметры *декоратора операции пути (path operation)*, такие как `response_model_include` и `response_model_exclude`.
<!-- You can also use the *path operation decorator* parameters `response_model_include` and `response_model_exclude`. -->

Они принимают аргументы типа `set`, состоящий из строк (`str`) с названиями аттрибутов, которые либо требуется включить в ответ (при этом исключив все остальные), либо  наоборот исключить (оставив в ответе все остальные поля).
<!-- They take a `set` of `str` with the name of the attributes to include (omitting the rest) or to exclude (including the rest). -->

Это можно использовать как быстрый способ исключить данные из ответа, не создавая отдельную схему Pydantic.
<!-- This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output. -->

!!! tip
    Но рекомендуется следовать всем советам, изложенным выше, используя несколько схем, вместо данных параметров.  
    <!-- But it is still recommended to use the ideas above, using multiple classes, instead of these parameters. -->

    Потому как OpenAPI JSON схема, генерируемая вашим приложением (а так же документация) все еще будет содержать все поля, даже если вы использовали `response_model_include` или `response_model_exclude` и исключили некоторые аттрибуты.
    <!-- This is because the JSON Schema generated in your app's OpenAPI (and the docs) will still be the one for the complete model, even if you use `response_model_include` or `response_model_exclude` to omit some attributes. -->

    Тоже самое применимо к параметру `response_model_by_alias`.
    <!-- This also applies to `response_model_by_alias` that works similarly. -->

=== "Python 3.10+"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial005_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial005.py!}
    ```

!!! tip
    При помощи кода `{"name","description"}` создается объект множества (`set`) с двумя строковыми значениями.
    <!-- The syntax `{"name", "description"}` creates a `set` with those two values. -->

    Того же самого можно достичь используя `set(["name", "description"])`.
    <!-- It is equivalent to `set(["name", "description"])`. -->

#### Что если использовать `list` вместо `set`?
<!-- #### Using `list`s instead of `set`s -->

Если вы забыли про `set` и использовали структуру `list` или `tuple`, FastAPI автоматически преобразует этот объект в `set`, чтобы обеспечить корректную работу:
<!-- If you forget to use a `set` and use a `list` or `tuple` instead, FastAPI will still convert it to a `set` and it will work correctly: -->

=== "Python 3.10+"

    ```Python hl_lines="29  35"
    {!> ../../../docs_src/response_model/tutorial006_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="31  37"
    {!> ../../../docs_src/response_model/tutorial006.py!}
    ```

## Резюме
<!-- ## Recap -->

Используйте параметр `response_model` у *декоратора операции пути (path operation)* для того, чтобы задать схему ответа и в большей степени для того, чтобы быть уверенным, что приватная информация будет отфильтрована.
<!-- Use the *path operation decorator's* parameter `response_model` to define response models and especially to ensure private data is filtered out. -->

А также используйте `response_model_exclude_unset`, чтобы возвращать только те значения, которые были заданы явно.
<!-- Use `response_model_exclude_unset` to return only the values explicitly set. -->
