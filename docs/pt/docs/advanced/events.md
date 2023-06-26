# Eventos de vida útil

Você pode definir a lógica (código) que poderia ser executada antes da aplicação **inicializar**. Isso significa que esse código será executado **uma vez**, **antes** da aplicação **começar a receber requisições**.

Do mesmo modo, você pode definir a lógica (código) que será executada quando a aplicação estiver sendo **encerrada**. Nesse caso, este código será executado **uma vez**, **depois** de ter possivelmente tratado **várias requisições**.

Por conta desse código ser executado antes da aplicação **começar** a receber requisições, e logo após **terminar** de lidar com as requisições, ele cobre toda a **vida útil** (_lifespan_) da aplicação (o termo "vida útil" será importante em um segundo 😉).

Pode ser muito útil para configurar **recursos** que você precisa usar por toda aplicação, e que são **compartilhados** entre as requisições, e/ou que você precisa **limpar** depois. Por exemplo, o pool de uma conexão com o banco de dados ou carregamento de um modelo compartilhado de aprendizado de máquina (_machine learning_).

## Caso de uso

Vamos iniciar com um exemplo de **caso de uso** e então ver como resolvê-lo com isso.

Vamos imaginar que você tem alguns **modelos de _machine learning_** que deseja usar para lidar com as requisições. 🤖

Os mesmos modelos são compartilhados entre as requisições, então não é um modelo por requisição, ou um por usuário ou algo parecido.

Vamos imaginar que o carregamento do modelo pode **demorar bastante tempo**, porque ele tem que ler muitos **dados do disco**. Então você não quer fazer isso a cada requisição.

Você poderia carregá-lo no nível mais alto do módulo/arquivo, mas isso também poderia significaria **carregar o modelo** mesmo se você estiver executando um simples teste automatizado, então esse teste poderia ser **lento** porque teria que esperar o carregamento do modelo antes de ser capaz de executar uma parte independente do código.


Isso é que nós iremos resolver, vamos carregar o modelo antes das requisições serem manuseadas, mas apenas um pouco antes da aplicação começar a receber requisições, não enquanto o código estiver sendo carregado.

## Vida útil (_Lifespan_)

Você pode definir essa lógica de *inicialização* e *encerramento* usando os parâmetros de `lifespan` da aplicação `FastAPI`, e um "gerenciador de contexto" (te mostrarei o que é isso a seguir).

Vamos iniciar com um exemplo e ver isso detalhadamente.

Nós criamos uma função assíncrona chamada `lifespan()` com `yield` como este:

```Python hl_lines="16  19"
{!../../../docs_src/events/tutorial003.py!}
```

Aqui nós estamos simulando a *inicialização* custosa do carregamento do modelo colocando a (falsa) função de modelo no dicionário com modelos de _machine learning_ antes do `yield`. Este código será executado **antes** da aplicação **começar a receber requisições**, durante a *inicialização*.

E então, logo após o `yield`, descarregaremos o modelo. Esse código será executado **após** a aplicação **terminar de lidar com as requisições**, pouco antes do *encerramento*. Isso poderia, por exemplo, liberar recursos como memória ou GPU.

!!! tip "Dica"
    O `shutdown` aconteceria quando você estivesse **encerrando** a aplicação.

    Talvez você precise inicializar uma nova versão, ou apenas cansou de executá-la. 🤷

### Função _lifespan_

A primeira coisa a notar, é que estamos definindo uma função assíncrona com `yield`. Isso é muito semelhante à Dependências com `yield`.

```Python hl_lines="14-19"
{!../../../docs_src/events/tutorial003.py!}
```

A primeira parte da função, antes do `yield`, será  executada **antes** da aplicação inicializar.

E a parte posterior do `yield` irá executar **após** a aplicação ser encerrada.

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

Nas versões mais recentes de Python, há também um **gerenciador de contexto assíncrono**. Você o usaria com `async with`:

```Python
async with lifespan(app):
    await do_stuff()
```

Quando você cria um gerenciador de contexto ou um gerenciador de contexto assíncrono como mencionado acima, o que ele faz é que, antes de entrar no bloco `with`, ele irá executar o código anterior ao `yield`, e depois de sair do bloco `with`, ele irá executar o código depois do `yield`.

No nosso exemplo de código acima, nós não usamos ele diretamente, mas nós passamos para o FastAPI para ele usá-lo.

O parâmetro `lifespan` da aplicação `FastAPI` usa um **Gerenciador de Contexto Assíncrono**, então nós podemos passar nosso novo gerenciador de contexto assíncrono do `lifespan` para ele.

```Python hl_lines="22"
{!../../../docs_src/events/tutorial003.py!}
```

## Eventos alternativos (deprecados)

!!! warning "Aviso"
    A maneira recomendada para lidar com a *inicialização* e o *encerramento* é usando o parâmetro `lifespan` da aplicação `FastAPI` como descrito acima.

    Você provavelmente pode pular essa parte.

Existe uma forma alternativa para definir a execução dessa lógica durante *inicialização* e durante *encerramento*.

Você pode definir manipuladores de eventos (funções) que precisam ser executadas antes da aplicação inicializar, ou quando a aplicação estiver encerrando.

Essas funções podem ser declaradas com `async def` ou `def` normal.

### Evento `startup`

Para adicionar uma função que deve rodar antes da aplicação iniciar, declare-a com o evento `"startup"`:

```Python hl_lines="8"
{!../../../docs_src/events/tutorial001.py!}
```

Nesse caso, a função de manipulação de evento `startup` irá inicializar os itens do "banco de dados" (só um `dict`) com alguns valores.

Você pode adicionar mais que uma função de manipulação de evento.

E sua aplicação não irá começar a receber requisições até que todos os manipuladores de eventos de `startup` sejam concluídos.

### Evento `shutdown`

Para adicionar uma função que deve ser executada quando a aplicação estiver encerrando, declare ela com o evento `"shutdown"`:

```Python hl_lines="6"
{!../../../docs_src/events/tutorial002.py!}
```

Aqui, a função de manipulação de evento `shutdown` irá escrever uma linha de texto `"Application shutdown"` no arquivo `log.txt`.

!!! info "Informação"
    Na função `open()`, o `mode="a"` significa "acrescentar", então, a linha irá ser adicionada depois de qualquer coisa que esteja naquele arquivo, sem sobrescrever o conteúdo anterior.

!!! tip "Dica"
    Perceba que nesse caso nós estamos usando a função padrão do Python `open()` que interage com um arquivo.

    Então, isso envolve I/O (input/output), que exige "esperar" que coisas sejam escritas em disco.

    Mas `open()` não usa `async` e `await`.

    Então, nós declaramos uma função de manipulação de evento com o padrão `def` ao invés de `async def`.

### `startup` e `shutdown` juntos

Há uma grande chance que a lógica para sua *inicialização* e *encerramento* esteja conectada, você pode querer iniciar alguma coisa e então finalizá-la, adquirir um recurso e então liberá-lo, etc.

Fazendo isso em funções separadas que não compartilham lógica ou variáveis entre elas é mais difícil já que você precisa armazenar os valores em variáveis globais ou truques parecidos.

Por causa disso, agora é recomendado em vez disso usar o `lifespan` como explicado acima.

## Detalhes técnicos

Só um detalhe técnico para nerds curiosos. 🤓

Por baixo, na especificação técnica ASGI, essa é a parte do <a href="https://asgi.readthedocs.io/en/latest/specs/lifespan.html" class="external-link" target="_blank">Protocolo Lifespan</a>, e define eventos chamados `startup` e `shutdown`.

!!! info "Informação"
    Você pode ler mais sobre o manipulador `lifespan` do Starlette na <a href="https://www.starlette.io/lifespan/" class="external-link" target="_blank">Documentação do Lifespan Starlette</a>.

    Incluindo como manipular estado do lifespan que pode ser usado em outras áreas do seu código.

## Sub Aplicações

🚨 Tenha em mente que esses eventos de lifespan (de inicialização e desligamento) irão somente ser executados para a aplicação principal, não para [Sub Aplicações - Montagem](./sub-applications.md){.internal-link target=_blank}.
