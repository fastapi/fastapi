# एडिटर समर्थन { #editor-support }

आधिकारिक [FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) आपके FastAPI डेवलपमेंट workflow को *path operation* discovery, navigation, साथ ही FastAPI Cloud deployment और live log streaming के साथ बेहतर बनाता है।

Extension के बारे में अधिक जानकारी के लिए, [GitHub repository](https://github.com/fastapi/fastapi-vscode) पर README देखें।

## सेटअप और इंस्टॉलेशन { #setup-and-installation }

**FastAPI Extension** [VS Code](https://code.visualstudio.com/) और [Cursor](https://www.cursor.com/) दोनों के लिए उपलब्ध है। इसे प्रत्येक एडिटर के Extensions panel से सीधे इंस्टॉल किया जा सकता है, "FastAPI" खोजकर और **FastAPI Labs** द्वारा प्रकाशित extension चुनकर। यह extension browser-based editors जैसे [vscode.dev](https://vscode.dev) और [github.dev](https://github.dev) में भी काम करता है।

### एप्लिकेशन डिस्कवरी { #application-discovery }

डिफ़ॉल्ट रूप से, extension आपके workspace में `FastAPI()` instantiate करने वाली files को scan करके FastAPI applications को अपने आप discover करेगा। यदि auto-detection आपके project structure के लिए काम नहीं करता, तो आप `pyproject.toml` में `[tool.fastapi]` के माध्यम से या module notation (जैसे `myapp.main:app`) का उपयोग करके `fastapi.entryPoint` VS Code setting में entrypoint निर्दिष्ट कर सकते हैं।

## सुविधाएँ { #features }

- **Path Operation Explorer** - आपके application में सभी <dfn title="रूट्स, एंडपॉइंट्स">*path operations*</dfn> का sidebar tree view। किसी भी route या router definition पर जाने के लिए क्लिक करें।
- **Route Search** - path, method, या name के आधार पर <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (macOS पर: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>) से search करें।
- **CodeLens Navigation** - test client calls (जैसे `client.get('/items')`) के ऊपर clickable links, जो tests और implementation के बीच तेज़ navigation के लिए matching *path operation* पर ले जाते हैं।
- **Deploy to FastAPI Cloud** - अपनी app को [FastAPI Cloud](https://fastapicloud.com/) पर one-click deployment।
- **Stream Application Logs** - level filtering और text search के साथ, आपकी FastAPI Cloud-deployed application से real-time log streaming।

यदि आप extension की सुविधाओं से परिचित होना चाहते हैं, तो Command Palette (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> या macOS पर: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>) खोलकर और "Welcome: Open walkthrough..." चुनकर, फिर "Get started with FastAPI" walkthrough चुनकर extension walkthrough देख सकते हैं।
