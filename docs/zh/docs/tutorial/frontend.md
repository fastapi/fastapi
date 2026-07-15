# 前端 { #frontend }

你可以使用 `app.frontend()`（或 `router.frontend()`）来提供静态前端应用。

这对会生成静态文件的前端工具很有用，例如使用 Vite 的 React、TanStack Router、Astro、Vue、Svelte、Angular、Solid 等。

使用这些工具时，通常会有一个构建前端的步骤，命令类似：

```bash
npm run build
```

它会生成一个类似 `./dist/` 的目录，里面包含你的前端文件。

你可以使用 `app.frontend()` 按照这些前端框架所需的约定来提供该目录。

**FastAPI** 会先检查*路径操作*。只有在没有普通路由匹配时，才会检查前端文件，因此你的 API 不会受到影响。

## 提供前端服务 { #serve-a-frontend }

构建前端之后，例如使用 `npm run build`，将生成的文件放入一个目录，例如 `dist`。

你的项目结构可能如下所示：

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

然后使用 `app.frontend()` 提供服务：

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

这样，对 `/assets/app.js` 的请求可以提供 `dist/assets/app.js`。

如果你还有一个 **FastAPI** *路径操作*，则*路径操作*优先。

## 客户端路由 { #client-side-routing }

许多前端应用，包括**单页应用**（SPA），都会使用客户端路由。像 `/dashboard/settings` 这样的路径可能并不是一个真实文件，而是由框架负责处理。

因此，如果直接访问该 URL（而不是通过应用内导航访问），后端应该从 `index.html` 提供前端应用，这样前端框架就可以处理客户端路由。

为此，使用 `fallback="index.html"`：

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** 只会对看起来像浏览器导航的 `GET` 和 `HEAD` 请求使用此 fallback。缺失的 JavaScript、CSS 和图片等文件仍会返回 `404`。

对于其他方法的请求，例如 `POST` 或 `PUT`，如果路径只匹配前端 fallback，也会返回 `404`。常规 **FastAPI** *路径操作*仍然比前端路由具有更高优先级。

/// tip | 提示

默认情况下，`fallback` 的值为 `fallback="auto"`。在大多数情况下，你不需要指定 `fallback`。详情见下文。

///

这正是许多使用客户端路由的前端应用所需的行为，例如使用 TanStack Router 的 React、Vue、Angular、SvelteKit 或 Solid。

## 自定义 404 页面 { #custom-404-page }

你也可以为缺失的前端路径提供一个静态 `404.html` 页面：

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

该响应会保持 `404` 状态码。

在这种情况下，**FastAPI** 不会为缺失的前端路径提供 `index.html`，而是返回 `404.html` 文件。

/// tip | 提示

默认情况下，`fallback` 的值为 `fallback="auto"`。这样，如果找到 `404.html` 文件，它会自动用作 fallback。

因此，通常你可以省略 `fallback` 参数。

///

这对会为每个页面生成静态 HTML 文件的前端工具很有用，例如 Astro。

## 自动 Fallback { #fallback-auto }

默认情况下，`app.frontend()` 使用 `fallback="auto"`。

如果前端目录中存在 `404.html` 文件，缺失的前端路径会以状态码 `404` 提供该文件。

否则，如果存在 `index.html` 文件，缺失的浏览器导航路径会提供 `index.html`，这正是许多使用客户端路由的前端应用所期望的行为。

因此，在大多数情况下，你可以使用 `app.frontend("/", directory="dist")`，而无需指定 `fallback` 参数。

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## 禁用 Fallback { #disable-fallback }

如果你不想为缺失的前端路径提供 fallback 文件，请使用 `fallback=None`：

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

这样，缺失的前端路径会返回普通的 `404`。

## 检查目录 { #check-directory }

默认情况下，`app.frontend()` 会在应用创建时检查目录是否存在。

这有助于尽早发现配置错误。例如，如果前端构建输出目录缺失，**FastAPI** 会在启动时抛出错误。

如果你的前端文件会稍后创建，例如在应用对象创建之后由单独的构建步骤创建，请设置 `check_dir=False`：

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

使用 `check_dir=False` 时，**FastAPI** 不会在应用创建时检查目录。如果在处理请求时配置的目录仍然缺失，**FastAPI** 会在那时抛出错误。

## 与 `APIRouter` 一起使用 { #use-it-with-apirouter }

你也可以将前端文件添加到一个 `APIRouter`，并使用前缀包含它：

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

在这个示例中，前端路径会在 `/app` 下提供服务。

应用中的任何常规*路径操作*仍会优先，包括其他 router 中的路径操作。

## 依赖项和中间件 { #dependencies-and-middleware }

前端响应在普通 **FastAPI** 应用内部运行，因此 HTTP 中间件会应用于它们。

来自 app、`APIRouter` 和 `include_router()` 的依赖项也会应用于前端响应。这可用于通过 cookie 身份验证或类似方式保护前端。

## 仅限静态构建输出 { #static-build-output-only }

`app.frontend()` 提供的是你的前端构建已经生成的文件。

它不会运行服务端渲染。它适用于生成静态文件的前端框架，而不适用于需要在服务器上为每个请求进行动态渲染的框架。
