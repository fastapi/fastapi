# Webhooks OpenAPI { #openapi-webhooks }

Existem situações onde você deseja informar os **usuários** da sua API que a sua aplicação pode chamar a aplicação *deles* (enviando uma requisição) com alguns dados, normalmente para **notificar** algum tipo de **evento**.

Isso significa que no lugar do processo normal de seus usuários enviarem requisições para a sua API, é a **sua API** (ou sua aplicação) que poderia **enviar requisições para o sistema deles** (para a API deles, a aplicação deles).

Isso normalmente é chamado de **webhook**.

## Etapas dos webhooks { #webhooks-steps }

Normalmente, o processo é que **você define** em seu código qual é a mensagem que você irá mandar, o **corpo da sua requisição**.

Você também define de alguma maneira em quais **momentos** a sua aplicação mandará essas requisições ou eventos.

E os **seus usuários** definem de alguma forma (em algum painel por exemplo) a **URL** que a sua aplicação deve enviar essas requisições.

Toda a **lógica** sobre como cadastrar as URLs para os webhooks e o código para enviar de fato as requisições cabe a você definir. Você escreve da maneira que você desejar no **seu próprio código**.

## Documentando webhooks com o FastAPI e OpenAPI { #documenting-webhooks-with-fastapi-and-openapi }

Com o **FastAPI**, utilizando o OpenAPI, você pode definir os nomes destes webhooks, os tipos das operações HTTP que a sua aplicação pode enviar (e.g. `POST`, `PUT`, etc.) e os **corpos** da requisição que a sua aplicação enviaria.

Isto pode facilitar bastante para os seus usuários **implementarem as APIs deles** para receber as requisições dos seus **webhooks**, eles podem inclusive ser capazes de gerar parte do código da API deles.

/// info | Informação

Webhooks estão disponíveis a partir do OpenAPI 3.1.0, e possui suporte do FastAPI a partir da versão `0.99.0`.

///

## Uma aplicação com webhooks { #an-app-with-webhooks }

Quando você cria uma aplicação com o **FastAPI**, existe um atributo chamado `webhooks`, que você utilizar para defini-los da mesma maneira que você definiria as suas **operações de rotas**, utilizando por exemplo `@app.webhooks.post()`.

{* ../../docs_src/openapi_webhooks/tutorial001.py hl[9:13,36:53] *}

Os webhooks que você define aparecerão no esquema do **OpenAPI** e na **página de documentação** gerada automaticamente.

/// info | Informação

O objeto `app.webhooks` é na verdade apenas um `APIRouter`, o mesmo tipo que você utilizaria ao estruturar a sua aplicação com diversos arquivos.

///

Note que utilizando webhooks você não está de fato declarando um *path* (como `/items/`), o texto que informa é apenas um **identificador** do webhook (o nome do evento), por exemplo em `@app.webhooks.post("new-subscription")`, o nome do webhook é `new-subscription`.

Isto porque espera-se que os **seus usuários** definam o verdadeiro **URL path** onde eles desejam receber a requisição do webhook de algum outra maneira. (e.g. um painel).

### Confira a documentação { #check-the-docs }

Agora você pode iniciar a sua aplicação e ir até <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá que a sua documentação possui as *operações de rota* normais e agora também possui alguns **webhooks**:

<img src="/img/tutorial/openapi-webhooks/image01.png">
