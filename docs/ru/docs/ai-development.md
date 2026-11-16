# Разработка с ИИ { #develop-with-ai }

FastAPI включает официальный **навык для ИИ-агента**, который поставляется вместе с Python-пакетом и содержит рекомендации для версии, установленной в вашем проекте.

## Установка навыка { #install-the-skill }

После [установки FastAPI](tutorial/index.md#install-fastapi) запустите [Library Skills](https://library-skills.io/use/) из каталога вашего проекта:

```bash
uvx library-skills
```

Выберите навык FastAPI и `.agents/skills` для Codex и большинства агентов или `.claude/skills` для Claude Code. Можно выбрать оба варианта.

После этого ваш агент сможет автоматически использовать навык при работе с кодом FastAPI.

### Установка без интерактивных запросов { #install-without-prompts }

Для агентов и скриптов выберите навык FastAPI без интерактивных запросов:

```bash
uvx library-skills install --skill fastapi --yes
```

Для Claude Code добавьте `--claude`, чтобы также установить его в `.claude/skills`:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Настройка приложения { #configure-your-app }

Настройте [точку входа приложения](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) в `pyproject.toml`, чтобы инструменты FastAPI могли найти ваше приложение:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Укажите модуль и имя переменной вашего приложения. Здесь `main:app` обозначает объект `app` в `main.py`.

## Запуск приложения { #run-your-app }

Используйте [FastAPI CLI](fastapi-cli.md) для локальной разработки:

```bash
uv run fastapi dev
```

Для продакшн используйте `uv run fastapi run`.

## Генерация SDK { #generate-an-sdk }

Для разработки фронтенда и API-клиентов см. раздел [Генерация SDK](advanced/generate-clients.md).

## Развертывание приложения { #deploy-your-app }

Для развертывания в [FastAPI Cloud](deployment/fastapicloud.md), официальной управляемой платформе развертывания от команды FastAPI:

```bash
uv run fastapi deploy
```

Вы также можете [развернуть приложение вручную](deployment/manually.md) у другого облачного провайдера или на собственном сервере.

## Плагины для агентов { #agent-plugins }

[Плагины FastAPI Cloud для Codex и Claude Code](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/) содержат инструкции по созданию проектов и использованию навыков библиотек, поставляемых вместе с вашими зависимостями. Они полезны, даже если вы не используете FastAPI Cloud.

Они также охватывают развертывание в FastAPI Cloud, логи и переменные окружения.
