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

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[12] *}

Neste caso, o `__call__` é o que o **FastAPI** utilizará para verificar parâmetros adicionais e sub dependências, e isso é o que será chamado para passar o valor ao parâmetro na sua *função de operação de rota* posteriormente.

## Parametrizar a instância

E agora, nós podemos utilizar o `__init__` para declarar os parâmetros da instância que podemos utilizar para "parametrizar" a dependência:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[9] *}

Neste caso, o **FastAPI** nunca tocará ou se importará com o `__init__`, nós vamos utilizar diretamente em nosso código.

## Crie uma instância

Nós poderíamos criar uma instância desta classe com:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[18] *}

E deste modo nós podemos "parametrizar" a nossa dependência, que agora possui `"bar"` dentro dele, como o atributo `checker.fixed_content`.

## Utilize a instância como dependência

Então, nós podemos utilizar este `checker` em um `Depends(checker)`, no lugar de `Depends(FixedContentQueryChecker)`, porque a dependência é a instância, `checker`, e não a própria classe.

E quando a dependência for resolvida, o **FastAPI** chamará este `checker` como:

```Python
checker(q="somequery")
```

...e passar o que quer que isso retorne como valor da dependência em nossa *função de operação de rota* como o parâmetro `fixed_content_included`:

{* ../../docs_src/dependencies/tutorial011_an_py39.py hl[22] *}

/// tip | Dica

Tudo isso parece não ser natural. E pode não estar muito claro ou aparentar ser útil ainda.

Estes exemplos são intencionalmente simples, porém mostram como tudo funciona.

Nos capítulos sobre segurança, existem funções utilitárias que são implementadas desta maneira.

Se você entendeu tudo isso, você já sabe como essas funções utilitárias para segurança funcionam por debaixo dos panos.

///
