# Parâmetros de path { #path-parameters }

Você pode declarar "parâmetros" ou "variáveis" de path com a mesma sintaxe usada por strings de formatação do Python:

{* ../../docs_src/path_params/tutorial001.py hl[6:7] *}

O valor do parâmetro de path `item_id` será passado para a sua função como o argumento `item_id`.

Então, se você executar este exemplo e acessar <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, você verá uma resposta:

```JSON
{"item_id":"foo"}
```

## Parâmetros de path com tipos { #path-parameters-with-types }

Você pode declarar o tipo de um parâmetro de path na função, usando as anotações de tipo padrão do Python:

{* ../../docs_src/path_params/tutorial002.py hl[7] *}

Neste caso, `item_id` é declarado como um `int`.

/// check | Verifique
Isso fornecerá suporte do editor dentro da sua função, com verificações de erros, preenchimento automático, etc.
///

## Dados <abbr title="também conhecido como: serialização, parsing, marshalling">conversão</abbr> { #data-conversion }

Se você executar este exemplo e abrir seu navegador em <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, você verá uma resposta:

```JSON
{"item_id":3}
```

/// check | Verifique
Perceba que o valor que sua função recebeu (e retornou) é `3`, como um `int` do Python, não uma string `"3"`.

Então, com essa declaração de tipo, o **FastAPI** fornece <abbr title="convertendo a string que vem de um request HTTP em dados Python">"parsing"</abbr> automático do request.
///

## Validação de dados { #data-validation }

Mas se você for no navegador para <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, verá um bom erro HTTP:

```JSON
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "foo"
    }
  ]
}
```

porque o parâmetro de path `item_id` tinha o valor `"foo"`, que não é um `int`.

O mesmo erro apareceria se você fornecesse um `float` em vez de um `int`, como em: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

/// check | Verifique
Então, com a mesma declaração de tipo do Python, o **FastAPI** fornece validação de dados.

Observe que o erro também declara claramente exatamente o ponto onde a validação não passou.

Isso é incrivelmente útil ao desenvolver e depurar código que interage com sua API.
///

## Documentação { #documentation }

E quando você abrir seu navegador em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, você verá documentação automática, interativa, da API como:

<img src="/img/tutorial/path-params/image01.png">

/// check | Verifique
Novamente, apenas com a mesma declaração de tipo do Python, o **FastAPI** fornece documentação automática e interativa (integrando o Swagger UI).

Observe que o parâmetro de path está declarado como um inteiro.
///

## Benefícios baseados em padrões, documentação alternativa { #standards-based-benefits-alternative-documentation }

E como o schema gerado é do padrão <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md" class="external-link" target="_blank">OpenAPI</a>, existem muitas ferramentas compatíveis.

Por causa disso, o próprio **FastAPI** fornece uma documentação alternativa da API (usando ReDoc), que você pode acessar em <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="/img/tutorial/path-params/image02.png">

Da mesma forma, existem muitas ferramentas compatíveis. Incluindo ferramentas de geração de código para muitas linguagens.

## Pydantic { #pydantic }

Toda a validação de dados é realizada nos bastidores pelo <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>, então você recebe todos os benefícios disso. E você sabe que está em boas mãos.

Você pode usar as mesmas declarações de tipo com `str`, `float`, `bool` e muitos outros tipos de dados complexos.

Vários deles são explorados nos próximos capítulos do tutorial.

## A ordem importa { #order-matters }

Ao criar *operações de rota*, você pode encontrar situações em que tem um path fixo.

Como `/users/me`, digamos que seja para obter dados sobre o usuário atual.

E então você também pode ter um path `/users/{user_id}` para obter dados sobre um usuário específico por algum ID de usuário.

Como as *operações de rota* são avaliadas em ordem, você precisa garantir que o path para `/users/me` seja declarado antes do de `/users/{user_id}`:

{* ../../docs_src/path_params/tutorial003.py hl[6,11] *}

Caso contrário, o path para `/users/{user_id}` também corresponderia a `/users/me`, "achando" que está recebendo um parâmetro `user_id` com o valor `"me"`.

Da mesma forma, você não pode redefinir uma operação de rota:

{* ../../docs_src/path_params/tutorial003b.py hl[6,11] *}

A primeira sempre será usada, já que o path corresponde primeiro.

## Valores predefinidos { #predefined-values }

Se você tem uma *operação de rota* que recebe um *parâmetro de path*, mas quer que os valores válidos possíveis do *parâmetro de path* sejam predefinidos, você pode usar um <abbr title="Enumeration">`Enum`</abbr> padrão do Python.

### Crie uma classe `Enum` { #create-an-enum-class }

Importe `Enum` e crie uma subclasse que herde de `str` e de `Enum`.

Ao herdar de `str`, a documentação da API saberá que os valores devem ser do tipo `string` e poderá renderizá-los corretamente.

Em seguida, crie atributos de classe com valores fixos, que serão os valores válidos disponíveis:

{* ../../docs_src/path_params/tutorial005.py hl[1,6:9] *}

/// info | Informação
<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerations (ou enums) estão disponíveis no Python</a> desde a versão 3.4.
///

/// tip | Dica
Se você está se perguntando, "AlexNet", "ResNet" e "LeNet" são apenas nomes de <abbr title="Tecnicamente, arquiteturas de modelos de Deep Learning">modelos</abbr> de Aprendizado de Máquina.
///

### Declare um parâmetro de path { #declare-a-path-parameter }

Em seguida, crie um *parâmetro de path* com anotação de tipo usando a classe enum que você criou (`ModelName`):

{* ../../docs_src/path_params/tutorial005.py hl[16] *}

### Verifique a documentação { #check-the-docs }

Como os valores disponíveis para o *parâmetro de path* são predefinidos, a documentação interativa pode mostrá-los de forma agradável:

<img src="/img/tutorial/path-params/image03.png">

### Trabalhando com *enumerações* do Python { #working-with-python-enumerations }

O valor do *parâmetro de path* será um *membro de enumeração*.

#### Compare membros de enumeração { #compare-enumeration-members }

Você pode compará-lo com o *membro de enumeração* no seu enum `ModelName` criado:

{* ../../docs_src/path_params/tutorial005.py hl[17] *}

#### Obtenha o valor da enumeração { #get-the-enumeration-value }

Você pode obter o valor real (um `str` neste caso) usando `model_name.value`, ou, em geral, `your_enum_member.value`:

{* ../../docs_src/path_params/tutorial005.py hl[20] *}

/// tip | Dica
Você também pode acessar o valor `"lenet"` com `ModelName.lenet.value`.
///

#### Retorne membros de enumeração { #return-enumeration-members }

Você pode retornar *membros de enum* da sua *operação de rota*, até mesmo aninhados em um corpo JSON (por exemplo, um `dict`).

Eles serão convertidos para seus valores correspondentes (strings neste caso) antes de serem retornados ao cliente:

{* ../../docs_src/path_params/tutorial005.py hl[18,21,23] *}

No seu cliente, você receberá uma resposta JSON como:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Parâmetros de path que contêm paths { #path-parameters-containing-paths }

Digamos que você tenha uma *operação de rota* com um path `/files/{file_path}`.

Mas você precisa que o próprio `file_path` contenha um *path*, como `home/johndoe/myfile.txt`.

Então, a URL para esse arquivo seria algo como: `/files/home/johndoe/myfile.txt`.

### Suporte do OpenAPI { #openapi-support }

O OpenAPI não oferece suporte a uma maneira de declarar um *parâmetro de path* que contenha um *path* dentro, pois isso poderia levar a cenários difíceis de testar e definir.

Ainda assim, você pode fazer isso no **FastAPI**, usando uma das ferramentas internas do Starlette.

E a documentação continuará funcionando, embora não adicione nenhuma informação dizendo que o parâmetro deve conter um path.

### Conversor de path { #path-convertor }

Usando uma opção diretamente do Starlette você pode declarar um *parâmetro de path* contendo um *path* usando uma URL como:

```
/files/{file_path:path}
```

Nesse caso, o nome do parâmetro é `file_path`, e a última parte, `:path`, diz que o parâmetro deve corresponder a qualquer *path*.

Então, você pode usá-lo com:

{* ../../docs_src/path_params/tutorial004.py hl[6] *}

/// tip | Dica
Você pode precisar que o parâmetro contenha `/home/johndoe/myfile.txt`, com uma barra inicial (`/`).

Nesse caso, a URL seria: `/files//home/johndoe/myfile.txt`, com uma barra dupla (`//`) entre `files` e `home`.
///

## Recapitulação { #recap }

Com o **FastAPI**, ao usar declarações de tipo do Python curtas, intuitivas e padrão, você obtém:

- Suporte no editor: verificações de erro, autocompletar, etc.
- "<abbr title="convertendo a string que vem de um request HTTP em dados Python">Parsing</abbr>" de dados
- Validação de dados
- Anotação da API e documentação automática

E você só precisa declará-los uma vez.

Essa é provavelmente a principal vantagem visível do **FastAPI** em comparação com frameworks alternativos (além do desempenho bruto).
