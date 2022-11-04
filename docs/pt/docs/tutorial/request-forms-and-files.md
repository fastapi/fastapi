# Formulários e Arquivos da Requisição

Você pode definir arquivos e campos de formulário ao mesmo tempo usando `File` e `Form`.

!!! info "Informação"
    Para receber arquivos carregados e/ou dados de formulário, primeiro instale <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

    Por exemplo: `pip install python-multipart`.


## Importe `File` e `Form`

```Python hl_lines="1"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

## Defina parâmetros de `File` e `Form`

Crie parâmetros de arquivo e formulário da mesma forma que você faria para `Body` ou `Query`:

```Python hl_lines="8"
{!../../../docs_src/request_forms_and_files/tutorial001.py!}
```

Os arquivos e campos de formulário serão carregados como dados de formulário e você receberá os arquivos e campos de formulário.

E você pode declarar alguns dos arquivos como `bytes` e alguns como `UploadFile`.

!!! warning "Aviso"
    Você pode declarar vários parâmetros `File` e `Form` em uma *operação de caminho*, mas não é possível declarar campos `Body` para receber como JSON, pois a requisição terá o corpo codificado usando `multipart/form-data` ao invés de `application/json`.

    Isso não é uma limitação do **FastAPI** , é parte do protocolo HTTP.

## Recapitulando

Usar `File` e `Form` juntos quando precisar receber dados e arquivos na mesma requisição.
