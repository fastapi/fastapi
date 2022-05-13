# Corpo da Requisição

Quando você precisa enviar dados de um cliente (como de um navegador web) para sua API, você o envia como um **corpo da requisição**.

O corpo da **requisição** é a informação enviada pelo cliente para sua API. O corpo da **resposta** é a informação que sua API envia para o cliente.

Sua API quase sempre irá enviar um corpo na **resposta**. Mas os clientes não necessariamente precisam enviar um corpo em toda **requisição**.

Para declarar um corpo da **requisição**, você utiliza os modelos do <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> com todos os seus poderes e benefícios.

!!! info "Informação"
    Para enviar dados, você deve usar utilizar um dos métodos: `POST` (Mais comum), `PUT`, `DELETE` ou `PATCH`.

    Enviar um corpo em uma requisição `GET` não tem um comportamento definido nas especificações, porém é suportado pelo FastAPI, apenas para casos de uso bem complexos/extremos.

    Como é desencorajado, a documentação interativa com Swagger UI não irá mostrar a documentação para o corpo da requisição para um `GET`, e proxies que intermediarem podem não suportar o corpo da requisição.

## Importe o `BaseModel` do Pydantic

Primeiro, você precisa importar `BaseModel` do `pydantic`:

```Python hl_lines="4"
{!../../../docs_src/body/tutorial001.py!}
```

## Crie seu modelo de dados

Então você declara seu modelo de dados como uma classe que herda `BaseModel`.

Utilize os tipos Python padrão para todos os atributos:

```Python hl_lines="7-11"
{!../../../docs_src/body/tutorial001.py!}
```

Assim como quando declaramos parâmetros de consulta, quando um atributo do modelo possui um valor padrão, ele se torna opcional. Caso contrário, se torna obrigatório. Use `None` para torná-lo opcional.

Por exemplo, o modelo acima declara um JSON "`object`" (ou `dict` no Python) como esse:

```JSON
{
    "name": "Foo",
    "description": "Uma descrição opcional",
    "price": 45.2,
    "tax": 3.5
}
```

...como `description` e `tax` são opcionais (Com um valor padrão de `None`), esse JSON "`object`" também é válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Declare como um parâmetro

Para adicionar o corpo na *função de operação de rota*, declare-o da mesma maneira que você declarou parâmetros de rota e consulta:

```Python hl_lines="18"
{!../../../docs_src/body/tutorial001.py!}
```

...E declare o tipo como o modelo que você criou, `Item`.

## Resultados

Apenas com esse declaração de tipos do Python, o **FastAPI** irá:

* Ler o corpo da requisição como um JSON.
* Converter os tipos correspondentes (se necessário).
* Validar os dados.
    * Se algum dados for inválido, irá retornar um erro bem claro, indicando exatamente onde e o que está incorreto.
* Entregar a você a informação recebida no parâmetro `item`.
    * Como você o declarou na função como do tipo `Item`, você também terá o suporte do editor (completação, etc) para todos os atributos e seus tipos.
* Gerar um <a href="https://json-schema.org" class="external-link" target="_blank">Esquema JSON</a> com as definições do seu modelo, você também pode utilizá-lo em qualquer lugar que quiser, se fizer sentido para seu projeto.
* Esses esquemas farão parte do esquema OpenAPI, e utilizados nas <abbr title="User Interfaces">UIs</abbr> de documentação automática.

## Documentação automática

Os esquemas JSON dos seus modelos farão parte do esquema OpenAPI gerado para sua aplicação, e aparecerão na documentação interativa da API:

<img src="/img/tutorial/body/image01.png">

E também serão utilizados em cada *função de operação de rota* que utilizá-los:

<img src="/img/tutorial/body/image02.png">

## Suporte do editor de texto:

No seu editor de texto, dentro da função você receberá dicas de tipos e completação em todo lugar (isso não aconteceria se você recebesse um `dict` em vez de um modelo Pydantic):

<img src="/img/tutorial/body/image03.png">

Você também poderá receber verificações de erros para operações de tipos incorretas:

<img src="/img/tutorial/body/image04.png">

Isso não é por acaso, todo o framework foi construído em volta deste design.

E foi imensamente testado na fase de design, antes de qualquer implementação, para garantir que funcionaria para todos os editores de texto.

Houveram mudanças no próprio Pydantic para que isso fosse possível.

As capturas de tela anteriores foram capturas no <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Mas você terá o mesmo suporte do editor no <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> e na maioria dos editores Python:

<img src="/img/tutorial/body/image05.png">

!!! tip "Dica"
    Se você utiliza o <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como editor, você pode utilizar o <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Plugin do Pydantic para o PyCharm </a>.

    Melhora o suporte do editor para seus modelos Pydantic com::

    * completação automática
    * verificação de tipos
    * refatoração
    * buscas
    * inspeções

## Use o modelo

Dentro da função, você pode acessar todos os atributos do objeto do modelo diretamente:

```Python hl_lines="21"
{!../../../docs_src/body/tutorial002.py!}
```

## Corpo da requisição + parâmetros de rota

Você pode declarar parâmetros de rota e corpo da requisição ao mesmo tempo.

O **FastAPI** irá reconhecer que os parâmetros da função que combinam com parâmetros de rota devem ser **retirados da rota**, e parâmetros da função que são declarados como modelos Pydantic sejam **retirados do corpo da requisição**.

```Python hl_lines="17-18"
{!../../../docs_src/body/tutorial003.py!}
```

## Corpo da requisição + parâmetros de rota + parâmetros de consulta

Você também pode declarar parâmetros de **corpo**, **rota** e **consulta**, ao mesmo tempo.

O **FastAPI** irá reconhecer cada um deles e retirar a informação do local correto.

```Python hl_lines="18"
{!../../../docs_src/body/tutorial004.py!}
```

Os parâmetros da função serão reconhecidos conforme abaixo:

* Se o parâmetro também é declarado na **rota**, será utilizado como um parâmetro de rota.
* Se o parâmetro é de um **tipo único** (como `int`, `float`, `str`, `bool`, etc) será interpretado como um parâmetro de **consulta**.
* Se o parâmetro é declarado como um **modelo Pydantic**, será interpretado como o **corpo** da requisição.

!!! note "Observação"
    O FastAPI saberá que o valor de `q` não é obrigatório por causa do valor padrão `= None`.

    O `Optional` em `Optional[str]` não é utilizado pelo FastAPI, mas permite ao seu editor de texto lhe dar um suporte melhor e detectar erros.

## Sem o Pydantic

Se você não quer utilizar os modelos Pydantic, você também pode utilizar o parâmetro **Body**. Veja a documentação para [Body - Parâmetros múltiplos: Valores singulares no body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
