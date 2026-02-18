# 生成 SDK { #generating-sdks }

因为 **FastAPI** 基于 **OpenAPI** 规范，它的 API 可以用许多工具都能理解的标准格式来描述。

这让你可以轻松生成最新的**文档**、多语言的客户端库（<abbr title="Software Development Kits - 软件开发工具包">**SDKs**</abbr>），以及与代码保持同步的**测试**或**自动化工作流**。

本指南将带你为 FastAPI 后端生成一个 **TypeScript SDK**。

## 开源 SDK 生成器 { #open-source-sdk-generators }

一个功能多样的选择是 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>，它支持**多种编程语言**，可以根据你的 OpenAPI 规范生成 SDK。

对于 **TypeScript 客户端**，<a href="https://heyapi.dev/" class="external-link" target="_blank">Hey API</a> 是为 TypeScript 生态打造的专用方案，提供优化的使用体验。

你还可以在 <a href="https://openapi.tools/#sdk" class="external-link" target="_blank">OpenAPI.Tools</a> 上发现更多 SDK 生成器。

/// tip | 提示

FastAPI 会自动生成 **OpenAPI 3.1** 规范，因此你使用的任何工具都必须支持该版本。

///

## 来自 FastAPI 赞助商的 SDK 生成器 { #sdk-generators-from-fastapi-sponsors }

本节介绍的是由赞助 FastAPI 的公司提供的、具备**风险投资背景**或**公司支持**的方案。这些产品在高质量生成的 SDK 之上，提供了**更多特性**和**集成**。

通过 ✨ [**赞助 FastAPI**](../help-fastapi.md#sponsor-the-author){.internal-link target=_blank} ✨，这些公司帮助确保框架及其**生态**保持健康并且**可持续**。

他们的赞助也体现了对 FastAPI **社区**（也就是你）的高度承诺，不仅关注提供**优秀的服务**，也支持一个**健壮且繁荣的框架**——FastAPI。🙇

例如，你可以尝试：

* <a href="https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship" class="external-link" target="_blank">Speakeasy</a>
* <a href="https://www.stainless.com/?utm_source=fastapi&utm_medium=referral" class="external-link" target="_blank">Stainless</a>
* <a href="https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi" class="external-link" target="_blank">liblab</a>

其中一些方案也可能是开源的或提供免费层级，你可以不花钱就先试用。其他商业 SDK 生成器也可在网上找到。🤓

## 创建一个 TypeScript SDK { #create-a-typescript-sdk }

先从一个简单的 FastAPI 应用开始：

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

请注意，这些*路径操作*使用 `Item` 和 `ResponseMessage` 模型来定义它们的请求载荷和响应载荷。

### API 文档 { #api-docs }

访问 `/docs` 时，你会看到有用于请求发送和响应接收数据的**模式**：

<img src="/img/tutorial/generate-clients/image01.png">

之所以能看到这些模式，是因为它们在应用中用模型声明了。

这些信息会包含在应用的 **OpenAPI 模式** 中，并显示在 API 文档里。

OpenAPI 中包含的这些模型信息就是用于**生成客户端代码**的基础。

### Hey API { #hey-api }

当我们有了带模型的 FastAPI 应用后，可以使用 Hey API 来生成 TypeScript 客户端。最快的方式是通过 npx：

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

这会在 `./src/client` 生成一个 TypeScript SDK。

你可以在其官网了解如何<a href="https://heyapi.dev/openapi-ts/get-started" class="external-link" target="_blank">安装 `@hey-api/openapi-ts`</a>，以及阅读<a href="https://heyapi.dev/openapi-ts/output" class="external-link" target="_blank">生成结果</a>的说明。

### 使用 SDK { #using-the-sdk }

现在你可以导入并使用客户端代码了。它可能是这样，并且你会发现方法有自动补全：

<img src="/img/tutorial/generate-clients/image02.png">

要发送的载荷也会有自动补全：

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | 提示

请注意 `name` 和 `price` 的自动补全，它们是在 FastAPI 应用中的 `Item` 模型里定义的。

///

你发送的数据如果不符合要求，会在编辑器中显示内联错误：

<img src="/img/tutorial/generate-clients/image04.png">

响应对象同样有自动补全：

<img src="/img/tutorial/generate-clients/image05.png">

## 带有标签的 FastAPI 应用 { #fastapi-app-with-tags }

很多情况下，你的 FastAPI 应用会更大，你可能会用标签来划分不同组的*路径操作*。

例如，你可以有一个 **items** 相关的部分和另一个 **users** 相关的部分，它们可以用标签来分隔：

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### 生成带标签的 TypeScript 客户端 { #generate-a-typescript-client-with-tags }

如果你为使用了标签的 FastAPI 应用生成客户端，通常也会根据标签来拆分客户端代码。

这样你就可以在客户端代码中把内容正确地组织和分组：

<img src="/img/tutorial/generate-clients/image06.png">

在这个例子中，你会有：

* `ItemsService`
* `UsersService`

### 客户端方法名 { #client-method-names }

现在，像 `createItemItemsPost` 这样的生成方法名看起来不太简洁：

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...这是因为客户端生成器会把每个*路径操作*的 OpenAPI 内部**操作 ID（operation ID）**用作方法名的一部分。

OpenAPI 要求每个操作 ID 在所有*路径操作*中都是唯一的，因此 FastAPI 会使用**函数名**、**路径**和**HTTP 方法/操作**来生成操作 ID，以确保其唯一性。

接下来我会告诉你如何改进。🤓

## 自定义操作 ID 与更好的方法名 { #custom-operation-ids-and-better-method-names }

你可以**修改**这些操作 ID 的**生成**方式，使之更简单，从而在客户端中得到**更简洁的方法名**。

在这种情况下，你需要用其他方式确保每个操作 ID 依然是**唯一**的。

例如，你可以确保每个*路径操作*都有一个标签，然后基于**标签**和*路径操作***名称**（函数名）来生成操作 ID。

### 自定义唯一 ID 生成函数 { #custom-generate-unique-id-function }

FastAPI 为每个*路径操作*使用一个**唯一 ID**，它既用于**操作 ID**，也用于请求或响应里任何需要的自定义模型名称。

你可以自定义这个函数。它接收一个 `APIRoute` 并返回一个字符串。

例如，这里使用第一个标签（你很可能只有一个标签）和*路径操作*名称（函数名）。

然后你可以把这个自定义函数通过 `generate_unique_id_function` 参数传给 **FastAPI**：

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### 使用自定义操作 ID 生成 TypeScript 客户端 { #generate-a-typescript-client-with-custom-operation-ids }

现在再次生成客户端，你会看到方法名已经改进：

<img src="/img/tutorial/generate-clients/image07.png">

如你所见，方法名现在由标签和函数名组成，不再包含 URL 路径和 HTTP 操作的信息。

### 为客户端生成器预处理 OpenAPI 规范 { #preprocess-the-openapi-specification-for-the-client-generator }

生成的代码中仍有一些**重复信息**。

我们已经知道这个方法与 **items** 有关，因为它位于 `ItemsService`（来自标签），但方法名里仍然带有标签名前缀。😕

通常我们仍然希望在 OpenAPI 中保留它，以确保操作 ID 的**唯一性**。

但对于生成的客户端，我们可以在生成之前**修改** OpenAPI 的操作 ID，只是为了让方法名更美观、更**简洁**。

我们可以把 OpenAPI JSON 下载到 `openapi.json` 文件中，然后用如下脚本**移除这个标签前缀**：

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

这样，操作 ID 会从 `items-get_items` 之类的名字重命名为 `get_items`，从而让客户端生成器生成更简洁的方法名。

### 使用预处理后的 OpenAPI 生成 TypeScript 客户端 { #generate-a-typescript-client-with-the-preprocessed-openapi }

因为最终结果现在保存在 `openapi.json` 中，你需要更新输入位置：

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

生成新客户端后，你将拥有**简洁的方法名**，并具备**自动补全**、**内联错误**等功能：

<img src="/img/tutorial/generate-clients/image08.png">

## 优点 { #benefits }

使用自动生成的客户端时，你会获得以下内容的**自动补全**：

* 方法
* 请求体中的数据、查询参数等
* 响应数据

你还会为所有内容获得**内联错误**。

每当你更新后端代码并**重新生成**前端时，新的*路径操作*会作为方法可用，旧的方法会被移除，其他任何更改都会反映到生成的代码中。🤓

这也意味着如果有任何变更，它会自动**反映**到客户端代码中。而当你**构建**客户端时，如果所用数据存在任何**不匹配**，它会直接报错。

因此，你可以在开发周期的早期就**发现许多错误**，而不必等到错误在生产环境中暴露给最终用户后再去调试问题所在。✨
