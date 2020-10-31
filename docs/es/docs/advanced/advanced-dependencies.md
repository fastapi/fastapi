# Dependencias Avanzadas

## Dependencias parametrizadas

Todas las dependencias que hemos visto son una función o una clase fija.


Pero puede haber casos en los que desees poder establecer parámetros en la dependencia, sin tener que declarar muchas funciones o clases diferentes.

Imaginemos que queremos tener una dependencia que compruebe si el parámetro de consulta `q` contiene algún contenido fijo.


Además queremos tener la posibilidad de parametrizar ese contenido fijo.

## Una instancia "invocable" 

En Python hay una manera de crear una instancia en una clase "invocable".


No en la clase misma (la cual ya es invocable), si no en una instancia de esa clase. 


Para hacer esto, debemos declarar un método `__call__` como se podemos ver en el siguiente código:  


```Python hl_lines="10"
{!../../../docs_src/dependencies/tutorial011.py!}
```

En este caso, `__call__` es el método que **FastAPI** usará para comprobar parámetros y subdependencias adicionales, y esto es lo que llamaremos para pasar un valor al parámetro en tu *path operation function* más adelante. 


## Parametrizar la instancia

Ahora podemos usar el método `__init__` para declarar los parámetros de la instancia que usaremos para "parametrizar" la dependencia: 


```Python hl_lines="7"
{!../../../docs_src/dependencies/tutorial011.py!}
```

En este caso, ** FastAPI ** nunca tocará o se preocupará por el método `__init__`, lo usaremos directamente en nuestro código.


## Crear una instancia

Podemos crear una instancia de esta clase con el siguiente código:


```Python hl_lines="16"
{!../../../docs_src/dependencies/tutorial011.py!}
```

De esta manera seremos capaces de "parametrizar" nuestra dependencia, `"bar"` dentro de él, como el atributo `checker.fixed_content`.


## Usar la instancia como una dependencia

De esta manera podemos usar este `checker` en un `Depends(checker)`, en lugar de `Depends(FixedContentQueryChecker)`, debido a que la dependecia es la instancia, `checker`, no la clase en sí.


Finalmente, al resolver la dependencia, **FastAPI** llamará a este `checker` de la siguiente manera:


```Python
checker(q="somequery")
```


...y pasará lo que sea que devuelva como el valor de la dependencia en nuestro path operation function* como el parámetro `fixed_content_included`:


```Python hl_lines="20"
{!../../../docs_src/dependencies/tutorial011.py!}
```

!!! tip
    Todo esto puede parecer inventado. Y es posible que todavía no esté muy claro su utilidad.
    

    Sabemos que estos ejemplos son intencionalmente sencillos, pero muestran cómo funciona todo.
    
    Además en los capítulos acerca de la seguridad, hay funciones de utilidad que se implementan de esta misma forma. 
    
    Si entendiste todo lo anterior, ya sabes cómo funcionan esas herramientas de gran utilidad para la seguridad.
    
