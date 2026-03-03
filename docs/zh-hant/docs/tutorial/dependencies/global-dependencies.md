# 全域依賴 { #global-dependencies }

在某些類型的應用程式中，你可能想為整個應用程式新增依賴。

類似於你可以在[路徑操作（path operation）的裝飾器中新增 `dependencies`](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 的方式，你也可以把它們加到 `FastAPI` 應用程式上。

在這種情況下，它們會套用到應用程式中的所有路徑操作：

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}

而且，在[將 `dependencies` 新增到路徑操作裝飾器](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} 那一節中的所有概念依然適用，只是這裡是套用到整個應用中的所有路徑操作。

## 路徑操作群組的依賴 { #dependencies-for-groups-of-path-operations }

之後，在閱讀如何組織更大的應用程式（[更大的應用程式 - 多個檔案](../../tutorial/bigger-applications.md){.internal-link target=_blank}）時，可能會有多個檔案，你將會學到如何為一組路徑操作宣告單一的 `dependencies` 參數。
