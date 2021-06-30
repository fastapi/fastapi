# Body - Fields

Da mesma forma que voĉe pode declarar uma validação adicional e metadados nas *funções de operação de rota* com `Query`, `Path` e `Body`, você também pode declarar validações e metadados dentro dos modelos Pydantic usando `Field` do Pydantic.

## Importe `Field`

Primeiro, você tem que importar isso:

```Python hl_lines="4"
{!../../../docs_src/body_fields/tutorial001.py!}
```

!!! Atenção
    Observe que `Field` é importado diretamente de `pydantic`, não de `fastapi` como todo o resto (`Query`, `Path`, `Body`, etc.).

## Declarar atributos de modelo

Você pode então usar `Field` com atributos de modelo:

```Python hl_lines="11-14"
{!../../../docs_src/body_fields/tutorial001.py!}
```

`Field` funciona da mesma maneira que `Query`, `Path` e `Body`, todos tem os mesmos parâmetros, etc.

!!! Nota "Detalhes Técnicos" você irá vê a seguir 
    Na verdade, `Query`, `Path` e outros você verá a seguir criar objetos de subclasses de uma classe `Param`, que é uma subclasses da classe `FieldInfo` de Pydanctic. 

    E o `Field` do Pydantic irá retornar uma instância de `FieldInfo` também.

    `Body` também retorna um objetio da subsclasse `FieldInfo` diretamente. E há outras que você verá mais tarde que são subsclasses da classe `Body`.

    Lembre-se que quando importa `Query`, `Path`, e outros de `fastapi`, esses são, na verdade, funções que retornam classes especiais.

!!! Dica
    Observe como cada atributo de modelo com um tipo, valor padrão e `Field` tem a mesma estrutura que os parametros de *funções de operação de caminho*, com `Field` em vez de `Path`, `Query` e `Body`.

## Adicionar informações extras

Você pode declarar informações extras em `Field`, `Query`, `Body`, etc. E serão incluidas na geração do JSON Schema.

Você aprenderá mais sobre adicionar informações extra posteriormente na documentação, ao aprender a declarar exemplos.

## Recapitulando

Você pode usar `Field` do Pydantic para declarar validações extras e metadata para atributos de modelo.

Você também pode usar os argumentos de palavra-chave extra para passar metadata JSON Schema.
