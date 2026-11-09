# Editor Support { #editor-support }

official [FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) আপনার FastAPI development workflow আরও ভালো করে: *path operation* discovery, navigation, সাথে FastAPI Cloud deployment আর live log streaming।

extension নিয়ে আরও জানতে [GitHub repository](https://github.com/fastapi/fastapi-vscode)-র README দেখুন।

## Setup আর Installation { #setup-and-installation }

**FastAPI Extension** [VS Code](https://code.visualstudio.com/) আর [Cursor](https://www.cursor.com/) দুটোর জন্যই পাওয়া যায়। প্রতিটি editor-এর Extensions panel-এ "FastAPI" লিখে খুঁজে **FastAPI Labs**-এর publish করা extension-টা বেছে নিয়ে সরাসরি install করা যায়। extension-টা [vscode.dev](https://vscode.dev) আর [github.dev](https://github.dev)-এর মতো browser-ভিত্তিক editors-এও কাজ করে।

### Application Discovery { #application-discovery }

default-ভাবে extension-টা আপনার workspace-এ `FastAPI()` instantiate করা files খুঁজে নিজে থেকেই FastAPI applications বের করে নেয়। আপনার project structure-এ auto-detection কাজ না করলে, `pyproject.toml`-এ `[tool.fastapi]` দিয়ে, বা `fastapi.entryPoint` VS Code setting দিয়ে module notation-এ (যেমন `myapp.main:app`) একটি entrypoint দিতে পারেন।

## Features { #features }

- **Path Operation Explorer** - আপনার application-এর সব <dfn title="routes, endpoints">*path operations*</dfn>-এর একটি sidebar tree view। যেকোনো route বা router definition-এ যেতে click করুন।
- **Route Search** - path, method বা name দিয়ে খুঁজুন <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> দিয়ে (macOS-এ: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>)।
- **CodeLens Navigation** - test client calls-এর (যেমন `client.get('/items')`) উপরে click করার মতো links, যেগুলো মিলে যাওয়া *path operation*-এ নিয়ে যায়, tests আর implementation-এর মধ্যে দ্রুত যাতায়াতের জন্য।
- **Deploy to FastAPI Cloud** - এক click-এ আপনার app [FastAPI Cloud](https://fastapicloud.com/)-এ deploy।
- **Stream Application Logs** - FastAPI Cloud-এ deploy করা application থেকে real-time log streaming, level filtering আর text search সহ।

extension-এর features-এর সাথে পরিচিত হতে চাইলে Command Palette খুলে (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>, বা macOS-এ: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) "Welcome: Open walkthrough..." বেছে নিন, তারপর "Get started with FastAPI" walkthrough-টা বেছে নিন।

## AI coding agents { #ai-coding-agents }

official FastAPI skill install আর ব্যবহার করতে [Develop with AI](ai-development.md) দেখুন।
