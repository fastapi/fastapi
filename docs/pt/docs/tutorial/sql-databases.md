# Bancos de Dados SQL (Relacionais) { #sql-relational-databases }

**FastAPI** não exige que você use um banco de dados SQL (relacional). Mas você pode usar **qualquer banco de dados** que quiser.

Aqui veremos um exemplo usando [SQLModel](https://sqlmodel.tiangolo.com/).

**SQLModel** é construído sobre [SQLAlchemy](https://www.sqlalchemy.org/) e Pydantic. Ele foi criado pelo mesmo autor do **FastAPI** para ser o par perfeito para aplicações **FastAPI** que precisam usar **bancos de dados SQL**.

/// tip | Dica

Você pode usar qualquer outra biblioteca de banco de dados SQL ou NoSQL que quiser (em alguns casos chamadas de <abbr title="Object Relational Mapper - Mapeador Objeto-Relacional: um termo sofisticado para uma biblioteca onde algumas classes representam tabelas SQL e instâncias representam linhas nessas tabelas">"ORMs"</abbr>), o FastAPI não obriga você a usar nada. 😎

///

Como o SQLModel é baseado no SQLAlchemy, você pode facilmente usar **qualquer banco de dados suportado** pelo SQLAlchemy (o que também os torna suportados pelo SQLModel), como:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

Neste exemplo, usaremos **SQLite**, porque ele usa um único arquivo e o Python tem suporte integrado. Assim, você pode copiar este exemplo e executá-lo como está.

Mais tarde, para sua aplicação em produção, você pode querer usar um servidor de banco de dados como o **PostgreSQL**.

/// tip | Dica

Existe um gerador de projetos oficial com **FastAPI** e **PostgreSQL** incluindo um frontend e mais ferramentas: [https://github.com/fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)

///

Este é um tutorial muito simples e curto, se você quiser aprender sobre bancos de dados em geral, sobre SQL ou recursos mais avançados, acesse a [documentação do SQLModel](https://sqlmodel.tiangolo.com/).

## Instalar o `SQLModel` { #install-sqlmodel }

Primeiro, certifique-se de criar seu [ambiente virtual](../virtual-environments.md), ativá-lo e, em seguida, instalar o `sqlmodel`:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Crear o App com um Único Modelo { #create-the-app-with-a-single-model }

Vamos criar a primeira versão mais simples do app com um único modelo **SQLModel**.

Depois, vamos melhorá-lo aumentando a segurança e versatilidade com **múltiplos modelos** abaixo. 🤓

### Criar Modelos { #create-models }

Importe o `SQLModel` e crie um modelo de banco de dados:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

A classe `Hero` é muito semelhante a um modelo Pydantic (na verdade, por baixo dos panos, ela *é um modelo Pydantic*).

Existem algumas diferenças:

* `table=True` informa ao SQLModel que este é um *modelo de tabela*, ele deve representar uma **tabela** no banco de dados SQL, não é apenas um *modelo de dados* (como seria qualquer outra classe Pydantic comum).

* `Field(primary_key=True)` informa ao SQLModel que o `id` é a **chave primária** no banco de dados SQL (você pode aprender mais sobre chaves primárias SQL na documentação do SQLModel).

    **Nota:** Usamos `int | None` para o campo de chave primária para que, no código Python, possamos *criar um objeto sem um `id`* (`id=None`), assumindo que o banco de dados irá *gerá-lo ao salvar*. O SQLModel entende que o banco de dados fornecerá o `id` e *define a coluna como um `INTEGER` não nulo* no esquema do banco de dados. Veja a [documentação do SQLModel sobre chaves primárias](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id) para detalhes.

* `Field(index=True)` informa ao SQLModel que ele deve criar um **índice SQL** para essa coluna, o que permitirá buscas mais rápidas no banco de dados ao ler dados filtrados por essa coluna.

    O SQLModel saberá que algo declarado como `str` será uma coluna SQL do tipo `TEXT` (ou `VARCHAR`, dependendo do banco de dados).

### Criar um Engine { #create-an-engine }
Um `engine` SQLModel (por baixo dos panos, ele é na verdade um `engine` do SQLAlchemy) é o que **mantém as conexões** com o banco de dados.

Você teria **um único objeto `engine`** para todo o seu código se conectar ao mesmo banco de dados.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

Usar `check_same_thread=False` permite que o FastAPI use o mesmo banco de dados SQLite em diferentes threads. Isso é necessário, pois **uma única requisição** pode usar **mais de uma thread** (por exemplo, em dependências).

Não se preocupe, com a forma como o código está estruturado, garantiremos que usamos **uma única *sessão* SQLModel por requisição** mais tarde, isso é realmente o que o `check_same_thread` está tentando conseguir.

### Criar as Tabelas { #create-the-tables }

Em seguida, adicionamos uma função que usa `SQLModel.metadata.create_all(engine)` para **criar as tabelas** para todos os *modelos de tabela*.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Criar uma Dependência de Sessão { #create-a-session-dependency }

Uma **`Session`** é o que armazena os **objetos na memória** e acompanha as alterações necessárias nos dados, para então **usar o `engine`** para se comunicar com o banco de dados.

Vamos criar uma **dependência** do FastAPI com `yield` que fornecerá uma nova `Session` para cada requisição. Isso é o que garante que usamos uma única sessão por requisição. 🤓

Então, criamos uma dependência `Annotated` chamada `SessionDep` para simplificar o restante do código que usará essa dependência.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Criar Tabelas de Banco de Dados na Inicialização { #create-database-tables-on-startup }

Vamos criar as tabelas do banco de dados quando o aplicativo for iniciado.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Aqui, criamos as tabelas em um evento de inicialização do aplicativo.

Para produção, você provavelmente usaria um script de migração que é executado antes de iniciar seu app. 🤓

/// tip | Dica

O SQLModel terá utilitários de migração envolvendo o Alembic, mas por enquanto, você pode usar o [Alembic](https://alembic.sqlalchemy.org/en/latest/) diretamente.

///

### Criar um Hero { #create-a-hero }

Como cada modelo SQLModel também é um modelo Pydantic, você pode usá-lo nas mesmas **anotações de tipo** que usaria para modelos Pydantic.

Por exemplo, se você declarar um parâmetro do tipo `Hero`, ele será lido do **corpo JSON**.

Da mesma forma, você pode declará-lo como o **tipo de retorno** da função, e então o formato dos dados aparecerá na interface de documentação automática da API.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Aqui, usamos a dependência `SessionDep` (uma `Session`) para adicionar o novo `Hero` à instância `Session`, fazer commit das alterações no banco de dados, atualizar os dados no `hero` e então retorná-lo.

### Ler Heroes { #read-heroes }

Podemos **ler** `Hero`s do banco de dados usando um `select()`. Podemos incluir um `limit` e `offset` para paginar os resultados.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Ler um Único Hero { #read-one-hero }

Podemos **ler** um único `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Deletar um Hero { #delete-a-hero }

Também podemos **deletar** um `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Executar o App { #run-the-app }

Você pode executar o app:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Então, vá para a interface `/docs`, você verá que o **FastAPI** está usando esses **modelos** para **documentar** a API, e ele também os usará para **serializar** e **validar** os dados.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Atualizar o App com Múltiplos Modelos { #update-the-app-with-multiple-models }

Agora vamos **refatorar** este app um pouco para aumentar a **segurança** e **versatilidade**.

Se você verificar o app anterior, na interface você pode ser que, até agora, ele permite que o cliente decida o `id` do `Hero` a ser criado. 😱

Não deveríamos deixar isso acontecer, eles poderiam sobrescrever um `id` que já atribuimos na base de dados. Decidir o `id` deve ser feito pelo **backend** ou pelo **banco de dados**, **não pelo cliente**.

Além disso, criamos um `secret_name` para o hero, mas até agora estamos retornando ele em todos os lugares, isso não é muito **secreto**... 😅

Vamos corrigir essas coisas adicionando alguns **modelos extras**. Aqui é onde o SQLModel vai brilhar. ✨

### Criar Múltiplos Modelos { #create-multiple-models }

No **SQLModel**, qualquer classe de modelo que tenha `table=True` é um **modelo de tabela**.

E qualquer classe de modelo que não tenha `table=True` é um **modelo de dados**, esses são na verdade apenas modelos Pydantic (com alguns recursos extras pequenos). 🤓

Com o SQLModel, podemos usar a **herança** para **evitar duplicação** de todos os campos em todos os casos.

#### `HeroBase` - a classe base { #herobase-the-base-class }

Vamos começar com um modelo `HeroBase` que tem todos os **campos compartilhados** por todos os modelos:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - o *modelo de tabela* { #hero-the-table-model }

Em seguida, vamos criar `Hero`, o verdadeiro *modelo de tabela*, com os **campos extras** que nem sempre estão nos outros modelos:

* `id`
* `secret_name`

Como `Hero` herda de `HeroBase`, ele **também** tem os **campos** declarados em `HeroBase`, então todos os campos para `Hero` são:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - o *modelo de dados* público { #heropublic-the-public-data-model }

Em seguida, criamos um modelo `HeroPublic`, que será **retornado** para os clientes da API.

Ele tem os mesmos campos que `HeroBase`, então não incluirá `secret_name`.

Finalmente, a identidade dos nossos heróis está protegida! 🥷

Ele também declara novamente `id: int`. Ao fazer isso, estamos fazendo um **contrato** com os clientes da API, para que eles possam sempre esperar que o `id` estará lá e será um `int` (nunca será `None`).

/// tip | Dica

Fazer com que o modelo de retorno garanta que um valor esteja sempre disponível e sempre seja um `int` (não `None`) é muito útil para os clientes da API, eles podem escrever código muito mais simples com essa certeza.

Além disso, **clientes gerados automaticamente** terão interfaces mais simples, para que os desenvolvedores que se comunicam com sua API possam ter uma experiência muito melhor trabalhando com sua API. 😎

///

Todos os campos em `HeroPublic` são os mesmos que em `HeroBase`, com `id` declarado como `int` (não `None`):

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - o *modelo de dados* para criar um hero { #herocreate-the-data-model-to-create-a-hero }

Agora criamos um modelo `HeroCreate`, este é o que **validará** os dados dos clientes.

Ele tem os mesmos campos que `HeroBase`, e também tem `secret_name`.

Agora, quando os clientes **criarem um novo hero**, eles enviarão o `secret_name`, ele será armazenado no banco de dados, mas esses nomes secretos não serão retornados na API para os clientes.

/// tip | Dica

É assim que você trataria **senhas**. Receba-as, mas não as retorne na API.

Você também faria um **hash** com os valores das senhas antes de armazená-los, **nunca os armazene em texto simples**.

///

Os campos de `HeroCreate` são:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - o *modelo de dados* para atualizar um hero { #heroupdate-the-data-model-to-update-a-hero }

Não tínhamos uma maneira de **atualizar um hero** na versão anterior do app, mas agora com **múltiplos modelos**, podemos fazer isso. 🎉

O *modelo de dados* `HeroUpdate` é um pouco especial, ele tem **todos os mesmos campos** que seriam necessários para criar um novo hero, mas todos os campos são **opcionais** (todos têm um valor padrão). Dessa forma, quando você atualizar um hero, poderá enviar apenas os campos que deseja atualizar.

Como todos os **campos realmente mudam** (o tipo agora inclui `None` e eles agora têm um valor padrão de `None`), precisamos **declarar novamente** todos eles.

Não precisamos herdar de `HeroBase`, pois estamos redeclarando todos os campos. Vou deixá-lo herdando apenas por consistência, mas isso não é necessário. É mais uma questão de gosto pessoal. 🤷

Os campos de `HeroUpdate` são:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Criar com `HeroCreate` e retornar um `HeroPublic` { #create-with-herocreate-and-return-a-heropublic }

Agora que temos **múltiplos modelos**, podemos atualizar as partes do app que os utilizam.

Recebemos na requisição um *modelo de dados* `HeroCreate`, e a partir dele, criamos um *modelo de tabela* `Hero`.

Esse novo *modelo de tabela* `Hero` terá os campos enviados pelo cliente, e também terá um `id` gerado pelo banco de dados.

Em seguida, retornamos o mesmo *modelo de tabela* `Hero` como está na função. Mas como declaramos o `response_model` com o *modelo de dados* `HeroPublic`, o **FastAPI** usará `HeroPublic` para validar e serializar os dados.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | Dica

Agora usamos `response_model=HeroPublic` em vez da **anotação de tipo de retorno** `-> HeroPublic` porque o valor que estamos retornando na verdade *não* é um `HeroPublic`.

Se tivéssemos declarado `-> HeroPublic`, seu editor e o linter reclamariam (com razão) que você está retornando um `Hero` em vez de um `HeroPublic`.

Ao declará-lo no `response_model`, estamos dizendo ao **FastAPI** para fazer o seu trabalho, sem interferir nas anotações de tipo e na ajuda do seu editor e de outras ferramentas.

///

### Ler Heroes com `HeroPublic` { #read-heroes-with-heropublic }

Podemos fazer o mesmo que antes para **ler** `Hero`s, novamente, usamos `response_model=list[HeroPublic]` para garantir que os dados sejam validados e serializados corretamente.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### Ler Um Hero com `HeroPublic` { #read-one-hero-with-heropublic }

Podemos **ler** um único herói:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Atualizar um Hero com `HeroUpdate` { #update-a-hero-with-heroupdate }

Podemos **atualizar um hero**. Para isso, usamos uma operação HTTP `PATCH`.

E no código, obtemos um `dict` com todos os dados enviados pelo cliente, **apenas os dados enviados pelo cliente**, excluindo quaisquer valores que estariam lá apenas por serem os valores padrão. Para fazer isso, usamos `exclude_unset=True`. Este é o truque principal. 🪄

Em seguida, usamos `hero_db.sqlmodel_update(hero_data)` para atualizar o `hero_db` com os dados de `hero_data`.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Deletar um Hero Novamente { #delete-a-hero-again }

**Deletar** um hero permanece praticamente o mesmo.

Não vamos satisfazer o desejo de refatorar tudo neste aqui. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Executar o App Novamente { #run-the-app-again }

Você pode executar o app novamente:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Se você for para a interface `/docs` da API, verá que agora ela está atualizada e não esperará receber o `id` do cliente ao criar um hero, etc.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Recapitulando { #recap }

Você pode usar [**SQLModel**](https://sqlmodel.tiangolo.com/) para interagir com um banco de dados SQL e simplificar o código com *modelos de dados* e *modelos de tabela*.

Você pode aprender muito mais na documentação do **SQLModel**, há um mini [tutorial sobre como usar SQLModel com **FastAPI**](https://sqlmodel.tiangolo.com/tutorial/fastapi/) mais longo. 🚀
