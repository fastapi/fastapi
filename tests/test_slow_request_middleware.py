import asyncio
import logging
import time

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/fast")
async def fast_endpoint():
    return {"message": "Fast response"}


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(0.6)
    return {"message": "Slow response"}


def test_slow_request_logging(caplog):
    caplog.set_level(logging.WARNING)
    client = TestClient(app)

    # 测试快速请求，不应记录警告
    response = client.get("/fast")
    assert response.status_code == 200
    assert "Slow request" not in caplog.text

    # 测试慢速请求，应记录警告
    response = client.get("/slow")
    assert response.status_code == 200

    # 检查日志是否包含预期的警告信息
    slow_request_logs = [record for record in caplog.records if "Slow request" in record.message]
    assert len(slow_request_logs) == 1

    log_message = slow_request_logs[0].message
    assert "GET" in log_message
    assert "/slow" in log_message
    # 检查是否包含两位小数的时间
    import re
    match = re.search(r"took (\d+\.\d{2})s", log_message)
    assert match is not None, f"Log message should contain time with two decimal places: {log_message}"

    print("✅ 慢请求监控中间件测试通过！")
    print(f"   日志消息: {log_message}")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
