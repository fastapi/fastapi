# Response Status Code

De la misma manera que puedes especificar un modelo de respuesta, también puedes declarar codigos de estado HTTP
usados para la respuesta con el parametro `status_code` en cualquiera de los *path operations*:

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.delete()`
- etc.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

!!! note Toma en cuenta que `status_code` es un parámetro del método del "decorador" (`get`, `post`, etc)-
No de la función de tu *path operation*, como todos los parámetros y cuerpo.


El parámetro `status_code` recibe un número con el código del estado HTTP.

!!! info `status_code` puede alternamente recibir un `IntEnum`, como `http.HTTPStatus` de Python.

Será:

- Retorna ese código de estado en la respuesta.
- Documentado como en el OpenAPI "schema" (además, en la interfaz de usuario):

![image](https://user-images.githubusercontent.com/70811425/194106058-239f3547-e430-4d72-bb61-df7cf8dd2acb.png)


!!! note Algunos códigos de respuesta (ve la siguiente sección) indica que la respuesta no tiene body.

```
FastAPI sabe esto, y producirá documentatión OpenAPI diciendo que no hay body en la respuesta.
```

# Acerca de los códigos de estado HTTP.

!!! note Si ya sabes lo que son los códigos de estado HTTP, salta a la siguiente sección.

En HTTP, tu envías un código de estado de tres dígitos como parte de la respuesta.

Estos códigos de estado tienen un nombre asociado para reconocerlos, pero lo más importante es el número.

En resumen:

 - `100` en adelante son para "Información". Rara vez los usas directamente. Las respuestas con estos códigos de estado no tienen body.
 - `200` en adelante son para respuestas "Exitosas". Esta son las que se usan con mayor frecuencia.
      - `200` código  de estado por defecto, el cual significa que todo estuvo "OK".
      - Otro ejemplo sería `201`, "Creado". Es comúnmente usado después de crear una observación en la base de datos.
      - `204` es un caso especial, "Sin contenido". Esta respuesta es usada cuando no hay contenido de retorno por parte del cliente,
      y la respuesta no debe tener cuerpo.

- `300` en adelante son para "Redirección". Respuestas con estos códigos de estado pueden o no tener body, excepto para `304`, "No Modificado",
  el cual no debe tener body.

- `400` en adelante son para respuestas para `Error del Cliente`. Estos son el segundo tipo de codigós que más usarás.
     - Un ejemplo es `404`, para respuesta de "No encontrado".
     - Para errores genéricos desde el cliente, puedes usar `400`.

- `500` en adelante son para errores del servidor. Tú nunca los usas directamente. Cuando algo sale mal en alguna parte del código de tu aplicación,
  o en el servidor, automáticamente retornará uno de estos códigos.

!!! tip Para saber más acerca de estos códigos de estado y cuál código se usa para cada caso, revisa el
[MDN documentation about HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

# Atajos para recordar los nombres

Vamos a ver el ejemplo previo otra vez:

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial001.py!}
```

`201` es el código de estado para "Creado".

Pero tú no tienes que memorizar lo que significa cada uno de estos códigos.

Puedes usar las convenientes variables desde `fastapi.status`.

```Python hl_lines="6"
{!../../../docs_src/response_status_code/tutorial002.py!}
```

Son tan convenientes, mantienen el mismo número, pero puedes usar el autocompletado del editor para encontrarlas:

![image](https://user-images.githubusercontent.com/70811425/194105942-a95651b0-fe60-4c3a-b166-999a077886d5.png)

!!! note "Detalles técnicos" Podrías usar también `from starlette import status`.


```
**FastAPI** provee el mismo `starlette.status` como  `fastapi.status`  conveniente para tí, el desarrollador. Pero viene directamente de Starlette.
```

# Cambiando el por defecto

Después, en la [Guía Avanzada de Usuario](https://github.com/carlosm27/fastapi/blob/master/docs/en/docs/advanced/response-change-status-code.md), verás cómo retornar diferentes códigos de estado que los de por defecto declaras aquí.
