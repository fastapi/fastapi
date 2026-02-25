# 關於 FastAPI 版本 { #about-fastapi-versions }

**FastAPI** 已經在許多應用與系統的生產環境中使用，且測試涵蓋率維持在 100%。同時開發仍在快速推進。

經常加入新功能、定期修復錯誤，程式碼也在持續改進。

這就是為什麼目前版本仍為 `0.x.x`，這表示每個版本都可能包含破壞性變更。這遵循 <a href="https://semver.org/" class="external-link" target="_blank">語意化版本（Semantic Versioning）</a> 的慣例。

你現在就可以用 **FastAPI** 建置生產環境的應用（而且你可能已經這麼做一段時間了），只要確保你使用的版本能與其餘程式碼正確相容。

## 鎖定你的 `fastapi` 版本 { #pin-your-fastapi-version }

首先，你應該將你使用的 **FastAPI** 版本「鎖定（pin）」到你知道對你的應用可正常運作的最新特定版本。

例如，假設你的應用使用 `0.112.0` 版本。

如果你使用 `requirements.txt` 檔案，可以這樣指定版本：

```txt
fastapi[standard]==0.112.0
```

這表示你會使用完全相同的 `0.112.0` 版本。

或你也可以這樣鎖定：

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

這表示會使用 `0.112.0`（含）以上但小於 `0.113.0` 的版本，例如 `0.112.2` 也會被接受。

如果你使用其他安裝管理工具，例如 `uv`、Poetry、Pipenv 等，它們也都有可用來指定套件特定版本的方法。

## 可用版本 { #available-versions }

你可以在 [發行說明](../release-notes.md){.internal-link target=_blank} 查看可用版本（例如用來確認目前最新版本）。

## 關於版本 { #about-versions }

依照語意化版本的慣例，任何低於 `1.0.0` 的版本都可能加入破壞性變更。

FastAPI 也遵循慣例：任何「PATCH」版本變更僅用於修正錯誤與非破壞性變更。

/// tip

「PATCH」是最後一個數字，例如在 `0.2.3` 中，PATCH 版本是 `3`。

///

因此，你可以將版本鎖定為如下形式：

```txt
fastapi>=0.45.0,<0.46.0
```

破壞性變更與新功能會在「MINOR」版本加入。

/// tip

「MINOR」是中間的數字，例如在 `0.2.3` 中，MINOR 版本是 `2`。

///

## 升級 FastAPI 版本 { #upgrading-the-fastapi-versions }

你應該為你的應用撰寫測試。

在 **FastAPI** 中這很容易（感謝 Starlette），請參考文件：[測試](../tutorial/testing.md){.internal-link target=_blank}

有了測試之後，你就可以將 **FastAPI** 升級到較新的版本，並透過執行測試來確保所有程式碼都能正確運作。

如果一切正常，或在完成必要調整且所有測試通過之後，就可以把你的 `fastapi` 鎖定到該新的版本。

## 關於 Starlette { #about-starlette }

你不應鎖定 `starlette` 的版本。

不同的 **FastAPI** 版本會使用特定較新的 Starlette 版本。

因此，你可以直接讓 **FastAPI** 使用正確的 Starlette 版本。

## 關於 Pydantic { #about-pydantic }

Pydantic 在其測試中涵蓋了 **FastAPI** 的測試，因此 Pydantic 的新版本（高於 `1.0.0`）一律與 FastAPI 相容。

你可以將 Pydantic 鎖定到任何高於 `1.0.0`、適合你的版本。

例如：

```txt
pydantic>=2.7.0,<3.0.0
```
