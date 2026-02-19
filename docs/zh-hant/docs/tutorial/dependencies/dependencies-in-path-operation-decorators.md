# 路徑操作裝飾器中的依賴 { #dependencies-in-path-operation-decorators }

有時在你的路徑操作函式中，其實不需要某個依賴的回傳值。

或是該依賴根本沒有回傳值。

但你仍需要它被執行／解析。

這種情況下，你可以不在路徑操作函式的參數上使用 `Depends`，而是在路徑操作裝飾器加入一個 `dependencies` 的 `list`。

## 在路徑操作裝飾器加入 `dependencies` { #add-dependencies-to-the-path-operation-decorator }

路徑操作裝飾器可接受一個可選參數 `dependencies`。

它應該是由 `Depends()` 組成的 `list`：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

這些依賴會以與一般依賴相同的方式被執行／解析。但它們的值（如果有回傳）不會傳遞給你的路徑操作函式。

/// tip

有些編輯器會檢查未使用的函式參數，並將其標示為錯誤。

把這些依賴放在路徑操作裝飾器中，可以確保它們被執行，同時避免編輯器／工具報錯。

這也有助於避免讓新加入的開發者看到未使用的參數時，以為它是不必要的而感到困惑。

///

/// info

在這個範例中我們使用了自訂的（虛構的）標頭 `X-Key` 與 `X-Token`。

但在實際情況下，當你實作安全機制時，使用整合的 [Security utilities（下一章）](../security/index.md){.internal-link target=_blank} 會獲得更多好處。

///

## 依賴的錯誤與回傳值 { #dependencies-errors-and-return-values }

你可以使用與平常相同的依賴函式。

### 依賴的需求 { #dependency-requirements }

它們可以宣告請求需求（例如標頭（headers））或其他子依賴：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### 拋出例外 { #raise-exceptions }

這些依賴可以 `raise` 例外，與一般依賴相同：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### 回傳值 { #return-values }

它們可以回傳值，也可以不回傳；無論如何，回傳值都不會被使用。

因此，你可以重複使用在其他地方已使用過的一般依賴（會回傳值），即使回傳值不會被使用，該依賴仍會被執行：

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## 一組路徑操作的依賴 { #dependencies-for-a-group-of-path-operations }

之後在閱讀如何組織較大的應用程式（[較大型應用程式——多個檔案](../../tutorial/bigger-applications.md){.internal-link target=_blank}）時，你會學到如何為一組路徑操作宣告一個共同的 `dependencies` 參數。

## 全域依賴 { #global-dependencies }

接著我們會看看如何把依賴加到整個 `FastAPI` 應用程式，使其套用到每個路徑操作。
