# 严格的 Content-Type 检查 { #strict-content-type-checking }

默认情况下，FastAPI 对 JSON 请求体使用严格的 `Content-Type` 头检查。这意味着，JSON 请求必须包含有效的 `Content-Type` 头（例如 `application/json`），其请求体才会被按 JSON 解析。

## CSRF 风险 { #csrf-risk }

此默认行为在一个非常特定的场景下，可防御一类跨站请求伪造（CSRF）攻击。

这类攻击利用了浏览器的一个事实：当请求满足以下条件时，浏览器允许脚本在不进行任何 CORS 预检的情况下直接发送请求：

- 没有 `Content-Type` 头（例如使用 `fetch()` 携带 `Blob` 作为 body）
- 且不发送任何认证凭据。

这种攻击主要在以下情况下相关：

- 应用在本地（如 `localhost`）或内网中运行
- 且应用没有任何认证，假定来自同一网络的请求都可信。

## 攻击示例 { #example-attack }

假设你构建了一个本地运行的 AI 代理。

它提供了一个 API，地址为

```
http://localhost:8000/v1/agents/multivac
```

另有一个前端，地址为

```
http://localhost:8000
```

/// tip | 提示

注意它们的主机相同。

///

之后，你可以通过前端让该 AI 代理替你执行操作。

由于它在本地运行、而非暴露在开放的互联网，你决定不配置任何认证，只信任对本地网络的访问。

于是，你的某位用户安装并在本地运行了它。

然后他（她）可能会打开一个恶意网站，例如

```
https://evilhackers.example.com
```

该恶意网站使用 `fetch()` 携带 `Blob` 作为 body，向本地 API 发送请求，地址为

```
http://localhost:8000/v1/agents/multivac
```

尽管恶意网站与本地应用的主机不同，浏览器仍不会触发 CORS 预检请求，原因是：

- 请求不涉及任何认证，无需发送凭据。
- 浏览器认为它并未发送 JSON（因为缺少 `Content-Type` 头）。

于是，该恶意网站就可能让本地 AI 代理替用户向前老板发送愤怒消息……甚至更糟。😅

## 开放的互联网 { #open-internet }

如果你的应用部署在开放的互联网，你不会“信任网络”，也不会允许任何人不经认证就发送特权请求。

攻击者完全可以直接运行脚本向你的 API 发送请求，无需借助浏览器交互，因此你很可能已经对任何特权端点做好了安全防护。

在这种情况下，以上攻击/风险不适用于你。

该风险/攻击主要发生在应用运行于本地网络、且“仅依赖网络隔离作为保护”的场景。

## 允许无 Content-Type 的请求 { #allowing-requests-without-content-type }

如果你需要兼容不发送 `Content-Type` 头的客户端，可以通过设置 `strict_content_type=False` 来关闭严格检查：

{* ../../docs_src/strict_content_type/tutorial001_py310.py hl[4] *}

启用该设置后，缺少 `Content-Type` 头的请求其请求体也会按 JSON 解析，这与旧版本 FastAPI 的行为一致。

/// info | 信息

此行为和配置在 FastAPI 0.132.0 中新增。

///
