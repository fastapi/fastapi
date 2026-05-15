# Editör Desteği { #editor-support }

Resmi [FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode), FastAPI geliştirme akışınızı iyileştirir: *path operation* keşfi, gezinme, FastAPI Cloud’a deploy ve canlı log akışı.

Daha fazla ayrıntı için, GitHub deposundaki README’ye bakın: [GitHub repository](https://github.com/fastapi/fastapi-vscode).

## Kurulum ve Yükleme { #setup-and-installation }

**FastAPI Extension**, hem [VS Code](https://code.visualstudio.com/) hem de [Cursor](https://www.cursor.com/) için mevcuttur. Her editörde Extensions panelinden "FastAPI" aratıp **FastAPI Labs** tarafından yayımlanan eklentiyi seçerek doğrudan kurabilirsiniz. Eklenti [vscode.dev](https://vscode.dev) ve [github.dev](https://github.dev) gibi tarayıcı tabanlı editörlerde de çalışır.

### Uygulama Keşfi { #application-discovery }

Varsayılan olarak, eklenti çalışma alanınızda `FastAPI()` örnekleyen dosyaları tarayarak FastAPI uygulamalarını otomatik olarak keşfeder. Proje yapınız nedeniyle otomatik algılama çalışmazsa, `pyproject.toml` içindeki `[tool.fastapi]` ile veya VS Code ayarı `fastapi.entryPoint` üzerinden modül gösterimiyle (ör. `myapp.main:app`) bir entrypoint belirtebilirsiniz.

## Özellikler { #features }

- **Path Operation Explorer** - Uygulamanızdaki tüm <dfn title="route'lar, endpoint'ler">*path operation*'lar</dfn> için yan panelde bir ağaç görünümü. Herhangi bir route veya router tanımına tıklayarak atlayın.
- **Route Search** - <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>) ile path, method veya ada göre arama.
- **CodeLens Navigation** - Test client çağrılarının (ör. `client.get('/items')`) üzerinde, ilgili *path operation*’a atlayan tıklanabilir bağlantılar; testlerle implementasyon arasında hızlı gezinme sağlar.
- **Deploy to FastAPI Cloud** - Uygulamanızı tek tıkla [FastAPI Cloud](https://fastapicloud.com/)'a deploy edin.
- **Stream Application Logs** - FastAPI Cloud’a deploy ettiğiniz uygulamadan, seviye filtreleme ve metin arama ile gerçek zamanlı log akışı.

Eklentinin özelliklerine hızlıca aşina olmak isterseniz, Komut Paleti’ni açın (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> veya macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>), "Welcome: Open walkthrough..." öğesini seçin ve ardından "Get started with FastAPI" walkthrough’unu açın.
