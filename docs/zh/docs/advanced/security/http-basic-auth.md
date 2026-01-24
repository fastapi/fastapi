# HTTP 基础授权 { #http-basic-auth }

对于最简单的用例，你可以使用 HTTP 基础授权（HTTP Basic Auth）。

在 HTTP 基础授权中，应用会期望有一个包含用户名和密码的请求头。

如果没有接收到它，就会返回 HTTP 401 `"Unauthorized"` 错误。

并返回请求头 `WWW-Authenticate`，其值为 `Basic`，以及可选的 `realm` 参数。

这会让浏览器显示内置的用户名和密码提示框。

然后，当你输入用户名和密码时，浏览器会自动把它们发送到请求头中。

## 简单的 HTTP 基础授权 { #simple-http-basic-auth }

* 导入 `HTTPBasic` 和 `HTTPBasicCredentials`。
* 使用 `HTTPBasic` 创建一个 "`security` scheme"。
* 在你的 *路径操作* 中，通过依赖项使用该 `security`。
* 它会返回一个类型为 `HTTPBasicCredentials` 的对象：
    * 它包含发送的 `username` 和 `password`。

{* ../../docs_src/security/tutorial006_an_py39.py hl[4,8,12] *}

当你第一次尝试打开该 URL（或在文档中点击 "Execute" 按钮）时，浏览器会要求你输入用户名和密码：

<img src="/img/tutorial/security/image12.png">

## 检查用户名 { #check-the-username }

以下是更完整的示例。

使用依赖项检查用户名和密码是否正确。

为此，使用 Python 标准模块 <a href="https://docs.python.org/3/library/secrets.html" class="external-link" target="_blank">`secrets`</a> 来检查用户名和密码。

`secrets.compare_digest()` 需要接收仅包含 ASCII 字符（英语字符）的 `bytes` 或 `str`，这意味着它不能处理像 `Sebastián` 里的 `á` 这样的字符。

为了解决这个问题，我们首先将 `username` 和 `password` 转换为使用 UTF-8 编码的 `bytes`。

然后我们可以使用 `secrets.compare_digest()` 来确保 `credentials.username` 是 `"stanleyjobson"`，并且 `credentials.password` 是 `"swordfish"`。

{* ../../docs_src/security/tutorial007_an_py39.py hl[1,12:24] *}

这类似于：

```Python
if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # Return some error
    ...
```

但是，通过使用 `secrets.compare_digest()`，它将对一种称为 “timing attacks” 的攻击方式是安全的。

### 时差攻击 { #timing-attacks }

但什么是 “timing attack”？

让我们想象一些攻击者正在尝试猜测用户名和密码。

他们发送了一个用户名为 `johndoe`、密码为 `love123` 的请求。

那么，你的应用中的 Python 代码就等同于类似下面这样：

```Python
if "johndoe" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

但当 Python 将 `johndoe` 的第一个 `j` 与 `stanleyjobson` 的第一个 `s` 进行比较时，就会返回 `False`，因为它已经知道这两个字符串不相同，于是会认为“没必要浪费更多计算去比较剩余的字母”。然后你的应用会提示“用户名或密码不正确”。

但接下来攻击者会尝试用户名 `stanleyjobsox`、密码 `love123`。

而你的应用代码会执行类似下面的操作：

```Python
if "stanleyjobsox" == "stanleyjobson" and "love123" == "swordfish":
    ...
```

Python 必须对比 `stanleyjobsox` 和 `stanleyjobson` 中完整的 `stanleyjobso`，才能意识到这两个字符串不相同。因此，它会多花费几微秒来回复“用户名或密码不正确”。

#### 响应时间会帮助攻击者 { #the-time-to-answer-helps-the-attackers }

在这个时候，通过注意到服务器发送“用户名或密码不正确”的响应多花了几微秒，攻击者就会知道他们有 _某些_ 内容猜对了，开头的一些字母是正确的。

然后他们就可以再次尝试，并且知道它很可能比 `johndoe` 更接近 `stanleyjobsox`。

#### “专业”的攻击 { #a-professional-attack }

当然，攻击者不会手动进行这些尝试，他们会编写程序来做，可能每秒执行成千上万次或数百万次测试，并且每次只多猜对一个字母。

但这样做，在几分钟或几小时内，攻击者就能猜出正确的用户名和密码，在我们的应用“帮助”下，仅仅通过响应所用的时间。

#### 用 `secrets.compare_digest()` 修复 { #fix-it-with-secrets-compare-digest }

但在我们的代码中，实际上使用了 `secrets.compare_digest()`。

简而言之，它比较 `stanleyjobsox` 与 `stanleyjobson` 所需的时间，会与比较 `johndoe` 与 `stanleyjobson` 所需的时间相同。对密码也是如此。

这样，在你的应用代码中使用 `secrets.compare_digest()`，就能在这一整类安全攻击面前保持安全。

### 返回错误 { #return-the-error }

在检测到凭证不正确后，返回一个状态码为 401 的 `HTTPException`（与未提供凭证时返回的内容相同），并添加请求头 `WWW-Authenticate`，让浏览器再次显示登录提示框：

{* ../../docs_src/security/tutorial007_an_py39.py hl[26:30] *}
