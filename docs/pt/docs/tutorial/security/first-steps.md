# Segurança - Primeiros Passos { #security-first-steps }

Vamos imaginar que você tem a sua API de **backend** em algum domínio.

E você tem um **frontend** em outro domínio ou em um path diferente no mesmo domínio (ou em uma aplicação mobile).

E você quer uma maneira de o frontend autenticar com o backend, usando um **username** e **password**.

Podemos usar **OAuth2** para construir isso com o **FastAPI**.

Mas vamos poupar o seu tempo de ler toda a especificação extensa apenas para achar as pequenas informações de que você precisa.

Vamos usar as ferramentas fornecidas pelo **FastAPI** para lidar com segurança.

## Como Parece { #how-it-looks }

Vamos primeiro usar o código e ver como funciona, e depois voltaremos para entender o que está acontecendo.

## Crie um `main.py` { #create-main-py }

Copie o exemplo em um arquivo `main.py`:

{* ../../docs_src/security/tutorial001_an_py39.py *}

## Execute-o { #run-it }

/// info | Informação

O pacote <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> é instalado automaticamente com o **FastAPI** quando você executa o comando `pip install "fastapi[standard]"`.

Entretanto, se você usar o comando `pip install fastapi`, o pacote `python-multipart` não é incluído por padrão.

Para instalá-lo manualmente, certifique-se de criar um [ambiente virtual](../../virtual-environments.md){.internal-link target=_blank}, ativá-lo e então instalá-lo com:

```console
$ pip install python-multipart
```

Isso ocorre porque o **OAuth2** usa "form data" para enviar o `username` e o `password`.

///

Execute o exemplo com:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Verifique-o { #check-it }

Vá até a documentação interativa em: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá algo deste tipo:

<img src="/img/tutorial/security/image01.png">

/// check | Botão Autorizar!

Você já tem um novo botão 'Authorize'.

E sua operação de rota tem um pequeno cadeado no canto superior direito em que você pode clicar.

///

E se você clicar, verá um pequeno formulário de autorização para digitar um `username` e um `password` (e outros campos opcionais):

<img src="/img/tutorial/security/image02.png">

/// note | Nota

Não importa o que você digite no formulário, ainda não vai funcionar. Mas nós vamos chegar lá.

///

Claro que este não é o frontend para os usuários finais, mas é uma ótima ferramenta automática para documentar interativamente toda a sua API.

Pode ser usada pelo time de frontend (que pode ser você mesmo).

Pode ser usada por aplicações e sistemas de terceiros.

E também pode ser usada por você mesmo, para depurar, verificar e testar a mesma aplicação.

## O fluxo de `password` { #the-password-flow }

Agora vamos voltar um pouco e entender o que é isso tudo.

O "fluxo" `password` é uma das formas ("fluxos") definidas no OAuth2 para lidar com segurança e autenticação.

O OAuth2 foi projetado para que o backend ou a API pudesse ser independente do servidor que autentica o usuário.

Mas, neste caso, a mesma aplicação **FastAPI** irá lidar com a API e com a autenticação.

Então, vamos rever de um ponto de vista simplificado:

* O usuário digita o `username` e o `password` no frontend e pressiona `Enter`.
* O frontend (rodando no navegador do usuário) envia esse `username` e `password` para uma URL específica na nossa API (declarada com `tokenUrl="token"`).
* A API verifica esse `username` e `password`, e responde com um "token" (ainda não implementamos nada disso).
    * Um "token" é apenas uma string com algum conteúdo que podemos usar depois para verificar esse usuário.
    * Normalmente, um token é definido para expirar depois de algum tempo.
        * Então, o usuário terá que fazer login novamente em algum momento.
        * E se o token for roubado, o risco é menor. Não é como uma chave permanente que funcionará para sempre (na maioria dos casos).
* O frontend armazena esse token temporariamente em algum lugar.
* O usuário clica no frontend para ir para outra seção do aplicativo web.
* O frontend precisa buscar mais dados da API.
    * Mas precisa de autenticação para aquele endpoint específico.
    * Então, para autenticar com nossa API, ele envia um header `Authorization` com o valor `Bearer ` mais o token.
    * Se o token contém `foobar`, o conteúdo do header `Authorization` seria: `Bearer foobar`.

## O `OAuth2PasswordBearer` do **FastAPI** { #fastapis-oauth2passwordbearer }

O **FastAPI** fornece várias ferramentas, em diferentes níveis de abstração, para implementar essas funcionalidades de segurança.

Neste exemplo, vamos usar **OAuth2**, com o fluxo **Password**, usando um token **Bearer**. Fazemos isso usando a classe `OAuth2PasswordBearer`.

/// info | Informação

Um token "bearer" não é a única opção.

Mas é a melhor para o nosso caso de uso.

E pode ser a melhor para a maioria dos casos de uso, a menos que você seja um especialista em OAuth2 e saiba exatamente por que existe outra opção que se adapta melhor às suas necessidades.

Nesse caso, o **FastAPI** também fornece as ferramentas para construí-la.

///

Quando criamos uma instância da classe `OAuth2PasswordBearer`, passamos o parâmetro `tokenUrl`. Esse parâmetro contém a URL que o client (o frontend rodando no navegador do usuário) usará para enviar o `username` e o `password` para obter um token.

{* ../../docs_src/security/tutorial001_an_py39.py hl[8] *}

/// tip | Dica

Aqui `tokenUrl="token"` refere-se a uma URL relativa `token` que ainda não criamos. Como é uma URL relativa, é equivalente a `./token`.

Como estamos usando uma URL relativa, se sua API estivesse localizada em `https://example.com/`, então se referiria a `https://example.com/token`. Mas se sua API estivesse localizada em `https://example.com/api/v1/`, então se referiria a `https://example.com/api/v1/token`.

Usar uma URL relativa é importante para garantir que sua aplicação continue funcionando mesmo em um caso de uso avançado como [Atrás de um Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}.

///

Esse parâmetro não cria aquele endpoint/operação de rota, mas declara que a URL `/token` será aquela que o client deve usar para obter o token. Essa informação é usada no OpenAPI e depois nos sistemas de documentação interativa da API.

Em breve também criaremos a operação de rota real.

/// info | Informação

Se você é um "Pythonista" muito rigoroso, pode não gostar do estilo do nome do parâmetro `tokenUrl` em vez de `token_url`.

Isso ocorre porque ele usa o mesmo nome da especificação do OpenAPI. Assim, se você precisar investigar mais sobre qualquer um desses esquemas de segurança, pode simplesmente copiar e colar para encontrar mais informações sobre isso.

///

A variável `oauth2_scheme` é uma instância de `OAuth2PasswordBearer`, mas também é "chamável" (callable).

Ela pode ser chamada como:

```Python
oauth2_scheme(some, parameters)
```

Então, pode ser usada com `Depends`.

### Use-o { #use-it }

Agora você pode passar esse `oauth2_scheme` em uma dependência com `Depends`.

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

Essa dependência fornecerá uma `str` que é atribuída ao parâmetro `token` da função de operação de rota.

O **FastAPI** saberá que pode usar essa dependência para definir um "esquema de segurança" no esquema OpenAPI (e na documentação automática da API).

/// info | Detalhes Técnicos

O **FastAPI** saberá que pode usar a classe `OAuth2PasswordBearer` (declarada em uma dependência) para definir o esquema de segurança no OpenAPI porque ela herda de `fastapi.security.oauth2.OAuth2`, que por sua vez herda de `fastapi.security.base.SecurityBase`.

Todos os utilitários de segurança que se integram com o OpenAPI (e com a documentação automática da API) herdam de `SecurityBase`, é assim que o **FastAPI** sabe como integrá-los ao OpenAPI.

///

## O que ele faz { #what-it-does }

Ele irá procurar na requisição pelo header `Authorization`, verificar se o valor é `Bearer ` mais algum token e retornará o token como uma `str`.

Se não houver um header `Authorization`, ou se o valor não tiver um token `Bearer `, ele responderá diretamente com um erro de status 401 (`UNAUTHORIZED`).

Você nem precisa verificar se o token existe para retornar um erro. Você pode ter certeza de que, se sua função for executada, ela terá uma `str` nesse token.

Você já pode experimentar na documentação interativa:

<img src="/img/tutorial/security/image03.png">

Ainda não estamos verificando a validade do token, mas isso já é um começo.

## Recapitulando { #recap }

Então, com apenas 3 ou 4 linhas extras, você já tem alguma forma primitiva de segurança.
