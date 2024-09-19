# HTTP Basic Auth

Para os casos mais simples, você pode utilizar o HTTP Basic Auth.

No HTTP Basic Auth, a aplicação espera um cabeçalho que contém um usuário e uma senha.

Caso ela não receba, ela retorna um erro HTTP 401 "Unauthorized" (*Não Autorizado*).

E retorna um cabeçalho `WWW-Authenticate` com o valor `Basic`, e um parâmetro opcional `realm`.

Isso sinaliza ao navegador para mostrar o prompt integrado para um usuário e senha.

Então, quando você digitar o usuário e senha, o navegador os envia automaticamente no cabeçalho.

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

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="2  6  10"
{!> ../../../docs_src/security/tutorial006.py!}
```

////

Quando você tentar abrir a URL pela primeira vez (ou clicar no botão "Executar" nos documentos) o navegador vai pedir pelo seu usuário e senha:

<img src="/img/tutorial/security/image12.png">

## Verifique o usuário

Aqui está um exemplo mais completo.

Utilize uma dependência para verificar se o usuário e a senha estão corretos.

Para isso, utilize o módulo padrão do Python <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> para verificar o usuário e senha.

O `secrets.compare_digest()` necessita receber `bytes` ou `str` que possuem apenas caracteres ASCII (os em Inglês). Isso significa que não funcionaria com caracteres como o `á`, como em `Sebastián`.

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

/// tip | "Dica"

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

#### Um ataque "profissional"

Claro, os invasores não tentariam tudo isso de forma manual, eles escreveriam um programa para fazer isso, possivelmente com milhares ou milhões de testes por segundo. E obteriam apenas uma letra a mais por vez.

Mas fazendo isso, em alguns minutos ou horas os invasores teriam adivinhado o usuário e senha corretos, com a "ajuda" da nossa aplicação, apenas usando o tempo levado para responder.

#### Corrija com o `secrets.compare_digest()`

Mas em nosso código nós estamos utilizando o `secrets.compare_digest()`.

Resumindo, levará o mesmo tempo para comparar `stanleyjobsox` com `stanleyjobson` do que comparar `johndoe` com `stanleyjobson`. E o mesmo para a senha.

Deste modo, ao utilizar `secrets.compare_digest()` no código de sua aplicação, ela esterá a salvo contra toda essa gama de ataques de segurança.


### Retorne o erro

Depois de detectar que as credenciais estão incorretas, retorne um `HTTPException` com o status 401 (o mesmo retornado quando nenhuma credencial foi informada) e adicione o cabeçalho `WWW-Authenticate` para fazer com que o navegador mostre o prompt de login novamente:

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

/// tip | "Dica"

Prefira utilizar a versão `Annotated` se possível.

///

```Python hl_lines="23-27"
{!> ../../../docs_src/security/tutorial007.py!}
```

////
