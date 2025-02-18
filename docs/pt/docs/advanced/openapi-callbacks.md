# Callbacks na OpenAPI

Você poderia criar uma API com uma *operação de rota* que poderia acionar uma solicitação a uma *API externa* criada por outra pessoa (provavelmente o mesmo desenvolvedor que estaria *usando* sua API).

O processo que acontece quando seu aplicativo de API chama a *API externa* é chamado de "callback". Porque o software que o desenvolvedor externo escreveu envia uma solicitação para sua API e então sua API *chama de volta*, enviando uma solicitação para uma *API externa* (que provavelmente foi criada pelo mesmo desenvolvedor).

Nesse caso, você poderia querer documentar como essa API externa *deveria* ser. Que *operação de rota* ela deveria ter, que corpo ela deveria esperar, que resposta ela deveria retornar, etc.

## Um aplicativo com callbacks

Vamos ver tudo isso com um exemplo.

Imagine que você tem um aplicativo que permite criar faturas.

Essas faturas terão um `id`, `title` (opcional), `customer` e `total`.

O usuário da sua API (um desenvolvedor externo) criará uma fatura em sua API com uma solicitação POST.

Então sua API irá (vamos imaginar):

* Enviar uma solicitação de pagamento para o desenvolvedor externo.
* Coletar o dinheiro.
* Enviar a notificação de volta para o usuário da API (o desenvolvedor externo).
* Isso será feito enviando uma solicitação POST (de *sua API*) para alguma *API externa* fornecida por esse desenvolvedor externo (este é o "callback").

## O aplicativo **FastAPI** normal

Vamos primeiro ver como o aplicativo da API normal se pareceria antes de adicionar o callback.

Ele terá uma *operação de rota* que receberá um corpo `Invoice`, e um parâmetro de consulta `callback_url` que conterá a URL para o callback.

Essa parte é bastante normal, a maior parte do código provavelmente já é familiar para você:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[9:13,36:53] *}

/// tip | Dica

O parâmetro de consulta `callback_url` usa um tipo Pydantic <a href="https://docs.pydantic.dev/latest/api/networks/" class="external-link" target="_blank">Url</a>.

///

A única coisa nova é o argumento `callbacks=invoices_callback_router.routes` no decorador da *operação de rota*. Veremos o que é isso a seguir.

## Documentando o callback

O código real do callback dependerá muito do seu próprio aplicativo de API.

E provavelmente variará muito de um aplicativo para o outro.

Poderia ser apenas uma ou duas linhas de código, como:

```Python
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

Mas possivelmente a parte mais importante do callback é garantir que o usuário da sua API (o desenvolvedor externo) implemente a *API externa* corretamente, de acordo com os dados que *sua API* vai enviar no corpo da solicitação do callback, etc.

Então, o que faremos a seguir é adicionar o código para documentar como essa *API externa* deve ser para receber o callback de *sua API*.

A documentação aparecerá na interface do Swagger em `/docs` em sua API, e permitirá que os desenvolvedores externos saibam como construir a *API externa*.

Esse exemplo não implementa o callback em si (que poderia ser apenas uma linha de código), apenas a parte da documentação.

/// tip | Dica

O callback real é apenas uma solicitação HTTP.

Quando implementando o callback por você mesmo, você pode usar algo como <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a> ou <a href="https://requests.readthedocs.io/" class="external-link" target="_blank">Requisições</a>.

///

## Escrevendo o código de documentação do callback

Esse código não será executado em seu aplicativo, nós só precisamos dele para *documentar* como essa *API externa* deveria ser.

Mas, você já sabe como criar facilmente documentação automática para uma API com o **FastAPI**.

Então vamos usar esse mesmo conhecimento para documentar como a *API externa* deveria ser... criando as *operações de rota* que a *API externa* deveria implementar (as que sua API irá chamar).

/// tip | Dica

Quando escrever o código para documentar um callback, pode ser útil imaginar que você é aquele *desenvolvedor externo*. E que você está atualmente implementando a *API externa*, não *sua API*.

Adotar temporariamente esse ponto de vista (do *desenvolvedor externo*) pode ajudar a sentir que é mais óbvio onde colocar os parâmetros, o modelo Pydantic para o corpo, para a resposta, etc. para essa *API externa*.

///

### Criar um `APIRouter` para o callback

Primeiramente crie um novo `APIRouter` que conterá um ou mais callbacks.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[3,25] *}

### Crie a *operação de rota* do callback

Para criar a *operação de rota* do callback, use o mesmo `APIRouter` que você criou acima.

Ele deve parecer exatamente como uma *operação de rota* normal do FastAPI:

* Ele provavelmente deveria ter uma declaração do corpo que deveria receber, por exemplo. `body: InvoiceEvent`.
* E também deveria ter uma declaração de um código de status de resposta, por exemplo. `response_model=InvoiceEventReceived`.

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[16:18,21:22,28:32] *}

Há 2 diferenças principais de uma *operação de rota* normal:

* Ela não necessita ter nenhum código real, porque seu aplicativo nunca chamará esse código. Ele é usado apenas para documentar a *API externa*. Então, a função poderia ter apenas `pass`.
* A *rota* pode conter uma <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expressão OpenAPI 3</a> (veja mais abaixo) onde pode usar variáveis com parâmetros e partes da solicitação original enviada para *sua API*.

### A expressão do caminho do callback

A *rota* do callback pode ter uma <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#key-expression" class="external-link" target="_blank">expressão OpenAPI 3</a> que pode conter partes da solicitação original enviada para *sua API*.

Nesse caso, é a `str`:

```Python
"{$callback_url}/invoices/{$request.body.id}"
```

Então, se o usuário da sua API (o desenvolvedor externo) enviar uma solicitação para *sua API* para:

```
https://yourapi.com/invoices/?callback_url=https://www.external.org/events
```

com um corpo JSON de:

```JSON
{
    "id": "2expen51ve",
    "customer": "Mr. Richie Rich",
    "total": "9999"
}
```

então *sua API* processará a fatura e, em algum momento posterior, enviará uma solicitação de callback para o `callback_url` (a *API externa*):

```
https://www.external.org/events/invoices/2expen51ve
```

com um corpo JSON contendo algo como:

```JSON
{
    "description": "Payment celebration",
    "paid": true
}
```

e esperaria uma resposta daquela *API externa* com um corpo JSON como:

```JSON
{
    "ok": true
}
```

/// tip | Dica

Perceba como a URL de callback usada contém a URL recebida como um parâmetro de consulta em `callback_url` (`https://www.external.org/events`) e também o `id` da fatura de dentro do corpo JSON (`2expen51ve`).

///

### Adicionar o roteador de callback

Nesse ponto você tem a(s) *operação de rota de callback* necessária(s) (a(s) que o *desenvolvedor externo* deveria implementar na *API externa*) no roteador de callback que você criou acima.

Agora use o parâmetro `callbacks` no decorador da *operação de rota de sua API* para passar o atributo `.routes` (que é na verdade apenas uma `list` de rotas/*operações de rota*) do roteador de callback que você criou acima:

{* ../../docs_src/openapi_callbacks/tutorial001.py hl[35] *}

/// tip | Dica

Perceba que você não está passando o roteador em si (`invoices_callback_router`) para `callback=`, mas o atributo `.routes`, como em `invoices_callback_router.routes`.

///

### Verifique a documentação

Agora você pode iniciar seu aplicativo e ir para <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá sua documentação incluindo uma seção "Callbacks" para sua *operação de rota* que mostra como a *API externa* deveria ser:

<img src="/img/tutorial/openapi-callbacks/image01.png">
