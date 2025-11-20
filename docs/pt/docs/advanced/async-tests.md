# Testes Assíncronos { #async-tests }

Você já viu como testar as suas aplicações **FastAPI** utilizando o `TestClient` que é fornecido. Até agora, você viu apenas como escrever testes síncronos, sem utilizar funções `async`.

Ser capaz de utilizar funções assíncronas em seus testes pode ser útil, por exemplo, quando você está realizando uma consulta em seu banco de dados de maneira assíncrona. Imagine que você deseja testar realizando requisições para a sua aplicação FastAPI e depois verificar que a sua aplicação inseriu corretamente as informações no banco de dados, ao utilizar uma biblioteca assíncrona para banco de dados.

Vamos ver como nós podemos fazer isso funcionar.

## pytest.mark.anyio { #pytest-mark-anyio }

Se quisermos chamar funções assíncronas em nossos testes, as nossas funções de teste precisam ser assíncronas. O AnyIO oferece um plugin bem legal para isso, que nos permite especificar que algumas das nossas funções de teste precisam ser chamadas de forma assíncrona.

## HTTPX { #httpx }

Mesmo que a sua aplicação **FastAPI** utilize funções normais com `def` no lugar de `async def`, ela ainda é uma aplicação `async` por baixo dos panos.

O `TestClient` faz algumas mágicas para invocar a aplicação FastAPI assíncrona em suas funções `def` normais, utilizando o pytest padrão. Porém a mágica não acontece mais quando nós estamos utilizando dentro de funções assíncronas. Ao executar os nossos testes de forma assíncrona, nós não podemos mais utilizar o `TestClient` dentro das nossas funções de teste.

O `TestClient` é baseado no <a href="https://www.python-httpx.org" class="external-link" target="_blank">HTTPX</a>, e felizmente nós podemos utilizá-lo diretamente para testar a API.

## Exemplo { #example }

Para um exemplos simples, vamos considerar uma estrutura de arquivos semelhante ao descrito em [Bigger Applications](../tutorial/bigger-applications.md){.internal-link target=_blank} e [Testing](../tutorial/testing.md){.internal-link target=_blank}:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
```

O arquivo `main.py` teria:

{* ../../docs_src/async_tests/main.py *}

O arquivo `test_main.py` teria os testes para para o arquivo `main.py`, ele poderia ficar assim:

{* ../../docs_src/async_tests/test_main.py *}

## Executá-lo { #run-it }

Você pode executar os seus testes normalmente via:

<div class="termy">

```console
$ pytest

---> 100%
```

</div>

## Em Detalhes { #in-detail }

O marcador `@pytest.mark.anyio` informa ao pytest que esta função de teste deve ser invocada de maneira assíncrona:

{* ../../docs_src/async_tests/test_main.py hl[7] *}

/// tip | Dica

Note que a função de teste é `async def` agora, no lugar de apenas `def` como quando estávamos utilizando o `TestClient` anteriormente.

///

Então podemos criar um `AsyncClient` com a aplicação, e enviar requisições assíncronas para ela utilizando `await`.

{* ../../docs_src/async_tests/test_main.py hl[9:12] *}

Isso é equivalente a:

```Python
response = client.get('/')
```

...que nós utilizamos para fazer as nossas requisições utilizando o `TestClient`.

/// tip | Dica

Note que nós estamos utilizando async/await com o novo `AsyncClient` - a requisição é assíncrona.

///

/// warning | Atenção

Se a sua aplicação depende de eventos de lifespan, o `AsyncClient` não acionará estes eventos. Para garantir que eles são acionados, utilize o `LifespanManager` do <a href="https://github.com/florimondmanca/asgi-lifespan#usage" class="external-link" target="_blank">florimondmanca/asgi-lifespan</a>.

///

## Outras Chamadas de Funções Assíncronas { #other-asynchronous-function-calls }

Como a função de teste agora é assíncrona, você pode chamar (e `await`) outras funções `async` além de enviar requisições para a sua aplicação FastAPI em seus testes, exatamente como você as chamaria em qualquer outro lugar do seu código.

/// tip | Dica

Se você se deparar com um `RuntimeError: Task attached to a different loop` ao integrar funções assíncronas em seus testes (e.g. ao utilizar o <a href="https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop" class="external-link" target="_blank">MotorClient do MongoDB</a>) Lembre-se de instanciar objetos que precisam de um loop de eventos (*event loop*) apenas em funções assíncronas, e.g. um callback `@app.on_event("startup")`.

///
