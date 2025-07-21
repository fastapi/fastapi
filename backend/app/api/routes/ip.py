import ipaddress
from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response

from app.api.deps import CurrentUser

router = APIRouter(prefix="/ip", tags=["ip"])


@router.get("/", response_model=dict)
@router.get("", response_model=dict)
async def get_client_ip(request: Request):
    """
    获取客户端IP地址

    返回客户端的公网IP地址，通常是通过代理转发的X-Forwarded-For头获取
    """
    # 尝试从各种HTTP头获取IP地址
    client_ip = _extract_client_ip(request)

    return {"ip": client_ip}


@router.get("/text/", response_class=Response)
async def get_client_ip_text(request: Request):
    """
    获取客户端IP地址（纯文本格式）

    返回客户端的公网IP地址，以纯文本格式
    """
    # 尝试从各种HTTP头获取IP地址
    client_ip = _extract_client_ip(request)

    return Response(content=client_ip, media_type="text/plain")


@router.get("/headers/", response_model=dict)
async def get_request_headers(request: Request):
    """
    获取请求的所有头信息

    返回包含所有HTTP请求头的字典
    """
    return {"headers": dict(request.headers)}


# 示例：添加需要登录的IP端点
@router.get("/secure/", response_model=dict)
async def get_secure_ip(request: Request, current_user: CurrentUser):
    """
    获取客户端IP地址（需要登录）

    这是一个需要用户登录的示例端点
    """
    client_ip = _extract_client_ip(request)

    return {
        "ip": client_ip,
        "user_id": str(current_user.id),
        "user_email": current_user.email,
    }


@router.get("/analyze/{ip_address}", response_model=dict[str, Any])
async def analyze_ip(ip_address: str):
    """
    分析指定的IP地址

    返回IP地址的基本信息，如版本、是否私有等
    """
    try:
        ip = ipaddress.ip_address(ip_address)

        result = {
            "ip": str(ip),
            "version": f"IPv{ip.version}",
            "is_private": ip.is_private,
            "is_global": ip.is_global,
            "is_multicast": ip.is_multicast,
            "is_loopback": ip.is_loopback,
            "is_link_local": ip.is_link_local,
        }

        # IPv6特有属性
        if ip.version == 6:
            ipv6 = ipaddress.IPv6Address(ip_address)
            result.update(
                {
                    "is_site_local": ipv6.is_site_local,
                    "ipv4_mapped": ipv6.ipv4_mapped is not None,
                    "teredo": ipv6.teredo is not None,
                    "sixtofour": ipv6.sixtofour is not None,
                }
            )

        # 尝试获取反向DNS查询名称
        try:
            import socket

            result["reverse_pointer"] = socket.gethostbyaddr(ip_address)[0]
        except (socket.herror, socket.gaierror):
            result["reverse_pointer"] = None

        return result
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的IP地址: {ip_address}")


def _extract_client_ip(request: Request) -> str:
    """
    从请求中提取客户端IP地址

    按照优先级尝试从不同的HTTP头获取
    """
    # 检查常见的代理头
    for header in [
        "X-Forwarded-For",
        "X-Real-IP",
        "CF-Connecting-IP",  # Cloudflare
        "True-Client-IP",  # Akamai/Cloudflare
        "X-Client-IP",
    ]:
        if header_value := request.headers.get(header):
            # 如果是X-Forwarded-For，可能包含多个IP，取第一个
            if header == "X-Forwarded-For" and "," in header_value:
                return header_value.split(",")[0].strip()
            return header_value.strip()

    # 如果没有代理头，使用直接连接的客户端地址
    return request.client.host if request.client else "unknown"
