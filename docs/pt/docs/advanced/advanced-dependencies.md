# Dependências avançadas

## Dependências parametrizadas

Todas as dependências que vimos até agora são funções ou classes fixas.

Mas podem ocorrer casos onde você deseja ser capaz de definir parâmetros na dependência, sem ter a necessidade de declarar diversas funções ou classes.

Vamos imaginar que queremos ter uma dependência que verifica se o parâmetro de consulta `q` possui um valor fixo.

Porém nós queremos poder parametrizar o conteúdo fixo.

## Uma instância "chamável"

Em Python existe uma maneira de fazer com que uma instância de uma classe seja um "chamável".

Não propriamente a classe (que já é um chamável), mas a instância desta classe.

Para fazer isso, nós declaramos o método `__call__`:

//// tab | Python 3.9+

```Python hl_lines="12"
{!> ../../../docs_src/dependencies/tutorial011_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11"
{!> ../../../docs_src/dependencies/tutorial011_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="10"
{!> ../../../docs_src/dependencies/tutorial011.py!}
```

////

Neste caso, o `__call__` é o que o **FastAPI** utilizará para verificar parâmetros adicionais e sub dependências, e isso é o que será chamado para passar o valor ao parâmetro na sua *função de operação de rota* posteriormente.

## Parametrizar a instância

E agora, nós podemos utilizar o `__init__` para declarar os parâmetros da instância que podemos utilizar para "parametrizar" a dependência:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/dependencies/tutorial011_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/dependencies/tutorial011_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="7"
{!> ../../../docs_src/dependencies/tutorial011.py!}
```

////

Neste caso, o **FastAPI** nunca tocará ou se importará com o `__init__`, nós vamos utilizar diretamente em nosso código.

## Crie uma instância

Nós poderíamos criar uma instância desta classe com:

//// tab | Python 3.9+

```Python hl_lines="18"
{!> ../../../docs_src/dependencies/tutorial011_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="17"
{!> ../../../docs_src/dependencies/tutorial011_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="16"
{!> ../../../docs_src/dependencies/tutorial011.py!}
```

////

E deste modo nós podemos "parametrizar" a nossa dependência, que agora possui `"bar"` dentro dele, como o atributo `checker.fixed_content`.

## Utilize a instância como dependência

Então, nós podemos utilizar este `checker` em um `Depends(checker)`, no lugar de `Depends(FixedContentQueryChecker)`, porque a dependência é a instância, `checker`, e não a própria classe.

E quando a dependência for resolvida, o **FastAPI** chamará este `checker` como:

```Python
checker(q="somequery")
```

...e passar o que quer que isso retorne como valor da dependência em nossa *função de operação de rota* como o parâmetro `fixed_content_included`:

//// tab | Python 3.9+

```Python hl_lines="22"
{!> ../../../docs_src/dependencies/tutorial011_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="21"
{!> ../../../docs_src/dependencies/tutorial011_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="20"
{!> ../../../docs_src/dependencies/tutorial011.py!}
```

////

/// tip | "Dica"

Tudo isso parece não ser natural. E pode não estar muito claro ou aparentar ser útil ainda.

Estes exemplos são intencionalmente simples, porém mostram como tudo funciona.

Nos capítulos sobre segurança, existem funções utilitárias que são implementadas desta maneira.

Se você entendeu tudo isso, você já sabe como essas funções utilitárias para segurança funcionam por debaixo dos panos.

///
