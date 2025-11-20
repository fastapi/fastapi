# Corpo da requisição { #request-body }

Quando você precisa enviar dados de um cliente (como de um navegador) para sua API, você os envia como um **corpo da requisição**.

O corpo da **requisição** é a informação enviada pelo cliente para sua API. O corpo da **resposta** é a informação que sua API envia para o cliente.

Sua API quase sempre precisa enviar um corpo na **resposta**. Mas os clientes não necessariamente precisam enviar **corpos de requisição** o tempo todo, às vezes eles apenas requisitam um path, talvez com alguns parâmetros de consulta, mas não enviam um corpo.

Para declarar um corpo da **requisição**, você utiliza os modelos do <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> com todos os seus poderes e benefícios.

/// info | Informação

Para enviar dados, você deve usar um dos: `POST` (o mais comum), `PUT`, `DELETE` ou `PATCH`.

Enviar um corpo em uma requisição `GET` não tem um comportamento definido nas especificações, porém é suportado pelo FastAPI, apenas para casos de uso bem complexos/extremos.

Como é desencorajado, a documentação interativa com Swagger UI não irá mostrar a documentação para o corpo da requisição para um `GET`, e proxies que intermediarem podem não suportar o corpo da requisição.

///

## Importe o `BaseModel` do Pydantic { #import-pydantics-basemodel }

Primeiro, você precisa importar `BaseModel` do `pydantic`:

{* ../../docs_src/body/tutorial001_py310.py hl[2] *}

## Crie seu modelo de dados { #create-your-data-model }

Então você declara seu modelo de dados como uma classe que herda `BaseModel`.

Utilize os tipos Python padrão para todos os atributos:

{* ../../docs_src/body/tutorial001_py310.py hl[5:9] *}

Assim como quando declaramos parâmetros de consulta, quando um atributo do modelo possui um valor padrão, ele se torna opcional. Caso contrário, se torna obrigatório. Use `None` para torná-lo opcional.

Por exemplo, o modelo acima declara um JSON "`object`" (ou `dict` no Python) como esse:

```JSON
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

...como `description` e `tax` são opcionais (com um valor padrão de `None`), esse JSON "`object`" também é válido:

```JSON
{
    "name": "Foo",
    "price": 45.2
}
```

## Declare como um parâmetro { #declare-it-as-a-parameter }

Para adicioná-lo à sua *operação de rota*, declare-o da mesma maneira que você declarou parâmetros de rota e de consulta:

{* ../../docs_src/body/tutorial001_py310.py hl[16] *}

...e declare o seu tipo como o modelo que você criou, `Item`.

## Resultados { #results }

Apenas com essa declaração de tipos do Python, o **FastAPI** irá:

* Ler o corpo da requisição como um JSON.
* Converter os tipos correspondentes (se necessário).
* Validar os dados.
    * Se algum dado for inválido, irá retornar um erro bem claro, indicando exatamente onde e o que estava incorreto.
* Entregar a você a informação recebida no parâmetro `item`.
    * Como você o declarou na função como do tipo `Item`, você também terá o suporte do editor (completação, etc) para todos os atributos e seus tipos.
* Gerar definições de <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> para o seu modelo; você também pode usá-las em qualquer outro lugar se fizer sentido para o seu projeto.
* Esses schemas farão parte do esquema OpenAPI gerado, e serão usados pelas <abbr title="User Interfaces – Interfaces de usuário">UIs</abbr> de documentação automática.

## Documentação automática { #automatic-docs }

Os JSON Schemas dos seus modelos farão parte do esquema OpenAPI gerado para sua aplicação, e aparecerão na documentação interativa da API:

<img src="/img/tutorial/body/image01.png">

E também serão utilizados na documentação da API dentro de cada *operação de rota* que precisar deles:

<img src="/img/tutorial/body/image02.png">

## Suporte do editor { #editor-support }

No seu editor, dentro da função você receberá dicas de tipos e completação em todo lugar (isso não aconteceria se você recebesse um `dict` em vez de um modelo Pydantic):

<img src="/img/tutorial/body/image03.png">

Você também poderá receber verificações de erros para operações de tipos incorretas:

<img src="/img/tutorial/body/image04.png">

Isso não é por acaso, todo o framework foi construído em volta deste design.

E foi imensamente testado na fase de design, antes de qualquer implementação, para garantir que funcionaria para todos os editores de texto.

Houveram mudanças no próprio Pydantic para que isso fosse possível.

As capturas de tela anteriores foram capturas no <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Mas você terá o mesmo suporte do editor no <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> e na maioria dos editores Python:

<img src="/img/tutorial/body/image05.png">

/// tip | Dica

Se você utiliza o <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> como editor, você pode utilizar o <a href="https://github.com/koxudaxi/pydantic-pycharm-plugin/" class="external-link" target="_blank">Plugin do Pydantic para o PyCharm </a>.

Melhora o suporte do editor para seus modelos Pydantic com:

* preenchimento automático
* verificação de tipos
* refatoração
* buscas
* inspeções

///

## Use o modelo { #use-the-model }

Dentro da função, você pode acessar todos os atributos do objeto do modelo diretamente:

{* ../../docs_src/body/tutorial002_py310.py *}

/// info | Informação

No Pydantic v1 o método se chamava `.dict()`, ele foi descontinuado (mas ainda é suportado) no Pydantic v2, e renomeado para `.model_dump()`.

Os exemplos aqui usam `.dict()` para compatibilidade com o Pydantic v1, mas você deve usar `.model_dump()` se puder usar o Pydantic v2.

///

## Corpo da requisição + parâmetros de rota { #request-body-path-parameters }

Você pode declarar parâmetros de rota e corpo da requisição ao mesmo tempo.

O **FastAPI** irá reconhecer que os parâmetros da função que combinam com parâmetros de rota devem ser **retirados da rota**, e que parâmetros da função que são declarados como modelos Pydantic sejam **retirados do corpo da requisição**.

{* ../../docs_src/body/tutorial003_py310.py hl[15:16] *}

## Corpo da requisição + parâmetros de rota + parâmetros de consulta { #request-body-path-query-parameters }

Você também pode declarar parâmetros de **corpo**, **rota** e **consulta**, ao mesmo tempo.

O **FastAPI** irá reconhecer cada um deles e retirar a informação do local correto.

{* ../../docs_src/body/tutorial004_py310.py hl[16] *}

Os parâmetros da função serão reconhecidos conforme abaixo:

* Se o parâmetro também é declarado no **path**, será utilizado como um parâmetro de rota.
* Se o parâmetro é de um **tipo único** (como `int`, `float`, `str`, `bool`, etc) será interpretado como um parâmetro de **consulta**.
* Se o parâmetro é declarado como um **modelo Pydantic**, será interpretado como o **corpo** da requisição.

/// note | Nota

O FastAPI saberá que o valor de `q` não é obrigatório por causa do valor padrão `= None`.

O `str | None` (Python 3.10+) ou o `Union` em `Union[str, None]` (Python 3.8+) não é utilizado pelo FastAPI para determinar que o valor não é obrigatório, ele saberá que não é obrigatório porque tem um valor padrão `= None`.

Mas adicionar as anotações de tipo permitirá ao seu editor oferecer um suporte melhor e detectar erros.

///

## Sem o Pydantic { #without-pydantic }

Se você não quer utilizar os modelos Pydantic, você também pode utilizar o parâmetro **Body**. Veja a documentação para [Body - Parâmetros múltiplos: Valores singulares no body](body-multiple-params.md#singular-values-in-body){.internal-link target=_blank}.
