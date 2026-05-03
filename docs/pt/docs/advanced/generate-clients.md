# Gerando SDKs { #generating-sdks }

Como o **FastAPI** é baseado na especificação **OpenAPI**, suas APIs podem ser descritas em um formato padrão que muitas ferramentas entendem.

Isso facilita gerar **documentação** atualizada, bibliotecas clientes (<abbr title="Software Development Kits - Kits de Desenvolvimento de Software">**SDKs**</abbr>) em várias linguagens e **testes** ou **fluxos de trabalho de automação** que permanecem em sincronia com o seu código.

Neste guia, você aprenderá como gerar um **SDK em TypeScript** para o seu backend FastAPI.

## Geradores de SDK de código aberto { #open-source-sdk-generators }

Uma opção versátil é o [OpenAPI Generator](https://openapi-generator.tech/), que suporta **muitas linguagens de programação** e pode gerar SDKs a partir da sua especificação OpenAPI.

Para **clientes TypeScript**, o [Hey API](https://heyapi.dev/) é uma solução feita sob medida, oferecendo uma experiência otimizada para o ecossistema TypeScript.

Você pode descobrir mais geradores de SDK em [OpenAPI.Tools](https://openapi.tools/#sdk).

/// tip | Dica

O FastAPI gera automaticamente especificações **OpenAPI 3.1**, então qualquer ferramenta que você usar deve suportar essa versão.

///

## Geradores de SDK dos patrocinadores do FastAPI { #sdk-generators-from-fastapi-sponsors }

Esta seção destaca soluções **financiadas por investimento** e **com suporte de empresas** que patrocinam o FastAPI. Esses produtos fornecem **funcionalidades adicionais** e **integrações** além de SDKs gerados com alta qualidade.

Ao ✨ [**patrocinar o FastAPI**](../help-fastapi.md#sponsor-the-author) ✨, essas empresas ajudam a garantir que o framework e seu **ecossistema** continuem saudáveis e **sustentáveis**.

O patrocínio também demonstra um forte compromisso com a **comunidade** FastAPI (você), mostrando que elas se importam não apenas em oferecer um **ótimo serviço**, mas também em apoiar um **framework robusto e próspero**, o FastAPI. 🙇

Por exemplo, você pode querer experimentar:

* [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
* [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
* [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

Algumas dessas soluções também podem ser open source ou oferecer planos gratuitos, para que você possa testá-las sem compromisso financeiro. Outros geradores comerciais de SDK estão disponíveis e podem ser encontrados online. 🤓

## Crie um SDK em TypeScript { #create-a-typescript-sdk }

Vamos começar com uma aplicação FastAPI simples:

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

Note que as *operações de rota* definem os modelos que usam para o corpo da requisição e o corpo da resposta, usando os modelos `Item` e `ResponseMessage`.

### Documentação da API { #api-docs }

Se você for para `/docs`, verá que ela tem os **schemas** para os dados a serem enviados nas requisições e recebidos nas respostas:

<img src="/img/tutorial/generate-clients/image01.png">

Você pode ver esses schemas porque eles foram declarados com os modelos no app.

Essas informações estão disponíveis no **schema OpenAPI** do app e são mostradas na documentação da API.

E essas mesmas informações dos modelos que estão incluídas no OpenAPI são o que pode ser usado para **gerar o código do cliente**.

### Hey API { #hey-api }

Depois que tivermos uma aplicação FastAPI com os modelos, podemos usar o Hey API para gerar um cliente TypeScript. A forma mais rápida é via npx.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Isso gerará um SDK TypeScript em `./src/client`.

Você pode aprender como [instalar `@hey-api/openapi-ts`](https://heyapi.dev/openapi-ts/get-started) e ler sobre o [resultado gerado](https://heyapi.dev/openapi-ts/output) no site deles.

### Usando o SDK { #using-the-sdk }

Agora você pode importar e usar o código do cliente. Poderia ser assim, observe que você obtém preenchimento automático para os métodos:

<img src="/img/tutorial/generate-clients/image02.png">

Você também obterá preenchimento automático para o corpo a ser enviado:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | Dica

Observe o preenchimento automático para `name` e `price`, que foi definido na aplicação FastAPI, no modelo `Item`.

///

Você terá erros em linha para os dados que você envia:

<img src="/img/tutorial/generate-clients/image04.png">

O objeto de resposta também terá preenchimento automático:

<img src="/img/tutorial/generate-clients/image05.png">

## Aplicação FastAPI com Tags { #fastapi-app-with-tags }

Em muitos casos, sua aplicação FastAPI será maior, e você provavelmente usará tags para separar diferentes grupos de *operações de rota*.

Por exemplo, você poderia ter uma seção para **items** e outra seção para **users**, e elas poderiam ser separadas por tags:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Gere um cliente TypeScript com Tags { #generate-a-typescript-client-with-tags }

Se você gerar um cliente para uma aplicação FastAPI usando tags, normalmente também separará o código do cliente com base nas tags.

Dessa forma, você poderá ter as coisas ordenadas e agrupadas corretamente para o código do cliente:

<img src="/img/tutorial/generate-clients/image06.png">

Nesse caso você tem:

* `ItemsService`
* `UsersService`

### Nomes dos métodos do cliente { #client-method-names }

Agora os nomes dos métodos gerados como `createItemItemsPost` não parecem muito “limpos”:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...isso ocorre porque o gerador de clientes usa o **ID de operação** interno do OpenAPI para cada *operação de rota*.

O OpenAPI exige que cada ID de operação seja único em todas as *operações de rota*, então o FastAPI usa o **nome da função**, o **path** e o **método/operação HTTP** para gerar esse ID de operação, porque dessa forma ele pode garantir que os IDs de operação sejam únicos.

Mas eu vou te mostrar como melhorar isso a seguir. 🤓

## IDs de operação personalizados e nomes de métodos melhores { #custom-operation-ids-and-better-method-names }

Você pode **modificar** a maneira como esses IDs de operação são **gerados** para torná-los mais simples e ter **nomes de método mais simples** nos clientes.

Neste caso, você terá que garantir que cada ID de operação seja **único** de alguma outra maneira.

Por exemplo, você poderia garantir que cada *operação de rota* tenha uma tag, e então gerar o ID de operação com base na **tag** e no **nome** da *operação de rota* (o nome da função).

### Função personalizada para gerar IDs exclusivos { #custom-generate-unique-id-function }

O FastAPI usa um **ID exclusivo** para cada *operação de rota*, ele é usado para o **ID de operação** e também para os nomes de quaisquer modelos personalizados necessários, para requisições ou respostas.

Você pode personalizar essa função. Ela recebe uma `APIRoute` e retorna uma string.

Por exemplo, aqui está usando a primeira tag (Você provavelmente terá apenas uma tag) e o nome da *operação de rota* (o nome da função).

Você pode então passar essa função personalizada para o **FastAPI** como o parâmetro `generate_unique_id_function`:

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### Gere um cliente TypeScript com IDs de operação personalizados { #generate-a-typescript-client-with-custom-operation-ids }

Agora, se você gerar o cliente novamente, verá que ele tem os nomes dos métodos melhorados:

<img src="/img/tutorial/generate-clients/image07.png">

Como você pode ver, os nomes dos métodos agora têm a tag e, em seguida, o nome da função. Agora eles não incluem informações do path da URL e da operação HTTP.

### Pré-processar a especificação OpenAPI para o gerador de clientes { #preprocess-the-openapi-specification-for-the-client-generator }

O código gerado ainda tem algumas **informações duplicadas**.

Nós já sabemos que esse método está relacionado aos **items** porque essa palavra está no `ItemsService` (retirada da tag), mas ainda temos o nome da tag prefixado no nome do método também. 😕

Provavelmente ainda queremos mantê-lo para o OpenAPI em geral, pois isso garantirá que os IDs de operação sejam **únicos**.

Mas para o cliente gerado, poderíamos **modificar** os IDs de operação do OpenAPI logo antes de gerar os clientes, apenas para tornar esses nomes de método mais agradáveis e **limpos**.

Poderíamos baixar o JSON do OpenAPI para um arquivo `openapi.json` e então poderíamos **remover essa tag prefixada** com um script como este:

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Com isso, os IDs de operação seriam renomeados de coisas como `items-get_items` para apenas `get_items`, dessa forma o gerador de clientes pode gerar nomes de métodos mais simples.

### Gere um cliente TypeScript com o OpenAPI pré-processado { #generate-a-typescript-client-with-the-preprocessed-openapi }

Como o resultado final está agora em um arquivo `openapi.json`, você precisa atualizar o local de entrada:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

Depois de gerar o novo cliente, você terá agora **nomes de métodos “limpos”**, com todo o **preenchimento automático**, **erros em linha**, etc:

<img src="/img/tutorial/generate-clients/image08.png">

## Benefícios { #benefits }

Ao usar os clientes gerados automaticamente, você terá **preenchimento automático** para:

* Métodos.
* Corpos de requisições, parâmetros de query, etc.
* Corpos de respostas.

Você também terá **erros em linha** para tudo.

E sempre que você atualizar o código do backend e **regenerar** o frontend, ele terá quaisquer novas *operações de rota* disponíveis como métodos, as antigas removidas, e qualquer outra alteração será refletida no código gerado. 🤓

Isso também significa que, se algo mudou, será **refletido** no código do cliente automaticamente. E se você **construir** o cliente, ele falhará caso haja qualquer **incompatibilidade** nos dados usados.

Assim, você **detectará muitos erros** muito cedo no ciclo de desenvolvimento, em vez de ter que esperar que os erros apareçam para seus usuários finais em produção e então tentar depurar onde está o problema. ✨
