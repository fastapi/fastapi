# Obter Usuário Atual { #get-current-user }

No capítulo anterior, o sistema de segurança (que é baseado no sistema de injeção de dependências) estava fornecendo à *função de operação de rota* um `token` como uma `str`:

{* ../../docs_src/security/tutorial001_an_py39.py hl[12] *}

Mas isso ainda não é tão útil.

Vamos fazer com que ele nos forneça o usuário atual.

## Criar um modelo de usuário { #create-a-user-model }

Primeiro, vamos criar um modelo de usuário com Pydantic.

Da mesma forma que usamos o Pydantic para declarar corpos, podemos usá-lo em qualquer outro lugar:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## Criar uma dependência `get_current_user` { #create-a-get-current-user-dependency }

Vamos criar uma dependência chamada `get_current_user`.

Lembra que as dependências podem ter subdependências?

`get_current_user` terá uma dependência com o mesmo `oauth2_scheme` que criamos antes.

Da mesma forma que estávamos fazendo antes diretamente na *operação de rota*, a nossa nova dependência `get_current_user` receberá um `token` como uma `str` da subdependência `oauth2_scheme`:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## Obter o usuário { #get-the-user }

`get_current_user` usará uma função utilitária (falsa) que criamos, que recebe um token como uma `str` e retorna nosso modelo Pydantic `User`:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## Injetar o usuário atual { #inject-the-current-user }

Então agora nós podemos usar o mesmo `Depends` com nosso `get_current_user` na *operação de rota*:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

Observe que nós declaramos o tipo de `current_user` como o modelo Pydantic `User`.

Isso nos ajudará dentro da função com todo o preenchimento automático e verificações de tipo.

/// tip | Dica

Você pode se lembrar que corpos de requisição também são declarados com modelos Pydantic.

Aqui, o **FastAPI** não ficará confuso porque você está usando `Depends`.

///

/// check | Verifique

A forma como esse sistema de dependências foi projetado nos permite ter diferentes dependências (diferentes "dependables") que retornam um modelo `User`.

Não estamos restritos a ter apenas uma dependência que possa retornar esse tipo de dado.

///

## Outros modelos { #other-models }

Agora você pode obter o usuário atual diretamente nas *funções de operação de rota* e lidar com os mecanismos de segurança no nível da **Injeção de Dependências**, usando `Depends`.

E você pode usar qualquer modelo ou dado para os requisitos de segurança (neste caso, um modelo Pydantic `User`).

Mas você não está restrito a usar um modelo de dados, classe ou tipo específico.

Você quer ter apenas um `id` e `email`, sem incluir nenhum `username` no modelo? Claro. Você pode usar essas mesmas ferramentas.

Você quer ter apenas uma `str`? Ou apenas um `dict`? Ou uma instância de modelo de classe de banco de dados diretamente? Tudo funciona da mesma forma.

Na verdade, você não tem usuários que fazem login no seu aplicativo, mas sim robôs, bots ou outros sistemas, que possuem apenas um token de acesso? Novamente, tudo funciona da mesma forma.

Apenas use qualquer tipo de modelo, qualquer tipo de classe, qualquer tipo de banco de dados que você precise para a sua aplicação. O **FastAPI** cobre tudo com o sistema de injeção de dependências.

## Tamanho do código { #code-size }

Este exemplo pode parecer verboso. Lembre-se de que estamos misturando segurança, modelos de dados, funções utilitárias e *operações de rota* no mesmo arquivo.

Mas aqui está o ponto principal.

O código relacionado à segurança e à injeção de dependências é escrito apenas uma vez.

E você pode torná-lo tão complexo quanto quiser. E ainda assim, tê-lo escrito apenas uma vez, em um único lugar. Com toda a flexibilidade.

Mas você pode ter milhares de endpoints (*operações de rota*) usando o mesmo sistema de segurança.

E todos eles (ou qualquer parte deles que você desejar) podem aproveitar o reuso dessas dependências ou de quaisquer outras dependências que você criar.

E todos esses milhares de *operações de rota* podem ter apenas 3 linhas:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Recapitulação { #recap }

Agora você pode obter o usuário atual diretamente na sua *função de operação de rota*.

Já estamos na metade do caminho.

Só precisamos adicionar uma *operação de rota* para que o usuário/cliente realmente envie o `username` e `password`.

Isso vem a seguir.
