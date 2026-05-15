# Sobre HTTPS { #about-https }

Es fácil asumir que HTTPS es algo que simplemente está "activado" o no.

Pero es mucho más complejo que eso.

/// tip | Consejo

Si tienes prisa o no te importa, continúa con las siguientes secciones para ver instrucciones paso a paso para configurar todo con diferentes técnicas.

///

Para **aprender los conceptos básicos de HTTPS**, desde una perspectiva de consumidor, revisa [https://howhttps.works/](https://howhttps.works/).

Ahora, desde una **perspectiva de desarrollador**, aquí hay varias cosas a tener en cuenta al pensar en HTTPS:

* Para HTTPS, **el servidor** necesita **tener "certificados"** generados por un **tercero**.
    * Esos certificados en realidad son **adquiridos** del tercero, no "generados".
* Los certificados tienen una **vida útil**.
    * Ellos **expiran**.
    * Y luego necesitan ser **renovados**, **adquiridos nuevamente** del tercero.
* La encriptación de la conexión ocurre a nivel de **TCP**.
    * Esa es una capa **debajo de HTTP**.
    * Por lo tanto, el manejo de **certificados y encriptación** se realiza **antes de HTTP**.
* **TCP no sabe acerca de "dominios"**. Solo sobre direcciones IP.
    * La información sobre el **dominio específico** solicitado va en los **datos HTTP**.
* Los **certificados HTTPS** "certifican" un **cierto dominio**, pero el protocolo y la encriptación ocurren a nivel de TCP, **antes de saber** con cuál dominio se está tratando.
* **Por defecto**, eso significaría que solo puedes tener **un certificado HTTPS por dirección IP**.
    * No importa cuán grande sea tu servidor o qué tan pequeña pueda ser cada aplicación que tengas en él.
    * Sin embargo, hay una **solución** para esto.
* Hay una **extensión** para el protocolo **TLS** (el que maneja la encriptación a nivel de TCP, antes de HTTP) llamada **[<abbr title="Server Name Indication - Indicación del nombre del servidor">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)**.
    * Esta extensión SNI permite que un solo servidor (con una **sola dirección IP**) tenga **varios certificados HTTPS** y sirva **múltiples dominios/aplicaciones HTTPS**.
    * Para que esto funcione, un componente (programa) **único** que se ejecute en el servidor, escuchando en la **dirección IP pública**, debe tener **todos los certificados HTTPS** en el servidor.
* **Después** de obtener una conexión segura, el protocolo de comunicación sigue siendo **HTTP**.
    * Los contenidos están **encriptados**, aunque se envién con el **protocolo HTTP**.

Es una práctica común tener **un programa/servidor HTTP** ejecutándose en el servidor (la máquina, host, etc.) y **gestionando todas las partes de HTTPS**: recibiendo los **requests HTTPS encriptados**, enviando los **requests HTTP desencriptados** a la aplicación HTTP real que se ejecuta en el mismo servidor (la aplicación **FastAPI**, en este caso), tomando el **response HTTP** de la aplicación, **encriptándolo** usando el **certificado HTTPS** adecuado y enviándolo de vuelta al cliente usando **HTTPS**. Este servidor a menudo se llama un **[TLS Termination Proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy)**.

Algunas de las opciones que podrías usar como un TLS Termination Proxy son:

* Traefik (que también puede manejar la renovación de certificados)
* Caddy (que también puede manejar la renovación de certificados)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Antes de Let's Encrypt, estos **certificados HTTPS** eran vendidos por terceros.

El proceso para adquirir uno de estos certificados solía ser complicado, requerir bastante papeleo y los certificados eran bastante costosos.

Pero luego se creó **[Let's Encrypt](https://letsencrypt.org/)**.

Es un proyecto de la Linux Foundation. Proporciona **certificados HTTPS de forma gratuita**, de manera automatizada. Estos certificados usan toda la seguridad criptográfica estándar, y tienen una corta duración (aproximadamente 3 meses), por lo que la **seguridad es en realidad mejor** debido a su lifespan reducida.

Los dominios son verificados de manera segura y los certificados se generan automáticamente. Esto también permite automatizar la renovación de estos certificados.

La idea es automatizar la adquisición y renovación de estos certificados para que puedas tener **HTTPS seguro, gratuito, para siempre**.

## HTTPS para Desarrolladores { #https-for-developers }

Aquí tienes un ejemplo de cómo podría ser una API HTTPS, paso a paso, prestando atención principalmente a las ideas importantes para los desarrolladores.

### Nombre de Dominio { #domain-name }

Probablemente todo comenzaría adquiriendo un **nombre de dominio**. Luego, lo configurarías en un servidor DNS (posiblemente tu mismo proveedor de la nube).

Probablemente conseguirías un servidor en la nube (una máquina virtual) o algo similar, y tendría una **dirección IP pública** <dfn title="No cambia con el tiempo. No dinámica.">fija</dfn>.

En el/los servidor(es) DNS configurarías un registro (un "`A record`") para apuntar **tu dominio** a la **dirección IP pública de tu servidor**.

Probablemente harías esto solo una vez, la primera vez, al configurar todo.

/// tip | Consejo

Esta parte del Nombre de Dominio es mucho antes de HTTPS, pero como todo depende del dominio y la dirección IP, vale la pena mencionarlo aquí.

///

### DNS { #dns }

Ahora centrémonos en todas las partes realmente de HTTPS.

Primero, el navegador consultaría con los **servidores DNS** cuál es la **IP del dominio**, en este caso, `someapp.example.com`.

Los servidores DNS le dirían al navegador que use una **dirección IP** específica. Esa sería la dirección IP pública utilizada por tu servidor, que configuraste en los servidores DNS.

<img src="/img/deployment/https/https01.drawio.svg">

### Inicio del Handshake TLS { #tls-handshake-start }

El navegador luego se comunicaría con esa dirección IP en el **puerto 443** (el puerto HTTPS).

La primera parte de la comunicación es solo para establecer la conexión entre el cliente y el servidor y decidir las claves criptográficas que usarán, etc.

<img src="/img/deployment/https/https02.drawio.svg">

Esta interacción entre el cliente y el servidor para establecer la conexión TLS se llama **handshake TLS**.

### TLS con Extensión SNI { #tls-with-sni-extension }

**Solo un proceso** en el servidor puede estar escuchando en un **puerto** específico en una **dirección IP** específica. Podría haber otros procesos escuchando en otros puertos en la misma dirección IP, pero solo uno para cada combinación de dirección IP y puerto.

TLS (HTTPS) utiliza el puerto específico `443` por defecto. Así que ese es el puerto que necesitaríamos.

Como solo un proceso puede estar escuchando en este puerto, el proceso que lo haría sería el **TLS Termination Proxy**.

El TLS Termination Proxy tendría acceso a uno o más **certificados TLS** (certificados HTTPS).

Usando la **extensión SNI** discutida anteriormente, el TLS Termination Proxy verificaría cuál de los certificados TLS (HTTPS) disponibles debería usar para esta conexión, usando el que coincida con el dominio esperado por el cliente.

En este caso, usaría el certificado para `someapp.example.com`.

<img src="/img/deployment/https/https03.drawio.svg">

El cliente ya **confía** en la entidad que generó ese certificado TLS (en este caso Let's Encrypt, pero lo veremos más adelante), por lo que puede **verificar** que el certificado sea válido.

Luego, usando el certificado, el cliente y el TLS Termination Proxy **deciden cómo encriptar** el resto de la **comunicación TCP**. Esto completa la parte de **Handshake TLS**.

Después de esto, el cliente y el servidor tienen una **conexión TCP encriptada**, esto es lo que proporciona TLS. Y luego pueden usar esa conexión para iniciar la comunicación **HTTP real**.

Y eso es lo que es **HTTPS**, es simplemente HTTP simple **dentro de una conexión TLS segura** en lugar de una conexión TCP pura (sin encriptar).

/// tip | Consejo

Ten en cuenta que la encriptación de la comunicación ocurre a nivel de **TCP**, no a nivel de HTTP.

///

### Request HTTPS { #https-request }

Ahora que el cliente y el servidor (específicamente el navegador y el TLS Termination Proxy) tienen una **conexión TCP encriptada**, pueden iniciar la **comunicación HTTP**.

Así que, el cliente envía un **request HTTPS**. Esto es simplemente un request HTTP a través de una conexión TLS encriptada.

<img src="/img/deployment/https/https04.drawio.svg">

### Desencriptar el Request { #decrypt-the-request }

El TLS Termination Proxy usaría la encriptación acordada para **desencriptar el request**, y transmitiría el **request HTTP simple (desencriptado)** al proceso que ejecuta la aplicación (por ejemplo, un proceso con Uvicorn ejecutando la aplicación FastAPI).

<img src="/img/deployment/https/https05.drawio.svg">

### Response HTTP { #http-response }

La aplicación procesaría el request y enviaría un **response HTTP simple (sin encriptar)** al TLS Termination Proxy.

<img src="/img/deployment/https/https06.drawio.svg">

### Response HTTPS { #https-response }

El TLS Termination Proxy entonces **encriptaría el response** usando la criptografía acordada antes (que comenzó con el certificado para `someapp.example.com`), y lo enviaría de vuelta al navegador.

Luego, el navegador verificaría que el response sea válido y encriptado con la clave criptográfica correcta, etc. Entonces **desencriptaría el response** y lo procesaría.

<img src="/img/deployment/https/https07.drawio.svg">

El cliente (navegador) sabrá que el response proviene del servidor correcto porque está utilizando la criptografía que acordaron usando el **certificado HTTPS** anteriormente.

### Múltiples Aplicaciones { #multiple-applications }

En el mismo servidor (o servidores), podrían haber **múltiples aplicaciones**, por ejemplo, otros programas API o una base de datos.

Solo un proceso puede estar gestionando la IP y puerto específica (el TLS Termination Proxy en nuestro ejemplo) pero las otras aplicaciones/procesos pueden estar ejecutándose en el/los servidor(es) también, siempre y cuando no intenten usar la misma **combinación de IP pública y puerto**.

<img src="/img/deployment/https/https08.drawio.svg">

De esa manera, el TLS Termination Proxy podría gestionar HTTPS y certificados para **múltiples dominios**, para múltiples aplicaciones, y luego transmitir los requests a la aplicación correcta en cada caso.

### Renovación de Certificados { #certificate-renewal }

En algún momento en el futuro, cada certificado **expiraría** (alrededor de 3 meses después de haberlo adquirido).

Y entonces, habría otro programa (en algunos casos es otro programa, en algunos casos podría ser el mismo TLS Termination Proxy) que hablaría con Let's Encrypt y renovaría el/los certificado(s).

<img src="/img/deployment/https/https.drawio.svg">

Los **certificados TLS** están **asociados con un nombre de dominio**, no con una dirección IP.

Entonces, para renovar los certificados, el programa de renovación necesita **probar** a la autoridad (Let's Encrypt) que de hecho **"posee" y controla ese dominio**.

Para hacer eso, y para acomodar diferentes necesidades de aplicaciones, hay varias formas en que puede hacerlo. Algunas formas populares son:

* **Modificar algunos registros DNS**.
    * Para esto, el programa de renovación necesita soportar las API del proveedor de DNS, por lo que, dependiendo del proveedor de DNS que estés utilizando, esto podría o no ser una opción.
* **Ejecutarse como un servidor** (al menos durante el proceso de adquisición del certificado) en la dirección IP pública asociada con el dominio.
    * Como dijimos anteriormente, solo un proceso puede estar escuchando en una IP y puerto específicos.
    * Esta es una de las razones por las que es muy útil cuando el mismo TLS Termination Proxy también se encarga del proceso de renovación del certificado.
    * De lo contrario, podrías tener que detener momentáneamente el TLS Termination Proxy, iniciar el programa de renovación para adquirir los certificados, luego configurarlos con el TLS Termination Proxy, y luego reiniciar el TLS Termination Proxy. Esto no es ideal, ya que tus aplicaciones no estarán disponibles durante el tiempo que el TLS Termination Proxy esté apagado.

Todo este proceso de renovación, mientras aún se sirve la aplicación, es una de las principales razones por las que querrías tener un **sistema separado para gestionar el HTTPS** con un TLS Termination Proxy en lugar de simplemente usar los certificados TLS con el servidor de aplicaciones directamente (por ejemplo, Uvicorn).

## Headers reenviados por el proxy { #proxy-forwarded-headers }

Al usar un proxy para gestionar HTTPS, tu **servidor de aplicaciones** (por ejemplo Uvicorn vía FastAPI CLI) no sabe nada sobre el proceso HTTPS, se comunica con HTTP simple con el **TLS Termination Proxy**.

Este **proxy** normalmente configuraría algunos headers HTTP sobre la marcha antes de transmitir el request al **servidor de aplicaciones**, para hacerle saber al servidor de aplicaciones que el request está siendo **reenviado** por el proxy.

/// note | Detalles técnicos

Los headers del proxy son:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

Aun así, como el **servidor de aplicaciones** no sabe que está detrás de un **proxy** de confianza, por defecto, no confiaría en esos headers.

Pero puedes configurar el **servidor de aplicaciones** para confiar en los headers reenviados enviados por el **proxy**. Si estás usando FastAPI CLI, puedes usar la *Opción de la CLI* `--forwarded-allow-ips` para indicarle desde qué IPs debería confiar en esos headers reenviados.

Por ejemplo, si el **servidor de aplicaciones** solo está recibiendo comunicación del **proxy** de confianza, puedes establecerlo en `--forwarded-allow-ips="*"` para hacer que confíe en todas las IPs entrantes, ya que solo recibirá requests desde la IP que sea utilizada por el **proxy**.

De esta manera la aplicación podrá saber cuál es su propia URL pública, si está usando HTTPS, el dominio, etc.

Esto sería útil, por ejemplo, para manejar correctamente redirecciones.

/// tip | Consejo

Puedes aprender más sobre esto en la documentación de [Detrás de un proxy - Habilitar headers reenviados por el proxy](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## Resumen { #recap }

Tener **HTTPS** es muy importante y bastante **crítico** en la mayoría de los casos. La mayor parte del esfuerzo que como desarrollador tienes que poner en torno a HTTPS es solo sobre **entender estos conceptos** y cómo funcionan.

Pero una vez que conoces la información básica de **HTTPS para desarrolladores** puedes combinar y configurar fácilmente diferentes herramientas para ayudarte a gestionar todo de una manera sencilla.

En algunos de los siguientes capítulos, te mostraré varios ejemplos concretos de cómo configurar **HTTPS** para aplicaciones **FastAPI**. 🔒
