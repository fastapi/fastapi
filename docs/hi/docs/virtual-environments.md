# Virtual Environments { #virtual-environments }

जब आप Python projects पर काम करते हैं, तो आपको हर project के लिए install किए गए packages को अलग रखने के लिए एक **virtual environment** का उपयोग करना चाहिए।

FastAPI projects के लिए, मैं project, उसकी dependencies, और उसके virtual environment को manage करने के लिए [uv](https://docs.astral.sh/uv/) उपयोग करने की सलाह देता हूँ।

## Project बनाएँ { #create-a-project }

[official installation guide](https://docs.astral.sh/uv/getting-started/installation/) का उपयोग करके `uv` install करें, और फिर एक project बनाएँ:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` project के लिए virtual environment automatically बनाता है। आपको खुद कोई बनाने या activate करने की ज़रूरत नहीं है।

Project environment के अंदर commands `uv run` से चलाएँ, उदाहरण के लिए:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## और जानें { #learn-more }

Virtual environments अंदर से कैसे काम करते हैं, यह जानने के लिए [Virtual Environments guide](https://tiangolo.com/guides/virtual-environments/) पढ़ें, जिसमें activation और alternative `python -m venv` और `pip` workflow शामिल हैं।
