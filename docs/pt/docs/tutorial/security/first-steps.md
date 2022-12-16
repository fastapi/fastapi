# Segurança - Primeiros Passos

Vamos imaginar que você tem a sua API **backend** em algum domínio.

E você tem um **frontend** em outro domínio ou em um path diferente no mesmo domínio (ou em uma aplicação mobile).

E você quer uma maneira de o frontend autenticar o backend, usando um **username** e **senha**.

Nós podemos usar o **OAuth2** junto com o **FastAPI**.

Mas, vamos poupar-lhe o tempo de ler toda a especificação apenas para achar as pequenas informações que você precisa.

Vamos usar as ferramentas fornecidas pela **FastAPI** para lidar com segurança.

## Como Parece

Vamos primeiro usar o código e ver como funciona, e depois voltaremos para entender o que está acontecendo.

## Crie um `main.py`
Copie o exemplo em um arquivo `main.py`:

```Python
{!../../../docs_src/security/tutorial001.py!}
```

## Execute-o

!!! informação
	Primeiro, instale <a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>.

	Ex: `pip install python-multipart`.

	Isso ocorre porque o **OAuth2** usa "dados de um formulário" para mandar o **username** e **senha**.

Execute esse exemplo com:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

## Verifique-o

Vá até a documentação interativa em: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá algo deste tipo:

<img src="/img/tutorial/security/image01.png">

!!! marque o "botão de Autorizar!"
	Você já tem um novo "botão de autorizar!".

	E seu *path operation* tem um pequeno cadeado no canto superior direito que você pode clicar.

E se você clicar, você terá um pequeno formulário de autorização para digitar o `username` e `senha` (e outros campos opcionais):

<img src="/img/tutorial/security/image02.png">

!!! nota
	Não importa o que você digita no formulário, não vai funcionar ainda. Mas nós vamos chegar lá.

Claro que este não é o frontend para os usuários finais, mas é uma ótima ferramenta automática para documentar interativamente toda sua API.

Pode ser usado pelo time de frontend (que pode ser você no caso).

Pode ser usado por aplicações e sistemas third party (de terceiros).

E também pode ser usada por você mesmo, para debugar, checar e testar a mesma aplicação.

## O Fluxo da `senha`

Agora vamos voltar um pouco e entender o que é isso tudo.

O "fluxo" da `senha` é um dos caminhos ("fluxos") definidos no OAuth2, para lidar com a segurança e autenticação.

OAuth2 foi projetado para que o backend ou a API pudesse ser independente do servidor que autentica o usuário.

Mas nesse caso, a mesma aplicação **FastAPI** irá lidar com a API e a autenticação.

Então, vamos rever de um ponto de vista simplificado:

* O usuário digita o `username` e a `senha` no frontend e aperta `Enter`.
* O frontend (rodando no browser do usuário) manda o `username` e a `senha` para uma URL específica na sua API (declarada com `tokenUrl="token"`).
* A API checa aquele `username` e `senha`, e responde com um "token" (nós não implementamos nada disso ainda).
	* Um "token" é apenas uma string com algum conteúdo que nós podemos utilizar mais tarde para verificar o usuário.
	* Normalmente, um token é definido para expirar depois de um tempo.
		* Então, o usuário terá que se logar de novo depois de um tempo.
		* E se o token for roubado, o risco é menor. Não é como se fosse uma chave permanente que vai funcionar para sempre (na maioria dos casos).
	* O frontend armazena aquele token temporariamente em algum lugar.
	* O usuário clica no frontend para ir à outra seção daquele frontend do aplicativo web.
	* O frontend precisa buscar mais dados daquela API.
		* Mas precisa de autenticação para aquele endpoint em específico.
		* Então, para autenticar com nossa API, ele manda um header de `Autorização` com o valor `Bearer` mais o token.
		* Se o token contém `foobar`, o conteúdo do header de `Autorização` será: `Bearer foobar`.

## **FastAPI**'s `OAuth2PasswordBearer`

**FastAPI** fornece várias ferramentas, em diferentes níveis de abstração, para implementar esses recursos de segurança.

Neste exemplo, nós vamos usar o **OAuth2** com o fluxo de **Senha**, usando um token **Bearer**. Fazemos isso usando a classe `OAuth2PasswordBearer`.

!!! informação
	Um token "bearer" não é a única opção.

	Mas é a melhor no nosso caso.

	E talvez seja a melhor para a maioria dos casos, a não ser que você seja um especialista em OAuth2 e saiba exatamente o porquê de existir outras opções que se adequam melhor às suas necessidades.

	Nesse caso, **FastAPI** também fornece as ferramentas para construir.

Quando nós criamos uma instância da classe `OAuth2PasswordBearer`, nós passamos pelo parâmetro `tokenUrl` Esse parâmetro contém a URL que o client (o frontend rodando no browser do usuário) vai usar para mandar o `username` e `senha` para obter um token.

```Python hl_lines="6"
{!../../../docs_src/security/tutorial001.py!}
```

!!! dica
	Esse `tokenUrl="token"` se refere a uma URL relativa que nós não criamos ainda. Como é uma URL relativa, é equivalente a `./token`.

	Porque estamos usando uma URL relativa, se sua API estava localizada em `https://example.com/`, então irá referir-se à `https://example.com/token`. Mas se sua API estava localizada em `https://example.com/api/v1/`, então irá referir-se à `https://example.com/api/v1/token`.

	Usar uma URL relativa é importante para garantir que sua aplicação continue funcionando, mesmo em um uso avançado tipo [Atrás de um Proxy](../../advanced/behind-a-proxy.md){.internal-link target=_blank}.

Esse parâmetro não cria um endpoint / *path operation*, mas declara que a URL `/token` vai ser aquela que o client deve usar para obter o token. Essa informação é usada no OpenAPI, e depois na API Interativa de documentação de sistemas.

Em breve também criaremos o atual path operation.

!!! informação
	Se você é um "Pythonista" muito rigoroso, você pode não gostar do estilo do nome do parâmetro `tokenUrl` em vez de `token_url`.

	Isso ocorre porque está utilizando o mesmo nome que está nas especificações do OpenAPI. Então, se você precisa investigar mais sobre qualquer um desses esquemas de segurança, você pode simplesmente copiar e colar para encontrar mais informações sobre isso.

A variável `oauth2_scheme` é um instância de `OAuth2PasswordBearer`, mas também é um "callable".

Pode ser chamada de:

```Python
oauth2_scheme(some, parameters)
```

Então, pode ser usado com `Depends`.

## Use-o

Agora você pode passar aquele `oauth2_scheme` em uma dependência com `Depends`.

```Python hl_lines="10"
{!../../../docs_src/security/tutorial001.py!}
```

Esse dependência vai fornecer uma `str` que é atribuído ao parâmetro `token da *função do path operation*

A **FastAPI** saberá que pode usar essa dependência para definir um "esquema de segurança" no esquema da OpenAPI (e na documentação da API automática).

!!! informação "Detalhes técnicos"
	**FastAPI** saberá que pode usar a classe `OAuth2PasswordBearer` (declarada na dependência) para definir o esquema de segurança na OpenAPI porque herda de `fastapi.security.oauth2.OAuth2`, que por sua vez herda de `fastapi.security.base.Securitybase`.

	 Todos os utilitários de segurança que se integram com OpenAPI (e na documentação da API automática) herdam de `SecurityBase`, é assim que **FastAPI** pode saber como integrá-los no OpenAPI.

## O que ele faz

Ele irá e olhará na requisição para aquele header de `Autorização`, verificará se o valor é `Bearer` mais algum token, e vai retornar o token como uma `str`

Se ele não ver o header de `Autorização` ou o valor não tem um token `Bearer`, vai responder com um código de erro  401 (`UNAUTHORIZED`) diretamente.

Você nem precisa verificar se o token existe para retornar um erro. Você pode ter certeza de que se a sua função for executada, ela terá um `str` nesse token.

Você já pode experimentar na documentação interativa:

<img src="/img/tutorial/security/image03.png">

Não estamos verificando a validade do token ainda, mas isso já é um começo

## Recapitulando

Então, em apenas 3 ou 4 linhas extras, você já tem alguma forma primitiva de segurança.
