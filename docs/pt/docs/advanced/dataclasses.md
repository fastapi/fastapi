# Usando Dataclasses { #using-dataclasses }

FastAPI é construído em cima do **Pydantic**, e eu tenho mostrado como usar modelos Pydantic para declarar requisições e respostas.

Mas o FastAPI também suporta o uso de <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a> da mesma forma:

{* ../../docs_src/dataclasses/tutorial001.py hl[1,7:12,19:20] *}

Isso ainda é suportado graças ao **Pydantic**, pois ele tem <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">suporte interno para `dataclasses`</a>.

Então, mesmo com o código acima que não usa Pydantic explicitamente, o FastAPI está usando Pydantic para converter essas dataclasses padrão para a versão do Pydantic.

E claro, ele suporta o mesmo:

* validação de dados
* serialização de dados
* documentação de dados, etc.

Isso funciona da mesma forma que com os modelos Pydantic. E na verdade é alcançado da mesma maneira por baixo dos panos, usando Pydantic.

/// info | Informação

Lembre-se de que dataclasses não podem fazer tudo o que os modelos Pydantic podem fazer.

Então, você ainda pode precisar usar modelos Pydantic.

Mas se você tem um monte de dataclasses por aí, este é um truque legal para usá-las para alimentar uma API web usando FastAPI. 🤓

///

## Dataclasses em `response_model` { #dataclasses-in-response-model }

Você também pode usar `dataclasses` no parâmetro `response_model`:

{* ../../docs_src/dataclasses/tutorial002.py hl[1,7:13,19] *}

A dataclass será automaticamente convertida para uma dataclass Pydantic.

Dessa forma, seu esquema aparecerá na interface de documentação da API:

<img src="/img/tutorial/dataclasses/image01.png">

## Dataclasses em Estruturas de Dados Aninhadas { #dataclasses-in-nested-data-structures }

Você também pode combinar `dataclasses` com outras anotações de tipo para criar estruturas de dados aninhadas.

Em alguns casos, você ainda pode ter que usar a versão do Pydantic das `dataclasses`. Por exemplo, se você tiver erros com a documentação da API gerada automaticamente.

Nesse caso, você pode simplesmente trocar as `dataclasses` padrão por `pydantic.dataclasses`, que é um substituto direto:

{* ../../docs_src/dataclasses/tutorial003.py hl[1,5,8:11,14:17,23:25,28] *}

1. Ainda importamos `field` das `dataclasses` padrão.

2. `pydantic.dataclasses` é um substituto direto para `dataclasses`.

3. A dataclass `Author` inclui uma lista de dataclasses `Item`.

4. A dataclass `Author` é usada como o parâmetro `response_model`.

5. Você pode usar outras anotações de tipo padrão com dataclasses como o corpo da requisição.

    Neste caso, é uma lista de dataclasses `Item`.

6. Aqui estamos retornando um dicionário que contém `items`, que é uma lista de dataclasses.

    O FastAPI ainda é capaz de <abbr title="converter os dados para um formato que pode ser transmitido">serializar</abbr> os dados para JSON.

7. Aqui o `response_model` está usando uma anotação de tipo de uma lista de dataclasses `Author`.

    Novamente, você pode combinar `dataclasses` com anotações de tipo padrão.

8. Note que esta *função de operação de rota* usa `def` regular em vez de `async def`.

    Como sempre, no FastAPI você pode combinar `def` e `async def` conforme necessário.

    Se você precisar de uma atualização sobre quando usar qual, confira a seção _"Com pressa?"_ na documentação sobre [`async` e `await`](../async.md#in-a-hurry){.internal-link target=_blank}.

9. Esta *função de operação de rota* não está retornando dataclasses (embora pudesse), mas uma lista de dicionários com dados internos.

    O FastAPI usará o parâmetro `response_model` (que inclui dataclasses) para converter a resposta.

Você pode combinar `dataclasses` com outras anotações de tipo em muitas combinações diferentes para formar estruturas de dados complexas.

Confira as dicas de anotação no código acima para ver mais detalhes específicos.

## Saiba Mais { #learn-more }

Você também pode combinar `dataclasses` com outros modelos Pydantic, herdar deles, incluí-los em seus próprios modelos, etc.

Para saber mais, confira a <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">documentação do Pydantic sobre dataclasses</a>.

## Versão { #version }

Isso está disponível desde a versão `0.67.0` do FastAPI. 🔖
