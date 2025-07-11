# 生成客户端

因为 **FastAPI** 是基于OpenAPI规范的，自然您可以使用许多相匹配的工具，包括自动生成API文档 (由 Swagger UI 提供)。

一个不太明显而又特别的优势是，你可以为你的API针对不同的**编程语言**来**生成客户端**(有时候被叫做 <abbr title="Software Development Kits">**SDKs**</abbr> )。

## OpenAPI 客户端生成

有许多工具可以从**OpenAPI**生成客户端。

一个常见的工具是 <a href="https://openapi-generator.tech/" class="external-link" target="_blank">OpenAPI Generator</a>。

如果您正在开发**前端**，一个非常有趣的替代方案是 <a href="https://github.com/hey-api/openapi-ts" class="external-link" target="_blank">openapi-ts</a>。

## 生成一个 TypeScript 前端客户端

让我们从一个简单的 FastAPI 应用开始：

{* ../../docs_src/generate_clients/tutorial001_py39.py hl[7:9,12:13,16:17,21] *}

请注意，*路径操作* 定义了他们所用于请求数据和回应数据的模型，所使用的模型是`Item` 和 `ResponseMessage`。

### API 文档

如果您访问API文档，您将看到它具有在请求中发送和在响应中接收数据的**模式(schemas)**：

<img src="/img/tutorial/generate-clients/image01.png">

您可以看到这些模式，因为它们是用程序中的模型声明的。

那些信息可以在应用的 **OpenAPI模式** 被找到，然后显示在API文档中（通过Swagger UI）。

OpenAPI中所包含的模型里有相同的信息可以用于 **生成客户端代码**。

### 生成一个TypeScript 客户端

现在我们有了带有模型的应用，我们可以为前端生成客户端代码。

#### 安装 `openapi-ts`

您可以使用以下工具在前端代码中安装 `openapi-ts`:

<div class="termy">

```console
$ npm install @hey-api/openapi-ts --save-dev

---> 100%
```

</div>

#### 生成客户端代码

要生成客户端代码，您可以使用现在将要安装的命令行应用程序 `openapi-ts`。

因为它安装在本地项目中，所以您可能无法直接使用此命令，但您可以将其放在 `package.json` 文件中。

它可能看起来是这样的:

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

在这里添加 NPM `generate-client` 脚本后，您可以使用以下命令运行它:

<div class="termy">

```console
$ npm run generate-client

frontend-app@1.0.0 generate-client /home/user/code/frontend-app
> openapi-ts --input http://localhost:8000/openapi.json --output ./src/client --client axios
```

</div>

此命令将在 `./src/client` 中生成代码，并将在其内部使用 `axios`（前端HTTP库）。

### 尝试客户端代码

现在您可以导入并使用客户端代码，它可能看起来像这样，请注意，您可以为这些方法使用自动补全：

<img src="/img/tutorial/generate-clients/image02.png">

您还将自动补全要发送的数据：

<img src="/img/tutorial/generate-clients/image03.png">

/// tip

请注意， `name` 和 `price` 的自动补全，是通过其在`Item`模型(FastAPI)中的定义实现的。

///

如果发送的数据字段不符，你也会看到编辑器的错误提示:

<img src="/img/tutorial/generate-clients/image04.png">

响应(response)对象也拥有自动补全:

<img src="/img/tutorial/generate-clients/image05.png">

## 带有标签的 FastAPI 应用

在许多情况下，你的FastAPI应用程序会更复杂，你可能会使用标签来分隔不同组的*路径操作(path operations)*。

例如，您可以有一个用 `items` 的部分和另一个用于 `users` 的部分，它们可以用标签来分隔：

{* ../../docs_src/generate_clients/tutorial002_py39.py hl[21,26,34] *}

### 生成带有标签的 TypeScript 客户端

如果您使用标签为FastAPI应用生成客户端，它通常也会根据标签分割客户端代码。

通过这种方式，您将能够为客户端代码进行正确地排序和分组：

<img src="/img/tutorial/generate-clients/image06.png">

在这个案例中，您有：

* `ItemsService`
* `UsersService`

### 客户端方法名称

现在生成的方法名像 `createItemItemsPost` 看起来不太简洁:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...这是因为客户端生成器为每个 *路径操作* 使用OpenAPI的内部 **操作 ID(operation ID)**。

OpenAPI要求每个操作 ID 在所有 *路径操作* 中都是唯一的，因此 FastAPI 使用**函数名**、**路径**和**HTTP方法/操作**来生成此操作ID，因为这样可以确保这些操作 ID 是唯一的。

但接下来我会告诉你如何改进。 🤓

## 自定义操作ID和更好的方法名

您可以**修改**这些操作ID的**生成**方式，以使其更简洁，并在客户端中具有**更简洁的方法名称**。

在这种情况下，您必须确保每个操作ID在其他方面是**唯一**的。

例如，您可以确保每个*路径操作*都有一个标签，然后根据**标签**和*路径操作***名称**（函数名）来生成操作ID。

### 自定义生成唯一ID函数

FastAPI为每个*路径操作*使用一个**唯一ID**，它用于**操作ID**，也用于任何所需自定义模型的名称，用于请求或响应。

你可以自定义该函数。它接受一个 `APIRoute` 对象作为输入，并输出一个字符串。

例如，以下是一个示例，它使用第一个标签（你可能只有一个标签）和*路径操作*名称（函数名）。

然后，你可以将这个自定义函数作为 `generate_unique_id_function` 参数传递给 **FastAPI**:

{* ../../docs_src/generate_clients/tutorial003_py39.py hl[6:7,10] *}

### 使用自定义操作ID生成TypeScript客户端

现在，如果你再次生成客户端，你会发现它具有改善的方法名称：

<img src="/img/tutorial/generate-clients/image07.png">

正如你所见，现在方法名称中只包含标签和函数名，不再包含URL路径和HTTP操作的信息。

### 预处理用于客户端生成器的OpenAPI规范

生成的代码仍然存在一些**重复的信息**。

我们已经知道该方法与 **items** 相关，因为它在 `ItemsService` 中（从标签中获取），但方法名中仍然有标签名作为前缀。😕

一般情况下对于OpenAPI，我们可能仍然希望保留它，因为这将确保操作ID是**唯一的**。

但对于生成的客户端，我们可以在生成客户端之前**修改** OpenAPI 操作ID，以使方法名称更加美观和**简洁**。

我们可以将 OpenAPI JSON 下载到一个名为`openapi.json`的文件中，然后使用以下脚本**删除此前缀的标签**：

{* ../../docs_src/generate_clients/tutorial004.py *}

通过这样做，操作ID将从类似于 `items-get_items` 的名称重命名为 `get_items` ，这样客户端生成器就可以生成更简洁的方法名称。

### 使用预处理的OpenAPI生成TypeScript客户端

现在，由于最终结果保存在文件openapi.json中，你可以修改 package.json 文件以使用此本地文件，例如：

```JSON  hl_lines="7"
{
  "name": "frontend-app",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "generate-client": "openapi-ts --input ./openapi.json --output ./src/client --client axios"
  },
  "author": "",
  "license": "",
  "devDependencies": {
    "@hey-api/openapi-ts": "^0.27.38",
    "typescript": "^4.6.2"
  }
}
```

生成新的客户端之后，你现在将拥有**清晰的方法名称**，具备**自动补全**、**错误提示**等功能：

<img src="/img/tutorial/generate-clients/image08.png">

## 优点

当使用自动生成的客户端时，你将获得以下的自动补全功能：

* 方法。
* 请求体中的数据、查询参数等。
* 响应数据。

你还将获得针对所有内容的错误提示。

每当你更新后端代码并**重新生成**前端代码时，新的*路径操作*将作为方法可用，旧的方法将被删除，并且其他任何更改将反映在生成的代码中。 🤓

这也意味着如果有任何更改，它将自动**反映**在客户端代码中。如果你**构建**客户端，在使用的数据上存在**不匹配**时，它将报错。

因此，你将在开发周期的早期**检测到许多错误**，而不必等待错误在生产环境中向最终用户展示，然后尝试调试问题所在。 ✨
