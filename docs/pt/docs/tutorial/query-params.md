# Parâmetros de Consulta

Quando você declara outros parâmetros na função que não fazem parte dos parâmetros da rota, esses parâmetros são automaticamente interpretados como parâmetros de "consulta".

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial001.py!}
```

A consulta é o conjunto de pares chave/valor que vai depois de `?` na URL, separada pelo caractere `&`.

Por exemplo, na URL:

```
http://127.0.0.1:8000/items/?skip=0&limit=10
```

...os parâmetros da consulta são:

* `skip`: com valor de `0`
* `limit`: com valor de `10`

Como eles são parte da URL, eles são "naturalmente" strings.

Mas quando você declara eles com os tipos do Python (no exemplo acima, como `int`), eles são convertidos para aquele tipo e validados contra ele.

Todo o processo que era aplicado para parâmetros de rota também é aplicado para parâmetros de consulta:

* Suporte do editor (obviamente)
* <abbr title="convertendo uma string que vem de um HTTP request em um dado Python">"Parsing"</abbr> de dados
* Validação de dados
* Documentação automática

## Configurações padrão

Como os parâmetros de consulta não são uma parte fixa da rota, eles podem ser opcionais e podem ter valores padrões.

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

Os valores do parâmetro na sua função serão:

* `skip=20`: Por que você definiu isso na URL
* `limit=10`: Por que esse era o valor padrão

## Parâmetros opcionais

Da mesma forma, você pode declarar parâmetros de consulta opcionais definindo o valor padrão para `None`:

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial002.py!}
```

Nesse caso, o parâmetro da função `q` será opcional, e `None` será o padrão.

!!! Verifique
    Você também pode notar que o **FastAPI** é esperto o suficiente para perceber que o parâmetro da rota `item_id` é um parâmetro da rota, e `q` não é, no caso `q` é o parâmetro da consulta.

!!! Observação
    O FastAPI vai saber que `q` é opcional justamente pelo valor `= None`.

    O `Optional` em `Optional[str]` não é usado pelo FastAPI (o FastAPI vai usar somente a parte `str`), mas o `Optional[str]` vai deixar o seu editor ajudar a achar erros no seu código.

## Conversão dos tipos de parâmetros de consulta

Você também pode declarar tipos `bool`, e eles serão convertidos:

```Python hl_lines="9"
{!../../../docs_src/query_params/tutorial003.py!}
```

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

## Múltiplos parâmetros de rota e consulta

Você pode declarar múltiplos parâmetros de rota e parâmetros de consulta ao mesmo tempo, o **FastAPI** vai saber o quê é o quê.

E você não precisa declarar eles em nenhuma ordem específica.

Eles serão detectados pelo nome:

```Python hl_lines="8  10"
{!../../../docs_src/query_params/tutorial004.py!}
```

## Parâmetros de consulta obrigatórios

Quando você declara um valor padrão para parâmetros sem rota (até agora, nós vimos apenas parâmetros de consultas), então isso não é obrigatório.

Caso você não queira adicionar um valor específico mas queira deixar esse valor apenas como opcional, defina o valor padrão como `None`.

Porém, quando você quiser fazer que o parâmetro de consulta seja obrigatório, você pode simplesmente não declarar nenhum valor como padrão.

```Python hl_lines="6-7"
{!../../../docs_src/query_params/tutorial005.py!}
```

Aqui o parâmetro de consulta `needy` é um valor obrigatório, do tipo `str`.

Se você abrir no seu navegador a URL:

```
http://127.0.0.1:8000/items/foo-item
```

... sem adicionar o parâmetro obrigatório `needy`, você verá um erro assim:

```JSON
{
    "detail": [
        {
            "loc": [
                "query",
                "needy"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

Como `needy` é um parâmetro obrigatório, você vai precisar definir ele na URL:

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

E claro, você pode definir alguns parâmetros como obrigatórios, alguns como sendo padrão, e outros sendo totalmente opcionais:

```Python hl_lines="10"
{!../../../docs_src/query_params/tutorial006.py!}
```

Nesse caso, existem 3 parâmetros de consulta:

* `needy`, um `str` obrigatório.
* `skip`, um `int` com um valor padrão sendo `0`.
* `limit`, um `int` opcional.

!!! Dica
    Você também poderia usar `Enum` da mesma forma que com [Path Parameters](path-params.md#predefined-values){.internal-link target=_blank}.
