# О HTTPS

Обычно представляется, что HTTPS это некая  опция, которая либо "включена", либо нет.

Но всё несколько сложнее.

!!! tip "Подсказка"
    Если Вы торопитесь или Вам не интересно, можете перейти на следующую страницу этого пошагового руководства по размещению приложений на серверах с использованием различных технологий.

Чтобы **изучить основы HTTPS** для клиента, перейдите по ссылке <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>.

Здесь же представлены некоторые вещи, которые **разработчик** должен иметь ввиду при размышлениях о HTTPS:

* Протокол HTTPS предполагает, что **серверу** нужно **располагать "сертификатами"** сгенерированными **третьей стороной**.
    * На самом деле эти сертификаты **приобретены** у третьей стороны, а не "сгенерированы".
* У сертификатов есть **срок годности**.
    * Срок годности **истекает**.
    * По истечении срока годности их нужно **обновить**, то есть **снова получить** у третьей стороны.
* Шифрованное соединение происходит **на уровне протокола TCP**.
    * Протокол TCP находится на один уровень **ниже протокола HTTP**.
    * Поэтому **проверка сертификатов и шифрование** происходит **до HTTP**.
* **TCP не знает о "доменах"**, но знает об IP-адресах.
    * Информация о **запрашиваемом домене** добавляется в данные **на уровне HTTP**.
* **Сертификаты HTTPS** "сертифицируют" **конкретный домен**, но проверка сертификатов и шифрование данных происходит на уровне протокола TCP, то есть **до того**, как станет известен домен-получатель данных.
* **По умолчанию** это означает, что у Вас может быть **только один сертификат HTTPS на один IP-адрес**.
    * Не важно, насколько большой у Вас сервер и насколько маленькие приложения на нём могут быть.
    * Однако, у этой проблемы есть **решение**.
* Существует **расширение** протокола **TLS** (который работает на уровне TCP, то есть до HTTP) называемое **<a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Указание имени сервера">SNI</abbr></a>**.
    * Рсширение SNI позволяет одному серверу (с **одним IP-адресом**) иметь **несколько сертификатов HTTPS** и обслуживать **множество HTTPS-доменов/приложений**.
    * Чтобы эта конструкция работала, **один** её компонент (программа) запушенный на сервере и слушающий **публичный IP-адрес**, должен ииметь **все сертификаты HTTPS** для этого сервера.
* **После** установления защищённого соединеиня, протколом передачи данных **остаётся HTTP**.
    * Но данные теперь **зашифрованы**, несмотря на то, что они передаются по **протоколу HTTP**.

Обычной практикой является иметь **одну программу/HTTP-сервер** запущенную на сервере (машине, хосте и т.д.) и **ответственную за всю работу с HTTPS**:

* получение **зашифрованных HTTPS-запросов**
* расшифровка запросов
* отправка **расшифрованных HTTP запросов** в соответствующее HTTP приложение, работающее на том же сервере (в нашем случае, это приложение **FastAPI**)
* получние **HTTP-ответа** от приложения
* **шифрование ответа** используя подходящий **сертификат HTTPS**
* отправка зашифрованного **HTTPS-ответа клиенту**.
Такой сервер часто называют **<a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">Прокси-сервер завершения работы TLS</a>**.

Вот некоторые варианты, которые Вы можете использовать в качестве такого прокси-сервера:

* Traefik (может обновлять сертификаты)
* Caddy (может обновлять сертификаты)
* Nginx
* HAProxy

## Let's Encrypt (центр сертификации)

До появления Let's Encrypt **сертификаты HTTPS** приходилось покупать у третьих сторон.

Процесс получения такого сертификата был трудоёмким, требовал предоставления документов и сертификаты стоили дорого.

Но затем был создан **<a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a>**.

It is a project from the Linux Foundation. It provides **HTTPS certificates for free**, in an automated way. These certificates use all the standard cryptographic security, and are short-lived (about 3 months), so the **security is actually better** because of their reduced lifespan.

The domains are securely verified and the certificates are generated automatically. This also allows automating the renewal of these certificates.

The idea is to automate the acquisition and renewal of these certificates so that you can have **secure HTTPS, for free, forever**.

## HTTPS for Developers

Here's an example of how an HTTPS API could look like, step by step, paying attention mainly to the ideas important for developers.

### Domain Name

It would probably all start by you **acquiring** some **domain name**. Then, you would configure it in a DNS server (possibly your same cloud provider).

You would probably get a cloud server (a virtual machine) or something similar, and it would have a <abbr title="That doesn't change">fixed</abbr> **public IP address**.

In the DNS server(s) you would configure a record (an "`A record`") to point **your domain** to the public **IP address of your server**.

You would probably do this just once, the first time, when setting everything up.

!!! tip
    This Domain Name part is way before HTTPS, but as everything depends on the domain and the IP address, it's worth mentioning it here.

### DNS

Now let's focus on all the actual HTTPS parts.

First, the browser would check with the **DNS servers** what is the **IP for the domain**, in this case, `someapp.example.com`.

The DNS servers would tell the browser to use some specific **IP address**. That would be the public IP address used by your server, that you configured in the DNS servers.

<img src="/img/deployment/https/https01.svg">

### TLS Handshake Start

The browser would then communicate with that IP address on **port 443** (the HTTPS port).

The first part of the communication is just to establish the connection between the client and the server and to decide the cryptographic keys they will use, etc.

<img src="/img/deployment/https/https02.svg">

This interaction between the client and the server to establish the TLS connection is called the **TLS handshake**.

### TLS with SNI Extension

**Only one process** in the server can be listening on a specific **port** in a specific **IP address**. There could be other processes listening on other ports in the same IP address, but only one for each combination of IP address and port.

TLS (HTTPS) uses the specific port `443` by default. So that's the port we would need.

As only one process can be listening on this port, the process that would do it would be the **TLS Termination Proxy**.

The TLS Termination Proxy would have access to one or more **TLS certificates** (HTTPS certificates).

Using the **SNI extension** discussed above, the TLS Termination Proxy would check which of the TLS (HTTPS) certificates available it should use for this connection, using the one that matches the domain expected by the client.

In this case, it would use the certificate for `someapp.example.com`.

<img src="/img/deployment/https/https03.svg">

The client already **trusts** the entity that generated that TLS certificate (in this case Let's Encrypt, but we'll see about that later), so it can **verify** that the certificate is valid.

Then, using the certificate, the client and the TLS Termination Proxy **decide how to encrypt** the rest of the **TCP communication**. This completes the **TLS Handshake** part.

After this, the client and the server have an **encrypted TCP connection**, this is what TLS provides. And then they can use that connection to start the actual **HTTP communication**.

And that's what **HTTPS** is, it's just plain **HTTP** inside a **secure TLS connection** instead of a pure (unencrypted) TCP connection.

!!! tip
    Notice that the encryption of the communication happens at the **TCP level**, not at the HTTP level.

### HTTPS Request

Now that the client and server (specifically the browser and the TLS Termination Proxy) have an **encrypted TCP connection**, they can start the **HTTP communication**.

So, the client sends an **HTTPS request**. This is just an HTTP request through an encrypted TLS connection.

<img src="/img/deployment/https/https04.svg">

### Decrypt the Request

The TLS Termination Proxy would use the encryption agreed to **decrypt the request**, and would transmit the **plain (decrypted) HTTP request** to the process running the application (for example a process with Uvicorn running the FastAPI application).

<img src="/img/deployment/https/https05.svg">

### HTTP Response

The application would process the request and send a **plain (unencrypted) HTTP response** to the TLS Termination Proxy.

<img src="/img/deployment/https/https06.svg">

### HTTPS Response

The TLS Termination Proxy would then **encrypt the response** using the cryptography agreed before (that started with the certificate for `someapp.example.com`), and send it back to the browser.

Next, the browser would verify that the response is valid and encrypted with the right cryptographic key, etc. It would then **decrypt the response** and process it.

<img src="/img/deployment/https/https07.svg">

The client (browser) will know that the response comes from the correct server because it is using the cryptography they agreed using the **HTTPS certificate** before.

### Multiple Applications

In the same server (or servers), there could be **multiple applications**, for example, other API programs or a database.

Only one process can be handling the specific IP and port (the TLS Termination Proxy in our example) but the other applications/processes can be running on the server(s) too, as long as they don't try to use the same **combination of public IP and port**.

<img src="/img/deployment/https/https08.svg">

That way, the TLS Termination Proxy could handle HTTPS and certificates for **multiple domains**, for multiple applications, and then transmit the requests to the right application in each case.

### Certificate Renewal

At some point in the future, each certificate would **expire** (about 3 months after acquiring it).

And then, there would be another program (in some cases it's another program, in some cases it could be the same TLS Termination Proxy) that would talk to Let's Encrypt, and renew the certificate(s).

<img src="/img/deployment/https/https.svg">

The **TLS certificates** are **associated with a domain name**, not with an IP address.

So, to renew the certificates, the renewal program needs to **prove** to the authority (Let's Encrypt) that it indeed **"owns" and controls that domain**.

To do that, and to accommodate different application needs, there are several ways it can do it. Some popular ways are:

* **Modify some DNS records**.
    * For this, the renewal program needs to support the APIs of the DNS provider, so, depending on the DNS provider you are using, this might or might not be an option.
* **Run as a server** (at least during the certificate acquisition process) on the public IP address associated with the domain.
    * As we said above, only one process can be listening on a specific IP and port.
    * This is one of the reasons why it's very useful when the same TLS Termination Proxy also takes care of the certificate renewal process.
    * Otherwise, you might have to stop the TLS Termination Proxy momentarily, start the renewal program to acquire the certificates, then configure them with the TLS Termination Proxy, and then restart the TLS Termination Proxy. This is not ideal, as your app(s) will not be available during the time that the TLS Termination Proxy is off.

All this renewal process, while still serving the app, is one of the main reasons why you would want to have a **separate system to handle HTTPS** with a TLS Termination Proxy instead of just using the TLS certificates with the application server directly (e.g. Uvicorn).

## Recap

Having **HTTPS** is very important, and quite **critical** in most cases. Most of the effort you as a developer have to put around HTTPS is just about **understanding these concepts** and how they work.

But once you know the basic information of **HTTPS for developers** you can easily combine and configure different tools to help you manage everything in a simple way.

In some of the next chapters, I'll show you several concrete examples of how to set up **HTTPS** for **FastAPI** applications. 🔒
