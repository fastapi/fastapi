# FastAPI CLI

**FastAPI CLI** é uma interface por linha de comando do `fastapi` que você pode usar para rodar sua app FastAPI, gerenciar seu projeto FastAPI e mais.

Quando você instala o FastAPI (ex.: com `pip install fastapi`), isso inclui um pacote chamado `fastapi-cli`. Esse pacote disponibiliza o comando `fastapi` no terminal.

Para rodar seu app FastAPI em desenvolvimento, você pode usar o comando `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
```

</div>

Aquele commando por linha de programa chamado `fastapi` é o **FastAPI CLI**.

O FastAPI CLI recebe o caminho do seu programa Python, detecta automaticamente a variável com o FastAPI (comumente nomeada `app`) e como importá-la, e então a serve.

Para produção você usaria `fastapi run` no lugar. 🚀

Internamente, **FastAPI CLI** usa <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a>, um servidor ASGI de alta performance e pronto para produção. 😎

## `fastapi dev`

Quando você roda `fastapi dev`, isso vai executar em modo de desenvolvimento.

Por padrão, teremos o **recarregamento automático** ativo, então o programa irá recarregar o servidor automaticamente toda vez que você fizer mudanças no seu código. Isso usa muitos recursos e pode ser menos estável. Você deve apenas usá-lo em modo de desenvolvimento.

O servidor de desenvolvimento escutará no endereço de IP `127.0.0.1` por padrão, este é o IP que sua máquina usa para se comunicar com ela mesma (`localhost`).

## `fastapi run`

Quando você rodar `fastapi run`, isso executará em modo de produção por padrão.

Este modo terá **recarregamento automático desativado** por padrão.

Isso irá escutar no endereço de IP `0.0.0.0`, o que significa todos os endereços IP disponíveis, dessa forma o programa estará acessível publicamente para qualquer um que consiga se comunicar com a máquina. Isso é como você normalmente roda em produção em um contêiner, por exemplo.

Em muitos casos você pode ter (e deveria ter) um "proxy de saída" tratando HTTPS no topo, isso dependerá de como você fará o deploy da sua aplicação, seu provedor pode fazer isso pra você ou talvez seja necessário fazer você mesmo.

/// tip

Você pode aprender mais sobre em [documentação de deployment](deployment/index.md){.internal-link target=_blank}.

///
