# Alternativas, Inspiração e Comparações { #alternatives-inspiration-and-comparisons }

O que inspirou o **FastAPI**, como ele se compara às alternativas e o que ele aprendeu com elas.

## Introdução { #intro }

**FastAPI** não existiria se não fosse pelo trabalho anterior de outras pessoas.

Houve muitas ferramentas criadas antes que ajudaram a inspirar sua criação.

Tenho evitado criar um novo framework por vários anos. Primeiro tentei resolver todas as funcionalidades cobertas pelo **FastAPI** utilizando muitos frameworks, plug-ins e ferramentas diferentes.

Mas em algum momento, não havia outra opção senão criar algo que fornecesse todos esses recursos, pegando as melhores ideias de ferramentas anteriores e combinando-as da melhor maneira possível, usando funcionalidades da linguagem que nem sequer estavam disponíveis antes (anotações de tipo no Python 3.6+).

## Ferramentas anteriores { #previous-tools }

### <a href="https://www.djangoproject.com/" class="external-link" target="_blank">Django</a> { #django }

É o framework Python mais popular e amplamente confiável. É utilizado para construir sistemas como o Instagram.

É relativamente bem acoplado com bancos de dados relacionais (como MySQL ou PostgreSQL), então, ter um banco de dados NoSQL (como Couchbase, MongoDB, Cassandra, etc.) como mecanismo principal de armazenamento não é muito fácil.

Foi criado para gerar o HTML no backend, não para criar APIs usadas por um frontend moderno (como React, Vue.js e Angular) ou por outros sistemas (como dispositivos <abbr title="Internet of Things – Internet das Coisas">IoT</abbr>) comunicando com ele.

### <a href="https://www.django-rest-framework.org/" class="external-link" target="_blank">Django REST Framework</a> { #django-rest-framework }

Django REST framework foi criado para ser uma caixa de ferramentas flexível para construção de APIs Web utilizando Django por baixo, para melhorar suas capacidades de API.

Ele é utilizado por muitas empresas incluindo Mozilla, Red Hat e Eventbrite.

Foi um dos primeiros exemplos de **documentação automática de API**, e essa foi especificamente uma das primeiras ideias que inspirou "a busca por" **FastAPI**.

/// note | Nota

Django REST Framework foi criado por Tom Christie. O mesmo criador de Starlette e Uvicorn, nos quais **FastAPI** é baseado.

///

/// check | **FastAPI** inspirado para

Ter uma interface web de documentação automática da API.

///

### <a href="https://flask.palletsprojects.com" class="external-link" target="_blank">Flask</a> { #flask }

Flask é um "microframework", não inclui integrações com banco de dados nem muitas das coisas que vêm por padrão no Django.

Essa simplicidade e flexibilidade permitem fazer coisas como utilizar bancos de dados NoSQL como o principal sistema de armazenamento de dados.

Por ser muito simples, é relativamente intuitivo de aprender, embora a documentação se torne um pouco técnica em alguns pontos.

Ele também é comumente utilizado por outras aplicações que não necessariamente precisam de banco de dados, gerenciamento de usuários, ou qualquer uma das muitas funcionalidades que já vêm prontas no Django. Embora muitas dessas funcionalidades possam ser adicionadas com plug-ins.

Esse desacoplamento de partes, e ser um "microframework" que pode ser estendido para cobrir exatamente o que é necessário era uma funcionalidade chave que eu queria manter.

Dada a simplicidade do Flask, ele parecia uma boa opção para construção de APIs. A próxima coisa a encontrar era um "Django REST Framework" para Flask.

/// check | **FastAPI** inspirado para

Ser um microframework. Tornar fácil misturar e combinar as ferramentas e partes necessárias.

Ter um sistema de roteamento simples e fácil de usar.

///

### <a href="https://requests.readthedocs.io" class="external-link" target="_blank">Requests</a> { #requests }

**FastAPI** na verdade não é uma alternativa ao **Requests**. O escopo deles é muito diferente.

Na verdade, é comum utilizar Requests dentro de uma aplicação FastAPI.

Ainda assim, o FastAPI tirou bastante inspiração do Requests.

**Requests** é uma biblioteca para interagir com APIs (como um cliente), enquanto **FastAPI** é uma biblioteca para construir APIs (como um servidor).

Eles estão, mais ou menos, em pontas opostas, complementando-se.

Requests tem um design muito simples e intuitivo, é muito fácil de usar, com padrões sensatos. Mas ao mesmo tempo, é muito poderoso e personalizável.

É por isso que, como dito no site oficial:

> Requests é um dos pacotes Python mais baixados de todos os tempos

O jeito de usar é muito simples. Por exemplo, para fazer uma requisição `GET`, você escreveria:

```Python
response = requests.get("http://example.com/some/url")
```

A contra-parte na aplicação FastAPI, a operação de rota, poderia ficar assim:

```Python hl_lines="1"
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

Veja as similaridades em `requests.get(...)` e `@app.get(...)`.

/// check | **FastAPI** inspirado para

* Ter uma API simples e intuitiva.
* Utilizar nomes de métodos HTTP (operações) diretamente, de um jeito direto e intuitivo.
* Ter padrões sensatos, mas customizações poderosas.

///

### <a href="https://swagger.io/" class="external-link" target="_blank">Swagger</a> / <a href="https://github.com/OAI/OpenAPI-Specification/" class="external-link" target="_blank">OpenAPI</a> { #swagger-openapi }

A principal funcionalidade que eu queria do Django REST Framework era a documentação automática da API.

Então descobri que existia um padrão para documentar APIs, utilizando JSON (ou YAML, uma extensão do JSON) chamado Swagger.

E havia uma interface web para APIs Swagger já criada. Então, ser capaz de gerar documentação Swagger para uma API permitiria usar essa interface web automaticamente.

Em algum ponto, Swagger foi doado para a Fundação Linux, para ser renomeado OpenAPI.

É por isso que ao falar sobre a versão 2.0 é comum dizer "Swagger", e para a versão 3+ "OpenAPI".

/// check | **FastAPI** inspirado para

Adotar e usar um padrão aberto para especificações de API, em vez de um schema personalizado.

E integrar ferramentas de interface para usuários baseadas nos padrões:

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>
* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>

Essas duas foram escolhidas por serem bem populares e estáveis, mas fazendo uma pesquisa rápida, você pode encontrar dúzias de interfaces alternativas adicionais para OpenAPI (que você pode utilizar com **FastAPI**).

///

### Flask REST frameworks { #flask-rest-frameworks }

Existem vários Flask REST frameworks, mas depois de investir tempo e trabalho investigando-os, descobri que muitos estão descontinuados ou abandonados, com diversas questões em aberto que os tornaram inadequados.

### <a href="https://marshmallow.readthedocs.io/en/stable/" class="external-link" target="_blank">Marshmallow</a> { #marshmallow }

Uma das principais funcionalidades necessárias em sistemas de API é a "<abbr title="também chamado marshalling, conversão">serialização</abbr>" de dados, que é pegar dados do código (Python) e convertê-los em algo que possa ser enviado pela rede. Por exemplo, converter um objeto contendo dados de um banco de dados em um objeto JSON. Converter objetos `datetime` em strings, etc.

Outra grande funcionalidade necessária pelas APIs é a validação de dados, garantindo que os dados são válidos, dados certos parâmetros. Por exemplo, que algum campo seja `int`, e não alguma string aleatória. Isso é especialmente útil para dados de entrada.

Sem um sistema de validação de dados, você teria que realizar todas as verificações manualmente, no código.

Essas funcionalidades são o que o Marshmallow foi construído para fornecer. É uma ótima biblioteca, e eu a utilizei bastante antes.

Mas ele foi criado antes de existirem as anotações de tipo do Python. Então, para definir cada <abbr title="a definição de como os dados devem ser formados">schema</abbr> você precisa utilizar utilitários e classes específicos fornecidos pelo Marshmallow.

/// check | **FastAPI** inspirado para

Usar código para definir "schemas" que forneçam, automaticamente, tipos de dados e validação.

///

### <a href="https://webargs.readthedocs.io/en/latest/" class="external-link" target="_blank">Webargs</a> { #webargs }

Outra grande funcionalidade requerida pelas APIs é o <abbr title="ler e converter para dados Python">parsing</abbr> de dados vindos de requisições de entrada.

Webargs é uma ferramenta feita para fornecer isso no topo de vários frameworks, inclusive Flask.

Ele utiliza Marshmallow por baixo para a validação de dados. E foi criado pelos mesmos desenvolvedores.

É uma grande ferramenta e eu também a utilizei bastante, antes de ter o **FastAPI**.

/// info | Informação

Webargs foi criado pelos mesmos desenvolvedores do Marshmallow.

///

/// check | **FastAPI** inspirado para

Ter validação automática dos dados de requisições de entrada.

///

### <a href="https://apispec.readthedocs.io/en/stable/" class="external-link" target="_blank">APISpec</a> { #apispec }

Marshmallow e Webargs fornecem validação, parsing e serialização como plug-ins.

Mas a documentação ainda estava faltando. Então APISpec foi criado.

É um plug-in para muitos frameworks (e há um plug-in para Starlette também).

O jeito como ele funciona é que você escreve a definição do schema usando formato YAML dentro da docstring de cada função que lida com uma rota.

E ele gera schemas OpenAPI.

É assim como funciona no Flask, Starlette, Responder, etc.

Mas então, temos novamente o problema de ter uma micro-sintaxe, dentro de uma string Python (um grande YAML).

O editor não pode ajudar muito com isso. E se modificarmos parâmetros ou schemas do Marshmallow e esquecermos de também modificar aquela docstring em YAML, o schema gerado ficaria obsoleto.

/// info | Informação

APISpec foi criado pelos mesmos desenvolvedores do Marshmallow.

///

/// check | **FastAPI** inspirado para

Dar suporte ao padrão aberto para APIs, OpenAPI.

///

### <a href="https://flask-apispec.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-apispec</a> { #flask-apispec }

É um plug-in Flask, que amarra juntos Webargs, Marshmallow e APISpec.

Ele utiliza a informação do Webargs e Marshmallow para gerar automaticamente schemas OpenAPI, usando APISpec.

É uma grande ferramenta, muito subestimada. Deveria ser bem mais popular do que muitos plug-ins Flask por aí. Pode ser devido à sua documentação ser concisa e abstrata demais.

Isso resolveu ter que escrever YAML (outra sintaxe) dentro das docstrings do Python.

Essa combinação de Flask, Flask-apispec com Marshmallow e Webargs foi a minha stack de backend favorita até construir o **FastAPI**.

Usá-la levou à criação de vários geradores Flask full-stack. Estas são as principais stacks que eu (e várias equipes externas) tenho utilizado até agora:

* <a href="https://github.com/tiangolo/full-stack" class="external-link" target="_blank">https://github.com/tiangolo/full-stack</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchbase" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchbase</a>
* <a href="https://github.com/tiangolo/full-stack-flask-couchdb" class="external-link" target="_blank">https://github.com/tiangolo/full-stack-flask-couchdb</a>

E esses mesmos geradores full-stack foram a base dos [Geradores de Projetos **FastAPI**](project-generation.md){.internal-link target=_blank}.

/// info | Informação

Flask-apispec foi criado pelos mesmos desenvolvedores do Marshmallow.

///

/// check | **FastAPI** inspirado para

Gerar o schema OpenAPI automaticamente, a partir do mesmo código que define serialização e validação.

///

### <a href="https://nestjs.com/" class="external-link" target="_blank">NestJS</a> (e <a href="https://angular.io/" class="external-link" target="_blank">Angular</a>) { #nestjs-and-angular }

Isso nem é Python, NestJS é um framework NodeJS em JavaScript (TypeScript) inspirado pelo Angular.

Ele alcança algo um tanto similar ao que pode ser feito com Flask-apispec.

Ele tem um sistema de injeção de dependência integrado, inspirado pelo Angular 2. É necessário fazer o pré-registro dos "injetáveis" (como todos os sistemas de injeção de dependência que conheço), então, adiciona verbosidade e repetição de código.

Como os parâmetros são descritos com tipos do TypeScript (similares às anotações de tipo do Python), o suporte do editor é muito bom.

Mas como os dados do TypeScript não são preservados após a compilação para JavaScript, ele não pode depender dos tipos para definir validação, serialização e documentação ao mesmo tempo. Devido a isso e a algumas decisões de projeto, para obter validação, serialização e geração automática de schema, é necessário adicionar decorators em muitos lugares. Então, ele se torna bastante verboso.

Ele não consegue lidar muito bem com modelos aninhados. Então, se o corpo JSON na requisição for um objeto JSON que contém campos internos que por sua vez são objetos JSON aninhados, ele não consegue ser documentado e validado apropriadamente.

/// check | **FastAPI** inspirado para

Usar tipos do Python para ter um ótimo suporte do editor.

Ter um sistema de injeção de dependência poderoso. Encontrar um jeito de minimizar repetição de código.

///

### <a href="https://sanic.readthedocs.io/en/latest/" class="external-link" target="_blank">Sanic</a> { #sanic }

Ele foi um dos primeiros frameworks Python extremamente rápidos baseados em `asyncio`. Ele foi feito para ser muito similar ao Flask.

/// note | Detalhes Técnicos

Ele utilizava <a href="https://github.com/MagicStack/uvloop" class="external-link" target="_blank">`uvloop`</a> em vez do loop `asyncio` padrão do Python. É isso que o deixava tão rápido.

Ele claramente inspirou Uvicorn e Starlette, que atualmente são mais rápidos que o Sanic em benchmarks abertos.

///

/// check | **FastAPI** inspirado para

Encontrar um jeito de ter uma performance insana.

É por isso que o **FastAPI** é baseado em Starlette, pois ela é o framework mais rápido disponível (testado por benchmarks de terceiros).

///

### <a href="https://falconframework.org/" class="external-link" target="_blank">Falcon</a> { #falcon }

Falcon é outro framework Python de alta performance, projetado para ser minimalista, e servir como base para outros frameworks como Hug.

Ele é projetado para ter funções que recebem dois parâmetros, uma "request" e uma "response". Então você "lê" partes da requisição, e "escreve" partes para a resposta. Por causa desse design, não é possível declarar parâmetros de requisição e corpos com as anotações de tipo padrão do Python como parâmetros de função.

Então, validação de dados, serialização e documentação têm que ser feitos no código, não automaticamente. Ou eles têm que ser implementados como um framework acima do Falcon, como o Hug. Essa mesma distinção acontece em outros frameworks inspirados pelo design do Falcon, de ter um objeto de request e um objeto de response como parâmetros.

/// check | **FastAPI** inspirado para

Encontrar maneiras de obter uma ótima performance.

Juntamente com Hug (como Hug é baseado no Falcon) inspirou **FastAPI** a declarar um parâmetro de `response` nas funções.

Embora no FastAPI seja opcional, é utilizado principalmente para configurar cabeçalhos, cookies e códigos de status alternativos.

///

### <a href="https://moltenframework.com/" class="external-link" target="_blank">Molten</a> { #molten }

Eu descobri Molten nos primeiros estágios da construção do **FastAPI**. E ele tem ideias bastante similares:

* Baseado nas anotações de tipo do Python.
* Validação e documentação a partir desses tipos.
* Sistema de Injeção de Dependência.

Ele não utiliza uma biblioteca de terceiros para validação de dados, serialização e documentação como o Pydantic, ele tem a sua própria. Então, essas definições de tipos de dados não seriam reutilizáveis tão facilmente.

Ele exige configurações um pouco mais verbosas. E como é baseado em WSGI (em vez de ASGI), ele não é projetado para tirar vantagem da alta performance fornecida por ferramentas como Uvicorn, Starlette e Sanic.

O sistema de injeção de dependência exige pré-registro das dependências e elas são resolvidas com base nos tipos declarados. Então, não é possível declarar mais de um "componente" que forneça um certo tipo.

As rotas são declaradas em um único lugar, usando funções declaradas em outros lugares (em vez de usar decorators que possam ser colocados diretamente acima da função que lida com o endpoint). Isso é mais próximo de como o Django faz do que de como o Flask (e o Starlette) fazem. Separa no código coisas que são relativamente bem acopladas.

/// check | **FastAPI** inspirado para

Definir validações extras para tipos de dados usando o valor "padrão" de atributos dos modelos. Isso melhora o suporte do editor, e não estava disponível no Pydantic antes.

Isso na verdade inspirou a atualização de partes do Pydantic, para dar suporte ao mesmo estilo de declaração da validação (toda essa funcionalidade já está disponível no Pydantic).

///

### <a href="https://github.com/hugapi/hug" class="external-link" target="_blank">Hug</a> { #hug }

Hug foi um dos primeiros frameworks a implementar a declaração de tipos de parâmetros de API usando anotações de tipo do Python. Isso foi uma ótima ideia que inspirou outras ferramentas a fazer o mesmo.

Ele usou tipos personalizados em suas declarações em vez dos tipos padrão do Python, mas mesmo assim foi um grande passo adiante.

Ele também foi um dos primeiros frameworks a gerar um schema personalizado declarando a API inteira em JSON.

Ele não era baseado em um padrão como OpenAPI e JSON Schema. Então não seria simples integrá-lo com outras ferramentas, como Swagger UI. Mas novamente, era uma ideia muito inovadora.

Ele tem um recurso interessante e incomum: usando o mesmo framework, é possível criar APIs e também CLIs.

Como é baseado no padrão anterior para frameworks web Python síncronos (WSGI), ele não consegue lidar com Websockets e outras coisas, embora ainda tenha alta performance também.

/// info | Informação

Hug foi criado por Timothy Crosley, o mesmo criador do <a href="https://github.com/timothycrosley/isort" class="external-link" target="_blank">`isort`</a>, uma ótima ferramenta para ordenar automaticamente imports em arquivos Python.

///

/// check | Ideias que inspiraram o **FastAPI**

Hug inspirou partes do APIStar, e foi uma das ferramentas que achei mais promissoras, ao lado do APIStar.

Hug ajudou a inspirar o **FastAPI** a usar anotações de tipo do Python para declarar parâmetros e para gerar um schema definindo a API automaticamente.

Hug inspirou **FastAPI** a declarar um parâmetro de `response` em funções para definir cabeçalhos e cookies.

///

### <a href="https://github.com/encode/apistar" class="external-link" target="_blank">APIStar</a> (<= 0.5) { #apistar-0-5 }

Pouco antes de decidir construir o **FastAPI** eu encontrei o servidor **APIStar**. Ele tinha quase tudo o que eu estava procurando e tinha um ótimo design.

Foi uma das primeiras implementações de um framework usando anotações de tipo do Python para declarar parâmetros e requisições que eu já vi (antes do NestJS e Molten). Eu o encontrei mais ou menos na mesma época que o Hug. Mas o APIStar utilizava o padrão OpenAPI.

Ele tinha validação de dados automática, serialização de dados e geração de schema OpenAPI baseadas nas mesmas anotações de tipo em vários locais.

As definições de schema de corpo não utilizavam as mesmas anotações de tipo do Python como o Pydantic, eram um pouco mais similares ao Marshmallow, então o suporte do editor não seria tão bom, ainda assim, APIStar era a melhor opção disponível.

Ele obteve os melhores benchmarks de performance na época (somente ultrapassado por Starlette).

A princípio, ele não tinha uma interface web com documentação automática da API, mas eu sabia que poderia adicionar o Swagger UI a ele.

Ele tinha um sistema de injeção de dependência. Exigia pré-registro dos componentes, como outras ferramentas já discutidas acima. Mas ainda assim era um grande recurso.

Eu nunca fui capaz de usá-lo em um projeto completo, pois ele não tinha integração de segurança, então, eu não pude substituir todos os recursos que eu tinha com os geradores full-stack baseados no Flask-apispec. Eu tinha no meu backlog de projetos criar um pull request adicionando essa funcionalidade.

Mas então, o foco do projeto mudou.

Ele não era mais um framework web de API, pois o criador precisava focar no Starlette.

Agora APIStar é um conjunto de ferramentas para validar especificações OpenAPI, não um framework web.

/// info | Informação

APIStar foi criado por Tom Christie. O mesmo cara que criou:

* Django REST Framework
* Starlette (no qual **FastAPI** é baseado)
* Uvicorn (usado por Starlette e **FastAPI**)

///

/// check | **FastAPI** inspirado para

Existir.

A ideia de declarar múltiplas coisas (validação de dados, serialização e documentação) com os mesmos tipos do Python, que ao mesmo tempo fornecessem grande suporte ao editor, era algo que eu considerava uma ideia brilhante.

E após procurar por muito tempo por um framework similar e testar muitas alternativas diferentes, APIStar foi a melhor opção disponível.

Então APIStar deixou de existir como servidor e o Starlette foi criado, sendo uma nova e melhor fundação para tal sistema. Essa foi a inspiração final para construir o **FastAPI**.

Eu considero o **FastAPI** um "sucessor espiritual" do APIStar, enquanto aprimora e amplia as funcionalidades, o sistema de tipagem e outras partes, baseado nos aprendizados de todas essas ferramentas anteriores.

///

## Usados por **FastAPI** { #used-by-fastapi }

### <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> { #pydantic }

Pydantic é uma biblioteca para definir validação de dados, serialização e documentação (usando JSON Schema) com base nas anotações de tipo do Python.

Isso o torna extremamente intuitivo.

Ele é comparável ao Marshmallow. Embora seja mais rápido que o Marshmallow em benchmarks. E como é baseado nas mesmas anotações de tipo do Python, o suporte do editor é ótimo.

/// check | **FastAPI** usa isso para

Controlar toda a validação de dados, serialização de dados e documentação automática de modelos (baseada no JSON Schema).

**FastAPI** então pega esses dados do JSON Schema e os coloca no OpenAPI, além de todas as outras coisas que faz.

///

### <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> { #starlette }

Starlette é um framework/caixa de ferramentas <abbr title="O novo padrão para construir aplicações web Python assíncronas">ASGI</abbr> leve, o que é ideal para construir serviços asyncio de alta performance.

Ele é muito simples e intuitivo. É projetado para ser facilmente extensível, e ter componentes modulares.

Ele tem:

* Performance seriamente impressionante.
* Suporte a WebSocket.
* Tarefas em segundo plano dentro do processo.
* Eventos de inicialização e encerramento.
* Cliente de testes construído com HTTPX.
* CORS, GZip, Arquivos Estáticos, respostas Streaming.
* Suporte para Sessão e Cookie.
* 100% coberto por testes.
* Código base 100% anotado com tipagem.
* Poucas dependências obrigatórias.

Starlette é atualmente o framework Python mais rápido testado. Somente ultrapassado pelo Uvicorn, que não é um framework, mas um servidor.

Starlette fornece toda a funcionalidade básica de um microframework web.

Mas ele não fornece validação de dados automática, serialização ou documentação.

Essa é uma das principais coisas que o **FastAPI** adiciona por cima, tudo baseado nas anotações de tipo do Python (usando Pydantic). Isso, mais o sistema de injeção de dependência, utilidades de segurança, geração de schema OpenAPI, etc.

/// note | Detalhes Técnicos

ASGI é um novo "padrão" sendo desenvolvido por membros do time central do Django. Ele ainda não é um "padrão Python" (uma PEP), embora eles estejam no processo de fazer isso.

No entanto, ele já está sendo utilizado como "padrão" por diversas ferramentas. Isso melhora enormemente a interoperabilidade, pois você poderia trocar Uvicorn por qualquer outro servidor ASGI (como Daphne ou Hypercorn), ou você poderia adicionar ferramentas compatíveis com ASGI, como `python-socketio`.

///

/// check | **FastAPI** usa isso para

Controlar todas as partes web centrais. Adiciona funcionalidades por cima.

A classe `FastAPI` em si herda diretamente da classe `Starlette`.

Então, qualquer coisa que você pode fazer com Starlette, você pode fazer diretamente com o **FastAPI**, pois ele é basicamente um Starlette com esteróides.

///

### <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a> { #uvicorn }

Uvicorn é um servidor ASGI extremamente rápido, construído com uvloop e httptools.

Ele não é um framework web, mas sim um servidor. Por exemplo, ele não fornece ferramentas para roteamento por paths. Isso é algo que um framework como Starlette (ou **FastAPI**) forneceria por cima.

Ele é o servidor recomendado para Starlette e **FastAPI**.

/// check | **FastAPI** o recomenda como

O principal servidor web para rodar aplicações **FastAPI**.

Você também pode usar a opção de linha de comando `--workers` para ter um servidor assíncrono multi-processos.

Verifique mais detalhes na seção [Deployment](deployment/index.md){.internal-link target=_blank}.

///

## Benchmarks e velocidade { #benchmarks-and-speed }

Para entender, comparar e ver a diferença entre Uvicorn, Starlette e FastAPI, verifique a seção sobre [Benchmarks](benchmarks.md){.internal-link target=_blank}.
