# Parâmetros de path e validações numéricas { #path-parameters-and-numeric-validations }

Da mesma forma que você pode declarar mais validações e metadados para parâmetros de consulta com `Query`, você pode declarar o mesmo tipo de validações e metadados para parâmetros de path com `Path`.

## Importe `Path` { #import-path }

Primeiro, importe `Path` de `fastapi`, e importe `Annotated`:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | Informação

O FastAPI adicionou suporte a `Annotated` (e passou a recomendá-lo) na versão 0.95.0.

Se você tiver uma versão mais antiga, verá erros ao tentar usar `Annotated`.

Certifique-se de [Atualizar a versão do FastAPI](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} para pelo menos 0.95.1 antes de usar `Annotated`.

///

## Declare metadados { #declare-metadata }

Você pode declarar todos os mesmos parâmetros que em `Query`.

Por exemplo, para declarar um valor de metadado `title` para o parâmetro de path `item_id` você pode digitar:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | Nota

Um parâmetro de path é sempre obrigatório, pois precisa fazer parte do path. Mesmo que você o declare como `None` ou defina um valor padrão, isso não afetaria nada, ele ainda seria sempre obrigatório.

///

## Ordene os parâmetros de acordo com sua necessidade { #order-the-parameters-as-you-need }

/// tip | Dica

Isso provavelmente não é tão importante ou necessário se você usar `Annotated`.

///

Vamos supor que você queira declarar o parâmetro de consulta `q` como uma `str` obrigatória.

E você não precisa declarar mais nada para esse parâmetro, então você realmente não precisa usar `Query`.

Mas você ainda precisa usar `Path` para o parâmetro de path `item_id`. E você não quer usar `Annotated` por algum motivo.

O Python vai reclamar se você colocar um valor com “padrão” antes de um valor que não tem “padrão”.

Mas você pode reordená-los e colocar primeiro o valor sem padrão (o parâmetro de consulta `q`).

Isso não faz diferença para o **FastAPI**. Ele vai detectar os parâmetros pelos seus nomes, tipos e declarações de padrão (`Query`, `Path`, etc.), sem se importar com a ordem.

Então, você pode declarar sua função assim:

{* ../../docs_src/path_params_numeric_validations/tutorial002.py hl[7] *}

Mas tenha em mente que, se você usar `Annotated`, você não terá esse problema, não fará diferença, pois você não está usando valores padrão de parâmetros de função para `Query()` ou `Path()`.

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py39.py *}

## Ordene os parâmetros de acordo com sua necessidade, truques { #order-the-parameters-as-you-need-tricks }

/// tip | Dica

Isso provavelmente não é tão importante ou necessário se você usar `Annotated`.

///

Aqui vai um pequeno truque que pode ser útil, mas você não vai precisar dele com frequência.

Se você quiser:

* declarar o parâmetro de consulta `q` sem um `Query` nem qualquer valor padrão
* declarar o parâmetro de path `item_id` usando `Path`
* tê-los em uma ordem diferente
* não usar `Annotated`

...o Python tem uma pequena sintaxe especial para isso.

Passe `*`, como o primeiro parâmetro da função.

O Python não fará nada com esse `*`, mas saberá que todos os parâmetros seguintes devem ser chamados como argumentos nomeados (pares chave-valor), também conhecidos como <abbr title="Do inglês: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>. Mesmo que eles não tenham um valor padrão.

{* ../../docs_src/path_params_numeric_validations/tutorial003.py hl[7] *}

### Melhor com `Annotated` { #better-with-annotated }

Tenha em mente que, se você usar `Annotated`, como você não está usando valores padrão de parâmetros de função, você não terá esse problema e provavelmente não precisará usar `*`.

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py39.py hl[10] *}

## Validações numéricas: maior que ou igual { #number-validations-greater-than-or-equal }

Com `Query` e `Path` (e outras que você verá depois) você pode declarar restrições numéricas.

Aqui, com `ge=1`, `item_id` precisará ser um número inteiro “`g`reater than or `e`qual” a `1`.

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py39.py hl[10] *}

## Validações numéricas: maior que e menor que ou igual { #number-validations-greater-than-and-less-than-or-equal }

O mesmo se aplica a:

* `gt`: maior que (`g`reater `t`han)
* `le`: menor que ou igual (`l`ess than or `e`qual)

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py39.py hl[10] *}

## Validações numéricas: floats, maior que e menor que { #number-validations-floats-greater-than-and-less-than }

Validações numéricas também funcionam para valores `float`.

Aqui é onde se torna importante poder declarar <abbr title="greater than – maior que"><code>gt</code></abbr> e não apenas <abbr title="greater than or equal – maior que ou igual"><code>ge</code></abbr>. Com isso você pode exigir, por exemplo, que um valor seja maior que `0`, mesmo que seja menor que `1`.

Assim, `0.5` seria um valor válido. Mas `0.0` ou `0` não seriam.

E o mesmo para <abbr title="less than – menor que"><code>lt</code></abbr>.

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py39.py hl[13] *}

## Recapitulando { #recap }

Com `Query`, `Path` (e outras que você ainda não viu) você pode declarar metadados e validações de string do mesmo modo que em [Parâmetros de consulta e validações de string](query-params-str-validations.md){.internal-link target=_blank}.

E você também pode declarar validações numéricas:

* `gt`: maior que (`g`reater `t`han)
* `ge`: maior que ou igual (`g`reater than or `e`qual)
* `lt`: menor que (`l`ess `t`han)
* `le`: menor que ou igual (`l`ess than or `e`qual)

/// info | Informação

`Query`, `Path` e outras classes que você verá depois são subclasses de uma classe comum `Param`.

Todas elas compartilham os mesmos parâmetros para validação adicional e metadados que você viu.

///

/// note | Detalhes Técnicos

Quando você importa `Query`, `Path` e outras de `fastapi`, elas são na verdade funções.

Que, quando chamadas, retornam instâncias de classes de mesmo nome.

Então, você importa `Query`, que é uma função. E quando você a chama, ela retorna uma instância de uma classe também chamada `Query`.

Essas funções existem (em vez de usar diretamente as classes) para que seu editor não marque erros sobre seus tipos.

Dessa forma, você pode usar seu editor e ferramentas de codificação normais sem precisar adicionar configurações personalizadas para desconsiderar esses erros.

///
