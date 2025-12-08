# Tarefas em segundo plano { #background-tasks }

Você pode definir tarefas em segundo plano para serem executadas *após* retornar uma resposta.

Isso é útil para operações que precisam acontecer após uma request, mas que o cliente não precisa realmente esperar a operação terminar antes de receber a resposta.

Isso inclui, por exemplo:

* Notificações por e-mail enviadas após realizar uma ação:
    * Como conectar-se a um servidor de e-mail e enviar um e-mail tende a ser “lento” (vários segundos), você pode retornar a resposta imediatamente e enviar a notificação por e-mail em segundo plano.
* Processamento de dados:
    * Por exemplo, digamos que você receba um arquivo que precisa passar por um processo lento; você pode retornar uma resposta “Accepted” (HTTP 202) e processar o arquivo em segundo plano.

## Usando `BackgroundTasks` { #using-backgroundtasks }

Primeiro, importe `BackgroundTasks` e defina um parâmetro na sua *função de operação de rota* com uma declaração de tipo `BackgroundTasks`:

{* ../../docs_src/background_tasks/tutorial001.py hl[1,13] *}

O **FastAPI** criará o objeto do tipo `BackgroundTasks` para você e o passará como esse parâmetro.

## Crie uma função de tarefa { #create-a-task-function }

Crie uma função para ser executada como a tarefa em segundo plano.

É apenas uma função padrão que pode receber parâmetros.

Pode ser uma função `async def` ou um `def` normal, o **FastAPI** saberá como lidar com isso corretamente.

Neste caso, a função da tarefa escreverá em um arquivo (simulando o envio de um e-mail).

E como a operação de escrita não usa `async` e `await`, definimos a função com um `def` normal:

{* ../../docs_src/background_tasks/tutorial001.py hl[6:9] *}

## Adicione a tarefa em segundo plano { #add-the-background-task }

Dentro da sua *função de operação de rota*, passe sua função de tarefa para o objeto de *tarefas em segundo plano* com o método `.add_task()`:

{* ../../docs_src/background_tasks/tutorial001.py hl[14] *}

O `.add_task()` recebe como argumentos:

* Uma função de tarefa a ser executada em segundo plano (`write_notification`).
* Qualquer sequência de argumentos que deve ser passada para a função de tarefa na ordem (`email`).
* Quaisquer argumentos nomeados que devem ser passados para a função de tarefa (`message="some notification"`).

## Injeção de dependências { #dependency-injection }

Usar `BackgroundTasks` também funciona com o sistema de injeção de dependências; você pode declarar um parâmetro do tipo `BackgroundTasks` em vários níveis: em uma *função de operação de rota*, em uma dependência (dependable), em uma subdependência, etc.

O **FastAPI** sabe o que fazer em cada caso e como reutilizar o mesmo objeto, de forma que todas as tarefas em segundo plano sejam combinadas e executadas em segundo plano depois:


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

Neste exemplo, as mensagens serão escritas no arquivo `log.txt` *após* o envio da resposta.

Se houver uma query na request, ela será registrada em uma tarefa em segundo plano.

E então outra tarefa em segundo plano gerada na *função de operação de rota* escreverá uma mensagem usando o parâmetro de path `email`.

## Detalhes técnicos { #technical-details }

A classe `BackgroundTasks` vem diretamente de <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">`starlette.background`</a>.

Ela é importada/incluída diretamente no FastAPI para que você possa importá-la de `fastapi` e evitar importar acidentalmente a alternativa `BackgroundTask` (sem o `s` no final) de `starlette.background`.

Usando apenas `BackgroundTasks` (e não `BackgroundTask`), é possível usá-la como um parâmetro de *função de operação de rota* e deixar o **FastAPI** cuidar do resto para você, assim como ao usar o objeto `Request` diretamente.

Ainda é possível usar `BackgroundTask` sozinho no FastAPI, mas você precisa criar o objeto no seu código e retornar uma `Response` da Starlette incluindo-o.

Você pode ver mais detalhes na <a href="https://www.starlette.dev/background/" class="external-link" target="_blank">documentação oficial da Starlette para tarefas em segundo plano</a>.

## Ressalva { #caveat }

Se você precisar realizar computação pesada em segundo plano e não necessariamente precisar que seja executada pelo mesmo processo (por exemplo, você não precisa compartilhar memória, variáveis, etc.), pode se beneficiar do uso de outras ferramentas maiores, como o <a href="https://docs.celeryq.dev" class="external-link" target="_blank">Celery</a>.

Elas tendem a exigir configurações mais complexas, um gerenciador de fila de mensagens/tarefas, como RabbitMQ ou Redis, mas permitem executar tarefas em segundo plano em vários processos e, especialmente, em vários servidores.

Mas se você precisa acessar variáveis e objetos da mesma aplicação **FastAPI**, ou precisa realizar pequenas tarefas em segundo plano (como enviar uma notificação por e-mail), você pode simplesmente usar `BackgroundTasks`.

## Recapitulando { #recap }

Importe e use `BackgroundTasks` com parâmetros em *funções de operação de rota* e dependências para adicionar tarefas em segundo plano.
