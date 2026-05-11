# Sobre HTTPS { #about-https }

É fácil assumir que HTTPS é algo que é apenas "habilitado" ou não.

Mas é bem mais complexo do que isso.

/// tip | Dica

Se você está com pressa ou não se importa, continue com as seções seguintes para instruções passo a passo para configurar tudo com diferentes técnicas.

///

Para aprender o básico de HTTPS do ponto de vista do consumidor, verifique [https://howhttps.works/](https://howhttps.works/).

Agora, a partir de uma perspectiva do desenvolvedor, aqui estão algumas coisas para ter em mente ao pensar em HTTPS:

* Para HTTPS, o servidor precisa ter "certificados" gerados por um terceiro.
    * Esses certificados são na verdade adquiridos de um terceiro, eles não são simplesmente "gerados".
* Certificados têm um tempo de vida.
    * Eles expiram.
    * E então eles precisam ser renovados, adquirindo-os novamente de um terceiro.
* A criptografia da conexão acontece no nível TCP.
    * Essa é uma camada abaixo do HTTP.
    * Portanto, o manuseio do certificado e da criptografia é feito antes do HTTP.
* O TCP não sabe sobre "domínios". Apenas sobre endereços IP.
    * As informações sobre o domínio específico solicitado vão nos dados HTTP.
* Os certificados HTTPS “certificam” um determinado domínio, mas o protocolo e a encriptação acontecem ao nível do TCP, antes de sabermos de que domínio se trata.
* Por padrão, isso significa que você só pode ter um certificado HTTPS por endereço IP.
    * Não importa o tamanho do seu servidor ou quão pequeno cada aplicativo que você tem nele possa ser.
    * No entanto, existe uma solução para isso.
* Há uma extensão para o protocolo TLS (aquele que lida com a criptografia no nível TCP, antes do HTTP) chamada [<abbr title="Server Name Indication - Indicação do Nome do Servidor">SNI</abbr>](https://en.wikipedia.org/wiki/Server_Name_Indication).
    * Esta extensão SNI permite que um único servidor (com um único endereço IP) tenha vários certificados HTTPS e atenda a vários domínios / aplicativos HTTPS.
    * Para que isso funcione, um único componente (programa) em execução no servidor, ouvindo no endereço IP público, deve ter todos os certificados HTTPS no servidor.
* Depois de obter uma conexão segura, o protocolo de comunicação ainda é HTTP.
    * Os conteúdos são criptografados, embora sejam enviados com o protocolo HTTP.

É uma prática comum ter um programa/servidor HTTP em execução no servidor (máquina, host, etc.) e gerenciar todas as partes HTTPS: recebendo as requisições HTTPS encriptadas, enviando as solicitações HTTP descriptografadas para o aplicativo HTTP real em execução no mesmo servidor (a aplicação FastAPI, neste caso), pegar a resposta HTTP do aplicativo, criptografá-la usando o certificado HTTPS apropriado e enviá-la de volta ao cliente usando HTTPS. Este servidor é frequentemente chamado de [Proxy de Terminação TLS](https://en.wikipedia.org/wiki/TLS_termination_proxy).

Algumas das opções que você pode usar como Proxy de Terminação TLS são:

* Traefik (que também pode gerenciar a renovação de certificados)
* Caddy (que também pode gerenciar a renovação de certificados)
* Nginx
* HAProxy

## Let's Encrypt { #lets-encrypt }

Antes de Let's Encrypt, esses certificados HTTPS eram vendidos por terceiros confiáveis.

O processo de aquisição de um desses certificados costumava ser complicado, exigia bastante papelada e os certificados eram bastante caros.

Mas então o [Let's Encrypt](https://letsencrypt.org/) foi criado.

Ele é um projeto da Linux Foundation que fornece certificados HTTPS gratuitamente. De forma automatizada. Esses certificados usam toda a segurança criptográfica padrão e têm vida curta (cerca de 3 meses), então a segurança é, na verdade, melhor por causa do seu lifespan reduzido.

Os domínios são verificados com segurança e os certificados são gerados automaticamente. Isso também permite automatizar a renovação desses certificados.

A ideia é automatizar a aquisição e renovação desses certificados, para que você tenha HTTPS seguro, de graça e para sempre.

## HTTPS para Desenvolvedores { #https-for-developers }

Aqui está um exemplo de como uma API HTTPS poderia ser estruturada, passo a passo, com foco principal nas ideias relevantes para desenvolvedores.

### Nome do domínio { #domain-name }

A etapa inicial provavelmente seria adquirir algum nome de domínio. Então, você iria configurá-lo em um servidor DNS (possivelmente no mesmo provedor em nuvem).

Você provavelmente usaria um servidor em nuvem (máquina virtual) ou algo parecido, e ele teria um <dfn title="Não muda ao longo do tempo. Não é dinâmico.">fixo</dfn> Endereço IP público.

No(s) servidor(es) DNS, você configuraria um registro (um `A record`) para apontar seu domínio para o endereço IP público do seu servidor.

Você provavelmente fará isso apenas uma vez, na primeira vez em que tudo estiver sendo configurado.

/// tip | Dica

Essa parte do Nome do Domínio se dá muito antes do HTTPS, mas como tudo depende do domínio e endereço IP público, vale a pena mencioná-la aqui.

///

### DNS { #dns }

Agora vamos focar em todas as partes que realmente fazem parte do HTTPS.

Primeiro, o navegador iria verificar com os servidores DNS qual o IP do domínio, nesse caso, `someapp.example.com`.

Os servidores DNS iriam informar o navegador para utilizar algum endereço IP específico. Esse seria o endereço IP público em uso no seu servidor, que você configurou nos servidores DNS.

<img src="/img/deployment/https/https01.drawio.svg">

### Início do Handshake TLS { #tls-handshake-start }

O navegador então irá comunicar-se com esse endereço IP na porta 443 (a porta HTTPS).

A primeira parte dessa comunicação é apenas para estabelecer a conexão entre o cliente e o servidor e para decidir as chaves criptográficas a serem utilizadas, etc.

<img src="/img/deployment/https/https02.drawio.svg">

Esse interação entre o cliente e o servidor para estabelecer uma conexão TLS é chamada de Handshake TLS.

### TLS com a Extensão SNI { #tls-with-sni-extension }

Apenas um processo no servidor pode se conectar a uma porta em um endereço IP. Poderiam existir outros processos conectados em outras portas desse mesmo endereço IP, mas apenas um para cada combinação de endereço IP e porta.

TLS (HTTPS) usa a porta `443` por padrão. Então essa é a porta que precisamos.

Como apenas um único processo pode se comunicar com essa porta, o processo que faria isso seria o Proxy de Terminação TLS.

O Proxy de Terminação TLS teria acesso a um ou mais certificados TLS (certificados HTTPS).

Utilizando a extensão SNI discutida acima, o Proxy de Terminação TLS iria checar qual dos certificados TLS (HTTPS) disponíveis deve ser usado para essa conexão, utilizando o que corresponda ao domínio esperado pelo cliente.

Nesse caso, ele usaria o certificado para `someapp.example.com`.

<img src="/img/deployment/https/https03.drawio.svg">

O cliente já confia na entidade que gerou o certificado TLS (nesse caso, o Let's Encrypt, mas veremos sobre isso mais tarde), então ele pode verificar que o certificado é válido.

Então, utilizando o certificado, o cliente e o Proxy de Terminação TLS decidem como encriptar o resto da comunicação TCP. Isso completa a parte do Handshake TLS.

Após isso, o cliente e o servidor possuem uma conexão TCP encriptada, que é provida pelo TLS. E então eles podem usar essa conexão para começar a comunicação HTTP propriamente dita.

E isso resume o que é HTTPS, apenas HTTP simples dentro de uma conexão TLS segura em vez de uma conexão TCP pura (não encriptada).

/// tip | Dica

Percebe que a encriptação da comunicação acontece no nível do TCP, não no nível do HTTP.

///

### Solicitação HTTPS { #https-request }

Agora que o cliente e servidor (especialmente o navegador e o Proxy de Terminação TLS) possuem uma conexão TCP encriptada, eles podem iniciar a comunicação HTTP.

Então, o cliente envia uma solicitação HTTPS. Que é apenas uma solicitação HTTP sobre uma conexão TLS encriptada.

<img src="/img/deployment/https/https04.drawio.svg">

### Desencripte a Solicitação { #decrypt-the-request }

O Proxy de Terminação TLS então usaria a encriptação combinada para desencriptar a solicitação, e transmitiria a solicitação básica (desencriptada) para o processo executando a aplicação (por exemplo, um processo com Uvicorn executando a aplicação FastAPI).

<img src="/img/deployment/https/https05.drawio.svg">

### Resposta HTTP { #http-response }

A aplicação processaria a solicitação e retornaria uma resposta HTTP básica (não encriptada) para o Proxy de Terminação TLS.

<img src="/img/deployment/https/https06.drawio.svg">

### Resposta HTTPS { #https-response }

O Proxy de Terminação TLS iria encriptar a resposta utilizando a criptografia combinada anteriormente (que foi definida com o certificado para `someapp.example.com`), e devolveria para o navegador.

No próximo passo, o navegador verifica que a resposta é válida e encriptada com a chave criptográfica correta, etc. E depois desencripta a resposta e a processa.

<img src="/img/deployment/https/https07.drawio.svg">

O cliente (navegador) saberá que a resposta vem do servidor correto por que ela usa a criptografia que foi combinada entre eles usando o certificado HTTPS anterior.

### Múltiplas Aplicações { #multiple-applications }

Podem existir múltiplas aplicações em execução no mesmo servidor (ou servidores), por exemplo: outras APIs ou um banco de dados.

Apenas um processo pode estar vinculado a um IP e porta (o Proxy de Terminação TLS, por exemplo), mas outras aplicações/processos também podem estar em execução no(s) servidor(es), desde que não tentem usar a mesma combinação de IP público e porta.

<img src="/img/deployment/https/https08.drawio.svg">

Dessa forma, o Proxy de Terminação TLS pode gerenciar o HTTPS e os certificados de múltiplos domínios, para múltiplas aplicações, e então transmitir as requisições para a aplicação correta em cada caso.

### Renovação de Certificados { #certificate-renewal }

Em algum momento futuro, cada certificado irá expirar (aproximadamente 3 meses após a aquisição).

E então, haverá outro programa (em alguns casos pode ser o próprio Proxy de Terminação TLS) que irá interagir com o Let's Encrypt e renovar o(s) certificado(s).

<img src="/img/deployment/https/https.drawio.svg">

Os certificados TLS são associados com um nome de domínio, e não a um endereço IP.

Então para renovar os certificados, o programa de renovação precisa provar para a autoridade (Let's Encrypt) que ele realmente "possui" e controla esse domínio.

Para fazer isso, e acomodar as necessidades de diferentes aplicações, existem diferentes opções para esse programa. Algumas escolhas populares são:

* Modificar alguns registros DNS
    * Para isso, o programa de renovação precisa ter suporte às APIs do provedor DNS, então, dependendo do provedor DNS que você utilize, isso pode ou não ser uma opção viável.
* Executar como um servidor (ao menos durante o processo de aquisição do certificado) no endereço IP público associado com o domínio.
    * Como dito anteriormente, apenas um processo pode estar ligado a uma porta e IP específicos.
    * Essa é uma dos motivos que fazem utilizar o mesmo Proxy de Terminação TLS para gerenciar a renovação de certificados ser tão útil.
    * Caso contrário, você pode ter que parar a execução do Proxy de Terminação TLS momentaneamente, inicializar o programa de renovação para adquirir os certificados, depois configurá-los com o Proxy de Terminação TLS, e então reiniciar o Proxy de Terminação TLS. Isso não é o ideal, já que sua(s) aplicação(ões) não vão estar disponíveis enquanto o Proxy de Terminação TLS estiver desligado.

Todo esse processo de renovação, enquanto o aplicativo ainda funciona, é uma das principais razões para preferir um sistema separado para gerenciar HTTPS com um Proxy de Terminação TLS em vez de usar os certificados TLS no servidor da aplicação diretamente (e.g. com o Uvicorn).

## Cabeçalhos encaminhados por Proxy { #proxy-forwarded-headers }

Ao usar um proxy para lidar com HTTPS, seu servidor de aplicação (por exemplo, Uvicorn via FastAPI CLI) não sabe nada sobre o processo de HTTPS; ele se comunica com HTTP simples com o Proxy de Terminação TLS.

Esse proxy normalmente define alguns cabeçalhos HTTP dinamicamente antes de transmitir a requisição para o servidor de aplicação, para informar ao servidor de aplicação que a requisição está sendo encaminhada pelo proxy.

/// note | Detalhes Técnicos

Os cabeçalhos do proxy são:

* [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
* [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
* [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

///

No entanto, como o servidor de aplicação não sabe que está atrás de um proxy confiável, por padrão ele não confiaria nesses cabeçalhos.

Mas você pode configurar o servidor de aplicação para confiar nos cabeçalhos encaminhados enviados pelo proxy. Se você estiver usando o FastAPI CLI, pode usar a opção de CLI `--forwarded-allow-ips` para dizer de quais IPs ele deve confiar nesses cabeçalhos encaminhados.

Por exemplo, se o servidor de aplicação só estiver recebendo comunicação do proxy confiável, você pode defini-lo como `--forwarded-allow-ips="*"` para fazê-lo confiar em todos os IPs de entrada, já que ele só receberá requisições de seja lá qual for o IP usado pelo proxy.

Dessa forma, a aplicação seria capaz de saber qual é sua própria URL pública, se está usando HTTPS, o domínio, etc.

Isso seria útil, por exemplo, para lidar corretamente com redirecionamentos.

/// tip | Dica

Você pode saber mais sobre isso na documentação em [Atrás de um Proxy - Habilitar cabeçalhos encaminhados pelo proxy](../advanced/behind-a-proxy.md#enable-proxy-forwarded-headers)

///

## Recapitulando { #recap }

Possuir HTTPS habilitado na sua aplicação é bastante importante, e até crítico na maioria dos casos. A maior parte do esforço que você tem que colocar sobre o HTTPS como desenvolvedor está em entender esses conceitos e como eles funcionam.

Mas uma vez que você saiba o básico de HTTPS para desenvolvedores, você pode combinar e configurar diferentes ferramentas facilmente para gerenciar tudo de uma forma simples.

Em alguns dos próximos capítulos, eu mostrarei para você vários exemplos concretos de como configurar o HTTPS para aplicações FastAPI. 🔒
