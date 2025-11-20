# OAuth2 com Senha (e hashing), Bearer com tokens JWT { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

Agora que temos todo o fluxo de segurança, vamos tornar a aplicação realmente segura, usando tokens <abbr title="JSON Web Tokens">JWT</abbr> e hashing de senhas seguras.

Este código é algo que você pode realmente usar na sua aplicação, salvar os hashes das senhas no seu banco de dados, etc.

Vamos começar de onde paramos no capítulo anterior e incrementá-lo.

## Sobre o JWT { #about-jwt }

JWT significa "JSON Web Tokens".

É um padrão para codificar um objeto JSON em uma string longa e densa sem espaços. Ele se parece com isso:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Ele não é criptografado, então qualquer pessoa pode recuperar as informações do seu conteúdo.

Mas ele é assinado. Assim, quando você recebe um token que você emitiu, você pode verificar que foi realmente você quem o emitiu.

Dessa forma, você pode criar um token com um prazo de expiração, digamos, de 1 semana. E então, quando o usuário voltar no dia seguinte com o token, você sabe que ele ainda está logado no seu sistema.

Depois de uma semana, o token expirará e o usuário não estará autorizado, precisando fazer login novamente para obter um novo token. E se o usuário (ou uma terceira parte) tentar modificar o token para alterar a expiração, você seria capaz de descobrir isso, pois as assinaturas não iriam corresponder.

Se você quiser brincar com tokens JWT e ver como eles funcionam, visite <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a>.

## Instalar `PyJWT` { #install-pyjwt }

Nós precisamos instalar o `PyJWT` para criar e verificar os tokens JWT em Python.

Certifique-se de criar um [ambiente virtual](../../virtual-environments.md){.internal-link target=_blank}, ativá-lo e então instalar o `pyjwt`:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | Informação

Se você pretente utilizar algoritmos de assinatura digital como o RSA ou o ECDSA, você deve instalar a dependência da biblioteca de criptografia `pyjwt[crypto]`.

Você pode ler mais sobre isso na <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">documentação de instalação do PyJWT</a>.

///

## Hashing de senhas { #password-hashing }

"Hashing" significa converter algum conteúdo (uma senha neste caso) em uma sequência de bytes (apenas uma string) que parece um monte de caracteres sem sentido.

Sempre que você passar exatamente o mesmo conteúdo (exatamente a mesma senha), você obterá exatamente o mesmo resultado.

Mas não é possível converter os caracteres sem sentido de volta para a senha original.

### Por que usar hashing de senhas { #why-use-password-hashing }

Se o seu banco de dados for roubado, o invasor não terá as senhas em texto puro dos seus usuários, apenas os hashes.

Então, o invasor não poderá tentar usar essas senhas em outro sistema (como muitos usuários utilizam a mesma senha em vários lugares, isso seria perigoso).

## Instalar o `pwdlib` { #install-pwdlib }

pwdlib é um excelente pacote Python para lidar com hashes de senhas.

Ele suporta muitos algoritmos de hashing seguros e utilitários para trabalhar com eles.

O algoritmo recomendado é o "Argon2".

Certifique-se de criar um [ambiente virtual](../../virtual-environments.md){.internal-link target=_blank}, ativá-lo e então instalar o pwdlib com Argon2:

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | Dica

Com o `pwdlib`, você poderia até configurá-lo para ser capaz de ler senhas criadas pelo **Django**, um plug-in de segurança do **Flask** ou muitos outros.

Assim, você poderia, por exemplo, compartilhar os mesmos dados de um aplicativo Django em um banco de dados com um aplicativo FastAPI. Ou migrar gradualmente uma aplicação Django usando o mesmo banco de dados.

E seus usuários poderiam fazer login tanto pela sua aplicação Django quanto pela sua aplicação **FastAPI**, ao mesmo tempo.

///

## Criar o hash e verificar as senhas { #hash-and-verify-the-passwords }

Importe as ferramentas que nós precisamos de `pwdlib`.

Crie uma instância de PasswordHash com as configurações recomendadas – ela será usada para criar o hash e verificar as senhas.

/// tip | Dica

pwdlib também oferece suporte ao algoritmo de hashing bcrypt, mas não inclui algoritmos legados – para trabalhar com hashes antigos, é recomendado usar a biblioteca passlib.

Por exemplo, você poderia usá-lo para ler e verificar senhas geradas por outro sistema (como Django), mas criar o hash de novas senhas com um algoritmo diferente, como o Argon2 ou o Bcrypt.

E ser compatível com todos eles ao mesmo tempo.

///

Crie uma função utilitária para criar o hash de uma senha fornecida pelo usuário.

E outra função utilitária para verificar se uma senha recebida corresponde ao hash armazenado.

E outra para autenticar e retornar um usuário.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,56:57,60:61,70:76] *}

/// note | Nota

Se você verificar o novo banco de dados (falso) `fake_users_db`, você verá como o hash da senha se parece agora: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## Manipular tokens JWT { #handle-jwt-tokens }

Importe os módulos instalados.

Crie uma chave secreta aleatória que será usada para assinar os tokens JWT.

Para gerar uma chave secreta aleatória e segura, use o comando:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

E copie a saída para a variável `SECRET_KEY` (não use a do exemplo).

Crie uma variável `ALGORITHM` com o algoritmo usado para assinar o token JWT e defina como `"HS256"`.

Crie uma variável para a expiração do token.

Defina um modelo Pydantic que será usado no endpoint de token para a resposta.

Crie uma função utilitária para gerar um novo token de acesso.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,79:87] *}

## Atualize as dependências { #update-the-dependencies }

Atualize `get_current_user` para receber o mesmo token de antes, mas desta vez, usando tokens JWT.

Decodifique o token recebido, verifique-o e retorne o usuário atual.

Se o token for inválido, retorne um erro HTTP imediatamente.

{* ../../docs_src/security/tutorial004_an_py310.py hl[90:107] *}

## Atualize a *operação de rota* `/token` { #update-the-token-path-operation }

Crie um `timedelta` com o tempo de expiração do token.

Crie um token de acesso JWT real e o retorne.

{* ../../docs_src/security/tutorial004_an_py310.py hl[118:133] *}

### Detalhes técnicos sobre o "sujeito" `sub` do JWT { #technical-details-about-the-jwt-subject-sub }

A especificação JWT diz que existe uma chave `sub`, com o sujeito do token.

É opcional usá-la, mas é onde você colocaria a identificação do usuário, então nós estamos usando aqui.

O JWT pode ser usado para outras coisas além de identificar um usuário e permitir que ele execute operações diretamente na sua API.

Por exemplo, você poderia identificar um "carro" ou uma "postagem de blog".

Depois, você poderia adicionar permissões sobre essa entidade, como "dirigir" (para o carro) ou "editar" (para o blog).

E então, poderia dar esse token JWT para um usuário (ou bot), e ele poderia usá-lo para realizar essas ações (dirigir o carro ou editar o blog) sem sequer precisar ter uma conta, apenas com o token JWT que sua API gerou para isso.

Usando essas ideias, o JWT pode ser usado para cenários muito mais sofisticados.

Nesses casos, várias dessas entidades poderiam ter o mesmo ID, digamos `foo` (um usuário `foo`, um carro `foo` e uma postagem de blog `foo`).

Então, para evitar colisões de ID, ao criar o token JWT para o usuário, você poderia prefixar o valor da chave `sub`, por exemplo, com `username:`. Assim, neste exemplo, o valor de `sub` poderia ser: `username:johndoe`.

O importante a se lembrar é que a chave `sub` deve ter um identificador único em toda a aplicação e deve ser uma string.

## Verifique { #check-it }

Execute o servidor e vá para a documentação: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Você verá a interface de usuário assim:

<img src="/img/tutorial/security/image07.png">

Autorize a aplicação da mesma maneira que antes.

Usando as credenciais:

Username: `johndoe`
Password: `secret`

/// check | Verifique

Observe que em nenhuma parte do código está a senha em texto puro "`secret`", nós temos apenas o hash.

///

<img src="/img/tutorial/security/image08.png">

Chame o endpoint `/users/me/`, você receberá o retorno como:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Se você abrir as ferramentas de desenvolvedor, poderá ver que os dados enviados incluem apenas o token. A senha é enviada apenas na primeira requisição para autenticar o usuário e obter o token de acesso, mas não é enviada nas próximas requisições:

<img src="/img/tutorial/security/image10.png">

/// note | Nota

Perceba que o cabeçalho `Authorization`, com o valor que começa com `Bearer `.

///

## Uso avançado com `scopes` { #advanced-usage-with-scopes }

O OAuth2 tem a noção de "scopes" (escopos).

Você pode usá-los para adicionar um conjunto específico de permissões a um token JWT.

Então, você pode dar este token diretamente a um usuário ou a uma terceira parte para interagir com sua API com um conjunto de restrições.

Você pode aprender como usá-los e como eles são integrados ao **FastAPI** mais adiante no **Guia Avançado do Usuário**.

## Recapitulação { #recap }

Com o que você viu até agora, você pode configurar uma aplicação **FastAPI** segura usando padrões como OAuth2 e JWT.

Em quase qualquer framework, lidar com a segurança se torna rapidamente um assunto bastante complexo.

Muitos pacotes que simplificam bastante isso precisam fazer muitas concessões com o modelo de dados, o banco de dados e os recursos disponíveis. E alguns desses pacotes que simplificam demais na verdade têm falhas de segurança subjacentes.

---

O **FastAPI** não faz nenhuma concessão com nenhum banco de dados, modelo de dados ou ferramenta.

Ele oferece toda a flexibilidade para você escolher as opções que melhor se ajustam ao seu projeto.

E você pode usar diretamente muitos pacotes bem mantidos e amplamente utilizados, como `pwdlib` e `PyJWT`, porque o **FastAPI** não exige mecanismos complexos para integrar pacotes externos.

Mas ele fornece as ferramentas para simplificar o processo o máximo possível, sem comprometer a flexibilidade, robustez ou segurança.

E você pode usar e implementar protocolos padrão seguros, como o OAuth2, de uma maneira relativamente simples.

Você pode aprender mais no **Guia Avançado do Usuário** sobre como usar os "scopes" do OAuth2 para um sistema de permissões mais refinado, seguindo esses mesmos padrões. O OAuth2 com scopes é o mecanismo usado por muitos provedores grandes de autenticação, como o Facebook, Google, GitHub, Microsoft, X (Twitter), etc. para autorizar aplicativos de terceiros a interagir com suas APIs em nome de seus usuários.
