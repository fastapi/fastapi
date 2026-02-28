# Desenvolvimento – Como contribuir

Para começar, você pode ver as formas básicas de [ajudar o FastAPI e obter ajuda](help-fastapi.md){.internal-link target=_blank}.

## Desenvolvimento

Se você já clonou o <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">repositório do FastAPI</a> e deseja se aprofundar no código, aqui estão algumas orientações para configurar seu ambiente. 

### Instalar dependências

Crie um ambiente virtual e instale as dependências necessárias com <a href="https://github.com/astral-sh/uv" class="external-link" target="_blank">`uv`</a>:

<div class="termy">

```console
$ uv sync --extra all

---> 100%
```

</div>

Isso irá instalar todas as dependências e a versão local do FastAPI no seu ambiente virtual.

### Usando seu FastAPI local

Se você criar um arquivo Python que importe e utilize o FastAPI, e executá-lo com o Python do seu ambiente local, ele usará o código fonte local do FastAPI que você clonou.

E, se você atualizar esse código fonte local do FastAPI, ao executar novamente o arquivo Python, ele utilizará a versão atualizada do FastAPI que você acabou de editar.

Dessa forma, você não precisa “instalar” sua versão local para testar cada alteração.

/// note | Detalhes técnicos

Isso só acontece quando você instala usando `uv sync --extra all` em vez de executar `pip install fastapi` diretamente.

Isso acontece porque `uv sync --extra all` instalará a versão local do FastAPI no modo “editável” por padrão.

///

### Formatar o código

Há um script que você pode executar para formatar e limpar todo o seu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Ele também organizará automaticamente todas as importações.

## Testes

Há um script que você pode executar localmente para testar todo o código e gerar relatórios de cobertura em HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Esse comando gera o diretório `./htmlcov/`. Se você abrir o arquivo `./htmlcov/index.html` no navegador, poderá explorar interativamente as partes do código cobertas pelos testes e verificar se há alguma região sem cobertura.

## Documentação

Primeiro, certifique-se de que seu ambiente esteja configurado conforme descrito acima. Isso instalará todas as dependências.

### Documentação ao vivo

Durante o desenvolvimento local, há um script que constrói o site e verifica alterações, recarregando-o automaticamente em tempo real:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

Ele disponibilizará a documentação em http://127.0.0.1:8008.

Dessa forma, você pode editar os arquivos da documentação ou do código fonte e ver as alterações em tempo real.

/// tip

Como alternativa, você pode executar manualmente os mesmos passos que o script realiza.

Entre no diretório do idioma, para a documentação principal em inglês, use `docs/en/`:

```console
$ cd docs/en/
```

Em seguida, execute `mkdocs` nesse diretório:

```console
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

///

#### CLI do Typer (opcional)

As instruções aqui mostram como usar diretamente o script em `./scripts/docs.py` diretamente com o interpretador `python`.

Mas você também pode usar o <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a> e obter autocomplete de comandos no terminal após instalar o suporte a completion.

Se você instalar o Typer CLI, poderá instalar o completion com:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Estrutura da documentação

A documentação utiliza o <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

E há ferramentas/scripts adicionais para lidar com as traduções em `./scripts/docs.py`.

/// tip

Você não precisa ver o código em `./scripts/docs.py`, basta usá-lo pela linha de comando.

///

Toda a documentação está no formato Markdown no diretório `./docs/en/`.

Muitos dos tutoriais possuem blocos de código.

Na maioria dos casos, esses blocos de código são aplicações completas que podem ser executadas como estão.

Na verdade, esses blocos de código não são escritos diretamente no Markdown, eles são arquivos Python no diretório `./docs_src/`.

E esses arquivos Python são incluídos/injetados na documentação durante a geração do site.


### Documentação para testes

A maioria dos testes é executada diretamente sobre os arquivos de código de exemplo presentes na documentação.

Isso ajuda a garantir que:

* A documentação esteja atualizada.
* Os exemplos da documentação possam ser executados como estão.
* A maior parte das funcionalidades esteja coberta pela documentação, conforme assegurado pela cobertura de testes.

#### Aplicações e documentação ao mesmo tempo

Se você executar os exemplos com o comando abaixo, por exemplo:

<div class="termy">

```console
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Como o Uvicorn usa a porta `8000` por padrão, a documentação servida na porta `8000` não entrará em conflito.


### Traduções

A ajuda com traduções é MUITO apreciada! E isso não seria possível sem o apoio da comunidade. 🌎 🚀

Pull requests de tradução são gerados por LLMs, orientados por prompts elaborados pela equipe do FastAPI em conjunto com a comunidade de falantes nativos de cada idioma suportado.

#### LLM Prompt por Idioma

Cada idioma possui um diretório: <a href="https://github.com/fastapi/fastapi/tree/master/docs" class="external-link" target="_blank">https://github.com/fastapi/fastapi/tree/master/docs</a>, nele você pode encontrar um arquivo chamado `llm-prompt.md` com o prompt específico para aquele idioma.

Por exemplo, para o espanhol, o prompt está em: <a href="https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md" class="external-link" target="_blank">`docs/es/llm-prompt.md`</a>.

Se você encontrar erros no seu idioma, pode sugerir melhorias no prompt desse arquivo para a sua língua e solicitar a regeneração das páginas específicas que deseja atualizar após as alterações.

#### Revisando PRs de Tradução

Você também pode verificar os pull requests existentes <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">existing pull requests</a> para o seu idioma. É possível filtrar os pull requests pelos que possuem a label correspondente à sua língua. Por exemplo, para o espanhol, a label é <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>.

Ao revisar um pull request, é melhor não sugerir alterações diretamente no mesmo PR, pois ele foi gerado por LLM, e não será possível garantir que pequenas mudanças individuais sejam replicadas em outras seções semelhantes, ou que sejam preservadas quando o mesmo conteúdo for traduzido novamente.

Em vez de adicionar sugestões no PR de tradução, faça as sugestões no arquivo de prompt da LLM para aquele idioma, criando um novo PR. Por exemplo, para o espanhol, o arquivo de prompt da LLM está em: <a href="https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md" class="external-link" target="_blank">`docs/es/llm-prompt.md`</a>.

/// tip

Consulte a documentação sobre <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">como adicionar uma revisão de pull request</a> para aprová-lo ou solicitar alterações.

///

#### Inscreva-se para Receber Notificações do Seu Idioma

Verifique se existe uma <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">Discussão no GitHub</a> para coordenar as traduções do seu idioma. Você pode se inscrever nela e, quando houver um novo pull request para revisar, um comentário automático será adicionado à discussão.

Para verificar o código de 2 letras do idioma que você deseja traduzir, você pode consultar a tabela <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">lista de códigos ISO 639-1</a>.

#### Solicitar um Novo Idioma

Vamos supor que você queira solicitar traduções para um idioma que ainda não foi traduzido, nem mesmo parcialmente. Por exemplo, latim.

* O primeiro passo seria encontrar outras 2 pessoas que estejam dispostas a revisar os PRs de tradução desse idioma junto com você.
* Quando houver pelo menos 3 pessoas dispostas a se comprometer a manter esse idioma, você pode continuar com os próximos passos.
* Crie uma nova discussão seguindo o template.
* Marque as outras 2 pessoas que irão ajudar com o idioma e peça que confirmem ali que irão colaborar.

Quando houver várias pessoas participando da discussão, a equipe do FastAPI poderá avaliá-la e torná-la uma tradução oficial.

Em seguida, a documentação será traduzida automaticamente usando LLMs, e a equipe de falantes nativos poderá revisar a tradução e ajudar a ajustar os prompts da LLM.

Sempre que houver uma nova tradução — por exemplo, quando a documentação for atualizada ou uma nova seção for adicionada — será feito um comentário na mesma discussão com o link para a nova tradução a ser revisada.

## Código Automatizado e IA

Você é incentivado a usar todas as ferramentas que desejar para realizar seu trabalho e contribuir da forma mais eficiente possível, incluindo ferramentas de IA (LLMs), etc. Ainda assim, as contribuições devem ter intervenção humana significativa, julgamento, contexto, entre outros aspectos.

Se o **esforço humano** investido em um PR, por exemplo, ao escrever prompts para LLM, for **menor** do que o **esforço que precisaríamos dedicar** para **revisá-lo**, por favor, **não** envie o PR.

Pense da seguinte forma: nós já podemos escrever prompts para LLM ou executar ferramentas automatizadas por conta própria, e isso seria mais rápido do que revisar PRs externos.

### Fechando PRs Automatizados e de IA

Se identificarmos PRs que pareçam ter sido gerados por IA ou automatizados de forma semelhante, iremos sinalizá-los e fechá-los.

O mesmo se aplica a comentários e descrições, por favor, não copie e cole conteúdo gerado por uma LLM.

### Negação de Serviço por Esforço Humano

Usar ferramentas automatizadas e IA para enviar PRs ou comentários que precisemos revisar e tratar cuidadosamente seria o equivalente a <span style="white-space: nowrap;">um <a href="https://en.wikipedia.org/wiki/Denial-of-service_attack" class="external-link" target="_blank">ataque de negação de serviço</a></span> ao nosso esforço humano.

Seria um esforço muito pequeno por parte da pessoa que envia o PR (um prompt para LLM), mas que gera uma grande quantidade de esforço do nosso lado (revisando o código cuidadosamente).

Por favor, não faça isso.

Teremos que bloquear contas que nos enviem repetidamente PRs ou comentários automatizados em excesso.

### Use as Ferramentas com Sabedoria

Como disse o Tio Ben:

<blockquote>
Com grandes <strike>poderes</strike> <strong>ferramentas</strong> vem grande responsabilidade.
</blockquote>

Evite causar danos inadvertidamente.

Você tem ferramentas incríveis à sua disposição, use-as com sabedoria para ajudar de forma eficaz.