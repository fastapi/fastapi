# CORS (Cross-Origin Resource Sharing)

<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">CORS hay "Cross-Origin Resource Sharing"</a> để chỉ trường hợp khi một frontend chạy trong trình duyệt có đoạn mã JavaScript tương tác với một backend, và backend ở trong một "origin" khác với frontend.

## Origin

Một origin là sự kết hợp của giao thức (protocol) (`http`, `https`), tên miền (domain) (`myapp.com`, `localhost`, `localhost.tiangolo.com`), và cổng (port) (`80`, `443`, `8080`).

Vì vậy, tất cả những thứ dưới đây đều là các origin khác nhau:

* `http://localhost`
* `https://localhost`
* `http://localhost:8080`

Kể cả khi chúng đều là `localhost`, chúng sử dụng các giao thức khác nhau hoặc cổng khác nhau, vì vậy, chúng là các origin khác nhau.

## Các bước

Giả sử bạn có một frontend chạy trong trình duyệt của bạn tại `http://localhost:8080`, và đoạn mã JavaScript của nó đang cố gắng giao tiếp với một backend chạy tại `http://localhost` (vì chúng ta không chỉ định cổng, trình duyệt sẽ giả sử cổng mặc định `80`).

Khi đó, trình duyệt sẽ gửi một HTTP `OPTIONS` request đến backend tại `:80`, và nếu backend gửi các header phù hợp chứng thực việc giao tiếp từ origin khác (`http://localhost:8080`) thì trình duyệt tại `:8080` sẽ cho phép đoạn mã JavaScript trong frontend gửi request đến backend `:80`.

Để có được điều này, backend tại `:80` phải có một danh sách các "allowed origins".

Trong trường hợp này, danh sách đó phải bao gồm `http://localhost:8080` để frontend tại `:8080` để hoạt động chính xác.

## Wildcards

Bạn hoàn toàn có thể chỉ định danh sách như `"*"` để cho phép tất cả.

Nhưng điều đó chỉ cho phép một số loại giao tiếp, loại bỏ tất cả những thứ liên quan đến việc xác thực: Cookies, các header như `Authorization` được sử dụng với Bearer Tokens, v.v.

Vì vậy, để mọi thứ hoạt động trơn tru, tốt hơn hết là chỉ định danh sách các origin rõ ràng.

## Sử dụng `CORSMiddleware`

Bạn có thể cấu hình nó trong ứng dụng **FastAPI** của bạn bằng cách sử dụng `CORSMiddleware`.

* Import `CORSMiddleware`.
* Tạo danh sách các origin cho phép (dưới dạng chuỗi).
* Thêm nó vào "middleware" của ứng dụng **FastAPI** của bạn.

Bạn cũng có thể chỉ định backend của mình cho phép:

* Credentials (Authorization headers, Cookies, etc).
* Các phương thức HTTP cụ thể (`POST`, `PUT`) hoặc tất cả chúng với wildcard `"*"`.
* Các header HTTP cụ thể hoặc tất cả chúng với wildcard `"*"`.

{* ../../docs_src/cors/tutorial001.py hl[2,6:11,13:19] *}

Các tham số mặc định của `CORSMiddleware` được thiết lập theo hướng hạn chế tối đa, vì vậy để cho phép trình duyệt thực hiện các yêu cầu từ domain khác, bạn cần chỉ định rõ những origin, phương thức, hoặc header nào được phép sử dụng.

Các tham số sau được hỗ trợ:

* `allow_origins` - Danh sách các origin mà nên được phép thực hiện các request cross-origin. Ví dụ: `['https://example.org', 'https://www.example.org']`. Bạn có thể sử dụng `['*']` để cho phép bất kỳ origin nào.
* `allow_origin_regex` - Một chuỗi regex để khớp với các origin mà nên được phép thực hiện các request cross-origin. Ví dụ: `'https://.*\.example\.org'`.
* `allow_methods` - Danh sách các phương thức HTTP mà nên được phép cho các request cross-origin. Mặc định là `['GET']`. Bạn có thể sử dụng `['*']` để cho phép tất cả các phương thức chuẩn.
* `allow_headers` - Danh sách các header request HTTP mà nên được hỗ trợ cho các request cross-origin. Mặc định là `[]`. Bạn có thể sử dụng `['*']` để cho phép tất cả các header. Các header `Accept`, `Accept-Language`, `Content-Language` và `Content-Type` luôn được phép cho các request CORS đơn giản.
* `allow_credentials` - Chỉ định rằng cookies nên được hỗ trợ cho các request cross-origin. Mặc định là `False`. Ngoài ra, `allow_origins` không thể được đặt thành `['*']` để cho phép credentials, origins phải được chỉ định.
* `expose_headers` - Chỉ định bất kỳ header response nào mà nên được làm truy cập được cho trình duyệt. Mặc định là `[]`.
* `max_age` - Đặt một thời gian tối đa tính bằng giây cho trình duyệt để cache các response CORS. Mặc định là `600`.

Middleware này phản hồi cho hai loại request HTTP cụ thể...

### CORS preflight requests

Đây là bất kỳ `OPTIONS` request với các header `Origin` và `Access-Control-Request-Method`.

Trong trường hợp này, middleware sẽ chặn request đến và phản hồi với các header CORS thích hợp, và một `200` hoặc `400` response cho mục đích thông tin.

### Simple requests

Bất kỳ request nào với header `Origin`. Trong trường hợp này, middleware sẽ chuyển tiếp request như bình thường, nhưng sẽ bao gồm các header CORS thích hợp trên response.

## Thông tin thêm

Để biết thêm thông tin về <abbr title="Cross-Origin Resource Sharing">CORS</abbr>, tham khảo <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS" class="external-link" target="_blank">tài liệu CORS của Mozilla</a>.

/// note | Chi tiết kỹ thuật

Bạn cũng có thể sử dụng `from starlette.middleware.cors import CORSMiddleware`.

**FastAPI** cung cấp nhiều middleware trong `fastapi.middleware` chỉ để thuận tiện hơn cho bạn, các lập trình viên. Thực ra hầu hết các middleware có sẵn đến từ Starlette.

///
