# Dependências avançadas { #advanced-dependencies }


## Dependências parametrizadas { #parameterized-dependencies }

Todas as dependências que vimos até agora são funções ou classes fixas.

Mas podem ocorrer casos onde você deseja ser capaz de definir parâmetros na dependência, sem ter a necessidade de declarar diversas funções ou classes.

Vamos imaginar que queremos ter uma dependência que verifica se o parâmetro de consulta `q` contém algum conteúdo fixo.

Porém nós queremos poder parametrizar o conteúdo fixo.

## Uma instância "chamável" { #a-callable-instance }

Em Python existe uma maneira de fazer com que uma instância de uma classe seja um "chamável".

Não propriamente a classe (que já é um chamável), mas a instância desta classe.

Para fazer isso, nós declaramos o método `__call__`:

{* ../../docs_src/dependencies/tutorial011.py hl[12] *}

Neste caso, o `__call__` é o que o **FastAPI** utilizará para verificar parâmetros adicionais e sub dependências, e isso é o que será chamado para passar o valor ao parâmetro na sua *função de operação de rota* posteriormente.

## Parametrize a instância { #parameterize-the-instance }

E agora, nós podemos utilizar o `__init__` para declarar os parâmetros da instância que podemos utilizar para "parametrizar" a dependência:

{* ../../docs_src/dependencies/tutorial011.py hl[9] *}

Neste caso, o **FastAPI** nunca tocará ou se importará com o `__init__`, nós vamos utilizar diretamente em nosso código.

## Crie uma instância { #create-an-instance }

Nós poderíamos criar uma instância desta classe com:

{* ../../docs_src/dependencies/tutorial011.py hl[18] *}

E deste modo nós podemos "parametrizar" a nossa dependência, que agora possui `"bar"` dentro dele, como o atributo `checker.fixed_content`.

## Utilize a instância como dependência { #use-the-instance-as-a-dependency }

Então, nós podemos utilizar este `checker` em um `Depends(checker)`, no lugar de `Depends(FixedContentQueryChecker)`, porque a dependência é a instância, `checker`, e não a própria classe.

E quando a dependência for resolvida, o **FastAPI** chamará este `checker` como:

```Python
checker(q="somequery")
```

...e passar o que quer que isso retorne como valor da dependência em nossa *função de operação de rota* como o parâmetro `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011.py hl[22] *}

/// tip | Dica

Tudo isso parece não ser natural. E pode não estar muito claro ou aparentar ser útil ainda.

Estes exemplos são intencionalmente simples, porém mostram como tudo funciona.

Nos capítulos sobre segurança, existem funções utilitárias que são implementadas desta maneira.

Se você entendeu tudo isso, você já sabe como essas funções utilitárias para segurança funcionam por debaixo dos panos.

///

## Limite a concorrência de dependências { #limit-dependency-concurrency }

Em alguns casos, você pode querer limitar quantos requests podem usar uma dependência ao mesmo tempo.

Por exemplo, seu banco de dados pode ter um número limitado de conexões disponíveis. Você poderia fazer novos requests esperarem antes de criar uma sessão, até que outro request termine de usar a sua.

Você pode fazer isso com `max_concurrency` em `Depends()`.

Vamos atualizar o alias `SessionDep` do [tutorial de bancos de dados SQL](../tutorial/sql-databases.md):

```Python
SessionDep = Annotated[Session, Depends(get_session, max_concurrency=5)]
```

Agora, até **cinco requests** podem ter uma sessão de banco de dados aberta por meio dessa dependência ao mesmo tempo.

Se outro request precisar de uma sessão, ele espera até que uma dessas sessões seja fechada.

Enquanto espera, ele **não ocupa uma thread de trabalho**, então essas threads ficam disponíveis para executar outro código.

O valor deve ser um inteiro positivo. O padrão é `None`, o que significa que o FastAPI não limita quantas vezes a dependência pode ser executada ao mesmo tempo.

### Compartilhe o limite entre rotas { #share-the-limit-between-routes }

Todas as rotas nesse exemplo usam o mesmo alias `SessionDep`, então compartilham o limite de cinco sessões.

Para compartilhar um limite, reutilize o **mesmo objeto `Depends()`**, por exemplo em um alias `Annotated` como este.

Se você escrever um novo `Depends(get_session, max_concurrency=5)` para cada rota, cada uma terá seu próprio limite de cinco. Isso vale mesmo que todas usem a mesma função `get_session`.

Reutilizar o mesmo `SessionDep` em outra aplicação também compartilha o limite, desde que ambas sejam executadas no mesmo loop de eventos. Isso inclui aplicações montadas.

Por exemplo, se duas aplicações usarem este `SessionDep` para o mesmo pool de conexões de banco de dados, juntas poderão ter até cinco sessões abertas por meio dessa dependência.

Se as aplicações usarem pools separados e precisarem de limites independentes, crie um objeto `Depends()` separado para cada aplicação.

### Feche a sessão antes de permitir outra { #close-the-session-before-allowing-another-one }

Neste exemplo, `get_session` usa `yield`. A sessão é contabilizada no limite até que o código de saída termine de fechá-la.

O `scope` da dependência determina quando esse código de saída é executado:

* Com `scope="request"`, o padrão, ele é executado depois que a response é enviada.
* Com `scope="function"`, ele é executado depois que a *função de operação de rota* termina, antes de enviar a response.

Você pode ler mais sobre [saída antecipada e escopo](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

Para uma dependência sem `yield`, a chamada é contabilizada no limite apenas até que a função termine.

Se você usar uma dependência com `yield` em um tratador de WebSocket, ela é contabilizada no limite até que o tratador termine e o código de saída da dependência seja concluído.

/// note | Nota

Reutilizar um [valor de dependência em cache](../tutorial/dependencies/sub-dependencies.md#using-the-same-dependency-multiple-times) não é contabilizado novamente no limite. Se diferentes declarações compartilharem esse valor, apenas a declaração que chama a dependência é contabilizada em seu limite.

///

### Escolha um limite para sua aplicação { #choose-a-limit-for-your-application }

Escolha um limite adequado ao número de conexões de banco de dados disponíveis para essas sessões.

Se outras partes da sua aplicação também usarem essas conexões, deixe espaço para elas também. O FastAPI não sabe o tamanho do seu pool de conexões de banco de dados.

Cada processo de trabalho tem seu próprio limite. Por exemplo, dois processos de trabalho com essa dependência poderiam ter até dez sessões abertas entre eles.

/// note | Detalhes Técnicos

Os limites também são separados para cada loop de eventos. Aplicações executadas em loops de eventos diferentes não compartilham um limite, mesmo que reutilizem o mesmo objeto `Depends()`.

///

### Dependências que precisam de mais de um recurso { #dependencies-that-need-more-than-one-resource }

O FastAPI executa as subdependências de uma dependência antes de aplicar o limite dela.

Então, para limitar sessões de banco de dados, coloque `max_concurrency` em `Depends(get_session, ...)`, onde a sessão é criada.

Um request pode ficar bloqueado se precisar de outra sessão enquanto ainda mantém uma que só será fechada ao final do request.

Por exemplo, imagine um `Depends(get_session, max_concurrency=1, use_cache=False)` compartilhado, usado duas vezes no mesmo request.

A primeira chamada cria uma sessão. A segunda espera que ela seja fechada. Mas a primeira sessão não pode ser fechada até que o request termine, e ele está esperando pela segunda chamada.

Dois requests também podem ficar bloqueados se um mantiver uma sessão enquanto espera por outro recurso, e o outro mantiver esse recurso enquanto espera por uma sessão.

Se seus requests precisarem de vários recursos, adquira-os na mesma ordem. O FastAPI aplica cada limite separadamente, não reserva antecipadamente todos os recursos de que um request precisará.

## Dependências com `yield`, `HTTPException`, `except` e Tarefas em Segundo Plano { #dependencies-with-yield-httpexception-except-and-background-tasks }

/// warning | Atenção

Muito provavelmente você não precisa desses detalhes técnicos.

Esses detalhes são úteis principalmente se você tinha uma aplicação FastAPI anterior à versão 0.121.0 e está enfrentando problemas com dependências com `yield`.

///

Dependências com `yield` evoluíram ao longo do tempo para contemplar diferentes casos de uso e corrigir alguns problemas, aqui está um resumo do que mudou.

### Dependências com `yield` e `scope` { #dependencies-with-yield-and-scope }

Na versão 0.121.0, o FastAPI adicionou suporte a `Depends(scope="function")` para dependências com `yield`.

Usando `Depends(scope="function")`, o código de saída após o `yield` é executado logo depois que a *função de operação de rota* termina, antes de a response ser enviada de volta ao cliente.

E ao usar `Depends(scope="request")` (o padrão), o código de saída após o `yield` é executado depois que a response é enviada.

Você pode ler mais na documentação em [Dependências com `yield` - Saída antecipada e `scope`](../tutorial/dependencies/dependencies-with-yield.md#early-exit-and-scope).

### Dependências com `yield` e `StreamingResponse`, Detalhes Técnicos { #dependencies-with-yield-and-streamingresponse-technical-details }

Antes do FastAPI 0.118.0, se você usasse uma dependência com `yield`, o código de saída rodaria depois que a *função de operação de rota* retornasse, mas logo antes de enviar a resposta.

A intenção era evitar manter recursos por mais tempo que o necessário, esperando a resposta percorrer a rede.

Essa mudança também significava que, se você retornasse um `StreamingResponse`, o código de saída da dependência com `yield` já teria sido executado.

Por exemplo, se você tivesse uma sessão de banco de dados em uma dependência com `yield`, o `StreamingResponse` não conseguiria usar essa sessão enquanto transmite dados, porque a sessão já teria sido fechada no código de saída após o `yield`.

Esse comportamento foi revertido na versão 0.118.0, para que o código de saída após o `yield` seja executado depois que a resposta for enviada.

/// note | Nota

Como você verá abaixo, isso é muito semelhante ao comportamento antes da versão 0.106.0, mas com várias melhorias e correções de bugs para casos extremos.

///

#### Casos de uso com código de saída antecipado { #use-cases-with-early-exit-code }

Há alguns casos de uso, com condições específicas, que poderiam se beneficiar do comportamento antigo de executar o código de saída das dependências com `yield` antes de enviar a resposta.

Por exemplo, imagine que você tem código que usa uma sessão de banco de dados em uma dependência com `yield` apenas para verificar um usuário, mas a sessão de banco de dados nunca é usada novamente na *função de operação de rota*, somente na dependência, **e** a response demora a ser enviada, como um `StreamingResponse` que envia dados lentamente, mas por algum motivo não usa o banco de dados.

Nesse caso, a sessão de banco de dados seria mantida até que a resposta termine de ser enviada, mas se você não a usa, então não seria necessário mantê-la.

Veja como poderia ser:

{* ../../docs_src/dependencies/tutorial013.py *}

O código de saída, o fechamento automático da `Session` em:

{* ../../docs_src/dependencies/tutorial013.py ln[19:21] *}

...seria executado depois que a resposta terminar de enviar os dados lentos:

{* ../../docs_src/dependencies/tutorial013.py ln[30:38] hl[31:33] *}

Mas como `generate_stream()` não usa a sessão do banco de dados, não é realmente necessário manter a sessão aberta enquanto envia a resposta.

Se você tiver esse caso específico usando SQLModel (ou SQLAlchemy), você poderia fechar explicitamente a sessão depois que não precisar mais dela:

{* ../../docs_src/dependencies/tutorial014.py ln[24:28] hl[28] *}

Dessa forma a sessão liberaria a conexão com o banco de dados, para que outras requisições pudessem usá-la.

Se você tiver um caso diferente que precise sair antecipadamente de uma dependência com `yield`, por favor crie uma [Pergunta no GitHub Discussions](https://github.com/fastapi/fastapi/discussions/new?category=questions) com o seu caso específico e por que você se beneficiaria de ter o fechamento antecipado para dependências com `yield`.

Se houver casos de uso convincentes para fechamento antecipado em dependências com `yield`, considerarei adicionar uma nova forma de optar por esse fechamento antecipado.

### Dependências com `yield` e `except`, Detalhes Técnicos { #dependencies-with-yield-and-except-technical-details }

Antes do FastAPI 0.110.0, se você usasse uma dependência com `yield`, e então capturasse uma exceção com `except` nessa dependência, e você não relançasse a exceção, a exceção seria automaticamente levantada/encaminhada para quaisquer tratadores de exceção ou para o tratador de erro interno do servidor.

Isso foi alterado na versão 0.110.0 para corrigir consumo de memória não tratado decorrente de exceções encaminhadas sem um tratador (erros internos do servidor), e para torná-lo consistente com o comportamento do código Python regular.

### Tarefas em Segundo Plano e Dependências com `yield`, Detalhes Técnicos { #background-tasks-and-dependencies-with-yield-technical-details }

Antes do FastAPI 0.106.0, lançar exceções após o `yield` não era possível, o código de saída em dependências com `yield` era executado *depois* que a resposta era enviada, então [Tratadores de Exceções](../tutorial/handling-errors.md#install-custom-exception-handlers) já teriam sido executados.

Isso foi projetado assim principalmente para permitir o uso dos mesmos objetos "yielded" por dependências dentro de tarefas em segundo plano, porque o código de saída seria executado depois que as tarefas em segundo plano fossem concluídas.

Isso foi alterado no FastAPI 0.106.0 com a intenção de não manter recursos enquanto se espera a response percorrer a rede.

/// tip | Dica

Além disso, uma tarefa em segundo plano normalmente é um conjunto de lógica independente que deve ser tratado separadamente, com seus próprios recursos (por exemplo, sua própria conexão de banco de dados).

Assim, desta forma você provavelmente terá um código mais limpo.

///

Se você costumava depender desse comportamento, agora você deveria criar os recursos para tarefas em segundo plano dentro da própria tarefa em segundo plano, e usar internamente apenas dados que não dependam dos recursos de dependências com `yield`.

Por exemplo, em vez de usar a mesma sessão de banco de dados, você criaria uma nova sessão de banco de dados dentro da tarefa em segundo plano, e obteria os objetos do banco de dados usando essa nova sessão. E então, em vez de passar o objeto do banco de dados como parâmetro para a função da tarefa em segundo plano, você passaria o ID desse objeto e então obteria o objeto novamente dentro da função da tarefa em segundo plano.
