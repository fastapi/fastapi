# Tutorial - Guia de Usuário - Introdução

Esse tutorial mostra como usar o **FastAPI** com a maior parte de seus recursos, passo a passo.

Cada seção constrói, gradualmente, sobre as anteriores, mas sua estrutura são tópicos separados, para que você possa ir a qualquer um específico e resolver suas necessidades específicas de API.

Ele também foi feito como referência futura.

Então você poderá voltar e ver exatamente o que precisar.

## Rode o código

Todos os blocos de código podem ser copiados e utilizados diretamente (eles são, na verdade, arquivos Python testados).

Para rodar qualquer um dos exemplos, copie o codigo para um arquivo `main.py`, e inicie o `uvivorn` com:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

É **ALTAMENTE recomendado** que você escreva ou copie o código, edite-o e rode-o localmente.

Usá-lo em seu editor é o que realmente te mostra os benefícios do FastAPI, ver quão pouco código você tem que escrever, todas as conferências de tipo, auto completações etc.

---

## Instale o FastAPI

O primeiro passo é instalar o FastAPI.

Para o tutorial, você deve querer instalá-lo com todas as dependências e recursos opicionais.

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...isso também inclui o `uvicorn`, que você pode usar como o servidor que rodará seu código.

!!! nota
    Você também pode instalar parte por parte.

    Isso é provavelmente o que você faria quando você quisesse lançar sua aplicação em produção:

    ```
    pip install fastapi
    ```

    Também instale o `uvicorn` para funcionar como servidor:

    ```
    pip install "uvicorn[standard]"
    ```

    E o mesmo para cada dependência opcional que você quiser usar.

## Guia Avançado de Usuário

Há também um **Guia Avançado de Usuário** que você pode ler após esse **Tutorial - Guia de Usuário**.

O **Guia Avançado de Usuário** constrói sobre esse, usa os mesmos conceitos e te ensina alguns recursos extras.

Mas você deveria ler primeiro o **Tutorial - Guia de Usuário** (que você está lendo agora).

Ele foi projetado para que você possa construir uma aplicação completa com apenas o **Tutorial - Guia de Usuário**, e então estendê-la de diferentes formas, dependendo das suas necessidades, usando algumas ideias adicionais do **Guia Avançado de Usuário**.
