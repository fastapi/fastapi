# Variáveis de Ambiente { #environment-variables }

/// tip | Dica

Se você já sabe o que são "variáveis de ambiente" e como usá-las, pode pular esta seção.

///

Uma variável de ambiente (também conhecida como "**env var**") é uma variável que existe **fora** do código Python, no **sistema operacional**, e pode ser lida pelo seu código Python (ou por outros programas também).

Variáveis de ambiente podem ser úteis para lidar com **configurações** do aplicativo, como parte da **instalação** do Python, etc.

## Criar e Usar Variáveis de Ambiente { #create-and-use-env-vars }

Você pode **criar** e usar variáveis de ambiente no **shell (terminal)**, sem precisar do Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Você pode criar uma variável de ambiente MY_NAME com
$ export MY_NAME="Wade Wilson"

// Então você pode usá-la com outros programas, como
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Criar uma variável de ambiente MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Usá-la com outros programas, como
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Ler Variáveis de Ambiente no Python { #read-env-vars-in-python }

Você também pode criar variáveis de ambiente **fora** do Python, no terminal (ou com qualquer outro método) e depois **lê-las no Python**.

Por exemplo, você poderia ter um arquivo `main.py` com:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip | Dica

O segundo argumento para <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> é o valor padrão a ser retornado.

Se não for fornecido, é `None` por padrão, Aqui fornecemos `"World"` como o valor padrão a ser usado.

///

Então você poderia chamar esse programa Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Aqui ainda não definimos a variável de ambiente
$ python main.py

// Como não definimos a variável de ambiente, obtemos o valor padrão

Hello World from Python

// Mas se criarmos uma variável de ambiente primeiro
$ export MY_NAME="Wade Wilson"

// E então chamar o programa novamente
$ python main.py

// Agora ele pode ler a variável de ambiente

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Aqui ainda não definimos a variável de ambiente
$ python main.py

// Como não definimos a variável de ambiente, obtemos o valor padrão

Hello World from Python

// Mas se criarmos uma variável de ambiente primeiro
$ $Env:MY_NAME = "Wade Wilson"

// E então chamar o programa novamente
$ python main.py

// Agora ele pode ler a variável de ambiente

Hello Wade Wilson from Python
```

</div>

////

Como as variáveis de ambiente podem ser definidas fora do código, mas podem ser lidas pelo código e não precisam ser armazenadas (com versão no `git`) com o restante dos arquivos, é comum usá-las para configurações ou **definições**.

Você também pode criar uma variável de ambiente apenas para uma **invocação específica do programa**, que só está disponível para aquele programa e apenas pela duração dele.

Para fazer isso, crie-a na mesma linha, antes do próprio programa:

<div class="termy">

```console
// Criar uma variável de ambiente MY_NAME para esta chamada de programa
$ MY_NAME="Wade Wilson" python main.py

// Agora ele pode ler a variável de ambiente

Hello Wade Wilson from Python

// A variável de ambiente não existe mais depois
$ python main.py

Hello World from Python
```

</div>

/// tip | Dica

Você pode ler mais sobre isso em <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Tipos e Validação { #types-and-validation }

Essas variáveis de ambiente só podem lidar com **strings de texto**, pois são externas ao Python e precisam ser compatíveis com outros programas e com o resto do sistema (e até mesmo com diferentes sistemas operacionais, como Linux, Windows, macOS).

Isso significa que **qualquer valor** lido em Python de uma variável de ambiente **será uma `str`**, e qualquer conversão para um tipo diferente ou qualquer validação precisa ser feita no código.

Você aprenderá mais sobre como usar variáveis de ambiente para lidar com **configurações do aplicativo** no [Guia do Usuário Avançado - Configurações e Variáveis de Ambiente](./advanced/settings.md){.internal-link target=_blank}.

## Variável de Ambiente `PATH` { #path-environment-variable }

Existe uma variável de ambiente **especial** chamada **`PATH`** que é usada pelos sistemas operacionais (Linux, macOS, Windows) para encontrar programas para executar.

O valor da variável `PATH` é uma longa string composta por diretórios separados por dois pontos `:` no Linux e macOS, e por ponto e vírgula `;` no Windows.

Por exemplo, a variável de ambiente `PATH` poderia ter esta aparência:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Isso significa que o sistema deve procurar programas nos diretórios:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Isso significa que o sistema deve procurar programas nos diretórios:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Quando você digita um **comando** no terminal, o sistema operacional **procura** o programa em **cada um dos diretórios** listados na variável de ambiente `PATH`.

Por exemplo, quando você digita `python` no terminal, o sistema operacional procura um programa chamado `python` no **primeiro diretório** dessa lista.

Se ele o encontrar, então ele o **usará**. Caso contrário, ele continua procurando nos **outros diretórios**.

### Instalando o Python e Atualizando o `PATH` { #installing-python-and-updating-the-path }

Durante a instalação do Python, você pode ser questionado sobre a atualização da variável de ambiente `PATH`.

//// tab | Linux, macOS

Vamos supor que você instale o Python e ele fique em um diretório `/opt/custompython/bin`.

Se você concordar em atualizar a variável de ambiente `PATH`, o instalador adicionará `/opt/custompython/bin` para a variável de ambiente `PATH`.

Poderia parecer assim:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Dessa forma, ao digitar `python` no terminal, o sistema encontrará o programa Python em `/opt/custompython/bin` (último diretório) e o utilizará.

////

//// tab | Windows

Digamos que você instala o Python e ele acaba em um diretório `C:\opt\custompython\bin`.

Se você disser sim para atualizar a variável de ambiente `PATH`, o instalador adicionará `C:\opt\custompython\bin` à variável de ambiente `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Dessa forma, quando você digitar `python` no terminal, o sistema encontrará o programa Python em `C:\opt\custompython\bin` (o último diretório) e o utilizará.

////

Então, se você digitar:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

O sistema **encontrará** o programa `python` em `/opt/custompython/bin` e o executará.

Seria aproximadamente equivalente a digitar:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

O sistema **encontrará** o programa `python` em `C:\opt\custompython\bin\python` e o executará.

Seria aproximadamente equivalente a digitar:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Essas informações serão úteis ao aprender sobre [Ambientes Virtuais](virtual-environments.md){.internal-link target=_blank}.

## Conclusão { #conclusion }

Com isso, você deve ter uma compreensão básica do que são **variáveis ​​de ambiente** e como usá-las em Python.

Você também pode ler mais sobre elas na <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia para Variáveis ​​de Ambiente</a>.

Em muitos casos, não é muito óbvio como as variáveis ​​de ambiente seriam úteis e aplicáveis ​​imediatamente. Mas elas continuam aparecendo em muitos cenários diferentes quando você está desenvolvendo, então é bom saber sobre elas.

Por exemplo, você precisará dessas informações na próxima seção, sobre [Ambientes Virtuais](virtual-environments.md).
