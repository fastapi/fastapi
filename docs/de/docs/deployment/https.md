# Über HTTPS { #about-https }

Es ist leicht anzunehmen, dass HTTPS etwas ist, was einfach nur „aktiviert“ wird oder nicht.

Aber es ist viel komplexer als das.

/// tip | Tipp

Wenn Sie es eilig haben oder es Ihnen egal ist, fahren Sie mit den nächsten Abschnitten fort, um Schritt-für-Schritt-Anleitungen für die Einrichtung der verschiedenen Technologien zu erhalten.

///

Um **die Grundlagen von HTTPS** aus Sicht des Benutzers zu erlernen, schauen Sie sich [https://howhttps.works/](https://howhttps.works/) an.

Aus **Sicht des Entwicklers** sollten Sie beim Nachdenken über HTTPS Folgendes beachten:

* Für HTTPS muss **der Server** über von einem **Dritten** generierte **„Zertifikate“** verfügen.
    * Diese Zertifikate werden tatsächlich vom Dritten **erworben** und nicht „generiert“.
* Zertifikate haben eine **Lebensdauer**.
    * Sie **verfallen**.
    * Und dann müssen sie vom Dritten **erneuert**, **erneut erworben** werden.
* Die Verschlüsselung der Verbindung erfolgt auf **TCP-Ebene**.
    * Das ist eine Schicht **unter HTTP**.
    * Die Handhabung von **Zertifikaten und Verschlüsselung** erfolgt also **vor HTTP**.
* **TCP weiß nichts über „Domains“**. Nur über IP-Adressen.
    * Die Informationen über die angeforderte **spezifische Domain** befinden sich in den **HTTP-Daten**.
* Die **HTTPS-Zertifikate** „zertifizieren“ eine **bestimmte Domain**, aber das Protokoll und die Verschlüsselung erfolgen auf TCP-Ebene, **ohne zu wissen**, um welche Domain es sich handelt.
* **Standardmäßig** bedeutet das, dass Sie nur **ein HTTPS-Zertifikat pro IP-Adresse** haben können.
    * Ganz gleich, wie groß Ihr Server ist oder wie klein die einzelnen Anwendungen darauf sind.
    * Hierfür gibt es jedoch eine **Lösung**.
* Es gibt eine **Erweiterung** zum **TLS**-Protokoll (dasjenige, das die Verschlüsselung auf TCP-Ebene, vor HTTP, verwaltet) namens **[<abbr title="Server Name Indication - Servernamensanzeige">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication)**.
    * Mit dieser SNI-Erweiterung kann ein einzelner Server (mit einer **einzelnen IP-Adresse**) über **mehrere HTTPS-Zertifikate** verfügen und **mehrere HTTPS-Domains/Anwendungen bereitstellen**.
    * Damit das funktioniert, muss eine **einzelne** Komponente (Programm), die auf dem Server ausgeführt wird und welche die **öffentliche IP-Adresse** überwacht, **alle HTTPS-Zertifikate** des Servers haben.
* **Nachdem** eine sichere Verbindung hergestellt wurde, ist das Kommunikationsprotokoll **immer noch HTTP**.
    * Die Inhalte sind **verschlüsselt**, auch wenn sie mit dem **HTTP-Protokoll** gesendet werden.

Es ist eine gängige Praxis, **ein Programm/HTTP-Server** auf dem Server (der Maschine, dem Host usw.) laufen zu lassen, welches **alle HTTPS-Aspekte verwaltet**: Empfangen der **verschlüsselten HTTPS-<abbr title="Request – Anfrage: Daten, die der Client zum Server sendet">Requests</abbr>**, Senden der **entschlüsselten HTTP-Requests** an die eigentliche HTTP-Anwendung die auf demselben Server läuft (in diesem Fall die **FastAPI**-Anwendung), entgegennehmen der **HTTP-Response** von der Anwendung, **verschlüsseln derselben** mithilfe des entsprechenden **HTTPS-Zertifikats** und Zurücksenden zum Client über **HTTPS**. Dieser Server wird oft als **[TLS-Terminierungsproxy](https://en.wikipedia.org/wiki/TLS_termination_proxy)** bezeichnet.

Einige der Optionen, die Sie als TLS-Terminierungsproxy verwenden können, sind:

* Traefik (kann auch Zertifikat-Erneuerungen durchführen)
* Caddy (kann auch Zertifikat-Erneuerungen durchführen)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Vor Let's Encrypt wurden diese **HTTPS-Zertifikate** von vertrauenswürdigen Dritten verkauft.

Der Prozess zum Erwerb eines dieser Zertifikate war früher umständlich, erforderte viel Papierarbeit und die Zertifikate waren ziemlich teuer.

Aber dann wurde **[Let's Encrypt](https://letsencrypt.org/)** geschaffen.

Es ist ein Projekt der Linux Foundation. Es stellt **kostenlose HTTPS-Zertifikate** automatisiert zur Verfügung. Diese Zertifikate nutzen standardmäßig die gesamte kryptografische Sicherheit und sind kurzlebig (circa 3 Monate), sodass die **Sicherheit tatsächlich besser ist**, aufgrund der kürzeren Lebensdauer.

Die Domains werden sicher verifiziert und die Zertifikate werden automatisch generiert. Das ermöglicht auch die automatische Erneuerung dieser Zertifikate.

Die Idee besteht darin, den Erwerb und die Erneuerung der Zertifikate zu automatisieren, sodass Sie **sicheres HTTPS, kostenlos und für immer** haben können.

## HTTPS für Entwickler { #https-for-developers }

Hier ist ein Beispiel, wie eine HTTPS-API aussehen könnte, Schritt für Schritt, wobei vor allem die für Entwickler wichtigen Ideen berücksichtigt werden.

### Domainname { #domain-name }

Alles beginnt wahrscheinlich damit, dass Sie einen **Domainnamen erwerben**. Anschließend konfigurieren Sie ihn in einem DNS-Server (wahrscheinlich beim selben Cloudanbieter).

Sie würden wahrscheinlich einen Cloud-Server (eine virtuelle Maschine) oder etwas Ähnliches bekommen, und dieser hätte eine <dfn title="Ändert sich im Laufe der Zeit nicht. Nicht dynamisch.">feste</dfn> **öffentliche IP-Adresse**.

In dem oder den DNS-Server(n) würden Sie einen Eintrag (einen „`A record`“) konfigurieren, um mit **Ihrer Domain** auf die öffentliche **IP-Adresse Ihres Servers** zu verweisen.

Sie würden dies wahrscheinlich nur einmal tun, beim ersten Mal, wenn Sie alles einrichten.

/// tip | Tipp

Dieser Domainnamen-Aspekt liegt weit vor HTTPS, aber da alles von der Domain und der IP-Adresse abhängt, lohnt es sich, das hier zu erwähnen.

///

### DNS { #dns }

Konzentrieren wir uns nun auf alle tatsächlichen HTTPS-Aspekte.

Zuerst würde der Browser mithilfe der **DNS-Server** herausfinden, welches die **IP für die Domain** ist, in diesem Fall `someapp.example.com`.

Die DNS-Server geben dem Browser eine bestimmte **IP-Adresse** zurück. Das wäre die von Ihrem Server verwendete öffentliche IP-Adresse, die Sie in den DNS-Servern konfiguriert haben.

<img src="/img/deployment/https/https01.drawio.svg">

### TLS-Handshake-Start { #tls-handshake-start }

Der Browser kommuniziert dann mit dieser IP-Adresse über **Port 443** (den HTTPS-Port).

Der erste Teil der Kommunikation besteht lediglich darin, die Verbindung zwischen dem Client und dem Server herzustellen und die zu verwendenden kryptografischen Schlüssel usw. zu vereinbaren.

<img src="/img/deployment/https/https02.drawio.svg">

Diese Interaktion zwischen dem Client und dem Server zum Aufbau der TLS-Verbindung wird als **<abbr title="TLS-Handschlag">TLS-Handshake</abbr>** bezeichnet.

### TLS mit SNI-Erweiterung { #tls-with-sni-extension }

**Nur ein Prozess** im Server kann an einem bestimmten **Port** einer bestimmten **IP-Adresse** lauschen. Möglicherweise gibt es andere Prozesse, die an anderen Ports dieselbe IP-Adresse abhören, jedoch nur einen für jede Kombination aus IP-Adresse und Port.

TLS (HTTPS) verwendet standardmäßig den spezifischen Port `443`. Das ist also der Port, den wir brauchen.

Da an diesem Port nur ein Prozess lauschen kann, wäre der Prozess, der dies tun würde, der **TLS-Terminierungsproxy**.

Der TLS-Terminierungsproxy hätte Zugriff auf ein oder mehrere **TLS-Zertifikate** (HTTPS-Zertifikate).

Mithilfe der oben beschriebenen **SNI-Erweiterung** würde der TLS-Terminierungsproxy herausfinden, welches der verfügbaren TLS-Zertifikate (HTTPS) er für diese Verbindung verwenden muss, und zwar das, welches mit der vom Client erwarteten Domain übereinstimmt.

In diesem Fall würde er das Zertifikat für `someapp.example.com` verwenden.

<img src="/img/deployment/https/https03.drawio.svg">

Der Client **vertraut** bereits der Entität, die das TLS-Zertifikat generiert hat (in diesem Fall Let's Encrypt, aber wir werden später mehr darüber erfahren), sodass er **verifizieren** kann, dass das Zertifikat gültig ist.

Mithilfe des Zertifikats entscheiden der Client und der TLS-Terminierungsproxy dann, **wie der Rest der TCP-Kommunikation verschlüsselt werden soll**. Damit ist der **TLS-Handshake** abgeschlossen.

Danach verfügen der Client und der Server über eine **verschlüsselte TCP-Verbindung**, via TLS. Und dann können sie diese Verbindung verwenden, um die eigentliche **HTTP-Kommunikation** zu beginnen.

Und genau das ist **HTTPS**, es ist einfach **HTTP** innerhalb einer **sicheren TLS-Verbindung**, statt einer puren (unverschlüsselten) TCP-Verbindung.

/// tip | Tipp

Beachten Sie, dass die Verschlüsselung der Kommunikation auf der **TCP-Ebene** und nicht auf der HTTP-Ebene erfolgt.

///

### HTTPS-Request { #https-request }

Da Client und Server (sprich, der Browser und der TLS-Terminierungsproxy) nun über eine **verschlüsselte TCP-Verbindung** verfügen, können sie die **HTTP-Kommunikation** starten.

Der Client sendet also einen **HTTPS-Request**. Das ist einfach ein HTTP-Request über eine verschlüsselte TLS-Verbindung.

<img src="/img/deployment/https/https04.drawio.svg">

### Den Request entschlüsseln { #decrypt-the-request }

Der TLS-Terminierungsproxy würde die vereinbarte Verschlüsselung zum **Entschlüsseln des Requests** verwenden und den **einfachen (entschlüsselten) HTTP-Request** an den Prozess weiterleiten, der die Anwendung ausführt (z. B. einen Prozess, bei dem Uvicorn die FastAPI-Anwendung ausführt).

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP-Response { #http-response }

Die Anwendung würde den Request verarbeiten und eine **einfache (unverschlüsselte) HTTP-Response** an den TLS-Terminierungsproxy senden.

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS-Response { #https-response }

Der TLS-Terminierungsproxy würde dann die Response mithilfe der zuvor vereinbarten Kryptografie (als das Zertifikat für `someapp.example.com` verhandelt wurde) **verschlüsseln** und sie an den Browser zurücksenden.

Als Nächstes überprüft der Browser, ob die Response gültig und mit dem richtigen kryptografischen Schlüssel usw. verschlüsselt ist. Anschließend **entschlüsselt er die Response** und verarbeitet sie.

<img src="/img/deployment/https/https07.drawio.svg">

Der Client (Browser) weiß, dass die Response vom richtigen Server kommt, da dieser die Kryptografie verwendet, die zuvor mit dem **HTTPS-Zertifikat** vereinbart wurde.

### Mehrere Anwendungen { #multiple-applications }

Auf demselben Server (oder denselben Servern) könnten sich **mehrere Anwendungen** befinden, beispielsweise andere API-Programme oder eine Datenbank.

Nur ein Prozess kann diese spezifische IP und den Port verarbeiten (in unserem Beispiel der TLS-Terminierungsproxy), aber die anderen Anwendungen/Prozesse können auch auf dem/den Server(n) ausgeführt werden, solange sie nicht versuchen, dieselbe **Kombination aus öffentlicher IP und Port** zu verwenden.

<img src="/img/deployment/https/https08.drawio.svg">

Auf diese Weise könnte der TLS-Terminierungsproxy HTTPS und Zertifikate für **mehrere Domains**, für mehrere Anwendungen, verarbeiten und die Requests dann jeweils an die richtige Anwendung weiterleiten.

### Verlängerung des Zertifikats { #certificate-renewal }

Irgendwann in der Zukunft würde jedes Zertifikat **ablaufen** (etwa 3 Monate nach dem Erwerb).

Und dann gäbe es ein anderes Programm (in manchen Fällen ist es ein anderes Programm, in manchen Fällen ist es derselbe TLS-Terminierungsproxy), das mit Let's Encrypt kommuniziert und das/die Zertifikat(e) erneuert.

<img src="/img/deployment/https/https.drawio.svg">

Die **TLS-Zertifikate** sind **einem Domainnamen zugeordnet**, nicht einer IP-Adresse.

Um die Zertifikate zu erneuern, muss das erneuernde Programm der Behörde (Let's Encrypt) **nachweisen**, dass es diese Domain tatsächlich **besitzt und kontrolliert**.

Um dies zu erreichen und den unterschiedlichen Anwendungsanforderungen gerecht zu werden, gibt es mehrere Möglichkeiten. Einige beliebte Methoden sind:

* **Einige DNS-Einträge ändern**.
    * Hierfür muss das erneuernde Programm die APIs des DNS-Anbieters unterstützen. Je nachdem, welchen DNS-Anbieter Sie verwenden, kann dies eine Option sein oder auch nicht.
* **Als Server ausführen** (zumindest während des Zertifikatserwerbsvorgangs), auf der öffentlichen IP-Adresse, die der Domain zugeordnet ist.
    * Wie oben erwähnt, kann nur ein Prozess eine bestimmte IP und einen bestimmten Port überwachen.
    * Das ist einer der Gründe, warum es sehr nützlich ist, wenn derselbe TLS-Terminierungsproxy auch den Zertifikats-Erneuerungsprozess übernimmt.
    * Andernfalls müssen Sie möglicherweise den TLS-Terminierungsproxy vorübergehend stoppen, das Programm starten, welches die neuen Zertifikate beschafft, diese dann mit dem TLS-Terminierungsproxy konfigurieren und dann den TLS-Terminierungsproxy neu starten. Das ist nicht ideal, da Ihre Anwendung(en) während der Zeit, in der der TLS-Terminierungsproxy ausgeschaltet ist, nicht erreichbar ist/sind.

Dieser ganze Erneuerungsprozess, während die Anwendung weiterhin bereitgestellt wird, ist einer der Hauptgründe, warum Sie ein **separates System zur Verarbeitung von HTTPS** mit einem TLS-Terminierungsproxy haben möchten, anstatt einfach die TLS-Zertifikate direkt mit dem Anwendungsserver zu verwenden (z. B. Uvicorn).

## Proxy-<abbr title="weitergeleitete Header">Forwarded-Header</abbr> { #proxy-forwarded-headers }

Wenn Sie einen Proxy zur Verarbeitung von HTTPS verwenden, weiß Ihr **Anwendungsserver** (z. B. Uvicorn über das FastAPI CLI) nichts über den HTTPS-Prozess, er kommuniziert per einfachem HTTP mit dem **TLS-Terminierungsproxy**.

Dieser **Proxy** würde normalerweise unmittelbar vor dem Übermitteln der Anfrage an den **Anwendungsserver** einige HTTP-Header dynamisch setzen, um dem Anwendungsserver mitzuteilen, dass der Request vom Proxy **weitergeleitet** wird.

/// note | Technische Details

Die Proxy-Header sind:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

Trotzdem, da der **Anwendungsserver** nicht weiß, dass er sich hinter einem vertrauenswürdigen **Proxy** befindet, würde er diesen Headern standardmäßig nicht vertrauen.

Sie können den **Anwendungsserver** jedoch so konfigurieren, dass er den vom **Proxy** gesendeten *Forwarded*-Headern vertraut. Wenn Sie das FastAPI CLI verwenden, können Sie die *CLI-Option* `--forwarded-allow-ips` nutzen, um anzugeben, von welchen IPs er diesen *Forwarded*-Headern vertrauen soll.

Wenn der **Anwendungsserver** beispielsweise nur Kommunikation vom vertrauenswürdigen **Proxy** empfängt, können Sie `--forwarded-allow-ips="*"` setzen, um allen eingehenden IPs zu vertrauen, da er nur Requests von der vom **Proxy** verwendeten IP erhalten wird.

Auf diese Weise kann die Anwendung ihre eigene öffentliche URL, ob sie HTTPS verwendet, die Domain, usw. erkennen.

Das ist z. B. nützlich, um <abbr title="Redirect – Umleitung">Redirects</abbr> korrekt zu handhaben.

/// tip | Tipp

Mehr dazu finden Sie in der Dokumentation zu [Hinter einem Proxy – Proxy-Forwarded-Header aktivieren](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## Zusammenfassung { #recap }

**HTTPS** zu haben ist sehr wichtig und in den meisten Fällen eine **kritische Anforderung**. Die meiste Arbeit, die Sie als Entwickler in Bezug auf HTTPS aufwenden müssen, besteht lediglich darin, **diese Konzepte zu verstehen** und wie sie funktionieren.

Sobald Sie jedoch die grundlegenden Informationen zu **HTTPS für Entwickler** kennen, können Sie verschiedene Tools problemlos kombinieren und konfigurieren, um alles auf einfache Weise zu verwalten.

In einigen der nächsten Kapitel zeige ich Ihnen einige konkrete Beispiele für die Einrichtung von **HTTPS** für **FastAPI**-Anwendungen. 🔒
