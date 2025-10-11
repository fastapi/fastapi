# Tệp tĩnh (Static Files)

Bạn có thể triển khai tệp tĩnh tự động từ một thư mục bằng cách sử dụng StaticFiles.

## Sử dụng `Tệp tĩnh`

- Nhập `StaticFiles`.
- "Mount" a `StaticFiles()` instance in a specific path.

{* ../../docs_src/static_files/tutorial001.py hl[2,6] *}

/// note | Chi tiết kỹ thuật

Bạn cũng có thể sử dụng `from starlette.staticfiles import StaticFiles`.

**FastAPI** cung cấp cùng `starlette.staticfiles` như `fastapi.staticfiles` giúp đơn giản hóa việc sử dụng, nhưng nó thực sự đến từ Starlette.

///

### "Mounting" là gì

"Mounting" có nghĩa là thêm một ứng dụng "độc lập" hoàn chỉnh vào một đường dẫn cụ thể, sau đó ứng dụng đó sẽ chịu trách nhiệm xử lý tất cả các đường dẫn con.

Điều này khác với việc sử dụng `APIRouter` vì một ứng dụng được gắn kết là hoàn toàn độc lập. OpenAPI và tài liệu từ ứng dụng chính của bạn sẽ không bao gồm bất kỳ thứ gì từ ứng dụng được gắn kết, v.v.

Bạn có thể đọc thêm về điều này trong [Hướng dẫn Người dùng Nâng cao](../advanced/index.md){.internal-link target=\_blank}.

## Chi tiết

Đường dẫn đầu tiên `"/static"` là đường dẫn con mà "ứng dụng con" này sẽ được "gắn" vào. Vì vậy, bất kỳ đường dẫn nào bắt đầu bằng `"/static"` sẽ được xử lý bởi nó.

Đường dẫn `directory="static"` là tên của thư mục chứa tệp tĩnh của bạn.

Tham số `name="static"` đặt tên cho nó để có thể được sử dụng bên trong **FastAPI**.

Tất cả các tham số này có thể khác với `static`, điều chỉnh chúng với phù hợp với ứng dụng của bạn.

## Thông tin thêm

Để biết thêm chi tiết và tùy chọn, hãy xem <a href="https://www.starlette.dev/staticfiles/" class="external-link" target="_blank">Starlette's docs about Static Files</a>.
