# API Key Auth

Otro método de autenticación, particularmente para communicación máquina-a-máquina (M2M) es un "API key". Un API key es una cadena de que la aplicación espera recibir con cada request del cliente. El API key puede ser enviado como "header", como "cookie", o como parámetro de query.

<!-- TODO: currently we return 403 in the implementation! discuss with @tiangolo et al -->
Si el API key no se incluye o es inválido, la aplicación devuelve un error HTTP 401 "Unauthorized".

/// warning

En general, se recomienda usar API keys para uso programático solamente. También
se recomienda mantener el API Key como un secreto entre el cliente autentificado
y el servidor. Dependiendo de tus requisitos, esto podría requerir tener el
API key como variable de entorno o en una base de datos cifrada (en vez de en pleno
código, como en los ejemplos que siguen), y hasta proveer una API key distinta
para cada cliente que intente autentificar.

///

/// tip
Puede referirse al [API Reference](../../reference/security/index.md#api-key-security-schemes){.internal-link target=_blank} para más detalles en cuanto a los esquemas discutidos.
///

## API Key como Header

* Importe `APIKeyHeader`.
* Cree una instancia de `APIKeyHeader`, especificando el nombre del header a probar.
* Cree una función `verify_api_key` que verifique el API Key.
* Añada un `Depends(verify_api_key)` globalmente o a un sólo "endpoint" (ver ejemplo).

```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial008.py!}
```

El cliente tendrá que enviar un request con el header correcto:

```http
GET /secure-data HTTP/1.1
X-API-Key: mysecretapikey
```

## API Key como Cookie

El proceso es similar al de `APIKeyHeader`, excepto que usamos `APIKeyCookie`:

```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial009.py!}
```

El cliente tendrá que enviar la API Key como cookie (recuerde que se distingue mayúscula y minúscula en el nombre de los cookies):

```http
GET /secure-data HTTP/1.1
Cookie: X-API-KEY=mysecretapikey
```

## API Key como parámetro de Query

/// warning
Enviar API keys como párametro de query no es muy seguro, pues pueden
ser vistos en el URL del request (por ejemplo, en tu browser o en los registros de acceso del servidor).
///

De nuevo, el proceso es similar a los anteriores, excepto usando `APIKeyQuery`:

```Python hl_lines="5  7  14  23"
{!../../docs_src/security/tutorial010.py!}
```

El cliente deberá enviar el API Key como parámetro:

```http
GET /secure-data?x-api-key=mysecretapikey HTTP/1.1
```

## Múltiples esquemas de autentificación

Estaas esquemas de API Key tienen `auto_error=True`, por defecto. Esto
significa que, si no hay un valor disponible en el lugar especificado (header, cookie, parámetro de query),
la aplicación devolverá un error (403). Si desea tener múltiples de estas esquemas
a la vez, puede configurar `auto_error=False` y combinar las esquemas deseadas.
