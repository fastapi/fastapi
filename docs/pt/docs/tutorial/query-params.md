# Parâmetros de Consulta { #query-parameters }

Quando você declara outros parâmetros na função que não fazem parte dos parâmetros da rota, esses parâmetros são automaticamente interpretados como parâmetros de "consulta".

{* ../../docs_src/query_params/tutorial001.py hl[9] *}

A consulta é o conjunto de pares chave-valor que vai depois de `?` na URL, separado pelo caractere `&`.

Por exemplo, na URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...os parâmetros da consulta são:

* `skip`: com o valor `0`
* `limit`: com o valor `10`

Como eles são parte da URL, eles são "naturalmente" strings.

Mas quando você declara eles com os tipos do Python (no exemplo acima, como `int`), eles são convertidos para aquele tipo e validados em relação a ele.

Todo o processo que era aplicado para parâmetros de rota também é aplicado para parâmetros de consulta:

* Suporte do editor (obviamente)
* <abbr title="convertendo uma string que vem de um request HTTP em um dado Python">"Parsing"</abbr> de dados
* Validação de dados
* Documentação automática

## Valores padrão { #defaults }

Como os parâmetros de consulta não são uma parte fixa da rota, eles podem ser opcionais e podem ter valores padrão.

No exemplo acima eles tem valores padrão de `skip=0` e `limit=10`.

Então, se você for até a URL:

```
http://127.0.0.1:8000/items/
```

Seria o mesmo que ir para:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

Mas, se por exemplo você for para:

```
http://127.0.0.1:8000/items/?skip=20
```

Os valores dos parâmetros na sua função serão:

* `skip=20`: Por que você definiu isso na URL
* `limit=10`: Por que esse era o valor padrão

## Parâmetros opcionais { #optional-parameters }

Da mesma forma, você pode declarar parâmetros de consulta opcionais, definindo o valor padrão para `None`:

{* ../../docs_src/query_params/tutorial002_py310.py hl[7] *}

Nesse caso, o parâmetro da função `q` será opcional, e `None` será o padrão.

/// check | Verifique

Você também pode notar que o **FastAPI** é esperto o suficiente para perceber que o parâmetro da rota `item_id` é um parâmetro da rota, e `q` não é, portanto, `q` é o parâmetro de consulta.

///

## Conversão dos tipos de parâmetros de consulta { #query-parameter-type-conversion }

Você também pode declarar tipos `bool`, e eles serão convertidos:

{* ../../docs_src/query_params/tutorial003_py310.py hl[7] *}

Nesse caso, se você for para:

```
http://127.0.0.1:8000/items/foo?short=1
```

ou

```
http://127.0.0.1:8000/items/foo?short=True
```

ou

```
http://127.0.0.1:8000/items/foo?short=true
```

ou

```
http://127.0.0.1:8000/items/foo?short=on
```

ou

```
http://127.0.0.1:8000/items/foo?short=yes
```

ou qualquer outra variação (tudo em maiúscula, primeira letra em maiúscula, etc), a sua função vai ver o parâmetro `short` com um valor `bool` de `True`. Caso contrário `False`.

## Múltiplos parâmetros de rota e consulta { #multiple-path-and-query-parameters }

Você pode declarar múltiplos parâmetros de rota e parâmetros de consulta ao mesmo tempo, o **FastAPI** vai saber o quê é o quê.

E você não precisa declarar eles em nenhuma ordem específica.

Eles serão detectados pelo nome:

{* ../../docs_src/query_params/tutorial004_py310.py hl[6,8] *}

## Parâmetros de consulta obrigatórios { #required-query-parameters }

Quando você declara um valor padrão para parâmetros que não são de rota (até agora, nós vimos apenas parâmetros de consulta), então eles não são obrigatórios.

Caso você não queira adicionar um valor específico mas queira apenas torná-lo opcional, defina o valor padrão como `None`.

Porém, quando você quiser fazer com que o parâmetro de consulta seja obrigatório, você pode simplesmente não declarar nenhum valor como padrão.

{* ../../docs_src/query_params/tutorial005.py hl[6:7] *}

Aqui o parâmetro de consulta `needy` é um valor obrigatório, do tipo `str`.

Se você abrir no seu navegador a URL:

```
http://127.0.0.1:8000/items/foo-item
```

... sem adicionar o parâmetro obrigatório `needy`, você verá um erro como:

```JSON
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "needy"
      ],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

Como `needy` é um parâmetro obrigatório, você precisaria defini-lo na URL:

```
http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
```

...isso deve funcionar:

```JSON
{
    "item_id": "foo-item",
    "needy": "sooooneedy"
}
```

E claro, você pode definir alguns parâmetros como obrigatórios, alguns possuindo um valor padrão, e outros sendo totalmente opcionais:

{* ../../docs_src/query_params/tutorial006_py310.py hl[8] *}

Nesse caso, existem 3 parâmetros de consulta:

* `needy`, um `str` obrigatório.
* `skip`, um `int` com o valor padrão `0`.
* `limit`, um `int` opcional.

/// tip | Dica

Você também poderia usar `Enum` da mesma forma que com [Path Parameters](path-params.md#predefined-values){.internal-link target=_blank}.

///
