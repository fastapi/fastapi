# FastAPI CLI

**FastAPI CLI** là một chương trình dòng lệnh có thể được sử dụng để phục vụ ứng dụng FastAPI của bạn, quản lý dự án FastAPI của bạn và nhiều hoạt động khác.

Khi bạn cài đặt FastAPI (vd với `pip install "fastapi[standard]"`), nó sẽ bao gồm một gói được gọi là `fastapi-cli`, gói này cung cấp lệnh `fastapi` trong terminal.

Để chạy ứng dụng FastAPI của bạn cho quá trình phát triển (development), bạn có thể sử dụng lệnh `fastapi dev`:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Chương trình dòng lệnh `fastapi` là **FastAPI CLI**.

FastAPI CLI nhận đường dẫn đến chương trình Python của bạn (vd `main.py`) và tự động phát hiện đối tượng `FastAPI` (thường được gọi là `app`), xác định quá trình nhập đúng, và sau đó chạy nó (serve).

Đối với vận hành thực tế (production), bạn sẽ sử dụng `fastapi run` thay thế. 🚀

Ở bên trong, **FastAPI CLI** sử dụng <a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a>, một server ASGI có hiệu suất cao, sẵn sàng cho vận hành thực tế (production). 😎

## `fastapi dev`

Chạy `fastapi dev` sẽ khởi động quá trình phát triển.

Mặc định, **auto-reload** được bật, tự động tải lại server khi bạn thay đổi code của bạn. Điều này tốn nhiều tài nguyên và có thể kém ổn định hơn khi nó bị tắt. Bạn nên sử dụng nó cho quá trình phát triển. Nó cũng lắng nghe địa chỉ IP `127.0.0.1`, đó là địa chỉ IP của máy tính để tự giao tiếp với chính nó (`localhost`).

## `fastapi run`

Chạy `fastapi run` mặc định sẽ khởi động FastAPI cho quá trình vận hành thực tế.

Mặc định, **auto-reload** bị tắt. Nó cũng lắng nghe địa chỉ IP `0.0.0.0`, đó là tất cả các địa chỉ IP có sẵn, như vậy nó sẽ được truy cập công khai bởi bất kỳ ai có thể giao tiếp với máy tính. Đây là cách bạn thường chạy nó trong sản phẩm hoàn thiện, ví dụ trong một container.

Trong hầu hết các trường hợp, bạn sẽ (và nên) có một "proxy điểm cuối (termination proxy)" xử lý HTTPS cho bạn, điều này sẽ phụ thuộc vào cách bạn triển khai ứng dụng của bạn, nhà cung cấp có thể làm điều này cho bạn, hoặc bạn có thể cần thiết lập nó.

/// tip

Bạn có thể tìm hiểu thêm về FastAPI CLI trong [tài liệu triển khai](deployment/index.md){.internal-link target=_blank}.

///
