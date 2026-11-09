# Tutorial - User Guide { #tutorial-user-guide }

এই tutorial আপনাকে ধাপে ধাপে দেখাবে কীভাবে **FastAPI**-এর বেশিরভাগ feature ব্যবহার করবেন।

প্রতিটি section আগেরগুলোর উপর একটু একটু করে গড়ে ওঠে, কিন্তু topic অনুযায়ী আলাদা করে সাজানো, যাতে আপনার API-এর নির্দিষ্ট কোনো দরকার মেটাতে সরাসরি সেই section-এ চলে যেতে পারেন।

এটা এমনভাবে বানানো যে পরেও reference হিসেবে কাজে লাগবে, যখন দরকার ফিরে এসে ঠিক যেটা লাগবে সেটা দেখে নিতে পারবেন।

## Code চালান { #run-the-code }

সব code blocks copy করে সরাসরি ব্যবহার করা যায় (এগুলো আসলে tested Python files)।

যেকোনো উদাহরণ চালাতে, code-টা একটি `main.py` file-এ copy করুন, তারপর `uv run` দিয়ে `fastapi dev` চালু করুন:

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

আপনি নিজে code লিখুন বা copy করুন, বদলান এবং local-এ চালান, এটা **খুবই recommended**।

Editor-এ ব্যবহার করলেই আসলে FastAPI-এর সুবিধাগুলো বোঝা যায়: কত কম code লিখতে হয়, সব type checks, autocompletion, ইত্যাদি।

---

## FastAPI install করুন { #install-fastapi }

প্রথম ধাপ হলো আপনার project set up করা আর FastAPI যোগ করা।

[`uv`](https://docs.astral.sh/uv/getting-started/installation/) install করুন, তারপর একটি project বানিয়ে FastAPI যোগ করুন:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` project-এর virtual environment `.venv`-এ বানায়, `pyproject.toml`-এ FastAPI যোগ করে, আর `uv.lock` বানায়, যাতে পরে ঠিক একই package versions install করা যায়।

/// details | এই commands কী করে

* `uv init`: একটি নতুন Python project বানায়।
* `awesome-project`: এই নামে একটি নতুন directory-তে project বানায়।
* `--bare`: শুধু সবচেয়ে ছোট `pyproject.toml` file বানায়, sample `main.py`, `README.md` বা অন্য কোনো file ছাড়াই। application files আপনি নিজেই এই tutorial-এর পরের ধাপগুলোতে বানাবেন।

তারপর FastAPI যোগ করার আগে `cd awesome-project` দিয়ে নতুন project directory-তে ঢোকা হয়।

`uv` আপনার system-এ আগে থেকে install করা compatible কোনো Python version ব্যবহার করবে, অথবা দরকার হলে download করে নেবে।

`uv add` চালালে এটা FastAPI আর FastAPI যেসব package-এর উপর নির্ভর করে, সেগুলোর compatible versions বেছে নেয়। ঠিক কোন versions, সেটা `uv.lock`-এ লিখে রাখে, যাতে পরে অন্য computer-এ বা application deploy করার সময় ঠিক একই package versions install করা যায়।

এই file বানানো বা update করাকে বলে [project dependencies **locking**](https://docs.astral.sh/uv/concepts/projects/sync/)। কোনো package যোগ করলে `uv` এটা নিজে থেকেই করে।

///

/// details | FastAPI installation options

`uv add "fastapi[standard]"` দিয়ে install করলে কিছু default optional standard dependencies সাথে আসে, যার মধ্যে `fastapi-cloud-cli` আছে, যেটা দিয়ে [FastAPI Cloud](https://fastapicloud.com)-এ deploy করা যায়।

ওই optional dependencies না চাইলে এর বদলে `uv add fastapi` দিয়ে install করতে পারেন।

standard dependencies চান কিন্তু `fastapi-cloud-cli` ছাড়া, তাহলে `uv add "fastapi[standard-no-fastapi-cloud-cli]"` দিয়ে install করুন।

///

/// details | এর বদলে `pip` ব্যবহার করা

আপনি যদি virtual environment আর packages নিজে হাতে manage করতে চান, তাহলে একটি virtual environment বানিয়ে activate করুন, তারপর `pip install "fastapi[standard]"` দিয়ে FastAPI install করুন।

বিস্তারিত ধাপের জন্য [Virtual Environments guide](https://tiangolo.com/guides/virtual-environments/) পড়ুন।

///

## AI Agent Skills { #ai-agent-skills }

AI coding agents-এর জন্য FastAPI-এর সাথে একটি official skill আসে। এটা package-এর সাথেই bundled, তাই এর guidance আপনার project-এ install করা FastAPI version-এর সাথে মিলে থাকে, আর FastAPI update করলে এটাও update হয়।

আপনার project-এ FastAPI install করার পর <a href="https://library-skills.io">Library Skills</a> দিয়ে skill-টা install করতে পারেন:

```bash
uvx library-skills
```

/// note | Note

`uvx` হলো `uv tool run`-এর alias। এটা Library Skills-কে একটি temporary, আলাদা environment-এ চালায়, আর Library Skills আপনার project-এ install করা packages scan করে।

///

এই skill Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode সহ বেশিরভাগ coding agent-এর সাথে কাজ করে। Claude Code-এর জন্য, skill কোথায় install করবেন জিজ্ঞেস করলে `.claude/skills` বেছে নিন।

আরও জানতে [Develop with AI](../ai-development.md) দেখুন।

## Advanced User Guide { #advanced-user-guide }

একটি **Advanced User Guide**-ও আছে, যেটা এই **Tutorial - User Guide**-এর পরে পড়তে পারেন।

**Advanced User Guide** এটার উপরেই গড়ে উঠেছে, একই concepts ব্যবহার করে, আর আপনাকে কিছু extra features শেখায়।

কিন্তু আগে **Tutorial - User Guide** (যেটা আপনি এখন পড়ছেন) পড়ে নেওয়া উচিত।

এটা এমনভাবে design করা যে শুধু **Tutorial - User Guide** দিয়েই একটি পুরো application বানাতে পারবেন, তারপর আপনার দরকার অনুযায়ী **Advanced User Guide**-এর কিছু বাড়তি idea দিয়ে সেটাকে নানাভাবে বাড়াতে পারবেন।
