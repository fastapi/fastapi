# Virtual Environments { #virtual-environments }

Python projects নিয়ে কাজ করার সময়, প্রতিটি project-এর জন্য install করা packages আলাদা রাখতে একটি **virtual environment** ব্যবহার করা উচিত।

FastAPI projects-এর জন্য project, এর dependencies আর virtual environment manage করতে আমি [uv](https://docs.astral.sh/uv/) ব্যবহার করার পরামর্শ দিই।

## একটি Project বানান { #create-a-project }

[official installation guide](https://docs.astral.sh/uv/getting-started/installation/) দেখে `uv` install করুন, তারপর একটি project বানান:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` project-এর জন্য নিজে থেকেই একটি virtual environment বানায়। আপনাকে নিজে বানাতে বা activate করতে হবে না।

project environment-এর ভেতরে commands চালান `uv run` দিয়ে, যেমন:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## আরও জানুন { #learn-more }

virtual environments ভেতরে ভেতরে কীভাবে কাজ করে, activation আর বিকল্প `python -m venv` ও `pip` workflow সহ, সেটা শিখতে [Virtual Environments guide](https://tiangolo.com/guides/virtual-environments/) পড়ুন।
