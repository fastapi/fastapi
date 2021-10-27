# Parâmetros da Rota e Validações Numéricas

Do mesmo modo que você pode declarar mais validações e metadados para parâmetros de consulta com `Query`, você pode declarar os mesmos tipos de validações e metadados para parâmetros de rota com `Path`.

## Importe `Path`

Primeiro, importe `Path` de `fastapi`:

```Python hl_lines="3"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

## Declare metadados

Você pode declarar todos os parâmetros da mesma maneira que na `Query`.

Por exemplo para declarar um valor de metadado `title` para o parâmetro de rota `item_id` você pode digitar:

```Python hl_lines="10"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

!!! nota
    Um parâmetro de rota é sempre obrigatório como se fosse parte da rota.
    
    Logo, você deve declará-lo com `...` para marcá-lo como obrigatório.

    Mesmo que você declare-o como `None` ou defina um valor padrão, isso não teria efeito algum, o parâmetro ainda seria obrigatório.

## Ordene os parâmetros de a acordo com sua necessidade

Suponha que você quer declarar o parâmetro de consulta `q` como uma `str` obrigatória.

E você não precisa declarar mais nada em relação a este parâmetro, então você não precisa necessariamente usar `Query`.

Mas você ainda precisa usar `Path` para o parâmetro de rota `item_id`.

O Python vai acusar se você colocar um elemento com um valor padrão definido antes de outro que não tenha um valor padrão.

Mas você pode reordená-los, colocando primeiro o elemento sem o valor padrão (o parâmetro de consulta `q`).

Isso não faz diferença para o **FastAPI**. Ele vai detectar os parâmetros pelos seus nomes, tipos e definições padrão (`Query`, `Path`, etc), sem se importar com a ordem.

Então, você pode declarar sua função assim:

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## Ordene os parâmetros de a acordo com sua necessidade, dicas

If you want to declare the `q` query parameter without a `Query` nor any default value, and the path parameter `item_id` using `Path`, and have them in a different order, Python has a little special syntax for that.

Pass `*`, as the first parameter of the function.

Python won't do anything with that `*`, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as <abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Even if they don't have a default value.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## Number validations: greater than or equal

With `Query` and `Path` (and other's you'll see later) you can declare string constraints, but also number constraints.

Here, with `ge=1`, `item_id` will need to be an integer number "`g`reater than or `e`qual" to `1`.

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## Number validations: greater than and less than or equal

The same applies for:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## Number validations: floats, greater than and less than

Number validations also work for `float` values.

Here's where it becomes important to be able to declare <abbr title="greater than"><code>gt</code></abbr> and not just <abbr title="greater than or equal"><code>ge</code></abbr>. As with it you can require, for example, that a value must be greater than `0`, even if it is less than `1`.

So, `0.5` would be a valid value. But `0.0` or `0` would not.

And the same for <abbr title="less than"><code>lt</code></abbr>.

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## Recap

With `Query`, `Path` (and others you haven't seen yet) you can declare metadata and string validations in the same ways as with [Query Parameters and String Validations](query-params-str-validations.md){.internal-link target=_blank}.

And you can also declare numeric validations:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

!!! info
    `Query`, `Path`, and others you will see later are subclasses of a common `Param` class (that you don't need to use).

    And all of them share the same all these same parameters of additional validation and metadata you have seen.

!!! note "Technical Details"
    When you import `Query`, `Path` and others from `fastapi`, they are actually functions.

    That when called, return instances of classes of the same name.

    So, you import `Query`, which is a function. And when you call it, it returns an instance of a class also named `Query`.

    These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about their types.

    That way you can use your normal editor and coding tools without having to add custom configurations to disregard those errors.
