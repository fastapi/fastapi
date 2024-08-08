# Sub Aplicações - Montagens

Se você precisar ter duas aplicações FastAPI independentes, cada uma com seu próprio OpenAPI e suas próprias interfaces de documentação, você pode ter um aplicativo principal e "montar" uma (ou mais) sub-aplicações.

## Montando uma aplicação **FastAPI**

"Montar" significa adicionar uma aplicação completamente "independente" em um caminho específico, que então se encarrega de lidar com tudo sob esse caminho, com as operações de rota declaradas nessa sub-aplicação.

### Aplicação de nível superior

Primeiro, crie a aplicação principal, de nível superior, **FastAPI**, e suas *operações de rota*:

```Python hl_lines="3  6-8"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Sub-aplicação

Em seguida, crie sua sub-aplicação e suas *operações de rota*.

Essa sub-aplicação é apenas outra aplicação FastAPI padrão, mas esta é a que será "montada":

```Python hl_lines="11  14-16"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Monte a sub-aplicação

Na sua aplicação de nível superior, `app`, monte a sub-aplicação, `subapi`.

Neste caso, ela será montada no caminho `/subapi`:

```Python hl_lines="11  19"
{!../../../docs_src/sub_applications/tutorial001.py!}
```

### Verifique a documentação automática da API

Agora, execute `uvicorn` com a aplicação principal, se o seu arquivo for `main.py`, seria:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

E abra a documentação em <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá a documentação automática da API para a aplicação principal, incluindo apenas suas próprias _operações de rota_:

<img src="/img/tutorial/sub-applications/image01.png">

E então, abra a documentação para a sub-aplicação, em <a href="http://127.0.0.1:8000/subapi/docs" class="external-link" target="_blank">http://127.0.0.1:8000/subapi/docs</a>.

Você verá a documentação automática da API para a sub-aplicação, incluindo apenas suas próprias _operações de rota_, todas sob o prefixo de sub-caminho correto `/subapi`:

<img src="/img/tutorial/sub-applications/image02.png">

Se você tentar interagir com qualquer uma das duas interfaces de usuário, elas funcionarão corretamente, porque o navegador será capaz de se comunicar com cada aplicação ou sub-aplicação específica.

### Detalhes Técnicos: `root_path`

Quando você monta uma sub-aplicação como descrito acima, o FastAPI se encarrega de comunicar o caminho de montagem para a sub-aplicação usando um mecanismo da especificação ASGI chamado `root_path`.

Dessa forma, a sub-aplicação saberá usar esse prefixo de caminho para a interface de documentação.

E a sub-aplicação também poderia ter suas próprias sub-aplicações montadas e tudo funcionaria corretamente, porque o FastAPI lida com todos esses `root_path`s automaticamente.

Você aprenderá mais sobre o `root_path` e como usá-lo explicitamente na seção sobre [Atrás de um Proxy](behind-a-proxy.md){.internal-link target=_blank}.
