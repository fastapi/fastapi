# 手动部署

您也可以手动部署 **FastAPI**。

只要安装 Uvicorn 等 ASGI 兼容的服务器：

=== "Uvicorn"

    * <a href="https://www.uvicorn.org/" class="external-link" target="_blank">Uvicorn</a>，快如闪电的 ASGI 服务器，基于 uvloop 与 httptools 构建。
    
    <div class="termy">
    
    ```console
    $ pip install uvicorn[standard]
    
    ---> 100%
    ```
    
    </div>
    
    !!! tip "提示"
        添加 `standard` 后，Uvicorn 会安装并使用更多依赖项。
        
        包括 `uvloop`，它是 `asyncio` 的高性能替代方案，极大地提升了并发性能。

=== "Hypercorn"

    * <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>，与 HTTP/2 兼容的 ASGI 服务器。
    
    <div class="termy">
    
    ```console
    $ pip install hypercorn
    
    ---> 100%
    ```
    
    </div>
    
    ……或其它 ASGI 服务器。

以用户指南中介绍的方式运行应用，但不要使用 `--reload` 选项，例如：

=== "Uvicorn"

    <div class="termy">
    
    ```console
    $ uvicorn main:app --host 0.0.0.0 --port 80
    
    <span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
    ```
    
    </div>

=== "Hypercorn"

    <div class="termy">
    
    ```console
    $ hypercorn main:app --bind 0.0.0.0:80
    
    Running on 0.0.0.0:8080 over http (CTRL + C to quit)
    ```
    
    </div>

如果需要使用工具设置停止服务后自动重启。

建议安装 <a href="https://gunicorn.org/" class="external-link" target="_blank">Gunicorn</a>， <a href="https://www.uvicorn.org/#running-with-gunicorn" class="external-link" target="_blank">用它作为 Uvicorn 的管理器 </a>，或使用支持多个 worker 的 Hypercorn。

一定要校准好 worker 的数量。

但这么做时最好使用 Docker 镜像，自动完成这些操作。
