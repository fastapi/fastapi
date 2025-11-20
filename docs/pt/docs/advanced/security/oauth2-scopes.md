# Escopos OAuth2 { #oauth2-scopes }

Você pode utilizar escopos do OAuth2 diretamente com o **FastAPI**, eles são integrados para funcionar perfeitamente.

Isso permitiria que você tivesse um sistema de permissionamento mais refinado, seguindo o padrão do OAuth2 integrado na sua aplicação OpenAPI (e as documentações da API).

OAuth2 com escopos é o mecanismo utilizado por muitos provedores de autenticação, como o Facebook, Google, GitHub, Microsoft, X (Twitter), etc. Eles utilizam isso para prover permissões específicas para os usuários e aplicações.

Toda vez que você "se autentica com" Facebook, Google, GitHub, Microsoft, X (Twitter), aquela aplicação está utilizando o OAuth2 com escopos.

Nesta seção, você verá como gerenciar a autenticação e autorização com os mesmos escopos do OAuth2 em sua aplicação **FastAPI**.

/// warning | Atenção

Isso é uma seção mais ou menos avançada. Se você está apenas começando, você pode pular.

Você não necessariamente precisa de escopos do OAuth2, e você pode lidar com autenticação e autorização da maneira que você achar melhor.

Mas o OAuth2 com escopos pode ser integrado de maneira fácil em sua API (com OpenAPI) e a sua documentação de API.

No entanto, você ainda aplica estes escopos, ou qualquer outro requisito de segurança/autorização, conforme necessário, em seu código.

Em muitos casos, OAuth2 com escopos pode ser um exagero.

Mas se você sabe que precisa, ou está curioso, continue lendo.

///

## Escopos OAuth2 e OpenAPI { #oauth2-scopes-and-openapi }

A especificação OAuth2 define "escopos" como uma lista de strings separadas por espaços.

O conteúdo de cada uma dessas strings pode ter qualquer formato, mas não devem possuir espaços.

Estes escopos representam "permissões".

No OpenAPI (e.g. os documentos da API), você pode definir "esquemas de segurança".

Quando um desses esquemas de segurança utiliza OAuth2, você pode também declarar e utilizar escopos.

Cada "escopo" é apenas uma string (sem espaços).

Eles são normalmente utilizados para declarar permissões de segurança específicas, como por exemplo:

* `users:read` or `users:write` são exemplos comuns.
* `instagram_basic` é utilizado pelo Facebook / Instagram.
* `https://www.googleapis.com/auth/drive` é utilizado pelo Google.

/// info | Informação

No OAuth2, um "escopo" é apenas uma string que declara uma permissão específica necessária.

Não importa se ela contém outros caracteres como `:` ou se ela é uma URL.

Estes detalhes são específicos da implementação.

Para o OAuth2, eles são apenas strings.

///

## Visão global { #global-view }

Primeiro, vamos olhar rapidamente as partes que mudam dos exemplos do **Tutorial - Guia de Usuário** para [OAuth2 com Senha (e hash), Bearer com tokens JWT](../../tutorial/security/oauth2-jwt.md){.internal-link target=_blank}. Agora utilizando escopos OAuth2:

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,9,13,47,65,106,108:116,122:126,130:136,141,157] *}

Agora vamos revisar essas mudanças passo a passo.

## Esquema de segurança OAuth2 { #oauth2-security-scheme }

A primeira mudança é que agora nós estamos declarando o esquema de segurança OAuth2 com dois escopos disponíveis, `me` e `items`.

O parâmetro `scopes` recebe um `dict` contendo cada escopo como chave e a descrição como valor:

{* ../../docs_src/security/tutorial005_an_py310.py hl[63:66] *}

Pelo motivo de estarmos declarando estes escopos, eles aparecerão nos documentos da API quando você se autenticar/autorizar.

E você poderá selecionar quais escopos você deseja dar acesso: `me` e `items`.

Este é o mesmo mecanismo utilizado quando você adiciona permissões enquanto se autentica com o Facebook, Google, GitHub, etc:

<img src="/img/tutorial/security/image11.png">

## Token JWT com escopos { #jwt-token-with-scopes }

Agora, modifique a *operação de rota* do token para retornar os escopos solicitados.

Nós ainda estamos utilizando o mesmo `OAuth2PasswordRequestForm`. Ele inclui a propriedade `scopes` com uma `list` de `str`, com cada escopo que ele recebeu na requisição.

E nós retornamos os escopos como parte do token JWT.

/// danger | Cuidado

Para manter as coisas simples, aqui nós estamos apenas adicionando os escopos recebidos diretamente ao token.

Porém em sua aplicação, por segurança, você deve garantir que você apenas adiciona os escopos que o usuário possui permissão de fato, ou aqueles que você predefiniu.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[157] *}

## Declare escopos em *operações de rota* e dependências { #declare-scopes-in-path-operations-and-dependencies }

Agora nós declaramos que a *operação de rota* para `/users/me/items/` exige o escopo `items`.

Para isso, nós importamos e utilizamos `Security` de `fastapi`.

Você pode utilizar `Security` para declarar dependências (assim como `Depends`), porém o `Security` também recebe o parâmetro `scopes` com uma lista de escopos (strings).

Neste caso, nós passamos a função `get_current_active_user` como dependência para `Security` (da mesma forma que nós faríamos com `Depends`).

Mas nós também passamos uma `list` de escopos, neste caso com apenas um escopo: `items` (poderia ter mais).

E a função de dependência `get_current_active_user` também pode declarar subdependências, não apenas com `Depends`, mas também com `Security`. Ao declarar sua própria função de subdependência (`get_current_user`), e mais requisitos de escopo.

Neste caso, ele requer o escopo `me` (poderia requerer mais de um escopo).

/// note | Nota

Você não necessariamente precisa adicionar diferentes escopos em diferentes lugares.

Nós estamos fazendo isso aqui para demonstrar como o **FastAPI** lida com escopos declarados em diferentes níveis.

///

{* ../../docs_src/security/tutorial005_an_py310.py hl[5,141,172] *}

/// info | Detalhes Técnicos

`Security` é na verdade uma subclasse de `Depends`, e ele possui apenas um parâmetro extra que veremos depois.

Porém ao utilizar `Security` no lugar de `Depends`, o **FastAPI** saberá que ele pode declarar escopos de segurança, utilizá-los internamente, e documentar a API com o OpenAPI.

Mas quando você importa `Query`, `Path`, `Depends`, `Security` entre outros de `fastapi`, eles são na verdade funções que retornam classes especiais.

///

## Utilize `SecurityScopes` { #use-securityscopes }

Agora atualize a dependência `get_current_user`.

Este é o usado pelas dependências acima.

Aqui é onde estamos utilizando o mesmo esquema OAuth2 que nós declaramos antes, declarando-o como uma dependência: `oauth2_scheme`.

Porque esta função de dependência não possui nenhum requerimento de escopo, nós podemos utilizar `Depends` com o `oauth2_scheme`. Nós não precisamos utilizar `Security` quando nós não precisamos especificar escopos de segurança.

Nós também declaramos um parâmetro especial do tipo `SecurityScopes`, importado de `fastapi.security`.

A classe `SecurityScopes` é semelhante à classe `Request` (`Request` foi utilizada para obter o objeto da requisição diretamente).

{* ../../docs_src/security/tutorial005_an_py310.py hl[9,106] *}

## Utilize os `scopes` { #use-the-scopes }

O parâmetro `security_scopes` será do tipo `SecurityScopes`.

Ele terá a propriedade `scopes` com uma lista contendo todos os escopos requeridos por ele e todas as dependências que utilizam ele como uma subdependência. Isso significa, todos  os "dependentes"... pode soar meio confuso, e isso será explicado novamente mais adiante.

O objeto `security_scopes` (da classe `SecurityScopes`) também oferece um atributo `scope_str` com uma única string, contendo os escopos separados por espaços (nós vamos utilizar isso).

Nós criamos uma `HTTPException` que nós podemos reutilizar (`raise`) mais tarde em diversos lugares.

Nesta exceção, nós incluímos os escopos necessários (se houver algum) como uma string separada por espaços (utilizando `scope_str`). Nós colocamos esta string contendo os escopos no cabeçalho `WWW-Authenticate` (isso é parte da especificação).

{* ../../docs_src/security/tutorial005_an_py310.py hl[106,108:116] *}

## Verifique o `username` e o formato dos dados { #verify-the-username-and-data-shape }

Nós verificamos que nós obtemos um `username`, e extraímos os escopos.

E depois nós validamos esse dado com o modelo Pydantic (capturando a exceção `ValidationError`), e se nós obtemos um erro ao ler o token JWT ou validando os dados com o Pydantic, nós levantamos a exceção `HTTPException` que criamos anteriormente.

Para isso, nós atualizamos o modelo Pydantic `TokenData` com a nova propriedade `scopes`.

Ao validar os dados com o Pydantic nós podemos garantir que temos, por exemplo, exatamente uma `list` de `str` com os escopos e uma `str` com o `username`.

No lugar de, por exemplo, um `dict`, ou alguma outra coisa, que poderia quebrar a aplicação em algum lugar mais tarde, tornando isso um risco de segurança.

Nós também verificamos que nós temos um usuário com o "*username*", e caso contrário, nós levantamos a mesma exceção que criamos anteriormente.

{* ../../docs_src/security/tutorial005_an_py310.py hl[47,117:129] *}

## Verifique os `scopes` { #verify-the-scopes }

Nós verificamos agora que todos os escopos necessários, por essa dependência e todos os dependentes (incluindo as *operações de rota*) estão incluídas nos escopos fornecidos pelo token recebido, caso contrário, levantamos uma `HTTPException`.

Para isso, nós utilizamos `security_scopes.scopes`, que contém uma `list` com todos esses escopos como uma `str`.

{* ../../docs_src/security/tutorial005_an_py310.py hl[130:136] *}

## Árvore de dependência e escopos { #dependency-tree-and-scopes }

Vamos rever novamente essa árvore de dependência e os escopos.

Como a dependência `get_current_active_user` possui uma subdependência em `get_current_user`, o escopo `"me"` declarado em `get_current_active_user` será incluído na lista de escopos necessários em `security_scopes.scopes` passado para `get_current_user`.

A própria *operação de rota* também declara o escopo, `"items"`, então ele também estará na lista de `security_scopes.scopes` passado para o `get_current_user`.

Aqui está como a hierarquia de dependências e escopos parecem:

* A *operação de rota* `read_own_items` possui:
    * Escopos necessários `["items"]` com a dependência:
    * `get_current_active_user`:
        *  A função de dependência `get_current_active_user` possui:
            * Escopos necessários `["me"]` com a dependência:
            * `get_current_user`:
                * A função de dependência `get_current_user` possui:
                    * Nenhum escopo necessário.
                    * Uma dependência utilizando `oauth2_scheme`.
                    * Um parâmetro `security_scopes` do tipo `SecurityScopes`:
                        * Este parâmetro `security_scopes` possui uma propriedade `scopes` com uma `list` contendo todos estes escopos declarados acima, então:
                            * `security_scopes.scopes` terá `["me", "items"]` para a *operação de rota* `read_own_items`.
                            * `security_scopes.scopes` terá `["me"]` para a *operação de rota* `read_users_me`, porque ela declarou na dependência `get_current_active_user`.
                            * `security_scopes.scopes` terá `[]` (nada) para a *operação de rota* `read_system_status`, porque ele não declarou nenhum `Security` com `scopes`, e sua dependência, `get_current_user`, não declara nenhum `scopes` também.

/// tip | Dica

A coisa importante e "mágica" aqui é que `get_current_user` terá diferentes listas de `scopes` para validar para cada *operação de rota*.

Tudo depende dos `scopes` declarados em cada *operação de rota* e cada dependência da árvore de dependências para aquela *operação de rota* específica.

///

## Mais detalhes sobre `SecurityScopes` { #more-details-about-securityscopes }

Você pode utilizar `SecurityScopes` em qualquer lugar, e em diversos lugares. Ele não precisa estar na dependência "raiz".

Ele sempre terá os escopos de segurança declarados nas dependências atuais de `Security` e todos os dependentes para **aquela** *operação de rota* **específica** e **aquela** árvore de dependência **específica**.

Porque o `SecurityScopes` terá todos os escopos declarados por dependentes, você pode utilizá-lo para verificar se o token possui os escopos necessários em uma função de dependência central, e depois declarar diferentes requisitos de escopo em diferentes *operações de rota*.

Todos eles serão validados independentemente para cada *operação de rota*.

## Verifique { #check-it }

Se você abrir os documentos da API, você pode autenticar e especificar quais escopos você quer autorizar.

<img src="/img/tutorial/security/image11.png">

Se você não selecionar nenhum escopo, você terá "autenticado", mas quando você tentar acessar `/users/me/` ou `/users/me/items/`, você vai obter um erro dizendo que você não possui as permissões necessárias. Você ainda poderá acessar `/status/`.

E se você selecionar o escopo `me`, mas não o escopo `items`, você poderá acessar `/users/me/`, mas não `/users/me/items/`.

Isso é o que aconteceria se uma aplicação terceira que tentou acessar uma dessas *operações de rota* com um token fornecido por um usuário, dependendo de quantas permissões o usuário forneceu para a aplicação.

## Sobre integrações de terceiros { #about-third-party-integrations }

Neste exemplo nós estamos utilizando o fluxo de senha do OAuth2.

Isso é apropriado quando nós estamos autenticando em nossa própria aplicação, provavelmente com o nosso próprio "*frontend*".

Porque nós podemos confiar nele para receber o `username` e o `password`, pois nós controlamos isso.

Mas se nós estamos construindo uma aplicação OAuth2 que outros poderiam conectar (i.e., se você está construindo um provedor de autenticação equivalente ao Facebook, Google, GitHub, etc.) você deveria utilizar um dos outros fluxos.

O mais comum é o fluxo implícito.

O mais seguro é o fluxo de código, mas ele é mais complexo para implementar, pois ele necessita mais passos. Como ele é mais complexo, muitos provedores terminam sugerindo o fluxo implícito.

/// note | Nota

É comum que cada provedor de autenticação nomeie os seus fluxos de forma diferente, para torná-lo parte de sua marca.

Mas no final, eles estão implementando o mesmo padrão OAuth2.

///

O **FastAPI** inclui utilitários para todos esses fluxos de autenticação OAuth2 em `fastapi.security.oauth2`.

## `Security` em decoradores de `dependencies` { #security-in-decorator-dependencies }

Da mesma forma que você pode definir uma `list` de `Depends` no parâmetro `dependencies` do decorador (como explicado em [Dependências em decoradores de operações de rota](../../tutorial/dependencies/dependencies-in-path-operation-decorators.md){.internal-link target=_blank}), você também pode utilizar `Security` com escopos lá.
