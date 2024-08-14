# Arquivos de Requisição

Você pode definir arquivos para serem enviados para o cliente utilizando `File`.

/// info

Para receber arquivos compartilhados, primeiro  instale <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

E.g. `pip install python-multipart`.

Isso se deve por que arquivos enviados são enviados como "dados de formulário".

///

## Importe `File`

Importe `File` e `UploadFile` do `fastapi`:

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="1"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

## Defina os parâmetros de `File`

Cria os parâmetros do arquivo da mesma forma que você faria para `Body` ou `Form`:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="7"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

/// info | Informação

`File` é uma classe que herda diretamente de `Form`.

Mas lembre-se que quando você importa `Query`,`Path`, `File`, entre outros, do `fastapi`, essas são na verdade funções que retornam classes especiais.

///

/// tip | Dica

Para declarar o corpo de arquivos, você precisa utilizar `File`, do contrário os parâmetros seriam interpretados como parâmetros de consulta ou corpo (JSON) da requisição.

///

Os arquivos serão enviados como "form data".

Se você declarar o tipo do seu parâmetro na sua *função de operação de rota* como `bytes`, o **FastAPI** irá ler o arquivo para você e você receberá o conteúdo como `bytes`.

Lembre-se que isso significa que o conteúdo inteiro será armazenado em memória. Isso funciona bem para arquivos pequenos.

Mas existem vários casos em que você pode se beneficiar ao usar `UploadFile`.

## Parâmetros de arquivo com `UploadFile`

Defina um parâmetro de arquivo com o tipo `UploadFile`

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="13"
{!> ../../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="12"
{!> ../../../docs_src/request_files/tutorial001.py!}
```

////

Utilizando `UploadFile` tem várias vantagens sobre `bytes`:

* Você não precisa utilizar `File()` como o valor padrão do parâmetro.
* A classe utiliza um arquivo em "spool":
    * Um arquivo guardado em memória até um tamanho máximo, depois desse limite ele é guardado em disco.
* Isso significa que a classe funciona bem com arquivos grandes como imagens, vídeos, binários extensos, etc. Sem consumir toda a memória.
* Você pode obter metadados do arquivo enviado.
* Ela possui uma interface <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">semelhante a arquivos</a> `async`.
* Ela expõe um objeto python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> que você pode repassar para bibliotecas que esperam um objeto com comportamento de arquivo.

### `UploadFile`

`UploadFile` tem os seguintes atributos:

* `filename`: Uma string (`str`) com o nome original do arquivo enviado (e.g. `myimage.jpg`).
* `content-type`: Uma `str` com o tipo do conteúdo (tipo MIME / media) (e.g. `image/jpeg`).
* `file`: Um objeto do tipo <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (um objeto <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a>). O arquivo propriamente dito que você pode passar diretamente para outras funções ou bibliotecas que esperam um objeto "file-like".

`UploadFile` tem os seguintes métodos `async`. Todos eles chamam os métodos de arquivos por baixo dos panos (usando o objeto `SpooledTemporaryFile` interno).

* `write(data)`: escreve dados (`data`) em `str` ou `bytes` no arquivo.
* `read(size)`: Lê um número de bytes/caracteres de acordo com a quantidade `size` (`int`).
* `seek(offset)`: Navega para o byte na posição `offset` (`int`) do arquivo.
    * E.g., `await myfile.seek(0)` navegaria para o ínicio do arquivo.
    * Isso é especialmente útil se você executar `await myfile.read()` uma vez e depois precisar ler os conteúdos do arquivo de novo.
* `close()`: Fecha o arquivo.

Como todos esses métodos são assíncronos (`async`) você precisa esperar ("await") por eles.

Por exemplo, dentro de uma *função de operação de rota* assíncrona você pode obter os conteúdos com:

```Python
contents = await myfile.read()
```

Se você estiver dentro de uma *função de operação de rota* definida normalmente com `def`, você pode acessar `UploadFile.file` diretamente, por exemplo:

```Python
contents = myfile.file.read()
```

/// note | Detalhes técnicos do `async`

Quando você utiliza métodos assíncronos, o **FastAPI** executa os métodos do arquivo em uma threadpool e espera por eles.

///

/// note | Detalhes técnicos do Starlette

O `UploadFile` do **FastAPI** herda diretamente do `UploadFile` do **Starlette**, mas adiciona algumas funcionalidades necessárias para ser compatível com o **Pydantic**

///

## O que é "Form Data"

A forma como formulários HTML(`<form></form>`) enviam dados para o servidor normalmente utilizam uma codificação "especial" para esses dados, que é diferente do JSON.

O **FastAPI** garante que os dados serão lidos da forma correta, em vez do JSON.

/// note | Detalhes Técnicos

Dados vindos de formulários geralmente tem a codificação com o "media type" `application/x-www-form-urlencoded` quando estes não incluem arquivos.

Mas quando os dados incluem arquivos, eles são codificados como `multipart/form-data`. Se você utilizar `File`, **FastAPI** saberá que deve receber os arquivos da parte correta do corpo da requisição.

Se você quer ler mais sobre essas codificações e campos de formulário, veja a documentação online da <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> sobre <code> POST</code> </a>.

///

/// warning | Aviso

Você pode declarar múltiplos parâmetros `File` e `Form` em uma *operação de rota*, mas você não pode declarar campos `Body`que seriam recebidos como JSON junto desses parâmetros, por que a codificação do corpo da requisição será `multipart/form-data` em vez de `application/json`.

Isso não é uma limitação do **FastAPI**, é uma parte do protocolo HTTP.

///

## Arquivo de upload opcional

Você pode definir um arquivo como opcional utilizando as anotações de tipo padrão e definindo o valor padrão como `None`:

//// tab | Python 3.10+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10  18"
{!> ../../../docs_src/request_files/tutorial001_02_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated`, se possível

///

```Python hl_lines="7  15"
{!> ../../../docs_src/request_files/tutorial001_02_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated`, se possível

///

```Python hl_lines="9  17"
{!> ../../../docs_src/request_files/tutorial001_02.py!}
```

////

## `UploadFile` com Metadados Adicionais

Você também pode utilizar `File()` com `UploadFile`, por exemplo, para definir metadados adicionais:

//// tab | Python 3.9+

```Python hl_lines="9  15"
{!> ../../../docs_src/request_files/tutorial001_03_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8  14"
{!> ../../../docs_src/request_files/tutorial001_03_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível

///

```Python hl_lines="7  13"
{!> ../../../docs_src/request_files/tutorial001_03.py!}
```

////

## Envio de Múltiplos Arquivos

É possível enviar múltiplos arquivos ao mesmo tmepo.

Ele ficam associados ao mesmo "campo do formulário" enviado com "form data".

Para usar isso, declare uma lista de `bytes` ou `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11  16"
{!> ../../../docs_src/request_files/tutorial002_an.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível

///

```Python hl_lines="8  13"
{!> ../../../docs_src/request_files/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível

///

```Python hl_lines="10  15"
{!> ../../../docs_src/request_files/tutorial002.py!}
```

////

Você irá receber, como delcarado uma lista (`list`) de `bytes` ou `UploadFile`s,

/// note | Detalhes Técnicos

Você também poderia utilizar `from starlette.responses import HTMLResponse`.

O **FastAPI** fornece as mesmas `starlette.responses` como `fastapi.responses` apenas como um facilitador para você, desenvolvedor. Mas a maior parte das respostas vem diretamente do Starlette.

///

### Enviando Múltiplos Arquivos com Metadados Adicionais

E da mesma forma que antes, você pode utilizar `File()` para definir parâmetros adicionais, até mesmo para `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="11  18-20"
{!> ../../../docs_src/request_files/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12  19-21"
{!> ../../../docs_src/request_files/tutorial003_an.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="9  16"
{!> ../../../docs_src/request_files/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Utilize a versão com `Annotated` se possível.

///

```Python hl_lines="11  18"
{!> ../../../docs_src/request_files/tutorial003.py!}
```

////

## Recapitulando

Use `File`, `bytes` e `UploadFile` para declarar arquivos que serão enviados na requisição, enviados como dados do formulário.
