# 关于 HTTPS

不少人会想当然地认为 HTTPS 只涉及**启用**和**禁用**。

但其实 HTTPS 要复杂得多。

!!! tip "提示"

    如果您时间紧或不在意，请继续阅读下一节，了解如何使用不同技术分步设置所有部署操作。

从消费者角度了解 HTTPS 的基础知识，请参阅 <a href="https://howhttps.works/" class="external-link" target="_blank">https://howhttps.works/。</a>

现在，从开发者角度介绍 HTTPS 的一些知识要点：

* 对于 HTTPS，服务器需要有第三方生成的**证书**
    * 这些证书实际上是从第三方获得的，而不是**生成**的
* 证书有生命周期
    * 证书会过期
    * 过期后，需要重新从第三方获取更新的证书
* 在 TCP 层进行连接加密
    * TCP 在 HTTP 之下
    * 因此，证书与加密是在 HTTP 之前处理完成的
* TCP 不关心**域**，只关注 IP 地址
    * 有关请求的特定域的信息在 HTTP 数据里
* HTTPS 证书**验证**某个域，但在知道处理哪个域之前，协议与加密就发生在 TCP 层了
* 默认情况下，每个 IP 地址只能有一个 HTTPS 证书
    * 不论服务器有多大，或每个应用有多小
    * 只有一种解决方案
* TLS 协议（在 HTTP 前，用于在 TCP 层处理加密的协议）支持 <a href="https://en.wikipedia.org/wiki/Server_Name_Indication" class="external-link" target="_blank"><abbr title="Server Name Indication">SNI</abbr></a> 扩展
    * SNI 扩展允许让一台服务器（只有单个 IP 地址）拥有多个 HTTPS 证书并服务多个 HTTPS 域/应用
    * 为此，运行在服务器上的，监听公共 IP 地址的单个组件（程序）必须具有服务器里的全部 HTTPS 证书
* 获得安全连接后，通信协议仍是 HTTP
    * 即便由 HTTP 协议发送，这些组件也是加密的

在服务器（机器、主机等）上运行程序/HTTP 服务器，并管理所有 HTTPS 组件是一种常见的做法：把解密的 HTTP 请求发送至运行同一个服务器（本例中是 **FastAPI** 应用）的实际 HTTP 应用，从应用中获取 HTTP 响应，使用适当的证书加密，再使用 HTTPS 把它发送回客户端。这种服务器就是常说的 <a href="https://en.wikipedia.org/wiki/TLS_termination_proxy" class="external-link" target="_blank">TLS 终止代理</a>。

## Let's Encrypt

在 Let's Encrypt 之前， HTTPS 证书是由值得信赖的第三方出售的。

但获取证书的手续十分繁杂，还要做很多书面工作，证书也十分昂贵。

但后来 <a href="https://letsencrypt.org/" class="external-link" target="_blank">Let's Encrypt</a> 横空出世了。

它是 Linux 基金会的项目，自动提供免费 HTTPS 证书。这些证书使用了所有标准安全加密措施，生命周期也很短（约 3 个月），因为生命周期短，实际上反而更安全。

域经过安全验证，证书是自动生成的，因此可以自动更新证书。

它的思路是自动获取并更新证书，这样一来，您就可以永久免费使用安全的 HTTPS 了。
