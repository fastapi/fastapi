# Corpo da requisição

Quando for preciso enviar dados de um cliente(Por exemplo, um browser) para a sua API, o envio é feito no **corpo da requisição**.

O corpo da **requisição** são os dados enviados pelo cliente para a sua API, enquanto que o corpo da **resposta** são os dados que a sua API envia para o cliente.

A sua API quase sempre terá que enviar algo no corpo da **resposta**. Mas os clientes não necessariamente precisam enviar um corpo da **requisição** o tempo todo.

Para declarar um corpo de **requisição**, você irá usar modelos <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> com todo o seu poder e benefícios.

!!! Informação
    Para enviar dados, você deve usar: `POST` (o mais comum), `PUT`, `DELETE` ou `PATCH`.

    Enviar um corpo numa requisição `GET` tem um comportamento indefinido nas especificações, de qualquer forma isso é suportado pelo FastAPI, apenas para casos muito complexos/extremos.

    Visto que, não é aconselhado, a documentação iterativa com Swagger UI não irá mostrar documentação para o corpo quando se usar o método `GET`, e possíveis proxies no meio podem não    suportar.

## Importe o `BaseModel` do Pydantic

Primeiramente, será preciso importar o `BaseModel` do `pydantic`:

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## Crie o seu modelo de dados

Apõs isso, será preciso criar o seu modelo de dados que irá herdar do `BaseModel`.

Use os tipos padrões do Python para todos os atributos:

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

Da mesma forma de quando-se declara parâmetros de query, quando o atributo de um modelo possui um valor padrão, esse atributo não será obrigatório. Caso contrário sim. Use `None` para fazê-lo meramente opcional.

Por exemplo, esse modelo abaixo declara um "`object`" JSON(ou `dict` Python):

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...uma vez que, `description` e `tax` são opcionais (com um valor padrão de `None`), esse "`object`" JSON também será válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Declare como um parâmetro

De forma a adicionar para a sua *operação de rota*, declare da mesma forma que você declarou os parâmetros de rota e de query:

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

...e declare o tipo como o modelo criado anteriormente, `Item`.

## Resultados

Com apenas essa declaração de tipos do Python, o **FastAPI** vai:

* Ler o corpo da requisição como um JSON.
* Converter os tipos correspondentes(caso necessário).
* Validar os dados.
    * Se os dados forem inválidos, um erro bonito e claro vai ser retornado, indicando exatamente aonde e o que foi o dado incorreto..
* Lhe fornecer os dados recebidos no parâmetro `item`.
    * Uma vez que, você declarou-o dentro da função como do tipo `Item`, você também receberá todo o suporte do editor de texto(compleção, etc) em relação a todos os atributos e seus respectivos tipos.
* Gerar definições no formato de <a href="https://json-schema.org" class="external-link" target="_blank">schema JSON</a> para o seu modelo, você pode usa-las em qualquer lugar que quiser se fizer sentido para o seu proejto.
* Esses schemas serão parte do schema OpenAPI gerado, e serâo usados pelas <abbr title="User Interfaces">UIs</abbr> de documentação automatica.

## Documentação automática

Os schemas JSON dos seus modelos serão parte do schema gerado pela OpenAPI, e serão mostrados na documentação interativa da API:

<img src="/img/tutorial/body/image01.png">

E serão também usadas na documentação dentro de cada *operação de rota* que precisar deles:

<img src="/img/tutorial/body/image02.png">

## Suporte do editor

No seu editor, dentro da sua função você irá receber dicas de tipos e compleção em todos os locais(isso não iria acontecer se um `dict` fosse recebido invés de um modelo do Pydantic):

<img src="/img/tutorial/body/image03.png">

Você tambẽm irá ter checagem de erros para os casos de operações com tipos incorretos:

<img src="/img/tutorial/body/image04.png">

Isso não é por acaso, o framework inteiro foi feito ao redor desse design.

E foi testado exaustivamente na fase de design, antes de qualquer implementação, para garantir que funcione com todos os editores de texto.

Houveram até mesmo algumas mudanças feitas dentro do próprio Pydantic para suportar isso.

As capturas de tela anteriores foram capturadas com o <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Mas você receberia o mesmo tipo de suporte com o <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> e com a maioria dos outros editores de Python:

<img src="/img/tutorial/body/image05.png">

!!! Dica
    Se você usa o <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como o seu editor, você pode usar o <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Pydantic PyCharm Plugin</a>.

    Ele vai melhorar o suporte do editor para modelos do Pydantic, em relação a:
    
    * auto-complementação
    * checagem de tipos
    * refactoração
    * busca
    * inspeções

## Usando o modelo

Dentro da função, você pode acessar todos os atributos do objeto do modelo diretamente:

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## Corpo de requisição + parâmetros de rota

Você pode declarar parâmetros de rota e um corpo de requisição ao mesmo tempo.

O **FastAPI** vai reconhecer que os parâmetros da função que correspondem aos parâmetros da rota devem ser **retirados da rota**, e que os parâmetros da função que são declarados como modelos do Pydantic devem ser **retirados do corpo da requisição**.

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## Parâmetros de corpo + rota + query

Você também pode declarar parâmetros de **corpo**, **rota** e **query**, todos ao mesmo tempo.

O **FastAPI** vai reconhecer cada um deles e extrair os dados do local certo.

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

Os parâmetros da função vão ser reconhecidos da seguinte forma:

* Se o parâmetro também for declarado na **rota**, ele será usado como um parâmetro de rota.
* Se o parâmetro for de um **tipo singular**( como `int`, `float`, `str`, `bool`, etc) ele será interpretado como um parâmetro de query.
* Se o parâmetro for declarado como sendo do tipo de um **modelo do Pydantic**, ele será interpretado como sendo o **corpo** da requisição.

!!! Nota
    O FastAPI vai saber que o valor de `q` não é obrigatório porque seu valor padrão é `= None`.

    O `Optional` em `Optional[str]` não é usado pelo FastAPI, mas irá permitir que o editor lhe dê um suporte melhor e detecte erros.

## Sem o Pydantic

Se você não quer usar modelos Pydantic, você também pode usar parâmetros de **Body**. Para mais informações cheque a documentação para [Body - Multiple Parameters: Singular values in body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.

