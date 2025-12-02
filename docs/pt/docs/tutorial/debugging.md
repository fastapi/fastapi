# Depuração { #debugging }

Você pode conectar o depurador no seu editor, por exemplo, com o Visual Studio Code ou PyCharm.

## Chamar `uvicorn` { #call-uvicorn }

Em sua aplicação FastAPI, importe e execute `uvicorn` diretamente:

{* ../../docs_src/debugging/tutorial001.py hl[1,15] *}

### Sobre `__name__ == "__main__"` { #about-name-main }

O objetivo principal de `__name__ == "__main__"` é ter algum código que seja executado quando seu arquivo for chamado com:

<div class="termy">

```console
$ python myapp.py
```

</div>

mas não é chamado quando outro arquivo o importa, como em:

```Python
from myapp import app
```

#### Mais detalhes { #more-details }

Digamos que seu arquivo se chama `myapp.py`.

Se você executá-lo com:

<div class="termy">

```console
$ python myapp.py
```

</div>

então a variável interna `__name__` no seu arquivo, criada automaticamente pelo Python, terá como valor a string `"__main__"`.

Então, a seção:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

vai executar.

---

Isso não acontecerá se você importar esse módulo (arquivo).

Então, se você tiver outro arquivo `importer.py` com:

```Python
from myapp import app

# Mais um pouco de código
```

nesse caso, a variável criada automaticamente dentro de `myapp.py` não terá a variável `__name__` com o valor `"__main__"`.

Então, a linha:

```Python
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

não será executada.

/// info | Informação

Para mais informações, consulte <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">a documentação oficial do Python</a>.

///

## Execute seu código com seu depurador { #run-your-code-with-your-debugger }

Como você está executando o servidor Uvicorn diretamente do seu código, você pode chamar seu programa Python (sua aplicação FastAPI) diretamente do depurador.

---

Por exemplo, no Visual Studio Code, você pode:

* Ir para o painel "Debug".
* "Add configuration...".
* Selecionar "Python"
* Executar o depurador com a opção "`Python: Current File (Integrated Terminal)`".

Em seguida, ele iniciará o servidor com seu código **FastAPI**, parará em seus pontos de interrupção, etc.

Veja como pode parecer:

<img src="/img/tutorial/debugging/image01.png">

---

Se você usar o Pycharm, você pode:

* Abrir o menu "Executar".
* Selecionar a opção "Depurar...".
* Então um menu de contexto aparece.
* Selecionar o arquivo para depurar (neste caso, `main.py`).

Em seguida, ele iniciará o servidor com seu código **FastAPI**, parará em seus pontos de interrupção, etc.

Veja como pode parecer:

<img src="/img/tutorial/debugging/image02.png">
