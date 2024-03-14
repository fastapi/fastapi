# StaticFiles

Bạn có thể tự động cung cấp các tệp tĩnh từ một thư mục bằng `StaticFiles`.

## Sử dụng `StaticFiles`

* Import `StaticFiles`.
* "Mount" một `StaticFiles()` instance trong một đường dẫn cụ thể.

```Python hl_lines="2  6"
{!../../../docs_src/static_files/tutorial001.py!}
```

!!! note "Chi tiết kỹ thuật"
    Bạn cũng có thể dùng `from starlette.staticfiles import StaticFiles`.

    **FastAPI** cung cấp `starlette.staticfiles` tương tự `fastapi.staticfiles` để thuận tiện hơn cho các lập trình viên. Tuy nhiên nó thực sự bắt nguồn từ Starlette.

### "Mounting" là gì

"Mounting" có nghĩ là thêm một ứng dụng "độc lập" hoàn chỉnh vào một đường dẫn cụ thể, sau đó sẽ xử lý tất cả các đường dẫn phụ.

Điều này khác với việc sử dụng `APIRouter` vì một ứng dụng được gắn kết hoàn toàn độc lập. OpenAPI và docs được tạo ra từ ứng dụng của bạn sẽ không bao gồm bất kỳ thứ gì từ ứng dụng được gắn kết, v.v.

You can read more about this in the [Advanced User Guide](../advanced/index.md){.internal-link target=_blank}.

## Cụ thể

Đường dẫn `"/static"` đầu tiên đề cập đến đường dẫn phụ mà "ứng dụng phụ" này sẽ được "gắn kết" vào. Vì vậy, bất kỳ đường dẫn nào bắt đầu bằng `"/static"` sẽ được nó xử lý.

`directory="static"` đề cập đến tên của thư mục chứa các tệp tĩnh của bạn.

`name="static"` đặt cho nó một tên mà **FastAPI** có thể sử dụng nội bộ.

Tất cả các tham số này có thể khác với "`static`, hãy điều chỉnh chúng theo nhu cầu và chi tiết cụ thể của ứng dụng của bạn.

## Tìm hiểu thêm

Để biết thêm chi tiết và tùy chọn, hãy xem <a href="https://www.starlette.io/staticfiles/" class="external-link" target="_blank">Tài liệu của Starlette về Tệp tĩnh</a>.
