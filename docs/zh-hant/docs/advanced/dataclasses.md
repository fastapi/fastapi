# 使用 Dataclasses { #using-dataclasses }

FastAPI 建立在 **Pydantic** 之上，我之前示範過如何使用 Pydantic 模型來宣告請求與回應。

但 FastAPI 也同樣支援以相同方式使用 <a href="https://docs.python.org/3/library/dataclasses.html" class="external-link" target="_blank">`dataclasses`</a>：

{* ../../docs_src/dataclasses_/tutorial001_py310.py hl[1,6:11,18:19] *}

這之所以可行，要感謝 **Pydantic**，因為它 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/#use-of-stdlib-dataclasses-with-basemodel" class="external-link" target="_blank">內建支援 `dataclasses`</a>。

所以，即使上面的程式碼沒有明確使用 Pydantic，FastAPI 仍會使用 Pydantic 將那些標準的 dataclass 轉換為 Pydantic 版本的 dataclass。

而且當然一樣支援：

- 資料驗證
- 資料序列化
- 資料文件化等

它的運作方式與 Pydantic 模型相同；實際上，底層就是透過 Pydantic 達成的。

/// info

請記得，dataclass 無法做到 Pydantic 模型能做的一切。

所以你可能仍然需要使用 Pydantic 模型。

但如果你手邊剛好有一堆 dataclass，這是個不錯的小技巧，可以用來用 FastAPI 驅動一個 Web API。🤓

///

## 在 `response_model` 中使用 Dataclasses { #dataclasses-in-response-model }

你也可以在 `response_model` 參數中使用 `dataclasses`：

{* ../../docs_src/dataclasses_/tutorial002_py310.py hl[1,6:12,18] *}

該 dataclass 會自動轉換為 Pydantic 的 dataclass。

如此一來，其結構描述（schema）會顯示在 API 文件介面中：

<img src="/img/tutorial/dataclasses/image01.png">

## 巢狀資料結構中的 Dataclasses { #dataclasses-in-nested-data-structures }

你也可以將 `dataclasses` 與其他型別註記結合，建立巢狀的資料結構。

在某些情況下，你可能仍需要使用 Pydantic 版本的 `dataclasses`。例如，當自動產生的 API 文件出現錯誤時。

這種情況下，你可以把標準的 `dataclasses` 直接換成 `pydantic.dataclasses`，它是可直接替換（drop-in replacement）的：

{* ../../docs_src/dataclasses_/tutorial003_py310.py hl[1,4,7:10,13:16,22:24,27] *}

1. 我們仍然從標準的 `dataclasses` 匯入 `field`。
2. `pydantic.dataclasses` 是 `dataclasses` 的可直接替換版本。
3. `Author` dataclass 內含一個 `Item` dataclass 的清單。
4. `Author` dataclass 被用作 `response_model` 參數。
5. 你可以將其他標準型別註記與 dataclass 一起用作請求本文。

   在此例中，它是 `Item` dataclass 的清單。
6. 這裡我們回傳一個字典，其中的 `items` 是一個 dataclass 清單。

   FastAPI 仍能將資料<dfn title="將資料轉換成可傳輸的格式">序列化</dfn>為 JSON。
7. 這裡 `response_model` 使用的是「`Author` dataclass 的清單」這種型別註記。

   同樣地，你可以把 `dataclasses` 與標準型別註記組合使用。
8. 注意這個「路徑操作函式」使用的是一般的 `def` 而非 `async def`。

   一如往常，在 FastAPI 中你可以視需要混用 `def` 與 `async def`。

   如果需要複習何時用哪個，請參考文件中關於 [`async` 與 `await`](../async.md#in-a-hurry){.internal-link target=_blank} 的章節「In a hurry?」。
9. 這個「路徑操作函式」回傳的不是 dataclass（雖然也可以），而是一個包含內部資料的字典清單。

   FastAPI 會使用 `response_model` 參數（其中包含 dataclass）來轉換回應。

你可以把 `dataclasses` 與其他型別註記以多種方式組合，形成複雜的資料結構。

查看上面程式碼中的註解提示以了解更具體的細節。

## 延伸閱讀 { #learn-more }

你也可以將 `dataclasses` 與其他 Pydantic 模型結合、從它們繼承、把它們包含進你的自訂模型等。

想了解更多，請參考 <a href="https://docs.pydantic.dev/latest/concepts/dataclasses/" class="external-link" target="_blank">Pydantic 關於 dataclasses 的文件</a>。

## 版本 { #version }

自 FastAPI 版本 `0.67.0` 起可用。🔖
