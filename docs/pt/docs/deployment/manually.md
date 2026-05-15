# Execute um Servidor Manualmente { #run-a-server-manually }

## Utilize o comando `fastapi run` { #use-the-fastapi-run-command }

Em resumo, utilize o comando `fastapi run` para inicializar sua aplicação FastAPI:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Isto deve funcionar para a maioria dos casos. 😎

Você pode utilizar esse comando, por exemplo, para iniciar sua aplicação **FastAPI** em um contêiner, em um servidor, etc.

## Servidores ASGI { #asgi-servers }

Vamos nos aprofundar um pouco mais em detalhes.

FastAPI utiliza um padrão para construir frameworks e servidores web em Python chamado <abbr title="Asynchronous Server Gateway Interface - Interface de Gateway de Servidor Assíncrono">ASGI</abbr>. FastAPI é um framework web ASGI.

A principal coisa que você precisa para executar uma aplicação **FastAPI** (ou qualquer outra aplicação ASGI) em uma máquina de servidor remoto é um programa de servidor ASGI como o **Uvicorn**, que é o que vem por padrão no comando `fastapi`.

Existem diversas alternativas, incluindo:

* [Uvicorn](https://www.uvicorn.dev/): um servidor ASGI de alta performance.
* [Hypercorn](https://hypercorn.readthedocs.io/): um servidor ASGI compatível com HTTP/2, Trio e outros recursos.
* [Daphne](https://github.com/django/daphne): servidor ASGI construído para Django Channels.
* [Granian](https://github.com/emmett-framework/granian): um servidor HTTP Rust para aplicações Python.
* [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit é um runtime de aplicação web leve e versátil.

## Máquina Servidora e Programa Servidor { #server-machine-and-server-program }

Existe um pequeno detalhe sobre estes nomes para se manter em mente. 💡

A palavra "**servidor**" é comumente usada para se referir tanto ao computador remoto/nuvem (a máquina física ou virtual) quanto ao programa que está sendo executado nessa máquina (por exemplo, Uvicorn).

Apenas tenha em mente que quando você ler "servidor" em geral, isso pode se referir a uma dessas duas coisas.

Quando se refere à máquina remota, é comum chamá-la de **servidor**, mas também de **máquina**, **VM** (máquina virtual), **nó**. Todos esses termos se referem a algum tipo de máquina remota, normalmente executando Linux, onde você executa programas.

## Instale o Programa Servidor { #install-the-server-program }

Quando você instala o FastAPI, ele vem com um servidor de produção, o Uvicorn, e você pode iniciá-lo com o comando `fastapi run`.

Mas você também pode instalar um servidor ASGI manualmente.

Certifique-se de criar um [ambiente virtual](../virtual-environments.md), ativá-lo e, em seguida, você pode instalar a aplicação do servidor.

Por exemplo, para instalar o Uvicorn:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Um processo semelhante se aplicaria a qualquer outro programa de servidor ASGI.

/// tip | Dica

Adicionando o `standard`, o Uvicorn instalará e usará algumas dependências extras recomendadas.

Isso inclui o `uvloop`, a substituição de alto desempenho para `asyncio`, que fornece um grande aumento de desempenho de concorrência.

Quando você instala o FastAPI com algo como `pip install "fastapi[standard]"`, você já obtém `uvicorn[standard]` também.

///

## Execute o Programa Servidor { #run-the-server-program }

Se você instalou um servidor ASGI manualmente, normalmente precisará passar uma string de importação em um formato especial para que ele importe sua aplicação FastAPI:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Nota

O comando `uvicorn main:app` refere-se a:

* `main`: o arquivo `main.py` (o "módulo" Python).
* `app`: o objeto criado dentro de `main.py` com a linha `app = FastAPI()`.

É equivalente a:

```Python
from main import app
```

///

Cada programa de servidor ASGI alternativo teria um comando semelhante, você pode ler mais na documentação respectiva.

/// warning | Atenção

Uvicorn e outros servidores suportam a opção `--reload` que é útil durante o desenvolvimento.

A opção `--reload` consome muito mais recursos, é mais instável, etc.

Ela ajuda muito durante o **desenvolvimento**, mas você **não deve** usá-la em **produção**.

///

## Conceitos de Implantação { #deployment-concepts }

Esses exemplos executam o programa do servidor (por exemplo, Uvicorn), iniciando **um único processo**, ouvindo em todos os IPs (`0.0.0.0`) em uma porta predefinida (por exemplo, `80`).

Esta é a ideia básica. Mas você provavelmente vai querer cuidar de algumas coisas adicionais, como:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (o número de processos em execução)
* Memória
* Passos anteriores antes de começar

Vou te contar mais sobre cada um desses conceitos, como pensar sobre eles e alguns exemplos concretos com estratégias para lidar com eles nos próximos capítulos. 🚀
