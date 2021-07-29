# Security - Primeiros passos

Vamos imaginar que você tem sua API **backend** em um domínio.

E você tem um **frontend** em outro domínio ou em um caminho diferente no mesmo domínio (ou em uma aplicação mobile).

E você quer criar um caminho para o frontend autenticar com o backend, usando **usuário** e **senha**.

Podemos usar **OAuth2** para criá-lo com o **FastAPI**.

Mas vamos ganhar o tempo de leitura de longas especificações só para encontrar esses pequenos pedaços de informações que você precisa.

Vamos usar as ferramentas disponibilizadas pelo **FastAPI** para lidar com a segurança.

## Como seria

Primeiro vamos só usar o código e ver como ele funciona, e depois nós iremos voltar para entender o que está acontecendo.

## Criando `main.py`

Copie o exemplo em um arquivo `main.py`:

```Python
{!../../../docs_src/security/tutorial001.py!}
```

## Execute

!!! info "Informação"
    Primeiro instale <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.
    Exemplo: `pip install python-multipart`.

    Isso porque o **OAuth2** usa "form data" para enviar `usuário` e `senha`.

Execute o exemplo:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Verifique

Vá para a documentação interativa em: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você irá ver algo como isso:

<img src="/img/tutorial/security/image01.png">

!!! check "Botão de autorização"
    Você já tem um botão "Authorize" novinho em folha.

    E onde está o seu *path* tem um pequeno cadeado no canto direito-superior que você pode clicar.

E se você clicar, você terá um pequeno formulário do tipo `usuário` e `senha` (e outros campos opcionais):

<img src="/img/tutorial/security/image02.png">

!!! note
    Não importa o que você escrever no formulário, isso não vai funcionar ainda. Mas nós iremos chegar lá.

Claro que isso não é o frontend destinado para o usuário final, mas é uma excelente ferramenta de automação para documentação interativa de toda sua API.

Pode ser usado pelo time de frontend (que pode ser você também).

Pode ser usado por aplicações e sistemas de terceiros.

E isso pode também ser usado por você, para _debug_, verificação e teste da mesma aplicação.

## O fluxo `senha`

Agora vamos voltar um pouco e entender o que é tudo isso.

O fluxo de `senha` é um dos caminhos (fluxos) definidos em OAuth2, para lidar com segurança e autenticação.

OAuth2 foi desenhado para que o backend ou API pudesse ser independente do servidor que autentica o usuário.

Mas nesse caso, a mesma aplicação **FastAPI** irá lidar com a API e a autenticação.

Então, vamos revisá-lo desse ponto de vista simplificado:
* O usuário escreve `usuario` e `senha` em um frontend, e pressiona `Enter`.
* O frontend (rodando no browser do usuário) envia aquele `username` e `password`paara uma URL específica em nossa API (declarada com `tokenUrl="token"`)
* A API verifica aquele `usuario` e `senha`, e responde com um "token" (nós não implementamos nada disso ainda).
    * Um "token" é uma string com algum conteúdo que nós podemos usar depois para verificar esse usuário.
    * Normalmente, um token expira após um certo tempo.
        * Então, o usuário terá que entrar novamente no futuro.
        * E se o token for roubado, o risco é menor. Isso não é como uma chave permanente que irá funcionar para sempre (na maioria dos casos).
* O frontend guarda aquele token temporariamente em algum lugar.
* O usuário clica no frontend para ir para outra seção da aplicação web do frontend.
* O fontend precisa buscar mais alguns dados da API.
    * Mas precisa autenticar naquele endpoint específico.
    * Então, para autenticar com nossa API, precisa de um header `Authorization` com um valor de `Bearer` e o token.
    * Se o token for `foobar`, o conteúdo do header `Authorization` seria: `Bearer foobar`.

## **FastAPI** `OAuth2PasswordBearer`

**FastAPI** disponibiliza diversas ferramentas em diferentes níveis de abstração para implementar esses recursos de segurança.

Nesse exemplo nós vamos usar **OAuth2**, com o fluxo de **senha**, usando um token **Bearer**. Nós faremos isso usando a classe `OAuth2PasswordBearer`.

!!! info "Informação"
    Um token "bearer" não é a única opção.

    Mas ele é a melhor para nosso caso de uso.

    E pode ser a melhor para a maioria dos casos de uso, a não ser que você seja um expert em OAuth2 e saiba exatamente por que a outra opção se encaixa melhor no que você precisa.

    Nesse caso, o **FastAPI** também disponibiliza as ferramentas para você criar isso.

Quando criamos uma instância da classe `OAuth2PasswordBearer` passamos o parâmetro `tokenUrl`. Esse parâmetro contém a URL que o cliente (o frontend rodando no browser do usuário) usará para enviar o `usuario` e `senha`  a fim de obter um token.

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! tip "Dica"
    Aqui `tokenUrl="token"` se refere a uma URL relativa a `token` que nós ainda não criamos. Como ela é uma URL relativa, equivale a `./token`.

    Por estarmos usando uma URL relativa, se sua API está localizada em `https://example.com/`, então ela seria refenciada para `https://example.com/token`. Mas se sua API estiver localizada em `https://example.com/api/v1/`, então ela seria referenciada para `https://example.com/api/v1/token`.

    Ao usar uma URL relativa é importante ter certeza que sua aplicação continue funcionando mesmo em uso avançado como [Behind a Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}.

Esse parametro não cria esse endpoint / *rota*, mas declara que a URL `/token` será aquele que o cliente deve usar para obter o token. Essa informação é usada na OpenAPI, e então no sistema de documentação interativa da API.

Em breve, criaremos um caminho para uma operação real.

!!! info "Informação"
    Se você é estritamente "Pythonista" você não vai gostar do estilo do parâmetro com nome `tokenUrl` em vez de `token_url`.

    Isso é porque está usando o mesmo nome especificado na OpenAPI. De modo que se você precisar investigar mais sobre algum desses esquemas de segurança você pode somente copiar e colar para encontrar mais informações sobre isso.

A variável `oauth2_scheme` é uma instância de `OAuth2PasswordBearer`, mas também é um "callable".

Pode ser chamada assim:

```Python
oauth2_scheme(alguns, parametros)
```

Então, pode ser usada com `Depends`.

### Utilização

Agora você pode passar esse `oauth2_schema` em uma dependência com `Depends`.

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

Essa dependência irá providenciar uma `str` que será atribuída ao parâmetro `token` de uma determinada *rota de operação funcional*.

O **FastAPI** saberá que e possível usar essa dependência para definir um "esquema de segurança" no esquema da OpenAPI (e a documentação automática da API).

!!! info "Detalhes técnicos"
    O **FastAPI** irá saber que é possível usar a classe `OAuth2PasswordBearer` (declarada em uma dependência) para definir o esquema de segurança na OpenAPI, porque isso herda de `fastapi.security.oauth2.OAuth2`, que por sua vez herda `fastapi.security.base.ScurityBase`.

    Todos os utilitários de segurança que integram com a OpenAPI (e a documentação automática da API) herdam de `SecurityBase`, é assim que o **FastAPI** consegue saber como integrá-los na OpenAPI.
## O que isso faz

Ele irá procurar no request header `Authorization`,  e checar se o valor é `Bearer` com algum token, e então retorna o token como um `str`.

Se não ver um header `Authorization`, ou o valor não tiver um token `Bearer `, irá responder diretamente com um código de erro com status 401 (`UNAUTHORIZED`).

Você não tem que checar se o token existe para retornar um erro. É certeza que se sua função for executada, irá ter um `str` naquele token.

Você pode tentar diretamente na documentação interativa:

<img src="/img/tutorial/security/image03.png">

Ainda não estamos verificando a validade do token, mas isso já é um começo.

## Recaptulando

Então, em somente 3 ou 4 linhas extras, você já tem uma forma primitiva de segurança.
