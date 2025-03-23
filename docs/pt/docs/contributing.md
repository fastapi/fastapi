# Desenvolvimento - Contribuindo

Primeiro, você poderá querer ver as formas básicas de [ajudar o FastAPI e obter ajuda](help-fast-api.md){.internal-link target=_blank}. 

## Desenvolvimento

Se você já clonou o <a href="https://github.com/fastapi/fastapi" class="external-link" target="_blank">repositório fastapi</a> e quer mergulhar fundo no código, aqui estão algumas orientações para configurar o seu ambiente.

### Ambiente virtual

Siga as instruções para criar e ativar um [ambiente virtual](virtual-environments.md){.internal-link target=_blank} para o código interno do `fastapi`.

### Instalar requisitos usando o pip

Depois de ativar o ambiente, instale os pacotes necessários:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

Isso vai instalar todas as dependências e seu FastAPI local no seu ambiente local.

### Usando seu FastAPI local

Se criou um arquivo Python que importe e use o FastAPI, e o executa com o Python em seu ambiente local, ele irá usar o código fonte do seu FastAPI local clonado.

E se atualizar o código fonte local do FastAPI quando voltar a executar o arquivo Python, ele utilizará a nova versão do FastAPI que acabou de editar.

Desta forma, você não tem que "instalar" sua versão local para poder testar todas as alterações.

/// note | Detalhe técnicos

Isso só acontece quando você instala usando o `requirements.txt` ao invés de executar `pip install fastapi` diretamente.

Isso acontece porque dentro do arquivo `requirements.txt`, a versão local do FastAPI está marcada para ser instalada em modo "editável", com a opção `-e`.

///

### Formatar o código

Existe um script que você pode executar para formatar e limpar todo o seu código:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

Também classifica automaticamente todas as suas importações.

## Testes

Existe um script que pode ser executado localmente para testar todo o código e gerar relatórios de cobertura em HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

Esse comando gera um diretório `./htmlcov/`, se você abrir o arquivo `./htmlcov/index.html` em seu navegador, você pode explorar interativamente as regiões de código que são cobertas pelos testes, e avisam se falta alguma região.

## Documentação

Primeiro, certifique-se de configurar seu ambiente como descrito acima, que instalará todos os requisitos.

### Documentação em tempo real

Durante o desenvolvimento local, existe um script que constrói o site e verifica se existem alterações, ou seja, live-reloading:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

A documentação será mostrada em `http://127.0.0.1:8008`.

Desse modo, você pode editar os arquivos da documentação/fonte e ver as alterações em tempo real.

/// tip | Dica

Alternativamente, você pode executar os mesmos passos que os scripts fazem manualmente.

Vá para a pasta do idioma, para os documentos principais em inglês, estão em `docs/en`:

```console
$ cd docs/en/
```

Então execute `mkdocs` nesse diretório:

```console
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

///

#### Typer CLI (opcional)

As instruções aqui mostram como usar o script `./scripts/docs.py` com o programa `python` diretamente.

Mas você também pode usar o <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, e obterá o preenchimento automático dos comandos no seu terminal após a instalação completa.

Se instalar o Typer CLI, você pode instalar o completion com:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Estrutura dos documentos

A documentação usa o <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

E existem ferramentas/scripts adicionais para lidar com traduções em `./scripts/docs.py`.

/// tip | Dica

Não é preciso ver o código em `./scripts/docs.py`, basta usá-lo na linha de comando.

///


Toda a documentação está no formato Markdown no diretório `./docs/en/`

Muitos dos tutoriais têm blocos de código.

Na maioria dos casos, estes blocos de código são verdadeiras aplicações completas que podem ser executadas como estão.

Na verdade, esses blocos de código não estão escritos dentro do Markdown, eles são arquivos Python no diretório `./docs_src/`.

E esses arquivos Python são incluídos/injetados na documentação quando gera o site.

### Documentos para testes

A maioria dos testes é executada com base nos arquivos de exemplo da documentação.

Isso ajuda a garantir que:

* A documentação está atualizada.
* Os exemplos da documentação podem ser executados como estão.
* A maioria das funcionalidades são cobertas pela documentação, garantidas pelo teste de cobertura. 

#### Aplicações e documentação ao mesmo tempo

Se executar os exemplos com, por exemplo:

<div class="termy">

```console
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

como o Uvicorn por padrão usa a porta `8000`, a documentação na porta `8008` não vai colidir.

### Traduções

A ajuda com as traduções é MUITO apreciada! E isso não pode ser feito sem a ajuda da comunidade. 🌎🚀

Aqui estão os passos para ajudar com as traduções

#### Dicas e orientações

* Verifique os <a href="https://github.com/fastapi/fastapi/pulls" class="external-link" target="_blank">pull requests existentes </a> para o seu idioma. Por exemplo, para Espanhol, a label é <a href="https://github.com/fastapi/fastapi/pulls?q=is%3Aopen+sort%3Aupdated-desc+label%3Alang-es+label%3Aawaiting-review" class="external-link" target="_blank">`lang-es`</a>.

* Revise esses pull requests, solicitando modificações ou aprovando eles. Para os idiomas que não falo, espero que outras pessoas revisem a tradução antes do merging.

/// tip | Dica

É possível <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request" class="external-link" target="_blank">adicionar comentários com sugestões de alteração</a> para pull requests existentes.

Verifique os documentos sobre como <a href="https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews" class="external-link" target="_blank">adicionar uma revisão de pull request</a> para aprová-la ou solicitar alterações.

///

* Verifique se existe uma <a href="https://github.com/fastapi/fastapi/discussions/categories/translations" class="external-link" target="_blank">GitHub Discussion</a> para coordenar traduções para o seu idioma. Pode subscrevê-lo, e quando houver um novo pull request para revisão, um comentário automático será adicionado à discussão.

* Se traduzir páginas, adicione um único pull request por página traduzida. Isso fará com que seja muito mais fácil para os outros revisarem.

* Para revisar o código de 2-letras do idioma que quer traduzir, pode usar a tabela <a href="https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" class="external-link" target="_blank">Lista de códigos ISO 639-1</a>.

#### Idiomas existentes

Digamos que quer traduzir uma página para um idioma que já tem traduções para algumas páginas, como Espanhol.

Nesse caso do Espanhol, o código de 2-letras é `es`. Então, o diretório para as traduções em espanhol está localizado em `docs/es/`.

/// tip | Dica

O idioma principal (oficial) é o Inglês, localizado em `docs/en`.

///

Agora, execute o live server para os documentoes em Espanhol.

<div class="termy">

```console
// Use o comando "live" e passe o código do idioma como argumento CLI
$ python ./scripts/docs.py live es

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

/// tip | Dica

Como alternativa, você pode executar os mesmos passos que os scripts fazem manualmente.

Vá para o diretório do idioma, para traduções em Espanhol está em `docs/es`:

```console
$ cd docs/es/
```

Em seguida, execute `mkdocs` nesse diretório:
Then run `mkdocs` in that directory:

```console
$ mkdocs serve --dev-addr 127.0.0.1:8008
```

///

Agora vá para <a href="http://127.0.0.1:8008" class="external-link" target="_blank">http://127.0.0.1:8008</a> e veja suas alterações em tempo real.

Você verá que todos os idiomas têm todas as páginas. Mas algumas páginas não estão traduzidas e têm uma caixa de informação no topo, sobre a tradução em falta.

Agora, digamos que você quer adicionar uma tradução para a seção [Features](features.md){.internal-link target=_blank}.

* Copie o arquivo em:

```
docs/en/docs/features.md
```

* Cole-o exatamente no mesmo local mas para o idioma que pretende traduzir, por exemplo:

```
docs/es/docs/features.md
```

/// tip | Dica

Note que a única alteração no caminho e o nome do arquivo é o código do idioma, de `en` para `es`.


///

Se for ao seu navegador verá que agora os documentos mostram a sua nova seção (a caixa de informação no topo desapareceu). 🎉

Agora pode traduzir tudo e ver como fica quando salvar o arquivo.


#### Não traduza essas páginas

🚨 Não traduza:

* Arquivos em `reference/`
* `release-notes.md`
* `fastapi-people.md`
* `external-links.md`
* `newsletter.md`
* `management-tasks.md`
* `management.md`
* `contributing.md`

Alguns desses arquivos são atualizados com muita frequência e uma tradução estaria sempre atrasada, ou incluem o conteúdo principal dos arquivos fonte do Inglês, etc.

#### Novo Idioma

Digamos que quer adicionar traduções para um idioma que ainda não está traduzida, nem mesmo algumas páginas.

E quer adicioanr traduções para Creole, e ele ainda não está em docs.

Verificando o link abaixo, o código para "Creole" é `ht`.

O próximo passo é executar o script para gerar um novo diretório de tradução:

<div class="termy">

```console
// Use o comando new-lang, passe o código do idioma como argumento CLI
$ python ./scripts/docs.py new-lang ht

Successfully initialized: docs/ht
```

</div>

Agora pode verificar em seu editor de código o novo diretório criado `docs/ht/`.

Esse comando criou um arquivo `docs/ht/mkdocs.yml` com uma configuração simples que herda tudo da versão `en`:

```yaml
INHERIT: ../en/mkdocs.yml
```

/// tip | Dica

Você também pode simplesmente criar esse arquivo com esse conteúdos manualmente.

///

Esse comando também criou um arquivo fictício `docs/ht/index.md` para a página principal, pode começar por traduzir este.

Pode continuar com as intruções anteriores para uma "Idioma Existente" para esse processo.

Você pode fazer o primeiro pull request com esses dois arquivos, `docs/ht/mkdocs.yml` e `docs/ht/index.md`. 🎉


#### Pré-visualizar o resultado

Como já mencionado acima, pode-se usar o `./scripts/docs.py` com o comando `live` para pré-visualizar os resultados (or `mkdocs serve`)

Uma vez pronto, pode também testar tudo como ficaria online, incluindo todos os outros idiomas.

Para fazer isso, comece por construir todos os documentos:

<div class="termy">

```console
// Use o comando "build-all", isto vai demorar um pouco
$ python ./scripts/docs.py build-all

Building docs for: en
Building docs for: es
Successfully built docs for: es
```

</div>

Isso constrói todos os sites MkDocs para cada idioma, combina-os, e gera o resultado final em `./site/`.

Depois, pode servi-lo com o comando `serve`:

<div class="termy">

```console
// Use o comando "serve" depois de executar "build-all"
$ python ./scripts/docs.py serve

Aviso: esse é um um servidor muito simples. Para desenvolvimento, use o mkdocs em vez disso.
Isso está aqui apenas para pré-visualizar um site com traduções já construídas.
Certifique-se de executar o comando build-all primeiro.
Servindo em: http://127.0.0.1:8008  

```

</div>

#### Sugestões e orientações específicas para a tradução

* Traduza apenas os documentos Markdown (`.md`). Não traduza exemplos de código em `./docs_src`.

* Em blocos de código dentro do documento Markdown, traduza os comentários (`# um comentário`), mas deixe o resto inalterado.

* Não altere nada do que está incluído em "``" (código em linha).

* Nas linhas que começam com `///` traduza apenas a parte do text depois de `|`. Deixe o resto inalterado.

* Pode traduzir caixas de informação como `/// warning` como por exemplo `/// warning | Achtung`. Mas não altere a palavra imediatamente após o `///`, pois isso determina a cor da caixa de informação.

* Não altere os caminhos nos links para imagens, arquivos de código, documentos Markdown.

* No entanto, quando um documento Markdown é traduzido os `#hash-parts` em links para os cabeçalhos pode mudar. Atualize esses links se possível.
    * Procure por esses links no documento traduzido usando o regex `#[^# ]`.
    * Procure em todos os documentos já traduzidos para o seu idioma por `your-translated-document.md`. Por exemplo VS Code tem uma opção "Editar" -> "Procurar em Arquivos".
    * Ao traduzir um documento, não "pré-traduza" `#hash-parts` que ligam a títulos em documentos não traduzidos.
