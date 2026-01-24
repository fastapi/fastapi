# 生成 SDKs { #generating-sdks }

因为 **FastAPI** 基于 **OpenAPI** 规范，它的 API 可以用一种许多工具都能理解的标准格式来描述。

这使得你可以轻松生成最新的**文档**、多语言的客户端库（<abbr title="Software Development Kits">**SDKs**</abbr>），以及与代码保持同步的**测试**或**自动化工作流**。

在本指南中，你将学习如何为你的 FastAPI 后端生成一个 **TypeScript SDK**。

## 开源 SDK 生成器 { #open-source-sdk-generators }

一个通用的选项是 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>，它支持**多种编程语言**，并且可以根据你的 OpenAPI 规范生成 SDK。

对于 **TypeScript 客户端**，<a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> 是一个专门为 TypeScript 生态打造的解决方案，能提供更优化的体验。

你还可以在 <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a> 上发现更多 SDK 生成器。

/// tip | 提示

FastAPI 会自动生成 **OpenAPI 3.1** 规范，所以你使用的任何工具都必须支持这个版本。

///

## FastAPI 赞助商提供的 SDK 生成器 { #sdk-generators-from-fastapi-sponsors }

本节重点介绍由赞助 FastAPI 的公司提供的**风险投资支持**或**公司支持**的解决方案。这些产品会在高质量生成的 SDK 之上，提供**额外功能**与**集成**。

通过 ✨ [**赞助 FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨，这些公司帮助确保框架及其**生态系统**保持健康并且**可持续**。

他们的赞助也体现了对 FastAPI **社区**（你）的坚定承诺，表明他们不仅在意提供**优质服务**，也在支持一个**强大且繁荣的框架**——FastAPI。 🙇

例如，你可能会想试试：

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

其中一些解决方案也可能是开源的或提供免费层级，因此你可以在不做财务承诺的情况下试用它们。也有其他商业 SDK 生成器可用，并且可以在网上找到。 🤓

## 创建 TypeScript SDK { #create-a-typescript-sdk }

让我们从一个简单的 FastAPI 应用开始：

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

请注意，*路径操作* 使用 `Item` 和 `ResponseMessage` 这两个模型，来定义它们用于请求载荷和响应载荷的模型。

### API 文档 { #api-docs }

如果你访问 `/docs`，你会看到它有用于在请求中发送和在响应中接收数据的 **schemas**：

<img src="/img/tutorial/generate-clients/image01.png">

你可以看到这些 schema，因为它们是在应用中用模型声明的。

这些信息在应用的 **OpenAPI schema** 中可用，然后显示在 API 文档中。

OpenAPI 中包含的、来自模型的这些信息，就可以用来**生成客户端代码**。

### Hey API { #hey-api }

一旦我们有了带模型的 FastAPI 应用，就可以使用 Hey API 来生成 TypeScript 客户端。最快的方式是通过 npx。

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

这会在 `./src/client` 中生成一个 TypeScript SDK。

你可以在他们的网站上了解如何 <a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">安装 `@hey-api/openapi-ts`</a>，以及阅读关于<a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">生成输出</a>的说明。

### 使用 SDK { #using-the-sdk }

现在你可以导入并使用客户端代码。它可能看起来像这样，请注意你会获得方法的自动补全：

<img src="/img/tutorial/generate-clients/image02.png">

你也会对要发送的载荷获得自动补全：

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | 提示

注意 `name` 和 `price` 的自动补全，它是在 FastAPI 应用的 `Item` 模型中定义的。

///

对于你发送的数据，你会看到行内错误提示：

<img src="/img/tutorial/generate-clients/image04.png">

响应对象也会有自动补全：

<img src="/img/tutorial/generate-clients/image05.png">

## 带标签的 FastAPI 应用 { #fastapi-app-with-tags }

在很多情况下，你的 FastAPI 应用会更大，你可能会用标签来分隔不同组的*路径操作*。

例如，你可以有一个 **items** 的部分和另一个 **users** 的部分，并且它们可以用标签来分隔：

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### 生成带标签的 TypeScript 客户端 { #generate-a-typescript-client-with-tags }

如果你为使用标签的 FastAPI 应用生成客户端，它通常也会基于标签来拆分客户端代码。

这样你就能让客户端代码中的内容被正确地排序和分组：

<img src="/img/tutorial/generate-clients/image06.png">

在这个例子中，你有：

* `ItemsService`
* `UsersService`

### 客户端方法名 { #client-method-names }

现在，生成的方法名像 `createItemItemsPost` 看起来并不太简洁：

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...这是因为客户端生成器为每个*路径操作*使用 OpenAPI 内部的 **operation ID**。

OpenAPI 要求每个 operation ID 在所有*路径操作*中都是唯一的，因此 FastAPI 使用**函数名**、**路径**和**HTTP 方法/操作**来生成该 operation ID，因为这样能确保 operation ID 唯一。

但接下来我会告诉你如何改进。 🤓

## 自定义 Operation ID 和更好的方法名 { #custom-operation-ids-and-better-method-names }

你可以**修改**这些 operation ID 的**生成**方式，让它们更简单，并让客户端里有**更简单的方法名**。

在这种情况下，你必须用其他方式确保每个 operation ID 是**唯一**的。

例如，你可以确保每个*路径操作*都有一个标签，然后基于**标签**和*路径操作***名称**（函数名）来生成 operation ID。

### 自定义生成唯一 ID 的函数 { #custom-generate-unique-id-function }

FastAPI 为每个*路径操作*使用一个**唯一 ID**，它用于 **operation ID**，也用于请求或响应中任何所需自定义模型的名称。

你可以自定义该函数。它接收一个 `APIRoute` 并输出一个字符串。

例如，下面这个示例使用第一个标签（你可能只有一个标签）和*路径操作*名称（函数名）。

然后你可以将这个自定义函数作为 `generate_unique_id_function` 参数传递给 **FastAPI**：

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### 使用自定义 Operation ID 生成 TypeScript 客户端 { #generate-a-typescript-client-with-custom-operation-ids }

现在，如果你再次生成客户端，你会看到它具有改进的方法名：

<img src="/img/tutorial/generate-clients/image07.png">

如你所见，现在方法名包含标签以及函数名，不再包含 URL 路径和 HTTP 操作的信息。

### 为客户端生成器预处理 OpenAPI 规范 { #preprocess-the-openapi-specification-for-the-client-generator }

生成的代码仍然有一些**重复的信息**。

我们已经知道这个方法与 **items** 相关，因为该词在 `ItemsService` 中（来自标签），但方法名中仍然还带着标签名作为前缀。😕

对于 OpenAPI 总体来说，我们可能仍希望保留它，因为它能确保 operation ID **唯一**。

但对于生成的客户端，我们可以在生成客户端之前**修改** OpenAPI operation ID，只是为了让方法名更好看、更**干净**。

我们可以把 OpenAPI JSON 下载到一个 `openapi.json` 文件中，然后用这样的脚本**移除这个带前缀的标签**：

{* ../../docs_src/generate_clients/tutorial004_py39.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

这样，operation ID 会从类似 `items-get_items` 重命名为 `get_items`，从而让客户端生成器能生成更简单的方法名。

### 使用预处理后的 OpenAPI 生成 TypeScript 客户端 { #generate-a-typescript-client-with-the-preprocessed-openapi }

由于最终结果现在在一个 `openapi.json` 文件中，你需要更新你的输入位置：

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

生成新的客户端之后，你现在会有**干净的方法名**，以及所有的**自动补全**、**行内错误**等：

<img src="/img/tutorial/generate-clients/image08.png">

## 优点 { #benefits }

使用自动生成的客户端时，你将获得以下内容的**自动补全**：

* 方法。
* body 中的请求载荷、查询参数等。
* 响应载荷。

你还会对所有内容获得**行内错误**提示。

并且每当你更新后端代码并**重新生成**前端时，任何新的*路径操作*都会作为方法可用，旧的方法会被移除，任何其他更改也会反映到生成的代码中。 🤓

这也意味着如果有任何改动，它会自动**反映**在客户端代码中。如果你**构建**客户端，当使用的数据存在**不匹配**时，它就会报错。

因此，你会在开发周期非常早期就**检测到很多错误**，而不必等到错误在生产环境中暴露给最终用户，然后再去尝试调试问题所在。 ✨
