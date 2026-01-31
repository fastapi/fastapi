# Змінні середовища { #environment-variables }

/// tip | Порада

Якщо ви вже знаєте, що таке «змінні середовища», і як ними користуватися, можете пропустити цей розділ.

///

Змінна середовища (також відома як «**env var**») — це змінна, що існує **поза** Python-кодом, в **операційній системі**, і може бути прочитана вашим Python-кодом (або також іншими програмами).

Змінні середовища можуть бути корисними для керування **налаштуваннями** застосунку, як частина **встановлення** Python тощо.

## Створення і використання env var { #create-and-use-env-vars }

Ви можете **створювати** та використовувати змінні середовища в **оболонці (терміналі)**, без потреби в Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// You could create an env var MY_NAME with
$ export MY_NAME="Wade Wilson"

// Then you could use it with other programs, like
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Create an env var MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Use it with other programs, like
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Читання env var у Python { #read-env-vars-in-python }

Ви також можете створювати змінні середовища **поза** Python, у терміналі (або будь-яким іншим способом), а потім **читати їх у Python**.

Наприклад, у вас може бути файл `main.py` з таким вмістом:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Порада

Другий аргумент у <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> — це значення за замовчуванням, яке слід повернути.

Якщо його не передати, за замовчуванням буде `None`; тут ми задаємо `"World"` як значення за замовчуванням.

///

Після цього ви можете викликати цю Python-програму:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ $Env:MY_NAME = "Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

</div>

////

Оскільки змінні середовища можна задавати поза кодом, але їх може читати код, і їх не потрібно зберігати (комітити в `git`) разом з іншими файлами, їх часто використовують для конфігурації або **налаштувань**.

Ви також можете створити змінну середовища лише для **конкретного запуску програми** — вона буде доступна тільки цій програмі й лише на час її виконання.

Для цього задайте її прямо перед запуском програми, в тому самому рядку:

<div class="termy">

```console
// Create an env var MY_NAME in line for this program call
$ MY_NAME="Wade Wilson" python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python

// The env var no longer exists afterwards
$ python main.py

Hello World from Python
```

</div>

/// tip | Порада

Докладніше про це можна прочитати тут: <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Типи та валідація { #types-and-validation }

Ці змінні середовища можуть зберігати лише **текстові рядки**, оскільки вони є зовнішніми відносно Python і мають бути сумісними з іншими програмами та рештою системи (і навіть з різними операційними системами, як-от Linux, Windows, macOS).

Це означає, що **будь-яке значення**, прочитане в Python зі змінної середовища, **буде `str`**, а будь-яке перетворення в інший тип або будь-яка валідація мають виконуватися в коді.

Більше про використання змінних середовища для керування **налаштуваннями застосунку** ви дізнаєтеся в розділі [Розширений посібник користувача — Налаштування та змінні середовища](./advanced/settings.md){.internal-link target=_blank}.

## Змінна середовища `PATH` { #path-environment-variable }

Існує **особлива** змінна середовища **`PATH`**, яку використовують операційні системи (Linux, macOS, Windows), щоб знаходити програми для запуску.

Значення змінної `PATH` — це довгий рядок, що складається з директорій, розділених двокрапкою `:` у Linux і macOS та крапкою з комою `;` у Windows.

Наприклад, змінна середовища `PATH` може виглядати так:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Це означає, що система має шукати програми в директоріях:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Це означає, що система має шукати програми в директоріях:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Коли ви вводите **команду** в терміналі, операційна система **шукає** програму в **кожній із директорій**, перелічених у змінній середовища `PATH`.

Наприклад, коли ви вводите `python` у терміналі, операційна система шукає програму з назвою `python` у **першій директорії** цього списку.

Якщо вона її знаходить — **використовує**. Інакше продовжує пошук в **інших директоріях**.

### Встановлення Python і оновлення `PATH` { #installing-python-and-updating-the-path }

Під час встановлення Python вас можуть запитати, чи потрібно оновити змінну середовища `PATH`.

//// tab | Linux, macOS

Припустімо, ви встановлюєте Python, і він опиняється в директорії `/opt/custompython/bin`.

Якщо ви погодитеся оновити змінну середовища `PATH`, тоді інсталятор додасть `/opt/custompython/bin` до змінної `PATH`.

Це може виглядати так:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Таким чином, коли ви введете `python` у терміналі, система знайде програму Python у `/opt/custompython/bin` (останній директорії) і використає саме її.

////

//// tab | Windows

Припустімо, ви встановлюєте Python, і він опиняється в директорії `C:\opt\custompython\bin`.

Якщо ви погодитеся оновити змінну середовища `PATH`, тоді інсталятор додасть `C:\opt\custompython\bin` до змінної `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Таким чином, коли ви введете `python` у терміналі, система знайде програму Python у `C:\opt\custompython\bin` (останній директорії) і використає саме її.

////

Отже, якщо ви введете:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Система **знайде** програму `python` у `/opt/custompython/bin` і запустить її.

Це буде приблизно еквівалентно введенню:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Система **знайде** програму `python` у `C:\opt\custompython\bin\python` і запустить її.

Це буде приблизно еквівалентно введенню:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Ця інформація буде корисною під час вивчення [Віртуальних середовищ](virtual-environments.md){.internal-link target=_blank}.

## Висновок { #conclusion }

Тепер у вас має бути базове розуміння того, що таке **змінні середовища** і як ними користуватися в Python.

Також ви можете прочитати більше про них у статті <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia про Environment Variable</a>.

У багатьох випадках не дуже очевидно, як змінні середовища можуть бути корисними й застосовними одразу. Але під час розробки вони з’являються в багатьох різних сценаріях, тож корисно знати про них.

Наприклад, вам знадобиться ця інформація в наступному розділі про [Віртуальні середовища](virtual-environments.md).
