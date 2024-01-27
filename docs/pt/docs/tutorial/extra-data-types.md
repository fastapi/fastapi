# Tipos de dados extras

Até agora, você tem usado tipos de dados comuns, tais como:

* `int`
* `float`
* `str`
* `bool`

Mas você também pode usar tipos de dados mais complexos.

E você ainda terá os mesmos recursos que viu até agora:

* Ótimo suporte do editor.
* Conversão de dados das requisições recebidas.
* Conversão de dados para os dados da resposta.
* Validação de dados.
* Anotação e documentação automáticas.

## Outros tipos de dados

Aqui estão alguns dos tipos de dados adicionais que você pode usar:

* `UUID`:
    * Um "Identificador Universalmente Único" padrão, comumente usado como ID em muitos bancos de dados e sistemas.
    * Em requisições e respostas será representado como uma `str`.
* `datetime.datetime`:
    * O `datetime.datetime` do Python.
    * Em requisições e respostas será representado como uma `str` no formato ISO 8601, exemplo: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * O `datetime.date` do Python.
    * Em requisições e respostas será representado como uma `str` no formato ISO 8601, exemplo: `2008-09-15`.
* `datetime.time`:
    * O `datetime.time` do Python.
    * Em requisições e respostas será representado como uma `str` no formato ISO 8601, exemplo: `14:23:55.003`.
* `datetime.timedelta`:
    * O `datetime.timedelta` do Python.
    * Em requisições e respostas será representado como um `float` de segundos totais.
    * O Pydantic também permite representá-lo como uma "codificação ISO 8601 diferença de tempo", <a href="https://pydantic-docs.helpmanual.io/#json-serialisation" class="external-link" target="_blank">cheque a documentação para mais informações</a>.
* `frozenset`:
    * Em requisições e respostas, será tratado da mesma forma que um `set`:
        * Nas requisições, uma lista será lida, eliminando duplicadas e convertendo-a em um `set`.
        * Nas respostas, o `set` será convertido para uma `list`.
        * O esquema gerado vai especificar que os valores do `set` são unicos (usando o `uniqueItems` do JSON Schema).
* `bytes`:
    * O `bytes` padrão do Python.
    * Em requisições e respostas será representado como uma `str`.
    * O esquema gerado vai especificar que é uma `str` com o "formato" `binary`.
* `Decimal`:
    * O `Decimal` padrão do Python.
    * Em requisições e respostas será representado como um `float`.
* Você pode checar todos os tipos de dados válidos do Pydantic aqui: <a href="https://pydantic-docs.helpmanual.io/usage/types" class="external-link" target="_blank">Tipos de dados do Pydantic</a>.

## Exemplo

Aqui está um exemplo de *operação de rota* com parâmetros utilizando-se de alguns dos tipos acima.

```Python hl_lines="1  3  12-16"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```

Note que os parâmetros dentro da função tem seu tipo de dados natural, e você pode, por exemplo, realizar manipulações normais de data, como:

```Python hl_lines="18-19"
{!../../../docs_src/extra_data_types/tutorial001.py!}
```
