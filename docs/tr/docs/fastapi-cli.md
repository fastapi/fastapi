# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - komut satırı arayüzü">CLI</abbr>**, FastAPI uygulamanızı servis etmek, FastAPI projenizi yönetmek ve daha fazlası için kullanabileceğiniz bir komut satırı programıdır.

FastAPI'yi kurduğunuzda (ör. `pip install "fastapi[standard]"`), terminalde çalıştırabileceğiniz bir komut satırı programı birlikte gelir.

FastAPI uygulamanızı geliştirme için çalıştırmak üzere `fastapi dev` komutunu kullanabilirsiniz:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

/// tip | İpucu

Production için `fastapi dev` yerine `fastapi run` kullanırsınız. 🚀

///

İçeride, **FastAPI CLI**, yüksek performanslı, production'a hazır bir ASGI server olan [Uvicorn](https://www.uvicorn.dev)'u kullanır. 😎

`fastapi` CLI, çalıştırılacak FastAPI app'ini otomatik olarak tespit etmeye çalışır; `main.py` dosyasında `app` adlı bir nesne olduğunu varsayar (veya birkaç başka varyant).

Ancak, kullanılacak app'i açıkça yapılandırabilirsiniz.

## Uygulama `entrypoint`'ini `pyproject.toml` İçinde Yapılandırma { #configure-the-app-entrypoint-in-pyproject-toml }

Uygulamanızın nerede olduğunu aşağıdaki gibi bir `pyproject.toml` dosyasında yapılandırabilirsiniz:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Bu `entrypoint`, `fastapi` komutuna app'i şu şekilde import etmesi gerektiğini söyler:

```python
from main import app
```

Kodunuz şu şekilde yapılandırılmışsa:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

O zaman `entrypoint`'i şu şekilde ayarlarsınız:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

Bu da şu koda eşdeğerdir:

```python
from backend.main import app
```

### path ile `fastapi dev` { #fastapi-dev-with-path }

Ayrıca `fastapi dev` komutuna dosya path'ini de verebilirsiniz; hangi FastAPI app nesnesinin kullanılacağını tahmin eder:

```console
$ fastapi dev main.py
```

Ancak `fastapi` komutunu her çağırdığınızda doğru path'i geçmeyi hatırlamanız gerekir.

Ayrıca, [VS Code Extension](editor-support.md) veya [FastAPI Cloud](https://fastapicloud.com) gibi diğer araçlar da bunu bulamayabilir; bu yüzden `pyproject.toml` içindeki `entrypoint`'i kullanmanız önerilir.

## `fastapi dev` { #fastapi-dev }

`fastapi dev` çalıştırmak, geliştirme modunu başlatır.

Varsayılan olarak **auto-reload** etkindir; kodunuzda değişiklik yaptığınızda server'ı otomatik olarak yeniden yükler. Bu, kaynak tüketimi yüksek bir özelliktir ve kapalı olduğuna kıyasla daha az stabil olabilir. Sadece geliştirme sırasında kullanmalısınız. Ayrıca yalnızca `127.0.0.1` IP adresini dinler; bu, makinenizin sadece kendisiyle iletişim kurması için kullanılan IP'dir (`localhost`).

## `fastapi run` { #fastapi-run }

`fastapi run` çalıştırmak, varsayılan olarak FastAPI'yi production modunda başlatır.

Varsayılan olarak **auto-reload** kapalıdır. Ayrıca `0.0.0.0` IP adresini dinler; bu, kullanılabilir tüm IP adresleri anlamına gelir. Böylece makineyle iletişim kurabilen herkes tarafından genel erişime açık olur. Bu, normalde production'da çalıştırma şeklidir; örneğin bir container içinde.

Çoğu durumda (ve genellikle yapmanız gereken şekilde) üst tarafta sizin yerinize HTTPS'i yöneten bir "termination proxy" bulunur. Bu, uygulamanızı nasıl deploy ettiğinize bağlıdır; sağlayıcınız bunu sizin için yapabilir ya da sizin ayrıca kurmanız gerekebilir.

/// tip | İpucu

Bununla ilgili daha fazla bilgiyi [deployment dokümantasyonunda](deployment/index.md) bulabilirsiniz.

///
