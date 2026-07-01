# Frontend { #frontend }

Você pode servir aplicações frontend estáticas com `app.frontend()` ou `router.frontend()`.

Isso é útil para ferramentas de frontend que geram arquivos estáticos, como React com Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid e outras.

Com essas ferramentas, normalmente há uma etapa que faz o build do frontend, com um comando como:

```bash
npm run build
```

Isso geraria um diretório como `./dist/` com seus arquivos de frontend.

Você pode usar `app.frontend()` para servir esse diretório seguindo as convenções necessárias por esses frameworks de frontend.

**FastAPI** verifica as *operações de rota* primeiro. Os arquivos de frontend são verificados somente se nenhuma rota normal corresponder, então sua API não será afetada.

## Sirva um Frontend { #serve-a-frontend }

Depois de fazer o build do seu frontend, por exemplo com `npm run build`, coloque os arquivos gerados em um diretório, por exemplo, `dist`.

A estrutura do seu projeto poderia ser assim:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

Então sirva-o com `app.frontend()`:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

Com isso, um request para `/assets/app.js` pode servir `dist/assets/app.js`.

Se você também tiver uma *operação de rota* do **FastAPI**, a *operação de rota* tem prioridade.

## Roteamento no Lado do Cliente { #client-side-routing }

Muitas aplicações frontend, incluindo **aplicações de página única** (SPAs), usam roteamento no lado do cliente. Um path como `/dashboard/settings` pode não ser um arquivo real, mas o framework cuidaria de lidar com ele.

Então, ao acessar essa URL diretamente (em vez de navegar pela aplicação), o backend deveria servir a aplicação frontend a partir de `index.html`, para que o framework de frontend possa então lidar com o roteamento no lado do cliente.

Para isso, use `fallback="index.html"`:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** usa esse fallback somente para requests `GET` e `HEAD` que parecem navegação do navegador. Arquivos ausentes como JavaScript, CSS e imagens ainda retornam `404`.

Requests com outros métodos, como `POST` ou `PUT`, para paths que correspondem apenas ao fallback do frontend também retornam `404`. *Operações de rota* regulares do **FastAPI** ainda têm prioridade maior que rotas de frontend.

/// tip | Dica

Por padrão, `fallback` tem o valor `fallback="auto"`. Na maioria dos casos, você não precisará especificar `fallback`. Leia abaixo para detalhes.

///

Isso é o que você desejaria com muitas aplicações frontend que usam roteamento no lado do cliente, por exemplo, React com TanStack Router, Vue, Angular, SvelteKit ou Solid.

## Página 404 Personalizada { #custom-404-page }

Você também pode servir uma página estática `404.html` para paths de frontend ausentes:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Essa response mantém um código de status `404`.

Neste caso, **FastAPI** não servirá `index.html` para paths de frontend ausentes. Ele retornará o arquivo `404.html` em vez disso.

/// tip | Dica

Por padrão, `fallback` tem o valor `fallback="auto"`. Com isso, se um arquivo `404.html` for encontrado, ele será usado automaticamente como fallback.

Então, normalmente você pode omitir o argumento `fallback`.

///

Isso é útil com ferramentas de frontend que geram arquivos HTML estáticos para cada página, como Astro.

## Fallback Automático { #fallback-auto }

Por padrão, `app.frontend()` usa `fallback="auto"`.

Se houver um arquivo `404.html` no diretório do frontend, paths de frontend ausentes servem esse arquivo com código de status `404`.

Caso contrário, se houver um arquivo `index.html`, paths de navegação do navegador ausentes servem `index.html`, que é o que muitas aplicações frontend com roteamento no lado do cliente esperam.

Então, na maioria dos casos, você pode usar `app.frontend("/", directory="dist")` sem especificar o argumento `fallback`.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Desative o Fallback { #disable-fallback }

Se você não quiser servir um arquivo de fallback para paths de frontend ausentes, use `fallback=None`:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Então paths de frontend ausentes retornam o `404` normal.

## Verifique o Diretório { #check-directory }

Por padrão, `app.frontend()` verifica se o diretório existe quando a aplicação é criada.

Isso ajuda a identificar erros de configuração cedo. Por exemplo, se o diretório de saída do build do frontend estiver ausente, **FastAPI** gerará um erro na inicialização.

Se seus arquivos de frontend forem criados depois, por exemplo por uma etapa de build separada após o objeto da aplicação ser criado, defina `check_dir=False`:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

Com `check_dir=False`, **FastAPI** não verificará o diretório quando a aplicação for criada. Se o diretório configurado ainda estiver ausente quando um request for processado, **FastAPI** gerará um erro nesse momento.

## Use com `APIRouter` { #use-it-with-apirouter }

Você também pode adicionar arquivos de frontend a um `APIRouter` e incluí-lo com um prefixo:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

Neste exemplo, os paths de frontend são servidos em `/app`.

Quaisquer *operações de rota* regulares na aplicação ainda terão precedência, inclusive em outros routers.

## Apenas Saída de Build Estático { #static-build-output-only }

`app.frontend()` serve arquivos já gerados pelo build do seu frontend.

Ele não executa renderização no lado do servidor. Ele é para frameworks de frontend que geram arquivos estáticos, não para frameworks que precisam de renderização dinâmica no servidor para cada request.
