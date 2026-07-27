# 通用 - 如何操作 - 诀窍 { #general-how-to-recipes }

这里是一些指向文档中其他部分的链接，用于解答一般性或常见问题。

## 数据过滤 - 安全性 { #filter-data-security }

为确保不返回超过需要的数据，请阅读 [教程 - 响应模型 - 返回类型](../tutorial/response-model.md) 文档。

## 优化响应性能 - 响应模型 - 返回类型 { #optimize-response-performance-response-model-return-type }

在返回 JSON 数据时优化性能，请使用返回类型或响应模型，这样 Pydantic 会在 Rust 侧处理到 JSON 的序列化，而无需经过 Python。更多内容请阅读 [教程 - 响应模型 - 返回类型](../tutorial/response-model.md) 文档。

## 文档的标签 - OpenAPI { #documentation-tags-openapi }

在文档界面中添加**路径操作**的标签和进行分组，请阅读 [教程 - 路径操作配置 - Tags](../tutorial/path-operation-configuration.md#tags) 文档。

## 文档的概要和描述 - OpenAPI { #documentation-summary-and-description-openapi }

在文档界面中添加**路径操作**的概要和描述，请阅读 [教程 - 路径操作配置 - Summary 和 Description](../tutorial/path-operation-configuration.md#summary-and-description) 文档。

## 文档的响应描述 - OpenAPI { #documentation-response-description-openapi }

在文档界面中定义并显示响应描述，请阅读 [教程 - 路径操作配置 - 响应描述](../tutorial/path-operation-configuration.md#response-description) 文档。

## 文档弃用**路径操作** - OpenAPI { #documentation-deprecate-a-path-operation-openapi }

在文档界面中显示弃用的**路径操作**，请阅读 [教程 - 路径操作配置 - 弃用](../tutorial/path-operation-configuration.md#deprecate-a-path-operation) 文档。

## 将任何数据转换为 JSON 兼容格式 { #convert-any-data-to-json-compatible }

要将任何数据转换为 JSON 兼容格式，请阅读 [教程 - JSON 兼容编码器](../tutorial/encoder.md) 文档。

## OpenAPI 元数据 - 文档 { #openapi-metadata-docs }

要添加 OpenAPI 的元数据，包括许可证、版本、联系方式等，请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md) 文档。

## OpenAPI 自定义 URL { #openapi-custom-url }

要自定义 OpenAPI 的 URL（或删除它），请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md#openapi-url) 文档。

## OpenAPI 文档 URL { #openapi-docs-urls }

要更改自动生成的文档用户界面所使用的 URL，请阅读 [教程 - 元数据和文档 URL](../tutorial/metadata.md#docs-urls)。
