# Middleware

Bạn có thể thêm middleware vào ứng dụng **FastAPI**.

Một "middleware" là một hàm mà làm việc với mỗi **request** trước khi nó được xử lý bởi bất kỳ *path operation* nào. Đồng thời cũng tương tự với mỗi **response** trước khi trả về.

* Nó tiếp nhận mỗi **request** mà đến ứng dụng của bạn.
* Nó có thể thực hiện một số thay đổi với **request** hoặc chạy một số đoạn mã cần thiết.
* Nó sau đó chuyển tiếp **request** để phần còn lại của ứng dụng xử lí (bởi một *path operation* nào đó).
* Nó tiếp nhận **response** được tạo ra bởi ứng dụng (bởi một *path operation* nào đó).
* Nó có thể thực hiện một số thay đổi với **response** hoặc chạy một số đoạn mã cần thiết.
* Sau đó nó trả về **response**.

/// note | Chi tiết kỹ thuật

Nếu bạn có dependencies với `yield`, mã thoát sẽ chạy *sau* middleware.

Nếu có bất kỳ task nền (sẽ được thêm vào tài liệu sau), chúng sẽ chạy *sau* tất cả middleware.

///

## Tạo một middleware

Để tạo một middleware, bạn dùng decorator `@app.middleware("http")` phía trên một hàm.

Middleware nhận:

* `request`.
* Một hàm `call_next` sẽ nhận `request` làm tham số.
    * Hàm này sẽ chuyển tiếp `request` đến *path operation* tương ứng.
    * Sau đó nó trả về `response` được tạo ra bởi *path operation* tương ứng.
* Bạn có thể chỉnh sửa thêm `response` trước khi trả về.

{* ../../docs_src/middleware/tutorial001.py hl[8:9,11,14] *}

/// tip

Lưu ý rằng các header tùy chỉnh có thể được thêm bằng cách<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">sử dụng tiền tố 'X-'</a>.

Nhưng nếu bạn có header tùy chỉnh mà bạn muốn một client trong trình duyệt có thể thấy, bạn cần thêm chúng vào cấu hình CORS ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank}) bằng tham số `expose_headers` được tài liệu trong <a href="https://www.starlette.io/middleware/#corsmiddleware" class="external-link" target="_blank">Starlette's CORS docs</a>.

///

/// note | Chi tiết kỹ thuật

Bạn cũng có thể sử dụng `from starlette.requests import Request`.

**FastAPI** cung cấp nó như một tiện ích cho bạn, lập trình viên. Nhưng nó đến trực tiếp từ Starlette.

///

### Trước và sau `response`

Bạn có thể thêm mã để chạy với `request`, trước khi bất kỳ *path operation* nào nhận được nó.
Bạn cũng có thể làm điều tương tự với `response` sau khi nó được tạo ra, trước khi trả nó về.
Ví dụ, bạn có thể thêm một header tùy chỉnh `X-Process-Time` chứa thời gian tính bằng giây mà nó đã mất để xử lí request và tạo ra response:

{* ../../docs_src/middleware/tutorial001.py hl[10,12:13] *}

/// tip

Ở đây chúng ta sử dụng <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> thay vì `time.time()` vì nó chính xác hơn cho các trường hợp này. 🤓

///

## Các middleware khác

Bạn có thể đọc thêm về các middleware khác trong [Hướng dẫn sử dụng nâng cao: Middleware nâng cao](../advanced/middleware.md){.internal-link target=_blank}.

Bạn sẽ đọc về cách xử lí <abbr title="Cross-Origin Resource Sharing">CORS</abbr> với một middleware trong phần tiếp theo.
