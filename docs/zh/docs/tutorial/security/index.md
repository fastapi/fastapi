# 安全 - 简介

处理安全、身份验证和授权的方式很多。

一般来说，处理安全是比较繁难的工作。

许多框架或系统处理安全和身份验证都需要费时费力编写大量代码，有时安全代码甚至会超过代码总量的一半。

**FastAPI** 则提供了众多工具，开发者无需研习各种安全规范，就能轻松、快速地以标准的方式实现**安全**机制。

首先，我们来了解一些安全方面的基本概念。

## 不想浪费时间？

如果对以下术语不感兴趣，*现在*只想以用户名和密码作为安全机制进行身份验证，您可以跳过下面的内容，直接阅读下一章。

## OAuth2

OAuth2 是定义了多种身份验证和授权方式的规范。

它定义了诸多规范，且涵盖了许多复杂用例。

还包括各种**第三方**身份验证的方法。

这就是脸书、谷歌、推特、GitHub 等第三方平台登录后台使用的机制。

### OAuth 1

OAuth 1 与 OAuth2 完全不同，它更复杂，而且直接包含了加密通信的规范。

OAuth 1 现在已经没什么人用了。

OAuth2 没有指定如何加密通信，而是要求应用使用 HTTPS 进行通信。

!!! tip "提示"

    **部署**一章将介绍如何使用 Traefik 和 Let's Encrypt 免费设置 HTTPS。


## OpenID Connect

OpenID Connect 是基于 **OAuth2** 的另一个规范。

它只是扩展了 OAuth2，明确了一些在 OAuth2 中相对模糊的内容，使其更具互操作性。

例如，谷歌登录使用的就是 OpenID Connect（底层使用 OAuth2）。

脸书没有使用 OpenID Connect 登录，而是基于 OAuth2 进行了定制。

### OpenID（非**OpenID Connect**）

**OpenID**也是一种规范。它要解决的问题与 **OpenID Connect** 相同，但不是基于 OAuth2。

OpenID 曾是一个完整的附属系统。

但现在也已经没什么人用了。

## OpenAPI

OpenAPI（曾用名为 Swagger）是构建 API 的开放规范（现为 Linux Foundation 的组件）。

**FastAPI** 基于 **OpenAPI**。

正因如此，FastAPI 才具备了 API 文档和代码生成等功能。

OpenAPI 定义了多种安全**方案**。

使用这些安全方案，开发者可以享受包括 API 文档在内的标准工具带来的所有优势。

OpenAPI 定义了以下安全方案：

* `apiKey`：从以下几个来源获取应用的指定密钥：
    * 查询参数
    * 请求头
    * cookie
* `http`：标准的 HTTP 身份验证系统，包括：
    * `bearer`：继承自 OAuth2，值为 `Bearer` 加 Token 字符串的 `Authorization` 请求头
    * HTTP Basic 验证方式
    * HTTP Digest 等
* `oauth2`：OAuth2 处理安全的所有方法（称为**流**）
    * 以下是几种构建谷歌、脸书、推特、GitHub 等 OAuth 2.0 第三方身份验证应用的流：
        * `implicit`
        * `clientCredentials`
        * `authorizationCode`
    * 但是，有一个特定**流**可以完美地用于直接在应用程序中处理身份验证：
        * `password`：后续章主要介绍密码流示例
* `openIdConnect`：定义了自动发现 OAuth2 身份验证数据的方法
    * 自动发现机制是在 OpenID Connect 规范中定义的



!!! tip "提示"

    集成其它类似谷歌、脸书、推特、GitHub 等第三方身份验证/授权身份验证应用也是可能的，而且不难。
    
    创建类似于上述身份验证/授权的应用是最复杂的问题，**FastAPI** 提供了相应的工具，完成了最繁重的工作，让开发者可以轻松地创建新的身份验证/授权应用。

## **FastAPI** 实用工具

FastAPI 在 `fastapi.security` 模块中为每种安全方案都提供了多种工具，这些工具让安全机制用起来更加简单。

下一章，将介绍如何使用 **FastAPI** 的工具为 API 增加安全机制。

此外，还会介绍如何把安全机制自动集成至 API 文档。