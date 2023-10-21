# 历史、设计与未来

不久前, <a href="https://github.com/tiangolo/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">一位 **FastAPI** 用户询问</a>:

> 这个项目的历史是怎样的？它似乎在几周内从无到有，变得令人惊叹 [...]

以下是这段历史的一小部分。

## 替代方案

几年来，我一直在创建具有复杂需求的API（机器学习、分布式系统、异步任务、NoSQL数据库等)，领导了几个开发团队。

作为其中的一部分，我需要调查、测试和使用许多替代方案。

**FastAPI** 的历史在很大程度上是它前辈们的历史。

如 [Alternatives](alternatives.md){.internal-link target=_blank}一节中所述：

<blockquote markdown="1">

如果没有前人的工作，就不会有 **FastAPI**。

之前许多已有的工具促使了它的诞生。

几年来，我一直在避免创建一个新的框架。首先，我尝试使用许多不同的框架、插件和工具来解决 **FastAPI** 涵盖的所有功能。

但在某种程度上，除了创建提供所有这些功能之外，别无选择。通过从以前的工具中汲取最好的想法，并使用以前甚至不可用的语言功能（Python 3.6+ 类型提示），以尽可能好的方式将它们组合在一起。

</blockquote>

## 调查研究

通过使用以前的所有替代方案，我有机会从中学习，获取想法，并以我能为自己和我合作过的开发团队找到的最佳方式将它们结合起来。

例如，很明显在理想情况下它应该基于标准的Python类型提示。

此外，最好的办法是使用现有的标准。

因此，在开始编写 **FastAPI** 之前，我花了几个月的时间研究学习OpenAPI、JSON Schema、OAuth2等规范。了解它们的关系、重叠和差异。

## 设计

然后，我花了一些时间设计从用户角度（作为使用FastAPI的开发人员）出发的开发人员“API”。

我在最流行的Python编辑器中测试了几个想法：PyCharm，VS Code，基于Jedi的编辑器。

根据上一次 <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python开发者调查</a>，这项调查覆盖了大约80%的用户。

这意味着 **FastAPI** 是用80%的Python开发人员使用的编辑器专门测试过的。由于其他大多数编辑器都倾向于有着类似的工作方式，它的所有好处应该适用于几乎所有的编辑器。

这样我就可以找到最好的方法来尽可能地减少重复代码，到处都有补全，类型和错误检查，等等。

所有这些都给开发人员提供了最佳的开发体验。

## 必要条件

在测试了几种替代方案后，我决定使用 <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">**Pydantic**</a>，因为它具有优势。

然后，我为它做出了贡献，使它完全符合JSON模式，支持定义约束声明的不同方式，并基于几个编辑器中的测试改进编辑器支持（类型检查、自动填充）。

在开发过程中，我还为 <a href="https://www.starlette.io/" class="external-link" target="_blank">**Starlette**</a> 的另一个关键需求做出了贡献。

## 发展

当我开始创建 **FastAPI** 时，大多数组件已经就位，设计已经定义，需求和工具已经准备好，关于标准和规范的知识也很清晰明了。

## 未来

到目前为止，很明显，**FastAPI** 及其思想对许多人都很有用。

为了更好的适应许多案例，人们选择了它而不是以前的替代方案。

许多开发人员和团队（包括我和我的团队）的项目已经依赖于 **FastAPI**。

但尽管如此，仍有许多改进和功能即将到来。

**FastAPI** 大有可为。

非常感谢[您的帮助](help-fastapi.md){.internal-link target=_blank}。
