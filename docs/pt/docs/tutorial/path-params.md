# Parâmetros de rota

Você pode declarar "parâmetros" ou "variáveis" de rota com a mesma sintaxe usada para formatar strings em Python:

```Python hl_lines="6-7"
{!../../../docs_src/path_params/tutorial001.py!}
```


O valor do parâmetro de rota `item_id` será passado para sua função como o argumento `item_id`.

Então, se você executar este exemplo e for para <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, você verá a seguinte resposta:

```JSON
{"item_id":"foo"}
```

## Parâmetros de rota com tipos

Você pode declarar o tipo de um parâmetro de rota na função, usando anotações de tipo padrão de Python:

```Python hl_lines="7"
{!../../../docs_src/path_params/tutorial002.py!}
```

Neste caso, `item_id` é declarado como um `int`.

!!! check
    Isso lhe dará suporte ao editor dentro de sua função, com verificações de erros, preenchimento automático, etc.

## <abbr title="também conhecido como: serialização, parseamento, marshalling">Conversão</abbr> de Dados

Se você executar este exemplo e abrir o seu navegador em <a href="http://127.0.0.1:8000/items/3" class="external-link" target="_blank">http://127.0.0.1:8000/items/3</a>, você verá a seguinte resposta:

```JSON
{"item_id":3}
```

!!! check
   Observe que o valor que sua função recebeu (e devolveu) é `3`, como o tipo Python `int`, não uma string `"3"`.

    Então, com essa declaração de tipo, **FastAPI** oferece a você uma <abbr title="convertendo a string que vem de uma requisição HTTP em dados Python">"conversão"</abbr> automática de requisição.

## Validação de dados

Mas se você acessar o navegador em <a href="http://127.0.0.1:8000/items/foo" class="external-link" target="_blank">http://127.0.0.1:8000/items/foo</a>, você verá um erro HTTP como:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

isso acontece porque o parâmetro de rota `item_id` tinha um valor igual a `"foo"`, que não é um `int`.

O mesmo erro ocorreria se você fornecesse um valor `float` em vez de um int, como em: <a href="http://127.0.0.1:8000/items/4.2" class="external-link" target="_blank">http://127.0.0.1:8000/items/4.2</a>

!!! check
    Portanto, com a mesma declaração de tipo do Python, **FastAPI** oferece a você validação de dados.

    Observe que o erro também indica claramente o ponto em que a validação não passou.

    Isso é extremamente útil durante o desenvolvimento e depuração de código que interage com a sua API.


## Documentação

E quando você abre seu navegador em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>, você verá uma documentação de API automática e interativa como:

<img src="/img/tutorial/path-params/image01.png">

!!! check
    Novamente, apenas com a mesma declaração de tipo Python, **FastAPI** oferece documentação automática e interativa (integrando a IU Swagger).

    Observe que o parâmetro da rota é declarado como um inteiro.

## Benefícios baseados em padrões, documentação alternativa

E porque o *schema* gerado é do padrão <a href="https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md" class="external-link" target="_blank">OpenAPI</a>, existem muitas ferramentas compatíveis.

Por causa disso, o próprio **FastAPI** fornece uma documentação de API alternativa (usando ReDoc), que você pode acessar em <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>:

<img src="/img/tutorial/path-params/image02.png">

Da mesma forma, existem muitas ferramentas compatíveis. Incluindo ferramentas de geração de código para várias linguagens.

## Pydantic

Toda a validação de dados é realizada internamente por <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>, assim você obtem todos os beneficios dele. E você sabe que está em boas mãos.

Você pode usar as mesmas declarações de tipo com `str`,` float`, `bool` e muitos outros tipos de dados complexos.

Vários deles são explorados nos próximos capítulos do tutorial.

## Ordem importa

Ao criar *operações de rota*, você pode encontrar situações em que tem uma rota fixa.

Como `/users/me`, digamos que seja para obter dados sobre o usuário atual.

E você também pode ter uma rota `/users/{user_id}` para obter dados sobre um usuário específico por algum ID de usuário.

Como as *operações de rota* são avaliadas em ordem, você precisa se certificar de que a rota para `/users/me` seja declarada antes de `/users/{user_id}`:

```Python hl_lines="6  11"
{!../../../docs_src/path_params/tutorial003.py!}
```

Caso contrário, a rota para `/users/{user_id}` corresponderia também para `/users/me`, "pensando" que está recebendo um parâmetro `user_id` com o valor `"me"`.

## Valores predefinidos

Se você tem uma *operação de rota* que recebe um *parâmetro de rota*, mas deseja que os valores válidos do *parâmetro de rota* possíveis sejam predefinidos, você pode usar um <abbr title="Enumeration">`Enum`</abbr> padrão de Python.

### Crie uma classe `Enum`

Importe `Enum` e crie uma subclasse que herda de `str` e de `Enum`.

Ao herdar de `str` a documentação da API será capaz de saber que os valores devem ser do tipo `string` e irá renderizar corretamente.

Em seguida, crie atributos de classe com valores fixos, que serão os valores válidos disponíveis:

```Python hl_lines="1  6-9"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! info
    <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">Enumerações (ou enums) estão disponíveis em Python</a> desde a versão 3.4.

!!! tip
    Se você está se perguntando, "AlexNet", "ResNet" e "LeNet" são apenas nomes de <abbr title="Technically, Deep Learning model architectures">modelos</abbr> de Machine Learning.

### Declare um *parâmetro de rota*

Em seguida, crie um *parâmetro de rota* com uma anotação de tipo usando a classe enum que você criou (`ModelName`):

```Python hl_lines="16"
{!../../../docs_src/path_params/tutorial005.py!}
```

### Verifique a documentação

Como os valores disponíveis para o *parâmetro de rota* são predefinidos, os documentos interativos podem mostrá-los muito bem:

<img src="/img/tutorial/path-params/image03.png">

### Trabalhando com *enumerações* em Python

O valor do *parâmetro de rota* será um *membro de enumeração*.

#### Compare *membros da enumeração*

Você pode compará-lo com o *membro da enumeração* em seu enum `ModelName` criado:

```Python hl_lines="17"
{!../../../docs_src/path_params/tutorial005.py!}
```

#### Obtenha o *valor da enumeração*

Você pode obter o valor real (um `str` neste caso) usando `model_name.value`, ou em geral, `your_enum_member.value`:

```Python hl_lines="20"
{!../../../docs_src/path_params/tutorial005.py!}
```

!!! tip
    Você também pode acessar o valor `"lenet"` com `ModelName.lenet.value`.

#### Retornar *membros da enumeração*

Você pode retornar *membros enum* da sua *operação de rota*, mesmo aninhados em um corpo JSON (por exemplo, um `dict`).

Eles serão convertidos em seus valores correspondentes (strings neste caso) antes de devolvê-los ao cliente:

```Python hl_lines="18  21  23"
{!../../../docs_src/path_params/tutorial005.py!}
```

Em seu cliente, você receberá uma resposta JSON como:

```JSON
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

## Parâmetros de rota contendo rotas

Digamos que você tenha uma *operação de rota* com uma rota `/files/{file_path}`.

Mas você precisa do próprio `file_path` para conter uma *rota*, como `home/johndoe/myfile.txt`.

Portanto, a URL para esse arquivo seria algo como: `/files/home/johndoe/myfile.txt`.

### Suporte OpenAPI

OpenAPI não oferece suporte a uma forma de declarar um *parâmetro de rota* para conter uma *rota* dentro, pois isso pode levar a cenários que são difíceis de testar e definir.

No entanto, você ainda pode fazer isso no **FastAPI**, usando uma das ferramentas internas da Starlette.

E os documentos ainda funcionariam, embora não adicionassem nenhuma documentação informando que o parâmetro deve conter um caminho.

### Conversor de rota

Usando uma opção diretamente do Starlette, você pode declarar um *parâmetro de rota * contendo uma *rota* usando uma URL como:

```
/files/{file_path:path}
```

Neste caso, o nome do parâmetro é `file_path`, e a última parte,`:path`, informa que o parâmetro deve corresponder a qualquer *rota*.

Então, você pode usá-lo com:

```Python hl_lines="6"
{!../../../docs_src/path_params/tutorial004.py!}
```

!!! tip
    Você pode precisar que o parâmetro contenha `/home/johndoe/myfile.txt`, com uma barra inicial (`/`).

    Nesse caso, a URL seria: `/files//home/johndoe/myfile.txt`, com uma barra dupla (`//`) entre `files` e `home`.

## Recap

Com **FastAPI**, usando declarações de tipo curtas, intuitivas e padrão de Python, você obtém:

* Suporte ao editor: verificações de erros, preenchimento automático, etc.
* "<abbr title="Converter a string que vem de uma solicitação HTTP em dados Python">Conversão</abbr>" de dados
* Validação de dados
* Anotações de API e documentação automática

E você só precisa declará-los uma vez.

Essa é provavelmente a principal vantagem visível do **FastAPI** em comparação com frameworks alternativos (além do desempenho).
