# Розробляйте з ШІ { #develop-with-ai }

FastAPI містить офіційну **навичку агента**, що постачається з пакетом Python і надає рекомендації для версії, встановленої у вашому проєкті.

## Установіть навичку { #install-the-skill }

Після [встановлення FastAPI](tutorial/index.md#install-fastapi) запустіть [Library Skills](https://library-skills.io/use/) з каталогу вашого проєкту:

```bash
uvx library-skills
```

Виберіть навичку FastAPI та `.agents/skills` для Codex і більшості агентів або `.claude/skills` для Claude Code. Ви можете вибрати обидва варіанти.

Після цього ваш агент зможе автоматично використовувати навичку під час роботи з кодом FastAPI.

### Установіть без підсказок { #install-without-prompts }

Для агентів і скриптів виберіть навичку FastAPI без інтерактивних підсказок:

```bash
uvx library-skills install --skill fastapi --yes
```

Для Claude Code додайте `--claude`, щоб також установити її в `.claude/skills`:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Налаштуйте застосунок { #configure-your-app }

Налаштуйте [точку входу застосунку](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) у `pyproject.toml`, щоб інструменти FastAPI могли знайти ваш застосунок:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Використовуйте назву модуля та ім'я змінної вашого застосунку. Тут `main:app` посилається на об'єкт `app` у `main.py`.

## Запустіть застосунок { #run-your-app }

Використовуйте [FastAPI CLI](fastapi-cli.md) для локальної розробки:

```bash
uv run fastapi dev
```

Для промислового середовища використовуйте `uv run fastapi run`.

## Згенеруйте SDK { #generate-an-sdk }

Для розробки фронтенду та клієнтів API дивіться [Генерування SDK](advanced/generate-clients.md).

## Розгорніть застосунок { #deploy-your-app }

Щоб розгорнути застосунок у [FastAPI Cloud](deployment/fastapicloud.md), офіційній керованій платформі розгортання від команди FastAPI:

```bash
uv run fastapi deploy
```

Ви також можете [розгорнути застосунок вручну](deployment/manually.md) в іншого хмарного провайдера або на власному сервері.

## Плагіни для агентів { #agent-plugins }

[Плагіни FastAPI Cloud для Codex і Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) містять інструкції зі створення проєктів і використання навичок бібліотек, що постачаються з вашими залежностями. Вони корисні, навіть якщо ви не використовуєте FastAPI Cloud.

Вони також охоплюють розгортання у FastAPI Cloud, журнали та змінні оточення.
