# HTTP Basic Auth

Para os casos mais simples, você pode utilizar o HTTP Basic Auth.

No HTTP Basic Auth, a aplicação espera um cabeçalho que contém um usuário e uma senha.

Caso ele não receba, ele retorna um erro HTTP 401 "Unauthorized".

E retorna um header `WWW-Authenticate` com o valor `Basic`, e um parâmetro opcional `realm`.

Isso sinaliza ao navegador para mostrar o prompt integrado para um usuário e senha.

Então, quando você digitar o usuário e senha, o navegador os envia automaticamente no cabeçalho.ly.

## HTTP Basic Auth Simples

* Importe `HTTPBasic` e `HTTPBasicCredentials`.
* Crie um "esquema `security`" utilizando `HTTPBasic`.
* Utilize o `security` com uma dependência em sua *operação de rota*.
* Isso retorna um objeto do tipo `HTTPBasicCredentials`:
    * Isto contém o `username` e o `password` enviado.

//// tab | Python 3.9+

```Python hl_lines="4  8  12"
{!> ../../../docs_src/security/tutorial006_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="2  7  11"
{!> ../../../docs_src/security/tutorial006_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="2  6  10"
{!> ../../../docs_src/security/tutorial006.py!}
```

////

Quando você tenta abrir a URL pela primeira vez (ou clicar o botão "Executar" nos documentos) o navegador vai pedir pelo seu usuário e senha:

<img src="/img/tutorial/security/image12.png">

## Verifique o usuário

Aqui está um exemplo mais completo.

Utilize uma dependência para verificar se o usuário e a senha estão corretos.

Para isso, utilize o módulo padrão do Python <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> para verificar o usuário e senha.

`secrets.compare_digest()` necessita receber `bytes` ou `str` que possuem apenas caracteres ASCII (os em Inglês), that only contains ASCII characters (the ones in English). Isso significa que não funcionaria com caracteres como o `á`, como em `Sebastián`.

Para lidar com isso, primeiramente nós convertemos o `username` e o `password` para `bytes`, codificando-os com UTF-8.

Então nós podemos utilizar o `secrets.compare_digest()` para garantir que o `credentials.username` é `"stanleyjobson"`, e que o `credentials.password` é `"swordfish"`.

//// tab | Python 3.9+

```Python hl_lines="1  12-24"
{!> ../../../docs_src/security/tutorial007_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  12-24"
{!> ../../../docs_src/security/tutorial007_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="1  11-21"
{!> ../../../docs_src/security/tutorial007.py!}
```

////

Isso seria parecido com:

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

Porém ao utilizar o `secrets.compare_digest()`, isso estará seguro contra um tipo de ataque chamado "ataque de temporização (timing attacks)".

### Ataques de Temporização

Mas o que é um "ataque de temporização"?

Vamos imaginar que alguns invasores estão tentando adivinhar o usuário e a senha.

E eles enviam uma requisição com um usuário `johndoe` e uma senha `love123`.

Então o código Python em sua aplicação seria equivalente a algo como:

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Mas no exato momento que o Python compara o primeiro `j` em `johndoe` contra o primeiro `s` em `stanleyjobson`, ele retornará `False`, porque ele já sabe que aquelas duas strings não são a mesma, pensando que "não existe a necessidade de desperdiçar mais poder computacional comparando o resto das letras". E a sua aplicação dirá "Usuário ou senha incorretos".

Mas então os invasores vão tentar com o usuário `stanleyjobsox` e a senha `love123`.

E a sua aplicação faz algo como:

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

O Python terá que comparar todo o `stanleyjobso` tanto em `stanleyjobsox` como em `stanleyjobson` antes de perceber que as strings não são a mesma. Então isso levará alguns microsegundos a mais para retornar "Usuário ou senha incorretos".

#### O tempo para responder ajuda os invasores

Neste ponto, ao perceber que o servidor demorou alguns microsegundos a mais para enviar o retorno "Usuário ou senha incorretos", os invasores irão saber que eles acertaram _alguma coisa_, algumas das letras iniciais estavam certas.

E eles podem tentar de novo sabendo que provavelmente é algo mais parecido com `stanleyjobsox` do que com `johndoe`.

#### A "professional" attack

Of course, the attackers would not try all this by hand, they would write a program to do it, possibly with thousands or millions of tests per second. And would get just one extra correct letter at a time.

But doing that, in some minutes or hours the attackers would have guessed the correct username and password, with the "help" of our application, just using the time taken to answer.

#### Fix it with `secrets.compare_digest()`

But in our code we are actually using `secrets.compare_digest()`.

In short, it will take the same time to compare `stanleyjobsox` to `stanleyjobson` than it takes to compare `johndoe` to `stanleyjobson`. And the same for the password.

That way, using `secrets.compare_digest()` in your application code, it will be safe against this whole range of security attacks.

### Return the error

After detecting that the credentials are incorrect, return an `HTTPException` with a status code 401 (the same returned when no credentials are provided) and add the header `WWW-Authenticate` to make the browser show the login prompt again:

//// tab | Python 3.9+

```Python hl_lines="26-30"
{!> ../../../docs_src/security/tutorial007_an_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="26-30"
{!> ../../../docs_src/security/tutorial007_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="23-27"
{!> ../../../docs_src/security/tutorial007.py!}
```

////
