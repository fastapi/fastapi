# Arquivos de Requisição

Você pode definir arquivos para serem enviados pelo cliente usando `File`.

/// info | Informação

Para receber arquivos enviados, primeiro instale o <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Garanta que você criou um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, o ativou e então o instalou, por exemplo:

```console
$ pip install python-multipart
```

Isso é necessário, visto que os arquivos enviados são enviados como "dados de formulário".

///

## Importe `File`

Importe `File` e `UploadFile` de `fastapi`:

//// tab | Python 3.9+

```Python hl_lines="3"
{!> ../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1"
{!> ../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="1"
{!> ../../docs_src/request_files/tutorial001.py!}
```

////

## Definir Parâmetros `File`

Crie parâmetros de arquivo da mesma forma que você faria para `Body` ou `Form`:

//// tab | Python 3.9+

```Python hl_lines="9"
{!> ../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8"
{!> ../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="7"
{!> ../../docs_src/request_files/tutorial001.py!}
```

////

/// info | Informação

`File` é uma classe que herda diretamente de `Form`. 

Mas lembre-se que quando você importa `Query`, `Path`, `File` e outros de `fastapi`, eles são, na verdade, funções que retornam classes especiais.

///

/// tip | Dica

Para declarar corpos de arquivos, você precisa usar `File`, caso contrário, os parâmetros seriam interpretados como parâmetros de consulta ou parâmetros de corpo (JSON).

///

Os arquivos serão enviados como "dados de formulário".

Se você declarar o tipo do parâmetro da função da sua *operação de rota* como `bytes`, o **FastAPI** lerá o arquivo para você e você receberá o conteúdo como `bytes`.

Mantenha em mente que isso significa que todo o conteúdo será armazenado na memória. Isso funcionará bem para arquivos pequenos.

Mas há muitos casos em que você pode se beneficiar do uso de `UploadFile`.

## Parâmetros de Arquivo com `UploadFile`

Defina um parâmetro de arquivo com um tipo de `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="14"
{!> ../../docs_src/request_files/tutorial001_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="13"
{!> ../../docs_src/request_files/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="12"
{!> ../../docs_src/request_files/tutorial001.py!}
```

////

Utilizar `UploadFile` tem várias vantagens sobre `bytes`:

* Você não precisa utilizar o `File()` no valor padrão do parâmetro.
* Ele utiliza um arquivo "spooled":
    * Um arquivo armazenado na memória até um limite máximo de tamanho, e após passar esse limite, ele será armazenado no disco.
* Isso significa que funcionará bem para arquivos grandes como imagens, vídeos, binários grandes, etc., sem consumir toda a memória.
* Você pode receber metadados do arquivo enviado.
* Ele tem uma <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> interface `assíncrona`.
* Ele expõe um objeto python <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> que você pode passar diretamente para outras bibliotecas que esperam um objeto semelhante a um arquivo("file-like").

### `UploadFile`

`UploadFile` tem os seguintes atributos:

* `filename`: Uma `str` com o nome do arquivo original que foi enviado (por exemplo, `myimage.jpg`).
* `content_type`: Uma `str` com o tipo de conteúdo (tipo MIME / tipo de mídia) (por exemplo, `image/jpeg`).
* `file`: Um <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (um <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> objeto). Este é o objeto de arquivo Python que você pode passar diretamente para outras funções ou bibliotecas que esperam um objeto semelhante a um arquivo("file-like").

`UploadFile` tem os seguintes métodos `assíncronos`. Todos eles chamam os métodos de arquivo correspondentes por baixo dos panos (usando o `SpooledTemporaryFile` interno).

* `write(data)`: Escreve `data` (`str` ou `bytes`) no arquivo.
* `read(size)`: Lê `size` (`int`) bytes/caracteres do arquivo.
* `seek(offset)`: Vai para o byte na posição `offset` (`int`) no arquivo.
    * Por exemplo, `await myfile.seek(0)` irá para o início do arquivo.
    * Isso é especialmente útil se você executar `await myfile.read()` uma vez e precisar ler o conteúdo novamente.
* `close()`: Fecha o arquivo.

Como todos esses métodos são métodos `assíncronos`, você precisa "aguardar" por eles.

Por exemplo, dentro de uma função de *operação de rota* `assíncrona`, você pode obter o conteúdo com:

```Python
contents = await myfile.read()
```

Se você estiver dentro de uma função de *operação de rota* normal `def`, você pode acessar o `UploadFile.file` diretamente, por exemplo:

```Python
contents = myfile.file.read()
```

/// note | Detalhes Técnicos do `async`

Quando você usa os métodos `async`, o **FastAPI** executa os métodos de arquivo em um threadpool e aguarda por eles.

///

/// note | "Detalhes Técnicos do Starlette"

O `UploadFile` do ***FastAPI** herda diretamente do `UploadFile` do **Starlette** , mas adiciona algumas partes necessárias para torná-lo compatível com o **Pydantic** e as outras partes do FastAPI.

///

## O que é "Form Data"

O jeito que os formulários HTML (`<form></form>`) enviam os dados para o servidor normalmente usa uma codificação "especial" para esses dados, a qual é diferente do JSON.

**FastAPI** se certificará de ler esses dados do lugar certo, ao invés de JSON.

/// note | "Detalhes Técnicos"

Dados de formulários normalmente são codificados usando o "media type" (tipo de mídia) `application/x-www-form-urlencoded` quando não incluem arquivos.

Mas quando o formulário inclui arquivos, ele é codificado como `multipart/form-data`. Se você usar `File`, o **FastAPI** saberá que tem que pegar os arquivos da parte correta do corpo da requisição.

Se você quiser ler mais sobre essas codificações e campos de formulário, vá para a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr> web docs para <code>POST</code></a>.

///

/// warning | Aviso

Você pode declarar multiplos parâmetros `File` e `Form` em uma *operação de rota*, mas você não pode declarar campos `Body` que você espera receber como JSON, pois a requisição terá o corpo codificado usando `multipart/form-data` ao invés de `application/json`.

Isso não é uma limitação do **FastAPI**, é parte do protocolo HTTP.

///

## Upload de Arquivo Opcional

Você pode tornar um arquivo opcional usando anotações de tipo padrão e definindo um valor padrão de `None`:

//// tab | Python 3.10+

```Python hl_lines="9  17"
{!> ../../docs_src/request_files/tutorial001_02_an_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="9  17"
{!> ../../docs_src/request_files/tutorial001_02_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="10  18"
{!> ../../docs_src/request_files/tutorial001_02_an.py!}
```

////

//// tab | Python 3.10+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="7  15"
{!> ../../docs_src/request_files/tutorial001_02_py310.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira usar a versão `Annotated` se possível.

///

```Python hl_lines="9  17"
{!> ../../docs_src/request_files/tutorial001_02.py!}
```

////

## `UploadFile` com Metadados Adicionais

Você também pode usar `File()` com `UploadFile`, por exemplo, para definir metadados adicionais:

//// tab | Python 3.9+

```Python hl_lines="9  15"
{!> ../../docs_src/request_files/tutorial001_03_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="8  14"
{!> ../../docs_src/request_files/tutorial001_03_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="7  13"
{!> ../../docs_src/request_files/tutorial001_03.py!}
```

////

## Uploads de Múltiplos Arquivos

É possível realizar o upload de vários arquivos ao mesmo tempo.

Eles serão associados ao mesmo "campo de formulário" enviado usando "dados de formulário".

Para usar isso, declare uma lista de `bytes` ou `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="10  15"
{!> ../../docs_src/request_files/tutorial002_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="11  16"
{!> ../../docs_src/request_files/tutorial002_an.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="8  13"
{!> ../../docs_src/request_files/tutorial002_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="10  15"
{!> ../../docs_src/request_files/tutorial002.py!}
```

////

Você receberá, tal como declarado, uma `list` de `bytes` ou `UploadFile`.

/// note | "Detalhes Técnicos"

Você pode também pode usar `from starlette.responses import HTMLResponse`.

**FastAPI** providencia o mesmo `starlette.responses` que `fastapi.responses` apenas como uma conveniência para você, o desenvolvedor. Mas a maioria das respostas disponíveis vem diretamente do Starlette.

///

### Uploads de Múltiplos Arquivos com Metadados Adicionais

Da mesma forma de antes, você pode usar `File()` para definir parâmetros adicionais, mesmo para `UploadFile`:

//// tab | Python 3.9+

```Python hl_lines="11  18-20"
{!> ../../docs_src/request_files/tutorial003_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="12  19-21"
{!> ../../docs_src/request_files/tutorial003_an.py!}
```

////

//// tab | Python 3.9+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="9  16"
{!> ../../docs_src/request_files/tutorial003_py39.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip | Dica

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="11  18"
{!> ../../docs_src/request_files/tutorial003.py!}
```

////

## Recapitulando

Utilize `File`, `bytes` e `UploadFile` para declarar arquivos a serem enviados na requisição, enviados como dados de formulário.
