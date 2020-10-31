# Respuesta - Cambiar el Status Code

Probablemente ya haz leído con anterioridad acerca de los [Response Status Code](../tutorial/response-status-code.md){.internal-link target=_blank}.


Pero en algunos casos necesitarás retornar un status code diferente a los estándar.


## Caso de uso

Por ejemplo, imagina que quieres retornar un HTTP status code
de OK" `200` por defecto.


Si aún no tienes datos, desearás crearlos y retornar un HTTP status code de "CREATED" `201`


Pero además deseas poder filtrar y convertir los datos que retornan de un `response_model`.

Para estos casos, puedes usar un parámetro `Response`.

## Usar un parámetro `Response` 

Puedes declarar un parámetro de tipo `Response` en tu *path operation function* (de manera similar como se hace con las cookies y headers).

Y entonces, podrás configurar las cookies en ese objeto de 
response *temporal*.

```Python hl_lines="1  9  12"
{!../../../docs_src/response_change_status_code/tutorial001.py!}
```

Posteriormente, podrá retornar cualquier objeto que necesite, como lo haría normalmente (un `diccionario`, un modelo de base de datos, etc).


Si declaraste un `response_model`, este se continuará usando para filtrar y convertir el objeto que devolviste.


**FastAPI** usará esa *temporal* response para extraer los headers (al igual que las cookies y los headers), además las pondrá en la respuesta final que contendrá el valor retornado y filtrado por algún `response_model`.


También podrás declarar el parámetro `Response` en dependencias, así como configurar los headers (y las cookies) en ellas. Pero ten en cuenta que quedará la última configuración.
