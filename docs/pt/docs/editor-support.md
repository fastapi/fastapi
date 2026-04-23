# Suporte a Editores { #editor-support }

A [FastAPI Extension](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) oficial melhora seu fluxo de trabalho de desenvolvimento com descoberta e navegação de *operação de rota*, além de implantação no FastAPI Cloud e transmissão ao vivo de logs.

Para mais detalhes sobre a extensão, consulte o README no [repositório do GitHub](https://github.com/fastapi/fastapi-vscode).

## Configuração e Instalação { #setup-and-installation }

A **FastAPI Extension** está disponível para [VS Code](https://code.visualstudio.com/) e [Cursor](https://www.cursor.com/). Pode ser instalada diretamente pelo painel de Extensões de cada editor, pesquisando por "FastAPI" e selecionando a extensão publicada por **FastAPI Labs**. A extensão também funciona em editores no navegador, como [vscode.dev](https://vscode.dev) e [github.dev](https://github.dev).

### Descoberta da Aplicação { #application-discovery }

Por padrão, a extensão descobre automaticamente aplicações FastAPI no seu workspace procurando por arquivos que instanciam `FastAPI()`. Se a detecção automática não funcionar para a estrutura do seu projeto, você pode especificar um ponto de entrada via `[tool.fastapi]` em `pyproject.toml` ou pela configuração `fastapi.entryPoint` do VS Code usando notação de módulo (por exemplo, `myapp.main:app`).

## Funcionalidades { #features }

- **Explorador de Operações de Rota** - Uma visualização em árvore na barra lateral de todas as <dfn title="rotas, endpoints">*operações de rota*</dfn> da sua aplicação. Clique para ir diretamente a qualquer definição de rota ou de router.
- **Pesquisa de Rotas** - Pesquise por path, método ou nome com <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd> (no macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>E</kbd>).
- **Navegação com CodeLens** - Links clicáveis acima das chamadas do cliente de testes (por exemplo, `client.get('/items')`) que levam à *operação de rota* correspondente, facilitando a navegação entre testes e implementação.
- **Implantar no FastAPI Cloud** - Implantação com um clique da sua aplicação no [FastAPI Cloud](https://fastapicloud.com/).
- **Transmitir logs da aplicação** - Transmissão em tempo real dos logs da aplicação implantada no FastAPI Cloud, com filtragem por nível e busca de texto.

Se quiser se familiarizar com as funcionalidades da extensão, você pode abrir o walkthrough da extensão acessando a Paleta de Comandos (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> ou no macOS: <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>), selecionando "Welcome: Open walkthrough..." e, em seguida, escolhendo o walkthrough "Get started with FastAPI".
