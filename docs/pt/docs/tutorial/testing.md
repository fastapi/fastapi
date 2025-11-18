# Testando { #testing }

Graças ao <a href="https://www.starlette.dev/testclient/" class="external-link" target="_blank">Starlette</a>, testar aplicativos **FastAPI** é fácil e agradável.

Ele é baseado no <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, que por sua vez é projetado com base em Requests, por isso é muito familiar e intuitivo.

Com ele, você pode usar o <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> diretamente com **FastAPI**.

## Usando `TestClient` { #using-testclient }

/// info | Informação

Para usar o `TestClient`, primeiro instale o <a href="https://www.python-httpx.org" class="external-link" target="_blank">`httpx`</a>.

Certifique-se de criar um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, ativá-lo e instalá-lo, por exemplo:

```console
$ pip install httpx
```

///

Importe `TestClient`.

Crie um `TestClient` passando seu aplicativo **FastAPI** para ele.

Crie funções com um nome que comece com `test_` (essa é a convenção padrão do `pytest`).

Use o objeto `TestClient` da mesma forma que você faz com `httpx`.

Escreva instruções `assert` simples com as expressões Python padrão que você precisa verificar (novamente, `pytest` padrão).

{* ../../docs_src/app_testing/tutorial001.py hl[2,12,15:18] *}

/// tip | Dica

Observe que as funções de teste são `def` normais, não `async def`.

E as chamadas para o cliente também são chamadas normais, não usando `await`.

Isso permite que você use `pytest` diretamente sem complicações.

///

/// note | Detalhes Técnicos

Você também pode usar `from starlette.testclient import TestClient`.

**FastAPI** fornece o mesmo `starlette.testclient` que `fastapi.testclient` apenas como uma conveniência para você, o desenvolvedor. Mas ele vem diretamente da Starlette.

///

/// tip | Dica

Se você quiser chamar funções `async` em seus testes além de enviar solicitações ao seu aplicativo FastAPI (por exemplo, funções de banco de dados assíncronas), dê uma olhada em [Testes assíncronos](../advanced/async-tests.md){.internal-link target=_blank} no tutorial avançado.

///

## Separando testes { #separating-tests }

Em uma aplicação real, você provavelmente teria seus testes em um arquivo diferente.

E seu aplicativo **FastAPI** também pode ser composto de vários arquivos/módulos, etc.

### Arquivo do aplicativo **FastAPI** { #fastapi-app-file }

Digamos que você tenha uma estrutura de arquivo conforme descrito em [Aplicações maiores](bigger-applications.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

No arquivo `main.py` você tem seu aplicativo **FastAPI**:


{* ../../docs_src/app_testing/main.py *}

### Arquivo de teste { #testing-file }

Então você poderia ter um arquivo `test_main.py` com seus testes. Ele poderia estar no mesmo pacote Python (o mesmo diretório com um arquivo `__init__.py`):

``` hl_lines="5"
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Como esse arquivo está no mesmo pacote, você pode usar importações relativas para importar o objeto `app` do módulo `main` (`main.py`):

{* ../../docs_src/app_testing/test_main.py hl[3] *}

...e ter o código para os testes como antes.

## Testando: exemplo estendido { #testing-extended-example }

Agora vamos estender este exemplo e adicionar mais detalhes para ver como testar diferentes partes.

### Arquivo de aplicativo **FastAPI** estendido { #extended-fastapi-app-file }

Vamos continuar com a mesma estrutura de arquivo de antes:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

Digamos que agora o arquivo `main.py` com seu aplicativo **FastAPI** tenha algumas outras **operações de rotas**.

Ele tem uma operação `GET` que pode retornar um erro.

Ele tem uma operação `POST` que pode retornar vários erros.

Ambas as *operações de rotas* requerem um cabeçalho `X-Token`.

//// tab | Python 3.10+

```Python
{!> ../../docs_src/app_testing/app_b_an_py310/main.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/app_testing/app_b_an_py39/main.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/app_testing/app_b_an/main.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python
{!> ../../docs_src/app_testing/app_b_py310/main.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python
{!> ../../docs_src/app_testing/app_b/main.py!}
```

////

### Arquivo de teste estendido { #extended-testing-file }

Você pode então atualizar `test_main.py` com os testes estendidos:

{* ../../docs_src/app_testing/app_b/test_main.py *}

Sempre que você precisar que o cliente passe informações na requisição e não souber como, você pode pesquisar (no Google) como fazer isso no `httpx`, ou até mesmo como fazer isso com `requests`, já que o design do HTTPX é baseado no design do Requests.

Depois é só fazer o mesmo nos seus testes.

Por exemplo:

* Para passar um parâmetro *path* ou *query*, adicione-o à própria URL.
* Para passar um corpo JSON, passe um objeto Python (por exemplo, um `dict`) para o parâmetro `json`.
* Se você precisar enviar *Dados de Formulário* em vez de JSON, use o parâmetro `data`.
* Para passar *headers*, use um `dict` no parâmetro `headers`.
* Para *cookies*, um `dict` no parâmetro `cookies`.

Para mais informações sobre como passar dados para o backend (usando `httpx` ou `TestClient`), consulte a <a href="https://www.python-httpx.org" class="external-link" target="_blank">documentação do HTTPX</a>.

/// info | Informação

Observe que o `TestClient` recebe dados que podem ser convertidos para JSON, não para modelos Pydantic.

Se você tiver um modelo Pydantic em seu teste e quiser enviar seus dados para o aplicativo durante o teste, poderá usar o `jsonable_encoder` descrito em [Codificador compatível com JSON](encoder.md){.internal-link target=_blank}.

///

## Execute-o { #run-it }

Depois disso, você só precisa instalar o `pytest`.

Certifique-se de criar um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, ativá-lo e instalá-lo, por exemplo:

<div class="termy">

```console
$ pip install pytest

---> 100%
```

</div>

Ele detectará os arquivos e os testes automaticamente, os executará e informará os resultados para você.

Execute os testes com:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 6 items

---> 100%

test_main.py <span style="color: green; white-space: pre;">......                            [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>
