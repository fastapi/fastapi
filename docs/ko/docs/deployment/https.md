# HTTPS 알아보기 { #about-https }

HTTPS는 그냥 “켜져 있거나” 아니면 “꺼져 있는” 것이라고 생각하기 쉽습니다.

하지만 실제로는 훨씬 더 복잡합니다.

/// tip | 팁

바쁘거나 별로 신경 쓰고 싶지 않다면, 다음 섹션에서 다양한 기법으로 모든 것을 설정하는 단계별 안내를 계속 보세요.

///

소비자 관점에서 **HTTPS의 기본을 배우려면** <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/</a>를 확인하세요.

이제 **개발자 관점**에서 HTTPS를 생각할 때 염두에 두어야 할 여러 가지가 있습니다:

* HTTPS를 사용하려면, **서버**가 **제3자**가 발급한 **"인증서(certificates)"**를 **보유**해야 합니다.
    * 이 인증서는 실제로 제3자가 “생성”해 주는 것이고, 서버가 만드는 것이 아니라 제3자로부터 **발급/획득**하는 것입니다.
* 인증서에는 **유효 기간**이 있습니다.
    * 즉, **만료**됩니다.
    * 그리고 나면 제3자로부터 다시 **갱신**해서 **재발급/재획득**해야 합니다.
* 연결의 암호화는 **TCP 레벨**에서 일어납니다.
    * 이는 **HTTP보다 한 계층 아래**입니다.
    * 따라서 **인증서와 암호화** 처리는 **HTTP 이전**에 수행됩니다.
* **TCP는 "도메인"을 모릅니다.** IP 주소만 압니다.
    * 어떤 **특정 도메인**을 요청했는지에 대한 정보는 **HTTP 데이터**에 들어 있습니다.
* **HTTPS 인증서**는 특정 **도메인**을 “인증”하지만, 프로토콜과 암호화는 TCP 레벨에서 일어나며, 어떤 도메인을 다루는지 **알기 전에** 처리됩니다.
* **기본적으로** 이는 IP 주소 하나당 **HTTPS 인증서 하나만** 둘 수 있다는 뜻입니다.
    * 서버가 아무리 크든, 그 위에 올린 각 애플리케이션이 아무리 작든 상관없습니다.
    * 하지만 이에 대한 **해결책**이 있습니다.
* **TLS** 프로토콜(HTTP 이전, TCP 레벨에서 암호화를 처리하는 것)에 대한 **확장** 중에 **<a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication - 서버 이름 표시">SNI</abbr></a>**라는 것이 있습니다.
    * 이 SNI 확장을 사용하면, 단일 서버(**단일 IP 주소**)에서 **여러 HTTPS 인증서**를 사용하고 **여러 HTTPS 도메인/애플리케이션**을 제공할 수 있습니다.
    * 이를 위해서는 서버에서 **공개 IP 주소**로 리스닝하는 **하나의** 컴포넌트(프로그램)가 서버에 있는 **모든 HTTPS 인증서**에 접근할 수 있어야 합니다.
* 보안 연결을 얻은 **이후에도**, 통신 프로토콜 자체는 **여전히 HTTP**입니다.
    * **HTTP 프로토콜**로 전송되더라도, 내용은 **암호화**되어 있습니다.

일반적으로 서버(머신, 호스트 등)에는 **프로그램/HTTP 서버 하나**를 실행해 **HTTPS 관련 부분 전체**를 관리하게 합니다: **암호화된 HTTPS 요청**을 받고, 복호화된 **HTTP 요청**을 같은 서버에서 실행 중인 실제 HTTP 애플리케이션(이 경우 **FastAPI** 애플리케이션)으로 전달하고, 애플리케이션의 **HTTP 응답**을 받아 적절한 **HTTPS 인증서**로 **암호화**한 뒤 **HTTPS**로 클라이언트에 다시 보내는 역할입니다. 이런 서버를 흔히 **<a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS Termination Proxy</a>**라고 부릅니다.

TLS Termination Proxy로 사용할 수 있는 옵션은 다음과 같습니다:

* Traefik (인증서 갱신도 처리 가능)
* Caddy (인증서 갱신도 처리 가능)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Let's Encrypt 이전에는 이러한 **HTTPS 인증서**가 신뢰할 수 있는 제3자에 의해 판매되었습니다.

인증서를 획득하는 과정은 번거롭고, 꽤 많은 서류 작업이 필요했으며, 인증서도 상당히 비쌌습니다.

하지만 그 후 **<a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a>**가 만들어졌습니다.

이는 Linux Foundation의 프로젝트입니다. 표준 암호학적 보안을 모두 사용하는 **HTTPS 인증서**를 **무료로**, 자동화된 방식으로 제공합니다. 이 인증서들은 수명이 짧고(약 3개월) 그래서 유효 기간이 짧은 만큼 **실제로 보안이 더 좋아지기도** 합니다.

도메인은 안전하게 검증되며 인증서는 자동으로 생성됩니다. 또한 이로 인해 인증서 갱신도 자동화할 수 있습니다.

목표는 인증서의 발급과 갱신을 자동화하여 **무료로, 영구히, 안전한 HTTPS**를 사용할 수 있게 하는 것입니다.

## 개발자를 위한 HTTPS { #https-for-developers }

개발자에게 중요한 개념들을 중심으로, HTTPS API가 단계별로 어떻게 보일 수 있는지 예시를 들어 보겠습니다.

### 도메인 이름 { #domain-name }

아마도 시작은 **도메인 이름**을 **획득**하는 것일 겁니다. 그 다음 DNS 서버(아마 같은 클라우드 제공업체)에서 이를 설정합니다.

대개 클라우드 서버(가상 머신) 같은 것을 사용하게 되고, 거기에는 <abbr title="That doesn't change - 변하지 않음">fixed</abbr> **공개 IP 주소**가 있습니다.

DNS 서버(들)에서 **도메인**이 서버의 **공개 IP 주소**를 가리키도록 레코드(“`A record`”)를 설정합니다.

보통은 처음 한 번, 모든 것을 설정할 때만 이 작업을 합니다.

/// tip | 팁

도메인 이름 부분은 HTTPS보다 훨씬 이전 단계지만, 모든 것이 도메인과 IP 주소에 의존하므로 여기서 언급할 가치가 있습니다.

///

### DNS { #dns }

이제 실제 HTTPS 부분에 집중해 보겠습니다.

먼저 브라우저는 **DNS 서버**에 질의하여, 여기서는 `someapp.example.com`이라는 **도메인에 대한 IP**가 무엇인지 확인합니다.

DNS 서버는 브라우저에게 특정 **IP 주소**를 사용하라고 알려줍니다. 이는 DNS 서버에 설정해 둔, 서버가 사용하는 공개 IP 주소입니다.

<img src="/img/deployment/https/https01.drawio.svg">

### TLS 핸드셰이크 시작 { #tls-handshake-start }

그 다음 브라우저는 **포트 443**(HTTPS 포트)에서 해당 IP 주소와 통신합니다.

통신의 첫 부분은 클라이언트와 서버 사이의 연결을 설정하고, 사용할 암호화 키 등을 결정하는 과정입니다.

<img src="/img/deployment/https/https02.drawio.svg">

클라이언트와 서버가 TLS 연결을 설정하기 위해 상호작용하는 이 과정을 **TLS 핸드셰이크**라고 합니다.

### SNI 확장을 사용하는 TLS { #tls-with-sni-extension }

서버에서는 특정 **IP 주소**의 특정 **포트**에서 **하나의 프로세스만** 리스닝할 수 있습니다. 같은 IP 주소에서 다른 포트로 리스닝하는 프로세스는 있을 수 있지만, IP 주소와 포트 조합마다 하나만 가능합니다.

TLS(HTTPS)는 기본적으로 특정 포트 `443`을 사용합니다. 따라서 우리가 필요한 포트는 이것입니다.

이 포트에서 하나의 프로세스만 리스닝할 수 있으므로, 그 역할을 하는 프로세스는 **TLS Termination Proxy**가 됩니다.

TLS Termination Proxy는 하나 이상의 **TLS 인증서**(HTTPS 인증서)에 접근할 수 있습니다.

앞에서 설명한 **SNI 확장**을 사용해, TLS Termination Proxy는 이 연결에 사용할 수 있는 TLS(HTTPS) 인증서들 중에서 클라이언트가 기대하는 도메인과 일치하는 것을 확인해 선택합니다.

이 경우에는 `someapp.example.com`에 대한 인증서를 사용합니다.

<img src="/img/deployment/https/https03.drawio.svg">

클라이언트는 이미 해당 TLS 인증서를 생성한 주체(여기서는 Let's Encrypt이지만, 이는 뒤에서 다시 보겠습니다)를 **신뢰**하므로, 인증서가 유효한지 **검증**할 수 있습니다.

그 다음 인증서를 사용해 클라이언트와 TLS Termination Proxy는 나머지 **TCP 통신**을 어떻게 **암호화할지 결정**합니다. 이로써 **TLS 핸드셰이크** 단계가 완료됩니다.

이후 클라이언트와 서버는 TLS가 제공하는 **암호화된 TCP 연결**을 갖게 됩니다. 그리고 그 연결을 사용해 실제 **HTTP 통신**을 시작할 수 있습니다.

이것이 바로 **HTTPS**입니다. 순수(암호화되지 않은) TCP 연결 대신 **안전한 TLS 연결** 안에서 **HTTP**를 그대로 사용하는 것입니다.

/// tip | 팁

통신의 암호화는 HTTP 레벨이 아니라 **TCP 레벨**에서 일어난다는 점에 주의하세요.

///

### HTTPS 요청 { #https-request }

이제 클라이언트와 서버(구체적으로는 브라우저와 TLS Termination Proxy)가 **암호화된 TCP 연결**을 갖게 되었으니 **HTTP 통신**을 시작할 수 있습니다.

따라서 클라이언트는 **HTTPS 요청**을 보냅니다. 이는 암호화된 TLS 연결을 통해 전달되는 HTTP 요청일 뿐입니다.

<img src="/img/deployment/https/https04.drawio.svg">

### 요청 복호화 { #decrypt-the-request }

TLS Termination Proxy는 합의된 암호화를 사용해 **요청을 복호화**하고, 애플리케이션을 실행 중인 프로세스(예: FastAPI 애플리케이션을 실행하는 Uvicorn 프로세스)에 **일반(복호화된) HTTP 요청**을 전달합니다.

<img src="/img/deployment/https/https05.drawio.svg">

### HTTP 응답 { #http-response }

애플리케이션은 요청을 처리하고 **일반(암호화되지 않은) HTTP 응답**을 TLS Termination Proxy로 보냅니다.

<img src="/img/deployment/https/https06.drawio.svg">

### HTTPS 응답 { #https-response }

그 다음 TLS Termination Proxy는 이전에 합의한 암호화( `someapp.example.com` 인증서로 시작된 것)를 사용해 **응답을 암호화**하고, 브라우저로 다시 보냅니다.

이후 브라우저는 응답이 유효한지, 올바른 암호화 키로 암호화되었는지 등을 확인합니다. 그런 다음 **응답을 복호화**하고 처리합니다.

<img src="/img/deployment/https/https07.drawio.svg">

클라이언트(브라우저)는 앞서 **HTTPS 인증서**로 합의한 암호화를 사용하고 있으므로, 해당 응답이 올바른 서버에서 왔다는 것을 알 수 있습니다.

### 여러 애플리케이션 { #multiple-applications }

같은 서버(또는 여러 서버)에는 예를 들어 다른 API 프로그램이나 데이터베이스처럼 **여러 애플리케이션**이 있을 수 있습니다.

특정 IP와 포트 조합은 하나의 프로세스만 처리할 수 있지만(예시에서는 TLS Termination Proxy), 다른 애플리케이션/프로세스도 **공개 IP와 포트 조합**을 동일하게 쓰려고만 하지 않는다면 서버에서 함께 실행될 수 있습니다.

<img src="/img/deployment/https/https08.drawio.svg">

이렇게 하면 TLS Termination Proxy가 **여러 도메인**에 대한 HTTPS와 인증서를 **여러 애플리케이션**에 대해 처리하고, 각 경우에 맞는 애플리케이션으로 요청을 전달할 수 있습니다.

### 인증서 갱신 { #certificate-renewal }

미래의 어느 시점에는 각 인증서가 **만료**됩니다(획득 후 약 3개월).

그 다음에는 또 다른 프로그램(경우에 따라 별도 프로그램일 수도 있고, 경우에 따라 같은 TLS Termination Proxy일 수도 있습니다)이 Let's Encrypt와 통신하여 인증서를 갱신합니다.

<img src="/img/deployment/https/https.drawio.svg">

**TLS 인증서**는 IP 주소가 아니라 **도메인 이름**과 **연결**되어 있습니다.

따라서 인증서를 갱신하려면, 갱신 프로그램이 권한 기관(Let's Encrypt)에게 해당 도메인을 실제로 **“소유”하고 제어하고 있음**을 **증명**해야 합니다.

이를 위해, 그리고 다양한 애플리케이션 요구를 수용하기 위해 여러 방법이 있습니다. 널리 쓰이는 방법은 다음과 같습니다:

* **일부 DNS 레코드 수정**.
    * 이를 위해서는 갱신 프로그램이 DNS 제공업체의 API를 지원해야 하므로, 사용하는 DNS 제공업체에 따라 가능할 수도, 아닐 수도 있습니다.
* 도메인과 연결된 공개 IP 주소에서 **서버로 실행**(적어도 인증서 발급 과정 동안).
    * 앞에서 말했듯 특정 IP와 포트에서는 하나의 프로세스만 리스닝할 수 있습니다.
    * 이것이 동일한 TLS Termination Proxy가 인증서 갱신 과정까지 처리할 때 매우 유용한 이유 중 하나입니다.
    * 그렇지 않으면 TLS Termination Proxy를 잠시 중지하고, 갱신 프로그램을 시작해 인증서를 획득한 다음, TLS Termination Proxy에 인증서를 설정하고, 다시 TLS Termination Proxy를 재시작해야 할 수도 있습니다. 이는 TLS Termination Proxy가 꺼져 있는 동안 앱(들)을 사용할 수 없으므로 이상적이지 않습니다.

앱을 계속 제공하면서 이 갱신 과정을 처리할 수 있는 것은, 애플리케이션 서버(예: Uvicorn)에서 TLS 인증서를 직접 쓰는 대신 TLS Termination Proxy로 HTTPS를 처리하는 **별도의 시스템**을 두고 싶어지는 주요 이유 중 하나입니다.

## 프록시 전달 헤더 { #proxy-forwarded-headers }

프록시를 사용해 HTTPS를 처리할 때, **애플리케이션 서버**(예: FastAPI CLI를 통한 Uvicorn)는 HTTPS 과정에 대해 아무것도 알지 못하고 **TLS Termination Proxy**와는 일반 HTTP로 통신합니다.

이 **프록시**는 보통 요청을 **애플리케이션 서버**에 전달하기 전에, 요청이 프록시에 의해 **전달(forwarded)**되고 있음을 애플리케이션 서버가 알 수 있도록 일부 HTTP 헤더를 즉석에서 설정합니다.

/// note | 기술 세부사항

프록시 헤더는 다음과 같습니다:

* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For" class="external-link" target="_blank">X-Forwarded-For</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto" class="external-link" target="_blank">X-Forwarded-Proto</a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host" class="external-link" target="_blank">X-Forwarded-Host</a>

///

그럼에도 불구하고 **애플리케이션 서버**는 자신이 신뢰할 수 있는 **프록시** 뒤에 있다는 것을 모르므로, 기본적으로는 그 헤더들을 신뢰하지 않습니다.

하지만 **애플리케이션 서버**가 **프록시**가 보낸 *forwarded* 헤더를 신뢰하도록 설정할 수 있습니다. FastAPI CLI를 사용하고 있다면, *CLI Option* `--forwarded-allow-ips`를 사용해 어떤 IP에서 온 *forwarded* 헤더를 신뢰할지 지정할 수 있습니다.

예를 들어 **애플리케이션 서버**가 신뢰하는 **프록시**로부터만 통신을 받는다면, `--forwarded-allow-ips="*"`로 설정해 들어오는 모든 IP를 신뢰하게 할 수 있습니다. 어차피 **프록시**가 사용하는 IP에서만 요청을 받게 될 것이기 때문입니다.

이렇게 하면 애플리케이션은 자신이 사용하는 공개 URL이 무엇인지, HTTPS를 사용하는지, 도메인이 무엇인지 등을 알 수 있습니다.

예를 들어 리다이렉트를 올바르게 처리하는 데 유용합니다.

/// tip | 팁

이에 대해서는 [프록시 뒤에서 실행하기 - 프록시 전달 헤더 활성화](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers){.internal-link target=_blank} 문서에서 더 알아볼 수 있습니다.

///

## 요약 { #recap }

**HTTPS**는 매우 중요하며, 대부분의 경우 상당히 **핵심적**입니다. 개발자가 HTTPS와 관련해 해야 하는 노력의 대부분은 결국 **이 개념들을 이해**하고 그것들이 어떻게 동작하는지 파악하는 것입니다.

하지만 **개발자를 위한 HTTPS**의 기본 정보를 알고 나면, 여러 도구를 쉽게 조합하고 설정하여 모든 것을 간단하게 관리할 수 있습니다.

다음 장들에서는 **FastAPI** 애플리케이션을 위한 **HTTPS** 설정 방법을 여러 구체적인 예시로 보여드리겠습니다. 🔒
