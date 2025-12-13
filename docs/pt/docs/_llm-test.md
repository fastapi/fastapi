# Arquivo de teste de LLM { #llm-test-file }

Este documento testa se o <abbr title="Large Language Model – Modelo de Linguagem de Grande Porte">LLM</abbr>, que traduz a documentação, entende o `general_prompt` em `scripts/translate.py` e o prompt específico do idioma em `docs/{language code}/llm-prompt.md`. O prompt específico do idioma é anexado ao `general_prompt`.

Os testes adicionados aqui serão vistos por todos os autores dos prompts específicos de idioma.

Use da seguinte forma:

* Tenha um prompt específico do idioma – `docs/{language code}/llm-prompt.md`.
* Faça uma tradução nova deste documento para o seu idioma de destino (veja, por exemplo, o comando `translate-page` do `translate.py`). Isso criará a tradução em `docs/{language code}/docs/_llm-test.md`.
* Verifique se está tudo certo na tradução.
* Se necessário, melhore seu prompt específico do idioma, o prompt geral ou o documento em inglês.
* Em seguida, corrija manualmente os problemas restantes na tradução, para que fique uma boa tradução.
* Retraduzir, tendo a boa tradução no lugar. O resultado ideal seria que o LLM não fizesse mais mudanças na tradução. Isso significa que o prompt geral e o seu prompt específico do idioma estão tão bons quanto possível (às vezes fará algumas mudanças aparentemente aleatórias, a razão é que <a href="https://doublespeak.chat/#/handbook#deterministic-output" class="external-link" target="_blank">LLMs não são algoritmos determinísticos</a>).

Os testes:

## Trechos de código { #code-snippets }

//// tab | Teste

Este é um trecho de código: `foo`. E este é outro trecho de código: `bar`. E mais um: `baz quux`.

////

//// tab | Informações

O conteúdo dos trechos de código deve ser deixado como está.

Veja a seção `### Content of code snippets` no prompt geral em `scripts/translate.py`.

////

## Citações { #quotes }

//// tab | Teste

Ontem, meu amigo escreveu: "Se você soletrar incorretamente corretamente, você a soletrou incorretamente". Ao que respondi: "Correto, mas 'incorrectly' está incorretamente não '"incorrectly"'".

/// note | Nota

O LLM provavelmente vai traduzir isso errado. O interessante é apenas se ele mantém a tradução corrigida ao retraduzir.

///

////

//// tab | Informações

O autor do prompt pode escolher se deseja converter aspas neutras em aspas tipográficas. Também é aceitável deixá-las como estão.

Veja, por exemplo, a seção `### Quotes` em `docs/de/llm-prompt.md`.

////

## Citações em trechos de código { #quotes-in-code-snippets }

//// tab | Teste

`pip install "foo[bar]"`

Exemplos de literais de string em trechos de código: `"this"`, `'that'`.

Um exemplo difícil de literais de string em trechos de código: `f"I like {'oranges' if orange else "apples"}"`

Pesado: `Yesterday, my friend wrote: "If you spell incorrectly correctly, you have spelled it incorrectly". To which I answered: "Correct, but 'incorrectly' is incorrectly not '"incorrectly"'"`

////

//// tab | Informações

... No entanto, as aspas dentro de trechos de código devem permanecer como estão.

////

## Blocos de código { #code-blocks }

//// tab | Teste

Um exemplo de código Bash...

```bash
# Imprimir uma saudação ao universo
echo "Hello universe"
```

...e um exemplo de código de console...

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
<span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting server
        Searching for package file structure
```

...e outro exemplo de código de console...

```console
// Crie um diretório "Code"
$ mkdir code
// Entre nesse diretório
$ cd code
```

...e um exemplo de código Python...

```Python
wont_work()  # Isto não vai funcionar 😱
works(foo="bar")  # Isto funciona 🎉
```

...e é isso.

////

//// tab | Informações

O código em blocos de código não deve ser modificado, com exceção dos comentários.

Veja a seção `### Content of code blocks` no prompt geral em `scripts/translate.py`.

////

## Abas e caixas coloridas { #tabs-and-colored-boxes }

//// tab | Teste

/// info | Informação
Algum texto
///

/// note | Nota
Algum texto
///

/// note | Detalhes Técnicos
Algum texto
///

/// check | Verifique
Algum texto
///

/// tip | Dica
Algum texto
///

/// warning | Atenção
Algum texto
///

/// danger | Cuidado
Algum texto
///

////

//// tab | Informações

Abas e blocos `Info`/`Note`/`Warning`/etc. devem ter a tradução do seu título adicionada após uma barra vertical (`|`).

Veja as seções `### Special blocks` e `### Tab blocks` no prompt geral em `scripts/translate.py`.

////

## Links da Web e internos { #web-and-internal-links }

//// tab | Teste

O texto do link deve ser traduzido, o endereço do link deve permanecer inalterado:

* [Link para o título acima](#code-snippets)
* [Link interno](index.md#installation){.internal-link target=_blank}
* <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">Link externo</a>
* <a href="https://fastapi.tiangolo.com/css/styles.css" class="external-link" target="_blank">Link para um estilo</a>
* <a href="https://fastapi.tiangolo.com/js/logic.js" class="external-link" target="_blank">Link para um script</a>
* <a href="https://fastapi.tiangolo.com/img/foo.jpg" class="external-link" target="_blank">Link para uma imagem</a>

O texto do link deve ser traduzido, o endereço do link deve apontar para a tradução:

* <a href="https://fastapi.tiangolo.com/pt/" class="external-link" target="_blank">Link do FastAPI</a>

////

//// tab | Informações

Os links devem ser traduzidos, mas seus endereços devem permanecer inalterados. Uma exceção são links absolutos para páginas da documentação do FastAPI. Nesse caso, devem apontar para a tradução.

Veja a seção `### Links` no prompt geral em `scripts/translate.py`.

////

## Elementos HTML "abbr" { #html-abbr-elements }

//// tab | Teste

Aqui estão algumas coisas envolvidas em elementos HTML "abbr" (algumas são inventadas):

### O abbr fornece uma frase completa { #the-abbr-gives-a-full-phrase }

* <abbr title="Getting Things Done – Fazer as Coisas">GTD</abbr>
* <abbr title="menos que"><code>lt</code></abbr>
* <abbr title="XML Web Token – Token Web XML">XWT</abbr>
* <abbr title="Parallel Server Gateway Interface – Interface de Gateway de Servidor Paralelo">PSGI</abbr>

### O abbr fornece uma explicação { #the-abbr-gives-an-explanation }

* <abbr title="Um grupo de máquinas configuradas para estarem conectadas e trabalharem juntas de alguma forma.">cluster</abbr>
* <abbr title="Um método de aprendizado de máquina que usa redes neurais artificiais com numerosas camadas ocultas entre as camadas de entrada e saída, desenvolvendo assim uma estrutura interna abrangente">Aprendizado Profundo</abbr>

### O abbr fornece uma frase completa e uma explicação { #the-abbr-gives-a-full-phrase-and-an-explanation }

* <abbr title="Mozilla Developer Network – Rede de Desenvolvedores da Mozilla: documentação para desenvolvedores, escrita pelo pessoal do Firefox">MDN</abbr>
* <abbr title="Input/Output – Entrada/Saída: leitura ou escrita em disco, comunicações de rede.">I/O</abbr>.

////

//// tab | Informações

Os atributos "title" dos elementos "abbr" são traduzidos seguindo algumas instruções específicas.

As traduções podem adicionar seus próprios elementos "abbr" que o LLM não deve remover. Por exemplo, para explicar palavras em inglês.

Veja a seção `### HTML abbr elements` no prompt geral em `scripts/translate.py`.

////

## Títulos { #headings }

//// tab | Teste

### Desenvolver uma aplicação web - um tutorial { #develop-a-webapp-a-tutorial }

Olá.

### Anotações de tipo e -anotações { #type-hints-and-annotations }

Olá novamente.

### Super- e subclasses { #super-and-subclasses }

Olá novamente.

////

//// tab | Informações

A única regra rígida para títulos é que o LLM deixe a parte do hash dentro de chaves inalterada, o que garante que os links não quebrem.

Veja a seção `### Headings` no prompt geral em `scripts/translate.py`.

Para algumas instruções específicas do idioma, veja, por exemplo, a seção `### Headings` em `docs/de/llm-prompt.md`.

////

## Termos usados na documentação { #terms-used-in-the-docs }

//// tab | Teste

* você
* seu

* por exemplo
* etc.

* `foo` como um `int`
* `bar` como uma `str`
* `baz` como uma `list`

* o Tutorial - Guia do Usuário
* o Guia do Usuário Avançado
* a documentação do SQLModel
* a documentação da API
* a documentação automática

* Ciência de Dados
* Aprendizado Profundo
* Aprendizado de Máquina
* Injeção de Dependências
* autenticação HTTP Basic
* HTTP Digest
* formato ISO
* o padrão JSON Schema
* o JSON schema
* a definição do schema
* Fluxo de Senha
* Mobile

* descontinuado
* projetado
* inválido
* dinamicamente
* padrão
* padrão predefinido
* sensível a maiúsculas e minúsculas
* não sensível a maiúsculas e minúsculas

* servir a aplicação
* servir a página

* o app
* a aplicação

* a requisição
* a resposta
* a resposta de erro

* a operação de rota
* o decorador de operação de rota
* a função de operação de rota

* o corpo
* o corpo da requisição
* o corpo da resposta
* o corpo JSON
* o corpo do formulário
* o corpo do arquivo
* o corpo da função

* o parâmetro
* o parâmetro de corpo
* o parâmetro de path
* o parâmetro de query
* o parâmetro de cookie
* o parâmetro de header
* o parâmetro de formulário
* o parâmetro da função

* o evento
* o evento de inicialização
* a inicialização do servidor
* o evento de encerramento
* o evento de lifespan

* o manipulador
* o manipulador de eventos
* o manipulador de exceções
* tratar

* o modelo
* o modelo Pydantic
* o modelo de dados
* o modelo de banco de dados
* o modelo de formulário
* o objeto de modelo

* a classe
* a classe base
* a classe pai
* a subclasse
* a classe filha
* a classe irmã
* o método de classe

* o cabeçalho
* os cabeçalhos
* o cabeçalho de autorização
* o cabeçalho `Authorization`
* o cabeçalho encaminhado

* o sistema de injeção de dependências
* a dependência
* o dependable
* o dependant

* limitado por I/O
* limitado por CPU
* concorrência
* paralelismo
* multiprocessamento

* a env var
* a variável de ambiente
* o `PATH`
* a variável `PATH`

* a autenticação
* o provedor de autenticação
* a autorização
* o formulário de autorização
* o provedor de autorização
* o usuário se autentica
* o sistema autentica o usuário

* a CLI
* a interface de linha de comando

* o servidor
* o cliente

* o provedor de nuvem
* o serviço de nuvem

* o desenvolvimento
* as etapas de desenvolvimento

* o dict
* o dicionário
* a enumeração
* o enum
* o membro do enum

* o codificador
* o decodificador
* codificar
* decodificar

* a exceção
* lançar

* a expressão
* a instrução

* o frontend
* o backend

* a discussão do GitHub
* a issue do GitHub

* o desempenho
* a otimização de desempenho

* o tipo de retorno
* o valor de retorno

* a segurança
* o esquema de segurança

* a tarefa
* a tarefa em segundo plano
* a função da tarefa

* o template
* o mecanismo de template

* a anotação de tipo
* a anotação de tipo

* o worker de servidor
* o worker do Uvicorn
* o Worker do Gunicorn
* o processo worker
* a classe de worker
* a carga de trabalho

* a implantação
* implantar

* o SDK
* o kit de desenvolvimento de software

* o `APIRouter`
* o `requirements.txt`
* o Bearer Token
* a alteração com quebra de compatibilidade
* o bug
* o botão
* o chamável
* o código
* o commit
* o gerenciador de contexto
* a corrotina
* a sessão do banco de dados
* o disco
* o domínio
* o mecanismo
* o X falso
* o método HTTP GET
* o item
* a biblioteca
* o lifespan
* o bloqueio
* o middleware
* a aplicação mobile
* o módulo
* a montagem
* a rede
* a origem
* a sobrescrita
* a carga útil
* o processador
* a propriedade
* o proxy
* o pull request
* a consulta
* a RAM
* a máquina remota
* o código de status
* a string
* a tag
* o framework web
* o curinga
* retornar
* validar

////

//// tab | Informações

Esta é uma lista não completa e não normativa de termos (principalmente) técnicos vistos na documentação. Pode ser útil para o autor do prompt descobrir para quais termos o LLM precisa de uma ajudinha. Por exemplo, quando ele continua revertendo uma boa tradução para uma tradução subótima. Ou quando tem problemas para conjugar/declinar um termo no seu idioma.

Veja, por exemplo, a seção `### List of English terms and their preferred German translations` em `docs/de/llm-prompt.md`.

////
