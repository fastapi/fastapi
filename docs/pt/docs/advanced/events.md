# Eventos de vida útil

Você pode definir a lógica (código) que poderia ser executada antes da aplicação **começar**. Isso significa que esse código será executado **uma vez**, **antes** da aplicação **começar a receber requests**.

Do mesmo modo, você pode definir a lógica (código) que será executada quando a aplicação estiver **desligando**. Nesse caso, esse código será executado **uma vez**, **depois** de ter possivelmente tratado **várias requests**.

Por conta desse código ser executado antes da aplição **começar** a receber requests, e logo depois disso **termina** de lidar com as requests, isso cobre toda a **vida útil** da aplicação (o termo "vida útil" será importante em um segundo 😉).

Pode ser muito útil para configurar **recursos** que você precisa usar por toda aplicação, e que são **compartilhadas** entre os requests, e/ou que você precisa **limpar** após. Por exemplo, o pool de uma conexão com o banco, ou carregamento de um modelo compartilhado de _machine learning_.

## Caso de uso

Vamos iniciar com um exemplo de **caso de uso** e então ver como resolvê-lo com isso.

Vamos imaginar que você tem algum **modelos de _machine learning_** que você quer usar para lidar com os requests. 🤖

Os mesmos modelos são compartilhados entre os requests, então, não é um modelo por request, ou um por usuário ou algo parecido.

Vamos imaginar que o carregamento do modelo pode **levar bastante tempo**, porque ele pode ler uma grande quantidade de **dados do disco**. Então você não quer fazer isso a cada request.

Você poderia carregá-lo em um nível mais alto do módulo/arquivo, mas isso poderia também significaria **carregar o modelo** mesmo se você estiver executando um simples teste automatizado, então esse teste poderia ficar **lento** por causa porque teria que esperar o carregamento do modelo antes de ser capaz de executar uma parte independete do código.


Isso é o que nós iremos resolver, vamos carregar o modelo antes das requests serem manuseadas, mas apenas um pouco antes da aplicação iniciar o recebimento de requests, não enquanto o código estiver sendo carregado.

## Lifespan

Você pode defini-lo com lógica de *inicialização* e *desligamento* usando os parâmetros de `lifespan` da aplicação `FastAPI`, e um "gerenciador de contexto" (Te mostrarei o que é isso a seguir).

Vamos iniciar com um exemplo e ver isso detalhadamente.

Nós criamos uma função assíncrona chamada `lifespan()` com `yield` como isso:

```Python hl_lines="16  19"
{!../../../docs_src/events/tutorial003.py!}
```

Aqui nós estamos simulando a *inicialização* custosa de carregamento do modelo colocando a (falsa) função modelo em um dicionário em um dicinário com modelo de _machine learning_ antes do `yield`. Esse código será executado **antes** da aplicação **começar a receber requests**, durante a *inicialização*.

E então, logo após o `yield`, descarregaremos o modelo. Esse código será executado **após** a aplicação **terminar de lidar com os requests**, pouco antes do *desligamento*. Isso poderia, por exemplo, liberar recursos como memória ou GPU.

!!! tip
    O `shutdown` aconteceria quando você está **parando** a aplicação.

    Talvez você precise inicializar uma nova versão, ou apenas cansou de executá-la. 🤷

### Função _lifespan_

A primeira coisa a notar, é que nós estamos definindo uma função assíncrona com `yield`. Isso é muito semelhante à Dependências com `yield`.

```Python hl_lines="14-19"
{!../../../docs_src/events/tutorial003.py!}
```

A primeira parte da função, antes do `yield`, irá ser executada **antes** da aplicação começar.

E a parte posterior do `yield` irá executar **após** a aplicação ser finalizada.

### Gerenciador de Contexto Assíncrono

Se você verificar, a função está decorada com um `@asynccontextmanager`.

Que converte a função em algo chamado de "**Gerenciador de Contexto Assíncrono**".

```Python hl_lines="1  13"
{!../../../docs_src/events/tutorial003.py!}
```

Um **gerenciador de contexto** em Python é algo que você pode usar em uma declaração `with`, por exemplo, `open()` pode ser usado como um gerenciador de contexto:

```Python
with open("file.txt") as file:
    file.read()
```

Nas versões mais recentes de Python, há também um **gerenciador de contexto assíncrono**. Você deveria usar isso com `async with`:

```Python
async with lifespan(app):
    await do_stuff()
```

Quando você cria um gerenciador de contexto ou um gerenciador de contexto assíncrono como o mencionado acima, o que ele faz é que, antes de entrar no bloco `with`, ele irá executar o código anterior ao `yield`, e depois de sair do bloco `with`, ele irá executar o código depois do `yield`.

No nosso exemplo de código acima, nós não usamos ele diretamente, mas nós passamos para o FastAPI para ele usá-lo.

O parâmetro `lifespan` da aplicação `FastAPI` leva um **Gerenciador de Contexto Assíncrono**, então nós podemos passar nosso novo gerenciador de contexto assíncrono do `lifespan` para ele.

```Python hl_lines="22"
{!../../../docs_src/events/tutorial003.py!}
```

## Eventos alternativos (deprecados)

!!! warning
    O caminho recomendável para lidar com a *inicialização* e o *desligamento* é usando o parâmetro `lifespan` da aplicação `FastAPI` como descrito acima.

    Você provavelmente pode pular essa parte.

Há um caminho alternativo para refinir a execução dessa lógica durante *inicialização* e durante *desligamento*.

Você pode definir manipuladores de eventos (funções) que precisam ser executadas antes da aplicação começar, ou quando a aplicação está desligando.

Essas funções podem ser declaradas com `async def` ou `def` normal.

### Evento `startup`

Para adicionar uma função que deve rodar antes da aplicação iniciar, declare-a com o evento `"startup"`:

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

Nesse caso, a função de manipulação de evento `startup` irá inicializar os itens do "database" (só um `dict`) com alguns valores.

Você pode adicionar mais que uma função de manipulação de evento.

E sua aplicação não irá começar a receber requests até que tudo da manipulação de evento `startup` esteja completo.

### Evento `shutdown`

Para adicionar uma função que deve ser executada quando a aplicação estiver desligando, declare ela com o evento `"shutdown"`:

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

Aqui, a função de manipulação de evento `shutdown` irá escrever uma linha de texto `"Application shutdown"` no arquivo `log.txt`.

!!! info
    Na função `open()`, o `mode="a"` significa "acrescentar", então, a linha irá ser adicionada depois de qualquer coisa que esteja naquele arquivo, sem sobrescrever o conteúdo anterior.

!!! tip
    Perceba que nesse caso nós estamos usando a função padrão do Python `open()` que interage com um arquivo.

    Então, isso envolve I/O (input/output), que requer "espera" para coisas serem escritas em disco.

    Mas `open()` não usa `async` e `await`.

    Então, nós declaramos uma função de manipulação de evento com o padrão `def` ao invés de `async def`.

### `startup` e `shutdown` juntos

Há uma grande chance que a lógica para sua *inicialização* e *desligamento* esteja conectada, você pode querer iniciar alguma coisa e então finalizá-la, adquirir um recurso e então liberá-lo, etc.

Fazendo isso em funções separadas que não compartilham lógica ou variáveis entre elas é mais difícil já que você precisa armazenar os valores em variáveis globais ou truques parecidos.

Por causa disso, agora é recomendado em vez disso usar o `lifespan` como explicado acima.

## Detalhes técnicos

Só um detalhe técnico para nerds curiosos. 🤓

Por baixo, na especificação técnica ASGI, essa é a parte do <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Protocolo Lifespan</a>, e define eventos chamados `startup` e `shutdown`.

!!! info
    Você pode ler mais sobre o manipulador `lifespan` do Starlette na <a href="https://www.starlette.io/lifespan/" class="external-link" target="_blank">Documentação do Lifespan Starlette</a>.

    Incluindo como manipular estado do lifespan que pode ser usado em outras áreas do seu código.

## Sub Aplicações

🚨 Tenha em mente que esses eventos de lifespan (de inicialização e desligamento) irão somente ser executados para a aplicação principal, não para [Sub Aplicações - Montagem](./sub-applications.md){.internal-link target=_blank}.
