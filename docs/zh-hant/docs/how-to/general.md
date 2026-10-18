# 通用 - 操作指南 - 實用範例 { #general-how-to-recipes }

以下是文件中其他位置的指引連結，適用於一般或常見問題。

## 篩選資料 - 安全性 { #filter-data-security }

為確保你不會回傳超出應有的資料，請參閱[教學 - 回應模型 - 回傳型別](../tutorial/response-model.md)。

## 最佳化回應效能 - 回應模型 - 回傳型別 { #optimize-response-performance-response-model-return-type }

為了在回傳 JSON 資料時最佳化效能，請使用回傳型別或回應模型，如此 Pydantic 會在 Rust 端處理序列化為 JSON，而不經過 Python。更多內容請參閱[教學 - 回應模型 - 回傳型別](../tutorial/response-model.md)。

## 文件標籤 - OpenAPI { #documentation-tags-openapi }

要在你的*路徑操作（path operation）*加入標籤，並在文件 UI 中分組，請參閱[教學 - 路徑操作設定 - 標籤](../tutorial/path-operation-configuration.md#tags)。

## 文件摘要與描述 - OpenAPI { #documentation-summary-and-description-openapi }

要為你的*路徑操作*加入摘要與描述，並在文件 UI 中顯示，請參閱[教學 - 路徑操作設定 - 摘要與描述](../tutorial/path-operation-configuration.md#summary-and-description)。

## 文件回應描述 - OpenAPI { #documentation-response-description-openapi }

要定義在文件 UI 中顯示的回應描述，請參閱[教學 - 路徑操作設定 - 回應描述](../tutorial/path-operation-configuration.md#response-description)。

## 文件將*路徑操作*標記為已棄用 - OpenAPI { #documentation-deprecate-a-path-operation-openapi }

要將*路徑操作*標記為已棄用，並在文件 UI 中顯示，請參閱[教學 - 路徑操作設定 - 棄用](../tutorial/path-operation-configuration.md#deprecate-a-path-operation)。

## 將任意資料轉換為 JSON 相容格式 { #convert-any-data-to-json-compatible }

要將任意資料轉換為 JSON 相容格式，請參閱[教學 - JSON 相容編碼器](../tutorial/encoder.md)。

## OpenAPI 中繼資料 - 文件 { #openapi-metadata-docs }

要在你的 OpenAPI 綱要中加入中繼資料（包含授權、版本、聯絡方式等），請參閱[教學 - 中繼資料與文件 URL](../tutorial/metadata.md)。

## 自訂 OpenAPI URL { #openapi-custom-url }

要自訂（或移除）OpenAPI 的 URL，請參閱[教學 - 中繼資料與文件 URL](../tutorial/metadata.md#openapi-url)。

## OpenAPI 文件 URL { #openapi-docs-urls }

要更新自動產生的文件使用者介面所使用的 URL，請參閱[教學 - 中繼資料與文件 URL](../tutorial/metadata.md#docs-urls)。
