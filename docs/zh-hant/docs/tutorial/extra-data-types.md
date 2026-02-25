# 額外的資料型別 { #extra-data-types }

到目前為止，你一直在使用常見的資料型別，例如：

* `int`
* `float`
* `str`
* `bool`

但你也可以使用更複雜的資料型別。

而且你仍然會擁有目前為止所見的同樣功能：

* 極佳的編輯器支援。
* 將傳入請求的資料轉換。
* 回應資料的轉換。
* 資料驗證。
* 自動產生註解與文件。

## 其他資料型別 { #other-data-types }

以下是你可以使用的一些其他資料型別：

* `UUID`：
    * 一種標準的「通用唯一識別碼 (Universally Unique Identifier)」，常見於許多資料庫與系統的 ID。
    * 在請求與回應中會以 `str` 表示。
* `datetime.datetime`：
    * Python 的 `datetime.datetime`。
    * 在請求與回應中會以 ISO 8601 格式的 `str` 表示，例如：`2008-09-15T15:53:00+05:00`。
* `datetime.date`：
    * Python 的 `datetime.date`。
    * 在請求與回應中會以 ISO 8601 格式的 `str` 表示，例如：`2008-09-15`。
* `datetime.time`：
    * Python 的 `datetime.time`。
    * 在請求與回應中會以 ISO 8601 格式的 `str` 表示，例如：`14:23:55.003`。
* `datetime.timedelta`：
    * Python 的 `datetime.timedelta`。
    * 在請求與回應中會以總秒數的 `float` 表示。
    * Pydantic 也允許用「ISO 8601 time diff encoding」來表示，<a href="https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers" class="external-link" target="_blank">詳情見文件</a>。
* `frozenset`：
    * 在請求與回應中與 `set` 相同處理：
        * 在請求中，會讀取一個 list，去除重複並轉為 `set`。
        * 在回應中，`set` 會被轉為 `list`。
        * 生成的 schema 會指定 `set` 的值為唯一（使用 JSON Schema 的 `uniqueItems`）。
* `bytes`：
    * 標準的 Python `bytes`。
    * 在請求與回應中會被當作 `str` 處理。
    * 生成的 schema 會指定其為 `str`，且 "format" 為 `binary`。
* `Decimal`：
    * 標準的 Python `Decimal`。
    * 在請求與回應中，與 `float` 的處理方式相同。
* 你可以在此查閱所有可用的 Pydantic 資料型別：<a href="https://docs.pydantic.dev/latest/usage/types/types/" class="external-link" target="_blank">Pydantic 資料型別</a>。

## 範例 { #example }

以下是一個帶有參數、使用上述部分型別的 *路徑操作 (path operation)* 範例。

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

請注意，函式內的參數會是它們的自然資料型別，因此你可以進行一般的日期運算，例如：

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
