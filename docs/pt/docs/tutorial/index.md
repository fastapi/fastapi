# Tutorial - Guia de Usuário

Esse tutorial mostra como usar o **FastAPI** com a maior parte de seus recursos, passo a passo.

Cada seção constrói, gradualmente, sobre as anteriores, mas sua estrutura são tópicos separados, para que você possa ir a qualquer um específico e resolver suas necessidades específicas de API.

Ele também foi construído para servir como uma referência futura, então você pode voltar e ver exatamente o que você precisa.

## Rode o código

Todos os blocos de código podem ser copiados e utilizados diretamente (eles são, na verdade, arquivos Python testados).

Para rodar qualquer um dos exemplos, copie o codigo para um arquivo `main.py`, e inicie o `uvivorn` com:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

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

É **ALTAMENTE recomendado** que você escreva ou copie o código, edite-o e rode-o localmente.

Usá-lo em seu editor é o que realmente te mostra os benefícios do FastAPI, ver quão pouco código você tem que escrever, todas as conferências de tipo, auto completações etc.

---

## Instale o FastAPI

O primeiro passo é instalar o FastAPI.

Para o tutorial, você deve querer instalá-lo com todas as dependências e recursos opicionais.

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note | Nota

Quando você instala com pip install "fastapi[standard]", ele vem com algumas dependências opcionais padrão.

Se você não quiser ter essas dependências opcionais, pode instalar pip install fastapi em vez disso.

///

## Guia Avançado de Usuário

Há também um **Guia Avançado de Usuário** que você pode ler após esse **Tutorial - Guia de Usuário**.

O **Guia Avançado de Usuário** constrói sobre esse, usa os mesmos conceitos e te ensina alguns recursos extras.

Mas você deveria ler primeiro o **Tutorial - Guia de Usuário** (que você está lendo agora).

Ele foi projetado para que você possa construir uma aplicação completa com apenas o **Tutorial - Guia de Usuário**, e então estendê-la de diferentes formas, dependendo das suas necessidades, usando algumas ideias adicionais do **Guia Avançado de Usuário**.
