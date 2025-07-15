# Metadata và URLs tài liệu

Bạn hoàn toàn có thể tùy chỉnh các cấu hình metadata trong ứng dụng **FastAPI** của mình.

## Metadata cho API

Bạn có thể thiết lập các trường sau đây, chúng được sử dụng trong đặc tả OpenAPI và giao diện tài liệu API tự động:

| Tham số | Kiểu | Mô tả |
|------------|------|-------------|
| `title` | `str` | Tiêu đề của API. |
| `summary` | `str` | Tóm tắt ngắn gọn của API. <small>Đã có sẵn kể từ OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | Mô tả ngắn gọn của API. Nó có thể sử dụng Markdown. |
| `version` | `string` | Phiên bản của API. Đây là phiên bản từ ứng dụng của bạn, không phải của OpenAPI. Ví dụ: `2.5.0`. |
| `terms_of_service` | `str` | URL đến Điều khoản dịch vụ của API. Nếu cung cấp, trường này phải là URL. |
| `contact` | `dict` | Thông tin liên hệ cho API được cung cấp. Nó có thể bao gồm một số trường sau. <details><summary><code>contact</code> Các trường</summary><table><thead><tr><th>Tham số</th><th>Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>Tên nhận dạng của người liên hệ/tổ chức.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>URL chỉ đến thông tin liên hệ. PHẢI là định dạng URL.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>Địa chỉ email của người liên hệ/tổ chức. PHẢI là định dạng email.</td></tr></tbody></table></details> |
| `license_info` | `dict` | Thông tin chứng chỉ của API được cung cấp. Nó có thể bao gồm một số trường sau. <details><summary><code>license_info</code> Các trường</summary><table><thead><tr><th>Tham số</th><th>Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>BẮT BUỘC</strong> (Nếu có một <code>license_info</code> được thiết lập). Tên chứng chỉ của API được sử dụng.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>Một biểu thức giấy phép <a href="https://spdx.org/licenses/" class="external-link" target="blank">SPDX</a> cho API. Trường identifier và trường url loại trừ lẫn nhau (không thể dùng đồng thời). <small>Có sẵn từ OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>URL đến giấy phép được sử dụng cho API. PHẢI ở định dạng URL.</td></tr></tbody></table></details> |

Bạn có thể thiết lập chúng như sau:

{* ../../docs_src/metadata/tutorial001.py hl[3:16, 19:32] *}

/// tip

Bạn có thể viết Markdown trong trường `description` và nó sẽ được hiển thị ở giao diện tài liệu API tự động.

///

Với cấu hình này, giao diện tài liệu API tự động sẽ trông như thế này:

<img src="/img/tutorial/metadata/image01.png">

## License identifier

Kể từ OpenAPI 3.1.0 và FastAPI 0.99.0, bạn cũng có thể thiết lập `license_info` với `identifier` thay vì `url`.

Ví dụ:

{* ../../docs_src/metadata/tutorial001_1.py hl[31] *}

## Metadata cho tags

Bạn cũng có thể thêm metadata bổ sung cho các tags khác nhau được sử dụng để nhóm các path operations của bạn với tham số `openapi_tags`.

Nó lấy một danh sách chứa một dictionary cho mỗi tag.

Mỗi dictionary có thể chứa:

* `name` (**bắt buộc**): một `str` với tên tag giống như khi bạn sử dụng trong tham số `tags` của các *path operations* và `APIRouter`s.
* `description`: một `str` với mô tả ngắn cho tag. Nó có thể sử dụng Markdown và sẽ được hiển thị trong giao diện tài liệu.
* `externalDocs`: một `dict` mô tả tài liệu bên ngoài với:
    * `description`: một `str` với mô tả ngắn cho tài liệu bên ngoài.
    * `url` (**bắt buộc**): một `str` với URL cho tài liệu bên ngoài.

### Tạo metadata cho tags

Hãy thử điều đó trong ví dụ với tags `users` và `items`.

Tạo metadata cho tags và chuyển nó đến tham số `openapi_tags`:

{* ../../docs_src/metadata/tutorial004.py hl[3:16,18] *}

Lưu ý rằng bạn có thể sử dụng Markdown trong các mô tả, ví dụ "login" sẽ được hiển thị in đậm (**login**) và "fancy" sẽ được hiển thị in nghiêng (_fancy_).

/// tip

Bạn không cần thêm metadata cho tất cả các tags mà bạn sử dụng.

///

### Sử dụng tags của bạn

Sử dụng tham số `tags` với các *path operations* (và `APIRouter`s) để gán chúng cho các tags khác nhau:

{* ../../docs_src/metadata/tutorial004.py hl[21,26] *}

/// info

Đọc thêm về tag trong phần [Cấu hình Path Operations](path-operation-configuration.md#tags){.internal-link target=_blank}.

///

### Kiểm tra tài liệu

Bây giờ, nếu bạn kiểm tra tài liệu, chúng sẽ hiển thị tất cả các metadata bổ sung:

<img src="/img/tutorial/metadata/image02.png">

### Thứ tự của tags

Thứ tự của mỗi dictionary metadata tag cũng xác định thứ tự hiển thị trong giao diện tài liệu.

Ví dụ, mặc dù `users` sẽ đứng sau `items` theo thứ tự bảng chữ cái, nhưng nó được hiển thị trước chúng, vì chúng ta đã thêm metadata của chúng nó làm dictionary đầu tiên trong danh sách.

## URL OpenAPI

Mặc định, schema OpenAPI được phục vụ tại `/openapi.json`.

Nhưng bạn có thể cấu hình nó với tham số `openapi_url`.

Ví dụ, để đặt nó được phục vụ tại `/api/v1/openapi.json`:

{* ../../docs_src/metadata/tutorial002.py hl[3] *}

Nếu bạn muốn vô hiệu hóa hoàn toàn schema OpenAPI hoàn toàn, bạn có thể đặt `openapi_url=None`, điều đó cũng sẽ tắt các giao diện tài liệu sử dụng nó.

## URL tài liệu

Bạn có thể cấu hình hai giao diện tài liệu được tích hợp:

* **Swagger UI**: được phục vụ tại `/docs`.
    * Bạn có thể đặt URL của nó với tham số `docs_url`.
    * Bạn có thể vô hiệu hóa nó bằng cách đặt `docs_url=None`.
* **ReDoc**: được phục vụ tại `/redoc`.
    * Bạn có thể đặt URL của nó với tham số `redoc_url`.
    * Bạn có thể vô hiệu hóa nó bằng cách đặt `redoc_url=None`.

Ví dụ, để đặt Swagger UI được phục vụ tại `/documentation` và vô hiệu hóa ReDoc:

{* ../../docs_src/metadata/tutorial003.py hl[3] *}
