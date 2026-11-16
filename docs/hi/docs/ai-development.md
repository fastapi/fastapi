# AI के साथ development करें { #develop-with-ai }

FastAPI में एक आधिकारिक **agent skill** शामिल है, जो Python package के साथ आती है और आपके project में install किए गए संस्करण के लिए मार्गदर्शन देती है।

## Skill install करें { #install-the-skill }

[FastAPI install करने](tutorial/index.md#install-fastapi) के बाद, अपने project की directory से [Library Skills](https://library-skills.io/use/) चलाएँ:

```bash
uvx library-skills
```

FastAPI skill चुनें और Codex तथा अधिकांश agents के लिए `.agents/skills`, या Claude Code के लिए `.claude/skills` चुनें। आप दोनों चुन सकते हैं।

इसके बाद आपका agent FastAPI कोड पर काम करते समय अपने आप इस skill का उपयोग कर सकता है।

### Prompts के बिना install करें { #install-without-prompts }

Agents और scripts के लिए, interactive prompts के बिना FastAPI skill चुनें:

```bash
uvx library-skills install --skill fastapi --yes
```

Claude Code के लिए, इसे `.claude/skills` में भी install करने के लिए `--claude` जोड़ें:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## अपना ऐप कॉन्फ़िगर करें { #configure-your-app }

`pyproject.toml` में [ऐप का entrypoint](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) कॉन्फ़िगर करें, ताकि FastAPI tools आपका ऐप ढूँढ़ सकें:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

अपने ऐप के module और variable का नाम उपयोग करें। यहाँ, `main:app` का अर्थ `main.py` में मौजूद `app` object है।

## अपना ऐप चलाएँ { #run-your-app }

स्थानीय development के लिए [FastAPI CLI](fastapi-cli.md) का उपयोग करें:

```bash
uv run fastapi dev
```

Production के लिए, `uv run fastapi run` का उपयोग करें।

## SDK जनरेट करें { #generate-an-sdk }

Frontend और API client development के लिए, [SDK जनरेट करना](advanced/generate-clients.md) देखें।

## अपना ऐप डिप्लॉय करें { #deploy-your-app }

FastAPI team के आधिकारिक managed deployment platform, [FastAPI Cloud](deployment/fastapicloud.md), पर डिप्लॉय करने के लिए:

```bash
uv run fastapi deploy
```

आप किसी अन्य cloud provider या अपने सर्वर पर भी [मैन्युअल रूप से डिप्लॉय](deployment/manually.md) कर सकते हैं।

## Agent plugins { #agent-plugins }

[Codex और Claude Code के लिए FastAPI Cloud plugins](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) में project बनाने और आपकी dependencies के साथ आने वाली library skills का उपयोग करने के निर्देश शामिल हैं। ये तब भी उपयोगी हैं जब आप FastAPI Cloud का उपयोग नहीं करते हैं।

इनमें FastAPI Cloud deployment, logs और environment variables के बारे में भी जानकारी दी गई है।
