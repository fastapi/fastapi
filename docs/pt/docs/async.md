# Concorrência e async / await { #concurrency-and-async-await }

Detalhes sobre a sintaxe `async def` para *funções de operação de rota* e alguns conceitos de código assíncrono, concorrência e paralelismo.

## Com pressa? { #in-a-hurry }

<abbr title="too long; didn't read – muito longo; não li"><strong>TL;DR:</strong></abbr>

Se você estiver utilizando bibliotecas de terceiros que dizem para você chamar as funções com `await`, como:

```Python
results = await some_library()
```

Então, declare suas *funções de operação de rota* com `async def` como:

```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | Nota

Você só pode usar `await` dentro de funções criadas com `async def`.

///

---

Se você está usando uma biblioteca de terceiros que se comunica com alguma coisa (um banco de dados, uma API, o sistema de arquivos etc.) e não tem suporte para utilizar `await` (esse é atualmente o caso para a maioria das bibliotecas de banco de dados), então declare suas *funções de operação de rota* normalmente, com apenas `def`, como:

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

Se sua aplicação (de alguma forma) não tem que se comunicar com nada mais e esperar que o respondam, use `async def`, mesmo que você não precise usar `await` dentro dela.

---

Se você simplesmente não sabe, use apenas `def`.

---

**Note**: Você pode misturar `def` e `async def` nas suas *funções de operação de rota* tanto quanto necessário e definir cada função usando a melhor opção para você. FastAPI irá fazer a coisa certa com elas.

De qualquer forma, em ambos os casos acima, FastAPI irá trabalhar assincronamente e ser extremamente rápido.

Mas, seguindo os passos acima, ele será capaz de fazer algumas otimizações de performance.

## Detalhes Técnicos { #technical-details }

Versões modernas de Python têm suporte para **"código assíncrono"** usando algo chamado **"corrotinas"**, com sintaxe **`async` e `await`**.

Vamos ver aquela frase por partes nas seções abaixo:

* **Código assíncrono**
* **`async` e `await`**
* **Corrotinas**

## Código assíncrono { #asynchronous-code }

Código assíncrono apenas significa que a linguagem 💬 tem um jeito de dizer para o computador / programa 🤖 que em certo ponto do código, ele 🤖 terá que esperar *algo* finalizar em outro lugar. Vamos dizer que esse *algo* seja chamado "arquivo lento" 📝.

Então, durante esse tempo, o computador pode ir e fazer outro trabalho, enquanto o "arquivo lento" 📝 termina.

Então o computador / programa 🤖 irá voltar sempre que tiver uma chance, seja porque ele está esperando novamente, ou quando ele 🤖 terminar todo o trabalho que tem até esse ponto. E ele 🤖 irá ver se alguma das tarefas que estava esperando já terminaram de fazer o que quer que tinham que fazer.

Depois, ele 🤖 pega a primeira tarefa para finalizar (vamos dizer, nosso "arquivo lento" 📝) e continua o que tem que fazer com ela.

Esse "esperar por algo" normalmente se refere a operações <abbr title="Input and Output – Entrada e Saída">I/O</abbr> que são relativamente "lentas" (comparadas à velocidade do processador e da memória RAM), como esperar por:

* dados do cliente para serem enviados através da rede
* dados enviados pelo seu programa serem recebidos pelo cliente através da rede
* conteúdo de um arquivo no disco ser lido pelo sistema e entregue ao seu programa
* conteúdo que seu programa deu ao sistema para ser escrito no disco
* uma operação em uma API remota
* uma operação no banco de dados finalizar
* uma solicitação no banco de dados retornar o resultado
* etc.

Quanto o tempo de execução é consumido majoritariamente pela espera de operações <abbr title="Input and Output – Entrada e Saída">I/O</abbr>, essas operações são chamadas operações "limitadas por I/O".

Isso é chamado de "assíncrono" porque o computador / programa não tem que ser "sincronizado" com a tarefa lenta, esperando pelo momento exato em que a tarefa finaliza, enquanto não faz nada, para ser capaz de pegar o resultado da tarefa e dar continuidade ao trabalho.

Ao invés disso, sendo um sistema "assíncrono", uma vez finalizada, a tarefa pode esperar na fila um pouco (alguns microssegundos) para que o computador / programa finalize o que quer que esteja fazendo, e então volte para pegar o resultado e continue trabalhando com ele.

Para "síncrono" (contrário de "assíncrono") também é utilizado o termo "sequencial", porquê o computador / programa segue todos os passos, em sequência, antes de trocar para uma tarefa diferente, mesmo se alguns passos envolvam esperar.

### Concorrência e hambúrgueres { #concurrency-and-burgers }

Essa ideia de código **assíncrono** descrita acima é às vezes chamada de **"concorrência"**. Isso é diferente de **"paralelismo"**.

**Concorrência** e **paralelismo** ambos são relacionados a "diferentes coisas acontecendo mais ou menos ao mesmo tempo".

Mas os detalhes entre *concorrência* e *paralelismo* são bem diferentes.

Para ver essa diferença, imagine a seguinte história sobre hambúrgueres:

### Hambúrgueres concorrentes { #concurrent-burgers }

Você vai com seu _crush_ na lanchonete, e fica na fila enquanto o caixa pega os pedidos das pessoas na sua frente. 😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

Então chega a sua vez, você pede dois saborosos hambúrgueres para você e seu _crush_.  🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

O caixa diz alguma coisa para o cozinheiro na cozinha para que eles saibam que têm que preparar seus hambúrgueres (mesmo que ele esteja atualmente preparando os lanches dos outros clientes).

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

Você paga. 💸

O caixa te entrega seu número de chamada.

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

Enquanto você espera, você vai com seu _crush_ e pega uma mesa, senta e conversa com seu _crush_ por um bom tempo (já que seus hambúrgueres são muito saborosos, e leva um tempo para serem preparados).

Já que você está sentado na mesa com seu _crush_, esperando os hambúrgueres, você pode passar esse tempo admirando o quão lindo, maravilhoso e esperto é seu _crush_ ✨😍✨.

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

Enquanto espera e conversa com seu _crush_, de tempos em tempos, você verifica o número da chamada exibido no balcão para ver se já é sua vez.

Então em algum momento, é finalmente sua vez. Você vai ao balcão, pega seus hambúrgueres e volta para a mesa.

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

Você e seu _crush_ comem os hambúrgueres e aproveitam o tempo. ✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info | Informação

Belas ilustrações de <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

Imagine que você seja o computador / programa 🤖 nessa história.

Enquanto você está na fila, você está somente ocioso 😴, esperando por sua vez, sem fazer nada muito "produtivo". Mas a fila é rápida porque o caixa só está pegando os pedidos (não os preparando), então está tudo bem.

Então, quando é sua vez, você faz trabalho realmente "produtivo", você processa o menu, decide o que quer, pega a escolha de seu _crush_, paga, verifica se entregou o cartão ou a cédula correta, verifica se foi cobrado corretamente, verifica se seu pedido está correto etc.

Mas então, embora você ainda não tenha os hambúrgueres, seu trabalho no caixa está "pausado" ⏸, porque você tem que esperar 🕙 seus hambúrgueres ficarem prontos.

Contudo, à medida que você se afasta do balcão e senta na mesa, com um número para sua chamada, você pode trocar 🔀 sua atenção para seu _crush_, e "trabalhar" ⏯ 🤓 nisso. Então você está novamente fazendo algo muito "produtivo", como flertar com seu _crush_ 😍.

Então o caixa 💁 diz que "seus hambúrgueres estão prontos" colocando seu número no balcão, mas você não corre que nem um maluco imediatamente quando o número exibido é o seu. Você sabe que ninguém irá roubar seus hambúrgueres porque você tem o seu número da chamada, e os outros têm os deles.

Então você espera seu _crush_ terminar a história que estava contando (terminar o trabalho atual ⏯ / tarefa sendo processada 🤓), sorri gentilmente e diz que você está indo buscar os hambúrgueres ⏸.

Então você vai ao balcão 🔀, para a tarefa inicial que agora está finalizada ⏯, pega os hambúrgueres, agradece, e leva-os para a mesa. Isso finaliza esse passo / tarefa da interação com o balcão ⏹. Isso, por sua vez, cria uma nova tarefa, a de "comer hambúrgueres" 🔀 ⏯, mas a tarefa anterior de "pegar os hambúrgueres" já está finalizada ⏹.

### Hambúrgueres paralelos { #parallel-burgers }

Agora vamos imaginar que esses não são "Hambúrgueres Concorrentes", e sim "Hambúrgueres Paralelos".

Você vai com seu _crush_ na lanchonete paralela.

Você fica na fila enquanto vários (vamos dizer 8) caixas que também são cozinheiros pegam os pedidos das pessoas na sua frente.

Todo mundo na sua frente está esperando seus hambúrgueres ficarem prontos antes de deixar o caixa porque cada um dos 8 caixas vai e prepara o hambúrguer logo após receber o pedido, antes de pegar o próximo pedido.

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

Então é finalmente sua vez, você pede 2 hambúrgueres muito saborosos para você e seu _crush_.

Você paga 💸.

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

O caixa vai para a cozinha.

Você espera, na frente do balcão 🕙, para que ninguém pegue seus hambúrgueres antes de você, já que não tem números de chamadas.

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

Como você e seu _crush_ estão ocupados não permitindo que ninguém passe na frente e pegue seus hambúrgueres assim que estiverem prontos, você não pode dar atenção ao seu _crush_. 😞

Isso é trabalho "síncrono", você está "sincronizado" com o caixa / cozinheiro 👨‍🍳. Você tem que esperar 🕙 e estar lá no exato momento que o caixa / cozinheiro 👨‍🍳 terminar os hambúrgueres e os der a você, ou então, outro alguém pode pegá-los.

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

Então seu caixa / cozinheiro 👨‍🍳 finalmente volta com seus hambúrgueres, depois de um longo tempo esperando 🕙 por eles em frente ao balcão.

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

Você pega seus hambúrgueres e vai para a mesa com seu _crush_.

Vocês comem os hambúrgueres, e o trabalho está terminado. ⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

Não houve muita conversa ou flerte já que a maior parte do tempo foi gasto esperando 🕙 na frente do balcão. 😞

/// info | Informação

Belas ilustrações de <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

Nesse cenário dos hambúrgueres paralelos, você é um computador / programa 🤖 com dois processadores (você e seu _crush_), ambos esperando 🕙 e dedicando sua atenção ⏯ "esperando no balcão" 🕙 por um bom tempo.

A lanchonete paralela tem 8 processadores (caixas / cozinheiros), enquanto a lanchonete dos hambúrgueres concorrentes tinha apenas 2 (um caixa e um cozinheiro).

Ainda assim, a experiência final não foi a melhor. 😞

---

Essa seria o equivalente paralelo à história dos hambúrgueres. 🍔

Para um exemplo "mais real", imagine um banco.

Até recentemente, a maioria dos bancos tinham muitos caixas 👨‍💼👨‍💼👨‍💼👨‍💼 e uma grande fila 🕙🕙🕙🕙🕙🕙🕙🕙.

Todos os caixas fazendo todo o trabalho, um cliente após o outro 👨‍💼⏯.

E você tinha que esperar 🕙 na fila por um longo tempo ou poderia perder a vez.

Você provavelmente não gostaria de levar seu _crush_ 😍 com você para um rolezinho no banco 🏦.

### Conclusão dos hambúrgueres { #burger-conclusion }

Nesse cenário dos "hambúrgueres com seu _crush_", como tem muita espera, faz mais sentido ter um sistema concorrente ⏸🔀⏯.

Esse é o caso da maioria das aplicações web.

Muitos, muitos usuários, mas seu servidor está esperando 🕙 pela sua conexão não tão boa enviar suas requisições.

E então esperando 🕙 novamente as respostas voltarem.

Essa "espera" 🕙 é medida em microssegundos, mas ainda assim, somando tudo, é um monte de espera no final.

Por isso que faz bastante sentido utilizar código assíncrono ⏸🔀⏯ para APIs web.

Esse tipo de assincronicidade é o que fez NodeJS popular (embora NodeJS não seja paralelo) e essa é a força do Go como uma linguagem de programação.

E esse é o mesmo nível de performance que você tem com o **FastAPI**.

E como você pode ter paralelismo e assincronicidade ao mesmo tempo, você tem uma maior performance do que a maioria dos frameworks NodeJS testados e lado a lado com Go, que é uma linguagem compilada, mais próxima ao C <a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">(tudo graças ao Starlette)</a>.

### Concorrência é melhor que paralelismo? { #is-concurrency-better-than-parallelism }

Não! Essa não é a moral da história.

Concorrência é diferente de paralelismo. E é melhor em cenários **específicos** que envolvam um monte de espera. Por isso, geralmente é muito melhor do que paralelismo para desenvolvimento de aplicações web. Mas não para tudo.

Então, para equilibrar tudo, imagine a seguinte historinha:

> Você tem que limpar uma casa grande e suja.

*Sim, essa é toda a história*.

---

Não há espera 🕙 em lugar algum, apenas um monte de trabalho para ser feito, em múltiplos cômodos da casa.

Você poderia ter turnos como no exemplo dos hambúrgueres, primeiro a sala de estar, então a cozinha, mas como você não está esperando por nada, apenas limpando e limpando, as chamadas não afetariam em nada.

Levaria o mesmo tempo para finalizar com ou sem turnos (concorrência) e você teria feito o mesmo tanto de trabalho.

Mas nesse caso, se você trouxesse os 8 ex-caixas / cozinheiros / agora-faxineiros, e cada um deles (mais você) pudessem dividir a casa para limpá-la, vocês fariam toda a limpeza em **paralelo**, com a ajuda extra, e terminariam muito mais cedo.

Nesse cenário, cada um dos faxineiros (incluindo você) poderia ser um processador, fazendo a sua parte do trabalho.

E a maior parte do tempo de execução é tomada por trabalho real (ao invés de ficar esperando), e o trabalho em um computador é feito pela <abbr title="Central Processing Unit – Unidade Central de Processamento">CPU</abbr>. Eles chamam esses problemas de "limitados por CPU".

---

Exemplos comuns de operações limitadas por CPU são coisas que exigem processamento matemático complexo.

Por exemplo:

* **Processamento de áudio** ou **imagem**
* **Visão Computacional**: uma imagem é composta por milhões de pixels, cada pixel tem 3 valores / cores, processar isso normalmente exige alguma computação em todos esses pixels ao mesmo tempo
* **Aprendizado de Máquina**: Normalmente exige muita multiplicação de matrizes e vetores. Pense numa grande planilha com números e em multiplicar todos eles juntos e ao mesmo tempo.
* **Deep Learning**: Esse é um subcampo do Aprendizado de Máquina, então, o mesmo se aplica. A diferença é que não há apenas uma grande planilha com números para multiplicar, mas um grande conjunto delas, e em muitos casos, você utiliza um processador especial para construir e/ou usar esses modelos.

### Concorrência + Paralelismo: Web + Aprendizado de Máquina { #concurrency-parallelism-web-machine-learning }

Com **FastAPI** você pode levar a vantagem da concorrência que é muito comum para desenvolvimento web (o mesmo atrativo de NodeJS).

Mas você também pode explorar os benefícios do paralelismo e multiprocessamento (tendo múltiplos processadores rodando em paralelo) para trabalhos **limitados por CPU** como aqueles em sistemas de Aprendizado de Máquina.

Isso, somado ao simples fato que Python é a principal linguagem para **Data Science**, Aprendizado de Máquina e especialmente Deep Learning, faz do FastAPI uma ótima escolha para APIs web e aplicações com Data Science / Aprendizado de Máquina (entre muitas outras).

Para ver como alcançar esse paralelismo em produção veja a seção sobre [Implantação](deployment/index.md){.internal-link target=_blank}.

## `async` e `await` { #async-and-await }

Versões modernas do Python têm um modo muito intuitivo para definir código assíncrono. Isso faz parecer do mesmo jeito do código normal "sequencial" e fazer a "espera" para você nos momentos certos.

Quando tem uma operação que exigirá espera antes de dar os resultados e tem suporte para esses novos recursos do Python, você pode escrever assim:

```Python
burgers = await get_burgers(2)
```

A chave aqui é o `await`. Ele diz ao Python que ele tem que esperar ⏸ por `get_burgers(2)` finalizar suas coisas 🕙 antes de armazenar os resultados em `burgers`. Com isso, o Python saberá que ele pode ir e fazer outras coisas 🔀 ⏯ nesse meio tempo (como receber outra requisição).

Para o `await` funcionar, tem que estar dentro de uma função que suporte essa assincronicidade. Para fazer isso, apenas declare a função com `async def`:

```Python hl_lines="1"
async def get_burgers(number: int):
    # Faz alguma coisa assíncrona para criar os hambúrgueres
    return burgers
```

...ao invés de `def`:

```Python hl_lines="2"
# Isso não é assíncrono
def get_sequential_burgers(number: int):
    # Faz alguma coisa sequencial para criar os hambúrgueres
    return burgers
```

Com `async def`, o Python sabe que, dentro dessa função, ele deve estar ciente das expressões `await`, e que isso poderá "pausar" ⏸ a execução dessa função, e ir fazer outra coisa 🔀 antes de voltar.

Quando você quiser chamar uma função `async def`, você tem que "esperar" ela. Então, isso não funcionará:

```Python
# Isso não irá funcionar, porquê get_burgers foi definido com: async def
burgers = get_burgers(2)
```

---

Então, se você está usando uma biblioteca que diz que você pode chamá-la com `await`, você precisa criar as *funções de operação de rota* com `async def`, como em:

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### Mais detalhes técnicos { #more-technical-details }

Você deve ter observado que `await` pode ser usado somente dentro de funções definidas com `async def`.

Mas ao mesmo tempo, funções definidas com `async def` têm que ser "aguardadas". Então, funções com `async def` podem ser chamadas somente dentro de funções definidas com `async def` também.

Então, sobre o ovo e a galinha, como você chama a primeira função async?

Se você estivar trabalhando com **FastAPI** não terá que se preocupar com isso, porquê essa "primeira" função será a sua *função de operação de rota*, e o FastAPI saberá como fazer a coisa certa.

Mas se você quiser usar `async` / `await` sem FastAPI, você também pode fazê-lo.

### Escreva seu próprio código assíncrono { #write-your-own-async-code }

Starlette (e **FastAPI**) são baseados no <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a>, o que o torna compatível com ambos o <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> da biblioteca padrão do Python, e o <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>.

Em particular, você pode usar diretamente o <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> para seus casos de uso avançados de concorrência que requerem padrões mais avançados no seu próprio código.

E até se você não estiver utilizando FastAPI, você também pode escrever suas próprias aplicações assíncronas com o <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> por ser altamente compatível e ganhar seus benefícios (e.g. *concorrência estruturada*).

Eu criei outra biblioteca em cima do AnyIO, como uma fina camada acima, para melhorar um pouco as anotações de tipo e obter melhor **preenchimento automático**, **erros inline**, etc. Ela também possui uma introdução amigável e um tutorial para ajudar você a **entender** e escrever **seu próprio código async**: <a href="https://asyncer.tiangolo.com/" class="external-link" target="_blank">Asyncer</a>. Seria particularmente útil se você precisar **combinar código async com código regular** (bloqueador/síncrono).

### Outras formas de código assíncrono { #other-forms-of-asynchronous-code }

Esse estilo de usar `async` e `await` é relativamente novo na linguagem.

Mas ele faz o trabalho com código assíncrono muito mais fácil.

Essa mesma sintaxe (ou quase a mesma) foi também incluída recentemente em versões modernas do JavaScript (no navegador e NodeJS).

Mas antes disso, controlar código assíncrono era bem mais complexo e difícil.

Nas versões anteriores do Python, você poderia utilizar threads ou <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a>. Mas o código é bem mais complexo de entender, debugar, e pensar sobre.

Nas versões anteriores do NodeJS / Navegador JavaScript, você utilizaria "callbacks". O que leva ao "inferno do callback".

## Corrotinas { #coroutines }

**Corrotina** é apenas um jeito bonitinho para a coisa que é retornada de uma função `async def`. O Python sabe que é algo como uma função, que pode começar e que vai terminar em algum ponto, mas que pode ser pausada ⏸ internamente também, sempre que tiver um `await` dentro dela.

Mas toda essa funcionalidade de código assíncrono com `async` e `await` é muitas vezes resumida como usando "corrotinas". É comparável ao principal recurso chave do Go, a "Gorrotina".

## Conclusão { #conclusion }

Vamos ver a mesma frase de cima:

> Versões modernas do Python têm suporte para **"código assíncrono"** usando algo chamado **"corrotinas"**, com sintaxe **`async` e `await`**.

Isso pode fazer mais sentido agora. ✨

Tudo isso é o que empodera o FastAPI (através do Starlette) e que o faz ter uma performance tão impressionante.

## Detalhes muito técnicos { #very-technical-details }

/// warning | Atenção

Você pode provavelmente pular isso.

Esses são detalhes muito técnicos de como **FastAPI** funciona por baixo do capô.

Se você tem certo conhecimento técnico (corrotinas, threads, blocking etc) e está curioso sobre como o FastAPI controla o `async def` vs normal `def`, vá em frente.

///

### Funções de operação de rota { #path-operation-functions }

Quando você declara uma *função de operação de rota* com `def` normal ao invés de `async def`, ela é rodada em uma threadpool externa que é então aguardada, ao invés de ser chamada diretamente (já que ela bloquearia o servidor).

Se você está chegando de outro framework assíncrono que não funciona como descrito acima e você está acostumado a definir *funções de operação de rota* triviais somente de computação com simples `def` para ter um mínimo ganho de performance (cerca de 100 nanosegundos), por favor observe que no **FastAPI** o efeito pode ser bem o oposto. Nesses casos, é melhor usar `async def` a menos que suas *funções de operação de rota* utilizem código que performe bloqueamento <abbr title="Input/Output – Entrada e Saída: leitura ou escrita no disco, comunicações de rede.">I/O</abbr>.

Ainda, em ambas as situações, as chances são que o **FastAPI** [ainda será mais rápido](index.md#performance){.internal-link target=_blank} do que (ou ao menos comparável a) seu framework anterior.

### Dependências { #dependencies }

O mesmo se aplica para as [dependências](tutorial/dependencies/index.md){.internal-link target=_blank}. Se uma dependência tem as funções com padrão `def` ao invés de `async def`, ela é rodada no threadpool externo.

### Sub-dependências { #sub-dependencies }

Você pode ter múltiplas dependências e [sub-dependências](tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} requisitando uma à outra (como parâmetros de definições de funções), algumas delas podem ser criadas com `async def` e algumas com `def` normal. Isso ainda funcionaria, e aquelas criadas com `def` normal seriam chamadas em uma thread externa (do threadpool) ao invés de serem "aguardadas".

### Outras funções de utilidade { #other-utility-functions }

Qualquer outra função de utilidade que você chame diretamente pode ser criada com `def` normal ou `async def` e o FastAPI não irá afetar o modo como você a chama.

Isso está em contraste às funções que o FastAPI chama para você: *funções de operação de rota* e dependências.

Se sua função de utilidade é uma função normal com `def`, ela será chamada diretamente (como você a escreve no código), não em uma threadpool, se a função é criada com `async def` então você deve esperar por essa função quando você chamá-la no seu código.

---

Novamente, esses são detalhes muito técnicos que provavelmente seriam úteis caso você esteja procurando por eles.

Caso contrário, você deve ficar bem com as dicas da seção acima: <a href="#in-a-hurry">Com pressa?</a>.
