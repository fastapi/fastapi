# HTTP 基础授权

最简单的用例是使用 HTTP 基础授权（HTTP Basic Auth）。

在 HTTP 基础授权中，应用需要请求头包含用户名与密码。

如果没有接收到 HTTP 基础授权，就返回 HTTP 401 `"Unauthorized"` 错误。

并返回含 `Basic` 值的请求头 `WWW-Authenticate`以及可选的 `realm` 参数。

HTTP 基础授权让浏览器显示内置的用户名与密码提示。

输入用户名与密码后，浏览器会把它们自动发送至请求头。

## 简单的 HTTP 基础授权

* 导入 `HTTPBasic` 与 `HTTPBasicCredentials`
* 使用 `HTTPBasic` 创建**安全概图**
* 在*路径操作*的依赖项中使用 `security`
* 返回类型为 `HTTPBasicCredentials` 的对象：
    * 包含发送的 `username` 与 `password`

{* ../../docs_src/security/tutorial006_an_py39.py hl[4,8,12] *}

第一次打开 URL（或在 API 文档中点击 **Execute** 按钮）时，浏览器要求输入用户名与密码：

<img src="/img/tutorial/security/image12.png">

## 检查用户名

以下是更完整的示例。

使用依赖项检查用户名与密码是否正确。

为此要使用 Python 标准模块 <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> 检查用户名与密码。

`secrets.compare_digest()` 需要仅包含 ASCII 字符（英语字符）的 `bytes` 或 `str`，这意味着它不适用于像`á`一样的字符，如 `Sebastián`。

为了解决这个问题，我们首先将 `username` 和 `password` 转换为使用 UTF-8 编码的 `bytes` 。

然后我们可以使用 `secrets.compare_digest()` 来确保 `credentials.username` 是 `"stanleyjobson"`，且 `credentials.password` 是`"swordfish"`。

{* ../../docs_src/security/tutorial007_an_py39.py hl[1,12:24] *}

这类似于：

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

但使用 `secrets.compare_digest()`，可以防御**时差攻击**，更加安全。

### 时差攻击

什么是**时差攻击**？

假设攻击者试图猜出用户名与密码。

他们发送用户名为 `johndoe`，密码为 `love123`  的请求。

然后，Python 代码执行如下操作：

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

但就在 Python 比较完 `johndoe` 的第一个字母 `j` 与 `stanleyjobson` 的 `s` 时，Python 就已经知道这两个字符串不相同了，它会这么想，**没必要浪费更多时间执行剩余字母的对比计算了**。应用立刻就会返回**错误的用户或密码**。

但接下来，攻击者继续尝试 `stanleyjobsox` 和 密码 `love123`。

应用代码会执行类似下面的操作：

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

此时，Python 要对比 `stanleyjobsox` 与 `stanleyjobson` 中的 `stanleyjobso`，才能知道这两个字符串不一样。因此会多花费几微秒来返回**错误的用户或密码**。

#### 反应时间对攻击者的帮助

通过服务器花费了更多微秒才发送**错误的用户或密码**响应，攻击者会知道猜对了一些内容，起码开头字母是正确的。

然后，他们就可以放弃 `johndoe`，再用类似 `stanleyjobsox` 的内容进行尝试。

#### **专业**攻击

当然，攻击者不用手动操作，而是编写每秒能执行成千上万次测试的攻击程序，每次都会找到更多正确字符。

但是，在您的应用的**帮助**下，攻击者利用时间差，就能在几分钟或几小时内，以这种方式猜出正确的用户名和密码。

#### 使用 `secrets.compare_digest()` 修补

在此，代码中使用了 `secrets.compare_digest()`。

简单的说，它使用相同的时间对比 `stanleyjobsox` 和 `stanleyjobson`，还有 `johndoe` 和 `stanleyjobson`。对比密码时也一样。

在代码中使用 `secrets.compare_digest()` ，就可以安全地防御全面攻击了。

### 返回错误

检测到凭证不正确后，返回 `HTTPException` 及状态码 401（与无凭证时返回的内容一样），并添加请求头 `WWW-Authenticate`，让浏览器再次显示登录提示：

{* ../../docs_src/security/tutorial007_an_py39.py hl[26:30] *}
