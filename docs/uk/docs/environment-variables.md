# Змінні оточення { #environment-variables }

/// tip | Порада

Якщо ви вже знаєте, що таке «змінні оточення» і як їх використовувати, можете пропустити цей розділ.

///

Змінна оточення (також відома як «env var») - це змінна, що існує поза кодом Python, в операційній системі, і може бути прочитана вашим кодом Python (а також іншими програмами).

Змінні оточення корисні для роботи з налаштуваннями застосунку, як частина встановлення Python тощо.

## Створення і використання змінних оточення { #create-and-use-env-vars }

Ви можете створювати і використовувати змінні оточення в оболонці (терміналі) без участі Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Ви можете створити змінну оточення MY_NAME командою
$ export MY_NAME="Wade Wilson"

// Потім можна використати її з іншими програмами, наприклад
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Створіть змінну оточення MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Використайте її з іншими програмами, наприклад
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Читання змінних оточення в Python { #read-env-vars-in-python }

Ви також можете створити змінні оточення поза Python, у терміналі (або будь-яким іншим способом), а потім зчитати їх у Python.

Наприклад, у вас може бути файл `main.py` з:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Порада

Другий аргумент до <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> - це значення за замовчуванням, яке буде повернено.

Якщо його не вказано, за замовчуванням це `None`. Тут ми надаємо `"World"` як значення за замовчуванням.

///

Потім ви можете запустити цю програму Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Тут ми ще не встановлюємо змінну оточення
$ python main.py

// Оскільки ми не встановили змінну оточення, отримуємо значення за замовчуванням

Hello World from Python

// Але якщо спочатку створимо змінну оточення
$ export MY_NAME="Wade Wilson"

// А потім знову викличемо програму
$ python main.py

// Тепер вона може прочитати змінну оточення

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Тут ми ще не встановлюємо змінну оточення
$ python main.py

// Оскільки ми не встановили змінну оточення, отримуємо значення за замовчуванням

Hello World from Python

// Але якщо спочатку створимо змінну оточення
$ $Env:MY_NAME = "Wade Wilson"

// А потім знову викличемо програму
$ python main.py

// Тепер вона може прочитати змінну оточення

Hello Wade Wilson from Python
```

</div>

////

Оскільки змінні оточення можна встановлювати поза кодом, але читати в коді, і їх не потрібно зберігати (фіксувати у `git`) разом з іншими файлами, їх часто використовують для конфігурацій або налаштувань.

Ви також можете створити змінну оточення лише для конкретного запуску програми, вона буде доступна тільки цій програмі і лише на час її виконання.

Щоб зробити це, створіть її безпосередньо перед командою запуску програми, в тому самому рядку:

<div class="termy">

```console
// Створіть змінну оточення MY_NAME безпосередньо в цьому виклику програми
$ MY_NAME="Wade Wilson" python main.py

// Тепер вона може прочитати змінну оточення

Hello Wade Wilson from Python

// Після цього змінна оточення більше не існує
$ python main.py

Hello World from Python
```

</div>

/// tip | Порада

Докладніше про це можна прочитати у <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Типи і перевірка { #types-and-validation }

Ці змінні оточення можуть містити лише текстові строки, оскільки вони зовнішні щодо Python і мають бути сумісними з іншими програмами та рештою системи (і навіть з різними операційними системами, як-от Linux, Windows, macOS).

Це означає, що будь-яке значення, прочитане в Python зі змінної оточення, буде `str`, а будь-яке перетворення до іншого типу або будь-яка перевірка має виконуватися в коді.

Ви дізнаєтеся більше про використання змінних оточення для роботи з налаштуваннями застосунку в розділі [Просунутий посібник користувача - Налаштування і змінні оточення](./advanced/settings.md){.internal-link target=_blank}.

## Змінна оточення `PATH` { #path-environment-variable }

Є спеціальна змінна оточення `PATH`, яку використовують операційні системи (Linux, macOS, Windows) для пошуку програм для запуску.

Значення змінної `PATH` - це довга строка, що складається з каталогів, розділених двокрапкою `:` у Linux і macOS та крапкою з комою `;` у Windows.

Наприклад, змінна оточення `PATH` може виглядати так:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Це означає, що система має шукати програми в каталогах:

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

Це означає, що система має шукати програми в каталогах:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Коли ви вводите команду в терміналі, операційна система шукає програму в кожному з тих каталогів, перелічених у змінній оточення `PATH`.

Наприклад, коли ви вводите `python` у терміналі, операційна система шукає програму з назвою `python` у першому каталозі цього списку.

Якщо знайде, вона використає її. Інакше продовжить пошук в інших каталогах.

### Встановлення Python і оновлення `PATH` { #installing-python-and-updating-the-path }

Під час встановлення Python вас можуть запитати, чи хочете ви оновити змінну оточення `PATH`.

//// tab | Linux, macOS

Припустімо, ви встановлюєте Python і він опиняється в каталозі `/opt/custompython/bin`.

Якщо ви погодитеся оновити змінну оточення `PATH`, інсталятор додасть `/opt/custompython/bin` до змінної `PATH`.

Це може виглядати так:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Тепер, коли ви введете `python` у терміналі, система знайде програму Python у `/opt/custompython/bin` (останній каталог) і використає саме її.

////

//// tab | Windows

Припустімо, ви встановлюєте Python і він опиняється в каталозі `C:\opt\custompython\bin`.

Якщо ви погодитеся оновити змінну оточення `PATH`, інсталятор додасть `C:\opt\custompython\bin` до змінної `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Тепер, коли ви введете `python` у терміналі, система знайде програму Python у `C:\opt\custompython\bin` (останній каталог) і використає саме її.

////

Отже, якщо ви введете:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Система знайде програму `python` у `/opt/custompython/bin` і запустить її.

Це приблизно еквівалентно введенню:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Система знайде програму `python` у `C:\opt\custompython\bin\python` і запустить її.

Це приблизно еквівалентно введенню:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Ця інформація стане у пригоді під час вивчення [Віртуальних середовищ](virtual-environments.md){.internal-link target=_blank}.

## Висновок { #conclusion }

Тепер ви маєте базове розуміння того, що таке змінні оточення і як їх використовувати в Python.

Також можна прочитати більше у <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Вікіпедії про змінну оточення</a>.

У багатьох випадках не одразу очевидно, як змінні оточення будуть корисними та застосовними. Але вони постійно з’являються в різних сценаріях під час розробки, тож варто про них знати.

Наприклад, вам знадобиться ця інформація в наступному розділі про [Віртуальні середовища](virtual-environments.md).
