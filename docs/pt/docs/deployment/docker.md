# FastAPI em contêineres - Docker

Ao fazer o deploy de aplicações FastAPI uma abordagem comum é construir uma **imagem de contêiner Linux**. Isso normalmente é feito usando o <a href="https://www.docker.com/" class="external-link" target="_blank">**Docker**</a>. Você pode a partir disso fazer o deploy dessa imagem de algumas maneiras.

Usando contêineres Linux você tem diversas vantagens incluindo **segurança**, **replicabilidade**, **simplicidade**, entre outras.

!!! Dica
    Está com pressa e já sabe dessas coisas? Pode ir direto para [`Dockerfile` abaixo 👇](#build-a-docker-image-for-fastapi).


<details>
<summary>Visualização do Dockerfile 👀</summary>

```Dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
```

</details>

## O que é um Contêiner

Contêineres (especificamente contêineres Linux) são um jeito muito **leve** de empacotar aplicações contendo todas as dependências e arquivos necessários enquanto os mantém isolados de outros contêineres (outras aplicações ou componentes) no mesmo sistema.

Contêineres Linux rodam usando o mesmo kernel Linux do hospedeiro (máquina, máquina virtual, servidor na nuvem, etc). Isso simplesmente significa que eles são muito leves (comparados com máquinas virtuais emulando um sistema operacional completo).

Dessa forma, contêineres consomem **poucos recursos**, uma quantidade comparável com rodar os processos diretamente (uma máquina virtual consumiria muito mais).

Contêineres também possuem seus próprios processos (comumente um único processo), sistema de arquivos e rede **isolados** simplificando deploy, segurança, desenvolvimento, etc.

## O que é uma Imagem de Contêiner

Um **contêiner** roda a partir de uma **imagem de contêiner**.

Uma imagem de contêiner é uma versão **estática** de todos os arquivos, variáveis de ambiente e do comando/programa padrão que deve estar presente num contêiner. **Estática** aqui significa que a **imagem** de contêiner não está rodando, não está sendo executada, somente contém os arquivos e metadados empacotados.

Em contraste com a "**imagem de contêiner**" que contém os conteúdos estáticos armazenados, um "**contêiner**" normalmente se refere à instância rodando, a coisa que está sendo **executada**.

Quando o **contêiner** é iniciado e está rodando (iniciado a partir de uma **imagem de contêiner**), ele pode criar ou modificar arquivos, variáveis de ambiente, etc. Essas mudanças vão existir somente nesse contêiner, mas não persistirão na imagem subjacente do container (não serão salvas no disco).

Uma imagem de contêiner é comparável ao arquivo de **programa** e seus conteúdos, ex.: `python` e algum arquivo `main.py`.

E o **contêiner** em si (em contraste à **imagem de contêiner**) é a própria instância da imagem rodando, comparável a um **processo**. Na verdade, um contêiner está rodando somente quando há um **processo rodando** (e normalmente é somente um processo). O contêiner finaliza quando não há um processo rodando nele.

## Imagens de contêiner

Docker tem sido uma das principais ferramentas para criar e gerenciar **imagens de contêiner** e **contêineres**.

E existe um <a href="https://hub.docker.com/" class="external-link" target="_blank">Docker Hub</a> público com **imagens de contêiner oficiais** pré-prontas para diversas ferramentas, ambientes, bancos de dados e aplicações.

Por exemplo, há uma <a href="https://hub.docker.com/_/python" class="external-link" target="_blank">Imagem Python</a> oficial.

E existe muitas outras imagens para diferentes coisas, como bancos de dados, por exemplo:

* <a href="https://hub.docker.com/_/postgres" class="external-link" target="_blank">PostgreSQL</a>
* <a href="https://hub.docker.com/_/mysql" class="external-link" target="_blank">MySQL</a>
* <a href="https://hub.docker.com/_/mongo" class="external-link" target="_blank">MongoDB</a>
* <a href="https://hub.docker.com/_/redis" class="external-link" target="_blank">Redis</a>, etc.

Usando imagens de contêiner pré-prontas é muito fácil **combinar** e usar diferentes ferramentas. Por exemplo, para testar um novo banco de dados. Em muitos casos, você pode usar as **imagens oficiais** precisando somente de variáveis de ambiente para configurá-las.

Dessa forma, em muitos casos você pode aprender sobre contêineres e Docker e re-usar essa experiência com diversos componentes e ferramentas.

Então, você rodaria **vários contêineres** com coisas diferentes, como um banco de dados, uma aplicação Python, um servidor web com uma aplicação frontend React, e conectá-los juntos via sua rede interna.

Todos os sistemas de gerenciamento de contêineres (como Docker ou Kubernetes) possuem essas funcionalidades de rede integradas a eles.

## Contêineres e Processos

Uma **imagem de contêiner** normalmente inclui em seus metadados o programa padrão ou comando que deve ser executado quando o **contêiner** é iniciado e os parâmetros a serem passados para esse programa. Muito similar ao que seria se estivesse na linha de comando.

Quando um **contêiner** é iniciado, ele irá rodar esse comando/programa (embora você possa sobrescrevê-lo e fazer com que ele rode um comando/programa diferente).

Um contêiner está rodando enquanto o **processo principal** (comando ou programa) estiver rodando.

Um contêiner normalmente tem um **único processo**, mas também é possível iniciar sub-processos a partir do processo principal, e dessa forma você terá **vários processos** no mesmo contêiner.

Mas não é possível ter um contêiner rodando sem **pelo menos um processo rodando**. Se o processo principal parar, o contêiner também para.

## Construindo uma Imagem Docker para FastAPI

Okay, vamos construir algo agora! 🚀

Eu vou mostrar como construir uma **imagem Docker** para FastAPI **do zero**, baseado na **imagem oficial do Python**.

Isso é o que você quer fazer na **maioria dos casos**, por exemplo:

* Usando **Kubernetes** ou ferramentas similares
* Quando rodando em uma **Raspberry Pi**
* Usando um serviço em nuvem que irá rodar uma imagem de contêiner para você, etc.

### O Pacote Requirements

Você normalmente teria os **requisitos do pacote** para sua aplicação em algum arquivo.

Isso pode depender principalmente da ferramenta que você usa para **instalar** esses requisitos.

O caminho mais comum de fazer isso é ter um arquivo `requirements.txt` com os nomes dos pacotes e suas versões, um por linha.

Você, naturalmente, usaria as mesmas ideias que você leu em [Sobre Versões do FastAPI](./versions.md){.internal-link target=_blank} para definir os intervalos de versões.

Por exemplo, seu `requirements.txt` poderia parecer com:

```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
```

E você normalmente instalaria essas dependências de pacote com `pip`, por exemplo:

<div class="termy">

```console
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic uvicorn
```

</div>

!!! info
    Há outros formatos e ferramentas para definir e instalar dependências de pacote.

    Eu vou mostrar um exemplo depois usando Poetry em uma seção abaixo. 👇

### Criando o Código do **FastAPI**

* Crie um diretório `app` e entre nele.
* Crie um arquivo vazio `__init__.py`.
* Crie um arquivo `main.py` com:

```Python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile

Agora, no mesmo diretório do projeto, crie um arquivo `Dockerfile` com:

```{ .dockerfile .annotate }
# (1)
FROM python:3.9

# (2)
WORKDIR /code

# (3)
COPY ./requirements.txt /code/requirements.txt

# (4)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)
COPY ./app /code/app

# (6)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. Inicie a partir da imagem base oficial do Python.

2. Defina o diretório de trabalho atual para `/code`.

    Esse é o diretório onde colocaremos o arquivo `requirements.txt` e o diretório `app`.

3. Copie o arquivo com os requisitos para o diretório `/code`.

    Copie **somente** o arquivo com os requisitos primeiro, não o resto do código.

    Como esse arquivo **não muda com frequência**, o Docker irá detectá-lo e usar o **cache** para esse passo, habilitando o cache para o próximo passo também.

4. Instale as dependências de pacote vindas do arquivo de requisitos.

    A opção `--no-cache-dir` diz ao `pip` para não salvar os pacotes baixados localmente, pois isso só aconteceria se `pip` fosse executado novamente para instalar os mesmos pacotes, mas esse não é o caso quando trabalhamos com contêineres.

    !!! note
        `--no-cache-dir` é apenas relacionado ao `pip`, não tem nada a ver com Docker ou contêineres.

    A opção `--upgrade` diz ao `pip` para atualizar os pacotes se eles já estiverem instalados.

    Por causa do passo anterior de copiar o arquivo, ele pode ser detectado pelo **cache do Docker**, esse passo também **usará o cache do Docker** quando disponível.

    Usando o cache nesse passo irá **salvar** muito **tempo** quando você for construir a imagem repetidas vezes durante o desenvolvimento, ao invés de **baixar e instalar** todas as dependências **toda vez**.

5. Copie o diretório `./app` dentro do diretório `/code`.

    Como isso tem todo o código contendo o que **muda com mais frequência**, o **cache do Docker** não será usado para esse passo ou para **qualquer passo seguinte** facilmente.

    Então, é importante colocar isso **perto do final** do `Dockerfile`, para otimizar o tempo de construção da imagem do contêiner.

6. Defina o **comando** para rodar o servidor `uvicorn`.

    `CMD` recebe uma lista de strings, cada uma dessas strings é o que você digitaria na linha de comando separado por espaços.

    Esse comando será executado a partir do **diretório de trabalho atual**, o mesmo diretório `/code` que você definiu acima com `WORKDIR /code`.

    Porque o programa será iniciado em `/code` e dentro dele está o diretório `./app` com seu código, o **Uvicorn** será capaz de ver e **importar** `app` de `app.main`.

!!! tip
    Revise o que cada linha faz clicando em cada bolha com o número no código. 👆

Agora você deve ter uma estrutura de diretório como:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Por Trás de um Proxy de Terminação TLS

Se você está executando seu contêiner atrás de um Proxy de Terminação TLS (load balancer) como Nginx ou Traefik, adicione a opção `--proxy-headers`, isso fará com que o Uvicorn confie nos cabeçalhos enviados por esse proxy, informando que o aplicativo está sendo executado atrás do HTTPS, etc.

```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

#### Cache Docker

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

### Construindo a Imagem Docker

Agora que todos os arquivos estão no lugar, vamos construir a imagem do contêiner.

* Vá para o diretório do projeto (onde está o seu `Dockerfile`, contendo o diretório `app`).
* Construa sua imagem FastAPI:

<div class="termy">

```console
$ docker build -t myimage .

---> 100%
```

</div>

!!! tip
    Note o `.` no final, é equivalente a `./`, ele diz ao Docker o diretório a ser usado para construir a imagem do contêiner.

    Nesse caso, é o mesmo diretório atual (`.`).

### Inicie o contêiner Docker

* Execute um contêiner baseado na sua imagem:

<div class="termy">

```console
$ docker run -d --name mycontêiner -p 80:80 myimage
```

</div>

## Verifique

Você deve ser capaz de verificar isso no URL do seu contêiner Docker, por exemplo: <a href="http://192.168.99.100/items/5?q=somequery" class="external-link" target="_blank">http://192.168.99.100/items/5?q=somequery</a> ou <a href="http://127.0.0.1/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1/items/5?q=somequery</a> (ou equivalente, usando seu host Docker).

Você verá algo como:

```JSON
{"item_id": 5, "q": "somequery"}
```

## Documentação interativa da API

Agora você pode ir para <a href="http://192.168.99.100/docs" class="external-link" target="_blank">http://192.168.99.100/docs</a> ou <a href="http://127.0.0.1/docs" class="external-link" target="_blank">http://127.0.0.1/docs</a> (ou equivalente, usando seu host Docker).

Você verá a documentação interativa automática da API (fornecida pelo <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Documentação alternativa da API

E você também pode ir para <a href="http://192.168.99.100/redoc" class="external-link" target="_blank">http://192.168.99.100/redoc</a> ou <a href="http://127.0.0.1/redoc" class="external-link" target="_blank">http://127.0.0.1/redoc</a> (ou equivalente, usando seu host Docker).

Você verá a documentação alternativa automática (fornecida pela <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Construindo uma Imagem Docker com um Arquivo Único FastAPI

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

# (1)
COPY ./main.py /code/

# (2)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. Copie o arquivo `main.py` para o diretório `/code` diretamente (sem nenhum diretório `./app`).

2. Execute o Uvicorn e diga a ele para importar o objeto `app` de `main` (em vez de importar de `app.main`).

Então ajuste o comando Uvicorn para usar o novo módulo `main` em vez de `app.main` para importar o objeto FastAPI `app`.

## Conceitos de Implantação

Vamos falar novamente sobre alguns dos mesmos [Conceitos de Implantação](./concepts.md){.internal-link target=_blank} em termos de contêineres.

Contêineres são principalmente uma ferramenta para simplificar o processo de **construção e implantação** de um aplicativo, mas eles não impõem uma abordagem particular para lidar com esses **conceitos de implantação** e existem várias estratégias possíveis.

A **boa notícia** é que com cada estratégia diferente há uma maneira de cobrir todos os conceitos de implantação. 🎉

Vamos revisar esses **conceitos de implantação** em termos de contêineres:

* HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (número de processos rodando)
* Memória
* Passos anteriores antes de começar

## HTTPS

Se nos concentrarmos apenas na **imagem do contêiner** para um aplicativo FastAPI (e posteriormente no **contêiner** em execução), o HTTPS normalmente seria tratado **externamente** por outra ferramenta.

Isso poderia ser outro contêiner, por exemplo, com <a href="https://traefik.io/" class="external-link" target="_blank">Traefik</a>, lidando com **HTTPS** e aquisição **automática** de **certificados**.

!!! tip
    Traefik tem integrações com Docker, Kubernetes e outros, portanto, é muito fácil configurar e configurar o HTTPS para seus contêineres com ele.

Alternativamente, o HTTPS poderia ser tratado por um provedor de nuvem como um de seus serviços (enquanto ainda executasse o aplicativo em um contêiner).

## Executando na inicialização e reinicializações

Normalmente, outra ferramenta é responsável por **iniciar e executar** seu contêiner.

Ela poderia ser o **Docker** diretamente, **Docker Compose**, **Kubernetes**, um **serviço de nuvem**, etc.

Na maioria (ou em todos) os casos, há uma opção simples para habilitar a execução do contêiner na inicialização e habilitar reinicializações em falhas. Por exemplo, no Docker, é a opção de linha de comando `--restart`.

Sem usar contêineres, fazer aplicativos executarem na inicialização e com reinicializações pode ser trabalhoso e difícil. Mas quando **trabalhando com contêineres** em muitos casos essa funcionalidade é incluída por padrão. ✨

## Replicação - Número de Processos

Se você tiver um <abbr title="Um grupo de máquinas que são configuradas para estarem conectadas e trabalharem juntas de alguma forma">cluster</abbr> de máquinas com **Kubernetes**, Docker Swarm Mode, Nomad ou outro sistema complexo semelhante para gerenciar contêineres distribuídos em várias máquinas, então provavelmente desejará **lidar com a replicação** no **nível do cluster** em vez de usar um **gerenciador de processos** (como o Gunicorn com workers) em cada contêiner.

Um desses sistemas de gerenciamento de contêineres distribuídos como o Kubernetes normalmente tem alguma maneira integrada de lidar com a **replicação de contêineres** enquanto ainda oferece **balanceamento de carga** para as solicitações recebidas. Tudo no **nível do cluster**.

Nesses casos, você provavelmente desejará criar uma **imagem do contêiner do zero** como [explicado acima](#dockerfile), instalando suas dependências e executando **um único processo Uvicorn** em vez de executar algo como Gunicorn com trabalhadores Uvicorn.

### Balanceamento de Carga

Quando usando contêineres, normalmente você terá algum componente **escutando na porta principal**. Poderia ser outro contêiner que também é um **Proxy de Terminação TLS** para lidar com **HTTPS** ou alguma ferramenta semelhante.

Como esse componente assumiria a **carga** de solicitações e distribuiria isso entre os trabalhadores de uma maneira (esperançosamente) **balanceada**, ele também é comumente chamado de **Balanceador de Carga**.

!!! tip
    O mesmo componente **Proxy de Terminação TLS** usado para HTTPS provavelmente também seria um **Balanceador de Carga**.

E quando trabalhar com contêineres, o mesmo sistema que você usa para iniciar e gerenciá-los já terá ferramentas internas para transmitir a **comunicação de rede** (por exemplo, solicitações HTTP) do **balanceador de carga** (que também pode ser um **Proxy de Terminação TLS**) para o(s) contêiner(es) com seu aplicativo.

### Um Balanceador de Carga - Múltiplos Contêineres de Workers

Quando trabalhando com **Kubernetes** ou sistemas similares de gerenciamento de contêiner distribuído, usando seus mecanismos de rede internos permitiria que o único **balanceador de carga** que estivesse escutando na **porta principal** transmitisse comunicação (solicitações) para possivelmente **múltiplos contêineres** executando seu aplicativo.

Cada um desses contêineres executando seu aplicativo normalmente teria **apenas um processo** (ex.: um processo Uvicorn executando seu aplicativo FastAPI). Todos seriam **contêineres idênticos**, executando a mesma coisa, mas cada um com seu próprio processo, memória, etc. Dessa forma, você aproveitaria a **paralelização** em **núcleos diferentes** da CPU, ou até mesmo em **máquinas diferentes**.

E o sistema de contêiner com o **balanceador de carga** iria **distribuir as solicitações** para cada um dos contêineres com seu aplicativo **em turnos**. Portanto, cada solicitação poderia ser tratada por um dos múltiplos **contêineres replicados** executando seu aplicativo.

E normalmente esse **balanceador de carga** seria capaz de lidar com solicitações que vão para *outros* aplicativos em seu cluster (por exemplo, para um domínio diferente, ou sob um prefixo de URL diferente), e transmitiria essa comunicação para os contêineres certos para *esse outro* aplicativo em execução em seu cluster.

### Um Processo por Contêiner

Nesse tipo de cenário, provavelmente você desejará ter **um único processo (Uvicorn) por contêiner**, pois já estaria lidando com a replicação no nível do cluster.

Então, nesse caso, você **não** desejará ter um gerenciador de processos como o Gunicorn com trabalhadores Uvicorn, ou o Uvicorn usando seus próprios trabalhadores Uvicorn. Você desejará ter apenas um **único processo Uvicorn** por contêiner (mas provavelmente vários contêineres).

Tendo outro gerenciador de processos dentro do contêiner (como seria com o Gunicorn ou o Uvicorn gerenciando trabalhadores Uvicorn) só adicionaria **complexidade desnecessária** que você provavelmente já está cuidando com seu sistema de cluster.

### Contêineres com Múltiplos Processos e Casos Especiais

Claro, existem **casos especiais** em que você pode querer ter um **contêiner** com um **gerenciador de processos Gunicorn** iniciando vários **processos trabalhadores Uvicorn** dentro.

Nesses casos, você pode usar a **imagem oficial do Docker** que inclui o **Gunicorn** como um gerenciador de processos executando vários **processos trabalhadores Uvicorn**, e algumas configurações padrão para ajustar o número de trabalhadores com base nos atuais núcleos da CPU automaticamente. Eu vou te contar mais sobre isso abaixo em [Imagem Oficial do Docker com Gunicorn - Uvicorn](#imagem-oficial-do-docker-com-gunicorn-uvicorn).

Aqui estão alguns exemplos de quando isso pode fazer sentido:

#### Um Aplicativo Simples

Você pode querer um gerenciador de processos no contêiner se seu aplicativo for **simples o suficiente** para que você não precise (pelo menos não agora) ajustar muito o número de processos, e você pode simplesmente usar um padrão automatizado (com a imagem oficial do Docker), e você está executando em um **único servidor**, não em um cluster.

#### Docker Compose

Você pode estar implantando em um **único servidor** (não em um cluster) com o **Docker Compose**, então você não teria uma maneira fácil de gerenciar a replicação de contêineres (com o Docker Compose) enquanto preserva a rede compartilhada e o **balanceamento de carga**.

Então você pode querer ter **um único contêiner** com um **gerenciador de processos** iniciando **vários processos trabalhadores** dentro.

#### Prometheus and Outros Motivos

Você também pode ter **outros motivos** que tornariam mais fácil ter um **único contêiner** com **múltiplos processos** em vez de ter **múltiplos contêineres** com **um único processo** em cada um deles.

Por exemplo (dependendo de sua configuração), você poderia ter alguma ferramenta como um exportador do Prometheus no mesmo contêiner que deve ter acesso a **cada uma das solicitações** que chegam.

Nesse caso, se você tivesse **múltiplos contêineres**, por padrão, quando o Prometheus fosse **ler as métricas**, ele receberia as métricas de **um único contêiner cada vez** (para o contêiner que tratou essa solicitação específica), em vez de receber as **métricas acumuladas** de todos os contêineres replicados.

Então, nesse caso, poderia ser mais simples ter **um único contêiner** com **múltiplos processos**, e uma ferramenta local (por exemplo, um exportador do Prometheus) no mesmo contêiner coletando métricas do Prometheus para todos os processos internos e expor essas métricas no único contêiner.

---

O ponto principal é que **nenhum** desses são **regras escritas em pedra** que você deve seguir cegamente. Você pode usar essas idéias para **avaliar seu próprio caso de uso** e decidir qual é a melhor abordagem para seu sistema, verificando como gerenciar os conceitos de:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (o número de processos em execução)
* Memória
* Passos anteriores antes de inicializar

## Memória

Se você executar **um único processo por contêiner**, terá uma quantidade mais ou menos bem definida, estável e limitada de memória consumida por cada um desses contêineres (mais de um se eles forem replicados).

E então você pode definir esses mesmos limites e requisitos de memória em suas configurações para seu sistema de gerenciamento de contêineres (por exemplo, no **Kubernetes**). Dessa forma, ele poderá **replicar os contêineres** nas **máquinas disponíveis** levando em consideração a quantidade de memória necessária por eles e a quantidade disponível nas máquinas no cluster.

Se sua aplicação for **simples**, isso provavelmente **não será um problema**, e você pode não precisar especificar limites de memória rígidos. Mas se você estiver **usando muita memória** (por exemplo, com **modelos de aprendizado de máquina**), deve verificar quanta memória está consumindo e ajustar o **número de contêineres** que executa em **cada máquina** (e talvez adicionar mais máquinas ao seu cluster).

Se você executar **múltiplos processos por contêiner** (por exemplo, com a imagem oficial do Docker), deve garantir que o número de processos iniciados não **consuma mais memória** do que o disponível.

## Passos anteriores antes de inicializar e contêineres

Se você estiver usando contêineres (por exemplo, Docker, Kubernetes), existem duas abordagens principais que você pode usar.

### Contêineres Múltiplos

Se você tiver **múltiplos contêineres**, provavelmente cada um executando um **único processo** (por exemplo, em um cluster do **Kubernetes**), então provavelmente você gostaria de ter um **contêiner separado** fazendo o trabalho dos **passos anteriores** em um único contêiner, executando um único processo, **antes** de executar os contêineres trabalhadores replicados.

!!! info
    Se você estiver usando o Kubernetes, provavelmente será um <a href="https://kubernetes.io/docs/concepts/workloads/pods/init-containers/" class="external-link" target="_blank">Init Container</a>.

Se no seu caso de uso não houver problema em executar esses passos anteriores **em paralelo várias vezes** (por exemplo, se você não estiver executando migrações de banco de dados, mas apenas verificando se o banco de dados está pronto), então você também pode colocá-los em cada contêiner logo antes de iniciar o processo principal.

### Contêiner Único

Se você tiver uma configuração simples, com um **único contêiner** que então inicia vários **processos trabalhadores** (ou também apenas um processo), então poderia executar esses passos anteriores no mesmo contêiner, logo antes de iniciar o processo com o aplicativo. A imagem oficial do Docker suporta isso internamente.

## Imagem Oficial do Docker com Gunicorn - Uvicorn

Há uma imagem oficial do Docker que inclui o Gunicorn executando com trabalhadores Uvicorn, conforme detalhado em um capítulo anterior: [Server Workers - Gunicorn com Uvicorn](./server-workers.md){.internal-link target=_blank}.

Essa imagem seria útil principalmente nas situações descritas acima em: [Contêineres com Múltiplos Processos e Casos Especiais](#contêineres-com-múltiplos-processos-e-casos-Especiais).

* <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

!!! warning
    Existe uma grande chance de que você **não** precise dessa imagem base ou de qualquer outra semelhante, e seria melhor construir a imagem do zero, como [descrito acima em: Construa uma Imagem Docker para o FastAPI](#construa-uma-imagem-docker-para-o-fastapi).

Essa imagem tem um mecanismo de **auto-ajuste** incluído para definir o **número de processos trabalhadores** com base nos núcleos de CPU disponíveis.

Isso tem **padrões sensíveis**, mas você ainda pode alterar e atualizar todas as configurações com **variáveis de ambiente** ou arquivos de configuração.

Há também suporte para executar <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#pre_start_path" class="external-link" target="_blank">**passos anteriores antes de iniciar**</a> com um script.

!!! tip
    Para ver todas as configurações e opções, vá para a página da imagem Docker:  <a href="https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker" class="external-link" target="_blank">tiangolo/uvicorn-gunicorn-fastapi</a>.

### Número de Processos na Imagem Oficial do Docker

O **número de processos** nesta imagem é **calculado automaticamente** a partir dos **núcleos de CPU** disponíveis.

Isso significa que ele tentará **aproveitar** o máximo de **desempenho** da CPU possível.

Você também pode ajustá-lo com as configurações usando **variáveis de ambiente**, etc.

Mas isso também significa que, como o número de processos depende da CPU do contêiner em execução, a **quantidade de memória consumida** também dependerá disso.

Então, se seu aplicativo consumir muito memória (por exemplo, com modelos de aprendizado de máquina), e seu servidor tiver muitos núcleos de CPU **mas pouca memória**, então seu contêiner pode acabar tentando usar mais memória do que está disponível e degradar o desempenho muito (ou até mesmo travar). 🚨

### Criando um `Dockerfile`

Aqui está como você criaria um `Dockerfile` baseado nessa imagem:

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

### Aplicações Maiores

Se você seguiu a seção sobre a criação de [Aplicações Maiores com Múltiplos Arquivos](../tutorial/bigger-applications.md){.internal-link target=_blank}, seu `Dockerfile` pode parecer com isso:

```Dockerfile

```Dockerfile hl_lines="7"
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
```

### Quando Usar

Você provavelmente **não** deve usar essa imagem base oficial (ou qualquer outra semelhante) se estiver usando **Kubernetes** (ou outros) e já estiver definindo **replicação** no nível do cluster, com vários **contêineres**. Nesses casos, é melhor **construir uma imagem do zero** conforme descrito acima: [Construindo uma Imagem Docker para FastAPI](#construindo-uma-imagem-docker-para-fastapi).

Essa imagem seria útil principalmente nos casos especiais descritos acima em [Contêineres com Múltiplos Processos e Casos Especiais](#contêineres-com-múltiplos-processos-e-casos-Especiais). Por exemplo, se sua aplicação for **simples o suficiente** para que a configuração padrão de número de processos com base na CPU funcione bem, você não quer se preocupar com a configuração manual da replicação no nível do cluster e não está executando mais de um contêiner com seu aplicativo. Ou se você estiver implantando com **Docker Compose**, executando em um único servidor, etc.

## Deploy da Imagem do Contêiner

Depois de ter uma imagem de contêiner (Docker), existem várias maneiras de implantá-la.

Por exemplo:

* Com **Docker Compose** em um único servidor
* Com um cluster **Kubernetes**
* Com um cluster Docker Swarm Mode
* Com outra ferramenta como o Nomad
* Com um serviço de nuvem que pega sua imagem de contêiner e a implanta

## Imagem Docker com Poetry

Se você usa <a href="https://python-poetry.org/" class="external-link" target="_blank">Poetry</a> para gerenciar as dependências do seu projeto, pode usar a construção multi-estágio do Docker:

```{ .dockerfile .annotate }
# (1)
FROM python:3.9 as requirements-stage

# (2)
WORKDIR /tmp

# (3)
RUN pip install poetry

# (4)
COPY ./pyproject.toml ./poetry.lock* /tmp/

# (5)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# (6)
FROM python:3.9

# (7)
WORKDIR /code

# (8)
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# (9)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (10)
COPY ./app /code/app

# (11)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

1. Esse é o primeiro estágio, ele é chamado `requirements-stage`.

2. Defina `/tmp` como o diretório de trabalho atual.

    Aqui é onde geraremos o arquivo `requirements.txt`

3. Instale o Poetry nesse estágio do Docker.

4. Copie os arquivos `pyproject.toml` e `poetry.lock` para o diretório `/tmp`.

    Porque está usando `./poetry.lock*` (terminando com um `*`), não irá falhar se esse arquivo ainda não estiver disponível.

5. Gere o arquivo `requirements.txt`.

6. Este é o estágio final, tudo aqui será preservado na imagem final do contêiner.

7. Defina o diretório de trabalho atual como `/code`.

8. Copie o arquivo `requirements.txt` para o diretório `/code`.

    Essse arquivo só existe no estágio anterior do Docker, é por isso que usamos `--from-requirements-stage` para copiá-lo.

9. Instale as dependências de pacote do arquivo `requirements.txt` gerado.

10. Copie o diretório `app` para o diretório `/code`.

11. Execute o comando `uvicorn`, informando-o para usar o objeto `app` importado de `app.main`.

!!! tip
    Clique nos números das bolhas para ver o que cada linha faz.

Um **estágio do Docker** é uma parte de um `Dockerfile` que funciona como uma **imagem temporária do contêiner** que só é usada para gerar alguns arquivos para serem usados posteriormente.

O primeiro estágio será usado apenas para **instalar Poetry** e para **gerar o `requirements.txt`** com as dependências do seu projeto a partir do arquivo `pyproject.toml` do Poetry.

Esse arquivo `requirements.txt` será usado com `pip` mais tarde no **próximo estágio**.

Na imagem final do contêiner, **somente o estágio final** é preservado. Os estágios anteriores serão descartados.

Quando usar Poetry, faz sentido usar **construções multi-estágio do Docker** porque você realmente não precisa ter o Poetry e suas dependências instaladas na imagem final do contêiner, você **apenas precisa** ter o arquivo `requirements.txt` gerado para instalar as dependências do seu projeto.

Então, no próximo (e último) estágio, você construiria a imagem mais ou menos da mesma maneira descrita anteriormente.

### Por trás de um proxy de terminação TLS - Poetry

Novamente, se você estiver executando seu contêiner atrás de um proxy de terminação TLS (balanceador de carga) como Nginx ou Traefik, adicione a opção `--proxy-headers` ao comando:

```Dockerfile
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

## Recapitulando

Usando sistemas de contêiner (por exemplo, com **Docker** e **Kubernetes**), torna-se bastante simples lidar com todos os **conceitos de implantação**:

* HTTPS
* Executando na inicialização
* Reinícios
* Replicação (o número de processos rodando)
* Memória
* Passos anteriores antes de inicializar

Na maioria dos casos, você provavelmente não desejará usar nenhuma imagem base e, em vez disso, **construir uma imagem de contêiner do zero** baseada na imagem oficial do Docker Python.

Tendo cuidado com a **ordem** das instruções no `Dockerfile` e o **cache do Docker**, você pode **minimizar os tempos de construção**, para maximizar sua produtividade (e evitar a tédio). 😎

Em alguns casos especiais, você pode querer usar a imagem oficial do Docker para o FastAPI. 🤓
