# Debugando
 
Você pode conectar o debugger no seu editor, por exemplo com o Visual Studio Code ou PyCharm.
 
## Chamar `uvicorn`
 
Na sua aplicação FastAPI, importe e rode `uvicorn` diretamente:
 
```Python hl_lines="1  15"
{!../../../docs_src/debugging/tutorial001.py!}
```
 
### Sobre `__name__ == "__main__"`
 
O principal propósito do `__name__ == "__main__"` é ter um código que é executado quando o seu arquivo é chamado com:
 
<div class="termy">
 
```console
$ python myapp.py
```
 
</div>
 
mas não é chamado quando outro arquivo o importa, como em:
 
```Python
from myapp import app
```
 
#### Mais detalhes
 
Digamos que o seu arquivo tem o nome de `myapp.py`.
 
Se você rodá-lo com:
 
<div class="termy">
 
```console
$ python myapp.py
```
 
</div>
 
a variável interna `__name__` no seu arquivo, criada automaticamente pelo Python, vai ter como valor a string `"__main__"`.
 
Então, a sessão:
 
```Python
   uvicorn.run(app, host="0.0.0.0", port=8000)
```
 
vai rodar.
 
---
 
Isso não vai acontecer se você importar aquele módulo (arquivo).
 
Então, se você tiver outro arquivo `importer.py` com:
 
```Python
from myapp import app
 
# Some more code
```
 
nesse caso, a variável automática dentro de `myapp.py` não terá a variável `__name__` com o valor de `"__main__"`.
 
Então, a linha:
 
```Python
   uvicorn.run(app, host="0.0.0.0", port=8000)
```
 
não será executada.
 
!!! info "Informação"
   Para mais informações, olhe <a href="https://docs.python.org/3/library/__main__.html" class="external-link" target="_blank">a documentação oficial do Python</a>.
 
## Rode o seu código com o seu debugger
 
Por conta de você estar rodando o servidor Uvicorn diretamente do seu código, você pode chamar seu programa Python (a sua aplicação FastAPI) diretamente do debugger.
 
---
 
Por exemplo, no Visual Studio Code, você pode:
 
* Ir para o painel "Debug".
* "Adicionar configuração...".
* Selecionar "Python"
* Rodar o debugger com a opção "`Python: Arquivo atual (Terminal Integrado)`".
 
Isso então iniciará o servidor com o seu código **FastAPI**, irá parar nos seus breakpoints, etc.
 
Aqui está como pode parecer:
 
<img src="/img/tutorial/debugging/image01.png">
 
---
 
Se você usar Pycharm, você pode
 
* Abrir o menu "Run".
* Selecionar a opção "Debug...".
* Então, um menu de contexto vai aparecer.
* Selecione o arquivo para debugar (nesse caso, `main.py`).
 
Isso então iniciará o servidor com o seu código **FastAPI**, irá parar nos seus breakpoints, etc.
 
Aqui está como pode parecer:
 
<img src="/img/tutorial/debugging/image02.png">