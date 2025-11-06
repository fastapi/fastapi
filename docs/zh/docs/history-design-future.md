# 历史、设计、未来

不久前，<a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">曾有 **FastAPI** 用户问过</a>：

> 这个项目有怎样的历史？好像它只用了几周就从默默无闻变得众所周知……

在此，我们简单回顾一下 **FastAPI** 的历史。

## 备选方案

有那么几年，我曾领导数个开发团队为诸多复杂需求创建各种 API，这些需求包括机器学习、分布系统、异步任务、NoSQL 数据库等领域。

作为工作的一部分，我需要调研很多备选方案、还要测试并且使用这些备选方案。

**FastAPI** 其实只是延续了这些前辈的历史。

正如[备选方案](alternatives.md){.internal-link target=_blank}一章所述：

<blockquote markdown="1">
没有大家之前所做的工作，**FastAPI** 就不会存在。

以前创建的这些工具为它的出现提供了灵感。

在那几年中，我一直回避创建新的框架。首先，我尝试使用各种框架、插件、工具解决 **FastAPI** 现在的功能。

但到了一定程度之后，我别无选择，只能从之前的工具中汲取最优思路，并以尽量好的方式把这些思路整合在一起，使用之前甚至是不支持的语言特性（Python 3.6+ 的类型提示），从而创建一个能满足我所有需求的框架。

</blockquote>

## 调研

通过使用之前所有的备选方案，我有机会从它们之中学到了很多东西，获取了很多想法，并以我和我的开发团队能想到的最好方式把这些思路整合成一体。

例如，大家都清楚，在理想状态下，它应该基于标准的 Python 类型提示。

而且，最好的方式是使用现有的标准。

因此，甚至在开发 **FastAPI** 前，我就花了几个月的时间研究 OpenAPI、JSON Schema、OAuth2 等规范。深入理解它们之间的关系、重叠及区别之处。

## 设计

然后，我又花了一些时间从用户角度（使用 FastAPI 的开发者）设计了开发者 **API**。

同时，我还在最流行的 Python 代码编辑器中测试了很多思路，包括 PyCharm、VS Code、基于 Jedi 的编辑器。

根据最新 <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python 开发者调研报告</a>显示，这几种编辑器覆盖了约 80% 的用户。

也就是说，**FastAPI** 针对差不多 80% 的 Python 开发者使用的编辑器进行了测试，而且其它大多数编辑器的工作方式也与之类似，因此，**FastAPI** 的优势几乎能在所有编辑器上体现。

通过这种方式，我就能找到尽可能减少代码重复的最佳方式，进而实现处处都有自动补全、类型提示与错误检查等支持。

所有这些都是为了给开发者提供最佳的开发体验。

## 需求项

经过测试多种备选方案，我最终决定使用  <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a>，并充分利用它的优势。

我甚至为它做了不少贡献，让它完美兼容了 JSON Schema，支持多种方式定义约束声明，并基于多个编辑器，改进了它对编辑器支持（类型检查、自动补全）。

在开发期间，我还为 <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a> 做了不少贡献，这是另一个关键需求项。

## 开发

当我启动 **FastAPI** 开发的时候，绝大多数部件都已经就位，设计已经定义，需求项和工具也已经准备就绪，相关标准与规范的知识储备也非常清晰而新鲜。

## 未来

至此，**FastAPI** 及其理念已经为很多人所用。

对于很多用例，它比以前很多备选方案都更适用。

很多开发者和开发团队已经依赖 **FastAPI** 开发他们的项目（包括我和我的团队）。

但，**FastAPI** 仍有很多改进的余地，也还需要添加更多的功能。

总之，**FastAPI** 前景光明。

在此，我们衷心感谢[您的帮助](help-fastapi.md){.internal-link target=_blank}。
