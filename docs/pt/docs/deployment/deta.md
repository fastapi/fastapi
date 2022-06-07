# Implantação FastAPI na Deta

Nessa seção você aprenderá sobre como realizar a implantação de uma aplicação **FastAPI** na <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> utilizando o plano gratuito. 🎁

Isso tudo levará aproximadamente **10 minutos**.

!!! info "Informação"
    <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">Deta</a> é uma  patrocinadora do **FastAPI**. 🎉

## Uma aplicação **FastAPI** simples

* Crie e entre em um diretório para a sua aplicação, por exemplo, `./fastapideta/`.

### Código FastAPI

* Crie o arquivo `main.py` com:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Requisitos

Agora, no mesmo diretório crie o arquivo `requirements.txt` com:

```text
fastapi
```

!!! tip "Dica"
    Você não precisa instalar Uvicorn para realizar a implantação na Deta, embora provavelmente queira instalá-lo para testar seu aplicativo localmente.

### Estrutura de diretório

Agora você terá o diretório `./fastapideta/` com dois arquivos:

```
.
└── main.py
└── requirements.txt
```

## Crie uma conta gratuita na Deta

Agora crie <a href="https://www.deta.sh/?ref=fastapi" class="external-link" target="_blank">uma conta gratuita na Deta</a>, você precisará apenas de um email e senha.

Você nem precisa de um cartão de crédito.

## Instale a CLI

Depois de ter sua conta criada, instale Deta <abbr title="Interface de Linha de Comando">CLI</abbr>:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ curl -fsSL https://get.deta.dev/cli.sh | sh
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ iwr https://get.deta.dev/cli.ps1 -useb | iex
    ```

    </div>

Após a instalação, abra um novo terminal para que a CLI seja detectada.

Em um novo terminal, confirme se foi instalado corretamente com:

<div class="termy">

```console
$ deta --help

Deta command line interface for managing deta micros.
Complete documentation available at https://docs.deta.sh

Usage:
  deta [flags]
  deta [command]

Available Commands:
  auth        Change auth settings for a deta micro

...
```

</div>

!!! tip "Dica"
    Se você tiver problemas ao instalar a CLI, verifique a <a href="https://docs.deta.sh/docs/micros/getting_started?ref=fastapi" class="external-link" target="_blank">documentação oficial da Deta</a>.

## Login pela CLI

Agora faça login na Deta pela CLI com:

<div class="termy">

```console
$ deta login

Please, log in from the web page. Waiting..
Logged in successfully.
```

</div>

Isso abrirá um navegador da Web e autenticará automaticamente.

## Implantação com Deta

Em seguida, implante seu aplicativo com a Deta CLI:

<div class="termy">

```console
$ deta new

Successfully created a new micro

// Notice the "endpoint" 🔍

{
    "name": "fastapideta",
    "runtime": "python3.7",
    "endpoint": "https://qltnci.deta.dev",
    "visor": "enabled",
    "http_auth": "enabled"
}

Adding dependencies...


---> 100%


Successfully installed fastapi-0.61.1 pydantic-1.7.2 starlette-0.13.6
```

</div>

Você verá uma mensagem JSON semelhante a:

```JSON hl_lines="4"
{
        "name": "fastapideta",
        "runtime": "python3.7",
        "endpoint": "https://qltnci.deta.dev",
        "visor": "enabled",
        "http_auth": "enabled"
}
```

!!! tip "Dica"
    Sua implantação terá um URL `"endpoint"` diferente.

## Confira

Agora, abra seu navegador na URL do `endpoint`. No exemplo acima foi `https://qltnci.deta.dev`, mas o seu será diferente.

Você verá a resposta JSON do seu aplicativo FastAPI:

```JSON
{
    "Hello": "World"
}
```

Agora vá para o `/docs` da sua API, no exemplo acima seria `https://qltnci.deta.dev/docs`.

Ele mostrará sua documentação como:

<img src="/img/deployment/deta/image01.png">

## Permitir acesso público

Por padrão, a Deta lidará com a autenticação usando cookies para sua conta.

Mas quando estiver pronto, você pode torná-lo público com:

<div class="termy">

```console
$ deta auth disable

Successfully disabled http auth
```

</div>

Agora você pode compartilhar essa URL com qualquer pessoa e elas conseguirão acessar sua API. 🚀

## HTTPS

Parabéns! Você realizou a implantação do seu app FastAPI na Deta! 🎉 🍰

Além disso, observe que a Deta lida corretamente com HTTPS para você, para que você não precise cuidar disso e tenha a certeza de que seus clientes terão uma conexão criptografada segura. ✅ 🔒

## Verifique o Visor

Na UI da sua documentação (você estará em um URL como `https://qltnci.deta.dev/docs`) envie um request para *operação de rota* `/items/{item_id}`.

Por exemplo com ID `5`.

Agora vá para <a href="https://web.deta.sh/" class="external-link" target="_blank">https://web.deta.sh</a>.

Você verá que há uma seção à esquerda chamada <abbr title="it comes from Micro(server)">"Micros"</abbr> com cada um dos seus apps.

Você verá uma aba com "Detalhes", e também a aba "Visor", vá para "Visor".

Lá você pode inspecionar as solicitações recentes enviadas ao seu aplicativo.

Você também pode editá-los e reproduzi-los novamente.

<img src="/img/deployment/deta/image02.png">

## Saiba mais

Em algum momento, você provavelmente desejará armazenar alguns dados para seu aplicativo de uma forma que persista ao longo do tempo. Para isso você pode usar <a href="https://docs.deta.sh/docs/base/py_tutorial?ref=fastapi" class="external-link" target="_blank">Deta Base</a>, que também tem um generoso **nível gratuito**.

Você também pode ler mais na <a href="https://docs.deta.sh?ref=fastapi" class="external-link" target="_blank">documentação da Deta</a>.

## Conceitos de implantação

Voltando aos conceitos que discutimos em [Deployments Concepts](./concepts.md){.internal-link target=_blank}, veja como cada um deles seria tratado com a Deta:

* **HTTPS**: Realizado pela Deta, eles fornecerão um subdomínio e lidarão com HTTPS automaticamente.
* **Executando na inicialização**: Realizado pela Deta, como parte de seu serviço.
* **Reinicialização**: Realizado pela Deta, como parte de seu serviço.
* **Replicação**: Realizado pela Deta, como parte de seu serviço.
* **Memória**: Limite predefinido pela Deta, você pode contatá-los para aumentá-lo.
* **Etapas anteriores a inicialização**: Não suportado diretamente, você pode fazê-lo funcionar com o sistema Cron ou scripts adicionais.

!!! note "Nota"
    O Deta foi projetado para facilitar (e gratuitamente) a implantação rápida de aplicativos simples.

    Ele pode simplificar vários casos de uso, mas, ao mesmo tempo, não suporta outros, como o uso de bancos de dados externos (além do próprio sistema de banco de dados NoSQL da Deta), máquinas virtuais personalizadas, etc.

    Você pode ler mais detalhes na <a href="https://docs.deta.sh/docs/micros/about/" class="external-link" target="_blank">documentação da Deta</a> para ver se é a escolha certa para você.
