# Editor Support { #editor-support }

سرکاری [FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) آپ کے FastAPI development workflow کو *path operation* کی دریافت، navigation، نیز FastAPI Cloud deployment، اور لائیو log streaming کے ساتھ بہتر بناتا ہے۔

Extension کے بارے میں مزید تفصیلات کے لیے، [GitHub repository](https://github.com/fastapi/fastapi-vscode) پر README دیکھیں۔

## سیٹ اپ اور Installation { #setup-and-installation }

**FastAPI Extension** [VS Code](https://code.visualstudio.com/) اور [Cursor](https://www.cursor.com/) دونوں کے لیے دستیاب ہے۔ اسے ہر editor میں Extensions پینل سے "FastAPI" تلاش کرکے اور **FastAPI Labs** کی شائع کردہ extension منتخب کرکے براہ راست install کیا جا سکتا ہے۔ یہ extension browser پر مبنی editors جیسے [vscode.dev](https://vscode.dev) اور [github.dev](https://github.dev) میں بھی کام کرتا ہے۔

### Application Discovery { #application-discovery }

بطور default، extension آپ کے workspace میں `FastAPI()` instantiate کرنے والی فائلوں کو scan کرکے خودکار طور پر FastAPI applications دریافت کرے گا۔ اگر auto-detection آپ کے project structure کے لیے کام نہ کرے، تو آپ `pyproject.toml` میں `[tool.fastapi]` کے ذریعے یا `fastapi.entryPoint` VS Code setting میں module notation (مثلاً `myapp.main:app`) استعمال کرکے entrypoint بتا سکتے ہیں۔

## Features { #features }

- **Path Operation Explorer** - آپ کی application میں تمام <dfn title="routes, endpoints">*path operations*</dfn> کا ایک sidebar tree view۔ کسی بھی route یا router definition تک جانے کے لیے کلک کریں۔
- **Route Search** - <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (macOS پر: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>) سے path، method، یا name سے تلاش کریں۔
- **CodeLens Navigation** - Test client calls (مثلاً `client.get('/items')`) کے اوپر کلک کرنے والے links جو مماثل *path operation* تک لے جاتے ہیں تاکہ tests اور implementation کے درمیان تیز navigation ہو۔
- **Deploy to FastAPI Cloud** - ایک کلک سے اپنی app کو [FastAPI Cloud](https://fastapicloud.com/) پر deploy کریں۔
- **Stream Application Logs** - اپنی FastAPI Cloud پر deploy شدہ application سے level filtering اور text search کے ساتھ real-time log streaming۔

اگر آپ extension کی features سے واقف ہونا چاہتے ہیں، تو Command Palette (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> یا macOS پر: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) کھول کر "Welcome: Open walkthrough..." منتخب کریں اور پھر "Get started with FastAPI" walkthrough چنیں۔
