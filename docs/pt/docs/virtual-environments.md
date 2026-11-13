# Ambientes Virtuais { #virtual-environments }

Ao trabalhar com projetos Python, você deveria usar um **ambiente virtual** para isolar os pacotes instalados para cada projeto.

Para projetos FastAPI, recomendo usar [uv](https://docs.astral.sh/uv/) para gerenciar o projeto, suas dependências e seu ambiente virtual.

## Crie um Projeto { #create-a-project }

Instale `uv` usando o [guia oficial de instalação](https://docs.astral.sh/uv/getting-started/installation/) e então crie um projeto:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv` cria um ambiente virtual para o projeto automaticamente. Você não precisa criar ou ativar um por conta própria.

Execute comandos dentro do ambiente do projeto com `uv run`, por exemplo:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## Saiba Mais { #learn-more }

Leia o [guia de Ambientes Virtuais](https://tiangolo.com/guides/virtual-environments/) para aprender como ambientes virtuais funcionam por baixo, incluindo ativação e o fluxo de trabalho alternativo com `python -m venv` e `pip`.
