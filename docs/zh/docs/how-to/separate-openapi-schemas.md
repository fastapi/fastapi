# 是否为输入和输出分别生成 OpenAPI JSON Schema { #separate-openapi-schemas-for-input-and-output-or-not }

自从发布了 **Pydantic v2**，生成的 OpenAPI 比之前更精确、更**正确**了。😎

事实上，在某些情况下，对于同一个 Pydantic 模型，OpenAPI 中会根据是否带有**默认值**，为输入和输出分别生成**两个 JSON Schema**。

我们来看看它如何工作，以及在需要时如何修改。

## 用于输入和输出的 Pydantic 模型 { #pydantic-models-for-input-and-output }

假设你有一个带有默认值的 Pydantic 模型，例如：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:7] hl[7] *}

### 输入用的模型 { #model-for-input }

如果你像下面这样把该模型用作输入：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py ln[1:15] hl[14] *}

...那么 `description` 字段将**不是必填项**，因为它的默认值是 `None`。

### 文档中的输入模型 { #input-model-in-docs }

你可以在文档中确认，`description` 字段没有**红色星号**，也就是未被标记为必填：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image01.png">
</div>

### 输出用的模型 { #model-for-output }

但如果你把同一个模型用作输出，例如：

{* ../../docs_src/separate_openapi_schemas/tutorial001_py310.py hl[19] *}

...那么因为 `description` 有默认值，即使你**不返回该字段**，它仍然会有这个**默认值**。

### 输出响应数据的模型 { #model-for-output-response-data }

如果你在文档中交互并查看响应，即使代码没有给某个 `description` 字段赋值，JSON 响应中仍包含默认值（`null`）：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image02.png">
</div>

这意味着它**总会有值**，只是有时该值可能为 `None`（在 JSON 中是 `null`）。

这也意味着，使用你的 API 的客户端无需检查该值是否存在，他们可以**假设该字段总会存在**，只是有时它会是默认值 `None`。

在 OpenAPI 中描述这一点的方式，是把该字段标记为**必填**，因为它总会存在。

因此，一个模型的 JSON Schema 会根据它用于**输入还是输出**而有所不同：

- 用于**输入**时，`description` **不是必填**
- 用于**输出**时，它是**必填**（并且可能为 `None`，在 JSON 中为 `null`）

### 文档中的输出模型 { #model-for-output-in-docs }

你也可以在文档中查看输出模型，`name` 和 `description` **都**被**红色星号**标记为**必填**：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image03.png">
</div>

### 文档中的输入/输出模型 { #model-for-input-and-output-in-docs }

如果你查看 OpenAPI 中可用的所有 Schema（JSON Schema），你会看到有两个，一个是 `Item-Input`，一个是 `Item-Output`。

对于 `Item-Input`，`description` **不是必填**，没有红色星号。

但对于 `Item-Output`，`description` 是**必填**，带有红色星号。

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image04.png">
</div>

借助 **Pydantic v2** 的这个特性，你的 API 文档会更**精确**，如果你有自动生成的客户端和 SDK，它们也会更精确，带来更好的**开发者体验**和一致性。🎉

## 不要分离 Schema { #do-not-separate-schemas }

当然，在某些情况下，你可能希望**输入和输出使用同一个 schema**。

最常见的情形是：你已经有一些自动生成的客户端代码/SDK，你暂时不想更新所有这些自动生成的客户端代码/SDK（也许未来会，但不是现在）。

这种情况下，你可以在 **FastAPI** 中通过参数 `separate_input_output_schemas=False` 禁用该特性。

/// info | 信息

对 `separate_input_output_schemas` 的支持是在 FastAPI `0.102.0` 中添加的。🤓

///

{* ../../docs_src/separate_openapi_schemas/tutorial002_py310.py hl[10] *}

### 文档中输入/输出使用同一 Schema 的模型 { #same-schema-for-input-and-output-models-in-docs }

现在该模型的输入和输出将只使用一个 schema，即 `Item`，并且其中的 `description` **不是必填**：

<div class="screenshot">
<img src="/img/tutorial/separate-openapi-schemas/image05.png">
</div>
