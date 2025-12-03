# Formulários e Arquivos da Requisição { #request-forms-and-files }

Você pode definir arquivos e campos de formulário ao mesmo tempo usando `File` e `Form`.

/// info | Informação

Para receber arquivos carregados e/ou dados de formulário, primeiro instale <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>.

Certifique-se de criar um [ambiente virtual](../virtual-environments.md){.internal-link target=_blank}, ativá-lo e então instalar, por exemplo:

```console
$ pip install python-multipart
```

///

## Importe `File` e `Form` { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[3] *}

## Defina parâmetros de `File` e `Form` { #define-file-and-form-parameters }

Crie parâmetros de arquivo e formulário da mesma forma que você faria para `Body` ou `Query`:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py39.py hl[10:12] *}

Os arquivos e campos de formulário serão carregados como dados de formulário e você receberá os arquivos e campos de formulário.

E você pode declarar alguns dos arquivos como `bytes` e alguns como `UploadFile`.

/// warning | Atenção

Você pode declarar vários parâmetros `File` e `Form` em uma *operação de caminho*, mas não é possível declarar campos `Body` para receber como JSON, pois a requisição terá o corpo codificado usando `multipart/form-data` ao invés de `application/json`.

Isso não é uma limitação do **FastAPI**, é parte do protocolo HTTP.

///

## Recapitulando { #recap }

Usar `File` e `Form` juntos quando precisar receber dados e arquivos na mesma requisição.
