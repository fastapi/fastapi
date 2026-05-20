# 流式数据 { #stream-data }

如果你要流式传输可以结构化为 JSON 的数据，你应该[流式传输 JSON Lines](../tutorial/stream-json-lines.md)。

但如果你想流式传输纯二进制数据或字符串，可以按下面的方法操作。

/// info | 信息

自 FastAPI 0.134.0 起新增。

///

## 使用场景 { #use-cases }

如果你想流式传输纯字符串，例如直接来自某个 AI LLM 服务的输出，可以使用它。

你也可以用它来流式传输大型二进制文件，在读取的同时按块发送，无需一次性把所有内容读入内存。

你还可以用这种方式流式传输视频或音频，甚至可以在处理的同时生成并发送。

## 使用 `yield` 的 `StreamingResponse` { #a-streamingresponse-with-yield }

如果你在*路径操作函数*中声明 `response_class=StreamingResponse`，你就可以使用 `yield` 依次发送每个数据块。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI 会将每个数据块原样交给 `StreamingResponse`，不会尝试将其转换为 JSON 或做类似处理。

### 非 async 的*路径操作函数* { #non-async-path-operation-functions }

你也可以使用常规的 `def` 函数（不带 `async`），并以相同方式使用 `yield`。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### 无需注解 { #no-annotation }

你其实不需要为流式二进制数据声明返回类型注解。

由于 FastAPI 不会使用 Pydantic 将数据转换为 JSON，也不会以任何方式序列化，在这种情况下，类型注解只供你的编辑器和工具使用，FastAPI 不会使用它。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

这也意味着，使用 `StreamingResponse` 时，你拥有按需精确生成与编码字节数据的自由，同时也承担相应的责任，它与类型注解无关。🤓

### 流式传输字节 { #stream-bytes }

主要的用例之一是流式传输 `bytes` 而不是字符串，这当然可以做到。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## 自定义 `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

在上面的示例中，虽然按字节流式传输了数据，但响应没有 `Content-Type` 头，因此客户端不知道接收到的数据类型。

你可以创建 `StreamingResponse` 的自定义子类，将 `Content-Type` 头设置为你要流式传输的数据类型。

例如，你可以创建一个 `PNGStreamingResponse`，通过 `media_type` 属性把 `Content-Type` 头设置为 `image/png`：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

然后你可以在*路径操作函数*中通过 `response_class=PNGStreamingResponse` 使用这个新类：

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### 模拟文件 { #simulate-a-file }

在这个示例中，我们用 `io.BytesIO` 模拟了一个文件，它是只驻留在内存中的类文件对象，但提供相同的接口。

例如，我们可以像对文件那样迭代它来消费其内容。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | 技术细节

另外两个变量 `image_base64` 和 `binary_image` 表示一张图像，先用 Base64 编码，再转换为 bytes，最后传给 `io.BytesIO`。

只是为了让它们能和示例放在同一个文件里，便于你直接复制运行。🥚

///

通过使用 `with` 代码块，我们确保在生成器函数（带有 `yield` 的函数）完成后关闭这个类文件对象。也就是在发送完响应之后。

在这个特定示例中这并不那么重要，因为它是一个内存中的假文件（使用 `io.BytesIO`），但对于真实文件，确保在完成相关工作后关闭文件是很重要的。

### 文件与异步 { #files-and-async }

大多数情况下，类文件对象默认与 async 和 await 不兼容。

例如，它们没有 `await file.read()`，也不支持 `async for chunk in file`。

而且很多情况下，读取它们是一个阻塞操作（可能会阻塞事件循环），因为数据来自磁盘或网络。

/// info | 信息

上面的示例其实是个例外，因为 `io.BytesIO` 对象已经在内存中，所以读取它不会阻塞。

但在许多情况下，读取文件或类文件对象会发生阻塞。

///

为避免阻塞事件循环，你可以简单地把*路径操作函数*声明为常规的 `def`（而不是 `async def`），这样 FastAPI 会在一个线程池工作线程上运行它，从而避免阻塞主事件循环。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | 提示

如果你需要在异步函数里调用阻塞代码，或在阻塞函数里调用异步函数，可以使用 [Asyncer](https://asyncer.tiangolo.com)，它是 FastAPI 的姐妹库。

///

### `yield from` { #yield-from }

当你在迭代某个对象（例如类文件对象），并为每个条目执行 `yield` 时，你也可以使用 `yield from` 直接产出每个条目，从而省去 `for` 循环。

这并不是 FastAPI 特有的功能，只是 Python 的语法，但这是一个值得知道的小技巧。😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
