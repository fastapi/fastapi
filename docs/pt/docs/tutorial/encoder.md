# Codificador Compatível com JSON

Existem alguns casos em que você pode precisar converter um tipo de dados (como um modelo Pydantic) para algo compatível com JSON (como um `dict`, `list`, etc).

Por exemplo, se você precisar armazená-lo em um banco de dados.

Para isso, **FastAPI** fornece uma função `jsonable_encoder()`.

## Usando a função `jsonable_encoder`

Vamos imaginar que você tenha um banco de dados `fake_db` que recebe apenas dados compatíveis com JSON.

Por exemplo, ele não recebe objetos `datetime`, pois estes objetos não são compatíveis com JSON.

Então, um objeto `datetime` teria que ser convertido em um `str` contendo os dados no formato  <a href="https://en.wikipedia.org/wiki/ISO_8601" class="external-link" target="_blank">ISO</a>.

Da mesma forma, este banco de dados não receberia um modelo Pydantic (um objeto com atributos), apenas um `dict`.

Você pode usar a função `jsonable_encoder` para resolver isso.

A função recebe um objeto, como um modelo Pydantic e retorna uma versão compatível com JSON:

=== "Python 3.10+"

    ```Python hl_lines="4  21"
    {!> ../../../docs_src/encoder/tutorial001_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="5  22"
    {!> ../../../docs_src/encoder/tutorial001.py!}
    ```

Neste exemplo, ele converteria o modelo Pydantic em um `dict`, e o `datetime` em um `str`.

O resultado de chamar a função é algo que pode ser codificado com o padrão do Python <a href="https://docs.python.org/3/library/json.html#json.dumps" class="external-link" target="_blank">`json.dumps()`</a>.

A função não retorna um grande `str` contendo os dados no formato JSON (como uma string). Mas sim, retorna uma estrutura de dados padrão do Python (por exemplo, um `dict`) com valores e subvalores compatíveis com JSON.

!!! nota
    `jsonable_encoder` é realmente usado pelo **FastAPI** internamente para converter dados. Mas também é útil em muitos outros cenários.
