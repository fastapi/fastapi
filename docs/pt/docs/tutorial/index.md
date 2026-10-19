# Tutorial - Guia de Usuário { #tutorial-user-guide }

Este tutorial mostra como usar o **FastAPI** com a maior parte de seus recursos, passo a passo.

Cada seção constrói, gradualmente, sobre as anteriores, mas sua estrutura são tópicos separados, para que você possa ir a qualquer um específico e resolver suas necessidades específicas de API.

Ele também foi construído para servir como uma referência futura, então você pode voltar e ver exatamente o que você precisa.

## Execute o código { #run-the-code }

Todos os blocos de código podem ser copiados e utilizados diretamente (eles são, na verdade, arquivos Python testados).

Para executar qualquer um dos exemplos, copie o código para um arquivo `main.py`, e inicie o `fastapi dev` com `uv run`:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

É **ALTAMENTE recomendado** que você escreva ou copie o código, edite-o e execute-o localmente.

Usá-lo em seu editor é o que realmente mostra os benefícios do FastAPI, vendo quão pouco código você tem que escrever, todas as verificações de tipo, preenchimento automático, etc.

---

## Instale o FastAPI { #install-fastapi }

O primeiro passo é configurar seu projeto e adicionar o FastAPI.

Instale o [`uv`](https://docs.astral.sh/uv/getting-started/installation/), então crie um projeto e adicione o FastAPI:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add` cria o ambiente virtual do projeto em `.venv`, adiciona o FastAPI ao `pyproject.toml` e cria `uv.lock` para que as mesmas versões dos pacotes possam ser instaladas posteriormente.

/// details | O que estes comandos fazem

* `uv init`: cria um novo projeto Python.
* `awesome-project`: cria o projeto em um novo diretório com este nome.
* `--bare`: cria apenas o arquivo `pyproject.toml` mínimo, sem gerar um `main.py`, `README.md` ou outros arquivos de exemplo. Você criará os arquivos da aplicação nos próximos passos deste tutorial.

Então `cd awesome-project` entra no novo diretório do projeto antes de adicionar o FastAPI.

`uv` usará uma versão compatível do Python já instalada em seu sistema, ou baixará uma se necessário.

Quando você executa `uv add`, ele seleciona versões compatíveis do FastAPI e de todos os pacotes dos quais o FastAPI depende. Ele registra as versões exatas em `uv.lock`, tornando possível instalar as mesmas versões dos pacotes posteriormente em outro computador ou ao fazer deploy da aplicação.

Criar ou atualizar este arquivo é chamado de [**locking** das dependências do projeto](https://docs.astral.sh/uv/concepts/projects/sync/). O `uv` faz isso automaticamente quando você adiciona um pacote.

///

/// details | Opções de instalação do FastAPI

Quando você instala com `uv add "fastapi[standard]"`, ele vem com algumas dependências opcionais padrão, incluindo `fastapi-cloud-cli`, que permite fazer deploy na [FastAPI Cloud](https://fastapicloud.com).

Se você não quiser ter essas dependências opcionais, pode instalar `uv add fastapi` em vez disso.

Se você quiser instalar as dependências padrão, mas sem o `fastapi-cloud-cli`, você pode instalar com `uv add "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// details | Usando `pip` em vez disso

Se você preferir gerenciar um ambiente virtual e pacotes manualmente, crie e ative um ambiente virtual e então instale o FastAPI com `pip install "fastapi[standard]"`.

Leia o [guia de Ambientes Virtuais](https://tiangolo.com/guides/virtual-environments/) para os passos detalhados.

///

## Habilidades de Agentes de IA { #ai-agent-skills }

O FastAPI inclui uma skill oficial para agentes de codificação de IA. Ela é incluída no pacote, então sua orientação permanece alinhada com a versão do FastAPI instalada no seu projeto e é atualizada quando você atualiza o FastAPI.

Depois de instalar o FastAPI no seu projeto, você pode instalar a skill com <a href="https://library-skills.io">Library Skills</a>:

```bash
uvx library-skills
```

/// note | Nota

`uvx` é um alias para `uv tool run`. Ele executa Library Skills em um ambiente temporário e isolado enquanto Library Skills verifica os pacotes instalados no seu projeto.

///

A skill é compatível com Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode e a maioria dos outros agentes de codificação. Para Claude Code, selecione `.claude/skills` quando for perguntado onde instalar a skill.

## Guia Avançado de Usuário { #advanced-user-guide }

Há também um **Guia Avançado de Usuário** que você pode ler após esse **Tutorial - Guia de Usuário**.

O **Guia Avançado de Usuário** constrói sobre esse, usa os mesmos conceitos e ensina algumas funcionalidades extras.

Mas você deveria ler primeiro o **Tutorial - Guia de Usuário** (que você está lendo agora).

Ele foi projetado para que você possa construir uma aplicação completa com apenas o **Tutorial - Guia de Usuário**, e então estendê-la de diferentes formas, dependendo das suas necessidades, usando algumas ideias adicionais do **Guia Avançado de Usuário**.
