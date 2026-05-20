# Eventos de lifespan { #lifespan-events }

Você pode definir a lógica (código) que deve ser executada antes da aplicação **inicializar**. Isso significa que esse código será executado **uma vez**, **antes** de a aplicação **começar a receber requisições**.

Da mesma forma, você pode definir a lógica (código) que deve ser executada quando a aplicação estiver **encerrando**. Nesse caso, esse código será executado **uma vez**, **depois** de possivelmente ter tratado **várias requisições**.

Como esse código é executado antes de a aplicação **começar** a receber requisições e logo depois que ela **termina** de lidar com as requisições, ele cobre todo o **lifespan** da aplicação (a palavra "lifespan" será importante em um segundo 😉).

Isso pode ser muito útil para configurar **recursos** que você precisa usar por toda a aplicação, e que são **compartilhados** entre as requisições e/ou que você precisa **limpar** depois. Por exemplo, um pool de conexões com o banco de dados ou o carregamento de um modelo de Aprendizado de Máquina compartilhado.

## Caso de uso { #use-case }

Vamos começar com um exemplo de **caso de uso** e então ver como resolvê-lo com isso.

Vamos imaginar que você tem alguns **modelos de Aprendizado de Máquina** que deseja usar para lidar com as requisições. 🤖

Os mesmos modelos são compartilhados entre as requisições, então não é um modelo por requisição, ou um por usuário, ou algo parecido.

Vamos imaginar que o carregamento do modelo pode **demorar bastante tempo**, porque ele precisa ler muitos **dados do disco**. Então você não quer fazer isso a cada requisição.

Você poderia carregá-lo no nível mais alto do módulo/arquivo, mas isso também significaria **carregar o modelo** mesmo se você estivesse executando um teste automatizado simples; então esse teste poderia ser **lento** porque teria que esperar o carregamento do modelo antes de conseguir executar uma parte independente do código.

É isso que vamos resolver: vamos carregar o modelo antes de as requisições serem tratadas, mas apenas um pouco antes de a aplicação começar a receber requisições, não enquanto o código estiver sendo carregado.

## Lifespan { #lifespan }

Você pode definir essa lógica de *inicialização* e *encerramento* usando o parâmetro `lifespan` da aplicação `FastAPI`, e um "gerenciador de contexto" (vou mostrar o que é isso em um segundo).

Vamos começar com um exemplo e depois ver em detalhes.

Nós criamos uma função assíncrona `lifespan()` com `yield` assim:

{* ../../docs_src/events/tutorial003_py310.py hl[16,19] *}

Aqui estamos simulando a operação de *inicialização* custosa de carregar o modelo, colocando a (falsa) função do modelo no dicionário com modelos de Aprendizado de Máquina antes do `yield`. Esse código será executado **antes** de a aplicação **começar a receber requisições**, durante a *inicialização*.

E então, logo após o `yield`, descarregamos o modelo. Esse código será executado **depois** de a aplicação **terminar de lidar com as requisições**, pouco antes do *encerramento*. Isso poderia, por exemplo, liberar recursos como memória ou uma GPU.

/// tip | Dica

O `shutdown` aconteceria quando você estivesse **encerrando** a aplicação.

Talvez você precise iniciar uma nova versão, ou apenas cansou de executá-la. 🤷

///

### Função lifespan { #lifespan-function }

A primeira coisa a notar é que estamos definindo uma função assíncrona com `yield`. Isso é muito semelhante a Dependências com `yield`.

{* ../../docs_src/events/tutorial003_py310.py hl[14:19] *}

A primeira parte da função, antes do `yield`, será executada **antes** de a aplicação iniciar.

E a parte posterior ao `yield` será executada **depois** de a aplicação ter terminado.

### Gerenciador de contexto assíncrono { #async-context-manager }

Se você verificar, a função está decorada com um `@asynccontextmanager`.

Isso converte a função em algo chamado "**gerenciador de contexto assíncrono**".

{* ../../docs_src/events/tutorial003_py310.py hl[1,13] *}

Um **gerenciador de contexto** em Python é algo que você pode usar em uma declaração `with`, por exemplo, `open()` pode ser usado como um gerenciador de contexto:

```Python
with open("file.txt") as file:
    file.read()
```

Em versões mais recentes do Python, há também um **gerenciador de contexto assíncrono**. Você o usaria com `async with`:

```Python
async with lifespan(app):
    await do_stuff()
```

Quando você cria um gerenciador de contexto ou um gerenciador de contexto assíncrono como acima, o que ele faz é: antes de entrar no bloco `with`, ele executa o código antes do `yield`, e após sair do bloco `with`, ele executa o código depois do `yield`.

No nosso exemplo de código acima, não o usamos diretamente, mas passamos para o FastAPI para que ele o use.

O parâmetro `lifespan` da aplicação `FastAPI` aceita um **gerenciador de contexto assíncrono**, então podemos passar para ele nosso novo gerenciador de contexto assíncrono `lifespan`.

{* ../../docs_src/events/tutorial003_py310.py hl[22] *}

## Eventos alternativos (descontinuados) { #alternative-events-deprecated }

/// warning | Atenção

A forma recomendada de lidar com a *inicialização* e o *encerramento* é usando o parâmetro `lifespan` da aplicação `FastAPI`, como descrito acima. Se você fornecer um parâmetro `lifespan`, os manipuladores de eventos `startup` e `shutdown` não serão mais chamados. É tudo `lifespan` ou tudo por eventos, não ambos.

Você provavelmente pode pular esta parte.

///

Existe uma forma alternativa de definir essa lógica para ser executada durante a *inicialização* e durante o *encerramento*.

Você pode definir manipuladores de eventos (funções) que precisam ser executados antes de a aplicação iniciar ou quando a aplicação estiver encerrando.

Essas funções podem ser declaradas com `async def` ou `def` normal.

### Evento `startup` { #startup-event }

Para adicionar uma função que deve rodar antes de a aplicação iniciar, declare-a com o evento `"startup"`:

{* ../../docs_src/events/tutorial001_py310.py hl[8] *}

Nesse caso, a função de manipulador do evento `startup` inicializará os itens do "banco de dados" (apenas um `dict`) com alguns valores.

Você pode adicionar mais de uma função de manipulador de eventos.

E sua aplicação não começará a receber requisições até que todos os manipuladores de eventos `startup` sejam concluídos.

### Evento `shutdown` { #shutdown-event }

Para adicionar uma função que deve ser executada quando a aplicação estiver encerrando, declare-a com o evento `"shutdown"`:

{* ../../docs_src/events/tutorial002_py310.py hl[6] *}

Aqui, a função de manipulador do evento `shutdown` escreverá uma linha de texto `"Application shutdown"` no arquivo `log.txt`.

/// info | Informação

Na função `open()`, o `mode="a"` significa "acrescentar", então a linha será adicionada depois do que já estiver naquele arquivo, sem sobrescrever o conteúdo anterior.

///

/// tip | Dica

Perceba que, nesse caso, estamos usando a função padrão do Python `open()` que interage com um arquivo.

Então, isso envolve I/O (input/output), que requer "esperar" que as coisas sejam escritas em disco.

Mas `open()` não usa `async` e `await`.

Assim, declaramos a função de manipulador de evento com `def` padrão em vez de `async def`.

///

### `startup` e `shutdown` juntos { #startup-and-shutdown-together }

Há uma grande chance de que a lógica para sua *inicialização* e *encerramento* esteja conectada, você pode querer iniciar alguma coisa e então finalizá-la, adquirir um recurso e então liberá-lo, etc.

Fazer isso em funções separadas que não compartilham lógica ou variáveis entre si é mais difícil, pois você precisaria armazenar valores em variáveis globais ou truques semelhantes.

Por causa disso, agora é recomendado usar o `lifespan`, como explicado acima.

## Detalhes técnicos { #technical-details }

Apenas um detalhe técnico para nerds curiosos. 🤓

Por baixo, na especificação técnica do ASGI, isso é parte do [Protocolo Lifespan](https://asgi.readthedocs.io/en/latest/specs/lifespan.html), e define eventos chamados `startup` e `shutdown`.

/// info | Informação

Você pode ler mais sobre os manipuladores de `lifespan` do Starlette na [Documentação do Lifespan do Starlette](https://www.starlette.dev/lifespan/).

Incluindo como lidar com estado do lifespan que pode ser usado em outras áreas do seu código.

///

## Sub Aplicações { #sub-applications }

🚨 Tenha em mente que esses eventos de lifespan (inicialização e encerramento) serão executados apenas para a aplicação principal, não para [Sub Aplicações - Montagem](sub-applications.md).
