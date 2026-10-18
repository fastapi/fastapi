# Навчальний посібник - Посібник користувача { #tutorial-user-guide }

У цьому посібнику показано, як користуватися **FastAPI** з більшістю його функцій, крок за кроком.

Кожен розділ поступово надбудовується на попередні, але він структурований на окремі теми, щоб ви могли перейти безпосередньо до будь-якої конкретної, щоб вирішити ваші конкретні потреби API.

Також він створений як довідник для роботи у майбутньому, тож ви можете повернутися і побачити саме те, що вам потрібно.

## Запустіть код { #run-the-code }

Усі блоки коду можна скопіювати та використовувати безпосередньо (це фактично перевірені файли Python).

Щоб запустити будь-який із прикладів, скопіюйте код у файл `main.py` і запустіть `fastapi dev` за допомогою `uv run`:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

**ДУЖЕ радимо** написати або скопіювати код, відредагувати його та запустити локально.

Використання його у своєму редакторі - це те, що дійсно показує вам переваги FastAPI, бачите, як мало коду вам потрібно написати, всі перевірки типів, автозаповнення тощо.

---

## Встановлення FastAPI { #install-fastapi }

Першим кроком є налаштування вашого проєкту та додавання FastAPI.

Встановіть [`uv`](https://docs.astral.sh/uv/getting-started/installation/), потім створіть проєкт і додайте FastAPI:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` створює віртуальне середовище проєкту в `.venv`, додає FastAPI до `pyproject.toml` і створює `uv.lock`, щоб ті самі версії пакетів можна було встановити пізніше.

/// details | Що роблять ці команди

* `uv init`: створює новий Python-проєкт.
* `awesome-project`: створює проєкт у новому каталозі з цією назвою.
* `--bare`: створює лише мінімальний файл `pyproject.toml`, без генерування прикладу `main.py`, `README.md` або інших файлів. Ви створите файли застосунку самостійно в наступних кроках цього навчального посібника.

Потім `cd awesome-project` входить до нового каталогу проєкту перед додаванням FastAPI.

`uv` використовуватиме сумісну версію Python, уже встановлену у вашій системі, або завантажить її за потреби.

Коли ви запускаєте `uv add`, він вибирає сумісні версії FastAPI та всіх пакетів, від яких залежить FastAPI. Він записує точні версії в `uv.lock`, що дає змогу встановити ті самі версії пакетів пізніше на іншому комп'ютері або під час розгортання застосунку.

Створення або оновлення цього файлу називається [**закріпленням** залежностей проєкту](https://docs.astral.sh/uv/concepts/projects/sync/). `uv` робить це автоматично, коли ви додаєте пакет.

///

/// details | Варіанти встановлення FastAPI

Коли ви встановлюєте через `uv add "fastapi[standard]"`, він постачається з деякими типовими необов'язковими стандартними залежностями, включно з `fastapi-cloud-cli`, який дозволяє розгортати в [FastAPI Cloud](https://fastapicloud.com).

Якщо ви не хочете мати ці необов'язкові залежності, натомість можете встановити `uv add fastapi`.

Якщо ви хочете встановити стандартні залежності, але без `fastapi-cloud-cli`, ви можете встановити через `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// details | Натомість використання `pip`

Якщо ви віддаєте перевагу керуванню віртуальним середовищем і пакетами вручну, створіть і активуйте віртуальне середовище, а потім встановіть FastAPI за допомогою `pip install "fastapi[standard]"`.

Прочитайте [посібник з віртуальних середовищ](https://tiangolo.com/guides/virtual-environments/) для детальних кроків.

///

## Навички AI-агента { #ai-agent-skills }

FastAPI включає офіційну навичку для AI-агентів для кодування. Вона постачається з пакетом, тому її настанови залишаються узгодженими з версією FastAPI, встановленою у вашому проєкті, і оновлюються, коли ви оновлюєте FastAPI.

Після встановлення FastAPI у вашому проєкті ви можете встановити навичку за допомогою <a href="https://library-skills.io">Library Skills</a>:

```bash
uvx library-skills
```

/// note | Примітка

`uvx` - це псевдонім для `uv tool run`. Він запускає Library Skills у тимчасовому ізольованому середовищі, поки Library Skills сканує пакети, встановлені у вашому проєкті.

///

Навичка сумісна з Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode і більшістю інших агентів для кодування. Для Claude Code виберіть `.claude/skills`, коли вас запитають, куди встановити навичку.

## Просунутий посібник користувача { #advanced-user-guide }

Існує також **Просунутий посібник користувача**, який ви зможете прочитати пізніше після цього **Навчальний посібник - Посібник користувача**.

**Просунутий посібник користувача** засновано на цьому, використовує ті самі концепції та навчає вас деяким додатковим функціям.

Але вам слід спочатку прочитати **Навчальний посібник - Посібник користувача** (те, що ви зараз читаєте).

Він розроблений таким чином, що ви можете створити повну програму лише за допомогою **Навчальний посібник - Посібник користувача**, а потім розширити її різними способами, залежно від ваших потреб, використовуючи деякі з додаткових ідей з **Просунутого посібника користувача**.
