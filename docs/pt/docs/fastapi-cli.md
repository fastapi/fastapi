# FastAPI CLI { #fastapi-cli }

**FastAPI <abbr title="command line interface - interface de linha de comando">CLI</abbr>** é um programa de linha de comando que você pode usar para servir sua aplicação FastAPI, gerenciar seu projeto FastAPI e muito mais.

Quando você instala o FastAPI (por exemplo, com `pip install "fastapi[standard]"`), ele vem com um programa de linha de comando que você pode executar no terminal.

Para executar sua aplicação FastAPI durante o desenvolvimento, você pode usar o comando `fastapi dev`:

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

/// tip | Dica

Em produção, você usaria `fastapi run` em vez de `fastapi dev`. 🚀

///

Internamente, o **FastAPI CLI** usa o [Uvicorn](https://www.uvicorn.dev), um servidor ASGI de alta performance e pronto para produção. 😎

O CLI `fastapi` tentará detectar automaticamente a aplicação FastAPI a ser executada, assumindo que seja um objeto chamado `app` em um arquivo `main.py` (ou algumas outras variantes).

Mas você pode configurar explicitamente a aplicação a ser usada.

## Configure o `entrypoint` da aplicação em `pyproject.toml` { #configure-the-app-entrypoint-in-pyproject-toml }

Você pode configurar onde sua aplicação está localizada em um arquivo `pyproject.toml`, assim:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Esse `entrypoint` dirá ao comando `fastapi` que ele deve importar a aplicação assim:

```python
from main import app
```

Se o seu código estivesse estruturado assim:

```
.
├── backend
│   ├── main.py
│   ├── __init__.py
```

Então você definiria o `entrypoint` como:

```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

o que seria equivalente a:

```python
from backend.main import app
```

### `fastapi dev` com caminho { #fastapi-dev-with-path }

Você também pode passar o caminho do arquivo para o comando `fastapi dev`, e ele deduzirá o objeto da aplicação FastAPI a usar:

```console
$ fastapi dev main.py
```

Mas você teria que lembrar de passar o caminho correto toda vez que chamar o comando `fastapi`.

Além disso, outras ferramentas podem não conseguir encontrá-la, por exemplo a [Extensão do VS Code](editor-support.md) ou a [FastAPI Cloud](https://fastapicloud.com), então é recomendado usar o `entrypoint` em `pyproject.toml`.

## `fastapi dev` { #fastapi-dev }

Executar `fastapi dev` inicia o modo de desenvolvimento.

Por padrão, o **recarregamento automático** está ativado, recarregando o servidor automaticamente quando você faz mudanças no seu código. Isso consome muitos recursos e pode ser menos estável do que quando está desativado. Você deveria usá-lo apenas no desenvolvimento. Ele também escuta no endereço IP `127.0.0.1`, que é o IP para a sua máquina se comunicar apenas consigo mesma (`localhost`).

## `fastapi run` { #fastapi-run }

Executar `fastapi run` inicia o FastAPI em modo de produção.

Por padrão, o **recarregamento automático** está desativado. Ele também escuta no endereço IP `0.0.0.0`, o que significa todos os endereços IP disponíveis; dessa forma, ficará acessível publicamente para qualquer pessoa que consiga se comunicar com a máquina. É assim que você normalmente o executaria em produção, por exemplo, em um contêiner.

Na maioria dos casos, você teria (e você deveria ter) um "proxy de terminação" tratando o HTTPS por cima; isso dependerá de como você faz o deploy da sua aplicação, seu provedor pode fazer isso por você ou talvez seja necessário que você configure isso por conta própria.

/// tip | Dica

Você pode aprender mais sobre isso na [documentação de deployment](deployment/index.md).

///
