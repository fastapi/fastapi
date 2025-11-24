# FastAPI em contêineres - Docker { #fastapi-in-containers-docker }

Ao fazer o deploy de aplicações FastAPI uma abordagem comum é construir uma **imagem de contêiner Linux**. Isso normalmente é feito usando o <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>. Você pode a partir disso fazer o deploy dessa imagem de algumas maneiras.

Usando contêineres Linux você tem diversas vantagens incluindo **segurança**, **replicabilidade**, **simplicidade**, entre outras.

/// tip | Dica

Está com pressa e já sabe dessas coisas? Pode ir direto para o [`Dockerfile` abaixo 👇](#build-a-docker-image-for-fastapi).

///

<details>
<summary>Visualização do Dockerfile 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# Se estiver executando atrás de um proxy como Nginx ou Traefik, adicione --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

</details>

## O que é um Contêiner { #what-is-a-container }

Contêineres (principalmente contêineres Linux) são um jeito muito **leve** de empacotar aplicações contendo todas as dependências e arquivos necessários enquanto os mantém isolados de outros contêineres (outras aplicações ou componentes) no mesmo sistema.

Contêineres Linux rodam usando o mesmo kernel Linux do hospedeiro (máquina, máquina virtual, servidor na nuvem, etc). Isso simplesmente significa que eles são muito leves (comparados com máquinas virtuais emulando um sistema operacional completo).

Dessa forma, contêineres consomem **poucos recursos**, uma quantidade comparável com rodar os processos diretamente (uma máquina virtual consumiria muito mais).

Contêineres também possuem seus próprios processos em execução (comumente **um único processo**), sistema de arquivos e rede **isolados**, simplificando deploy, segurança, desenvolvimento, etc.

## O que é uma Imagem de Contêiner { #what-is-a-container-image }

Um **contêiner** roda a partir de uma **imagem de contêiner**.

Uma imagem de contêiner é uma versão **estática** de todos os arquivos, variáveis de ambiente e do comando/programa padrão que deve estar presente num contêiner. **Estática** aqui significa que a **imagem** de contêiner não está rodando, não está sendo executada, somente contém os arquivos e metadados empacotados.

Em contraste com a "**imagem de contêiner**" que contém os conteúdos estáticos armazenados, um "**contêiner**" normalmente se refere à instância rodando, a coisa que está sendo **executada**.

Quando o **contêiner** é iniciado e está rodando (iniciado a partir de uma **imagem de contêiner**), ele pode criar ou modificar arquivos, variáveis de ambiente, etc. Essas mudanças vão existir somente nesse contêiner, mas não persistirão na imagem subjacente do container (não serão salvas no disco).

Uma imagem de contêiner é comparável ao arquivo de **programa** e seus conteúdos, ex.: `python` e algum arquivo `main.py`.

E o **contêiner** em si (em contraste à **imagem de contêiner**) é a própria instância da imagem rodando, comparável a um **processo**. Na verdade, um contêiner está rodando somente quando há um **processo rodando** (e normalmente é somente um processo). O contêiner finaliza quando não há um processo rodando nele.

## Imagens de contêiner { #container-images }

Docker tem sido uma das principais ferramentas para criar e gerenciar **imagens de contêiner** e **contêineres**.

E existe um <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a> público com **imagens de contêiner oficiais** pré-prontas para diversas ferramentas, ambientes, bancos de dados e aplicações.

Por exemplo, há uma <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Imagem Python</a> oficial.

E existe muitas outras imagens para diferentes coisas, como bancos de dados, por exemplo:

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, etc.

Usando imagens de contêiner pré-prontas é muito fácil **combinar** e usar diferentes ferramentas. Por exemplo, para testar um novo banco de dados. Em muitos casos, você pode usar as **imagens oficiais**, precisando somente de variáveis de ambiente para configurá-las.

Dessa forma, em muitos casos você pode aprender sobre contêineres e Docker e reusar essa experiência com diversos componentes e ferramentas.

Então, você rodaria **vários contêineres** com coisas diferentes, como um banco de dados, uma aplicação Python, um servidor web com uma aplicação frontend React, e conectá-los juntos via sua rede interna.

Todos os sistemas de gerenciamento de contêineres (como Docker ou Kubernetes) possuem essas funcionalidades de rede integradas a eles.

## Contêineres e Processos { #containers-and-processes }

Uma **imagem de contêiner** normalmente inclui em seus metadados o programa padrão ou comando que deve ser executado quando o **contêiner** é iniciado e os parâmetros a serem passados para esse programa. Muito similar ao que seria se estivesse na linha de comando.

Quando um **contêiner** é iniciado, ele irá rodar esse comando/programa (embora você possa sobrescrevê-lo e fazer com que ele rode um comando/programa diferente).

Um contêiner está rodando enquanto o **processo principal** (comando ou programa) estiver rodando.

Um contêiner normalmente tem um **único processo**, mas também é possível iniciar sub-processos a partir do processo principal, e dessa forma você terá **vários processos** no mesmo contêiner.

Mas não é possível ter um contêiner rodando sem **pelo menos um processo rodando**. Se o processo principal parar, o contêiner também para.

## Construir uma Imagem Docker para FastAPI { #build-a-docker-image-for-fastapi }

Okay, vamos construir algo agora! 🚀

Eu vou mostrar como construir uma **imagem Docker** para FastAPI **do zero**, baseada na imagem **oficial do Python**.

Isso é o que você quer fazer na **maioria dos casos**, por exemplo:

* Usando **Kubernetes** ou ferramentas similares
* Quando rodando em uma **Raspberry Pi**
* Usando um serviço em nuvem que irá rodar uma imagem de contêiner para você, etc.

### Requisitos de Pacotes { #package-requirements }

Você normalmente teria os **requisitos de pacotes** da sua aplicação em algum arquivo.

Isso pode depender principalmente da ferramenta que você usa para **instalar** esses requisitos.

A forma mais comum de fazer isso é ter um arquivo `requirements.txt` com os nomes dos pacotes e suas versões, um por linha.

Você, naturalmente, usaria as mesmas ideias que você leu em [Sobre versões do FastAPI](versions.md){.internal-link target=_blank} para definir os intervalos de versões.

Por exemplo, seu `requirements.txt` poderia parecer com:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

E você normalmente instalaria essas dependências de pacote com `pip`, por exemplo:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

</div>

/// info | Informação

Há outros formatos e ferramentas para definir e instalar dependências de pacotes.

///

### Crie o código do **FastAPI** { #create-the-fastapi-code }

* Crie um diretório `app` e entre nele.
* Crie um arquivo vazio `__init__.py`.
* Crie um arquivo `main.py` com:

```Python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile { #dockerfile }

Agora, no mesmo diretório do projeto, crie um arquivo `Dockerfile` com:

```{ .dockerfile .annotate }
# (1)!
FROM python:3.9

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app

# (6)!
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1. Inicie a partir da imagem base oficial do Python.

2. Defina o diretório de trabalho atual para `/code`.

    Esse é o diretório onde colocaremos o arquivo `requirements.txt` e o diretório `app`.

3. Copie o arquivo com os requisitos para o diretório `/code`.

    Copie **somente** o arquivo com os requisitos primeiro, não o resto do código.

    Como esse arquivo **não muda com frequência**, o Docker irá detectá-lo e usar o **cache** para esse passo, habilitando o cache para o próximo passo também.

4. Instale as dependências de pacote vindas do arquivo de requisitos.

    A opção `--no-cache-dir` diz ao `pip` para não salvar os pacotes baixados localmente, pois isso só aconteceria se `pip` fosse executado novamente para instalar os mesmos pacotes, mas esse não é o caso quando trabalhamos com contêineres.

    /// note | Nota

    `--no-cache-dir` é apenas relacionado ao `pip`, não tem nada a ver com Docker ou contêineres.

    ///

    A opção `--upgrade` diz ao `pip` para atualizar os pacotes se eles já estiverem instalados.

    Por causa do passo anterior de copiar o arquivo, ele pode ser detectado pelo **cache do Docker**, esse passo também **usará o cache do Docker** quando disponível.

    Usando o cache nesse passo irá **salvar** muito **tempo** quando você for construir a imagem repetidas vezes durante o desenvolvimento, ao invés de **baixar e instalar** todas as dependências **toda vez**.

5. Copie o diretório `./app` dentro do diretório `/code`.

    Como isso tem todo o código contendo o que **muda com mais frequência**, o **cache do Docker** não será usado para esse passo ou para **qualquer passo seguinte** facilmente.

    Então, é importante colocar isso **perto do final** do `Dockerfile`, para otimizar o tempo de construção da imagem do contêiner.

6. Defina o **comando** para usar `fastapi run`, que utiliza o Uvicorn por baixo dos panos.

    `CMD` recebe uma lista de strings, cada uma dessas strings é o que você digitaria na linha de comando separado por espaços.

    Esse comando será executado a partir do **diretório de trabalho atual**, o mesmo diretório `/code` que você definiu acima com `WORKDIR /code`.

/// tip | Dica

Revise o que cada linha faz clicando em cada bolha com o número no código. 👆

///

/// warning | Atenção

Certifique-se de **sempre** usar a **forma exec** da instrução `CMD`, como explicado abaixo.

///

#### Use `CMD` - Forma Exec { #use-cmd-exec-form }

A instrução <a href="https://docs.docker.com/reference/dockerfile/#cmd" class="external-link" target="_blank">`CMD`</a> no Docker pode ser escrita de duas formas:

✅ Forma **Exec**:

```Dockerfile
# ✅ Faça assim
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ Forma **Shell**:

```Dockerfile
# ⛔️ Não faça assim
CMD fastapi run app/main.py --port 80
```

Garanta que você sempre use a forma **exec** para assegurar que o FastAPI consiga encerrar graciosamente e que os [eventos de lifespan](../advanced/events.md){.internal-link target=_blank} sejam disparados.

Você pode ler mais na <a href="https://docs.docker.com/reference/dockerfile/#shell-and-exec-form" class="external-link" target="_blank">documentação do Docker sobre as formas shell e exec</a>.

Isso pode ser bem perceptível ao usar `docker compose`. Veja esta seção de FAQ do Docker Compose para mais detalhes técnicos: <a href="https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop" class="external-link" target="_blank">Por que meus serviços demoram 10 segundos para recriar ou parar?</a>.

#### Estrutura de diretórios { #directory-structure }

Agora você deve haver uma estrutura de diretório como:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Por trás de um Proxy de Terminação TLS { #behind-a-tls-termination-proxy }

Se você está executando seu contêiner atrás de um Proxy de Terminação TLS (load balancer) como Nginx ou Traefik, adicione a opção `--proxy-headers`, isso fará com que o Uvicorn (pela CLI do FastAPI) confie nos cabeçalhos enviados por esse proxy, informando que o aplicativo está sendo executado atrás do HTTPS, etc.

```Dockerfile
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Cache Docker { #docker-cache }

Existe um truque importante nesse `Dockerfile`, primeiro copiamos o **arquivo com as dependências sozinho**, não o resto do código. Deixe-me te contar o porquê disso.

```Dockerfile
COPY ./requirements.txt /code/requirements.txt
```

Docker e outras ferramentas **constróem** essas imagens de contêiner **incrementalmente**, adicionando **uma camada em cima da outra**, começando do topo do `Dockerfile` e adicionando qualquer arquivo criado por cada uma das instruções do `Dockerfile`.

Docker e ferramentas similares também usam um **cache interno** ao construir a imagem, se um arquivo não mudou desde a última vez que a imagem do contêiner foi construída, então ele irá **reutilizar a mesma camada** criada na última vez, ao invés de copiar o arquivo novamente e criar uma nova camada do zero.

Somente evitar a cópia de arquivos não melhora muito as coisas, mas porque ele usou o cache para esse passo, ele pode **usar o cache para o próximo passo**. Por exemplo, ele pode usar o cache para a instrução que instala as dependências com:

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

O arquivo com os requisitos de pacote **não muda com frequência**. Então, ao copiar apenas esse arquivo, o Docker será capaz de **usar o cache** para esse passo.

E então, o Docker será capaz de **usar o cache para o próximo passo** que baixa e instala essas dependências. E é aqui que **salvamos muito tempo**. ✨ ...e evitamos tédio esperando. 😪😆

Baixar e instalar as dependências do pacote **pode levar minutos**, mas usando o **cache** leva **segundos** no máximo.

E como você estaria construindo a imagem do contêiner novamente e novamente durante o desenvolvimento para verificar se suas alterações de código estão funcionando, há muito tempo acumulado que isso economizaria.

A partir daí, perto do final do `Dockerfile`, copiamos todo o código. Como isso é o que **muda com mais frequência**, colocamos perto do final, porque quase sempre, qualquer coisa depois desse passo não será capaz de usar o cache.

```Dockerfile
COPY ./app /code/app
```

### Construa a Imagem Docker { #build-the-docker-image }

Agora que todos os arquivos estão no lugar, vamos construir a imagem do contêiner.

* Vá para o diretório do projeto (onde está o seu `Dockerfile`, contendo o diretório `app`).
* Construa sua imagem FastAPI:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

/// tip | Dica

Note o `.` no final, é equivalente a `./`, ele diz ao Docker o diretório a ser usado para construir a imagem do contêiner.

Nesse caso, é o mesmo diretório atual (`.`).

///

### Inicie o Contêiner Docker { #start-the-docker-container }

* Execute um contêiner baseado na sua imagem:

<div class="termy">

```console
$ docker run -d --name mycontainer -p 80:80 myimage
```

</div>

## Verifique { #check-it }

Você deve ser capaz de verificar isso no URL do seu contêiner Docker, por exemplo: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> ou <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (ou equivalente, usando seu host Docker).

Você verá algo como:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Documentação interativa da API { #interactive-api-docs }

Agora você pode ir para <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> ou <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (ou equivalente, usando seu host Docker).

Você verá a documentação interativa automática da API (fornecida pelo <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Documentação alternativa da API { #alternative-api-docs }

E você também pode ir para <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> ou <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (ou equivalente, usando seu host Docker).

Você verá a documentação alternativa automática (fornecida pela <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Construa uma Imagem Docker com um FastAPI de Arquivo Único { #build-a-docker-image-with-a-single-file-fastapi }

Se seu FastAPI for um único arquivo, por exemplo, `main.py` sem um diretório `./app`, sua estrutura de arquivos poderia ser assim:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Então você só teria que alterar os caminhos correspondentes para copiar o arquivo dentro do `Dockerfile`:

```{ .dockerfile .annotate hl_lines="10  13" }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/

# (2)!
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1. Copie o arquivo `main.py` para o diretório `/code` diretamente (sem nenhum diretório `./app`).

2. Use `fastapi run` para servir sua aplicação no arquivo único `main.py`.

Quando você passa o arquivo para `fastapi run` ele detecta automaticamente que é um arquivo único e não parte de um pacote e sabe como importá-lo e servir sua aplicação FastAPI. 😎

## Conceitos de Implantação { #deployment-concepts }

Vamos falar novamente sobre alguns dos mesmos [Conceitos de Implantação](concepts.md){.internal-link target=_blank} em termos de contêineres.

Contêineres são principalmente uma ferramenta para simplificar o processo de **construção e implantação** de um aplicativo, mas eles não impõem uma abordagem particular para lidar com esses **conceitos de implantação** e existem várias estratégias possíveis.

A **boa notícia** é que com cada estratégia diferente há uma maneira de cobrir todos os conceitos de implantação. 🎉

Vamos revisar esses **conceitos de implantação** em termos de contêineres:

* HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (número de processos rodando)
* Memória
* Passos anteriores antes de começar

## HTTPS { #https }

Se nos concentrarmos apenas na **imagem do contêiner** para um aplicativo FastAPI (e posteriormente no **contêiner** em execução), o HTTPS normalmente seria tratado **externamente** por outra ferramenta.

Isso poderia ser outro contêiner, por exemplo, com <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>, lidando com **HTTPS** e aquisição **automática** de **certificados**.

/// tip | Dica

Traefik tem integrações com Docker, Kubernetes e outros, portanto, é muito fácil configurar o HTTPS para seus contêineres com ele.

///

Alternativamente, o HTTPS poderia ser tratado por um provedor de nuvem como um de seus serviços (enquanto ainda executasse o aplicativo em um contêiner).

## Executando na inicialização e reinicializações { #running-on-startup-and-restarts }

Normalmente, outra ferramenta é responsável por **iniciar e executar** seu contêiner.

Ela poderia ser o **Docker** diretamente, **Docker Compose**, **Kubernetes**, um **serviço de nuvem**, etc.

Na maioria (ou em todos) os casos, há uma opção simples para habilitar a execução do contêiner na inicialização e habilitar reinicializações em falhas. Por exemplo, no Docker, é a opção de linha de comando `--restart`.

Sem usar contêineres, fazer aplicativos executarem na inicialização e com reinicializações pode ser trabalhoso e difícil. Mas quando **trabalhando com contêineres** em muitos casos essa funcionalidade é incluída por padrão. ✨

## Replicação - Número de Processos { #replication-number-of-processes }

Se você tiver um <abbr title="Um grupo de máquinas que são configuradas para estarem conectadas e trabalharem juntas de alguma forma.">cluster</abbr> de máquinas com **Kubernetes**, Docker Swarm Mode, Nomad ou outro sistema complexo semelhante para gerenciar contêineres distribuídos em várias máquinas, então provavelmente desejará **lidar com a replicação** no **nível do cluster** em vez de usar um **gerenciador de processos** (como Uvicorn com workers) em cada contêiner.

Um desses sistemas de gerenciamento de contêineres distribuídos como o Kubernetes normalmente tem alguma maneira integrada de lidar com a **replicação de contêineres** enquanto ainda oferece **balanceamento de carga** para as solicitações recebidas. Tudo no **nível do cluster**.

Nesses casos, você provavelmente desejará criar uma **imagem Docker do zero** como [explicado acima](#dockerfile), instalando suas dependências e executando **um único processo Uvicorn** em vez de usar múltiplos workers do Uvicorn.

### Balanceador de Carga { #load-balancer }

Quando usando contêineres, normalmente você terá algum componente **escutando na porta principal**. Poderia ser outro contêiner que também é um **Proxy de Terminação TLS** para lidar com **HTTPS** ou alguma ferramenta semelhante.

Como esse componente assumiria a **carga** de solicitações e distribuiria isso entre os workers de uma maneira (esperançosamente) **balanceada**, ele também é comumente chamado de **Balanceador de Carga**.

/// tip | Dica

O mesmo componente **Proxy de Terminação TLS** usado para HTTPS provavelmente também seria um **Balanceador de Carga**.

///

E quando trabalhar com contêineres, o mesmo sistema que você usa para iniciar e gerenciá-los já terá ferramentas internas para transmitir a **comunicação de rede** (por exemplo, solicitações HTTP) do **balanceador de carga** (que também pode ser um **Proxy de Terminação TLS**) para o(s) contêiner(es) com seu aplicativo.

### Um Balanceador de Carga - Múltiplos Contêineres de Workers { #one-load-balancer-multiple-worker-containers }

Quando trabalhando com **Kubernetes** ou sistemas similares de gerenciamento de contêiner distribuído, usar seus mecanismos de rede internos permite que o único **balanceador de carga** que está escutando na **porta principal** transmita a comunicação (solicitações) para possivelmente **múltiplos contêineres** executando seu aplicativo.

Cada um desses contêineres executando seu aplicativo normalmente teria **apenas um processo** (ex.: um processo Uvicorn executando seu aplicativo FastAPI). Todos seriam **contêineres idênticos**, executando a mesma coisa, mas cada um com seu próprio processo, memória, etc. Dessa forma, você aproveitaria a **paralelização** em **núcleos diferentes** da CPU, ou até mesmo em **máquinas diferentes**.

E o sistema de contêiner com o **balanceador de carga** iria **distribuir as solicitações** para cada um dos contêineres com seu aplicativo **em turnos**. Portanto, cada solicitação poderia ser tratada por um dos múltiplos **contêineres replicados** executando seu aplicativo.

E normalmente esse **balanceador de carga** seria capaz de lidar com solicitações que vão para *outros* aplicativos em seu cluster (por exemplo, para um domínio diferente, ou sob um prefixo de URL diferente), e transmitiria essa comunicação para os contêineres certos para *esse outro* aplicativo em execução em seu cluster.

### Um Processo por Contêiner { #one-process-per-container }

Nesse tipo de cenário, provavelmente você desejará ter **um único processo (Uvicorn) por contêiner**, pois já estaria lidando com a replicação no nível do cluster.

Então, nesse caso, você **não** desejará ter múltiplos workers no contêiner, por exemplo com a opção de linha de comando `--workers`. Você desejará ter apenas um **único processo Uvicorn** por contêiner (mas provavelmente vários contêineres).

Ter outro gerenciador de processos dentro do contêiner (como seria com múltiplos workers) só adicionaria **complexidade desnecessária** que você provavelmente já está cuidando com seu sistema de cluster.

### Contêineres com Múltiplos Processos e Casos Especiais { #containers-with-multiple-processes-and-special-cases }

Claro, existem **casos especiais** em que você pode querer ter **um contêiner** com vários **processos workers do Uvicorn** dentro.

Nesses casos, você pode usar a opção de linha de comando `--workers` para definir o número de workers que deseja executar:

```{ .dockerfile .annotate }
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1. Aqui usamos a opção de linha de comando `--workers` para definir o número de workers como 4.

Aqui estão alguns exemplos de quando isso pode fazer sentido:

#### Um Aplicativo Simples { #a-simple-app }

Você pode querer um gerenciador de processos no contêiner se seu aplicativo for **simples o suficiente** para rodar em um **único servidor**, não em um cluster.

#### Docker Compose { #docker-compose }

Você pode estar implantando em um **único servidor** (não em um cluster) com o **Docker Compose**, então você não teria uma maneira fácil de gerenciar a replicação de contêineres (com o Docker Compose) enquanto preserva a rede compartilhada e o **balanceamento de carga**.

Então você pode querer ter **um único contêiner** com um **gerenciador de processos** iniciando **vários processos workers** dentro.

---

O ponto principal é que **nenhum** desses são **regras escritas em pedra** que você deve seguir cegamente. Você pode usar essas ideias para **avaliar seu próprio caso de uso** e decidir qual é a melhor abordagem para seu sistema, verificando como gerenciar os conceitos de:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (o número de processos em execução)
* Memória
* Passos anteriores antes de iniciar

## Memória { #memory }

Se você executar **um único processo por contêiner**, terá uma quantidade mais ou menos bem definida, estável e limitada de memória consumida por cada um desses contêineres (mais de um se eles forem replicados).

E então você pode definir esses mesmos limites e requisitos de memória em suas configurações para seu sistema de gerenciamento de contêineres (por exemplo, no **Kubernetes**). Dessa forma, ele poderá **replicar os contêineres** nas **máquinas disponíveis** levando em consideração a quantidade de memória necessária por eles e a quantidade disponível nas máquinas no cluster.

Se sua aplicação for **simples**, isso provavelmente **não será um problema**, e você pode não precisar especificar limites de memória rígidos. Mas se você estiver **usando muita memória** (por exemplo, com **modelos de aprendizado de máquina**), deve verificar quanta memória está consumindo e ajustar o **número de contêineres** que executa em **cada máquina** (e talvez adicionar mais máquinas ao seu cluster).

Se você executar **múltiplos processos por contêiner**, deve garantir que o número de processos iniciados não **consuma mais memória** do que o disponível.

## Passos anteriores antes de iniciar e contêineres { #previous-steps-before-starting-and-containers }

Se você estiver usando contêineres (por exemplo, Docker, Kubernetes), existem duas abordagens principais que você pode usar.

### Contêineres Múltiplos { #multiple-containers }

Se você tiver **múltiplos contêineres**, provavelmente cada um executando um **único processo** (por exemplo, em um cluster do **Kubernetes**), então provavelmente você gostaria de ter um **contêiner separado** fazendo o trabalho dos **passos anteriores** em um único contêiner, executando um único processo, **antes** de executar os contêineres workers replicados.

/// info | Informação

Se você estiver usando o Kubernetes, provavelmente será um <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>.

///

Se no seu caso de uso não houver problema em executar esses passos anteriores **em paralelo várias vezes** (por exemplo, se você não estiver executando migrações de banco de dados, mas apenas verificando se o banco de dados está pronto), então você também pode colocá-los em cada contêiner logo antes de iniciar o processo principal.

### Contêiner Único { #single-container }

Se você tiver uma configuração simples, com um **único contêiner** que então inicia vários **processos workers** (ou também apenas um processo), então poderia executar esses passos anteriores no mesmo contêiner, logo antes de iniciar o processo com o aplicativo.

### Imagem Docker base { #base-docker-image }

Antes havia uma imagem oficial do FastAPI para Docker: <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>. Mas agora ela está descontinuada. ⛔️

Você provavelmente **não** deve usar essa imagem base do Docker (ou qualquer outra semelhante).

Se você está usando **Kubernetes** (ou outros) e já está definindo a **replicação** no nível do cluster, com vários **contêineres**. Nesses casos, é melhor **construir uma imagem do zero** como descrito acima: [Construir uma Imagem Docker para FastAPI](#build-a-docker-image-for-fastapi).

E se você precisar ter múltiplos workers, você pode simplesmente usar a opção de linha de comando `--workers`.

/// note | Detalhes Técnicos

A imagem Docker foi criada quando o Uvicorn não suportava gerenciar e reiniciar workers mortos, então era necessário usar o Gunicorn com o Uvicorn, o que adicionava bastante complexidade, apenas para que o Gunicorn gerenciasse e reiniciasse os processos workers do Uvicorn.

Mas agora que o Uvicorn (e o comando `fastapi`) suportam o uso de `--workers`, não há razão para usar uma imagem base do Docker em vez de construir a sua própria (é praticamente a mesma quantidade de código 😅).

///

## Deploy da Imagem do Contêiner { #deploy-the-container-image }

Depois de ter uma imagem de contêiner (Docker), existem várias maneiras de implantá-la.

Por exemplo:

* Com **Docker Compose** em um único servidor
* Com um cluster **Kubernetes**
* Com um cluster Docker Swarm Mode
* Com outra ferramenta como o Nomad
* Com um serviço de nuvem que pega sua imagem de contêiner e a implanta

## Imagem Docker com `uv` { #docker-image-with-uv }

Se você está usando o <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">uv</a> para instalar e gerenciar seu projeto, você pode seguir o <a href="https://docs.astral.sh/uv/guides/integration/docker/" class="external-link" target="_blank">guia de Docker do uv</a>.

## Recapitulando { #recap }

Usando sistemas de contêiner (por exemplo, com **Docker** e **Kubernetes**), torna-se bastante simples lidar com todos os **conceitos de implantação**:

* HTTPS
* Executando na inicialização
* Reinícios
* Replicação (o número de processos rodando)
* Memória
* Passos anteriores antes de iniciar

Na maioria dos casos, você provavelmente não desejará usar nenhuma imagem base e, em vez disso, **construir uma imagem de contêiner do zero** baseada na imagem oficial do Docker Python.

Tendo cuidado com a **ordem** das instruções no `Dockerfile` e o **cache do Docker**, você pode **minimizar os tempos de construção**, para maximizar sua produtividade (e evitar o tédio). 😎
