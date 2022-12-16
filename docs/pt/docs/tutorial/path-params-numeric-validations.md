# Parâmetros da Rota e Validações Numéricas

Do mesmo modo que você pode declarar mais validações e metadados para parâmetros de consulta com `Query`, você pode declarar os mesmos tipos de validações e metadados para parâmetros de rota com `Path`.

## Importe `Path`

Primeiro, importe `Path` de `fastapi`:

=== "Python 3.6 e superiores"

    ```Python hl_lines="3"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="1"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

## Declare metadados

Você pode declarar todos os parâmetros da mesma maneira que na `Query`.

Por exemplo para declarar um valor de metadado `title` para o parâmetro de rota `item_id` você pode digitar:

=== "Python 3.6 e superiores"

    ```Python hl_lines="10"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001.py!}
    ```

=== "Python 3.10 e superiores"

    ```Python hl_lines="8"
    {!> ../../../docs_src/path_params_numeric_validations/tutorial001_py310.py!}
    ```

!!! note "Nota"
    Um parâmetro de rota é sempre obrigatório, como se fizesse parte da rota.

    Então, você deve declará-lo com `...` para marcá-lo como obrigatório.

    Mesmo que você declare-o como `None` ou defina um valor padrão, isso não teria efeito algum, o parâmetro ainda seria obrigatório.

## Ordene os parâmetros de acordo com sua necessidade

Suponha que você queira declarar o parâmetro de consulta `q` como uma `str` obrigatória.

E você não precisa declarar mais nada em relação a este parâmetro, então você não precisa necessariamente usar `Query`.

Mas você ainda precisa usar `Path` para o parâmetro de rota `item_id`.

O Python irá acusar se você colocar um elemento com um valor padrão definido antes de outro que não tenha um valor padrão.

Mas você pode reordená-los, colocando primeiro o elemento sem o valor padrão (o parâmetro de consulta `q`).

Isso não faz diferença para o **FastAPI**. Ele vai detectar os parâmetros pelos seus nomes, tipos e definições padrão (`Query`, `Path`, etc), sem se importar com a ordem.

Então, você pode declarar sua função assim:

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## Ordene os parâmetros de a acordo com sua necessidade, truques

Se você quiser declarar o parâmetro de consulta `q` sem um `Query` nem um valor padrão, e o parâmetro de rota `item_id` usando `Path`, e definí-los em uma ordem diferente, Python tem um pequeno truque na sintaxe para isso.

Passe `*`, como o primeiro parâmetro da função.

O Python não vai fazer nada com esse `*`, mas ele vai saber que a partir dali os parâmetros seguintes deverão ser chamados argumentos nomeados (pares chave-valor), também conhecidos como <abbr title="Do inglês: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Mesmo que eles não possuam um valor padrão.

```Python hl_lines="7"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## Validações numéricas: maior que ou igual

Com `Query` e `Path` (e outras que você verá mais tarde) você pode declarar restrições numéricas.

Aqui, com `ge=1`, `item_id` precisará ser um número inteiro maior que ("`g`reater than") ou igual ("`e`qual") a 1.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## Validações numéricas: maior que e menor que ou igual

O mesmo se aplica para:

* `gt`: maior que (`g`reater `t`han)
* `le`: menor que ou igual (`l`ess than or `e`qual)

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## Validações numéricas: valores do tipo float, maior que e menor que

Validações numéricas também funcionam para valores do tipo `float`.

Aqui é onde se torna importante a possibilidade de declarar <abbr title="greater than"><code>gt</code></abbr> e não apenas <abbr title="greater than or equal"><code>ge</code></abbr>. Com isso você pode especificar, por exemplo, que um valor deve ser maior que `0`, ainda que seja menor que `1`.

Assim, `0.5` seria um valor válido. Mas `0.0` ou `0` não seria.

E o mesmo para <abbr title="less than"><code>lt</code></abbr>.

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## Recapitulando

Com `Query`, `Path` (e outras que você ainda não viu) você pode declarar metadados e validações de texto do mesmo modo que com [Parâmetros de consulta e validações de texto](query-params-str-validations.md){.internal-link target=_blank}.

E você também pode declarar validações numéricas:

* `gt`: maior que (`g`reater `t`han)
* `ge`: maior que ou igual (`g`reater than or `e`qual)
* `lt`: menor que (`l`ess `t`han)
* `le`: menor que ou igual (`l`ess than or `e`qual)

!!! info "Informação"
    `Query`, `Path` e outras classes que você verá a frente são subclasses de uma classe comum `Param`.

    Todas elas compartilham os mesmos parâmetros para validação adicional e metadados que você viu.

!!! note "Detalhes Técnicos"
    Quando você importa `Query`, `Path` e outras de `fastapi`, elas são na verdade funções.

    Que quando chamadas, retornam instâncias de classes de mesmo nome.

    Então, você importa `Query`, que é uma função. E quando você a chama, ela retorna uma instância de uma classe também chamada `Query`.

    Estas funções são assim (ao invés de apenas usar as classes diretamente) para que seu editor não acuse erros sobre seus tipos.

    Dessa maneira você pode user seu editor e ferramentas de desenvolvimento sem precisar adicionar configurações customizadas para ignorar estes erros.
