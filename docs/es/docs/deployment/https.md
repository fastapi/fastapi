# Acerca de HTTPS

Es bastante fácil asumir que HTTPS es algo que simplemente está "activado" o no.

Pero en la realidad es algo mucho más complicado que eso.

!!! tip
    Si estas en un apuro o simplemente no te importa, continua con la siguientes secciones para ver una guía paso a paso para configurar todo con técnicas diferentes.

Para aprender lo básico de HTTPS, desde una perspectiva del consumidor, revisa <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>.

Ahora, desde la perspectiva del desarrollador, aquí hay algunas cosas a tener en mente mientras pensamos sobre HTTPS:

* Para HTTPS, el servidor necesita tener "certificados" generados por una fuente externa.
    * Esos certificados son de hecho adquiridos de la fuente externa, no "generados"
* Los certificados tiene un tiempo de vida.
    * Ellos expiran.
    * Y luego necesitan ser renovados, adquiridos otra vez desde la fuente externa.
* La encriptación de la conexión ocurre a nivel TCP.
    * Eso es una capa debajo de HTTP.
    * Entonces, el manejo de certificado y encriptación es hecho antes de HTTP.
* TCP no conoce de "dominios". Solo de direcciones IP.
    * La información sobre el dominio específicamente requerido va en los datos de HTTP.
* Los certificados HTTPS "certifican" un cierto dominio, pero el protocolo y la encriptación suceden en el nivel TCP, antes de conocer con que dominio se está lidiando.
* Por defecto, eso diría que solamente puedes tener un certificado HTTPS por dirección IP.
    * No importa que tan grande sea tu servidor, o que tan pequeñas puedan ser las aplicaciones que tienes en él.
    * Sin embargo, existe una solución a esto.
* Existe una extensión al protocolo TLS (quien maneja la encriptación a nivel TCP, antes de HTTP) llamado <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a>.
    * Esta extensión SNI permite que un servidor particular (con una sola dirección IP) pueda tener varios certificados HTTPS y servir multiples dominios/aplicaciones HTTPS.
    * Para que esto funcione, un solo componente (programa) que este corriendo en el servidor, escuchando en la dirección IP publica, tenga todos los certificados HTTPS en el servidor.
* Después de obtener una conexión segura, la comunicación del protocolo sigue siendo HTTP.
    * El contenido es encriptado, incluso cuando está siendo enviado con el protocolo HTTP.

Es una practica común tener un servidor programa/HTTP corriendo en el servidor (la maquina, el huésped, etc.) y manejando todas las partes de HTTPS: enviando la desencriptada petición HTTP a la aplicación HTTP actual que esta corriendo en el mismo servidor (la aplicación con **FastAPI**, en este caso), tome la respuesta HTTP de la aplicación,  la encripte usando el certificado apropiado y la envié de vuelta al cliente usando HTTPS. Este servidor es comúnmente llamado un <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS Termination Proxy</a>.

## Let's Encrypt

Antes de comenzar a describir **Let's Encrypt**, estos certificados HTTPS fueron vendidos por fuentes externas de confianza.

EL proceso de adquirir uno de estos certificados solía ser tedioso, requería algo de papeleo y los certificados eran bastante caros.

Pero luego <a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a> fue creado.

Este proyecto de la Linux Foundation. Provee de certificados HTTPS de forma gratuita. En una manera automatizada. Estos certificados usan todos los estándares de seguridad criptográfica, y tienen una vida corta (cerca de 3 meses), por lo que la seguridad es mucho mejor debido a su reducida duración.

Los dominios son verificados de manera segura y los certificados son generados automáticamente. Esto también permite automatizar la renovación de estos certificados.

La idea es automatizar la adquisición y la renovación de estos certificados, para que puedas tener HTTPS seguros, de manera gratuita, por siempre.
