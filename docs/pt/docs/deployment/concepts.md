# Conceitos de Implantações { #deployments-concepts }

Ao implantar um aplicativo **FastAPI**, ou na verdade, qualquer tipo de API da web, há vários conceitos com os quais você provavelmente se importa e, usando-os, você pode encontrar a maneira **mais apropriada** de **implantar seu aplicativo**.

Alguns dos conceitos importantes são:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (o número de processos em execução)
* Memória
* Etapas anteriores antes de iniciar

Veremos como eles afetariam as **implantações**.

No final, o principal objetivo é ser capaz de **atender seus clientes de API** de uma forma **segura**, **evitar interrupções** e usar os **recursos de computação** (por exemplo, servidores remotos/máquinas virtuais) da forma mais eficiente possível. 🚀

Vou lhe contar um pouco mais sobre esses **conceitos** aqui, e espero que isso lhe dê a **intuição** necessária para decidir como implantar sua API em ambientes muito diferentes, possivelmente até mesmo em **futuros** ambientes que ainda não existem.

Ao considerar esses conceitos, você será capaz de **avaliar e projetar** a melhor maneira de implantar **suas próprias APIs**.

Nos próximos capítulos, darei a você mais **receitas concretas** para implantar aplicativos FastAPI.

Mas por enquanto, vamos verificar essas importantes **ideias conceituais**. Esses conceitos também se aplicam a qualquer outro tipo de API da web. 💡

## Segurança - HTTPS { #security-https }

No [capítulo anterior sobre HTTPS](https.md){.internal-link target=_blank} aprendemos como o HTTPS fornece criptografia para sua API.

Também vimos que o HTTPS normalmente é fornecido por um componente **externo** ao seu servidor de aplicativos, um **Proxy de terminação TLS**.

E tem que haver algo responsável por **renovar os certificados HTTPS**, pode ser o mesmo componente ou pode ser algo diferente.

### Ferramentas de exemplo para HTTPS { #example-tools-for-https }

Algumas das ferramentas que você pode usar como um proxy de terminação TLS são:

* Traefik
    * Lida automaticamente com renovações de certificados ✨
* Caddy
    * Lida automaticamente com renovações de certificados ✨
* Nginx
    * Com um componente externo como o Certbot para renovações de certificados
* HAProxy
    * Com um componente externo como o Certbot para renovações de certificados
* Kubernetes com um controlador Ingress como o Nginx
    * Com um componente externo como cert-manager para renovações de certificados
* Gerenciado internamente por um provedor de nuvem como parte de seus serviços (leia abaixo 👇)

Outra opção é que você poderia usar um **serviço de nuvem** que faz mais do trabalho, incluindo a configuração de HTTPS. Ele pode ter algumas restrições ou cobrar mais, etc. Mas, nesse caso, você não teria que configurar um Proxy de terminação TLS sozinho.

Mostrarei alguns exemplos concretos nos próximos capítulos.

---

Os próximos conceitos a serem considerados são todos sobre o programa que executa sua API real (por exemplo, Uvicorn).

## Programa e Processo { #program-and-process }

Falaremos muito sobre o "**processo**" em execução, então é útil ter clareza sobre o que ele significa e qual é a diferença com a palavra "**programa**".

### O que é um Programa { #what-is-a-program }

A palavra **programa** é comumente usada para descrever muitas coisas:

* O **código** que você escreve, os **arquivos Python**.
* O **arquivo** que pode ser **executado** pelo sistema operacional, por exemplo: `python`, `python.exe` ou `uvicorn`.
* Um programa específico enquanto está **em execução** no sistema operacional, usando a CPU e armazenando coisas na memória. Isso também é chamado de **processo**.

### O que é um Processo { #what-is-a-process }

A palavra **processo** normalmente é usada de forma mais específica, referindo-se apenas ao que está sendo executado no sistema operacional (como no último ponto acima):

* Um programa específico enquanto está **em execução** no sistema operacional.
    * Isso não se refere ao arquivo, nem ao código, refere-se **especificamente** à coisa que está sendo **executada** e gerenciada pelo sistema operacional.
* Qualquer programa, qualquer código, **só pode fazer coisas** quando está sendo **executado**. Então, quando há um **processo em execução**.
* O processo pode ser **terminado** (ou "morto") por você, ou pelo sistema operacional. Nesse ponto, ele para de rodar/ser executado, e ele **não pode mais fazer coisas**.
* Cada aplicativo que você tem em execução no seu computador tem algum processo por trás dele, cada programa em execução, cada janela, etc. E normalmente há muitos processos em execução **ao mesmo tempo** enquanto um computador está ligado.
* Pode haver **vários processos** do **mesmo programa** em execução ao mesmo tempo.

Se você verificar o "gerenciador de tarefas" ou o "monitor do sistema" (ou ferramentas semelhantes) no seu sistema operacional, poderá ver muitos desses processos em execução.

E, por exemplo, você provavelmente verá que há vários processos executando o mesmo programa de navegador (Firefox, Chrome, Edge, etc.). Eles normalmente executam um processo por aba, além de alguns outros processos extras.

<img class="shadow" src="/img/deployment/concepts/image01.png">

---

Agora que sabemos a diferença entre os termos **processo** e **programa**, vamos continuar falando sobre implantações.

## Executando na inicialização { #running-on-startup }

Na maioria dos casos, quando você cria uma API web, você quer que ela esteja **sempre em execução**, ininterrupta, para que seus clientes possam sempre acessá-la. Isso é claro, a menos que você tenha um motivo específico para querer que ela seja executada somente em certas situações, mas na maioria das vezes você quer que ela esteja constantemente em execução e **disponível**.

### Em um servidor remoto { #in-a-remote-server }

Ao configurar um servidor remoto (um servidor em nuvem, uma máquina virtual, etc.), a coisa mais simples que você pode fazer é usar `fastapi run` (que usa Uvicorn) ou algo semelhante, manualmente, da mesma forma que você faz ao desenvolver localmente.

E funcionará e será útil **durante o desenvolvimento**.

Mas se sua conexão com o servidor for perdida, o **processo em execução** provavelmente morrerá.

E se o servidor for reiniciado (por exemplo, após atualizações ou migrações do provedor de nuvem), você provavelmente **não notará**. E por causa disso, você nem saberá que precisa reiniciar o processo manualmente. Então, sua API simplesmente permanecerá inativa. 😱

### Executar automaticamente na inicialização { #run-automatically-on-startup }

Em geral, você provavelmente desejará que o programa do servidor (por exemplo, Uvicorn) seja iniciado automaticamente na inicialização do servidor e, sem precisar de nenhuma **intervenção humana**, tenha um processo sempre em execução com sua API (por exemplo, Uvicorn executando seu aplicativo FastAPI).

### Programa separado { #separate-program }

Para conseguir isso, você normalmente terá um **programa separado** que garantiria que seu aplicativo fosse executado na inicialização. E em muitos casos, ele também garantiria que outros componentes ou aplicativos também fossem executados, por exemplo, um banco de dados.

### Ferramentas de exemplo para executar na inicialização { #example-tools-to-run-at-startup }

Alguns exemplos de ferramentas que podem fazer esse trabalho são:

* Docker
* Kubernetes
* Docker Compose
* Docker em Modo Swarm
* Systemd
* Supervisor
* Gerenciado internamente por um provedor de nuvem como parte de seus serviços
* Outros...

Darei exemplos mais concretos nos próximos capítulos.

## Reinicializações { #restarts }

Semelhante a garantir que seu aplicativo seja executado na inicialização, você provavelmente também deseja garantir que ele seja **reiniciado** após falhas.

### Nós cometemos erros { #we-make-mistakes }

Nós, como humanos, cometemos **erros** o tempo todo. O software quase *sempre* tem **bugs** escondidos em lugares diferentes. 🐛

E nós, como desenvolvedores, continuamos aprimorando o código à medida que encontramos esses bugs e implementamos novos recursos (possivelmente adicionando novos bugs também 😅).

### Pequenos erros são tratados automaticamente { #small-errors-automatically-handled }

Ao criar APIs da web com FastAPI, se houver um erro em nosso código, o FastAPI normalmente o conterá na única solicitação que acionou o erro. 🛡

O cliente receberá um **Erro Interno do Servidor 500** para essa solicitação, mas o aplicativo continuará funcionando para as próximas solicitações em vez de travar completamente.

### Erros maiores - Travamentos { #bigger-errors-crashes }

No entanto, pode haver casos em que escrevemos algum código que **trava todo o aplicativo**, fazendo com que o Uvicorn e o Python travem. 💥

E ainda assim, você provavelmente não gostaria que o aplicativo permanecesse inativo porque houve um erro em um lugar, você provavelmente quer que ele **continue em execução** pelo menos para as *operações de caminho* que não estão quebradas.

### Reiniciar após falha { #restart-after-crash }

Mas nos casos com erros realmente graves que travam o **processo** em execução, você vai querer um componente externo que seja responsável por **reiniciar** o processo, pelo menos algumas vezes...

/// tip | Dica

...Embora se o aplicativo inteiro estiver **travando imediatamente**, provavelmente não faça sentido reiniciá-lo para sempre. Mas nesses casos, você provavelmente notará isso durante o desenvolvimento, ou pelo menos logo após a implantação.

Então, vamos nos concentrar nos casos principais, onde ele pode travar completamente em alguns casos específicos **no futuro**, e ainda faz sentido reiniciá-lo.

///

Você provavelmente gostaria de ter a coisa responsável por reiniciar seu aplicativo como um **componente externo**, porque a essa altura, o mesmo aplicativo com Uvicorn e Python já havia travado, então não há nada no mesmo código do mesmo aplicativo que possa fazer algo a respeito.

### Ferramentas de exemplo para reiniciar automaticamente { #example-tools-to-restart-automatically }

Na maioria dos casos, a mesma ferramenta usada para **executar o programa na inicialização** também é usada para lidar com **reinicializações** automáticas.

Por exemplo, isso poderia ser resolvido por:

* Docker
* Kubernetes
* Docker Compose
* Docker no Modo Swarm
* Systemd
* Supervisor
* Gerenciado internamente por um provedor de nuvem como parte de seus serviços
* Outros...

## Replicação - Processos e Memória { #replication-processes-and-memory }

Com um aplicativo FastAPI, usando um programa de servidor como o comando `fastapi` que executa o Uvicorn, executá-lo uma vez em **um processo** pode atender a vários clientes simultaneamente.

Mas em muitos casos, você desejará executar vários processos de trabalho ao mesmo tempo.

### Processos Múltiplos - Trabalhadores { #multiple-processes-workers }

Se você tiver mais clientes do que um único processo pode manipular (por exemplo, se a máquina virtual não for muito grande) e tiver **vários núcleos** na CPU do servidor, você poderá ter **vários processos** em execução com o mesmo aplicativo ao mesmo tempo e distribuir todas as solicitações entre eles.

Quando você executa **vários processos** do mesmo programa de API, eles são comumente chamados de **trabalhadores**.

### Processos do Trabalhador e Portas { #worker-processes-and-ports }

Lembra da documentação [Sobre HTTPS](https.md){.internal-link target=_blank} que diz que apenas um processo pode escutar em uma combinação de porta e endereço IP em um servidor?

Isso ainda é verdade.

Então, para poder ter **vários processos** ao mesmo tempo, tem que haver um **único processo escutando em uma porta** que então transmite a comunicação para cada processo de trabalho de alguma forma.

### Memória por Processo { #memory-per-process }

Agora, quando o programa carrega coisas na memória, por exemplo, um modelo de aprendizado de máquina em uma variável, ou o conteúdo de um arquivo grande em uma variável, tudo isso **consome um pouco da memória (RAM)** do servidor.

E vários processos normalmente **não compartilham nenhuma memória**. Isso significa que cada processo em execução tem suas próprias coisas, variáveis ​​e memória. E se você estiver consumindo uma grande quantidade de memória em seu código, **cada processo** consumirá uma quantidade equivalente de memória.

### Memória do servidor { #server-memory }

Por exemplo, se seu código carrega um modelo de Machine Learning com **1 GB de tamanho**, quando você executa um processo com sua API, ele consumirá pelo menos 1 GB de RAM. E se você iniciar **4 processos** (4 trabalhadores), cada um consumirá 1 GB de RAM. Então, no total, sua API consumirá **4 GB de RAM**.

E se o seu servidor remoto ou máquina virtual tiver apenas 3 GB de RAM, tentar carregar mais de 4 GB de RAM causará problemas. 🚨

### Processos Múltiplos - Um Exemplo { #multiple-processes-an-example }

Neste exemplo, há um **Processo Gerenciador** que inicia e controla dois **Processos de Trabalhadores**.

Este Processo de Gerenciador provavelmente seria o que escutaria na **porta** no IP. E ele transmitiria toda a comunicação para os processos de trabalho.

Esses processos de trabalho seriam aqueles que executariam seu aplicativo, eles executariam os cálculos principais para receber uma **solicitação** e retornar uma **resposta**, e carregariam qualquer coisa que você colocasse em variáveis ​​na RAM.

<img src="/img/deployment/concepts/process-ram.drawio.svg">

E, claro, a mesma máquina provavelmente teria **outros processos** em execução, além do seu aplicativo.

Um detalhe interessante é que a porcentagem da **CPU usada** por cada processo pode **variar** muito ao longo do tempo, mas a **memória (RAM)** normalmente fica mais ou menos **estável**.

Se você tiver uma API que faz uma quantidade comparável de cálculos todas as vezes e tiver muitos clientes, então a **utilização da CPU** provavelmente *também será estável* (em vez de ficar constantemente subindo e descendo rapidamente).

### Exemplos de ferramentas e estratégias de replicação { #examples-of-replication-tools-and-strategies }

Pode haver várias abordagens para conseguir isso, e falarei mais sobre estratégias específicas nos próximos capítulos, por exemplo, ao falar sobre Docker e contêineres.

A principal restrição a ser considerada é que tem que haver um **único** componente manipulando a **porta** no **IP público**. E então tem que ter uma maneira de **transmitir** a comunicação para os **processos/trabalhadores** replicados.

Aqui estão algumas combinações e estratégias possíveis:

* **Uvicorn** com `--workers`
    * Um **gerenciador de processos** Uvicorn escutaria no **IP** e na **porta** e iniciaria **vários processos de trabalho Uvicorn**.
* **Kubernetes** e outros **sistemas de contêineres** distribuídos
    * Algo na camada **Kubernetes** escutaria no **IP** e na **porta**. A replicação seria por ter **vários contêineres**, cada um com **um processo Uvicorn** em execução.
* **Serviços de nuvem** que cuidam disso para você
    * O serviço de nuvem provavelmente **cuidará da replicação para você**. Ele possivelmente deixaria você definir **um processo para executar**, ou uma **imagem de contêiner** para usar, em qualquer caso, provavelmente seria **um único processo Uvicorn**, e o serviço de nuvem seria responsável por replicá-lo.

/// tip | Dica

Não se preocupe se alguns desses itens sobre **contêineres**, Docker ou Kubernetes ainda não fizerem muito sentido.

Falarei mais sobre imagens de contêiner, Docker, Kubernetes, etc. em um capítulo futuro: [FastAPI em contêineres - Docker](docker.md){.internal-link target=_blank}.

///

## Etapas anteriores antes de começar { #previous-steps-before-starting }

Há muitos casos em que você deseja executar algumas etapas **antes de iniciar** sua aplicação.

Por exemplo, você pode querer executar **migrações de banco de dados**.

Mas na maioria dos casos, você precisará executar essas etapas apenas **uma vez**.

Portanto, você vai querer ter um **processo único** para executar essas **etapas anteriores** antes de iniciar o aplicativo.

E você terá que se certificar de que é um único processo executando essas etapas anteriores *mesmo* se depois, você iniciar **vários processos** (vários trabalhadores) para o próprio aplicativo. Se essas etapas fossem executadas por **vários processos**, eles **duplicariam** o trabalho executando-o em **paralelo**, e se as etapas fossem algo delicado como uma migração de banco de dados, elas poderiam causar conflitos entre si.

Claro, há alguns casos em que não há problema em executar as etapas anteriores várias vezes; nesse caso, é muito mais fácil de lidar.

/// tip | Dica

Além disso, tenha em mente que, dependendo da sua configuração, em alguns casos você **pode nem precisar de nenhuma etapa anterior** antes de iniciar sua aplicação.

Nesse caso, você não precisaria se preocupar com nada disso. 🤷

///

### Exemplos de estratégias de etapas anteriores { #examples-of-previous-steps-strategies }

Isso **dependerá muito** da maneira como você **implanta seu sistema** e provavelmente estará conectado à maneira como você inicia programas, lida com reinicializações, etc.

Aqui estão algumas ideias possíveis:

* Um "Init Container" no Kubernetes que roda antes do seu app container
* Um script bash que roda os passos anteriores e então inicia seu aplicativo
    * Você ainda precisaria de uma maneira de iniciar/reiniciar *aquele* script bash, detectar erros, etc.

/// tip | Dica

Darei exemplos mais concretos de como fazer isso com contêineres em um capítulo futuro: [FastAPI em contêineres - Docker](docker.md){.internal-link target=_blank}.

///

## Utilização de recursos { #resource-utilization }

Seu(s) servidor(es) é(são) um **recurso** que você pode consumir ou **utilizar**, com seus programas, o tempo de computação nas CPUs e a memória RAM disponível.

Quanto dos recursos do sistema você quer consumir/utilizar? Pode ser fácil pensar "não muito", mas, na realidade, você provavelmente vai querer consumir **o máximo possível sem travar**.

Se você está pagando por 3 servidores, mas está usando apenas um pouco de RAM e CPU, você provavelmente está **desperdiçando dinheiro** 💸, e provavelmente **desperdiçando energia elétrica do servidor** 🌎, etc.

Nesse caso, seria melhor ter apenas 2 servidores e usar uma porcentagem maior de seus recursos (CPU, memória, disco, largura de banda de rede, etc).

Por outro lado, se você tem 2 servidores e está usando **100% da CPU e RAM deles**, em algum momento um processo pedirá mais memória, e o servidor terá que usar o disco como "memória" (o que pode ser milhares de vezes mais lento), ou até mesmo **travar**. Ou um processo pode precisar fazer alguma computação e teria que esperar até que a CPU esteja livre novamente.

Nesse caso, seria melhor obter **um servidor extra** e executar alguns processos nele para que todos tenham **RAM e tempo de CPU suficientes**.

Também há a chance de que, por algum motivo, você tenha um **pico** de uso da sua API. Talvez ela tenha se tornado viral, ou talvez alguns outros serviços ou bots comecem a usá-la. E você pode querer ter recursos extras para estar seguro nesses casos.

Você poderia colocar um **número arbitrário** para atingir, por exemplo, algo **entre 50% a 90%** da utilização de recursos. O ponto é que essas são provavelmente as principais coisas que você vai querer medir e usar para ajustar suas implantações.

Você pode usar ferramentas simples como `htop` para ver a CPU e a RAM usadas no seu servidor ou a quantidade usada por cada processo. Ou você pode usar ferramentas de monitoramento mais complexas, que podem ser distribuídas entre servidores, etc.

## Recapitular { #recap }

Você leu aqui alguns dos principais conceitos que provavelmente precisa ter em mente ao decidir como implantar seu aplicativo:

* Segurança - HTTPS
* Executando na inicialização
* Reinicializações
* Replicação (o número de processos em execução)
* Memória
* Etapas anteriores antes de iniciar

Entender essas ideias e como aplicá-las deve lhe dar a intuição necessária para tomar qualquer decisão ao configurar e ajustar suas implantações. 🤓

Nas próximas seções, darei exemplos mais concretos de possíveis estratégias que você pode seguir. 🚀
