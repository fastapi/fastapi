# FastAPI CLI

**FastAPI CLI** це програма командного рядка, яку Ви можете використовувати, щоб обслуговувати Ваш додаток FastAPI, керувати Вашими FastApi проектами, тощо.

Коли Ви встановлюєте FastApi (тобто виконуєте `pip install "fastapi[standard]"`), Ви також встановлюєте пакунок `fastapi-cli`, цей пакунок надає команду `fastapi` в терміналі.

Для запуску Вашого FastAPI проекту для розробки, Ви можете скористатись командою `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

Програма командного рядка `fastapi` це **FastAPI CLI**.

FastAPI CLI приймає шлях до Вашої Python програми (напр. `main.py`) і автоматично виявляє екземпляр `FastAPI` (зазвичай названий `app`), обирає коректний процес імпорту, а потім обслуговує його.

Натомість, для запуску у продакшн використовуйте `fastapi run`. 🚀

Всередині **FastAPI CLI** використовує <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, високопродуктивний, production-ready, ASGI cервер. 😎

## `fastapi dev`

Використання `fastapi dev` ініціює режим розробки.

За замовчуванням, **автоматичне перезавантаження** увімкнене, автоматично перезавантажуючи сервер кожного разу, коли Ви змінюєте Ваш код. Це ресурсо-затратно, та може бути менш стабільним, ніж коли воно вимкнене. Ви повинні використовувати його тільки під час розробки. Воно також слухає IP-адресу `127.0.0.1`, що є IP Вашого девайсу для самостійної комунікації з самим собою (`localhost`).

## `fastapi run`

Виконання `fastapi run` запустить FastAPI у продакшн-режимі за замовчуванням.

За замовчуванням, **автоматичне перезавантаження** вимкнене. Воно також прослуховує IP-адресу `0.0.0.0`, що означає всі доступні IP адреси, тим самим даючи змогу будь-кому комунікувати з девайсом. Так Ви зазвичай будете запускати його у продакшн, наприклад у контейнері.

В більшості випадків Ви можете (і маєте) мати "termination proxy", який обробляє HTTPS для Вас, це залежить від способу розгортання вашого додатку, Ваш провайдер може зробити це для Вас, або Вам потрібно налаштувати його самостійно.

/// tip

Ви можете дізнатись більше про це у [документації про розгортування](deployment/index.md){.internal-link target=_blank}.

///
