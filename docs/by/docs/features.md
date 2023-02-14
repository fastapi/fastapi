# Асаблівасці

## Асаблівасці FastAPI

**FastAPI** дае Вам наступнае:

### Грунтуецца на адкрытых стандартах

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> для стварэння API, у тым ліку дэкларацыі аперацый шляху, параметраў, запытаў цела, бяспекі і г.д.
* Аўтаматычная дакументацыя мадэлі даных з выкарыстаннем <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (таму што OpenAPI заснаваны на JSON Schema).
* Распрацаваны вакол гэтых стандартаў пасля іх дасканалага вывучэння, а не як дадатковая надбудова над імі.
* Гэта таксама дазваляе выкарыстоўваць аўтаматычную **генерацыю кліенцкага кода** на многіх мовах.

### Аўтаматычная дакументацыя

Інтэрактыўная дакументацыя па API і вэб-інтэрфейс для даследавання карыстальніцкіх інтэрфейсаў. Паколькі фреймворк заснаваны на OpenAPI, ёсць некалькі варыянтаў, 2 з якіх уключаны па змаўчанні.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> - інтэрактыўнае даследаванне, выклік і тэставанне вашага API непасрэдна з браўзера.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> - альтэрнатыўная дакументацыя API.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Выключна сучасны Python

Усё заснавана на стандартных **анатацыях тыпаў Python 3.6** (дзякуючы Pydantic). Не трэба вывучаць новы сінтаксіс. Проста стандартны сучасны Python.

Калі вам трэба ўзгадаць, як выкарыстоўваць тыпы Python (нават калі вы не выкарыстоўваеце FastAPI), вылучыце 2 хвіліны і азнаёмцеся з кароткім кіраўніцтвам: [Python Types](python-types.md){.internal-link target=_blank}.

Вы пішаце на стандартным Python з анатацыямі тыпаў:

```Python
from datetime import date

from pydantic import BaseModel

# Аб'явіце пераменную як str
# і атрымайце падтрымку рэдактара ўнутры функцыі
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Гэта можа быць выкарыстана наступным чынам:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! Інфармацыя
    `**second_user_data` азначае:

    Перадайце ключы і значэнні слоўніка second_user_data непасрэдна ў якасці аргументаў ключ-значэнне, эквівалентна: `User(id=4, name="Mary", joined="2018-11-30")`

### Падтрымка рэдактараў

Увесь фрэймворк быў распрацаваны так, каб быць простым і інтуітыўна зразумелым у выкарыстанні, усе рашэнні былі правераны ў некалькіх рэдактарах яшчэ да пачатку стварэння, каб забяспечыць найлепшае уздзеянне на распрацоўку.

У апошнім апытанні Python-распрацоўшчыкаў было відавочна, <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">што найбольш часта выкарыстоўванай функцыяй з'яўляецца "аўтадапаўненне"</a>.

Увесь фрэймворк **FastAPI** задавальняе гэтаму. Аўтадапаўненне працуе ўсюды.

Вам рэдка трэба будзе вяртацца да дакументацыі.

Вось як вам можа дапамагчы ваш рэдактар:

* <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Вы атрымаеце дапаўненне ў кодзе, якое раней нават лічылася немагчымым. Напрыклад, ключ `price` у целе JSON (які можа быць укладзеным), які прыходзіць з запыту.

Больш ніякіх няправільна набраных імёнаў ключоў, пераходаў туды-сюды паміж дакументамі, або пракручванняў увех і ўніз, каб нарэште даведацца, выкарытоўваеце Вы `username` ці `user_name`.

### Кароткасць

Фрэймворк мае разумныя **значэння па змаўчанні** з дадатковымі канфігурацыямі для ўсяго. Усе параметры могуць быць дакладна настроены, каб рабіць тое, што вам трэба, і вызначаць неабходны API.

Але па змаўчанні ўсё гэта **"проста працуе"**.

### Праверка дадзеных

* Праверка большасці (ці ўсіх?) **тыпаў даных** Python, у тым ліку:
    * JSON аб'ектаў (`dict`).
    * JSON масіў (`list`) з вызначэннем тыпаў элемента.
    * Радковыя (`str`) палі з вызначэнне мінімальнай і максімальнай даўжыні.
    * Лічбы (`int`, `float`) з мінімальнымі і максімальнымі значэннямі і г.д.

* Праверка для больш экзатычных тыпаў, такіх як:
    * URL.
    * Email.
    * UUID.
    * ...і іншых.

Усе праверкі выконваюцца добра зарэкамендавалым сябе і надзейным **Pydantic**.

### Security and authentication

Security and authentication integrated. Without any compromise with databases or data models.

All the security schemes defined in OpenAPI, including:

* HTTP Basic.
* **OAuth2** (also with **JWT tokens**). Check the tutorial on [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys in:
    * Headers.
    * Query parameters.
    * Cookies, etc.

Plus all the security features from Starlette (including **session cookies**).

All built as reusable tools and components that are easy to integrate with your systems, data stores, relational and NoSQL databases, etc.

### Dependency Injection

FastAPI includes an extremely easy to use, but extremely powerful <abbr title='also known as "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></abbr> system.

* Even dependencies can have dependencies, creating a hierarchy or **"graph" of dependencies**.
* All **automatically handled** by the framework.
* All the dependencies can require data from requests and **augment the path operation** constraints and automatic documentation.
* **Automatic validation** even for *path operation* parameters defined in dependencies.
* Support for complex user authentication systems, **database connections**, etc.
* **No compromise** with databases, frontends, etc. But easy integration with all of them.

### Unlimited "plug-ins"

Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your *path operations*.

### Tested

* 100% <abbr title="The amount of code that is automatically tested">test coverage</abbr>.
* 100% <abbr title="Python type annotations, with this your editor and external tools can give you better support">type annotated</abbr> code base.
* Used in production applications.

## Starlette features

**FastAPI** is fully compatible with (and based on) <a href="https://www.starlette.io/" class="external-link" target="_blank"><strong>Starlette</strong></a>. So, any additional Starlette code you have, will also work.

`FastAPI` is actually a sub-class of `Starlette`. So, if you already know or use Starlette, most of the functionality will work the same way.

With **FastAPI** you get all of **Starlette**'s features (as FastAPI is just Starlette on steroids):

* Seriously impressive performance. It is <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">one of the fastest Python frameworks available, on par with **NodeJS** and **Go**</a>.
* **WebSocket** support.
* In-process background tasks.
* Startup and shutdown events.
* Test client built on HTTPX.
* **CORS**, GZip, Static Files, Streaming responses.
* **Session and Cookie** support.
* 100% test coverage.
* 100% type annotated codebase.

## Pydantic features

**FastAPI** is fully compatible with (and based on) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. So, any additional Pydantic code you have, will also work.

Including external libraries also based on Pydantic, as <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s for databases.

This also means that in many cases you can pass the same object you get from a request **directly to the database**, as everything is validated automatically.

The same applies the other way around, in many cases you can just pass the object you get from the database **directly to the client**.

With **FastAPI** you get all of **Pydantic**'s features (as FastAPI is based on Pydantic for all the data handling):

* **No brainfuck**:
    * No new schema definition micro-language to learn.
    * If you know Python types you know how to use Pydantic.
* Plays nicely with your **<abbr title="Integrated Development Environment, similar to a code editor">IDE</abbr>/<abbr title="A program that checks for code errors">linter</abbr>/brain**:
    * Because pydantic data structures are just instances of classes you define; auto-completion, linting, mypy and your intuition should all work properly with your validated data.
* **Fast**:
    * in <a href="https://pydantic-docs.helpmanual.io/benchmarks/" class="external-link" target="_blank">benchmarks</a> Pydantic is faster than all other tested libraries.
* Validate **complex structures**:
    * Use of hierarchical Pydantic models, Python `typing`’s `List` and `Dict`, etc.
    * And validators allow complex data schemas to be clearly and easily defined, checked and documented as JSON Schema.
    * You can have deeply **nested JSON** objects and have them all validated and annotated.
* **Extensible**:
    * Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.
* 100% test coverage.
