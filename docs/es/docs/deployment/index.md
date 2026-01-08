# Despliegue { #deployment }

Desplegar una aplicación **FastAPI** es relativamente fácil.

## Qué Significa Despliegue { #what-does-deployment-mean }

**Desplegar** una aplicación significa realizar los pasos necesarios para hacerla **disponible para los usuarios**.

Para una **API web**, normalmente implica ponerla en una **máquina remota**, con un **programa de servidor** que proporcione buen rendimiento, estabilidad, etc., para que tus **usuarios** puedan **acceder** a la aplicación de manera eficiente y sin interrupciones o problemas.

Esto contrasta con las etapas de **desarrollo**, donde estás constantemente cambiando el código, rompiéndolo y arreglándolo, deteniendo y reiniciando el servidor de desarrollo, etc.

## Estrategias de Despliegue { #deployment-strategies }

Hay varias maneras de hacerlo dependiendo de tu caso de uso específico y las herramientas que utilices.

Podrías **desplegar un servidor** tú mismo utilizando una combinación de herramientas, podrías usar un **servicio en la nube** que hace parte del trabajo por ti, u otras opciones posibles.

Por ejemplo, nosotros, el equipo detrás de FastAPI, construimos <a href="https://fastapicloud.com" class="external-link" target="_blank">**FastAPI Cloud**</a>, para hacer que desplegar aplicaciones de FastAPI en la nube sea lo más ágil posible, con la misma experiencia de desarrollador de trabajar con FastAPI.

Te mostraré algunos de los conceptos principales que probablemente deberías tener en cuenta al desplegar una aplicación **FastAPI** (aunque la mayoría se aplica a cualquier otro tipo de aplicación web).

Verás más detalles a tener en cuenta y algunas de las técnicas para hacerlo en las siguientes secciones. ✨
