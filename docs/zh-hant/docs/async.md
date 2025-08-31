# 並行與 async / await

有關*路徑操作函式*的 `async def` 語法的細節與非同步 (asynchronous) 程式碼、並行 (concurrency) 與平行 (parallelism) 的一些背景知識。

## 趕時間嗎?

<abbr title="too long; didn't read（文長慎入）"><strong>TL;DR:</strong></abbr>

如果你正在使用要求你以 `await` 語法呼叫的第三方函式庫，例如：

```Python
results = await some_library()
```

然後，使用 `async def` 宣告你的*路徑操作函式*：


```Python hl_lines="2"
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

/// note | 注意

你只能在 `async def` 建立的函式內使用 `await`。

///

---

如果你使用的是第三方函式庫並且它需要與某些外部資源（例如資料庫、API、檔案系統等）進行通訊，但不支援 `await`（目前大多數資料庫函式庫都是這樣），在這種情況下，你可以像平常一樣使用 `def` 宣告*路徑操作函式*，如下所示：

```Python hl_lines="2"
@app.get('/')
def results():
    results = some_library()
    return results
```

---

如果你的應用程式不需要與外部資源進行任何通訊並等待其回應，請使用 `async def`。

---

如果你不確定該用哪個，直接用 `def` 就好。

---

**注意**：你可以在*路徑操作函式*中混合使用 `def` 和 `async def` ，並使用最適合你需求的方式來定義每個函式。FastAPI 會幫你做正確的處理。

無論如何，在上述哪種情況下，FastAPI 仍將以非同步方式運行，並且速度非常快。

但透過遵循上述步驟，它將能進行一些效能最佳化。

## 技術細節

現代版本的 Python 支援使用 **「協程」** 的 **`async` 和 `await`** 語法來寫 **「非同步程式碼」**。

接下來我們逐一介紹：

* **非同步程式碼**
* **`async` 和 `await`**
* **協程**

## 非同步程式碼

非同步程式碼僅意味著程式語言 💬 有辦法告訴電腦/程式 🤖 在程式碼中的某個點，它 🤖 需要等待某些事情完成。讓我們假設這些事情被稱為「慢速檔案」📝。

因此，在等待「慢速檔案」📝 完成的這段時間，電腦可以去處理一些其他工作。

接著程式 🤖 會在有空檔時回來查看是否有等待的工作已經完成，並執行必要的後續操作。

接下來，它 🤖 完成第一個工作（例如我們的「慢速檔案」📝）並繼續執行相關的所有操作。
這個「等待其他事情」通常指的是一些相對較慢的（與處理器和 RAM 記憶體的速度相比）的 <abbr title="Input and Output">I/O</abbr> 操作，比如說：

* 透過網路傳送來自用戶端的資料
* 從網路接收來自用戶端的資料
* 從磁碟讀取檔案內容
* 將內容寫入磁碟
* 遠端 API 操作
* 資料庫操作
* 資料庫查詢
* 等等

由於大部分的執行時間都消耗在等待 <abbr title="輸入與輸出">I/O</abbr> 操作上，因此這些操作被稱為 "I/O 密集型" 操作。

之所以稱為「非同步」，是因為電腦/程式不需要與那些耗時的任務「同步」，等待任務完成的精確時間，然後才能取得結果並繼續工作。

相反地，非同步系統在任務完成後，可以讓任務稍微等一下（幾微秒），等待電腦/程式完成手頭上的其他工作，然後再回來取得結果繼續進行。

相對於「非同步」（asynchronous），「同步」（synchronous）也常被稱作「順序性」（sequential），因為電腦/程式會依序執行所有步驟，即便這些步驟涉及等待，才會切換到其他任務。

### 並行與漢堡

上述非同步程式碼的概念有時也被稱為「並行」，它不同於「平行」。

並行和平行都與 "不同的事情或多或少同時發生" 有關。

但並行和平行之間的細節是完全不同的。

為了理解差異，請想像以下有關漢堡的故事：

### 並行漢堡

你和你的戀人去速食店，排隊等候時，收銀員正在幫排在你前面的人點餐。😍

<img src="/img/async/concurrent-burgers/concurrent-burgers-01.png" class="illustration">

輪到你了，你給你與你的戀人點了兩個豪華漢堡。🍔🍔

<img src="/img/async/concurrent-burgers/concurrent-burgers-02.png" class="illustration">

收銀員通知廚房準備你的漢堡（儘管他們還在為前面其他顧客準備食物）。

<img src="/img/async/concurrent-burgers/concurrent-burgers-03.png" class="illustration">

之後你完成付款。💸

收銀員給你一個號碼牌。

<img src="/img/async/concurrent-burgers/concurrent-burgers-04.png" class="illustration">

在等待漢堡的同時，你可以與戀人選一張桌子，然後坐下來聊很長一段時間（因為漢堡十分豪華，準備特別費工。）

這段時間，你還能欣賞你的戀人有多麼的可愛、聰明與迷人。✨😍✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-05.png" class="illustration">

當你和戀人邊聊天邊等待時，你會不時地查看櫃檯上的顯示的號碼，確認是否已經輪到你了。

然後在某個時刻，終於輪到你了。你走到櫃檯，拿了漢堡，然後回到桌子上。

<img src="/img/async/concurrent-burgers/concurrent-burgers-06.png" class="illustration">

你和戀人享用這頓大餐，整個過程十分開心✨

<img src="/img/async/concurrent-burgers/concurrent-burgers-07.png" class="illustration">

/// info

漂亮的插畫來自 <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

想像你是故事中的電腦或程式 🤖。

當你排隊時，你在放空😴，等待輪到你，沒有做任何「生產性」的事情。但這沒關係，因為收銀員只是接單（而不是準備食物），所以排隊速度很快。

然後，當輪到你時，你開始做真正「有生產力」的工作，處理菜單，決定你想要什麼，替戀人選擇餐點，付款，確認你給了正確的帳單或信用卡，檢查你是否被正確收費，確認訂單中的項目是否正確等等。

但是，即使你還沒有拿到漢堡，你與收銀員的工作已經「暫停」了 ⏸，因為你必須等待 🕙 漢堡準備好。

但當你離開櫃檯，坐到桌子旁，拿著屬於你的號碼等待時，你可以把注意力 🔀 轉移到戀人身上，並開始「工作」⏯ 🤓——也就是和戀人調情 😍。這時你又開始做一些非常「有生產力」的事情。

接著，收銀員 💁 將你的號碼顯示在櫃檯螢幕上，並告訴你「漢堡已經做好了」。但你不會瘋狂地立刻跳起來，因為顯示的號碼變成了你的。你知道沒有人會搶走你的漢堡，因為你有自己的號碼，他們也有他們的號碼。

所以你會等戀人講完故事（完成當前的工作 ⏯/正在進行的任務 🤓），然後微笑著溫柔地說你要去拿漢堡了 ⏸。

然後你走向櫃檯 🔀，回到已經完成的最初任務 ⏯，拿起漢堡，說聲謝謝，並帶回桌上。這就結束了與櫃檯的互動步驟/任務 ⏹，接下來會產生一個新的任務，「吃漢堡」 🔀 ⏯，而先前的「拿漢堡」任務已經完成了 ⏹。

### 平行漢堡

現在，讓我們來想像這裡不是「並行漢堡」，而是「平行漢堡」。

你和戀人一起去吃平行的速食餐。

你們站在隊伍中，前面有幾位（假設有 8 位）既是收銀員又是廚師的員工，他們同時接單並準備餐點。

所有排在你前面的人都在等著他們的漢堡準備好後才會離開櫃檯，因為每位收銀員在接完單後，馬上會去準備漢堡，然後才回來處理下一個訂單。

<img src="/img/async/parallel-burgers/parallel-burgers-01.png" class="illustration">

終於輪到你了，你為你和你的戀人點了兩個非常豪華的漢堡。

你付款了 💸。

<img src="/img/async/parallel-burgers/parallel-burgers-02.png" class="illustration">

收銀員走進廚房準備食物。

你站在櫃檯前等待 🕙，以免其他人先拿走你的漢堡，因為這裡沒有號碼牌系統。

<img src="/img/async/parallel-burgers/parallel-burgers-03.png" class="illustration">

由於你和戀人都忙著不讓別人搶走你的漢堡，等漢堡準備好時，你根本無法專心和戀人互動。😞

這是「同步」(synchronous)工作，你和收銀員/廚師 👨‍🍳 是「同步化」的。你必須等到 🕙 收銀員/廚師 👨‍🍳 完成漢堡並交給你的那一刻，否則別人可能會拿走你的餐點。

<img src="/img/async/parallel-burgers/parallel-burgers-04.png" class="illustration">

最終，經過長時間的等待 🕙，收銀員/廚師 👨‍🍳 拿著漢堡回來了。

<img src="/img/async/parallel-burgers/parallel-burgers-05.png" class="illustration">

你拿著漢堡，和你的戀人回到餐桌。

你們僅僅是吃完漢堡，然後就結束了。⏹

<img src="/img/async/parallel-burgers/parallel-burgers-06.png" class="illustration">

整個過程中沒有太多的談情說愛，因為大部分時間 🕙 都花在櫃檯前等待。😞

/// info

漂亮的插畫來自 <a href="https://www.instagram.com/ketrinadrawsalot" class="external-link" target="_blank">Ketrina Thompson</a>. 🎨

///

---

在這個平行漢堡的情境下，你是一個程式 🤖 且有兩個處理器（你和戀人），兩者都在等待 🕙 並專注於等待櫃檯上的餐點 🕙，等待的時間非常長。

這家速食店有 8 個處理器（收銀員/廚師）。而並行漢堡店可能只有 2 個處理器（一位收銀員和一位廚師）。

儘管如此，最終的體驗並不是最理想的。😞

---

這是與漢堡類似的故事。🍔

一個更「現實」的例子，想像一間銀行。

直到最近，大多數銀行都有多位出納員 👨‍💼👨‍💼👨‍💼👨‍💼，以及一條長長的隊伍 🕙🕙🕙🕙🕙🕙🕙🕙。

所有的出納員都在一個接一個地滿足每位客戶的所有需求 👨‍💼⏯。

你必須長時間排隊 🕙，不然就會失去機會。

所以，你不會想帶你的戀人 😍 一起去銀行辦事 🏦。

### 漢堡結論

在「和戀人一起吃速食漢堡」的這個場景中，由於有大量的等待 🕙，使用並行系統 ⏸🔀⏯ 更有意義。

這也是大多數 Web 應用的情況。

許多用戶正在使用你的應用程式，而你的伺服器則在等待 🕙 這些用戶不那麼穩定的網路來傳送請求。

接著，再次等待 🕙 回應。

這種「等待」 🕙 通常以微秒來衡量，但累加起來，最終還是花費了很多等待時間。

這就是為什麼對於 Web API 來說，使用非同步程式碼 ⏸🔀⏯ 是非常有意義的。

這種類型的非同步性正是 NodeJS 成功的原因（儘管 NodeJS 不是平行的），這也是 Go 語言作為程式語言的一個強大優勢。

這與 **FastAPI** 所能提供的性能水平相同。

你可以同時利用並行性和平行性，進一步提升效能，這比大多數已測試的 NodeJS 框架都更快，並且與 Go 語言相當，而 Go 是一種更接近 C 的編譯語言（<a href="https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=query&l=zijmkf-1" class="external-link" target="_blank">感謝 Starlette</a>）。

### 並行比平行更好嗎？

不是的！這不是故事的本意。

並行與平行不同。並行在某些 **特定** 的需要大量等待的情境下表現更好。正因如此，並行在 Web 應用程式開發中通常比平行更有優勢。但並不是所有情境都如此。

因此，為了平衡報導，想像下面這個短故事

> 你需要打掃一間又大又髒的房子。

*是的，這就是全部的故事。*

---

這裡沒有任何需要等待 🕙 的地方，只需要在房子的多個地方進行大量的工作。

你可以像漢堡的例子那樣輪流進行，先打掃客廳，再打掃廚房，但由於你不需要等待 🕙 任何事情，只需要持續地打掃，輪流並不會影響任何結果。

無論輪流執行與否（並行），你都需要相同的工時完成任務，同時需要執行相同工作量。

但是，在這種情境下，如果你可以邀請8位前收銀員/廚師（現在是清潔工）來幫忙，每個人（加上你）負責房子的某個區域，這樣你就可以 **平行** 地更快完成工作。

在這個場景中，每個清潔工（包括你）都是一個處理器，完成工作的一部分。

由於大多數的執行時間都花在實際的工作上（而不是等待），而電腦中的工作由 <abbr title="Central Processing Unit">CPU</abbr> 完成，因此這些問題被稱為「CPU 密集型」。

---

常見的 CPU 密集型操作範例包括那些需要進行複雜數學計算的任務。

例如：

* **音訊**或**圖像處理**；
* **電腦視覺**：一張圖片由數百萬個像素組成，每個像素有 3 個值/顏色，處理這些像素通常需要同時進行大量計算；
* **機器學習**: 通常需要大量的「矩陣」和「向量」運算。想像一個包含數字的巨大電子表格，並所有的數字同時相乘;
* **深度學習**: 這是機器學習的子領域，同樣適用。只不過這不僅僅是一張數字表格，而是大量的數據集合，並且在很多情況下，你會使用特殊的處理器來構建或使用這些模型。

### 並行 + 平行: Web + 機器學習

使用 **FastAPI**，你可以利用並行的優勢，這在 Web 開發中非常常見（這也是 NodeJS 的最大吸引力）。

但你也可以利用平行與多行程 (multiprocessing)（讓多個行程同時運行） 的優勢來處理機器學習系統中的 **CPU 密集型**工作。

這一點，再加上 Python 是 **資料科學**、機器學習，尤其是深度學習的主要語言，讓 **FastAPI** 成為資料科學/機器學習 Web API 和應用程式（以及許多其他應用程式）的絕佳選擇。

想了解如何在生產環境中實現這種平行性，請參見 [部屬](deployment/index.md){.internal-link target=_blank}。

## `async` 和 `await`

現代 Python 版本提供一種非常直觀的方式定義非同步程式碼。這使得它看起來就像正常的「順序」程式碼，並在適當的時機「等待」。

當某個操作需要等待才能回傳結果，並且支援這些新的 Python 特性時，你可以像這樣編寫程式碼：

```Python
burgers = await get_burgers(2)
```

這裡的關鍵是 `await`。它告訴 Python 必須等待 ⏸ `get_burgers(2)` 完成它的工作 🕙， 然後將結果儲存在 `burgers` 中。如此，Python 就可以在此期間去處理其他事情 🔀 ⏯ （例如接收另一個請求）。

要讓 `await` 運作，它必須位於支持非同步功能的函式內。為此，只需使用 `async def` 宣告函式：

```Python hl_lines="1"
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

...而不是 `def`:

```Python hl_lines="2"
# This is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff to create the burgers
    return burgers
```

使用 `async def`，Python Python 知道在該函式內需要注意 `await`，並且它可以「暫停」 ⏸ 執行該函式，然後執行其他任務 🔀 後回來。

當你想要呼叫 `async def` 函式時，必須使用「await」。因此，這樣寫將無法運行：

```Python
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

---

如果你正在使用某個函式庫，它告訴你可以使用 `await` 呼叫它，那麼你需要用 `async def` 定義*路徑操作函式*，如：

```Python hl_lines="2-3"
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

### 更多技術細節

你可能已經注意到，`await` 只能在 `async def` 定義的函式內使用。

但同時，使用 `async def` 定義的函式本身也必須被「等待」。所以，帶有 `async def` 函式只能在其他使用 `async def` 定義的函式內呼叫。

那麼，這就像「先有雞還是先有蛋」的問題，要如何呼叫第一個 `async` 函式呢？

如果你使用 FastAPI，無需擔心這個問題，因為「第一個」函式將是你的*路徑操作函式*，FastAPI 會知道如何正確處理這個問題。

但如果你想在沒有 FastAPI 的情況下使用 `async` / `await`，你也可以這樣做。

### 編寫自己的非同步程式碼

Starlette （和 **FastAPI**） 是基於 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 實作的，這使得它們與 Python 標準函式庫相容 <a href="https://docs.python.org/3/library/asyncio-task.html" class="external-link" target="_blank">asyncio</a> 和 <a href="https://trio.readthedocs.io/en/stable/" class="external-link" target="_blank">Trio</a>。

特別是，你可以直接使用 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 來處理更複雜的並行使用案例，這些案例需要你在自己的程式碼中使用更高階的模式。

即使你不使用 **FastAPI**，你也可以使用 <a href="https://anyio.readthedocs.io/en/stable/" class="external-link" target="_blank">AnyIO</a> 來撰寫自己的非同步應用程式，並獲得高相容性及一些好處（例如結構化並行）。

### 其他形式的非同步程式碼

使用 `async` 和 `await` 的風格在語言中相對較新。

但它使處理異步程式碼變得更加容易。

相同的語法（或幾乎相同的語法）最近也被包含在現代 JavaScript（無論是瀏覽器還是 NodeJS）中。

但在此之前，處理異步程式碼要更加複雜和困難。

在較舊的 Python 版本中，你可能會使用多執行緒或 <a href="https://www.gevent.org/" class="external-link" target="_blank">Gevent</a>。但這些程式碼要更難以理解、調試和思考。

在較舊的 NodeJS / 瀏覽器 JavaScript 中，你會使用「回呼」，這可能會導致“回呼地獄”。

## 協程

**協程** 只是 `async def` 函式所回傳的非常特殊的事物名稱。Python 知道它是一個類似函式的東西，可以啟動它，並且在某個時刻它會結束，但它也可能在內部暫停 ⏸，只要遇到 `await`。

這種使用 `async` 和 `await` 的非同步程式碼功能通常被概括為「協程」。這與 Go 語言的主要特性「Goroutines」相似。

## 結論

讓我們再次回顧之前的句子：

> 現代版本的 Python 支持使用 **"協程"** 的 **`async` 和 `await`** 語法來寫 **"非同步程式碼"**。

現在應該能明白其含意了。✨

這些就是驅動 FastAPI（通過 Starlette）運作的原理，也讓它擁有如此驚人的效能。

## 非常技術性的細節

/// warning

你大概可以跳過這段。

這裡是有關 FastAPI 內部技術細節。

如果你有相當多的技術背景（例如協程、執行緒、阻塞等），並且對 FastAPI 如何處理 `async def` 與常規 `def` 感到好奇，請繼續閱讀。

///

### 路徑操作函数

當你使用 `def` 而不是 `async def` 宣告*路徑操作函式*時，該函式會在外部的執行緒池（threadpool）中執行，然後等待結果，而不是直接呼叫（因為這樣會阻塞伺服器）。

如果你來自於其他不以這種方式運作的非同步框架，而且你習慣於使用普通的 `def` 定義僅進行簡單計算的*路徑操作函式*，目的是獲得微小的性能增益（大約 100 奈秒），請注意，在 FastAPI 中，效果會完全相反。在這些情況下，最好使用 `async def`除非你的*路徑操作函式*執行阻塞的 <abbr title="輸入/輸出：磁碟讀寫或網路通訊">I/O</abbr> 的程式碼。

不過，在這兩種情況下，**FastAPI** [仍然很快](index.md#_11){.internal-link target=_blank}至少與你之前的框架相當（或者更快）。

### 依賴項(Dependencies)

同樣適用於[依賴項](tutorial/dependencies/index.md){.internal-link target=_blank}。如果依賴項是一個標準的 `def` 函式，而不是 `async def`，那麼它在外部的執行緒池被運行。

### 子依賴項

你可以擁有多個相互依賴的依賴項和[子依賴項](tutorial/dependencies/sub-dependencies.md){.internal-link target=_blank} （作為函式定義的參數），其中一些可能是用 `async def` 宣告，也可能是用 `def` 宣告。它們仍然可以正常運作，用 `def` 定義的那些將會在外部的執行緒中呼叫（來自執行緒池），而不是被「等待」。

### 其他輔助函式

你可以直接呼叫任何使用 `def` 或 `async def` 建立的其他輔助函式，FastAPI 不會影響你呼叫它們的方式。

這與 FastAPI 為你呼叫*路徑操作函式*和依賴項的邏輯有所不同。

如果你的輔助函式是用 `def` 宣告的，它將會被直接呼叫（按照你在程式碼中撰寫的方式），而不是在執行緒池中。如果該函式是用 `async def` 宣告，那麼你在呼叫時應該使用 `await` 等待其結果。

---

再一次強調，這些都是非常技術性的細節，如果你特地在尋找這些資訊，這些內容可能會對你有幫助。

否則，只需遵循上面提到的指引即可：<a href="#_1">趕時間嗎?</a>.
