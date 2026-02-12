# Simples OAuth2 com senha e Bearer { #simple-oauth2-with-password-and-bearer }

Agora vamos construir a partir do capítulo anterior e adicionar as partes que faltam para ter um fluxo de segurança completo.

## Obtenha o `username` e a `password` { #get-the-username-and-password }

É utilizado o utils de segurança da **FastAPI** para obter o `username` e a `password`.

OAuth2 especifica que ao usar o "password flow" (fluxo de senha), que estamos usando, o cliente/usuário deve enviar os campos `username` e `password` como dados do formulário.

E a especificação diz que os campos devem ser nomeados assim. Portanto, `user-name` ou `email` não funcionariam.

Mas não se preocupe, você pode mostrá-lo como quiser aos usuários finais no frontend.

E seus modelos de banco de dados podem usar qualquer outro nome que você desejar.

Mas para a *operação de rota* de login, precisamos usar esses nomes para serem compatíveis com a especificação (e poder, por exemplo, usar o sistema integrado de documentação da API).

A especificação também afirma que o `username` e a `password` devem ser enviados como dados de formulário (portanto, não há JSON aqui).

### `scope` { #scope }

A especificação também diz que o cliente pode enviar outro campo de formulário "`scope`".

O nome do campo do formulário é `scope` (no singular), mas na verdade é uma longa string com "escopos" separados por espaços.

Cada “scope” é apenas uma string (sem espaços).

Normalmente são usados para declarar permissões de segurança específicas, por exemplo:

* `users:read` ou `users:write` são exemplos comuns.
* `instagram_basic` é usado pelo Facebook e Instagram.
* `https://www.googleapis.com/auth/drive` é usado pelo Google.

/// info | Informação

No OAuth2, um "scope" é apenas uma string que declara uma permissão específica necessária.

Não importa se tem outros caracteres como `:` ou se é uma URL.

Esses detalhes são específicos da implementação.

Para OAuth2 são apenas strings.

///

## Código para conseguir o `username` e a `password` { #code-to-get-the-username-and-password }

Agora vamos usar os utilitários fornecidos pelo **FastAPI** para lidar com isso.

### `OAuth2PasswordRequestForm` { #oauth2passwordrequestform }

Primeiro, importe `OAuth2PasswordRequestForm` e use-o como uma dependência com `Depends` na *operação de rota* para `/token`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[4,78] *}

`OAuth2PasswordRequestForm` é uma dependência de classe que declara um corpo de formulário com:

* O `username`.
* A `password`.
* Um campo `scope` opcional como uma string grande, composta de strings separadas por espaços.
* Um `grant_type` opcional.

/// tip | Dica

A especificação OAuth2 na verdade *requer* um campo `grant_type` com um valor fixo de `password`, mas `OAuth2PasswordRequestForm` não o impõe.

Se você precisar aplicá-lo, use `OAuth2PasswordRequestFormStrict` em vez de `OAuth2PasswordRequestForm`.

///

* Um `client_id` opcional (não precisamos dele em nosso exemplo).
* Um `client_secret` opcional (não precisamos dele em nosso exemplo).

/// info | Informação

O `OAuth2PasswordRequestForm` não é uma classe especial para **FastAPI** como é `OAuth2PasswordBearer`.

`OAuth2PasswordBearer` faz com que **FastAPI** saiba que é um esquema de segurança. Portanto, é adicionado dessa forma ao OpenAPI.

Mas `OAuth2PasswordRequestForm` é apenas uma dependência de classe que você mesmo poderia ter escrito ou poderia ter declarado os parâmetros do `Form` (formulário) diretamente.

Mas como é um caso de uso comum, ele é fornecido diretamente pelo **FastAPI**, apenas para facilitar.

///

### Use os dados do formulário { #use-the-form-data }

/// tip | Dica

A instância da classe de dependência `OAuth2PasswordRequestForm` não terá um atributo `scope` com a string longa separada por espaços, em vez disso, terá um atributo `scopes` com a lista real de strings para cada escopo enviado.

Não estamos usando `scopes` neste exemplo, mas a funcionalidade está disponível se você precisar.

///

Agora, obtenha os dados do usuário do banco de dados (falso), usando o `username` do campo do formulário.

Se não existir tal usuário, retornaremos um erro dizendo "Incorrect username or password".

Para o erro, usamos a exceção `HTTPException`:

{* ../../docs_src/security/tutorial003_an_py310.py hl[3,79:81] *}

### Confira a senha { #check-the-password }

Neste ponto temos os dados do usuário do nosso banco de dados, mas não verificamos a senha.

Vamos colocar esses dados primeiro no modelo `UserInDB` do Pydantic.

Você nunca deve salvar senhas em texto simples, portanto, usaremos o sistema de hashing de senhas (falsas).

Se as senhas não corresponderem, retornaremos o mesmo erro.

#### Hashing de senha { #password-hashing }

"Hashing" significa: converter algum conteúdo (uma senha neste caso) em uma sequência de bytes (apenas uma string) que parece algo sem sentido.

Sempre que você passa exatamente o mesmo conteúdo (exatamente a mesma senha), você obtém exatamente a mesma sequência aleatória de caracteres.

Mas você não pode converter a sequência aleatória de caracteres de volta para a senha.

##### Porque usar hashing de senha { #why-use-password-hashing }

Se o seu banco de dados for roubado, o ladrão não terá as senhas em texto simples dos seus usuários, apenas os hashes.

Assim, o ladrão não poderá tentar usar essas mesmas senhas em outro sistema (como muitos usuários usam a mesma senha em todos os lugares, isso seria perigoso).

{* ../../docs_src/security/tutorial003_an_py310.py hl[82:85] *}

#### Sobre `**user_dict` { #about-user-dict }

`UserInDB(**user_dict)` significa:

*Passe as chaves e valores de `user_dict` diretamente como argumentos de valor-chave, equivalente a:*

```Python
UserInDB(
    username = user_dict["username"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    disabled = user_dict["disabled"],
    hashed_password = user_dict["hashed_password"],
)
```

/// info | Informação

Para uma explicação mais completa de `**user_dict`, verifique [a documentação para **Extra Models**](../extra-models.md#about-user-in-dict){.internal-link target=_blank}.

///

## Retorne o token { #return-the-token }

A resposta do endpoint `token` deve ser um objeto JSON.

Deve ter um `token_type`. No nosso caso, como estamos usando tokens "Bearer", o tipo de token deve ser "`bearer`".

E deve ter um `access_token`, com uma string contendo nosso token de acesso.

Para este exemplo simples, seremos completamente inseguros e retornaremos o mesmo `username` do token.

/// tip | Dica

No próximo capítulo, você verá uma implementação realmente segura, com hash de senha e tokens <abbr title="JSON Web Tokens">JWT</abbr>.

Mas, por enquanto, vamos nos concentrar nos detalhes específicos de que precisamos.

///

{* ../../docs_src/security/tutorial003_an_py310.py hl[87] *}

/// tip | Dica

Pela especificação, você deve retornar um JSON com um `access_token` e um `token_type`, o mesmo que neste exemplo.

Isso é algo que você mesmo deve fazer em seu código e certifique-se de usar essas chaves JSON.

É quase a única coisa que você deve se lembrar de fazer corretamente, para estar em conformidade com as especificações.

De resto, **FastAPI** cuida disso para você.

///

## Atualize as dependências { #update-the-dependencies }

Agora vamos atualizar nossas dependências.

Queremos obter o `current_user` *somente* se este usuário estiver ativo.

Portanto, criamos uma dependência adicional `get_current_active_user` que por sua vez usa `get_current_user` como dependência.

Ambas as dependências retornarão apenas um erro HTTP se o usuário não existir ou se estiver inativo.

Portanto, em nosso endpoint, só obteremos um usuário se o usuário existir, tiver sido autenticado corretamente e estiver ativo:

{* ../../docs_src/security/tutorial003_an_py310.py hl[58:66,69:74,94] *}

/// info | Informação

O cabeçalho adicional `WWW-Authenticate` com valor `Bearer` que estamos retornando aqui também faz parte da especificação.

Qualquer código de status HTTP (erro) 401 "UNAUTHORIZED" também deve retornar um cabeçalho `WWW-Authenticate`.

No caso de tokens ao portador (nosso caso), o valor desse cabeçalho deve ser `Bearer`.

Na verdade, você pode pular esse cabeçalho extra e ainda funcionaria.

Mas é fornecido aqui para estar em conformidade com as especificações.

Além disso, pode haver ferramentas que esperam e usam isso (agora ou no futuro) e que podem ser úteis para você ou seus usuários, agora ou no futuro.

Esse é o benefício dos padrões...

///

## Veja em ação { #see-it-in-action }

Abra o docs interativo: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

### Autentique-se { #authenticate }

Clique no botão "Authorize".

Use as credenciais:

User: `johndoe`

Password: `secret`

<img src="/img/tutorial/security/image04.png">

Após autenticar no sistema, você verá assim:

<img src="/img/tutorial/security/image05.png">

### Obtenha seus próprios dados de usuário { #get-your-own-user-data }

Agora use a operação `GET` com o caminho `/users/me`.

Você obterá os dados do seu usuário, como:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false,
  "hashed_password": "fakehashedsecret"
}
```

<img src="/img/tutorial/security/image06.png">

Se você clicar no ícone de cadeado, sair e tentar a mesma operação novamente, receberá um erro HTTP 401 de:

```JSON
{
  "detail": "Not authenticated"
}
```

### Usuário inativo { #inactive-user }

Agora tente com um usuário inativo, autentique-se com:

User: `alice`

Password: `secret2`

E tente usar a operação `GET` com o caminho `/users/me`.

Você receberá um erro "Usuário inativo", como:

```JSON
{
  "detail": "Inactive user"
}
```

## Recapitulando { #recap }

Agora você tem as ferramentas para implementar um sistema de segurança completo baseado em `username` e `password` para sua API.

Usando essas ferramentas, você pode tornar o sistema de segurança compatível com qualquer banco de dados e com qualquer usuário ou modelo de dados.

O único detalhe que falta é que ainda não é realmente "seguro".

No próximo capítulo você verá como usar uma biblioteca de hashing de senha segura e tokens <abbr title="JSON Web Tokens">JWT</abbr>.
