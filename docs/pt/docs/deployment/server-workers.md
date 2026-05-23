# Trabalhadores do Servidor - Uvicorn com Trabalhadores { #server-workers-uvicorn-with-workers }

Vamos rever os conceitos de implantação anteriores:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* **Replicação (o número de processos em execução)**
* Memória
* Etapas anteriores antes de iniciar

Até este ponto, com todos os tutoriais nos documentos, você provavelmente estava executando um **programa de servidor**, por exemplo, usando o comando `fastapi`, que executa o Uvicorn, executando um **único processo**.

Ao implantar aplicativos, você provavelmente desejará ter alguma **replicação de processos** para aproveitar **vários núcleos** e poder lidar com mais solicitações.

Como você viu no capítulo anterior sobre [Conceitos de implantação](concepts.md), há várias estratégias que você pode usar.

Aqui mostrarei como usar o **Uvicorn** com **processos de trabalho** usando o comando `fastapi` ou o comando `uvicorn` diretamente.

/// info | Informação

Se você estiver usando contêineres, por exemplo com Docker ou Kubernetes, falarei mais sobre isso no próximo capítulo: [FastAPI em contêineres - Docker](docker.md).

Em particular, ao executar no **Kubernetes** você provavelmente **não** vai querer usar vários trabalhadores e, em vez disso, executar **um único processo Uvicorn por contêiner**, mas falarei sobre isso mais adiante neste capítulo.

///

## Vários trabalhadores { #multiple-workers }

Você pode iniciar vários trabalhadores com a opção de linha de comando `--workers`:

//// tab | `fastapi`

Se você usar o comando `fastapi`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

Se você preferir usar o comando `uvicorn` diretamente:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

A única opção nova aqui é `--workers` informando ao Uvicorn para iniciar 4 processos de trabalho.

Você também pode ver que ele mostra o **PID** de cada processo, `27365` para o processo pai (este é o **gerenciador de processos**) e um para cada processo de trabalho: `27368`, `27369`, `27370` e `27367`.

## Conceitos de Implantação { #deployment-concepts }

Aqui você viu como usar vários **trabalhadores** para **paralelizar** a execução do aplicativo, aproveitar **vários núcleos** na CPU e conseguir atender **mais solicitações**.

Da lista de conceitos de implantação acima, o uso de trabalhadores ajudaria principalmente com a parte da **replicação** e um pouco com as **reinicializações**, mas você ainda precisa cuidar dos outros:

* **Segurança - HTTPS**
* **Executando na inicialização**
* ***Reinicializações***
* Replicação (o número de processos em execução)
* **Memória**
* **Etapas anteriores antes de iniciar**

## Contêineres e Docker { #containers-and-docker }

No próximo capítulo sobre [FastAPI em contêineres - Docker](docker.md), explicarei algumas estratégias que você pode usar para lidar com os outros **conceitos de implantação**.

Vou mostrar como **construir sua própria imagem do zero** para executar um único processo Uvicorn. É um processo simples e provavelmente é o que você gostaria de fazer ao usar um sistema de gerenciamento de contêineres distribuídos como o **Kubernetes**.

## Recapitular { #recap }

Você pode usar vários processos de trabalho com a opção CLI `--workers` com os comandos `fastapi` ou `uvicorn` para aproveitar as vantagens de **CPUs multi-core** e executar **vários processos em paralelo**.

Você pode usar essas ferramentas e ideias se estiver configurando **seu próprio sistema de implantação** enquanto cuida dos outros conceitos de implantação.

Confira o próximo capítulo para aprender sobre **FastAPI** com contêineres (por exemplo, Docker e Kubernetes). Você verá que essas ferramentas têm maneiras simples de resolver os outros **conceitos de implantação** também. ✨
